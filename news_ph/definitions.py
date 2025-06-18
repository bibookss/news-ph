from dagster import Definitions, ResourceDependency, load_assets_from_modules
from dagster_duckdb_pandas import DuckDBPandasIOManager

from news_ph import assets  # noqa: TID252

from .abscbn import ABSCBNResource

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": DuckDBPandasIOManager(database="news.duckdb"),
        "abs_cbn": ABSCBNResource(),
    },
)
