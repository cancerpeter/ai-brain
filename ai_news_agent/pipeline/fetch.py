from __future__ import annotations

import asyncio

from ai_news_agent.crawlers import ALL_CRAWLERS
from ai_news_agent.logger import logger


async def fetch_all_sources(max_items_per_source: int = 10) -> list[dict[str, str]]:
    crawler_instances = [crawler_cls(max_items=max_items_per_source) for crawler_cls in ALL_CRAWLERS]
    results = await asyncio.gather(
        *(crawler.get_articles() for crawler in crawler_instances),
        return_exceptions=True,
    )

    merged: list[dict[str, str]] = []
    for crawler, result in zip(crawler_instances, results, strict=False):
        if isinstance(result, Exception):
            logger.error("Crawler failed: %s | %s", crawler.source.name, result)
            continue
        merged.extend(result)

    logger.info("Fetched %s raw articles from %s sources", len(merged), len(crawler_instances))
    return merged

