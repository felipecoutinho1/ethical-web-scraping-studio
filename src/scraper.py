"""Responsible scraper with allowlisting, robots.txt, limits and delays."""

from __future__ import annotations

from time import perf_counter, sleep
from typing import Callable
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.models import ScrapeResult, Source


USER_AGENT = "Ethical-Scraping-Studio-Portfolio/1.0"


class ScrapingError(RuntimeError):
    """A safe error raised by the scraping workflow."""


def validate_url(url: str, allowed_host: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != allowed_host or parsed.username or parsed.password:
        raise ScrapingError("The page is outside the allowlisted HTTPS source.")


def create_session() -> requests.Session:
    retries = Retry(total=2, backoff_factor=0.4, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",))
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def robots_allowed(url: str, allowed_host: str, session: requests.Session, timeout: float) -> bool:
    robots_url = f"https://{allowed_host}/robots.txt"
    try:
        response = session.get(robots_url, timeout=timeout)
    except requests.RequestException as error:
        raise ScrapingError("The robots.txt policy could not be checked.") from error
    if response.status_code == 404:
        return True
    if not 200 <= response.status_code < 300:
        raise ScrapingError(f"robots.txt returned HTTP {response.status_code}.")
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def scrape_source(
    source: Source,
    max_pages: int = 3,
    delay_seconds: float = 0.5,
    timeout: float = 12.0,
    *,
    session: requests.Session | None = None,
    sleep_func: Callable[[float], None] = sleep,
    check_robots: bool = True,
) -> ScrapeResult:
    if not 1 <= max_pages <= 10:
        raise ValueError("max_pages must be between 1 and 10.")
    if not 0 <= delay_seconds <= 10:
        raise ValueError("delay_seconds must be between 0 and 10.")
    http = session or create_session()
    validate_url(source.start_url, source.allowed_host)
    if check_robots and not robots_allowed(source.start_url, source.allowed_host, http, timeout):
        raise ScrapingError("robots.txt does not allow this scraper to access the selected page.")

    started = perf_counter()
    url: str | None = source.start_url
    records: list[dict] = []
    log_rows: list[dict] = []
    requests_made = 1 if check_robots else 0

    for page_number in range(1, max_pages + 1):
        if not url:
            break
        validate_url(url, source.allowed_host)
        page_started = perf_counter()
        try:
            response = http.get(url, timeout=timeout)
            requests_made += 1
        except requests.Timeout as error:
            raise ScrapingError(f"Page {page_number} timed out after {timeout:g} seconds.") from error
        except requests.RequestException as error:
            raise ScrapingError(f"Page {page_number} could not be downloaded.") from error
        if not 200 <= response.status_code < 300:
            raise ScrapingError(f"Page {page_number} returned HTTP {response.status_code}.")
        detected_encoding = getattr(response, "apparent_encoding", None)
        current_encoding = (getattr(response, "encoding", None) or "").lower()
        if detected_encoding and current_encoding in ("", "iso-8859-1", "latin-1"):
            response.encoding = detected_encoding
        page_records, next_url = source.parser(response.text, url)
        records.extend(page_records)
        log_rows.append({
            "page": page_number, "url": url, "status": response.status_code, "records": len(page_records),
            "response_ms": round((perf_counter() - page_started) * 1000, 1),
        })
        url = next_url
        if url and page_number < max_pages and delay_seconds:
            sleep_func(delay_seconds)

    return ScrapeResult(
        source=source.key, data=pd.DataFrame(records), log=pd.DataFrame(log_rows), pages_visited=len(log_rows),
        requests_made=requests_made, elapsed_ms=(perf_counter() - started) * 1000,
    )
