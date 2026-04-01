from __future__ import annotations

from ai_news_agent.utils.text import title_hash


def deduplicate_articles(articles: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[str] = set()
    deduplicated: list[dict[str, str]] = []

    for article in articles:
        fingerprint = title_hash(article.get("title", ""))
        if not fingerprint or fingerprint in seen:
            continue
        seen.add(fingerprint)
        deduplicated.append({**article, "title_hash": fingerprint})

    return deduplicated

