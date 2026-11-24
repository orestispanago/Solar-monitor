import logging
import logging.config
import os
import traceback
from datetime import datetime, timezone

from mailer import send_mail
from qc import run_qc

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

os.makedirs("logs", exist_ok=True)
logging.config.fileConfig(
    "logging.conf",
    defaults={"logfile": "logs/midday_qc.log"},
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)

TRACKER_TESTS = ["Kn_LL_KT", "K_UL_KT"]


def main():
    today = datetime.now(tz=timezone.utc)
    summary = run_qc(today)
    tracker = summary.loc[TRACKER_TESTS].drop(columns="pct_failed")
    print(tracker)
    n_failed = tracker["n_failed"].sum()
    if n_failed > 0:
        send_mail(
            subject=f"Suntracker check: {n_failed} failures",
            html_table=tracker.reset_index().to_html(index=False),
        )


if __name__ == "__main__":
    try:
        main()
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
