# Best practices

QC procedures from the IEA PVPS Task 16 Best Practices Handbook, 4th edition (2024), chapter 4: https://iea-pvps.org/wp-content/uploads/2024/09/Best-Practices-Handbook-for-the-Collection-and-Use-of-Solar-Resource-Data-for-Solar-Energy-Applications-Fourth-Edition-.pdf

"Done by" column: libinsitu if libinsitu 1.8.0 does it (tests from its `res/qc-tests.csv`, plots from `visual_qc`), otherwise own code.

## Automated tests (4.2)

Most tests are not applied below 50 W/m² or sun elevation 2°. Meant for 1-min data.

| Test | Passing condition | Done by |
|---|---|---|
| BSRN physically possible upper limits (4.2.2) | GHI ≤ 1.5 · ETR · cos^1.2 Z + 100, DHI ≤ 0.95 · ETR · cos^1.2 Z + 50, DNI ≤ ETR | libinsitu |
| BSRN extremely rare upper limits (4.2.2) | GHI ≤ 1.2 · ETR · cos^1.2 Z + 50, DHI ≤ 0.75 · ETR · cos^1.2 Z + 30, DNI ≤ 0.95 · ETR · cos^0.2 Z + 10 | libinsitu |
| BSRN lower limits (4.2.2) | Physically possible ≥ −4, extremely rare ≥ −2 W/m². Needs offset-free or offset-corrected pyranometers (Nollas et al. 2023) | Own code |
| GHI lower limit (4.2.2) | GHI > GHImin (Nollas et al. 2023, Eq. 4-1), Z < 90° | Own code |
| DHI lower limit, cloudy (4.2.2) | DHI > DHImin (Eq. 4-1), DNI < 10 W/m², Z < 90° | Own code |
| DHI lower limit, cloudless (4.2.2) | DHI > Rayleigh limit − 1 (Eq. 4-2, needs pressure), DNI ≥ 10, GHI > 50 W/m², Kt < 0.8 | Own code |
| Closure ratio (4.2.3) | \|GHI / (DHI + DNI cos Z) − 1\| < 0.08 (Z < 75°) or 0.15 (75–93°), sum > 50 W/m² | libinsitu (Z < 90°). libinsitu also runs the Maxwell closure difference test |
| Diffuse fraction (4.2.3) | K = DHI/GHI < 1.05 (Z < 75°) or 1.10 (75–93°), GHI > 50 W/m² | libinsitu (Z < 90°) |
| Kt upper limit (4.2.4) | Kt < 1.4, Z < 90° | Own code |
| Kn–Kt comparison (4.2.4) | Kn < Kt, GHI > 50 W/m² | libinsitu |
| Kn upper limit (4.2.4) | Kn < (1100 + 0.03 · altitude) / ETR, GHI > 50 W/m² | Own code |
| Kd upper limit (4.2.4) | Kd < 0.6, Z < 90° | Own code |
| Tracker misalignment, Long & Shi 2008 (4.2.5) | K < 0.85 when GHI/GHIclear > 0.85 and DHI > 50 W/m² | Own code |
| Tracker misalignment, Geuder et al. 2015 (4.2.5) | K ≤ 0.96 when Kt > 0.6 | libinsitu |
| Tracker misalignment, Forstinger et al. 2021 (4.2.5) | (GHIclear − GHI)/(GHIclear + GHI) > 0.2 or (DNIclear − DNI)/(DNIclear + DNI) < 0.95, Z < 85°. GHIclear = 0.8 · ETR · cos Z, DNIclear = 0.688 · ETR | Own code. libinsitu has a different Forstinger tracker-off test (Kn > 0.0171 or Kt < 0.533) |
| Shadow ring misalignment (4.2.5) | \|K measured − K model\| < 0.1 clear sky, 0.35 otherwise, Z < 80° (Nollas et al. 2023) | Own code |
| Step change (4.2.6) | \|GHI(t) − GHI(t−1)\| < 1000 W/m² | Own code |
| Station-specific limits (4.2.7) | Stricter limits from 1–2 years of the station's data (QCRad, SERI-QC, K–Kt envelopes) | Own code |
| Horizon shading (4.2.8) | Flag minutes with the sun below the local horizon (PVGIS or SRTM horizon) | Own code. libinsitu gets the SRTM horizon, but only draws it on plots |

## Daily inspection (4.3)

Automate the daily plots as much as possible.

| Step | What to check | Done by |
|---|---|---|
| 1. Station operational | Data present from every sensor. If not: communications, logger, sensor, power or processing failure | Own code |
| 2. Inspect daily plots | GHI, DNI and DHI together. Look for disruptions, steps, soiling before a cleaning | Own code |
| 3. View with other measurements | Meteorological data in the same view, ideally interactive | Own code |
| 4. Compare with maintenance logs | Cleaning dips at the logged times. A missing or shifted dip points to a clock error or a missed visit | Own code |
| Daily summary of QC flags (4.6) | Turn the flags into a report on which instrument needs action | Own code |

## Long-term review (4.4)

| Check | What to look for | Done by |
|---|---|---|
| Closure ratio over time | GHI / (DHI + DNI cos Z) for Z < 75°, GHI > 50 W/m². Jumps and drifts that stay within the test tolerance | libinsitu |
| GHI/DHI over time when DNI < 1 W/m² | Tells whether a jump comes from a pyranometer or the pyrheliometer | libinsitu (uses DNI < 10 W/m²) |
| Multiplot of all QC tests | Heatmaps, test plots, K–Kt envelopes, closure, distributions, shadow analysis | libinsitu (`visual_qc`) |
| Manual inspection flag (4.6.2) | Default False, True for periods with a problem found in visual review, with a note on type, cause and action | Own code |

Where libinsitu differs from the handbook:
- Its closure ratio and diffuse fraction tests stop at zenith 90° instead of 93°.
- Its GHI/DHI long-term plot uses DNI < 10 W/m², not < 1 W/m².
- Its Forstinger test is a different formula from the one in the handbook's Table 4-8.
- It downloads the SRTM horizon but only draws it on plots. It doesn't flag the data.