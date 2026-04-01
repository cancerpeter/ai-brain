from __future__ import annotations

from ai_news_agent.crawlers.ai_news import ArtificialIntelligenceNewsCrawler
from ai_news_agent.crawlers.arxiv import ArxivCrawler
from ai_news_agent.crawlers.bair import BAIRCrawler
from ai_news_agent.crawlers.deepmind import DeepMindCrawler
from ai_news_agent.crawlers.huggingface import HuggingFaceCrawler
from ai_news_agent.crawlers.kdnuggets import KDNuggetsCrawler
from ai_news_agent.crawlers.marktechpost import MarkTechPostCrawler
from ai_news_agent.crawlers.mit import MITCrawler
from ai_news_agent.crawlers.openai import OpenAIBlogCrawler
from ai_news_agent.crawlers.paperswithcode import PapersWithCodeCrawler
from ai_news_agent.crawlers.theverge import TheVergeCrawler


ALL_CRAWLERS = [
    ArtificialIntelligenceNewsCrawler,
    TheVergeCrawler,
    OpenAIBlogCrawler,
    DeepMindCrawler,
    BAIRCrawler,
    MITCrawler,
    HuggingFaceCrawler,
    KDNuggetsCrawler,
    MarkTechPostCrawler,
    ArxivCrawler,
    PapersWithCodeCrawler,
]

# Business Insider AI is currently excluded because its previous section and RSS
# endpoints are no longer stable enough for automated daily ingestion.
