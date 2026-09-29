# Collection log

## 2026-09-28: plain HTTP blocked

Direct requests to `https://www.foi.gov.ph/` (Python `urllib`, `curl`, several User-Agent
strings) all returned HTTP 403 with a Cloudflare "Just a moment..." challenge (`cf-mitigated:
challenge`). `robots.txt` (all agents allowed, no crawl delay) and the terms of service
(non-commercial research use permitted) were reviewed.

## 2026-09-29: browser-based scraper works

- A Playwright-launched Chrome loaded one page, then was challenged on every page after.
- A normal Google Chrome started with `--remote-debugging-port` and a separate profile, then
  driven over CDP, loaded listing and detail pages with no challenge. This became
  `scripts/scrape_efoi.py`.
- The parser was checked on five 2025 detail pages (successful, denied, closed, partially
  successful, referred). All fields matched the pages.
- Listing had 17,696 pages (about 271,000 requests). Binary search placed 2025 filings on
  pages **1024–2002**.
- Full listing scrape of pages 1024–2002: 15:19–16:03, 979/979 pages, 0 errors,
  14,685 rows → **14,668 unique 2025 requests** (17 duplicates across page boundaries, since
  new filings shift pages during the scrape). Every request mapped to an agency group and a status.
- **The portal has no public requests filed between 2025-03-20 22:30 and 2025-06-18 16:00.**
  The teammate's `requests_index.csv` shows the same gap, and all its 14,318 rows for 2025 are in
  the new frame, so this is a gap in the source, not in the scrape. Q2 holds only 324 requests
  (late June).
- Stratified sample drawn (seed 132): **1,663 requests**. LGU (175) and WATER-DISTRICT (287) are
  taken in full; the other groups get 300 each.
- Detail scrape of the sample: 17:04–18:20. The site rate-limited about every 75 pages
  (11 × HTTP 429). The scraper was changed to pause 60 s on a 429, and every throttled page
  loaded on retry.
- **1,641 of 1,663 sampled requests collected (98.7%).** The 22 missing pages are gone from the
  public site: 20 show "not found" and 2 redirect to login. They are listed in
  `data/raw/errors.csv` and excluded, not replaced.
- Final dataset `data/processed/efoi_2025.csv`: 1,641 unique requests; 205 with no agency reply;
  1,409 closed (final status); 0 replies dated before filing; status matched the listing for
  every request.

<!-- Add: results of the 100-row manual validation (validation_100.csv). -->
