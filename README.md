# Solar-monitor

Daily quality control of the LAPUP radiometric stations.

`yesterday_qc.py` runs the [libinsitu](http://libinsitu.org/) QC tests on yesterday's files: GHI from the `solar` station, DHI and DNI from the `suntracker` station (resampled from 10 s to 1 min). It prints one row per test with the number of tested and failed points.

`midday_qc.py` runs the tracker tests (`Kn_LL_KT`, `K_UL_KT`) on today's partial files and emails the result if any point failed.

Reads the daily CSVs from `raw/solar/YYYY/` and `raw/suntracker/YYYY/`.

## Instructions

Python 3.14.4

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
chmod 600 .env
```

Set the email credentials in `.env`, replacing the placeholders. It is in `.gitignore`. Email recipients are in `config.json`. Each script logs to `logs/<script name>.log`.

To run Tuesday to Friday at 10:00 (host clock in Athens time), without overlapping runs. Monday is left for the weekly check:

```bash
# Runs the libinsitu QC tests on yesterday's solar and suntracker files
# Tue–Fri at 10:00 Athens time
0 10 * * 2-5 /usr/bin/flock -w 0 ~/solar_monitor_yesterday_qc.lock ~/Solar-monitor/.venv/bin/python ~/Solar-monitor/yesterday_qc.py
# Runs the tracker tests on today's partial files, so a stopped tracker can be fixed the same day
# Mon–Fri at 12:00 Athens time
0 12 * * 1-5 /usr/bin/flock -w 0 ~/solar_monitor_midday_qc.lock ~/Solar-monitor/.venv/bin/python ~/Solar-monitor/midday_qc.py
```

To check if your cron job is running:

```
grep CRON /var/log/syslog
```
