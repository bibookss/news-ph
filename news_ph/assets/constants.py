import os
from zoneinfo import ZoneInfo

DUCKDB_PATH = os.getenv("DUCKDB_PATH")
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR")
DBT_MANIFEST_PATH = os.getenv("DBT_MANIFEST_PATH")
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE"))
