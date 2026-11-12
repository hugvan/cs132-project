"""Shared visual styling for portfolio EDA figures (no footnotes or inference)."""
from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.ticker import FixedLocator, NullLocator, PercentFormatter
import numpy as np

from analysis import LABELS, OUTCOME_ORDER

PAPER = "#f4f1ea"
INK = "#173e35"
ACCENT = "#8c4a32"
SAND = "#c4a574"
OPEN = "#d7cfc3"
SAGE = "#6e7c74"
MUTED = "#627069"
RULE = "#dddcd3"
OUTCOME_COLORS = dict(zip(OUTCOME_ORDER, [INK, SAND, ACCENT, OPEN, SAGE]))


def apply_style():
    for path in (Path(__file__).resolve().parents[1] / "assets/fonts").glob("*.ttf"):
        fm.fontManager.addfont(str(path))
    plt.rcParams.update({
        "font.family": "Roboto", "font.size": 12, "text.color": INK,
        "axes.facecolor": PAPER, "figure.facecolor": PAPER, "savefig.facecolor": PAPER,
        "axes.labelcolor": INK, "axes.labelsize": 12, "axes.labelpad": 12,
        "axes.edgecolor": RULE, "axes.titleweight": "bold", "axes.titlesize": 15,
        "axes.titlepad": 22, "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.grid": False,
        "xtick.color": MUTED, "ytick.color": INK, "xtick.major.size": 0,
        "ytick.major.size": 0, "xtick.major.pad": 10, "ytick.major.pad": 14,
        "legend.frameon": False, "legend.fontsize": 11, "pdf.fonttype": 42,
    })


def group_labels(order):
    return [LABELS[g].replace("National government agencies", "National agencies") for g in order]


def grid(ax, direction="x"):
    ax.set_axisbelow(True)
    ax.grid(axis=direction, which="major", color=RULE, linewidth=.65)


def response_summary(summary):
    apply_style()
    order = summary.sort_values("weighted_median_days").index.tolist()
    y = np.arange(len(order))
    medians = summary.loc[order, "weighted_median_days"].to_numpy()
    missing = summary.loc[order, "no_reply_share"].to_numpy() * 100
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.4), sharey=True)
    fig.subplots_adjust(left=.23, right=.96, bottom=.15, top=.76, wspace=.22)
    fig.suptitle("First Agency Responses to eFOI Requests, 2025", x=.5, y=.95, fontsize=19, weight="bold")
    for ax, values, color, limit, ticks, title in zip(
        axes, [medians, missing], [INK, ACCENT], [6, 34],
        [[0, 1, 2, 3, 4, 5], [0, 10, 20, 30]],
        ["Median response time", "No recorded agency reply"],
    ):
        ax.hlines(y, 0, values, color=color, linewidth=2, alpha=.27)
        ax.scatter(values, y, s=85, color=color, zorder=3)
        for i, v in enumerate(values):
            ax.annotate(f"{v:.1f}" if ax is axes[0] else f"{v:.1f}%", (v, i),
                        xytext=(12, 0), textcoords="offset points", va="center", color=color, weight="bold")
        ax.set(xlim=(0, limit), xticks=ticks, ylim=(-.6, len(y) - .4))
        ax.set_title(title)
        grid(ax)
    axes[0].set_yticks(y, group_labels(order))
    axes[0].set_xlabel("Weighted median · days")
    axes[1].set_xlabel("Weighted share of sampled requests")
    axes[1].xaxis.set_major_formatter(PercentFormatter(100))
    return fig, order


def response_distribution(sample, order):
    apply_style()
    values = [sample.loc[sample.agency_group.eq(g), "first_response_days"].dropna().to_numpy() for g in order]
    fig, ax = plt.subplots(figsize=(13, 6.4))
    fig.subplots_adjust(left=.23, right=.96, bottom=.17, top=.79)
    fig.suptitle("Distribution of First-Response Times, 2025", y=.95, fontsize=19, weight="bold")
    ax.set_title("Requests with a recorded agency reply · unweighted", fontsize=12, weight="normal", color=MUTED, pad=23)
    ax.boxplot(values, orientation="horizontal", tick_labels=group_labels(order), patch_artist=True,
               widths=.38, medianprops={"color": INK, "linewidth": 2},
               boxprops={"facecolor": to_rgba(SAGE, .3), "edgecolor": INK, "linewidth": 1},
               whiskerprops={"color": SAGE, "linewidth": 1}, capprops={"color": SAGE},
               flierprops={"marker": "o", "markersize": 3, "markerfacecolor": INK,
                           "markeredgecolor": "none", "alpha": .3})
    ax.set_xscale("log")
    ticks = [1 / 1440, 1 / 24, 1, 7, 30, 365]
    ax.set_xticks(ticks, ["1 minute", "1 hour", "1 day", "7 days", "30 days", "1 year"])
    ax.set_xlim(.0005, 800)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlabel("Time to first agency reply · logarithmic scale")
    grid(ax)
    return fig


