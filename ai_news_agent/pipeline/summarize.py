from __future__ import annotations

from typing import Protocol

from ai_news_agent.utils.text import normalize_whitespace, truncate_text


class Summarizer(Protocol):
    async def summarize(self, article: dict[str, str]) -> str:
        """Return a summary for an article."""


class HeuristicSummarizer:
    async def summarize(self, article: dict[str, str]) -> str:
        summary = normalize_whitespace(article.get("summary", ""))
        if summary:
            return truncate_text(summary, 220)

        title = normalize_whitespace(article.get("title", ""))
        source = normalize_whitespace(article.get("source", ""))
        return truncate_text(f"{title} | 来源: {source}", 220)


async def summarize_articles(
    articles: list[dict[str, str]],
    summarizer: Summarizer | None = None,
) -> list[dict[str, str]]:
    engine = summarizer or HeuristicSummarizer()
    summarized: list[dict[str, str]] = []
    for article in articles:
        summary = await engine.summarize(article)
        summarized.append({**article, "summary": summary})
    return summarized

