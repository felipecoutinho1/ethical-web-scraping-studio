"""Explicitly allowlisted scraping sources."""

from src.models import Source
from src.parsers import parse_books, parse_quotes


SOURCES = {
    "books": Source("books", "https://books.toscrape.com/", "books.toscrape.com", parse_books),
    "quotes": Source("quotes", "https://quotes.toscrape.com/", "quotes.toscrape.com", parse_quotes),
}
