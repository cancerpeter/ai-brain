from __future__ import annotations

from ai_news_agent.utils.text import normalize_whitespace, parse_datetime_to_iso, truncate_text


def clean_articles(articles: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    for item in articles:
        title = normalize_whitespace(item.get("title", ""))
        url = normalize_whitespace(item.get("url", ""))
        if not title or not url:
            continue

        cleaned.append(
            {
                "title": title,
                "url": url,
                "summary": truncate_text(item.get("summary", ""), 280),
                "publish_time": parse_datetime_to_iso(item.get("publish_time", "")),
                "source": normalize_whitespace(item.get("source", "")),
                "category": normalize_whitespace(item.get("category", "")),
            }
        )
    return cleaned

