import logging
import logging.config
import os
import traceback
from datetime import datetime, timezone

import pandas as pd

from qc import run_qc

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.makedirs("logs", exist_ok=True)

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfile": "logs/yesterday_qc.log"},
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)


def main():
    yesterday = datetime.now(tz=timezone.utc) - pd.Timedelta(1, unit="D")
    summary = run_qc(yesterday)
    print(summary)


if __name__ == "__main__":
    try:
        main()
        logger.info(f"{'-' * 15} SUCCESS {'-' * 15}")
    except:
        logger.error("uncaught exception: %s", traceback.format_exc())
