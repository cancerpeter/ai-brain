from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from ai_news_agent.logger import logger
from ai_news_agent.pipeline.clean import clean_articles
from ai_news_agent.pipeline.deduplicate import deduplicate_articles
from ai_news_agent.pipeline.fetch import fetch_all_sources
from ai_news_agent.pipeline.summarize import summarize_articles
from ai_news_agent.storage.json_store import JsonStore
from ai_news_agent.storage.markdown_store import MarkdownStore
from ai_news_agent.workflow.reporting import build_daily_markdown_report


RECENT_HOURS = 72
MIN_FRESH_TARGET = 24


def _parse_publish_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).astimezone(timezone.utc)
    except ValueError:
        return None


def _article_sort_key(article: dict[str, str]) -> tuple[datetime, str, str]:
    publish_time = _parse_publish_time(article.get("publish_time", "")) or datetime.min.replace(
        tzinfo=timezone.utc
    )
    return (publish_time, article.get("source", ""), article.get("title", ""))


def _load_previous_title_hashes(output_dir: Path, *, current_run: datetime) -> tuple[set[str], str]:
    current_day = current_run.strftime("%Y%m%d")
    history_files = [
        path
        for path in sorted(output_dir.glob("ai_news_*.json"))
        if not path.name.startswith(f"ai_news_{current_day}_")
    ]
    if not history_files:
        return set(), ""

    latest = history_files[-1]
    try:
        payload = json.loads(latest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("Failed to read previous AI news payload: %s", latest)
        return set(), ""

    hashes = {
        str(article.get("title_hash", "")).strip()
        for article in payload.get("articles", [])
        if str(article.get("title_hash", "")).strip()
    }
    return hashes, str(latest)


def _prioritize_latest_articles(
    articles: list[dict[str, str]],
    *,
    previous_hashes: set[str],
) -> tuple[list[dict[str, str]], dict[str, object]]:
    now = datetime.now(timezone.utc)
    recency_cutoff = now.timestamp() - RECENT_HOURS * 3600
    fresh_recent: list[dict[str, str]] = []
    fresh_older: list[dict[str, str]] = []
    repeated_recent: list[dict[str, str]] = []
    repeated_older: list[dict[str, str]] = []

    for article in sorted(articles, key=_article_sort_key, reverse=True):
        title_hash = article.get("title_hash", "")
        publish_time = _parse_publish_time(article.get("publish_time", ""))
        is_recent = publish_time is not None and publish_time.timestamp() >= recency_cutoff
        is_repeat = title_hash in previous_hashes if title_hash else False
        enriched = {
            **article,
            "is_recent": "true" if is_recent else "false",
            "seen_in_previous_run": "true" if is_repeat else "false",
        }
        if is_repeat and is_recent:
            repeated_recent.append(enriched)
        elif is_repeat:
            repeated_older.append(enriched)
        elif is_recent:
            fresh_recent.append(enriched)
        else:
            fresh_older.append(enriched)

    prioritized = [*fresh_recent, *fresh_older]
    if len(prioritized) < MIN_FRESH_TARGET:
        deficit = MIN_FRESH_TARGET - len(prioritized)
        prioritized.extend(repeated_recent[:deficit])
        prioritized.extend(repeated_older[: max(0, deficit - len(repeated_recent[:deficit]))])
    else:
        prioritized.extend(repeated_recent)
        prioritized.extend(repeated_older)

    metadata = {
        "recent_window_hours": RECENT_HOURS,
        "fresh_article_count": len(fresh_recent) + len(fresh_older),
        "fresh_recent_count": len(fresh_recent),
        "repeated_article_count": len(repeated_recent) + len(repeated_older),
    }
    return prioritized, metadata


async def run_daily_pipeline(max_items_per_source: int = 10) -> dict[str, object]:
    current_run = datetime.now(timezone.utc)
    raw_articles = await fetch_all_sources(max_items_per_source=max_items_per_source)
    cleaned_articles = clean_articles(raw_articles)
    unique_articles = deduplicate_articles(cleaned_articles)
    summarized_articles = await summarize_articles(unique_articles)
    json_store = JsonStore()
    previous_hashes, previous_payload_path = _load_previous_title_hashes(
        json_store.output_dir,
        current_run=current_run,
    )
    prioritized_articles, freshness = _prioritize_latest_articles(
        summarized_articles,
        previous_hashes=previous_hashes,
    )

    payload = {
        "generated_at": current_run.isoformat(),
        "total_raw": len(raw_articles),
        "total_cleaned": len(cleaned_articles),
        "total_unique": len(prioritized_articles),
        "articles": prioritized_articles,
        "selection": {
            **freshness,
            "previous_payload_path": previous_payload_path,
            "latest_first": True,
        },
    }

    output_path = json_store.save(payload)
    payload["json_output_path"] = str(output_path)
    logger.info("Saved daily pipeline output to %s", output_path)

    report_store = MarkdownStore()
    report_name = f"{datetime.now().strftime('%Y-%m-%d')}-ai-news-agent-daily.md"
    report_content = build_daily_markdown_report(payload)
    report_path = report_store.save(report_content, report_name)
    logger.info("Saved markdown daily report to %s", report_path)

    return {
        "output_path": str(output_path),
        "report_path": str(report_path),
        "payload": payload,
    }
