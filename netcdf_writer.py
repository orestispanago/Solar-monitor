from datetime import datetime, timezone

import libinsitu
import pandas as pd
from libinsitu.cdl import init_nc
from libinsitu.cli.transform import process_chunck
from libinsitu.qc.qc_utils import write_flags
from netCDF4 import Dataset

from config import ELEVATION, LATITUDE, LONGITUDE

CDL_PATH = "lapup.cdl"
NETWORK_ID = "LAPUP"
STATION_ID = "ROOF"


NETCDF_NAMES = {
    "solar_GHI_Avg": "GHI",
    "solar_GHI_Std": "GHI_std",
    "suntracker_DHI_MS80_Avg": "DHI",
    "suntracker_DHI_MS80_Std": "DHI_std",
    "suntracker_DNI_MS57_Avg": "BNI",
    "suntracker_DNI_MS57_Std": "BNI_std",
    "solar_DHI_Avg": "DHI_ring",
    "solar_DHI_Std": "DHI_ring_std",
    "solar_GTI_Avg": "GTI",
    "solar_GTI_Std": "GTI_std",
    "solar_GTISW_Avg": "GTISW",
    "solar_GTISW_Std": "GTISW_std",
    "solar_Irrad_Direct_Avg": "BNI_CSD3",
    "solar_Irrad_Direct_Std": "BNI_CSD3_std",
    "solar_SunShine_Tot": "sunshine",
    "suntracker_MS80_temp_C_Avg": "MS80_temp",
    "solar_Bat_Min": "solar_battery",
    "suntracker_Bat_Min": "suntracker_battery",
    "solar_RecNbr": "solar_record",
    "suntracker_RecNbr": "suntracker_record",
}


def rename_for_netcdf(df):
    return df.rename(columns=NETCDF_NAMES)


def get_properties(month_start, last_data):
    """Values for the {placeholders} in lapup.cdl."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "Network_ID": NETWORK_ID,
        "Station_ID": STATION_ID,
        "Station_Latitude": LATITUDE,
        "Station_Longitude": LONGITUDE,
        "Station_Elevation": ELEVATION,
        "Station_StartDate": month_start.strftime("%Y-%m-%d"),
        "Station_TimeResolution": "1M",
        "LastData": last_data.isoformat(),
        "CreationTime": now,
        "UpdateTime": now,
        "Version": libinsitu.__version__,
    }


def fix_qc_attributes(ncfile):
    """Fixes the CF errors that libinsitu's write_flags leaves in QC and QC_run."""
    ncfile.variables["QC_run"].delncattr("standard_name")
    for var in ["QC", "QC_run"]:
        masks = ncfile.variables[var].getncattr("flag_masks")
        ncfile.variables[var].setncattr("flag_masks", masks.astype("uint32"))


def write_netcdf(df, flags, path, month_start):
    properties = get_properties(month_start, df.index[-1])
    ncfile = Dataset(path, "w")
    init_nc(ncfile, properties, [], custom_cdl=CDL_PATH)
    process_chunck(df, ncfile, properties, custom_cdl=CDL_PATH)
    full_index = pd.date_range(month_start, df.index[-1], freq="min")
    flags = flags.reindex(full_index, fill_value=-1)
    write_flags(ncfile, flags)
    fix_qc_attributes(ncfile)
    ncfile.close()
