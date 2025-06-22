import time
from datetime import datetime

import dagster as dg
import requests


class ABSCBNResource(dg.ConfigurableResource):
    def get_news_list_by_topic(
        self, section_id: str, limit: int = 10, offset: int = 0
    ) -> list[dict]:
        if section_id not in self.topics:
            raise ValueError(f"{section_id} is not supported!")

        url = "https://od2-content-api.abs-cbn.com/prod/latest"
        params = {
            "sectionId": section_id,
            "partner": "imp-01",
            "limit": limit,
            "offset": offset,
        }

        response = requests.get(url, params=params, headers=self.headers).json()[
            "listItem"
        ]
        time.sleep(0.2)
        return response

    def get_news_by_slugline_url(self, slugline_url: str) -> dict:
        url = "https://od2-content-api.abs-cbn.com/prod/item"
        params = {"url": slugline_url}

        response = requests.get(url, params=params, headers=self.headers).json()["data"]
        time.sleep(0.2)
        return response

    def get_news_list_by_topic_and_date(
        self,
        section_id: str,
        start_date: datetime,
        end_date: datetime,
        max_pages: int = 100,
        page_size: int = 20,
    ) -> list[dict]:
        if section_id not in self.topics:
            raise ValueError(f"{section_id} is not supported!")

        offset = 0
        collected = []

        for _ in range(max_pages):
            news_batch = self.get_news_list_by_topic(
                section_id, limit=page_size, offset=offset
            )
            if not news_batch:
                break

            for item in news_batch:
                created_date = datetime.fromisoformat(
                    item["createdDateFull"].replace("Z", "+00:00")
                ).replace(tzinfo=None)
                if start_date <= created_date < end_date:
                    collected.append(item)

            oldest = news_batch[-1]
            created_date = created_date = datetime.fromisoformat(
                oldest["createdDateFull"].replace("Z", "+00:00")
            ).replace(tzinfo=None)
            if created_date < start_date:
                break

            offset += page_size

        return collected

    @property
    def headers(self) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "origin": "https://www.abs-cbn.com",
            "priority": "u=1, i",
            "referer": "https://www.abs-cbn.com/",
            "user-agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
            ),
        }

    @property
    def topics(self) -> list[str]:
        return [
            "nation",
            "regions",
            "world",
            "health-science",
            "business",
            "technology",
            "weather-traffic",
        ]
