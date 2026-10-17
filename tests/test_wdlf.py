import numpy as np
import pytest

from wdcool import CoolingTrack, model_lf, fit_offset_norm
from wdcool.mesaio import read_history


def toy_track():
    # strictly monotonic toy track: log L = -1 - 0.55 * age^0.8, age in Gyr
    age = np.linspace(0, 12, 400)
    return CoolingTrack(age, -1 - 0.55 * age**0.8, label="toy")


def test_lf_sums_to_total_time():
    tr = toy_track()
    edges = np.linspace(-4.5, -1.0, 15)
    dt = model_lf(tr, edges)
    t_faint = np.interp(4.5, -tr.log_l, tr.age_gyr)
    t_bright = np.interp(1.0, -tr.log_l, tr.age_gyr)
    assert dt.sum() == pytest.approx(t_faint - t_bright, rel=1e-9)


def test_age_cut_removes_faint_bins():
    tr = toy_track()
    edges = np.linspace(-4.5, -1.0, 15)
    dt = model_lf(tr, edges, max_age_gyr=5.0)
    assert np.all(dt >= -1e-12)
    assert dt[0] == pytest.approx(0.0, abs=1e-12)  # faintest bin is older than 5 Gyr
    assert dt.sum() <= 5.0 + 1e-9


def test_fit_recovers_age():
    tr = toy_track()
    edges = np.linspace(-4.5, -1.0, 18)
    truth = model_lf(tr, edges, max_age_gyr=9.0) * 500
    rng = np.random.default_rng(1)
    counts = rng.poisson(truth)
    res = fit_offset_norm(tr, edges, counts, np.linspace(6, 12, 61))
    assert abs(res["best_age_gyr"] - 9.0) < 1.0


def test_read_history(tmp_path):
    p = tmp_path / "history.data"
    rows = ["x"] * 5
    rows.append("   model_number  star_age  log_L")
    for i in range(10):
        rows.append(f"{i} {1e6 * i * 1e3:.6e} {-0.5 - 0.1 * i:.4f}")
    p.write_text("\n".join(rows) + "\n")
    tr = read_history(p)
    assert tr.age_gyr[0] >= 0
    assert tr.log_l.size > 0
