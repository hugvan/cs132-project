# Methodology

## Source

The public [eFOI portal](https://www.foi.gov.ph/) (Philippine Freedom of Information,
Executive Order No. 2, s. 2016). Two page types are used:

- **Listing pages** (`/requests/page/N/`, 15 requests per page, newest first). Each card has the
  title, agency, filing date and time, purpose, tracking number and current status.
- **Detail pages** (`/agencies/<agency>/<slug>/`). These add the status timeline (submitted,
  processing, final status with timestamps) and the conversation, which has a timestamp on each
  requester and agency message.

Agency groups (NGA, GOCC, SUC, WATER-DISTRICT, LGU, LEA) come from the
[agency directory](https://www.foi.gov.ph/agencies/), saved in `data/raw/agencies.csv`
(739 agencies) and joined on the agency code in the URL.

`robots.txt` allows all user agents and has no crawl delay. The terms of service allow
non-commercial research use of the information.

## Why a browser-based scraper

The site is behind Cloudflare. Plain HTTP clients (`urllib`, `requests`, `curl`) get
HTTP 403 with a "Just a moment..." challenge page, whatever User-Agent they send.
A browser that Playwright launches in automation mode is also challenged after the first page.
A normal Google Chrome window loads the pages without a challenge. `scrape_efoi.py` starts
Chrome with a remote-debugging port and a separate profile (`.chrome-profile/`), connects to it
with Playwright, and reads each page's rendered HTML. It does not solve or bypass challenges: if
one appears, a team member ticks it in the window.

Politeness: one page at a time, with a random 1–2 second wait between loads and backoff on errors.

## Sampling frame

1. Binary search over listing pages finds the first and last page with 2025 filings
   (pages 1024–2002 on 2026-09-29).
2. Every listing page in that range is scraped to `data/raw/listing.csv`.
3. `build_dataset.py frame` deduplicates on tracking number, keeps filings from
   2025-01-01 to 2025-12-31 (Manila time, as displayed), and attaches the agency group.
   Result: `data/processed/frame_2025.csv`, the full population of public 2025 requests.

The frame alone answers RQ2 (status by agency group) for the full population.

## Sample for response times

Detail pages are needed for reply timestamps, so a stratified random sample is drawn
(`build_dataset.py sample`, seed 132):

- Strata: agency group × filing quarter.
- Each agency group gets up to 300 requests, split across quarters in proportion to that group's
  filings. Groups with fewer than 300 requests in 2025 are taken in full.
- `sampling_weight` = stratum population ÷ stratum sample size, for population-level estimates.

## Definitions

- **First response**: the earliest message the agency posted in the conversation.
  `first_response_days` = (first agency message − filing time) in fractional days. A request
  with no agency message has an empty value, not zero.
- **Outcome** (from portal status at scrape time): SUCCESSFUL → successful;
  PARTIALLY SUCCESSFUL → partially successful; DENIED, CLOSED → unsuccessful;
  REFERRED → referred; PENDING, ACCEPTED, PROCESSING, AWAITING CLARIFICATION → open.
- **Final (closed) request**: status is SUCCESSFUL, PARTIALLY SUCCESSFUL, DENIED or CLOSED.
  RQ3 uses these. `is_successful` is true for SUCCESSFUL and PARTIALLY SUCCESSFUL.

## Quality checks

- Tracking numbers are unique in every output.
- Replies timestamped before filing are flagged (`flag_reply_before_filing`), not dropped.
- Pages that fail to load or parse are logged in `data/raw/errors.csv`. The team re-runs the
  command to retry them. Pages the portal no longer serves (not found, or login required) are
  excluded, not replaced: 22 of 1,663 sampled requests.
- `data/processed/validation_100.csv` lists 100 random dataset rows. Team members open each URL
  and mark whether filing date, first reply and status match.

## Privacy

Only structural fields are stored: no requester names, contact details, message text or
attachments. Titles and purposes are public on the portal and kept for EDA. Before sharing,
check them for personal names.

## Limitations

- **Coverage gap:** the portal lists no public requests filed from 2025-03-20 22:30 to
  2025-06-18 16:00, so Q2 holds only late-June filings (324 requests). Quarter comparisons
  should note this. The cause is unknown; check with the FOI-PMO before reporting it.

- Status and replies are observed on the scrape date. Late-2025 requests have had less time to
  close.
- Only requests published on the portal are visible. Requests filed by other channels, or not
  made public, are not in the frame.
- The first agency message may be an acknowledgment, not a substantive answer.
