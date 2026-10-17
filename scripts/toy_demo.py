"""End-to-end demo of the pipeline on a TOY track. The numbers are not physical.

It exists to prove the code runs: track -> model LF -> fit. Replace the toy track
with read_history(...) on a real MESA run.
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from wdcool import CoolingTrack, model_lf, fit_offset_norm  # noqa: E402

age = np.linspace(0, 12, 400)
track = CoolingTrack(age, -1 - 0.55 * age**0.8, label="TOY track (not physical)")

edges = np.linspace(-4.5, -1.5, 13)
centres = 0.5 * (edges[1:] + edges[:-1])
rng = np.random.default_rng(42)
counts = rng.poisson(model_lf(track, edges, max_age_gyr=9.0) * 40)

grid = np.linspace(6, 12, 121)
res = fit_offset_norm(track, edges, counts, grid)
print(f"toy fit: best age = {res['best_age_gyr']:.2f} Gyr (injected 9.0)")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
shape = model_lf(track, edges, max_age_gyr=res["best_age_gyr"]) * res["best_norm"]
ax[0].errorbar(centres, counts, yerr=np.sqrt(np.maximum(counts, 1)), fmt="o", label="toy counts")
ax[0].step(centres, shape, where="mid", label="best fit")
ax[0].set_xlabel("log L / Lsun"); ax[0].set_ylabel("N per bin"); ax[0].legend()
ax[1].plot(grid, res["loglike"] - res["loglike"].max())
ax[1].set_xlabel("cluster WD age (Gyr)"); ax[1].set_ylabel("Δ log-likelihood")
fig.suptitle("Toy demo only: not a scientific result")
fig.tight_layout()
out = Path(__file__).resolve().parents[1] / "toy_demo.png"
fig.savefig(out, dpi=130)
print("wrote", out)
