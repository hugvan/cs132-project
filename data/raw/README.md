# Raw data

Scraped from https://www.foi.gov.ph/ by `scripts/scrape_efoi.py`. Files are not edited by hand.

- `listing.csv`: one row per request card on listing pages 1024–2002 (2025 filings), with the `page` number and `scraped_at`
- `details.csv`: fields parsed from each sampled request's detail page
- `agencies.csv`: agency directory with the official agency group
- `errors.csv`: pages that failed to load or parse (re-run the scrape command to retry)
- `requests_index.csv`: a teammate's earlier index (2024–2026). Not used: all its 2025 rows are also in `listing.csv`.
