from readers import SUNTRACKER_COLUMNS_CR1000

STD_COLUMNS = {"DHI_MS80_Std": "DHI_MS80_Avg", "DNI_MS57_Std": "DNI_MS57_Avg"}


def select_complete_minutes(df):
    minute = df.index.ceil("1min")
    sizes = df.groupby(minute).size()
    return sizes.index[sizes == 6]


def calc_combined_std(df, std_col, avg_col):
    """1-min std from the 10-s means and population stds (Campbell StdDev divides by N)."""
    minute = df.index.ceil("1min")
    minute_mean = df[avg_col].groupby(minute).transform("mean")
    spread = (df[avg_col] - minute_mean) ** 2
    within = (df[std_col] ** 2).groupby(minute).mean()
    between = spread.groupby(minute).mean()
    return (within + between) ** 0.5


def resample_suntracker(df):
    minute = df.index.ceil("1min")
    out = df.groupby(minute).agg(
        {
            "RecNbr": "last",
            "Bat_Min": "min",
            "DHI_MS80_Avg": "mean",
            "DNI_MS57_Avg": "mean",
            "MS80_temp_C_Avg": "mean",
        }
    )
    for std_col, avg_col in STD_COLUMNS.items():
        out[std_col] = calc_combined_std(df, std_col, avg_col)
    complete_minutes = select_complete_minutes(df)
    out = out.loc[complete_minutes]
    return out[SUNTRACKER_COLUMNS_CR1000]


def merge_stations(solar, suntracker):
    solar = solar.add_prefix("solar_")
    suntracker = suntracker.add_prefix("suntracker_")
    return solar.join(suntracker, how="outer")
