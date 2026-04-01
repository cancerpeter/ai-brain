from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any
from urllib import request
from urllib.parse import urljoin
from xml.etree import ElementTree

from ai_news_agent.config.sources import SourceDefinition
from ai_news_agent.logger import logger
from ai_news_agent.parsers.html_parser import parse_article_cards
from ai_news_agent.utils.text import normalize_whitespace, parse_datetime_to_iso, strip_html, truncate_text

try:
    import httpx
except ImportError:  # pragma: no cover
    httpx = None

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

try:
    import feedparser
except ImportError:  # pragma: no cover
    feedparser = None


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    )
}


@dataclass(slots=True)
class Article:
    title: str
    url: str
    summary: str
    publish_time: str
    source: str
    category: str

    def to_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "publish_time": self.publish_time,
            "source": self.source,
            "category": self.category,
        }


class CrawlerError(RuntimeError):
    """Raised when a crawler cannot fetch or parse a source."""


class BaseCrawler:
    source: SourceDefinition

    def __init__(
        self,
        timeout: float = 25.0,
        retries: int = 3,
        max_items: int = 10,
    ) -> None:
        self.timeout = timeout
        self.retries = retries
        self.max_items = max_items

    async def get_articles(self) -> list[dict[str, str]]:
        raise NotImplementedError

    async def fetch_text(self, client: Any, url: str) -> str:
        last_error: Exception | None = None
        for attempt in range(1, self.retries + 1):
            try:
                if client is not None:
                    response = await client.get(url, follow_redirects=True)
                    response.raise_for_status()
                    response.encoding = response.encoding or "utf-8"
                    return response.text
                return await self.fetch_text_stdlib(url)
            except Exception as exc:  # pragma: no cover - network runtime
                last_error = exc
                logger.warning("%s fetch failed (%s/%s): %s", self.source.name, attempt, self.retries, exc)
                await asyncio.sleep(min(1.0 * attempt, 3.0))

        raise CrawlerError(f"Failed to fetch {url}: {last_error}")

    async def fetch_text_requests_fallback(self, url: str) -> str:
        if requests is None:
            return await self.fetch_text_stdlib(url)

        def _sync_get() -> str:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.encoding or "utf-8"
            return response.text

        return await asyncio.to_thread(_sync_get)

    async def fetch_text_stdlib(self, url: str) -> str:
        def _sync_get() -> str:
            req = request.Request(url, headers=DEFAULT_HEADERS)
            with request.urlopen(req, timeout=self.timeout) as response:
                return response.read().decode("utf-8", errors="ignore")

        return await asyncio.to_thread(_sync_get)

    def build_article(
        self,
        *,
        title: str,
        url: str,
        summary: str = "",
        publish_time: str = "",
    ) -> Article | None:
        cleaned_title = normalize_whitespace(title)
        cleaned_url = normalize_whitespace(url)
        if not cleaned_title or not cleaned_url:
            return None

        return Article(
            title=cleaned_title,
            url=urljoin(self.source.base_url, cleaned_url),
            summary=truncate_text(strip_html(summary), 280),
            publish_time=parse_datetime_to_iso(publish_time),
            source=self.source.name,
            category=self.source.category,
        )


class RSSHTMLCrawler(BaseCrawler):
    async def get_articles(self) -> list[dict[str, str]]:
        if httpx is not None:
            async with httpx.AsyncClient(timeout=self.timeout, headers=DEFAULT_HEADERS) as client:
                rss_articles = await self._try_rss(client)
                if rss_articles:
                    return [item.to_dict() for item in rss_articles[: self.max_items]]

                html_articles = await self._try_html(client)
                return [item.to_dict() for item in html_articles[: self.max_items]]

        rss_articles = await self._try_rss(None)
        if rss_articles:
            return [item.to_dict() for item in rss_articles[: self.max_items]]

        html_articles = await self._try_html(None)
        return [item.to_dict() for item in html_articles[: self.max_items]]

    async def _try_rss(self, client: Any) -> list[Article]:
        for rss_url in self.source.rss_urls:
            try:
                body = await self.fetch_text(client, rss_url)
                parsed = self.parse_rss(body)
                if parsed:
                    logger.info("%s fetched via RSS: %s items", self.source.name, len(parsed))
                    return parsed
            except Exception as exc:  # pragma: no cover - network runtime
                logger.warning("%s RSS failed for %s: %s", self.source.name, rss_url, exc)
        return []

    async def _try_html(self, client: Any) -> list[Article]:
        try:
            html = await self.fetch_text(client, self.source.entry_url)
        except Exception:  # pragma: no cover - network runtime
            html = await self.fetch_text_requests_fallback(self.source.entry_url)

        articles = self.parse_html(html)
        logger.info("%s fetched via HTML: %s items", self.source.name, len(articles))
        return articles

    def parse_rss(self, body: str) -> list[Article]:
        entries: list[Any] = []
        if feedparser is not None:
            parsed = feedparser.parse(body)
            entries = parsed.entries
        else:
            root = ElementTree.fromstring(body)
            entries = []
            for item in root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                payload = {}
                for child in item:
                    key = child.tag.split("}")[-1]
                    value = child.text or ""
                    if key == "link" and not value:
                        value = child.attrib.get("href", "")
                    payload[key] = value
                entries.append(payload)

        articles: list[Article] = []
        for entry in entries[: self.max_items * 2]:
            article = self._rss_entry_to_article(entry)
            if article:
                articles.append(article)
            if len(articles) >= self.max_items:
                break
        return articles

    def _rss_entry_to_article(self, entry: Any) -> Article | None:
        if isinstance(entry, dict):
            title = entry.get("title", "")
            url = entry.get("link", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            publish_time = entry.get("published", "") or entry.get("pubDate", "") or entry.get("updated", "")
        else:
            title = getattr(entry, "title", "")
            url = getattr(entry, "link", "")
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
            publish_time = (
                getattr(entry, "published", "")
                or getattr(entry, "pubDate", "")
                or getattr(entry, "updated", "")
            )
        return self.build_article(title=title, url=url, summary=summary, publish_time=publish_time)

    def parse_html(self, html: str) -> list[Article]:
        raw_articles = parse_article_cards(
            html=html,
            base_url=self.source.base_url,
            rules=self.source.html_rules,
            limit=self.max_items * 2,
        )
        articles: list[Article] = []
        for item in raw_articles:
            article = self.build_article(**item)
            if article:
                articles.append(article)
            if len(articles) >= self.max_items:
                break
        return articles
