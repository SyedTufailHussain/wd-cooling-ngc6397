"""Simplified single-mass white dwarf luminosity function (WDLF).

For white dwarfs of one mass formed in a burst, the number per luminosity bin is
proportional to the time spent in that bin:  dN/dlogL  ∝  dt/dlogL.
This is the leading-order model. The paper version should integrate over the
progenitor IMF and the initial-final mass relation; see paper/outline.md.
"""

import numpy as np
from .mesaio import CoolingTrack


def model_lf(track: CoolingTrack, bin_edges, max_age_gyr=None):
    """Time (Gyr) the track spends in each log L bin.

    bin_edges   : increasing array of log10(L/Lsun) edges
    max_age_gyr : oldest cooling age present in the cluster (i.e. the cluster's
                  white dwarf age). Time beyond this age is not counted, which
                  produces the observed cut-off at faint luminosities.
    """
    edges = np.asarray(bin_edges, dtype=float)
    if np.any(np.diff(edges) <= 0):
        raise ValueError("bin_edges must be strictly increasing")
    # age as a function of log L (log L falls with age, so interpolate on -log L)
    order = np.argsort(-track.log_l)
    t_edge = np.interp(-edges, -track.log_l[order], track.age_gyr[order])
    if max_age_gyr is not None:
        t_edge = np.minimum(t_edge, max_age_gyr)
    # edges rise in log L, so ages fall: time in a bin is t(lower edge) - t(upper edge)
    return t_edge[:-1] - t_edge[1:]


def poisson_loglike(observed, expected):
    """Poisson log-likelihood (dropping the constant log(n!) term)."""
    obs = np.asarray(observed, dtype=float)
    exp = np.clip(np.asarray(expected, dtype=float), 1e-12, None)
    return float(np.sum(obs * np.log(exp) - exp))
