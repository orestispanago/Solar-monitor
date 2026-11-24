import json
import os

from dotenv import load_dotenv

dirname = os.path.dirname(__file__)
config_file = os.path.join(dirname, "config.json")
load_dotenv(os.path.join(dirname, ".env"))

with open(config_file, "r") as f:
    configs = json.load(f)

SOLAR_DIR = "raw/solar"
SUNTRACKER_DIR = "raw/suntracker"
SUNTRACKER_CR1000_START = "2025-04-27"

OUT_DIR = "out"

LATITUDE = 38.29136
LONGITUDE = 21.78858
ELEVATION = 44.5

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECIPIENTS = configs.get("EMAIL_RECIPIENTS")
