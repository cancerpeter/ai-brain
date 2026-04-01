from __future__ import annotations

from dataclasses import dataclass, field

from ai_news_agent.parsers.html_parser import HTMLExtractionRule


@dataclass(slots=True)
class SourceDefinition:
    key: str
    name: str
    category: str
    base_url: str
    entry_url: str
    rss_urls: list[str] = field(default_factory=list)
    html_rules: list[HTMLExtractionRule] = field(default_factory=list)
    enabled: bool = True


SOURCE_DEFINITIONS: list[SourceDefinition] = [
    SourceDefinition(
        key="artificial_intelligence_news",
        name="Artificial Intelligence News",
        category="news",
        base_url="https://artificialintelligence-news.com/",
        entry_url="https://artificialintelligence-news.com/",
        rss_urls=[
            "https://artificialintelligence-news.com/feed/",
            "https://artificialintelligence-news.com/category/artificial-intelligence/feed/",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article",
                title_selector="h2 a, h3 a",
                summary_selector="p",
                time_selector="time",
            )
        ],
    ),
    SourceDefinition(
        key="the_verge_ai",
        name="The Verge AI",
        category="news",
        base_url="https://www.theverge.com/",
        entry_url="https://www.theverge.com/ai-artificial-intelligence",
        rss_urls=[
            "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="div.duet--content-cards--content-card, div.c-entry-box--compact, article",
                title_selector="h2 a, h3 a, a[data-chorus-optimize-field='hed']",
                summary_selector="p",
                time_selector="time",
            )
        ],
    ),
    SourceDefinition(
        key="business_insider_ai",
        name="Business Insider AI",
        category="news",
        base_url="https://www.businessinsider.com/",
        entry_url="https://www.businessinsider.com/ai",
        rss_urls=[
            "https://www.businessinsider.com/rss",
            "https://www.businessinsider.com/sai/rss",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="section a[href*='/ai-'], article, div.river-post",
                title_selector="h2, h3, span[data-test='post-headline'], div[class*='headline']",
                link_selector="a[href]",
                summary_selector="p",
                time_selector="time",
            )
        ],
        enabled=False,
    ),
    SourceDefinition(
        key="openai_blog",
        name="OpenAI Blog",
        category="research",
        base_url="https://openai.com/",
        entry_url="https://openai.com/blog",
        rss_urls=[
            "https://openai.com/news/rss.xml",
            "https://openai.com/blog/rss.xml",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, div[class*='group']",
                title_selector="h2 a, h3 a, a[href*='/index/']",
                summary_selector="p",
                time_selector="time",
            )
        ],
    ),
    SourceDefinition(
        key="deepmind_blog",
        name="Google DeepMind Blog",
        category="research",
        base_url="https://deepmind.google/",
        entry_url="https://deepmind.google/blog/",
        rss_urls=[],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, li[class*='glue-card'], div[class*='card']",
                title_selector="h3 a, h2 a, a[href*='/blog/']",
                summary_selector="p",
                time_selector="time",
            )
        ],
    ),
    SourceDefinition(
        key="bair_blog",
        name="BAIR Blog",
        category="research",
        base_url="https://bair.berkeley.edu/",
        entry_url="https://bair.berkeley.edu/blog/",
        rss_urls=[
            "https://bair.berkeley.edu/blog/feed.xml",
            "https://bair.berkeley.edu/blog/feed/",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, div.post-preview, li",
                title_selector="h2 a, h3 a, a[href*='/blog/']",
                summary_selector="p",
                time_selector="time, small, .date",
            )
        ],
    ),
    SourceDefinition(
        key="mit_ai_news",
        name="MIT AI News",
        category="research",
        base_url="https://news.mit.edu/",
        entry_url="https://news.mit.edu/topic/artificial-intelligence2",
        rss_urls=[
            "https://news.mit.edu/rss/topic/artificial-intelligence2",
            "https://news.mit.edu/rss/topic/artificial-intelligence",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, .term-page--news-item, .view-content .views-row",
                title_selector="h3 a, h2 a",
                summary_selector="p",
                time_selector="time, .date, .news-date",
            )
        ],
    ),
    SourceDefinition(
        key="huggingface_blog",
        name="Hugging Face Blog",
        category="technical",
        base_url="https://huggingface.co/",
        entry_url="https://huggingface.co/blog",
        rss_urls=[
            "https://huggingface.co/blog/feed.xml",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, .grid article, a[href*='/blog/']",
                title_selector="h1, h2, h3, .prose h3",
                link_selector="a[href]",
                summary_selector="p",
                time_selector="time",
            )
        ],
    ),
    SourceDefinition(
        key="kdnuggets",
        name="KDnuggets",
        category="technical",
        base_url="https://www.kdnuggets.com/",
        entry_url="https://www.kdnuggets.com/",
        rss_urls=[
            "https://www.kdnuggets.com/feed",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, .post, .archive-list article",
                title_selector="h2 a, h3 a",
                summary_selector="p",
                time_selector="time, .loop-date",
            )
        ],
    ),
    SourceDefinition(
        key="marktechpost",
        name="MarkTechPost",
        category="technical",
        base_url="https://www.marktechpost.com/",
        entry_url="https://www.marktechpost.com/",
        rss_urls=[
            "https://www.marktechpost.com/feed/",
            "https://www.marktechpost.com/category/artificial-intelligence/feed/",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="article, .jeg_post, .td_module_wrap",
                title_selector="h3 a, h2 a",
                summary_selector="p",
                time_selector="time, .jeg_meta_date a",
            )
        ],
    ),
    SourceDefinition(
        key="arxiv_cs_ai",
        name="arXiv cs.AI",
        category="papers",
        base_url="https://arxiv.org/",
        entry_url="https://arxiv.org/list/cs.AI/recent",
        rss_urls=[
            "https://rss.arxiv.org/rss/cs.AI",
        ],
        html_rules=[
            HTMLExtractionRule(
                list_selector="dl > dt",
                title_selector="a[title='Abstract']",
                link_selector="a[title='Abstract']",
            )
        ],
    ),
    SourceDefinition(
        key="papers_with_code",
        name="Papers with Code",
        category="papers",
        base_url="https://paperswithcode.com/",
        entry_url="https://paperswithcode.com/",
        rss_urls=[],
        html_rules=[
            HTMLExtractionRule(
                list_selector="div.infinite-item, div.paper-card, article",
                title_selector="h1 a, h2 a, h3 a",
                summary_selector="p",
                time_selector="time, .date",
            )
        ],
    ),
]
