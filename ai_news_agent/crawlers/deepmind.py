from __future__ import annotations

import re

from ai_news_agent.config.sources import SOURCE_DEFINITIONS
from ai_news_agent.crawlers.base import RSSHTMLCrawler
from ai_news_agent.utils.text import normalize_whitespace

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class DeepMindCrawler(RSSHTMLCrawler):
    source = next(item for item in SOURCE_DEFINITIONS if item.key == "deepmind_blog")

    def parse_html(self, html: str):
        if BeautifulSoup is None:
            return self._parse_with_regex(html)

        soup = BeautifulSoup(html, "lxml")
        articles = []
        seen_urls: set[str] = set()

        for link in soup.select("a[href^='/blog/']"):
            href = normalize_whitespace(link.get("href", ""))
            if not href or href in {"/blog/", "/blog"} or "/page/" in href:
                continue

            title = normalize_whitespace(link.get_text(" ", strip=True))
            if not title:
                title = self._title_from_href(href)
            if len(title) < 12 or title.lower() in {"news", "learn more"}:
                continue

            article = self.build_article(title=title, url=href)
            if not article or article.url in seen_urls:
                continue

            seen_urls.add(article.url)
            articles.append(article)
            if len(articles) >= self.max_items:
                break

        if articles:
            return articles

        return self._parse_with_regex(html)

    def _parse_with_regex(self, html: str):
        pattern = re.compile(r"/blog/[^\"?# <]+", re.IGNORECASE)
        articles = []
        seen_urls: set[str] = set()

        for match in pattern.finditer(html):
            href = normalize_whitespace(match.group(0).rstrip(">"))
            if not href or href in {"/blog/", "/blog"} or "/page/" in href:
                continue

            title = self._title_from_href(href)
            if len(title) < 12 or title.lower() in {"news", "learn more"}:
                continue

            article = self.build_article(title=title, url=href)
            if not article or article.url in seen_urls:
                continue

            seen_urls.add(article.url)
            articles.append(article)
            if len(articles) >= self.max_items:
                break

        return articles

    @staticmethod
    def _title_from_href(href: str) -> str:
        slug = href.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ")
        return normalize_whitespace(title.title())
