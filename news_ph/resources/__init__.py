from dagster_duckdb_pandas import DuckDBPandasIOManager

from .abs_cbn import ABSCBNResource
from ..assets import constants


abs_cbn_resource = ABSCBNResource()
duck_db_pandas_io = DuckDBPandasIOManager(database=constants.DUCKDB_PATH)  #type: ignore
