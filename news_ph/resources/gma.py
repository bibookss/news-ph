import time
from datetime import datetime

import dagster as dg
import requests


class GMAResource(dg.ConfigurableResource):
    def get_latest_page_number_by_collection(self, collection: str) -> int:
        if collection not in self.collection_mapper:
            raise ValueError(f"{collection} is not supported!")

        url = f"https://apps.gmanetwork.com/news/archives/get_page_number"
        params = {"collection": self.collection_mapper[collection]}

        response = requests.get(url, params=params, headers=self.headers).json()[
            "page_num"
        ]
        time.sleep(0.2)
        return response

    def get_page_number_by_collection_and_month_year(
        self, collection: str, year: int, month: str
    ) -> int:
        if collection not in self.collection_mapper:
            raise ValueError(f"{collection} is not supported!")

        url = "https://apps.gmanetwork.com/news/archives/get_page_number"
        params = {
            "collection": self.collection_mapper[collection],
            "year": year,
            "month": month,
        }

        response = requests.get(url, params=params, headers=self.headers).json()[
            "page_num"
        ]
        time.sleep(0.2)
        return response

    # def get_news_list_by_collection(
    #     self, collection: str, start_date: datetime | None, end_date: datetime | None
    # ) -> list[dict]:
    #     if collection not in self.collection_mapper:
    #         raise ValueError(f"{collection} is not supported!")

    #     if not start_date and not end_date:
    #         page_num = self.get

    #     url = "https://data.gmanetwork.com/gno/widgets/grid_reverse_listing/story_news_nation/{page_number}.gz"
    #     response = requests.get(url, params=params, headers=self.headers).json()[
    #         "listItem"
    #     ]
    #     time.sleep(0.2)
    #     return response

    # def get_news_by_slugline_url(self, slugline_url: str) -> dict:
    #     url = "https://od2-content-api.abs-cbn.com/prod/item"
    #     params = {"url": slugline_url}

    #     response = requests.get(url, params=params, headers=self.headers).json()["data"]
    #     time.sleep(0.2)
    #     return response

    # def get_news_list_by_collection_and_date(
    #     self,
    #     collection_id: str,
    #     start_date: datetime,
    #     end_date: datetime,
    #     max_pages: int = 100,
    #     page_size: int = 20,
    # ) -> list[dict]:
    #     if collection_id not in self.collections:
    #         raise ValueError(f"{collection_id} is not supported!")

    #     offset = 0
    #     collected = []

    #     for _ in range(max_pages):
    #         news_batch = self.get_news_list_by_collection(
    #             collection_id, limit=page_size, offset=offset
    #         )
    #         if not news_batch:
    #             break

    #         for item in news_batch:
    #             created_date = datetime.fromisoformat(
    #                 item["createdDateFull"].replace("Z", "+00:00")
    #             ).replace(tzinfo=None)
    #             if start_date <= created_date < end_date:
    #                 collected.append(item)

    #         oldest = news_batch[-1]
    #         created_date = created_date = datetime.fromisoformat(
    #             oldest["createdDateFull"].replace("Z", "+00:00")
    #         ).replace(tzinfo=None)
    #         if created_date < start_date:
    #             break

    #         offset += page_size

    #     return collected

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://www.gmanetwork.com",
            "Referer": "https://www.gmanetwork.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        }

    @property
    def collection_mapper(self) -> dict:
        return {
            "nation": "story_news_nation",
            "world": "story_news_world",
            "regions": "story_news_regions",
            "weather": "story_scitech_weather",
            "technology": "story_scitech_technology",
        }
