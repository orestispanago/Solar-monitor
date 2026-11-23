import pandas as pd
from libinsitu.qc.qc_utils import compute_qc_flags, get_flags

from config import ELEVATION, LATITUDE, LONGITUDE

QC_COLUMNS = {
    "solar_GHI_Avg": "GHI",
    "suntracker_DHI_MS80_Avg": "DHI",
    "suntracker_DNI_MS57_Avg": "BNI",
}

TEST_INFO = {
    "GHI_PPL_UL_TOANI_SZA": {
        "description": "GHI below physically possible upper limit"
    },
    "GHI_ERL_UL_TOANI_SZA": {"description": "GHI below extremely rare upper limit"},
    "DIF_PPL_UL_TOANI_SZA": {
        "description": "DHI below physically possible upper limit"
    },
    "DIF_ERL_UL_TOANI_SZA": {"description": "DHI below extremely rare upper limit"},
    "DNI_PPL_UL_TOANI": {"description": "DNI below physically possible upper limit"},
    "DNI_ERL_UL_TOANI_SZA": {"description": "DNI below extremely rare upper limit"},
    "K_UL_SZA": {"description": "Diffuse fraction K < 1.05 (Z < 75°) or 1.10"},
    "K_UL_KT": {"description": "Tracker: K ≤ 0.96 when Kt > 0.6 (Geuder)"},
    "Kn_UL_KT": {"description": "Kn below Kt"},
    "Kn_LL_KT": {"description": "Tracker off: Kn > 0.0171 when Kt ≥ 0.533 (Forstinger)"},
    "ClosureRatio_tol_SZA": {
        "description": "GHI matches DHI + DNI·cos Z within 8% (Z ≤ 75°) or 15%"
    },
    "ClosureDelta_tol_TOAHI": {
        "description": "GHI matches DHI + DNI·cos Z within 3% of TOA or 7.5 W/m² (Maxwell)"
    },
}


def calc_qc_flags(df):
    meas_df = df[list(QC_COLUMNS)].rename(columns=QC_COLUMNS)
    meas_df = meas_df.asfreq("min")
    return compute_qc_flags(meas_df, LATITUDE, LONGITUDE, ELEVATION)


def summarize_flags(flags):
    """One row per test from flags of -1 (not run), 0 (passed), 1 (failed)."""
    summary = pd.DataFrame(
        {
            "n_tested": flags[flags != -1].count(),
            "n_failed": flags[flags == 1].count(),
        }
    )
    summary.index.name = "test"
    summary["pct_failed"] = 100 * summary["n_failed"] / summary["n_tested"]
    summary["pct_failed"] = summary["pct_failed"].round(1)
    return summary


def get_test_info():
    libinsitu_flags = get_flags()
    rows = {}
    for name, info in TEST_INFO.items():
        components = " ".join(libinsitu_flags[name].components)
        rows[name] = {"description": info["description"], "components": components}
    return pd.DataFrame.from_dict(rows, orient="index")


def add_test_info(summary):
    info = get_test_info()
    return info.join(summary, how="right")
