# Data dictionary

CSV encoding: UTF-8. One request per tracking number. All template columns must
exist; some cell values may be blank as described below. Blank means missing,
never zero. Use ISO 8601 timestamps with offsets where available.

| Field | Meaning / validation |
| --- | --- |
| `tracking_number` | Required string, unique request identifier; preserve leading zeros. |
| `agency` | Required source agency name. |
| `agency_group` | NGA, GOCC, SUC, WATER DISTRICT, LGU, LEA; blank is flagged, never inferred. |
| `filed_at` | Required filing timestamp/date in 2025 in Asia/Manila. |
| `first_response_at` | First agency reply after filing; blank when unavailable; may be after 2025. |
| `status` | Exact source status at observation time; unmapped labels remain unknown. |
| `purpose` | Optional source purpose; review for personal information before sharing. |
| `source_url` | Required HTTP(S) source page/download URL for provenance. |
| `collected_at` | Required date/time at which the record/status was observed or extracted. |

Example date formats (not observations): `2025-06-01` or
`2025-06-01T14:30:00+08:00`. A timestamp without an offset is interpreted as
Asia/Manila; record that assumption in the collection log. Date-only records retain
their date-only representation. Comparisons with date-only values use calendar
dates; precise elapsed hours cannot be recovered.

## Derived output fields

| Field | Meaning |
| --- | --- |
| `filing_quarter` | Q1–Q4 in Asia/Manila. |
| `first_response_days` | Nonnegative calendar days from filing; blank for missing replies. |
| `response_time_precision` | `timestamp`, `date`, `mixed`, or `missing`. |
| `outcome` | Reviewed mapping, or `unknown` when unmapped. |
| `is_closed` | `true`/`false` from mapping; blank if unknown. |
| `quality_flags` | Semicolon-separated warning codes for the retained row. |

## Status mapping

`status_mapping.csv` has `status,outcome,is_closed,definition,source_url`.
Matching ignores case and repeated whitespace, while preserving the original
input status. Every mapping must have a definition and supporting URL. Successful
and unsuccessful outcomes must be marked closed; pending outcomes must be open.
This is a research coding rule, not a claim about official status semantics.
The header-only template intentionally supplies no classifications.
