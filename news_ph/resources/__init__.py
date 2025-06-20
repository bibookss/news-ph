from dagster_dbt import DbtCliResource
from dagster_duckdb_pandas import DuckDBPandasIOManager

from ..assets import constants
from .abs_cbn import ABSCBNResource

abs_cbn_resource = ABSCBNResource()
duck_db_pandas_io = DuckDBPandasIOManager(database=constants.DUCKDB_PATH)  # type: ignore
dbt_cli_resource = DbtCliResource(
    project_dir=constants.DBT_PROJECT_DIR,
)
