# Data dictionary: `data/processed/efoi_2025.csv`

One row per sampled eFOI request filed in 2025. Times are Manila local time as shown on the portal.

| Column | Type | Description |
| --- | --- | --- |
| `tracking_number` | text | Portal tracking number, e.g. `DOJ-416806374185`. Unique key. |
| `title` | text | Request title as published |
| `agency_name` | text | Receiving agency, e.g. `Department of Justice(DOJ)` |
| `agency_code` | text | Agency slug from the URL, e.g. `doj` |
| `agency_group` | category | NGA, GOCC, SUC, WATER-DISTRICT, LGU, LEA (agency directory) |
| `filed_at` | datetime | Filing date and time (to the minute) |
| `filing_quarter` | category | Q1–Q4 of 2025 |
| `purpose` | text | Requester-stated purpose |
| `status` | category | Portal status on the scrape date |
| `outcome` | category | successful / partially successful / unsuccessful / referred / open (see methodology) |
| `is_final` | bool | Status is SUCCESSFUL, PARTIALLY SUCCESSFUL, DENIED or CLOSED |
| `is_successful` | bool | Status is SUCCESSFUL or PARTIALLY SUCCESSFUL |
| `has_agency_reply` | bool | At least one agency message exists |
| `first_agency_reply_at` | datetime | Earliest agency message (to the minute); empty if none |
| `first_response_days` | float | Days from filing to the first agency message; empty if none |
| `last_agency_reply_at` | datetime | Latest agency message |
| `processing_at` | datetime | "Processing" timestamp on the status timeline, if shown |
| `final_status_at` | datetime | Final-status timestamp on the timeline, if shown |
| `days_to_final_status` | float | Days from filing to `final_status_at` |
| `n_agency_messages` | int | Number of agency messages |
| `n_requester_messages` | int | Number of requester messages |
| `flag_reply_before_filing` | bool | First reply earlier than filing (data error, kept for review) |
| `stratum_population` | int | 2025 requests in this agency group × quarter |
| `stratum_sample` | int | Sampled requests in this stratum |
| `sampling_weight` | float | `stratum_population / stratum_sample` |
| `detail_url` | url | Source page |
| `scraped_at` | datetime | When the detail page was scraped |

`data/processed/frame_2025.csv` holds every public 2025 request, with the listing-level columns:
`tracking_number` through `purpose`, plus `status`, `outcome`, `filing_quarter` and `detail_url`.
