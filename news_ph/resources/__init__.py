from dagster_duckdb_pandas import DuckDBPandasIOManager

from .abs_cbn import ABSCBNResource

abs_cbn_resource = ABSCBNResource()
duck_db_pandas_io = DuckDBPandasIOManager(database="news.duckdb")  # Set using env
