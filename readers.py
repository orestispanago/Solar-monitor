import glob
import os

import pandas as pd

from config import SOLAR_DIR, SUNTRACKER_CR1000_START, SUNTRACKER_DIR

SOLAR_COLUMNS = [
    "Datetime_UTC",
    "RecNbr",
    "GHI_Avg",
    "GHI_Std",
    "DHI_Avg",
    "DHI_Std",
    "Irrad_Direct_Avg",
    "Irrad_Direct_Std",
    "SunShine_Tot",
    "GTI_Avg",
    "GTI_Std",
    "GTISW_Avg",
    "GTISW_Std",
    "Bat_Min",
]


SUNTRACKER_COLUMNS_CR1000 = [
    "RecNbr",
    "Bat_Min",
    "DHI_MS80_Avg",
    "DHI_MS80_Std",
    "DNI_MS57_Avg",
    "DNI_MS57_Std",
    "MS80_temp_C_Avg",
]

COMBILOG_TO_CR1000 = {
    "DHI-MS80": "DHI_MS80_Avg",
    "MS80-temp": "MS80_temp_C_Avg",
    "DNI-MS57": "DNI_MS57_Avg",
}


def create_paths_timeseries(paths, name_format):
    dates = []
    for fname in paths:
        base_name = os.path.basename(fname)
        date = pd.to_datetime(base_name, format=name_format)
        dates.append(date)
    return pd.Series(paths, index=dates)


def check_unique_times(df, path):
    duplicates = df.index[df.index.duplicated()]
    if len(duplicates) > 0:
        raise ValueError(f"{path}: duplicate timestamp {duplicates[0]}")


def read_solar(start=None, end=None, folder=SOLAR_DIR):
    all_files = sorted(glob.glob(f"{folder}/**/*.csv"))
    df_list = []
    paths_series = create_paths_timeseries(all_files, "solar1min_%Y%m%d.csv")
    for fname in paths_series.loc[start:end]:
        df = pd.read_csv(fname, index_col="Datetime_UTC", usecols=SOLAR_COLUMNS)
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")
        check_unique_times(df, fname)
        df_list.append(df)
    return pd.concat(df_list)


def read_combilog_file(path):
    usecols = ["Datetime_UTC"]
    for name in COMBILOG_TO_CR1000:
        usecols.append(name)
    df = pd.read_csv(
        path, index_col="Datetime_UTC", usecols=usecols, parse_dates=True
    )
    return df.rename(columns=COMBILOG_TO_CR1000)


def read_cr1000_file(path):
    return pd.read_csv(path, index_col="Datetime_UTC", parse_dates=True)


def read_suntracker(start=None, end=None, folder=SUNTRACKER_DIR):
    all_files = sorted(glob.glob(f"{folder}/**/*.csv"))
    df_list = []
    paths_series = create_paths_timeseries(
        all_files, "suntracker10sec_%Y%m%d.csv"
    )
    selected = paths_series.loc[start:end]
    for date, fname in zip(selected.index, selected):
        if date < pd.Timestamp(SUNTRACKER_CR1000_START):
            df = read_combilog_file(fname)
        else:
            df = read_cr1000_file(fname)
        check_unique_times(df, fname)
        df = df.reindex(columns=SUNTRACKER_COLUMNS_CR1000)
        df_list.append(df)
    return pd.concat(df_list)
