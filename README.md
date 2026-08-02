# Ethical Web Scraping Studio

A responsible web data extraction application with allowlisted sources, robots.txt checks, polite delays, pagination limits and a transparent page-by-page execution log.

This project demonstrates production-minded scraping rather than an unrestricted HTML downloader.

## Business value

Clients often need public product, market or research data converted into structured files. A reliable scraper must handle pagination, changing response conditions and data extraction while respecting the source website and avoiding unsafe targets.

Ethical Web Scraping Studio shows the complete collection workflow through a client-friendly interface.

## Features

- offline product catalog demonstration;
- live Books to Scrape and Quotes to Scrape integrations;
- HTTPS-only source allowlist;
- robots.txt policy verification;
- configurable request timeout;
- configurable delay between pages;
- strict page limit;
- retry policy for temporary failures;
- dedicated Beautiful Soup parsers;
- safe pagination URL validation;
- page-level status, latency and record log;
- summary metrics and data profiling;
- UTF-8 CSV and formatted JSON exports;
- English, Portuguese and Spanish interface;
- command-line automation;
- mocked tests that do not depend on external websites.

## Run locally

```powershell
git clone YOUR_REPOSITORY_URL
cd ethical-web-scraping-studio
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`.

## Command-line examples

```powershell
# Offline demonstration
.\.venv\Scripts\python.exe main.py demo --pages 2

# Live practice websites
.\.venv\Scripts\python.exe main.py books --pages 2 --delay 1
.\.venv\Scripts\python.exe main.py quotes --pages 2 --delay 1
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Architecture

```text
Allowlisted source
       │
       ▼
robots.txt check
       │
       ▼
Rate-limited page requests ──► timeout, retry, host validation
       │
       ▼
Beautiful Soup parser ──► structured records + next page
       │
       ├──► execution log
       └──► CSV / JSON export
```

## Project structure

```text
├── app.py                 # multilingual Streamlit interface
├── main.py                # command-line collection
├── src/
│   ├── scraper.py         # responsible collection engine
│   ├── parsers.py         # source-specific HTML parsing
│   ├── sources.py         # allowlisted source definitions
│   ├── demo.py            # deterministic offline result
│   ├── exporting.py       # CSV and JSON output
│   ├── models.py          # source and result models
│   └── i18n.py            # interface translations
├── tests/                 # mocked behavior and policy tests
└── requirements.txt
```

## Responsible-use design

- arbitrary URLs are not accepted;
- only websites explicitly created for scraping practice are enabled;
- robots.txt is checked before live collection;
- page count and request frequency are limited;
- every pagination URL is validated again;
- the demonstration works without contacting any website.

Always review a website's terms, robots.txt and applicable laws before adapting this code to another source.

## License

MIT
