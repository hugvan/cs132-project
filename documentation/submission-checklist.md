# Data repository submission checklist

## Data

- [x] Scraper works through the Cloudflare check (browser-based)
- [x] Full 2025 listing scraped → `frame_2025.csv` (14,668 requests)
- [x] Sample drawn → detail pages scraped → `efoi_2025.csv` (1,641 rows)
- [x] Failed pages checked: 22 no longer public (20 not found, 2 login-only), excluded
- [x] Team checks the 100 rows in `validation_100.csv` against the live pages
- [x] Public copies without `title`/`detail_url` (titles can name people; URLs repeat the title) → `data/public/`
- [ ] Skim `purpose` for personal names before publishing
- [x] Google Sheet with one tab per file in `data/public/`: `efoi_2025`, `frame_2025`, `agencies`

## Portfolio (`docs/index.html`)

- [x] Replace placeholder numbers with actual counts (frame size, sample size, dates)
- [x] Add the Google Sheet link
- [x] Background research with cited sources (EO No. 2, s. 2016)
- [ ] Fill in section and group number
- [ ] Enable GitHub Pages (Settings → Pages → main, `/docs`) and check the public link
- [ ] Print to PDF as `[Section-Group#] CS 132 Portfolio Page.pdf`; each member submits it on UVLE with the portfolio link
