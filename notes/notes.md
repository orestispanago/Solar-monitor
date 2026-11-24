# Notes

## QC work

Tests and conditions: [best_practices.md](best_practices.md). Grouped by the data each item needs, in build order. Within a group: tracker and ring first.

### 1. libinsitu flags on the merged df
- [x] Call `compute_qc_flags()` on solar GHI + suntracker DHI, DNI (`qc.py`)
- [x] Fix `yesterday_qc.py` (was `main.py`): pass `suntracker_1min` to `run_qc()`, drop the unused `merged`
- [x] Summarize the libinsitu tests, one row each (n_tested, n_failed, pct_failed): `summarize_flags()`
  - [x] BSRN physically possible upper limits, GHI, DHI, DNI
  - [x] BSRN extremely rare upper limits, GHI, DHI, DNI
  - [x] Diffuse fraction K < 1.05/1.10
  - [x] Geuder tracker test K ≤ 0.96 when Kt > 0.6
  - [x] Kn < Kt
  - [x] Forstinger tracker-off (Kn > 0.0171 or Kt < 0.533)
  - [x] Closure ratio
  - [x] Maxwell closure difference
- [x] Map each test to its likely cause and instrument (`TEST_INFO`)
- [ ] Status column: OK/ALERT threshold per test, NOT RUN when n_tested = 0

### 2. Needs only the df + sun position (zenith, ETR from libinsitu)
- [ ] Completeness: row count (1440 solar, 8640 suntracker), empty or stuck columns, time gaps
- [ ] Step change > 1000 W/m², pandas `diff`
- [ ] Kt < 1.4
- [ ] Kn < (1100 + 0.03 · altitude) / ETR
- [ ] Kd < 0.6
- [ ] Nighttime offset correction of the pyranometers (Nollas et al. 2023)
- [ ] BSRN lower limits −4/−2, after offset correction
- [ ] Nollas GHI lower limit (Eq. 4-1), after offset correction
- [ ] Nollas DHI lower limit, cloudy (Eq. 4-1), after offset correction

### 3. Needs clear-sky GHI and DNI (handbook formulas or McClear)
- [ ] Long & Shi tracker test
- [ ] Forstinger tracker test, handbook version (Table 4-8)

### 4. Needs outside data or models
- [ ] Shadow ring test on solar DHI, diffuse fraction model from pvlib
- [ ] Shadow ring correction of solar DHI
- [ ] DHI comparison: solar ring CMP11 vs suntracker MS-80, after ring correction
- [ ] Second libinsitu run on solar only (GHI, ring DHI, CSD3 DNI), trends only, no alerts
- [ ] Nollas DHI lower limit, cloudless (Rayleigh limit − 1, Eq. 4-2), pressure from meteo
- [ ] Horizon mask from `pvlib.iotools.get_pvgis_horizon`, flag only
- [ ] GTI and GTISW: upper limits and step change (Lorenz et al. 2022)
- [ ] GTI and GTISW within 200 W/m² of `pvlib.irradiance.get_total_irradiance(model='perez')`
- [ ] GTI vs GTISW cross-check

### 5. Daily inspection and outputs
- [ ] Daily plot: GHI, DNI, DHI together
- [ ] Daily plot with meteo data in the same view
- [ ] Cleaning dips vs maintenance log [TODO: where are cleanings logged?]
- [ ] Daily email: OK/ALERT, summary table, daily plot attached
- [ ] Cron jobs on .21, 10:00 Athens (one hour after FTP-alerts, so an outage it reports can be fixed first):
  - Tue–Fri: yesterday's files
  - Mon: weekly check of the past 7 days (Mon–Sun), no separate yesterday-only run [TODO: report format: totals over the week or one row per test per day]
- [ ] Optional: midday tracker check on today's partial file, email only on issues
  - Mon–Fri at 12:00 Athens: about 4.5 h of daylight data in winter
  - Own lock file, e.g. `~/solar_monitor_midday_qc.lock`, so neither job skips the other silently
  - Tests: tracker only, `Kn_LL_KT` (tracker stopped) and `K_UL_KT` (MS-80 not shaded), plus completeness once built. Other tests point to slow faults the yesterday run catches
  - Overcast morning: n_tested = 0, report NOT RUN, not OK
  - [TODO: export CSVs from both runs? If so, a separate name for midday, e.g. `qc_midday_%Y%m%d.csv`, so the yesterday run doesn't overwrite it]

### 6. Long-term review (monthly)
- [ ] Closure ratio over time (libinsitu `visual_qc`)
- [ ] GHI/DHI over time when DNI < 1 W/m² (libinsitu uses < 10)
- [ ] `visual_qc` multiplot of all QC tests
- [ ] Manual inspection flag: default False, True for problem periods, with a note on type, cause and action

### 7. Needs 1–2 years of data
- [ ] Station-specific limits (QCRad, SERI-QC or K–Kt envelopes), redo yearly
