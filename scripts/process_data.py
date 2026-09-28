"""Validate a locally supplied eFOI CSV. Never downloads or publishes data."""

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

MANILA = timezone(timedelta(hours=8))
FIELDS = "tracking_number agency agency_group filed_at first_response_at status purpose source_url collected_at".split()
DERIVED = "filing_quarter first_response_days response_time_precision outcome is_closed quality_flags".split()
GROUPS = {"NGA", "GOCC", "SUC", "WATER DISTRICT", "LGU", "LEA"}
MAP_FIELDS = "status outcome is_closed definition source_url".split()


def read_csv(path, fields):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or sorted(reader.fieldnames) != sorted(fields):
            raise ValueError(f"{path}: expected exactly these columns: {', '.join(fields)}")
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{path}: malformed CSV record near line {reader.line_num}")
            rows.append({key: value.strip() for key, value in row.items()})
        return rows


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def status_key(value):
    return " ".join(value.casefold().split())


def valid_url(value):
    try:
        parsed = urlparse(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not any(c.isspace() for c in value)
    except ValueError:
        return False


def load_mapping(path):
    result = {}
    for row in read_csv(path, MAP_FIELDS):
        key = status_key(row["status"])
        if not key or key in result:
            raise ValueError("Status mapping has an empty or duplicate status")
        if row["outcome"] not in {"successful", "unsuccessful", "pending", "other", "unknown"}:
            raise ValueError(f"Invalid outcome for status {row['status']}")
        if row["is_closed"] not in {"true", "false"}:
            raise ValueError("is_closed must be true or false")
        if row["outcome"] in {"successful", "unsuccessful"} and row["is_closed"] != "true":
            raise ValueError("Binary outcomes must be marked closed")
        if row["outcome"] == "pending" and row["is_closed"] != "false":
            raise ValueError("Pending outcomes must be marked open")
        if not row["definition"] or not valid_url(row["source_url"]):
            raise ValueError("Every status mapping needs a definition and HTTP(S) source URL")
        result[key] = row
    return result


def parse_date(value):
    # Reject compact ISO forms and ambiguous locale-specific dates.
    if len(value) < 10 or value[4] != "-" or value[7] != "-":
        raise ValueError("Use YYYY-MM-DD or an ISO timestamp")
    date_only = len(value) == 10
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=MANILA)
    return parsed.astimezone(MANILA), date_only


