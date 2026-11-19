from libinsitu.qc.qc_utils import compute_qc_flags

from config import ELEVATION, LATITUDE, LONGITUDE

QC_COLUMNS = {
    "solar_GHI_Avg": "GHI",
    "suntracker_DHI_MS80_Avg": "DHI",
    "suntracker_DNI_MS57_Avg": "BNI",
}


def calc_qc_flags(df):
    meas_df = df[list(QC_COLUMNS)].rename(columns=QC_COLUMNS)
    meas_df = meas_df.asfreq("min")
    return compute_qc_flags(meas_df, LATITUDE, LONGITUDE, ELEVATION)
