"""Command-line entry point for responsible scraping."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.demo import demo_result
from src.exporting import csv_bytes, json_bytes
from src.scraper import scrape_source
from src.sources import SOURCES


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect structured data from an allowlisted practice source.")
    parser.add_argument("source", choices=["demo", "books", "quotes"], nargs="?", default="demo")
    parser.add_argument("--pages", type=int, choices=range(1, 6), default=2)
    parser.add_argument("--delay", type=float, default=0.8)
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()

    result = demo_result(args.pages) if args.source == "demo" else scrape_source(SOURCES[args.source], args.pages, args.delay)
    args.output.mkdir(parents=True, exist_ok=True)
    csv_path = args.output / f"{args.source}_scraped_data.csv"
    json_path = args.output / f"{args.source}_scraped_data.json"
    csv_path.write_bytes(csv_bytes(result.data))
    json_path.write_bytes(json_bytes(result.data))
    print(f"Pages: {result.pages_visited} | Records: {len(result.data)} | Requests: {result.requests_made}")
    print(f"CSV: {csv_path.resolve()}")
    print(f"JSON: {json_path.resolve()}")


if __name__ == "__main__":
    main()
