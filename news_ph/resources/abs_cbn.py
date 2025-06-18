import time
from datetime import datetime

import dagster as dg
import requests


class ABSCBNResource(dg.ConfigurableResource):
    def get_news_list_by_topic(
        self, section_id: str, limit: int = 10, offset: int = 0
    ) -> list[dict]:
        if not section_id in self.topics:
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

    {
        "_created": "2025-06-17T13:33:31Z",
        "_etag": "64798e1788491f6175283c4c1b56059649635e16",
        "_id": "urn:newsml:od2-workbench-api.abs-cbn.com:2025-06-17T14:19:34.585683:531ff29d-e758-4bb1-ace1-11bbcc30e66e",
        "_updated": "2025-06-17T14:13:24Z",
        "associations": {
            "CoverImage": None,
            "Thumbnail": {
                "body_text": "The Department of Foreign Affairs along Macapagal Boulevard in Parañaque City in this photo taken on October 9, 2024",
                "byline": "Jonathan Cellona, ABS-CBN News",
                "description_text": "The Department of Foreign Affairs along Macapagal Boulevard in Parañaque City in this photo taken on October 9, 2024. Jonathan Cellona, ABS-CBN News",
                "headline": "DFA",
                "renditions": {
                    "baseImage": {
                        "media": "20250617140628/1dca428237d2736944dcd39776ba7fae42f5484c3a76c99d0c15f213663b8c0c.jpg"
                    }
                },
            },
            "photos": [],
            "products": [],
            "relatedContent": [],
            "showCasts": [],
            "showDesktopBanner": None,
            "showMobileBanner": None,
        },
        "attachments": None,
        "authors": [
            {
                "author_url": "zen-hernandez",
                "avatar_url": "https://od2-workbench-api.abs-cbn.com/api/upload-raw/20250213020232/c0a3dc4cbeaf109f27cd2f2a5ce559365197e4811014f6ecdb0bf64e3b402da3.jpg",
                "biography": "Zen Hernandez, a senior reporter and anchor for ABS-CBN News, covers foreign affairs and the Filipino diaspora. With 18 years of experience, she anchors TV Patrol Weekend and is a UP cum laude graduate with global journalism training.",
                "byline": "",
                "facebook": "https://www.facebook.com/profile.php?id=100045024427505",
                "instagram": "https://www.instagram.com/zenhernandez/?hl=en",
                "name": "Zen Hernandez",
                "pen_name": None,
                "sign_off": "ZH",
                "twitter": "@zenhernandez",
                "username": "zenhernandez",
            },
            {
                "author_url": "vivienne-gulla",
                "avatar_url": "https://od2-workbench-api.abs-cbn.com/api/upload-raw/20250213030256/c6c5d5c14c5468c62169550da6355761e779b7201f61abd13dd5f62bc0080d61.png",
                "biography": "Vivienne is a political journalist for ABS-CBN covering the House of Representatives and anchoring ANC’s Saturday Rundown. A magna cum laude Broadcast Communication graduate from UP Diliman, she reports on legislation, inquiries, and politics.",
                "byline": "",
                "facebook": "https://www.facebook.com/vivienne.gulla",
                "instagram": "https://www.instagram.com/viviennegulla/?hl=en",
                "name": "Vivienne Gulla",
                "pen_name": None,
                "sign_off": "VG",
                "twitter": "@VivienneGulla",
                "username": "viviennegulla",
            },
            {
                "author_url": "",
                "avatar_url": "",
                "biography": "",
                "byline": "",
                "facebook": "",
                "instagram": "",
                "name": "ABS-CBN News",
                "pen_name": None,
                "sign_off": "AN",
                "twitter": "",
                "username": "abscbnnews",
            },
        ],
        "body_html": None,
        "description_html": "<p>The officials were attending a short course in Israel, and are expected to come home over the weekend.</p>",
        "description_text": "The officials were attending a short course in Israel, and are expected to come home over the weekend.",
        "extra": {
            "EmbedId": None,
            "ReelContent": None,
            "SponsorName": None,
            "UnitId": None,
            "audio_url": None,
            "channelTimeslots": None,
            "credits": None,
            "duration": None,
            "endScheduleDate": None,
            "externalAuthor": None,
            "kenticoDateTimeUpdated": None,
            "kenticoID": None,
            "multimedia": None,
            "property": None,
            "rss_image": None,
            "rss_linkout": None,
            "rss_pubdate": None,
            "seasonEndYear": None,
            "seasonNo": None,
            "seasonStartYear": None,
            "short_title": "DFA facilitating return to PH of Filipino gov’t officials in Israel",
            "showDescription": None,
            "showKapamilyaLink": None,
            "showKapamilyaTime": None,
            "showMetaDescription": None,
            "showTfcLink": None,
            "slugline_url": "news/nation/2025/6/17/dfa-facilitating-return-to-ph-of-filipino-govt-officials-in-israel-2133",
            "startScheduleDate": None,
            "sync": None,
            "tags": "Israel, DFA, Department of Foreign Affairs, House of Representatives, ABSNews",
            "thumbnailURL": None,
        },
        "firstcreated": "2025-06-17T13:33:30Z",
        "firstpublished": "2025-06-17T13:33:30Z",
        "groups": None,
        "headline": "DFA facilitating return to PH of Filipino gov’t officials in Israel",
        "language": "en",
        "paginationToken": "CISgWBoJKRBIGH6XAQAAImo6aHVybjpuZXdzbWw6b2QyLXdvcmtiZW5jaC1hcGkuYWJzLWNibi5jb206MjAyNS0wNi0xN1QxNDoxOTozNC41ODU2ODM6NTMxZmYyOWQtZTc1OC00YmIxLWFjZTEtMTFiYmNjMzBlNjZl",
        "profile": "Article",
        "pubstatus": "usable",
        "slugline": "DFA facilitating return to PH of FIlipino govt officials in Israel",
        "source": "One Domain",
        "subject": [
            {"code": "pe", "name": "Professional/Editorial", "scheme": "ContentSource"},
            {"code": "standard", "name": "Standard", "scheme": "articleType"},
            {"code": "nation", "name": "Nation", "scheme": "section_id"},
            {"code": "english", "name": "English", "scheme": "article_language"},
            {"code": "IAB12-2", "name": "National News", "scheme": "iab-category"},
        ],
        "versioncreated": "2025-06-17T14:13:23Z",
        "wordcount": 250,
    }
