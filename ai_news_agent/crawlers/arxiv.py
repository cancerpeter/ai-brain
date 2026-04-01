from __future__ import annotations

from ai_news_agent.config.sources import SOURCE_DEFINITIONS
from ai_news_agent.crawlers.base import RSSHTMLCrawler
from ai_news_agent.utils.text import normalize_whitespace, strip_html

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


class ArxivCrawler(RSSHTMLCrawler):
    source = next(item for item in SOURCE_DEFINITIONS if item.key == "arxiv_cs_ai")

    def parse_html(self, html: str):
        if BeautifulSoup is None:
            return super().parse_html(html)

        soup = BeautifulSoup(html, "lxml")
        dates = soup.select("dl > dt")
        details = soup.select("dl > dd")
        articles = []

        for dt_node, dd_node in zip(dates, details, strict=False):
            title_node = dd_node.select_one("div.list-title")
            abstract_link = dt_node.select_one("a[title='Abstract']")
            summary_node = dd_node.select_one("p.mathjax")
            if not title_node or not abstract_link:
                continue

            title = normalize_whitespace(title_node.get_text(" ", strip=True).replace("Title:", "", 1))
            article = self.build_article(
                title=title,
                url=abstract_link.get("href", ""),
                summary=strip_html(summary_node.decode_contents()) if summary_node else "",
                publish_time="",
            )
            if article:
                articles.append(article)
            if len(articles) >= self.max_items:
                break

        return articles
