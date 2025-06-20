from datetime import datetime, timedelta

import dagster as dg

from ..jobs import abs_cbn_raw_job


@dg.schedule(job=abs_cbn_raw_job, cron_schedule="*/30 * * * *")
def abs_cbn_raw_schedule(context: dg.ScheduleEvaluationContext) -> dg.RunRequest:
    # now = datetime.now().replace(second=0, microsecond=0)
    now = context.scheduled_execution_time.replace(second=0, microsecond=0)
    start_time = now - timedelta(minutes=30)

    start = start_time.strftime("%Y%m%d %H%M%S")
    end = now.strftime("%Y%m%d %H%M%S")

    return dg.RunRequest(
        run_key=f"abs-cbn-raw-{start}-{end}",
        run_config={
            "ops": {
                "abs_cbn_article_index_raw": {
                    "config": {
                        "start_datetime": start,
                        "end_datetime": end,
                        "section_id": "nation",
                    }
                }
            }
        },
    )
