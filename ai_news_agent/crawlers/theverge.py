from __future__ import annotations

from ai_news_agent.config.sources import SOURCE_DEFINITIONS
from ai_news_agent.crawlers.base import RSSHTMLCrawler


class TheVergeCrawler(RSSHTMLCrawler):
    source = next(item for item in SOURCE_DEFINITIONS if item.key == "the_verge_ai")

