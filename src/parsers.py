"""HTML parsers for allowlisted practice websites."""

from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_books(html: str, page_url: str) -> tuple[list[dict], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        price = card.select_one(".price_color")
        availability = card.select_one(".availability")
        rating = card.select_one("p.star-rating")
        if not link:
            continue
        rating_classes = rating.get("class", []) if rating else []
        rating_value = next((item for item in rating_classes if item != "star-rating"), "")
        records.append({
            "title": link.get("title", link.get_text(strip=True)),
            "price": price.get_text(strip=True).replace("Â£", "£") if price else "",
            "availability": " ".join(availability.stripped_strings) if availability else "",
            "rating": rating_value,
            "product_url": urljoin(page_url, link.get("href", "")),
        })
    next_link = soup.select_one("li.next a")
    return records, urljoin(page_url, next_link["href"]) if next_link else None


def parse_quotes(html: str, page_url: str) -> tuple[list[dict], str | None]:
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for quote in soup.select("div.quote"):
        text = quote.select_one("span.text")
        author = quote.select_one("small.author")
        records.append({
            "quote": text.get_text(" ", strip=True) if text else "",
            "author": author.get_text(strip=True) if author else "",
            "tags": ", ".join(tag.get_text(strip=True) for tag in quote.select("a.tag")),
            "source_url": page_url,
        })
    next_link = soup.select_one("li.next a")
    return records, urljoin(page_url, next_link["href"]) if next_link else None
