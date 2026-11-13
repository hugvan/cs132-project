"""Export the nutshell swarm layout for the interactive figure on the portfolio page.

Reuses the packing in nutshell_plot.py so every point sits exactly where it does in
reports/figures/nutshell.png (1920 x 1080 pixel space). Only four fields leave the
dataset: agency group, first-response days, the observed portal status category, and
an approximate keyword topic (scripts/request_topics.py). Titles themselves, URLs,
tracking numbers, and agency names are never exported.

Run after nutshell_plot.py: python scripts/export_nutshell_data.py
"""
import json
from pathlib import Path

import numpy as np

import nutshell_plot as nutshell
from analysis import GROUP_ORDER, LABELS
from request_topics import GENERAL, TOPICS, topic

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/assets/data/nutshell.json"
CENTERS = [290, 390, 490, 620, 750, 850]  # matches nutshell_plot.draw()


def status_key(status):
    return {"SUCCESSFUL": "successful", "PARTIALLY SUCCESSFUL": "partial",
            "DENIED": "denied", "CLOSED": "closed"}.get(status, "other")


def main():
    sample = nutshell.load()
    rng = np.random.default_rng(132)  # same seed and call order as nutshell_plot.draw()
    topic_names = [name for name, _ in TOPICS] + [GENERAL]
    topic_index = {name: i for i, name in enumerate(topic_names)}
    groups, points = [], []
    for i, group in enumerate(GROUP_ORDER):
        center = CENTERS[i] - nutshell.GRAPH_RAISE
        part = sample.loc[sample["agency_group"] == group]
        replied = part.dropna(subset=["first_response_days"])
        missing = part.loc[part["first_response_days"].isna()]
        x = nutshell.time_position(replied["first_response_days"].to_numpy())
        y = nutshell.swarm_offsets(x)
        for xi, yi, days, status, title in zip(x, y, replied["first_response_days"], replied["status"],
                                               replied["title"]):
            points.append([round(float(xi), 1), round(float(center + yi), 1), status_key(status),
                           round(float(days), 4), i, topic_index[topic(title)]])
        positions = nutshell.missing_positions(len(missing))
        positions = positions[rng.permutation(len(positions))]
        for (px, py), status, title in zip(positions, missing["status"], missing["title"]):
            points.append([round(float(nutshell.NO_REPLY_X + px), 1), round(float(center + py), 1),
                           status_key(status), None, i, topic_index[topic(title)]])
        groups.append({
            "id": group,
            "label": LABELS[group].replace("National government agencies", "National agencies"),
            "n": int(len(part)),
            "center": center,
        })
    if len(points) != len(sample):
        raise AssertionError("Some requests were not exported")

    payload = {
        "width": nutshell.WIDTH, "height": nutshell.HEIGHT,
        "timeLeft": nutshell.TIME_LEFT, "timeRight": nutshell.TIME_RIGHT,
        "timeMin": nutshell.TIME_MIN, "timeMax": nutshell.TIME_MAX,
        "noReplyX": nutshell.NO_REPLY_X, "raise": nutshell.GRAPH_RAISE,
        "referenceDays": nutshell.REFERENCE_DAYS,
        "referenceX": round(float(nutshell.time_position(nutshell.REFERENCE_DAYS)), 1),
        "dotDiameter": nutshell.DOT_DIAMETER,
        "colors": nutshell.COLORS,
        "groups": groups,
        "topics": topic_names,
        "fields": ["x", "y", "outcome", "days", "group", "topic"],
        "points": points,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"Exported {len(points):,} points to {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
