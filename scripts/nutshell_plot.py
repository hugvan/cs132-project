"""Render an outcome-colored request swarm at 1920×1080 pixels.

Each equal-sized point is one sampled request, without sampling weights.
Horizontal positions preserve observed reply times on a logarithmic scale;
vertical offsets prevent overlap and have no quantitative meaning.
Run from any directory: python scripts/nutshell_plot.py.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image

from analysis import GROUP_ORDER, LABELS, SUCCESSFUL_OUTCOMES

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports/figures"
BG, TEXT, MUTED = "#1B181C", "#FFFFFF", "#C8C4CC"
COLORS = {"successful": "#648FFF", "partial": "#A3BCFF", "denied": "#DC267F", "closed": "#F08EBB", "other": "#A9A3AE"}
REFERENCE_DAYS = 15  # Calendar-time reference, not a working-day compliance cutoff.
HEADLINE = "eFOI Response Times and Request Outcomes, 2025"
WIDTH, HEIGHT = 1920, 1080
# Positions are in export pixels, so the packing matches the visible dot size.
TIME_LEFT, TIME_RIGHT = 365, 1520
NO_REPLY_X = 1715
GRAPH_RAISE = 45
TIME_MIN, TIME_MAX = 1 / 1440, 730  # one minute through two years, in days
DOT_DIAMETER, SEPARATION = 5.4, 6.2


def load():
    sample = pd.read_csv(ROOT / "data/processed/efoi_2025.csv")
    sample["first_response_days"] = pd.to_numeric(sample["first_response_days"], errors="raise")
    if sample["tracking_number"].duplicated().any():
        raise ValueError("Each point must represent a unique request")
    times = sample["first_response_days"].dropna()
    if not times.between(TIME_MIN, TIME_MAX).all():
        raise ValueError("Response times fall outside the displayed time scale")
    if not sample["outcome"].isin([*SUCCESSFUL_OUTCOMES, "unsuccessful", "open", "referred"]).all():
        raise ValueError("An outcome is missing from the color key")
    if not sample["status"].isin([
        "SUCCESSFUL", "PARTIALLY SUCCESSFUL", "DENIED", "CLOSED", "PENDING",
        "ACCEPTED", "PROCESSING", "AWAITING CLARIFICATION", "REFERRED",
    ]).all():
        raise ValueError("A portal status is missing from the color key")
    return sample


def time_position(days):
    fraction = (np.log10(days) - np.log10(TIME_MIN)) / np.log10(TIME_MAX / TIME_MIN)
    return TIME_LEFT + fraction * (TIME_RIGHT - TIME_LEFT)


def swarm_offsets(x):
    """Pack points without moving their x coordinates; return original row order."""
    offsets = np.zeros(len(x))
    placed = []
    for index in np.argsort(x, kind="stable"):
        current = x[index]
        placed = [(px, py) for px, py in placed if current - px < SEPARATION]
        candidates = [0.0]
        for px, py in placed:
            dy = np.sqrt(max(0, SEPARATION**2 - (current - px)**2)) + 1e-6
            candidates.extend([py + dy, py - dy])
        # Alternate the tie preference to avoid a persistent bias above a row.
        candidates.sort(key=lambda y: (abs(y), y if index % 2 else -y))
        for y in candidates:
            if all((current - px)**2 + (y - py)**2 >= SEPARATION**2 - 1e-7
                   for px, py in placed):
                offsets[index] = y
                placed.append((current, y))
                break
        else:
            raise RuntimeError("Could not place a request in the swarm")
    return offsets


def missing_positions(n):
    """A compact hexagonal cluster in a categorical column, not on the time scale."""
    if not n:
        return np.empty((0, 2))
    radius = int(np.ceil(np.sqrt(n))) + 1
    candidates = []
    for row in range(-radius, radius + 1):
        for col in range(-radius, radius + 1):
            x = (col + .5 * (row % 2)) * SEPARATION
            y = row * SEPARATION * np.sqrt(3) / 2
            candidates.append((x, y))
    candidates.sort(key=lambda p: (p[0]**2 + p[1]**2, p[1], p[0]))
    result = np.array(candidates[:n])
    return result - result.mean(axis=0)


def outcome_colors(part):
    return [COLORS["denied"] if status == "DENIED" else
            COLORS["closed"] if status == "CLOSED" else
            COLORS["successful"] if status == "SUCCESSFUL" else
            COLORS["partial"] if status == "PARTIALLY SUCCESSFUL" else
            COLORS["other"] for status in part["status"]]


def caption(sample):
    return (
        f"Response times and observed outcomes for {len(sample):,} sampled public eFOI requests filed in 2025. "
        "Each equal-sized point represents one request. Horizontal positions indicate elapsed time to the first "
        "agency reply on a logarithmic scale; vertical offsets prevent overlap and have no numerical meaning. "
        "Requests without an agency reply occupy a separate categorical column. Blue indicates successful "
        "requests; light blue indicates partially successful requests; dark pink indicates denied requests; light pink indicates closed requests; gray includes open and "
        "referred requests. The sample is stratified by agency group and filing quarter; points are unweighted "
        "and do not represent population proportions. Statuses were observed on 29 September 2026. "
        "A first reply may be an acknowledgment. The line marks 15 calendar days, not legal compliance: "
        "EO No. 2 specifies 15 working days for access decisions, with extensions possible."
    )


def draw(sample):
    for path in (ROOT / "assets/fonts").glob("*.ttf"):
        fm.fontManager.addfont(str(path))
    plt.rcParams.update({"font.family": "Roboto", "text.color": TEXT, "pdf.fonttype": 42})
    fig = plt.figure(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    ax.set(xlim=(0, WIDTH), ylim=(HEIGHT, 0))
    ax.set_axis_off()

    def text(x, y, label, size=14, color=TEXT, **kwargs):
        ax.text(x, y, label, fontsize=size, color=color, va="center", **kwargs)

    text(WIDTH / 2, 85, HEADLINE, 32, weight="bold", ha="center")
    text((TIME_LEFT + TIME_RIGHT) / 2, 220 - GRAPH_RAISE, "Time to first agency reply · calendar time", 17, ha="center")
    text(NO_REPLY_X, 220 - GRAPH_RAISE, "No reply", 17, ha="center")
    reference_x = time_position(REFERENCE_DAYS)
    ax.plot([reference_x, reference_x], [255 - GRAPH_RAISE, 900 - GRAPH_RAISE],
            color="#FFB000", linewidth=1, linestyle=(0, (5, 5)), alpha=.85, zorder=1)
    text(reference_x, 242 - GRAPH_RAISE, "15 calendar days", 10, "#FFB000", ha="center")
    # A categorical break prevents the no-reply column from implying elapsed time.
    ax.plot([1605, 1605], [255 - GRAPH_RAISE, 900 - GRAPH_RAISE], color="#514B55", lw=1, ls=(0, (3, 6)))
    dot_size = (DOT_DIAMETER * 72 / 100)**2
    total = 0
    max_offset = 0
    rng = np.random.default_rng(132)
    for i, group in enumerate(GROUP_ORDER):
        center = [290, 390, 490, 620, 750, 850][i] - GRAPH_RAISE
        part = sample.loc[sample["agency_group"] == group]
        replied = part.dropna(subset=["first_response_days"])
        missing = part.loc[part["first_response_days"].isna()]
        label = LABELS[group].replace("National government agencies", "National agencies")
        text(320, center - 9, label, 15, ha="right")
        text(320, center + 17, f"n = {len(part):,}", 12, MUTED, ha="right")
        x = time_position(replied["first_response_days"].to_numpy())
        y = swarm_offsets(x)
        max_offset = max(max_offset, float(np.abs(y).max()))
        if np.abs(y).max() > (96 if group == "WATER-DISTRICT" else 46):
            raise ValueError(f"Swarm exceeds its row height: {group}")
        ax.scatter(x, center + y, s=dot_size, c=outcome_colors(replied), linewidths=0, zorder=3)
        positions = missing_positions(len(missing))
        # Mix outcomes spatially without assigning quantitative meaning to position.
        positions = positions[rng.permutation(len(positions))]
        ax.scatter(NO_REPLY_X + positions[:, 0], center + positions[:, 1],
                   s=dot_size, c=outcome_colors(missing), linewidths=0, zorder=3)
        total += len(x) + len(positions)
    if total != len(sample):
        raise AssertionError("Some requests were not plotted")

    ax.plot([TIME_LEFT, TIME_RIGHT], [900 - GRAPH_RAISE, 900 - GRAPH_RAISE], color=MUTED, lw=.8)
    ticks = [(5 / 1440, "5 min"), (1 / 24, "1 hour"), (.25, "6 hours"),
             (1, "1 day"), (7, "7 days"), (30, "30 days"), (90, "90 days"), (365, "1 year")]
    for days, label in ticks:
        text(time_position(days), 925 - GRAPH_RAISE, label, 12, MUTED, ha="center")
    text((TIME_LEFT + TIME_RIGHT) / 2, 956 - GRAPH_RAISE, "Logarithmic time scale", 11, MUTED, ha="center")

    legend_items = [("Successful", COLORS["successful"]), ("Partially successful", COLORS["partial"]),
                    ("Denied", COLORS["denied"]), ("Closed", COLORS["closed"]),
                    ("Open / referred", COLORS["other"])]
    handles = [Line2D([], [], marker="o", color=color, linestyle="none", markersize=7, label=label)
               for label, color in legend_items]
    ax.legend(handles=handles, loc="center", bbox_to_anchor=(.53, .065 + GRAPH_RAISE / HEIGHT), ncol=5,
              frameon=False, labelcolor=TEXT, fontsize=13, handletextpad=.5, columnspacing=2.5)
    footer_font = fm.FontProperties(fname=str(ROOT / "assets/fonts/Roboto-CondensedRegular.ttf"))
    footer_lines = [
        "Data: eFOI portal, 2025 requests · Observed 29 September 2026 · Unweighted stratified sample",
        "Chart: V. Aquino, E. Lim, J. Mayuyu, C. Sim, PILIPINUTS 2026",
    ]
    for y, line in zip((1028, 1050), footer_lines):
        text(WIDTH - 85, y, line, 11, TEXT, ha="right", fontproperties=footer_font)
    print(f"Plotted {total:,} requests; largest vertical swarm offset: {max_offset:.1f} px")
    return fig


def main():
    sample = load()
    fig = draw(sample)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    png = OUT_DIR / "nutshell.png"
    fig.savefig(png, dpi=100, facecolor=BG)
    fig.savefig(OUT_DIR / "nutshell.pdf", facecolor=BG)
    plt.close(fig)
    with Image.open(png) as image:
        assert image.size == (WIDTH, HEIGHT), image.size
    description = caption(sample)
    assert len(HEADLINE.split()) <= 10
    assert len(description.split()) <= 150
    (ROOT / "reports/nutshell.md").write_text(
        f"# Nutshell\n\n**Headline** ({len(HEADLINE.split())} words)\n\n{HEADLINE}\n\n"
        f"**Caption** ({len(description.split())} words)\n\n{description}\n"
    )
    print(f"Rendered {png} and nutshell.pdf; caption: {len(description.split())} words")


if __name__ == "__main__":
    main()