def earlier(left, right):
    if left[1] or right[1]:
        return left[0].date() < right[0].date()
    return left[0] < right[0]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def process(input_path, mapping_path, output_dir):
    rows = read_csv(input_path, FIELDS)
    mapping = load_mapping(mapping_path)
    output = Path(output_dir)
    names = ["requests_clean.csv", "requests_quarantine.csv", "issues.csv", "quality_report.json"]
    if any((output / name).resolve() in {Path(input_path).resolve(), Path(mapping_path).resolve()} for name in names):
        raise ValueError("Output would overwrite an input file; choose another output directory")
    by_id = defaultdict(list)
    for index, row in enumerate(rows, 2):
        if row["tracking_number"]:
            by_id[row["tracking_number"]].append((index, row))
    conflicts, repeats = set(), set()
    for entries in by_id.values():
        if len(entries) > 1:
            if any(row != entries[0][1] for _, row in entries[1:]):
                conflicts.update(index for index, _ in entries)
            else:
                repeats.update(index for index, _ in entries[1:])
    clean, quarantine, issues = [], [], []
    for index, raw in enumerate(rows, 2):
        row = dict(raw)
        errors, warnings = [], []
        if index in repeats:
            issues.append({"input_record": index, "tracking_number": row["tracking_number"], "severity": "info", "code": "duplicate_identical_removed"})
            continue
        if index in conflicts:
            errors.append("duplicate_conflicting")
        for field in ("tracking_number", "agency"):
            if not row[field]:
                errors.append(f"missing_{field}")
        row["agency_group"] = " ".join(row["agency_group"].upper().split())
        if not row["agency_group"]:
            warnings.append("missing_agency_group")
        elif row["agency_group"] not in GROUPS:
            errors.append("invalid_agency_group")
        if not valid_url(row["source_url"]):
            errors.append("invalid_source_url")
        dates = {}
        for field in ("filed_at", "first_response_at", "collected_at"):
            if not row[field]:
                (warnings if field == "first_response_at" else errors).append(f"missing_{field}")
            else:
                try:
                    dates[field] = parse_date(row[field])
                except ValueError:
                    errors.append(f"invalid_{field}")
        filed, reply, collected = (dates.get(field) for field in ("filed_at", "first_response_at", "collected_at"))
        if filed and filed[0].year != 2025:
            errors.append("filing_outside_2025")
        if filed and reply and earlier(reply, filed):
            errors.append("response_before_filing")
        if filed and collected and earlier(collected, filed):
            errors.append("collection_before_filing")
        if reply and collected and earlier(collected, reply):
            errors.append("response_after_collection")
        precision, duration = "missing", ""
        if filed and reply:
            precision = "date" if filed[1] and reply[1] else "mixed" if filed[1] or reply[1] else "timestamp"
            if precision == "mixed":
                warnings.append("mixed_date_precision")
            days = (reply[0].date() - filed[0].date()).days if precision != "timestamp" else (reply[0] - filed[0]).total_seconds() / 86400
            duration = str(round(days, 6))
        classification = mapping.get(status_key(row["status"]))
        if classification is None:
            warnings.append("unmapped_status")
        if not row["purpose"]:
            warnings.append("missing_purpose")
        for severity, codes in (("error", errors), ("warning", warnings)):
            issues.extend({"input_record": index, "tracking_number": raw["tracking_number"], "severity": severity, "code": code} for code in codes)
        if errors:
            quarantine.append({**raw, "input_record": index, "errors": ";".join(errors)})
            continue
        for field, (value, date_only) in dates.items():
            row[field] = value.date().isoformat() if date_only else value.isoformat()
        row.update(filing_quarter=f"Q{(filed[0].month - 1) // 3 + 1}", first_response_days=duration,
                   response_time_precision=precision, outcome=classification["outcome"] if classification else "unknown",
                   is_closed=classification["is_closed"] if classification else "", quality_flags=";".join(warnings))
        clean.append(row)
    n = len(clean)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_sha256": sha256(input_path), "status_mapping_sha256": sha256(mapping_path),
        "input_rows": len(rows), "clean_rows": n, "quarantined_rows": len(quarantine),
        "identical_duplicates_removed": len(repeats), "unique_clean_tracking_numbers": n,
        "issue_counts": dict(sorted(Counter(issue["code"] for issue in issues).items())),
        "missing_values_clean": {field: sum(not row[field] for row in clean) for field in FIELDS},
        "agency_groups_clean": dict(sorted(Counter(row["agency_group"] or "missing" for row in clean).items())),
        "filing_quarters_clean": dict(sorted(Counter(row["filing_quarter"] for row in clean).items())),
        "size_thresholds": {str(threshold): n >= threshold for threshold in (100, 500, 1000)},
        "note": "Structural validation only; manual review, source permissions and publication review are still required.",
    }
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / names[0], clean, FIELDS + DERIVED)
    write_csv(output / names[1], quarantine, FIELDS + ["input_record", "errors"])
    write_csv(output / names[2], issues, ["input_record", "tracking_number", "severity", "code"])
    (output / names[3]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--status-map", type=Path, default=Path("data/templates/status_mapping.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    try:
        report = process(args.input, args.status_map, args.output_dir)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"Error: {error}\n")
    print(f"Input: {report['input_rows']} | Clean: {report['clean_rows']} | Quarantined: {report['quarantined_rows']}")
    print(f"Review {args.output_dir / 'quality_report.json'} and issues.csv before analysis.")
    return 1 if report["quarantined_rows"] or not report["clean_rows"] else 0


if __name__ == "__main__":
    sys.exit(main())
