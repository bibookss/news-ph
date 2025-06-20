import json
from datetime import datetime

import dagster as dg
import pandas as pd

from ..resources.abs_cbn import ABSCBNResource
from .constants import TIMEZONE


@dg.asset(
    config_schema={
        "start_datetime": dg.StringSource,
        "end_datetime": dg.StringSource,
        "section_id": str,
    }
)
def abs_cbn_article_index_raw(
    context: dg.AssetExecutionContext, abs_cbn: ABSCBNResource
) -> pd.DataFrame:
    cfg = context.op_config
    start = datetime.strptime(cfg["start_datetime"], "%Y%m%d %H%M%S").replace(
        tzinfo=None
    )
    end = datetime.strptime(cfg["end_datetime"], "%Y%m%d %H%M%S").replace(tzinfo=None)
    section_id = cfg["section_id"]

    context.log.info("Getting %s %s to %s", section_id, start, end)

    news = abs_cbn.get_news_list_by_topic_and_date(
        section_id=section_id,
        start_date=start,
        end_date=end,
    )

    if not news:
        context.log.warning("No news articles found in the given time window.")
        return pd.DataFrame(columns=["retrieved_at", "json_response"])

    return pd.DataFrame(
        [
            {
                "retrieved_at": datetime.now(tz=TIMEZONE).isoformat(),
                "json_response": json.dumps(news),
            }
        ]
    )


@dg.asset
def abs_cbn_article_detail_raw(
    context: dg.AssetExecutionContext,
    abs_cbn_article_index_raw: pd.DataFrame,
    abs_cbn: ABSCBNResource,
) -> pd.DataFrame:
    if abs_cbn_article_index_raw.empty:
        context.log.warning("No raw articles to process.")
        return pd.DataFrame(columns=["slugline_url", "retrieved_at", "json_response"])

    raw_json = abs_cbn_article_index_raw.iloc[0]["json_response"]
    news_list = json.loads(raw_json)

    detailed_articles = []
    for article in news_list:
        slug_url = article.get("slugline_url")
        if not slug_url:
            continue

        response = abs_cbn.get_news_by_slugline_url(slug_url)
        detailed_articles.append(
            {
                "slugline_url": slug_url,
                "retrieved_at": datetime.now(tz=TIMEZONE).isoformat(),
                "json_response": json.dumps(response),
            }
        )

    if not detailed_articles:
        context.log.warning("No detailed articles fetched.")
        return pd.DataFrame(columns=["slugline_url", "retrieved_at", "json_response"])

    return pd.DataFrame(detailed_articles)
