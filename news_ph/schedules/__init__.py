import dagster as dg
from datetime import datetime, timedelta
from ..jobs import abs_cbn_job

@dg.schedule(job=abs_cbn_job, cron_schedule="0 1 * * *")  
def abs_cbn_daily_schedule():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    start = yesterday.strftime("%Y%m%d %H%M%S")
    end = today.strftime("%Y%m%d %H%M%S")

    return dg.RunRequest(
        run_key=f"abs-cbn-{start}-{end}",
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