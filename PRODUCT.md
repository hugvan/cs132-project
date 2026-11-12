# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Primary users — CS 132 instructors and graders:** Evaluating the capstone portfolio (`docs/index.html` on GitHub Pages and its printed A4 PDF snapshot submitted on UVLE) against course requirements for data collection, exploratory data analysis, hypothesis testing, storytelling, and actionable conclusions.
- **Secondary users — Civic researchers, journalists, and citizens:** Exploring Philippine eFOI responsiveness across official agency groups, inspecting request-level methodology and caveats, and drawing evidence-based takeaways about access to public information under Executive Order No. 2, s. 2016.
- **Peer audience — CS 132 classmates:** Reviewing the Pilipinas in a Nutshell (PiNut) 2026 showcase and comparing empirical methods and visual narratives.

## Product Purpose

Deliver a single-page static research portfolio ("Who Gets an Answer? eFOI Response Times and Outcomes in 2025") that presents the complete, verified empirical story from notebooks 01–03 and `reports/nutshell.md`—centering on the finding that *"A fast reply is not a yes"*—while serving both as a live interactive web exploration on GitHub Pages and a complete, readable A4 PDF submission artifact for UVLE.

## Positioning

Unlike perception surveys or aggregate agency summaries, this portfolio is anchored in a reproducible, request-level census and stratified sample scraped directly from the public Philippine eFOI portal (14,668 public 2025 requests in the full frame; 1,641 sampled requests with minute-level reply timelines), pairing interactive web data exploration with strict methodological transparency (sampling weights, 100/100 manual validation, vanished pages, and the 90-day March–June portal gap).

## Operating Context

- **Course & theme:** UP Diliman CS 132 (AY 2026–2027, Semester 1), Section WFX · Group 1, under the "Pilipinas in a Nutshell (PiNut) 2026" theme and SDG 16 (Peace, Justice & Strong Institutions; targets 16.6 and 16.10).
- **Web deployment:** Hosted directly from `cs132-project/docs/` on GitHub Pages as a static single-page site (`docs/index.html`).
- **Academic submission ritual:** Exported via browser Print-to-PDF (`@media print`, A4) as `[WFX-Group1] CS 132 Portfolio Page` PDFs for individual group member submission on UVLE alongside the live GitHub Pages URL.
- **External deliverables linked from the page:** Public Google Sheet (`efoi_2025`, `frame_2025`, `agencies` tabs) and the `hugvan/cs132-project` GitHub repository containing scraping, parsing, analysis scripts, and notebooks 01–03.

## Capabilities and Constraints

- **Static single-page architecture:** Pure static HTML, CSS, and vanilla JS inside `cs132-project/docs/` with no build step, server runtime, or backend dependency so GitHub Pages serves `docs/` directly.
- **Milestone scope:** Complete research story covering background, research questions and hypotheses, data repository & methodology, exploratory data analysis, hypothesis tests, nutshell synthesis, discussion/limitations, and a grounded call to action—with **no** machine learning modeling section.
- **Interactive web + complete A4 print parity:** Interactive JS visualizations, filters, and stamped/dynamic views on the web must degrade or expand gracefully under `@media print` so every chart, table, finding, and takeaway prints cleanly on A4 in a complete, readable state.
- **Strict factual & statistical integrity:** All numbers, test results, methodology details, and recommendations must trace strictly to verified outputs in `notebooks/01_data_quality.ipynb`, `notebooks/02_response_times.ipynb`, `notebooks/03_outcomes.ipynb`, `scripts/analysis.py`, `documentation/`, and `reports/nutshell.md`.
- **Mandatory caveats & definitions:**
  - **90-day portal gap:** No public 2025 requests appear on the portal from `2025-03-20 22:30` to `2025-06-18 16:00` (Q2 holds only 324 late-June filings), limiting quarter-to-quarter comparisons.
  - **22 vanished detail pages:** Of 1,663 sampled requests, 22 were no longer publicly served at detail-scrape time (20 not found, 2 login-only; 20 in LEA Q1, 2 in NGA Q1) and are excluded rather than replaced; collected count is 1,641 (98.7%).
  - **Water District silence:** Water Districts show ~26% no-reply share (must be reported with exact verified figures from notebooks), and closed no-reply requests all ended unsuccessful.
  - **Acknowledgment vs. fulfillment:** `first_response_days` measures elapsed time to the earliest agency message, which may be an acknowledgment rather than a substantive answer ("A fast reply is not a yes").
  - **Missing replies & open cases:** Blank `first_response_days` stays blank (never zero); open and referred requests are not counted as unsuccessful in RQ2; RQ3 restricts to closed (`is_final`) requests; population estimates use `sampling_weight` (adjusted for collected counts).
