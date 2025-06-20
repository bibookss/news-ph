import dagster as dg

from .assets import abs_cbn, dbt
from .jobs import abs_cbn_job
from .resources import abs_cbn_resource, dbt_cli_resource, duck_db_pandas_io
from .schedules import abs_cbn_daily_schedule

abs_cbn_assets = dg.load_assets_from_modules([abs_cbn])


all_jobs = [abs_cbn_job]
all_schedules = [abs_cbn_daily_schedule]

defs = dg.Definitions(
    assets=abs_cbn_assets + [dbt.abs_cbn_dbt_assets],
    resources={
        "abs_cbn": abs_cbn_resource,
        "io_manager": duck_db_pandas_io,
        "dbt": dbt_cli_resource,
    },
    jobs=all_jobs,
    schedules=all_schedules,
)
