# Who Gets an Answer?

**Comparing eFOI Response Times and Outcomes in 2025**

FYI — FOI Your Information · CS 132 · SDG 16

Vaughn Aquino · Eliana Lim · Jon Mayuyu · Charlize Sim

## Current status

Repository and portfolio scaffold. **No data has been collected or analyzed.**
The 1,000-request figure is a target, not an observed sample size. Collection
and scraping are not run by any command or GitHub workflow in this repository.

## Where things go

```text
docs/                     GitHub Pages portfolio (plain HTML/CSS)
documentation/            Methods, dictionary, collection log, submission checklist
data/templates/           Header-only input templates
data/raw/                 Original source files (ignored by Git)
data/interim/             Working files (ignored by Git)
data/processed/           Cleaned CSV and audit outputs (ignored by Git)
scripts/                  Reproducible processing commands
tests/                    Synthetic tests; not research observations
notebooks/                Future EDA notebooks
reports/                  Future figures and portfolio PDF snapshots
.github/workflows/        Automated code and portfolio checks
```

## Quick start

Requires Python 3.10 or newer. The processing tools use only the standard library;
there are no packages to install.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
python3 -m http.server 8000 --directory docs
```

Open <http://localhost:8000> for the portfolio. Stop the server with Ctrl+C.
Edit `docs/index.html` for content and `docs/assets/styles.css` for appearance.
The page works without JavaScript and has a print stylesheet.

## When data collection begins

1. Read [the collection protocol](documentation/methodology.md) and
   [data dictionary](documentation/data-dictionary.md).
2. Preserve the original export in `data/raw/`. Create a separate input CSV using
   `data/templates/requests.csv`; do not overwrite the original file.
3. Record source, collection date, access conditions, sampling decisions and
   transformations in [the collection log](documentation/collection-log.md).
4. Use `data/templates/status_mapping.csv` to document the team's reviewed outcome
   definitions. It is intentionally empty: status labels must not be guessed.
5. Run the processor after supplying real data:

   ```bash
   python3 scripts/process_data.py data/raw/requests.csv \
     --status-map data/templates/status_mapping.csv \
     --output-dir data/processed
   ```

6. Inspect `quality_report.json` and `issues.csv`. `requests_clean.csv` contains
   structurally valid, deduplicated 2025 requests; `requests_quarantine.csv`
   contains rows needing correction. Warnings stay visible in the clean data.
   An empty file or quarantined rows produces exit code 1; bad schema/configuration
   produces exit code 2. Resolve issues and rerun before analysis.
7. Compare 100 collected rows with source pages using the manual validation
   template. Export reviewed data to Google Sheets with separate tabs per source.
   Turn off automatic conversion to formulas/numbers/dates on CSV import so
   tracking numbers and source text remain literal. Review free text for personal
   information before publication.
8. Update the portfolio's actual sample size, dates, collection account, quality
   report and Google Sheet link. Nothing automatically publishes local data.

## GitHub and portfolio setup

See [GitHub setup](documentation/github-setup.md). This repository uses the
`main` branch's `/docs` folder for GitHub Pages. Only that folder is published
as the website. Python runs locally or in CI, not on GitHub Pages.

The checks workflow runs on pushes and pull requests. It does not scrape, process
private files, or publish data. Use short feature branches and pull requests for
team changes; review data and documentation together before merging.

## Milestone requirements

The current deliverable needs the research background, questions, hypotheses,
proposed solution, data and method descriptions, a Google Sheet containing the
data, and a PDF snapshot. Follow [the submission checklist](documentation/submission-checklist.md).
Do not treat this scaffold as a completed data repository submission.

The supplied guidelines require some 2025/2026 observations and at least 100
unique samples; their highest size/quality band starts at 1,000 observations.
Our proposal specifically targets at least 1,000 requests filed in 2025.
The guidelines also contain older year references; follow the current requirement
and verify ambiguous instructions with the instructor.

## Sources and reuse

- Team proposal: `[CS 132] Proposal.pdf` (provided locally).
- Course guidelines: `CS 132 Project Guidelines - AY26-27 S1 (1).pdf` (provided locally).
- [Philippine eFOI portal](https://www.foi.gov.ph/)
- [eFOI request browser](https://www.foi.gov.ph/requests/)
- [eFOI agency directory](https://www.foi.gov.ph/agencies/)
- [UN Sustainable Development Goal 16](https://sdgs.un.org/goals/goal16)

Course PDFs are not redistributed in this repository. No license for third-party
data is implied; record source permissions before sharing data. A project code
license has not yet been selected by the team.
