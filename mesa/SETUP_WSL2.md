# MESA on Windows via WSL2

MESA runs on Linux or macOS, so on Windows use WSL2. Check the current instructions at
https://docs.mesastar.org before starting; versions and steps change.

## 1. Install WSL2 (PowerShell as Administrator)
```powershell
wsl --install -d Ubuntu
```
Restart when asked, then create your Ubuntu username and password.

## 2. Keep files inside Linux
Work in `~/` (for example `~/mesa`), not `/mnt/c/...`. Builds on the Windows drive are very slow.

## 3. Install MESA
Follow the official page for the current MESA release and the matching MESA SDK. You need:
- the MESA SDK (compilers and libraries), installed and initialised in your shell
- the MESA source for the release the SDK supports
- environment variables `MESA_DIR`, `MESASDK_ROOT` and `OMP_NUM_THREADS` set as the docs describe

## 4. First run: use the shipped test suites
Do not write inlists from scratch. The MESA test suite already includes white dwarf cases
(look in `$MESA_DIR/star/test_suite/` for the `make_co_wd` and `wd_cool_0.6M` style directories).
```bash
cd $MESA_DIR/star/test_suite/wd_cool_0.6M
./clean && ./mk && ./rn
```
If that finishes and writes `LOGS/history.data`, your install works.

## 5. What to change for this project
Copy a working test-suite directory into `mesa/runs/` and change only one thing at a time:
- the ¹²C(α,γ) rate multiplier (see the `rates_controls` section of the MESA docs for the current option names)
- the white dwarf mass
- an optional extra energy-loss term (via `run_star_extras`)

Record every change in `mesa/RUNLOG.md` with the date, MESA version and exact setting.
Never commit the large `LOGS/` folders; commit only `history.data` files you analyse (compressed if big).

## 6. Link to the Python code
```python
from wdcool import read_history
track = read_history("mesa/runs/wd060_rate1.0/LOGS/history.data", label="0.60 Msun, rate x1.0")
```
