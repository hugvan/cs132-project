"""Nutshell plot for the EDA submission.

Follows the PilipiNuts 2024 guidebook: Roboto, dark background #1B181C,
white text, the guidebook palette, no grid, and no tick marks.
The export is 1920 by 1080 pixels. Roboto is Apache 2.0; see assets/fonts/LICENSE.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from scipy.stats import mannwhitneyu

from analysis import (
    CLOSED_OUTCOMES,
    GROUP_ORDER,
    LABELS,
    SUCCESSFUL_OUTCOMES,
    collected_weights,
    weighted_mannwhitney,
    weighted_mean,
    weighted_median,
)

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
OUT_DIR = ROOT / "reports" / "figures"
ALPHA = 0.05

BG = "#1B181C"
TEXT = "#FFFFFF"
MUTED = "#C8C4CC"
BLUE = "#648FFF"
MAGENTA = "#DC267F"
AMBER = "#FFB000"

POINT_COLOR = {
    "WATER-DISTRICT": MAGENTA,
    "LGU": AMBER,
}


def font(name):
    path = FONT_DIR / name
    fm.fontManager.addfont(str(path))
    return fm.FontProperties(fname=str(path))


def load():
    frame = pd.read_csv(ROOT / "data" / "processed" / "frame_2025.csv")
    sample = pd.read_csv(ROOT / "data" / "processed" / "efoi_2025.csv")
    sample["first_response_days"] = pd.to_numeric(sample["first_response_days"], errors="coerce")
    sample["sampling_weight"] = collected_weights(sample)
    return frame, sample


def group_summary(frame, sample):
    rows = []
    for group in GROUP_ORDER:
        group_frame = frame.loc[frame["agency_group"] == group]
        group_sample = sample.loc[sample["agency_group"] == group]
        replied = group_sample.loc[group_sample["first_response_days"].notna()]
        rows.append({
            "agency_group": group,
            "success_rate": group_frame["outcome"].isin(SUCCESSFUL_OUTCOMES).mean(),
            "median_days": weighted_median(replied["first_response_days"], replied["sampling_weight"]),
            "no_reply_share": weighted_mean(
                group_sample["first_response_days"].isna().astype(float),
                group_sample["sampling_weight"],
            ),
            "n": len(group_frame),
        })
    return pd.DataFrame(rows).set_index("agency_group")


def reply_comparison(sample):
    """Weighted comparison of first-response time for closed requests that got a reply."""
    closed = sample.loc[
        sample["outcome"].isin(CLOSED_OUTCOMES) & sample["first_response_days"].notna()
    ].copy()
    success = closed["outcome"].isin(SUCCESSFUL_OUTCOMES).to_numpy()
    probability, p_value = weighted_mannwhitney(
        closed["first_response_days"], closed["sampling_weight"], success
    )
    succeeded = closed.loc[success]
    failed = closed.loc[~success]
    within_p = {}
    for group in GROUP_ORDER:
        part = closed.loc[closed["agency_group"] == group]
        part_success = part["outcome"].isin(SUCCESSFUL_OUTCOMES)
        result = mannwhitneyu(
            part.loc[part_success, "first_response_days"],
            part.loc[~part_success, "first_response_days"],
            alternative="two-sided",
        )
        within_p[group] = result.pvalue
    return {
        "n": len(closed),
        "success_median": weighted_median(succeeded["first_response_days"], succeeded["sampling_weight"]),
        "failure_median": weighted_median(failed["first_response_days"], failed["sampling_weight"]),
        "probability": probability,
        "p_value": p_value,
        "within_p": within_p,
    }


def caption(summary, comparison):
    lea, lgu, water, nga = (summary.loc[group] for group in ("LEA", "LGU", "WATER-DISTRICT", "NGA"))
    within = (
        "Inside every agency group that comparison stays above 0.05."
        if all(p >= ALPHA for p in comparison["within_p"].values())
        else "Inside at least one agency group that comparison is below 0.05."
    )
    text = (
        "A fast first reply does not mean an eFOI request succeeds. Among "
        f"{comparison['n']:,} closed requests with a reply, the weighted median wait was "
        f"{comparison['success_median']:.1f} days for a success and "
        f"{comparison['failure_median']:.1f} days for a failure. A weighted Mann–Whitney test "
        f"found no evidence of a link (p = {comparison['p_value']:.2f}). {within} The office still "
        f"matters. Law enforcement replies in {lea['median_days']:.1f} days, and "
        f"{lea['success_rate']:.0%} of its requests succeed. Local governments take "
        f"{lgu['median_days']:.1f} days, and {lgu['success_rate']:.0%} succeed. Water districts "
        f"reply in {water['median_days']:.1f} days when they reply, but "
        f"{water['no_reply_share']:.0%} get no reply, and {water['success_rate']:.0%} succeed. "
        f"National agencies, most of the record, succeed {nga['success_rate']:.0%} of the time. "
        "Success includes a partial success and counts every public 2025 request, including "
        "those still open. The first agency message may be only an acknowledgment. Status was "
        "observed on 29 September 2026, so later requests have had less time to close."
    )
    return text


def draw(summary):
    regular = font("Roboto-Regular.ttf")
    medium = font("Roboto-Medium.ttf")
    bold = font("Roboto-Bold.ttf")
    light = font("Roboto-Light.ttf")

    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    for group, row in summary.iterrows():
        ax.scatter(
            row["median_days"],
            row["success_rate"] * 100,
            s=420,
            color=POINT_COLOR.get(group, BLUE),
            linewidths=0,
            zorder=3,
        )

    offsets = {
        "LEA": (14, -36),
        "WATER-DISTRICT": (18, -18),
        "NGA": (14, 28),
        "GOCC": (16, 14),
        "SUC": (16, -24),
        "LGU": (-16, 12),
    }
    align = {"LGU": "right"}
    for group, row in summary.iterrows():
        ax.annotate(
            f"{LABELS[group]}\n{row['median_days']:.1f} days  ·  {row['success_rate']:.0%}",
            (row["median_days"], row["success_rate"] * 100),
            xytext=offsets[group],
            textcoords="offset points",
            ha=align.get(group, "left"),
            va="center",
            color=TEXT,
            fontproperties=medium,
            fontsize=16,
            linespacing=1.35,
            zorder=4,
        )

    ax.set_xlim(0, 6.4)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Median days to first reply", fontproperties=regular, fontsize=20, color=TEXT, labelpad=14)
    ax.set_ylabel("Success rate", fontproperties=regular, fontsize=20, color=TEXT, labelpad=14)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.tick_params(axis="both", which="both", length=0, labelsize=16, colors=TEXT, pad=8)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontproperties(regular)
        label.set_fontsize(16)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(TEXT)
    ax.spines["bottom"].set_color(TEXT)
    ax.grid(False)

    fig.suptitle("A fast reply is not a yes", fontproperties=bold, fontsize=48, color=TEXT, x=0.08, ha="left", y=0.94)
    fig.text(
        0.08,
        0.835,
        "How fast a group replies says little about whether its requests succeed.",
        fontproperties=regular,
        fontsize=20,
        color=MUTED,
        ha="left",
    )
    fig.text(
        0.08,
        0.058,
        "Source: eFOI portal, public requests filed in 2025, collected 29 September 2026.",
        fontproperties=light,
        fontsize=15,
        color=MUTED,
        ha="left",
    )
    fig.text(
        0.08,
        0.032,
        "Success rate is the share of all requests that succeeded or partly succeeded, including those still open. Median wait is weighted.",
        fontproperties=light,
        fontsize=15,
        color=MUTED,
        ha="left",
    )

    fig.subplots_adjust(left=0.08, right=0.94, top=0.78, bottom=0.16)
    return fig


def main():
    frame, sample = load()
    summary = group_summary(frame, sample)
    comparison = reply_comparison(sample)
    headline = "A fast reply is not a yes"
    text = caption(summary, comparison)
    headline_words = len(headline.split())
    caption_words = len(text.split())
    if headline_words > 10:
        raise SystemExit(f"Headline is {headline_words} words")
    if caption_words > 150:
        raise SystemExit(f"Caption is {caption_words} words")

    fig = draw(summary)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = OUT_DIR / "nutshell.png"
    pdf_path = OUT_DIR / "nutshell.pdf"
    fig.savefig(png_path, dpi=100)
    plt.close(fig)

    image = Image.open(png_path).convert("RGB")
    if image.size != (1920, 1080):
        raise SystemExit(f"Expected 1920x1080, got {image.size}")
    image.save(pdf_path, "PDF", resolution=72.0)

    notes_path = ROOT / "reports" / "nutshell.md"
    notes_path.write_text(
        f"# Nutshell\n\n"
        f"**Headline** ({headline_words} words)\n\n"
        f"{headline}\n\n"
        f"**Caption** ({caption_words} words)\n\n"
        f"{text}\n"
    )
    print(summary.round(3).to_string())
    print(
        f"weighted medians {comparison['success_median']:.3f} vs {comparison['failure_median']:.3f}, "
        f"P = {comparison['probability']:.3f}, p = {comparison['p_value']:.3f}, n = {comparison['n']}"
    )
    print(f"headline {headline_words} words")
    print(f"caption {caption_words} words")
    print(png_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
