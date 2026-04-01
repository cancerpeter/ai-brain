from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urljoin

from ai_news_agent.utils.text import normalize_whitespace, strip_html

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None


@dataclass(slots=True)
class HTMLExtractionRule:
    list_selector: str
    title_selector: str
    link_selector: str | None = None
    summary_selector: str | None = None
    time_selector: str | None = None
    href_attr: str = "href"


def parse_article_cards(html: str, base_url: str, rules: list[HTMLExtractionRule], limit: int = 20) -> list[dict[str, str]]:
    if BeautifulSoup is None:
        return parse_article_cards_fallback(html=html, base_url=base_url, limit=limit)

    soup = BeautifulSoup(html, "lxml")
    articles: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for rule in rules:
        for node in soup.select(rule.list_selector):
            title_node = node.select_one(rule.title_selector)
            link_node = node.select_one(rule.link_selector or rule.title_selector)
            if not title_node or not link_node:
                continue

            title = normalize_whitespace(title_node.get_text(" ", strip=True))
            href = normalize_whitespace(link_node.get(rule.href_attr, ""))
            url = urljoin(base_url, href)
            if not title or not url or url in seen_urls:
                continue

            summary = ""
            if rule.summary_selector:
                summary_node = node.select_one(rule.summary_selector)
                if summary_node:
                    summary = strip_html(summary_node.decode_contents())

            publish_time = ""
            if rule.time_selector:
                time_node = node.select_one(rule.time_selector)
                if time_node:
                    publish_time = normalize_whitespace(time_node.get_text(" ", strip=True))
                    if not publish_time and time_node.has_attr("datetime"):
                        publish_time = normalize_whitespace(time_node["datetime"])

            articles.append(
                {
                    "title": title,
                    "url": url,
                    "summary": summary,
                    "publish_time": publish_time,
                }
            )
            seen_urls.add(url)
            if len(articles) >= limit:
                return articles

    return articles


def parse_article_cards_fallback(html: str, base_url: str, limit: int = 20) -> list[dict[str, str]]:
    pattern = re.compile(
        r"<a[^>]+href=[\"'](?P<href>[^\"']+)[\"'][^>]*>(?P<title>.*?)</a>",
        re.IGNORECASE | re.DOTALL,
    )
    articles: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for match in pattern.finditer(html):
        title = strip_html(match.group("title"))
        url = urljoin(base_url, normalize_whitespace(match.group("href")))
        if len(title) < 20 or not url or url in seen_urls:
            continue
        articles.append(
            {
                "title": title,
                "url": url,
                "summary": "",
                "publish_time": "",
            }
        )
        seen_urls.add(url)
        if len(articles) >= limit:
            break

    return articles
