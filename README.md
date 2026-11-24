# Solar-monitor

Daily quality control of the LAPUP radiometric stations.

`yesterday_qc.py` runs the [libinsitu](http://libinsitu.org/) QC tests on yesterday's files: GHI from the `solar` station, DHI and DNI from the `suntracker` station (resampled from 10 s to 1 min). It prints one row per test with the number of tested and failed points.

Reads the daily CSVs from `raw/solar/YYYY/` and `raw/suntracker/YYYY/`.

## Instructions

Python 3.14.4

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

To run Tuesday to Friday at 10:00 (host clock in Athens time), without overlapping runs. Monday is left for the weekly check:

```bash
# Runs the libinsitu QC tests on yesterday's solar and suntracker files
# Tue–Fri at 10:00 Athens time
0 10 * * 2-5 /usr/bin/flock -w 0 ~/solar_monitor_yesterday_qc.lock ~/Solar-monitor/.venv/bin/python ~/Solar-monitor/yesterday_qc.py
```

To check if your cron job is running:

```
grep CRON /var/log/syslog
```
