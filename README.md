# wd-cooling-ngc6397

How do uncertainties in the ¹²C(α,γ)¹⁶O reaction rate, and an optional extra cooling channel
(axion-like bremsstrahlung), change the white dwarf cooling sequence of the globular cluster NGC 6397?

**Status: work in progress.** The analysis tools in `src/wdcool` are tested on toy data only.
No scientific result exists yet. The physics tracks come from MESA runs (see `mesa/`).

## Plan
1. Build MESA white dwarf models (0.53, 0.60, 0.70 Msun) while varying the ¹²C(α,γ) rate.
2. Add an extra energy-loss term to those models.
3. Convert each cooling track into a model luminosity function (`wdcool.model_lf`).
4. Fit the published NGC 6397 white dwarf luminosity function with a Poisson likelihood (`wdcool.fit_offset_norm`).
5. Write a short research note and archive the code on Zenodo.

## Layout
| Path | Contents |
|---|---|
| `src/wdcool/` | MESA reader, luminosity-function model, likelihood fit |
| `tests/` | unit tests (`pytest`) |
| `scripts/toy_demo.py` | end-to-end demo on a **toy** track (not physical) |
| `mesa/` | MESA setup on Windows (WSL2) and run notes |
| `paper/outline.md` | research-note outline |
| `data/` | put downloaded observational data here (not committed) |

## Install and test
```bash
python -m venv .venv && source .venv/bin/activate     # WSL2/Ubuntu or Linux/macOS
pip install -e . pytest
pytest
python scripts/toy_demo.py
```

## Honest limitations of the current model
- Single white dwarf mass; no progenitor IMF or initial–final mass relation yet.
- Cluster age enters only as a cut-off in cooling age; no photometric errors or completeness.
- These must be added (see `paper/outline.md`) before any result is claimed.

## Citing
See `CITATION.cff`. Please cite MESA (Paxton et al. 2011, 2013, 2015, 2018, 2019; Jermyn et al. 2023) if you use the MESA inputs.

## Licence
MIT
