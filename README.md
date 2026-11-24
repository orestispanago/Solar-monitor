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

To run on weekdays at 04:00, without overlapping runs:

```bash
# Runs the libinsitu QC tests on yesterday's solar and suntracker files
# Weekdays at 04:00
0 4 * * 1-5 cd ~/Solar-monitor && /usr/bin/flock -w 0 ~/solar_monitor.lock .venv/bin/python yesterday_qc.py
```

To check if your cron job is running:

```
grep CRON /var/log/syslog
```
