# Who Gets an Answer? eFOI Response Times and Outcomes in 2025

CS 132 project by **FYI – FOI Your Information** (Vaughn Aquino, Eliana Lim, Jon Mayuyu,
Charlize Sim). SDG 16 – Peace, Justice and Strong Institutions.

Portfolio: `docs/index.html` (GitHub Pages, served from `/docs`).

## Research questions

1. How long does each agency group take to post its first response to an eFOI request?
2. Do the shares of successful and unsuccessful requests differ by agency group?
3. Among closed requests, are faster first responses linked to a successful outcome?

## Data pipeline

The source is the public [eFOI request browser](https://www.foi.gov.ph/requests/). The site is
behind Cloudflare, which blocks plain HTTP clients (`requests`/`curl` get HTTP 403), so the
scraper drives a real Google Chrome window through Playwright. Details are in
[documentation/methodology.md](documentation/methodology.md).

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
source .venv/bin/activate

python scripts/scrape_efoi.py range --year 2025                   # find listing pages for 2025
python scripts/scrape_efoi.py listing --start 1024 --end 2002     # every 2025 request card
python scripts/build_dataset.py frame                             # -> data/processed/frame_2025.csv
python scripts/build_dataset.py sample                            # -> data/interim/sample.csv
python scripts/scrape_efoi.py details --sample data/interim/sample.csv   # reply timestamps
python scripts/build_dataset.py dataset                           # -> data/processed/efoi_2025.csv
python scripts/build_dataset.py public                            # -> data/public/ (Google Sheet copies)
```

Scrape commands are resumable: if one stops, run the same command again. A Chrome window opens
the first time. If Cloudflare shows a checkbox, tick it and the script continues.
Page numbers move as new requests are filed, so re-run `range` before a fresh listing scrape.

## Repository layout

| Path | Contents |
| --- | --- |
| `scripts/efoi_parse.py` | HTML → fields for listing and detail pages |
| `scripts/scrape_efoi.py` | Browser-based scraper (range / listing / details) |
| `scripts/build_dataset.py` | Frame, stratified sample, final dataset |
| `data/raw/` | Scraped outputs as collected (`listing.csv`, `details.csv`, `agencies.csv`, `errors.csv`) |
| `data/interim/` | `sample.csv`, the drawn sample with sampling weights |
| `data/processed/` | `frame_2025.csv` (all 2025 requests), `efoi_2025.csv` (study dataset), `validation_100.csv` |
| `data/public/` | Google Sheet copies of `efoi_2025`, `frame_2025` and `agencies`, without `title` and `detail_url` |
| `documentation/` | Methodology, data dictionary, collection log, submission checklist |
| `docs/` | Portfolio website |
| `tests/` | Parser tests on synthetic HTML (`python -m unittest discover -s tests`) |

`data/raw/requests_index.csv` is an earlier index scraped by a teammate (2024–2026, 42,765 rows).
Its 2025 rows are all contained in `listing.csv`, which is a newer, complete pass.
