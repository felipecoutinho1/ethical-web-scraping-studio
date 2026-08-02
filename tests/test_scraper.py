from io import BytesIO
import json
import unittest
from unittest.mock import Mock

import requests

from src.demo import demo_result
from src.exporting import csv_bytes, json_bytes
from src.i18n import TEXTS
from src.models import Source
from src.parsers import parse_books, parse_quotes
from src.scraper import ScrapingError, robots_allowed, scrape_source, validate_url


BOOKS_HTML = """
<article class="product_pod"><p class="star-rating Three"></p><h3><a href="book/a.html" title="Book A">A</a></h3><p class="price_color">£12.50</p><p class="availability">In stock</p></article>
<li class="next"><a href="page-2.html">next</a></li>
"""
QUOTES_HTML = """
<div class="quote"><span class="text">“Be curious.”</span><small class="author">Ada</small><a class="tag">learning</a><a class="tag">science</a></div>
"""


class FakeResponse:
    def __init__(self, text="", status=200):
        self.text, self.status_code = text, status


class TestWebScraper(unittest.TestCase):
    def test_book_parser_extracts_fields_and_next_page(self):
        records, next_url = parse_books(BOOKS_HTML, "https://books.toscrape.com/catalogue/page-1.html")
        self.assertEqual(records[0]["title"], "Book A")
        self.assertEqual(records[0]["price"], "£12.50")
        self.assertEqual(records[0]["rating"], "Three")
        self.assertEqual(next_url, "https://books.toscrape.com/catalogue/page-2.html")

    def test_book_parser_repairs_common_currency_mojibake(self):
        broken_html = BOOKS_HTML.replace("£12.50", "Â£12.50")
        records, _ = parse_books(broken_html, "https://books.toscrape.com/")
        self.assertEqual(records[0]["price"], "£12.50")

    def test_quote_parser_extracts_tags(self):
        records, next_url = parse_quotes(QUOTES_HTML, "https://quotes.toscrape.com/")
        self.assertEqual(records[0]["author"], "Ada")
        self.assertEqual(records[0]["tags"], "learning, science")
        self.assertIsNone(next_url)

    def test_url_allowlist_rejects_other_hosts_and_http(self):
        validate_url("https://books.toscrape.com/", "books.toscrape.com")
        with self.assertRaises(ScrapingError):
            validate_url("http://books.toscrape.com/", "books.toscrape.com")
        with self.assertRaises(ScrapingError):
            validate_url("https://127.0.0.1/", "books.toscrape.com")

    def test_robots_policy_is_respected(self):
        session = Mock()
        session.get.return_value = FakeResponse("User-agent: *\nDisallow: /private")
        self.assertFalse(robots_allowed("https://books.toscrape.com/private", "books.toscrape.com", session, 5))
        self.assertTrue(robots_allowed("https://books.toscrape.com/catalogue", "books.toscrape.com", session, 5))

    def test_missing_robots_file_allows_collection(self):
        session = Mock()
        session.get.return_value = FakeResponse(status=404)
        self.assertTrue(robots_allowed("https://quotes.toscrape.com/", "quotes.toscrape.com", session, 5))

    def test_scrape_paginates_and_waits_between_pages(self):
        page_two = BOOKS_HTML.replace("<li class=\"next\"><a href=\"page-2.html\">next</a></li>", "")
        session = Mock()
        session.get.side_effect = [FakeResponse("User-agent: *\nAllow: /"), FakeResponse(BOOKS_HTML), FakeResponse(page_two)]
        waits = []
        source = Source("test", "https://books.toscrape.com/catalogue/page-1.html", "books.toscrape.com", parse_books)
        result = scrape_source(source, max_pages=2, delay_seconds=0.5, session=session, sleep_func=waits.append)
        self.assertEqual(result.pages_visited, 2)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(waits, [0.5])
        self.assertEqual(result.requests_made, 3)

    def test_disallowed_robots_stops_before_page_request(self):
        session = Mock()
        session.get.return_value = FakeResponse("User-agent: *\nDisallow: /")
        source = Source("test", "https://books.toscrape.com/", "books.toscrape.com", parse_books)
        with self.assertRaisesRegex(ScrapingError, "robots.txt"):
            scrape_source(source, session=session)

    def test_timeout_becomes_clear_error(self):
        session = Mock()
        session.get.side_effect = requests.Timeout()
        source = Source("test", "https://books.toscrape.com/", "books.toscrape.com", parse_books)
        with self.assertRaisesRegex(ScrapingError, "robots.txt"):
            scrape_source(source, session=session)

    def test_demo_and_exports(self):
        result = demo_result(2)
        self.assertEqual(len(result.data), 8)
        self.assertTrue(csv_bytes(result.data).startswith(b"\xef\xbb\xbf"))
        self.assertEqual(len(json.loads(json_bytes(result.data))), 8)

    def test_translation_keys_match(self):
        self.assertEqual(set(TEXTS["en"]), set(TEXTS["pt"]))
        self.assertEqual(set(TEXTS["en"]), set(TEXTS["es"]))


if __name__ == "__main__":
    unittest.main()
