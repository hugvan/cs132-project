"""Copy reviewed figure exports into the self-contained GitHub Pages directory.

Run after regenerating figures: python scripts/sync_site_figures.py.
"""
from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]
FIGURES = (
    "rq1_median_and_noreply.png",
    "rq1_response_time_distribution.png",
    "rq2_outcome_shares.png",
    "rq3_speed_and_success.png",
    "nutshell.png",
    "nutshell.pdf",
)


def main():
    source = ROOT / "reports/figures"
    destination = ROOT / "docs/assets/figures"
    missing = [name for name in FIGURES if not (source / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing reviewed figures: {', '.join(missing)}")
    destination.mkdir(parents=True, exist_ok=True)
    for name in FIGURES:
        copyfile(source / name, destination / name)
    print(f"Copied {len(FIGURES)} reviewed figures to {destination}")


if __name__ == "__main__":
    main()
