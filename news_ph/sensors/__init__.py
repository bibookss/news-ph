from datetime import datetime, timedelta

import dagster as dg

from ..jobs import abs_cbn_staging_job


@dg.asset_sensor(
    asset_key=dg.AssetKey("abs_cbn_article_detail_raw"), job_name="abs_cbn_staging_job"
)
def abs_cbn_staging_sensor():
    now = datetime.now()
    return dg.RunRequest(
        run_key=f"abs-cbn-staging-{now.strftime('%Y%m%d-%H%M')}",
    )
