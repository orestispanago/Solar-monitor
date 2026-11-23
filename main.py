import datetime
import os

import pandas as pd

from config import OUT_DIR
from processing import merge_stations, resample_suntracker
from qc import add_test_info, calc_qc_flags, summarize_flags
from readers import read_cr1000_file

os.makedirs(OUT_DIR, exist_ok=True)


def run_qc(solar, suntracker):
    df = merge_stations(solar, suntracker)
    flags = calc_qc_flags(df)
    return df, flags


def get_files_by_day(yesterday):
    year = yesterday.strftime("%Y")
    solar_basename = yesterday.strftime("solar1min_%Y%m%d.csv")
    solar_path = f"raw/solar/{year}/{solar_basename}"
    suntracker_basename = yesterday.strftime("suntracker10sec_%Y%m%d.csv")
    suntracker_path = f"raw/suntracker/{year}/{suntracker_basename}"
    return solar_path, suntracker_path


today = datetime.datetime.now(tz=datetime.timezone.utc)
df_list = []
for day in range(1, 2):
    yesterday = today - pd.Timedelta(day, unit="D")

    solar_path, suntracker_path = get_files_by_day(yesterday)
    solar = read_cr1000_file(solar_path)
    suntracker = read_cr1000_file(suntracker_path)
    suntracker_1min = resample_suntracker(suntracker)

    df, flags = run_qc(solar, suntracker_1min)

    summary = summarize_flags(flags)
    summary = add_test_info(summary)
    summary.insert(0, "date", yesterday.date())
    df_list.append(summary)
    # summary.to_csv(yesterday.strftime("out/qc_%Y%m%d.csv"))
df_all = pd.concat(df_list)
print(df_all)
