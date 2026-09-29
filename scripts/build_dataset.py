"""Turn scraped eFOI pages into the study dataset.

  python scripts/build_dataset.py frame     # data/raw/listing.csv -> data/processed/frame_2025.csv
  python scripts/build_dataset.py sample    # frame -> data/interim/sample.csv (stratified, seed 132)
  python scripts/build_dataset.py dataset   # sample + data/raw/details.csv -> data/processed/efoi_2025.csv

Between `sample` and `dataset`, run: python scripts/scrape_efoi.py details --sample data/interim/sample.csv
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, INTERIM, PROCESSED = ROOT / "data/raw", ROOT / "data/interim", ROOT / "data/processed"
SEED = 132
PER_GROUP = 300  # target sample size per agency group; smaller groups are taken in full

# Portal statuses -> analysis categories. "Final" statuses are the closed requests used in RQ3.
OUTCOME = {
    "SUCCESSFUL": "successful",
    "PARTIALLY SUCCESSFUL": "partially successful",
    "DENIED": "unsuccessful",
    "CLOSED": "unsuccessful",
    "REFERRED": "referred",
    "PENDING": "open",
    "ACCEPTED": "open",
    "PROCESSING": "open",
    "AWAITING CLARIFICATION": "open",
}
FINAL = {"SUCCESSFUL", "PARTIALLY SUCCESSFUL", "DENIED", "CLOSED"}


def agencies():
    a = pd.read_csv(RAW / "agencies.csv")
    a["agency_code"] = a["agency_url"].str.rstrip("/").str.split("/").str[-1].str.lower()
    return a[["agency_code", "agency_group"]].drop_duplicates("agency_code")


def cmd_frame():
    df = pd.read_csv(RAW / "listing.csv", dtype=str)
    n_raw = len(df)
    df = df.drop_duplicates("tracking_number")
    df["filed_at"] = pd.to_datetime(df["filed_at"])
    df = df[df["filed_at"].dt.year == 2025].copy()
    df["agency_code"] = df["agency_code"].str.lower()
    df = df.merge(agencies(), on="agency_code", how="left")
    df["filing_quarter"] = "Q" + df["filed_at"].dt.quarter.astype(str)
    df["outcome"] = df["status"].map(OUTCOME)
    df = df.drop(columns=["page", "scraped_at"]).sort_values("filed_at")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "frame_2025.csv", index=False)

    print(f"{n_raw} listing rows -> {len(df)} unique 2025 requests")
    print(f"missing agency group: {df['agency_group'].isna().sum()} rows "
          f"({sorted(df.loc[df['agency_group'].isna(), 'agency_code'].unique())[:10]})")
    print(f"unmapped statuses: {sorted(df.loc[df['outcome'].isna(), 'status'].unique())}")
    print(pd.crosstab(df["agency_group"].fillna("UNKNOWN"), df["filing_quarter"], margins=True))


def cmd_sample():
    """Stratify by agency group x quarter. Each group gets up to PER_GROUP requests, split
    across quarters in proportion to that group's filings; groups smaller than that are taken
    in full. Sampling weight = stratum population / stratum sample size."""
    frame = pd.read_csv(PROCESSED / "frame_2025.csv", dtype=str).dropna(subset=["agency_group"])
    rng = np.random.default_rng(SEED)
    parts = []
    for group, g in frame.groupby("agency_group"):
        n_group = min(PER_GROUP, len(g))
        quota = (g["filing_quarter"].value_counts(normalize=True) * n_group).round().astype(int)
        for quarter, stratum in g.groupby("filing_quarter"):
            n = min(len(stratum), max(1, quota.get(quarter, 0)))
            picked = stratum.sample(n=n, random_state=rng.integers(1 << 31))
            picked = picked.assign(stratum_population=len(stratum), stratum_sample=n,
                                   sampling_weight=len(stratum) / n)
            parts.append(picked)
    sample = pd.concat(parts).sort_values("filed_at")
    INTERIM.mkdir(parents=True, exist_ok=True)
    sample.to_csv(INTERIM / "sample.csv", index=False)
    print(f"sampled {len(sample)} of {len(frame)} requests (seed {SEED})")
    print(pd.crosstab(sample["agency_group"], sample["filing_quarter"], margins=True))


def cmd_dataset():
    sample = pd.read_csv(INTERIM / "sample.csv", dtype=str)
    details = pd.read_csv(RAW / "details.csv", dtype=str).drop_duplicates("tracking_number", keep="last")
    keep = ["tracking_number", "status", "processing_at", "final_status_at", "first_agency_reply_at",
            "last_agency_reply_at", "n_agency_messages", "n_requester_messages", "scraped_at"]
    df = sample.drop(columns=["status", "outcome"]).merge(details[keep], on="tracking_number", how="inner")

    for col in ["filed_at", "processing_at", "final_status_at", "first_agency_reply_at", "last_agency_reply_at"]:
        df[col] = pd.to_datetime(df[col])
    df["outcome"] = df["status"].map(OUTCOME)
    df["is_final"] = df["status"].isin(FINAL)
    df["is_successful"] = df["status"].isin({"SUCCESSFUL", "PARTIALLY SUCCESSFUL"})
    df["has_agency_reply"] = df["first_agency_reply_at"].notna()
    df["first_response_days"] = ((df["first_agency_reply_at"] - df["filed_at"]).dt.total_seconds() / 86400).round(3)
    df["days_to_final_status"] = ((df["final_status_at"] - df["filed_at"]).dt.total_seconds() / 86400).round(3)
    # Replies timestamped before filing would be parsing/source errors; flag rather than drop.
    df["flag_reply_before_filing"] = df["first_response_days"] < 0

    cols = ["tracking_number", "title", "agency_name", "agency_code", "agency_group", "filed_at",
            "filing_quarter", "purpose", "status", "outcome", "is_final", "is_successful",
            "has_agency_reply", "first_agency_reply_at", "first_response_days", "last_agency_reply_at",
            "processing_at", "final_status_at", "days_to_final_status", "n_agency_messages",
            "n_requester_messages", "flag_reply_before_filing", "stratum_population", "stratum_sample",
            "sampling_weight", "detail_url", "scraped_at"]
    df = df[cols].sort_values("filed_at")
    df.to_csv(PROCESSED / "efoi_2025.csv", index=False)

    # 100 random rows for the team's manual check against the live pages (proposal: Validation).
    check = df.sample(n=min(100, len(df)), random_state=SEED)[
        ["tracking_number", "detail_url", "agency_group", "filed_at", "first_agency_reply_at", "status"]]
    check = check.assign(checked_by="", filed_at_ok="", first_reply_ok="", status_ok="", notes="")
    check.to_csv(PROCESSED / "validation_100.csv", index=False)

    print(f"{len(df)} of {len(sample)} sampled requests have detail data "
          f"({len(sample) - len(df)} missing -> see data/raw/errors.csv)")
    print(f"no agency reply: {(~df['has_agency_reply']).sum()}   "
          f"reply-before-filing flags: {df['flag_reply_before_filing'].sum()}")
    print(df.groupby("agency_group")["first_response_days"].describe().round(2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["frame", "sample", "dataset"])
    {"frame": cmd_frame, "sample": cmd_sample, "dataset": cmd_dataset}[ap.parse_args().cmd]()


if __name__ == "__main__":
    main()
