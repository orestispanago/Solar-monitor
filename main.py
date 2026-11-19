import datetime
import os

import pandas as pd

from config import OUT_DIR
from processing import merge_stations, resample_suntracker
from qc import calc_qc_flags
from readers import read_cr1000_file


def run_qc(solar, suntracker):
    df = merge_stations(solar, suntracker)
    flags = calc_qc_flags(df)
    return df, flags


def get_yesterday_files():
    today = datetime.datetime.now(tz=datetime.timezone.utc)
    yesterday = today - pd.Timedelta(1, unit="D")
    year = yesterday.strftime("%Y")
    solar_basename = yesterday.strftime("solar1min_%Y%m%d.csv")
    solar_path = f"raw/solar/{year}/{solar_basename}"
    suntracker_basename = yesterday.strftime("suntracker10sec_%Y%m%d.csv")
    suntracker_path = f"raw/suntracker/{year}/{suntracker_basename}"
    return solar_path, suntracker_path


solar_path, suntracker_path = get_yesterday_files()
solar = read_cr1000_file(solar_path)
suntracker = read_cr1000_file(suntracker_path)
suntracker_1min = resample_suntracker(suntracker)


os.makedirs(OUT_DIR, exist_ok=True)
df, flags = run_qc(solar, suntracker_1min)

print(list(flags))
