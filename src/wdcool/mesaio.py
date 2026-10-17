"""Read MESA history.data files into a cooling track (log L vs cooling age)."""

from dataclasses import dataclass
import numpy as np


@dataclass
class CoolingTrack:
    """A white dwarf cooling track, sorted by increasing age.

    age_gyr : cooling age in Gyr (monotonic increasing)
    log_l   : log10(L / Lsun)
    label   : free text, e.g. 'M=0.53 R=1.0'
    """

    age_gyr: np.ndarray
    log_l: np.ndarray
    label: str = ""

    def __post_init__(self):
        self.age_gyr = np.asarray(self.age_gyr, dtype=float)
        self.log_l = np.asarray(self.log_l, dtype=float)
        if self.age_gyr.shape != self.log_l.shape:
            raise ValueError("age and log_l must have the same shape")
        order = np.argsort(self.age_gyr)
        self.age_gyr = self.age_gyr[order]
        self.log_l = self.log_l[order]

    def log_l_at(self, age_gyr):
        """Interpolate log L at the given cooling age(s)."""
        return np.interp(age_gyr, self.age_gyr, self.log_l)


def read_history(path, age_col="star_age", lum_col="log_L", t0_years=None, label=""):
    """Read a MESA history.data file.

    MESA history files have 5 header lines, then a column-name line, then data.
    The cooling age is taken as star_age minus the age at which the model first
    drops below log L = -1 (override with t0_years, in years).
    """
    with open(path) as fh:
        lines = fh.readlines()
    # find the column-name line: the first line containing both column names
    hdr_idx = None
    for i, line in enumerate(lines[:20]):
        toks = line.split()
        if age_col in toks and lum_col in toks:
            hdr_idx = i
            names = toks
            break
    if hdr_idx is None:
        raise ValueError(f"could not find columns {age_col!r} and {lum_col!r} in {path}")
    data = np.loadtxt(lines[hdr_idx + 1:], ndmin=2)
    age = data[:, names.index(age_col)]
    logl = data[:, names.index(lum_col)]
    if t0_years is None:
        below = np.where(logl < -1.0)[0]
        t0_years = age[below[0]] if below.size else age[0]
    cool_gyr = (age - t0_years) / 1e9
    keep = cool_gyr >= 0
    return CoolingTrack(cool_gyr[keep], logl[keep], label=label or str(path))
