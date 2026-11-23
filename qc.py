import pandas as pd
from libinsitu.qc.qc_utils import compute_qc_flags

from config import ELEVATION, LATITUDE, LONGITUDE

QC_COLUMNS = {
    "solar_GHI_Avg": "GHI",
    "suntracker_DHI_MS80_Avg": "DHI",
    "suntracker_DNI_MS57_Avg": "BNI",
}

TEST_INFO = {
    "GHI_PPL_UL_TOANI_SZA": {
        "description": "GHI below physically possible upper limit",
        "cause": "Faulty sensor, wiring, calibration constant or timestamp",
    },
    "GHI_ERL_UL_TOANI_SZA": {
        "description": "GHI below extremely rare upper limit",
        "cause": "Calibration error",
    },
    "DIF_PPL_UL_TOANI_SZA": {
        "description": "DHI below physically possible upper limit",
        "cause": "Faulty sensor, wiring, calibration constant or timestamp",
    },
    "DIF_ERL_UL_TOANI_SZA": {
        "description": "DHI below extremely rare upper limit",
        "cause": "Calibration error or MS-80 not shaded",
    },
    "DNI_PPL_UL_TOANI": {
        "description": "DNI below physically possible upper limit",
        "cause": "Faulty sensor, wiring, calibration constant or timestamp",
    },
    "DNI_ERL_UL_TOANI_SZA": {
        "description": "DNI below extremely rare upper limit",
        "cause": "Calibration error",
    },
    "K_UL_SZA": {
        "description": "Diffuse fraction K < 1.05 (Z < 75°) or 1.10",
        "cause": "DHI too high or GHI too low: calibration or GHI soiling",
    },
    "K_UL_KT": {
        "description": "K ≤ 0.96 when Kt > 0.6 (Geuder)",
        "cause": "MS-80 not shaded: tracker off or misaligned",
    },
    "Kn_UL_KT": {
        "description": "Kn below Kt",
        "cause": "DNI too high or GHI too low",
    },
    "Kn_LL_KT": {
        "description": "Kn > 0.0171 when Kt ≥ 0.533 (Forstinger)",
        "cause": "Pyrheliometer off sun: tracker stopped or misaligned",
    },
    "ClosureRatio_tol_SZA": {
        "description": "GHI matches DHI + DNI·cos Z within 8% (Z ≤ 75°) or 15%",
        "cause": "Sensors disagree: soiling, misalignment, drift or clock offset",
    },
    "ClosureDelta_tol_TOAHI": {
        "description": "GHI matches DHI + DNI·cos Z within 3% of TOA or 7.5 W/m² (Maxwell)",
        "cause": "Sensors disagree: soiling, misalignment, drift or clock offset",
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


def add_test_info(summary):
    info = pd.DataFrame.from_dict(TEST_INFO, orient="index")
    return info.join(summary, how="right")
