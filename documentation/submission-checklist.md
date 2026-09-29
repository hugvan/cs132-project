# Data repository submission checklist

## Data

- [x] Scraper works through the Cloudflare check (browser-based)
- [x] Full 2025 listing scraped → `frame_2025.csv` (14,668 requests)
- [x] Sample drawn → detail pages scraped → `efoi_2025.csv` (1,641 rows)
- [x] Failed pages checked: 22 no longer public (20 not found, 2 login-only), excluded
- [ ] Team checks the 100 rows in `validation_100.csv` against the live pages
- [ ] Skim titles/purposes for personal names before publishing
- [ ] Google Sheet with tabs: `efoi_2025` (study dataset), `frame_2025` (all 2025 requests), `agencies`

## Portfolio (`docs/index.html`)

- [x] Replace placeholder numbers with actual counts (frame size, sample size, dates)
- [ ] Add the Google Sheet link
- [ ] Fill in section and group number
- [ ] Enable GitHub Pages (Settings → Pages → main, `/docs`) and check the public link
- [ ] Print to PDF as `[Section-Group#] CS 132 Portfolio Page.pdf`; each member submits it on UVLE with the portfolio link
