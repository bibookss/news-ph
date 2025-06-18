from .abs_cbn import ABSCBNResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

abs_cbn_resource = ABSCBNResource()
duck_db_pandas_io = DuckDBPandasIOManager(database="news.duckdb") # Set using env
