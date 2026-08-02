"""Deterministic offline scraping result."""

import pandas as pd

from src.models import ScrapeResult


PRODUCTS = [
    {"title": "Wireless Keyboard", "price": 49.90, "category": "Accessories", "rating": 4.6, "availability": "In stock"},
    {"title": "USB-C Hub", "price": 34.50, "category": "Accessories", "rating": 4.4, "availability": "In stock"},
    {"title": "Noise-Cancelling Headphones", "price": 129.00, "category": "Audio", "rating": 4.8, "availability": "Low stock"},
    {"title": "Portable SSD 1TB", "price": 99.90, "category": "Storage", "rating": 4.7, "availability": "In stock"},
    {"title": "Webcam Full HD", "price": 59.75, "category": "Video", "rating": 4.3, "availability": "In stock"},
    {"title": "Laptop Stand", "price": 42.00, "category": "Office", "rating": 4.5, "availability": "Low stock"},
    {"title": "Mechanical Mouse", "price": 27.90, "category": "Accessories", "rating": 4.2, "availability": "In stock"},
    {"title": "Desk Microphone", "price": 74.50, "category": "Audio", "rating": 4.6, "availability": "In stock"},
]


def demo_result(max_pages: int = 2) -> ScrapeResult:
    page_size = 4
    records = PRODUCTS[: max_pages * page_size]
    pages = min(max_pages, 2)
    log = pd.DataFrame([
        {"page": page, "url": f"https://demo.example.test/catalog?page={page}", "status": 200, "records": len(records[(page - 1) * page_size:page * page_size]), "response_ms": 62.0 + page * 7}
        for page in range(1, pages + 1)
    ])
    return ScrapeResult("demo", pd.DataFrame(records), log, pages, pages, 148.5)
