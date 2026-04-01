from __future__ import annotations

from ai_news_agent.config.sources import SOURCE_DEFINITIONS
from ai_news_agent.crawlers.base import RSSHTMLCrawler


class BusinessInsiderCrawler(RSSHTMLCrawler):
    source = next(item for item in SOURCE_DEFINITIONS if item.key == "business_insider_ai")

