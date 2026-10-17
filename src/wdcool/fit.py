"""Fit a model WDLF to observed counts: free cluster WD age, analytic normalisation."""

import numpy as np
from .wdlf import model_lf, poisson_loglike


def fit_offset_norm(track, bin_edges, counts, age_grid_gyr):
    """Grid over the cluster white dwarf age; the normalisation is profiled out.

    For Poisson counts with expected = A * shape, the maximum-likelihood
    A is sum(counts) / sum(shape).

    Returns dict with best age, best normalisation, log-likelihood array over the grid.
    """
    counts = np.asarray(counts, dtype=float)
    loglike = np.full(len(age_grid_gyr), -np.inf)
    norms = np.zeros(len(age_grid_gyr))
    for i, age in enumerate(age_grid_gyr):
        shape = model_lf(track, bin_edges, max_age_gyr=age)
        if shape.sum() <= 0:
            continue
        a = counts.sum() / shape.sum()
        norms[i] = a
        loglike[i] = poisson_loglike(counts, a * shape)
    best = int(np.argmax(loglike))
    return {
        "best_age_gyr": float(age_grid_gyr[best]),
        "best_norm": float(norms[best]),
        "loglike": loglike,
        "norms": norms,
        "age_grid_gyr": np.asarray(age_grid_gyr),
    }
