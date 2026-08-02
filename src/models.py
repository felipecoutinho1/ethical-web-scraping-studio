"""Models for scraping sources and results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd


@dataclass(frozen=True)
class Source:
    key: str
    start_url: str
    allowed_host: str
    parser: Callable[[str, str], tuple[list[dict], str | None]]


@dataclass
class ScrapeResult:
    source: str
    data: pd.DataFrame
    log: pd.DataFrame
    pages_visited: int
    requests_made: int
    elapsed_ms: float
