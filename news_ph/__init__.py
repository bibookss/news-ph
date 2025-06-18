import dagster as dg

from .assets import abs_cbn
from .resources import abs_cbn_resource, duck_db_pandas_io
from .jobs import abs_cbn_job
from .schedules import abs_cbn_daily_schedule

abs_cbn_assets = dg.load_assets_from_modules([abs_cbn], group_name="news")
all_jobs = [abs_cbn_job]
all_schedules = [abs_cbn_daily_schedule]

defs = dg.Definitions(
    assets=abs_cbn_assets,
    resources={
        "abs_cbn": abs_cbn_resource,
        "io_manager": duck_db_pandas_io
    },
    jobs=all_jobs,
    schedules=all_schedules,
)
