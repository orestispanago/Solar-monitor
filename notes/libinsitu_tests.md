# libinsitu tests

QC tests of libinsitu 1.8.0, from its `res/qc-tests.csv`. The naming convention is not documented in libinsitu; it is read from the formulas.

## Naming convention

**What is tested _ which limit _ upper or lower _ what the limit depends on**

`<quantity tested>_[PPL|ERL]_<UL|LL|tol>_<what the limit depends on>`

| | Part | Meaning |
|--- |---|---|
| Tested quantity | **GHI, DIF, DNI** | Irradiance tested. DIF = diffuse (DHI) |
| | **K** | Diffuse fraction K = DHI / GHI |
| | **Kn** | Direct transmittance Kn = DNI / TOANI |
| | **ClosureRatio / ClosureDelta** | Closure test: measured GHI vs DHI + DNI · cos Z, as a ratio / as a difference in W/m² |
| Limit | **PPL / ERL** | Physically Possible Limit / Extremely Rare Limit (BSRN) |
| | **UL / LL** | Upper Limit / Lower Limit |
| | **tol** | Tolerance: how far from the ideal value is allowed |
| Depends on | **TOANI** | Top Of Atmosphere Normal Irradiance, i.e. ETR, about 1361 W/m² on a surface facing the sun |
| | **TOAHI** | Top Of Atmosphere Horizontal Irradiance = TOANI · cos Z (in the formulas: `TOA`) |
| | **SZA** | Solar Zenith Angle |
| | **KT** | Clearness index Kt = GHI / TOAHI |

## Tests

| Test | Reads as | Formula |
|---|---|---|
| GHI_PPL_UL_TOANI_SZA | GHI, physically possible upper limit, from TOANI and SZA | GHI ≤ 1.5 · TOANI · cos^1.2 Z + 100 |
| GHI_ERL_UL_TOANI_SZA | GHI, extremely rare upper limit, from TOANI and SZA | GHI ≤ 1.2 · TOANI · cos^1.2 Z + 50 |
| DIF_PPL_UL_TOANI_SZA | DHI, physically possible upper limit, from TOANI and SZA | DHI ≤ 0.95 · TOANI · cos^1.2 Z + 50 |
| DIF_ERL_UL_TOANI_SZA | DHI, extremely rare upper limit, from TOANI and SZA | DHI ≤ 0.75 · TOANI · cos^1.2 Z + 30 |
| DNI_PPL_UL_TOANI | DNI, physically possible upper limit, from TOANI only | DNI ≤ TOANI. No SZA, because DNI faces the sun |
| DNI_ERL_UL_TOANI_SZA | DNI, extremely rare upper limit, from TOANI and SZA | DNI ≤ 0.95 · TOANI · cos^0.2 Z + 10 |
| K_UL_SZA | K upper limit, depends on SZA | K < 1.05 below 75°, 1.10 above |
| K_UL_KT | K upper limit, depends on Kt | K < 0.96, applied when Kt ≥ 0.6 |
| Kn_UL_KT | Kn upper limit, set by Kt | Kn < Kt |
| Kn_LL_KT | Kn lower limit, depends on Kt | Kn > 0.0171, applied when Kt ≥ 0.533 |
| ClosureRatio_tol_SZA | Closure ratio tolerance, depends on SZA | \|GHI / (DHI + DNI · cos Z) − 1\| ≤ 0.08 below 75°, 0.15 above |
| ClosureDelta_tol_TOAHI | Closure difference tolerance, depends on TOAHI | \|GHI − (DHI + DNI · cos Z)\| ≤ 3% of TOAHI, or 7.5 W/m² when TOAHI ≤ 250 |

`K_UL_KT` and `Kn_LL_KT` use Kt to decide when the test applies (clear-ish sky), not to set the limit.

## When a test is run

Each test runs only in its domain and when all its inputs are present. Other minutes are flagged −1 (not run) and are not counted in `n_tested`, so `n_tested` is never 1440 per day.

| Tests | Domain |
|---|---|
| PPL and ERL tests (GHI, DIF, DNI) | SZA ≤ 90° (daylight) |
| K, Kn and closure tests | GHI > 50 W/m² and SZA < 90° |

GHI > 50 W/m² excludes low sun and dark overcast, where ratios like K = DHI / GHI are unstable.

## What a failure means

| Test | A failure usually means |
|---|---|
| PPL tests (GHI, DIF, DNI) | Measurement error: faulty sensor, wiring, wrong calibration constant, bad timestamp |
| ERL tests (GHI, DIF, DNI) | Suspicious, not proof. Repeated failures point to a calibration error. For DIF: MS-80 not shaded |
| K_UL_SZA | DHI too high or GHI too low: calibration, or soiling of the GHI dome |
| K_UL_KT | MS-80 not shaded on a clear-ish sky: tracker off or misaligned |
| Kn_UL_KT | DNI too high or GHI too low |
| Kn_LL_KT | Pyrheliometer not pointing at the sun: tracker stopped or misaligned |
| ClosureRatio_tol_SZA | The three sensors disagree: soiling, misalignment, drift, or a clock offset between the solar and suntracker loggers. Doesn't say which sensor |
| ClosureDelta_tol_TOAHI | Same as the closure ratio. Strict at low sun, so winter failures are often not real |
