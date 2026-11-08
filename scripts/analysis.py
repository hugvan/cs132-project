"""Labels and weighted estimates shared by the notebooks and the nutshell plot.

Population descriptions use sampling_weight. Within one agency group the weights
barely vary, so an unweighted rank test inside a group matches the weighted one.
A test that pools groups does not: national agencies are most of the 2025 filings
and about a fifth of the sample.
"""

import numpy as np

GROUP_ORDER = ["NGA", "GOCC", "SUC", "WATER-DISTRICT", "LGU", "LEA"]
LABELS = {
    "NGA": "National government agencies",
    "GOCC": "Government corporations",
    "SUC": "State universities",
    "WATER-DISTRICT": "Water districts",
    "LGU": "Local governments",
    "LEA": "Law enforcement",
}
SUCCESSFUL_OUTCOMES = ("successful", "partially successful")
CLOSED_OUTCOMES = ("successful", "partially successful", "unsuccessful")
OUTCOME_ORDER = ["successful", "partially successful", "unsuccessful", "open", "referred"]


def collected_weights(sample):
    """Sampling weight based on the requests actually collected in each stratum.

    The stored sampling_weight divides the stratum population by the number drawn.
    22 drawn pages were no longer public (20 in LEA Q1, 2 in NGA Q1), so those strata
    hold fewer rows than drawn and their stored weights sum short of the frame.
    Dividing by the collected count makes the weights sum to the 14,668 frame requests.
    """
    collected = sample.groupby(["agency_group", "filing_quarter"])["tracking_number"].transform("size")
    return sample["stratum_population"].astype(float) / collected


def _paired(values, weights):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    return values[keep], weights[keep]


def weighted_median(values, weights):
    values, weights = _paired(values, weights)
    if values.size == 0:
        return float("nan")
    order = np.argsort(values, kind="mergesort")
    values = values[order]
    cumulative = np.cumsum(weights[order])
    return float(values[np.searchsorted(cumulative, cumulative[-1] / 2, side="left")])


def weighted_quartile_edges(values, weights):
    """Interior cut points that divide the weighted distribution into four groups."""
    values, weights = _paired(values, weights)
    order = np.argsort(values, kind="mergesort")
    values = values[order]
    cumulative = np.cumsum(weights[order])
    total = cumulative[-1]
    edges = []
    for quantile in (0.25, 0.5, 0.75):
        edge = float(values[np.searchsorted(cumulative, total * quantile, side="left")])
        if not edges or edge > edges[-1]:
            edges.append(edge)
    return edges


def weighted_mean(values, weights):
    values, weights = _paired(values, weights)
    if values.size == 0:
        return float("nan")
    return float(np.average(values, weights=weights))


def _dominance(x, wx, y, wy):
    """Weighted probability that a draw from x exceeds a draw from y, ties half."""
    order = np.argsort(y, kind="mergesort")
    y = y[order]
    cumulative = np.cumsum(wy[order])
    left = np.searchsorted(y, x, side="left")
    right = np.searchsorted(y, x, side="right")
    below = np.where(left > 0, cumulative[left - 1], 0.0)
    equal = np.where(right > 0, cumulative[right - 1], 0.0) - below
    return float(np.sum(wx * (below + 0.5 * equal)) / (wx.sum() * wy.sum()))


def weighted_mannwhitney(values, weights, success, n_perm=9999, seed=132):
    """Two-sided permutation test of whether first-response time differs by outcome.

    The statistic is the weighted probability that a successful request has a
    longer first-response time than an unsuccessful one; 0.5 means no difference.
    Weights stay with the request. The null permutes the success labels. Returns
    that probability and a two-sided p-value, which counts departures from 0.5
    in either direction.
    """
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    success = np.asarray(success, dtype=bool)
    keep = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    values, weights, success = values[keep], weights[keep], success[keep]
    observed = _dominance(values[success], weights[success], values[~success], weights[~success])
    rng = np.random.default_rng(seed)
    extreme = 0
    for _ in range(n_perm):
        perm = rng.permutation(success)
        stat = _dominance(values[perm], weights[perm], values[~perm], weights[~perm])
        if abs(stat - 0.5) >= abs(observed - 0.5) - 1e-12:
            extreme += 1
    return observed, (extreme + 1) / (n_perm + 1)