- **Privacy constraint:** Never expose individual request `title` values, source `detail_url` slugs, requester names, contact details, message text, or attachments on the portfolio or public dataset copies.

## Brand Commitments

- **Identity:** Team name **FYI — FOI Your Information** (CS 132 · AY 2026–2027, Semester 1 · Section WFX · Group 1; members: Vaughn Aquino, Eliana Lim, Jon Mayuyu, Charlize Sim).
- **Existing assets & links:** Preserve links to the project GitHub repository (`https://github.com/hugvan/cs132-project`), the public Google Sheet (`https://docs.google.com/spreadsheets/d/10om8YdCtoXA7cndqIHQegUSYfqqeKhTvkbDoB-45Vrc/edit?usp=sharing`), EO No. 2 s. 2016, eFOI portal/directory/terms, and UN SDG 16.
- **Voice:** Evidence-led, civic-minded, transparent, and restrained—stating methods, limitations, and statistical qualifiers plainly without hype or causal overclaiming.

## Evidence on Hand

- `docs/index.html` & `docs/assets/styles.css` — Incumbent portfolio webpage (currently staged at the data repository milestone, awaiting completed EDA/findings/conclusion integration).
- `notebooks/01_data_quality.ipynb` — Data quality checks, missingness, normality checks (Shapiro–Wilk), 90-day gap, and 22 missing detail pages audit.
- `notebooks/02_response_times.ipynb` — RQ1 analysis (weighted medians, no-reply shares, Kruskal–Wallis, pairwise Mann–Whitney with Bonferroni correction).
- `notebooks/03_outcomes.ipynb` — RQ2 and RQ3 analyses (outcome shares across 14,668 frame requests, chi-square test, open-denominator sensitivity, weighted Mann–Whitney permutation test for speed vs. success).
- `scripts/analysis.py` — Shared weighted estimators (`collected_weights`, `weighted_median`, `weighted_quartile_edges`, `weighted_mean`, `weighted_mannwhitney`).
- `reports/nutshell.md` & `reports/figures/` — Reviewed nutshell caption/headline and static plots (`nutshell.png`, `nutshell.pdf`, `rq1_median_and_noreply.png`, `rq1_response_time_distribution.png`, `rq2_outcome_shares.png`, `rq3_speed_and_success.png`).
- `documentation/methodology.md`, `documentation/data-dictionary.md`, `documentation/collection-log.md` — Verified collection protocol, definitions, validation results (100/100 random rows matched live pages; 17 cross-page duplicates removed), and limitations.

## Product Principles

1. **Truth over polish:** Every claim, chart, and takeaway must match verified notebook and script outputs, with denominators, weights, and caveats visible alongside headline numbers.
2. **Narrative continuity from question to action:** Flow logically from civic context (EO No. 2) and research questions through methodology, statistical findings, and honest limitations to concrete, evidence-grounded recommendations.
3. **Web interactivity without print breakage:** Interactive visual exploration enriches the browser experience for graders and civic researchers while `@media print` guarantees a complete, legible A4 PDF snapshot with no collapsed, clipped, or missing content.
4. **Privacy and non-causality discipline:** Protect individual requester privacy by omitting titles/URLs and maintain statistical rigor by distinguishing correlation from causation and acknowledgment from fulfillment.

## Accessibility & Inclusion

- Semantic HTML landmarks, heading hierarchy, skip-to-content link, accessible table headers/captions, and keyboard-visible focus indicators.
- Respect `prefers-reduced-motion` for all transitions, animations, and smooth scrolling.
- High-contrast readable typography and chart encodings in both screen viewing and A4 black-and-white/color print output.