def outcome_shares(shares, summary):
    apply_style()
    order = summary.sort_values("success_rate").index.tolist()
    y = np.arange(len(order))
    fig, ax = plt.subplots(figsize=(13, 6.8))
    fig.subplots_adjust(left=.23, right=.88, bottom=.14, top=.70)
    fig.suptitle("eFOI Request Outcomes by Agency Group, 2025", y=.95, fontsize=19, weight="bold")
    left = np.zeros(len(order))
    for name in OUTCOME_ORDER:
        segment = shares.loc[order, name].to_numpy() * 100
        ax.barh(y, segment, left=left, height=.52, color=OUTCOME_COLORS[name], label=name.capitalize())
        for row, (start, value) in enumerate(zip(left, segment)):
            if value >= 7:
                ax.text(start + value / 2, row, f"{value:.0f}%", ha="center", va="center", fontsize=11,
                        color=PAPER if name in ("successful", "unsuccessful", "referred") else INK)
        left += segment
    ax.set(yticks=y, yticklabels=group_labels(order), xlim=(0, 100), ylim=(-.65, len(order) - .35))
    ax.xaxis.set_major_locator(FixedLocator([0, 25, 50, 75, 100]))
    ax.xaxis.set_major_formatter(PercentFormatter(100))
    ax.set_xlabel("Share of all public requests")
    ax.legend(loc="lower center", bbox_to_anchor=(.5, 1.09), ncol=5, handlelength=1,
              columnspacing=1.3, handletextpad=.5)
    for row, group in enumerate(order):
        ax.text(1.075, row, f"{summary.loc[group, 'success_rate']:.1%}", transform=ax.get_yaxis_transform(),
                ha="center", va="center", weight="bold", clip_on=False)
    ax.text(1.075, 1.01, "Successful\n+ partial", transform=ax.transAxes, ha="center", va="bottom", fontsize=11)
    return fig


def speed_success(band_rates, overall_pct):
    apply_style()
    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    fig.subplots_adjust(left=.1, right=.96, bottom=.23, top=.80)
    fig.suptitle("Success Proportions by First-Response Time, 2025", y=.95, fontsize=19, weight="bold")
    ax.set_title("Closed requests with recorded replies · successful includes partial success", fontsize=12,
                 weight="normal", color=MUTED, pad=24)
    values = band_rates["success_rate"].to_numpy() * 100
    x = np.arange(len(values))
    ax.bar(x, values, color=INK, width=.5, zorder=3)
    ax.axhline(overall_pct, color=ACCENT, linestyle=(0, (5, 4)), linewidth=1.2, zorder=4)
    ax.annotate(f"Overall {overall_pct:.1f}%", (3.35, overall_pct), xytext=(0, 8), textcoords="offset points",
                color=ACCENT, ha="right", fontsize=11,
                bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 2})
    for i, value in enumerate(values):
        ax.text(i, value - 5, f"{value:.1f}%", ha="center", va="center", color=PAPER, weight="bold", fontsize=14)
    labels = [f"{label}\nn = {int(n):,}" for label, n in zip(band_rates.index, band_rates["n"])]
    ax.set(xticks=x, xticklabels=labels, ylim=(0, 100), xlim=(-.6, 3.6), yticks=[0, 25, 50, 75, 100])
    ax.yaxis.set_major_formatter(PercentFormatter(100))
    ax.set_ylabel("Weighted success proportion")
    ax.set_xlabel("First-response time · weighted quartile bands", labelpad=16)
    grid(ax, "y")
    return fig


def normality_plots(replied):
    from scipy.stats import probplot
    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), layout="constrained")
    for ax, values, title in zip(axes, [replied, np.log(replied)], ["Response time", "Log response time"]):
        probplot(values, dist="norm", plot=ax)
        points, line = ax.get_lines()
        points.set(marker="o", markersize=3, color=INK, alpha=.45, markeredgewidth=0)
        line.set(color=ACCENT, linewidth=1.3)
        ax.set_title(title)
        ax.set_xlabel("Theoretical normal quantiles")
        ax.set_ylabel("Observed days" if ax is axes[0] else "Log of observed days")
        grid(ax, "y")
    fig.suptitle("Normal Q–Q Plots of First-Response Times", fontsize=18, weight="bold")
    return fig
