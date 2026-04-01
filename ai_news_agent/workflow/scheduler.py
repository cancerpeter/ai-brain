from __future__ import annotations

from datetime import datetime, timezone

from ai_news_agent.logger import logger
from ai_news_agent.pipeline.clean import clean_articles
from ai_news_agent.pipeline.deduplicate import deduplicate_articles
from ai_news_agent.pipeline.fetch import fetch_all_sources
from ai_news_agent.pipeline.summarize import summarize_articles
from ai_news_agent.storage.json_store import JsonStore
from ai_news_agent.storage.markdown_store import MarkdownStore
from ai_news_agent.workflow.reporting import build_daily_markdown_report


async def run_daily_pipeline(max_items_per_source: int = 10) -> dict[str, object]:
    raw_articles = await fetch_all_sources(max_items_per_source=max_items_per_source)
    cleaned_articles = clean_articles(raw_articles)
    unique_articles = deduplicate_articles(cleaned_articles)
    summarized_articles = await summarize_articles(unique_articles)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_raw": len(raw_articles),
        "total_cleaned": len(cleaned_articles),
        "total_unique": len(summarized_articles),
        "articles": summarized_articles,
    }

    json_store = JsonStore()
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
