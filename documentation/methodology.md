# Collection and processing protocol

**Status: planned. No requests have been collected, sampled or analyzed.**

## Research scope

One row represents one eFOI request filed from 2025-01-01 through 2025-12-31
in Asia/Manila. The proposal targets at least 1,000 unique tracking numbers.
Dates of replies may fall in later years; do not filter replies to 2025.
The directory categories are NGA, GOCC, SUC, WATER DISTRICT, LGU and LEA.
Preserve these official labels without guessing categories from agency names.

## Planned acquisition

Primary route: ask the FOI Program Management Office for a de-identified CSV
containing tracking number, agency, group, filing date, first agency reply date,
status and purpose. No request has been sent by this repository setup.
Record the source's extraction date and coverage, not just the download date.

Fallback: build a 2025 request frame and stratify by filing quarter and agency
group. Before sampling, record frame completeness, stratum counts, allocation,
random seed and inclusion probabilities. Draw at least 1,000 unique requests,
using a documented reproducible script. Proportional allocation is a starting
option, not an implemented decision; retain weights if groups are oversampled.
Do not silently replace failed pages with convenient alternatives.

The proposal specifies a 1–2 second delay, caching completed pages and logging
errors. A scraper and sampler are intentionally not implemented yet. Verify
access conditions at collection time, avoid requester information and keep
cached source pages out of Git. Store only needed de-identified fields.

## Operational definitions

- **First response:** first agency-authored reply after filing; requester follow-ups
  do not count. The collector must verify author attribution. The processing script
  cannot determine authorship from a timestamp alone.
- **Response time:** elapsed calendar days, including fractional days when times
  are known. Date-only inputs produce calendar-date differences; do not interpret
  them as exact elapsed hours or mix precision without reporting it. This is not a
  business-day or statutory-compliance measure. Missing replies stay missing.
- **Status:** portal label as observed at the recorded extraction/collection date,
  not necessarily a final outcome. Do not call pending records unsuccessful.
- **Outcome/closure:** manually reviewed mapping in `status_mapping.csv`. Specify
  the definition and supporting URL for every label. Allowed outcomes are
  `successful`, `unsuccessful`, `pending`, `other`, `unknown`; `is_closed` is
  `true`/`false`. Partial fulfillment, referral and ambiguous labels need an
  explicit decision; the scaffold makes none. Unknown mappings generate warnings.

## Implemented preprocessing

`scripts/process_data.py` reads UTF-8 CSVs with the documented columns. It trims
outer whitespace, uppercases agency-group codes, interprets timezone-free dates
as Asia/Manila, normalizes timestamps to that timezone, and retains the original
CSV untouched. It rejects unexpected columns rather than accidentally carrying
unapproved personal fields through the output.

Missing tracking IDs/agencies, invalid dates, out-of-scope filing dates, replies
before filing, collection before filing/reply, unknown nonblank agency groups and
invalid source URLs are quarantined. Identical duplicate IDs retain one record;
conflicting duplicates quarantine all versions. Missing groups/replies/purpose,
unknown outcomes and mixed date precision generate warnings and are preserved.
Inputs with incomplete CSV rows or extra cells fail instead of being silently read.

Outputs include clean data, quarantine data, issue codes by input record, and a JSON
report with input SHA-256, status-map SHA-256, counts, missing values and coverage.
It reports the 100/500/1,000 size bands but does not certify quality or a grade.
Do not interpret a successful command as submission readiness.

## Manual validation and reporting

Compare 100 collected rows with original pages, recording selection method,
reviewer, discrepancies and corrections in the manual validation template.
Also investigate every flagged issue. Record before/after counts and retained
sample sizes; do not fill missing response times with zero.

For RQ1, report missing first responses by group alongside timing summaries.
For RQ2, show all status categories and explicit denominators. For RQ3, restrict
binary comparisons to reviewed closed requests with successful/unsuccessful
outcomes and known response times. Report excluded records and reasons.
Tests must be chosen after assessing distributions, counts and agency clustering.
Association does not establish that speed causes success.

## Limitations to assess

Incomplete public coverage, self-selection into eFOI, uneven agency participation,
sampling imbalance, unobserved replies, date precision and changing statuses may
affect interpretation. Fix a status observation cutoff and document follow-up time
before analysis. Portal records do not measure all Philippine information requests.
