import pandas as pd
import dagster as dg
from datetime import datetime
from .abscbn import ABSCBNResource

@dg.asset(
    config_schema={
        "start_datetime": dg.StringSource,
        "end_datetime": dg.StringSource,
        "section_id": str,
    }
)
def abs_cbn_news_raw(context: dg.AssetExecutionContext, abs_cbn: ABSCBNResource) -> pd.DataFrame:
    cfg = context.op_config
    start = datetime.strptime(cfg["start_datetime"], "%Y%m%d %H%M%S").replace(tzinfo=None)
    end = datetime.strptime(cfg["end_datetime"], "%Y%m%d %H%M%S").replace(tzinfo=None)
    section_id = cfg["section_id"]

    news = abs_cbn.get_news_list_by_topic_and_date(
        section_id=section_id,
        start_date=start,
        end_date=end,
    )

    return pd.DataFrame(news)

@dg.asset
def abs_cbn_news_detail(abs_cbn_news_raw: pd.DataFrame, abs_cbn: ABSCBNResource) -> pd.DataFrame:
    detailed_articles = []
    for _, row in abs_cbn_news_raw.iterrows():
        slug_url = row["slugline_url"]
        detail = abs_cbn.get_news_by_slugline_url(slug_url)
        detailed_articles.append(detail)

    return pd.DataFrame(detailed_articles)

