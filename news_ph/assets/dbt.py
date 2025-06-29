from pathlib import Path

from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from ..resources import dbt_cli_resource
from .constants import (
    DAGSTER_DBT_PARSE_PROJECT_ON_LOAD,
    DBT_MANIFEST_PATH,
)

if DAGSTER_DBT_PARSE_PROJECT_ON_LOAD:
    dbt_manifest_path = (
        dbt_cli_resource.cli(["--quiet", "parse"], target_path=Path("target"))
        .wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = DBT_MANIFEST_PATH


@dbt_assets(manifest=dbt_manifest_path)
def abs_cbn_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
