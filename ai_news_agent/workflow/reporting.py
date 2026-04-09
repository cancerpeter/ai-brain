from __future__ import annotations

import html
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


LOCAL_TZ = ZoneInfo("Asia/Shanghai")


@dataclass(frozen=True, slots=True)
class ThemeRule:
    name: str
    keywords: tuple[str, ...]
    description: str


THEME_RULES: tuple[ThemeRule, ...] = (
    ThemeRule(
        name="AI 智能体与执行系统",
        keywords=("agent", "agents", "identity", "openclaw", "sima", "robot", "workflow"),
        description="从会回答问题的模型，走向能在真实环境中执行任务的 agent 系统。",
    ),
    ThemeRule(
        name="AI 安全、治理与风险控制",
        keywords=("safety", "bug bounty", "model spec", "harmful", "risk", "secure", "governance"),
        description="能力之外，行业正在把安全边界、责任归属和审计能力前置成产品特性。",
    ),
    ThemeRule(
        name="AI for Science",
        keywords=("genome", "genetic", "protein", "materials", "earth", "science", "defects"),
        description="AI 正在持续渗透生命科学、材料科学、地球观测和科研自动化。",
    ),
    ThemeRule(
        name="多模态内容生成",
        keywords=("music", "image", "video", "audio", "voice", "sound", "creative"),
        description="生成式 AI 从文本继续向音乐、图像、视频和语音工具链扩张。",
    ),
    ThemeRule(
        name="开发者工具与开源生态",
        keywords=("open source", "embedding", "framework", "libraries", "hugging face", "evaluation"),
        description="开源模型、评测框架与组件化库仍是 AI 扩散速度的重要放大器。",
    ),
)


def _decoded(article: dict[str, str], key: str) -> str:
    return html.unescape(article.get(key, "")).strip()


def _theme_hits(articles: list[dict[str, str]]) -> list[tuple[ThemeRule, list[dict[str, str]]]]:
    results: list[tuple[ThemeRule, list[dict[str, str]]]] = []
    for rule in THEME_RULES:
        matched: list[dict[str, str]] = []
        for article in articles:
            haystack = f"{_decoded(article, 'title')} {_decoded(article, 'summary')}".lower()
            if any(keyword in haystack for keyword in rule.keywords):
                matched.append(article)
        if matched:
            results.append((rule, matched))
    results.sort(key=lambda item: len(item[1]), reverse=True)
    return results


def build_daily_markdown_report(payload: dict[str, object]) -> str:
    generated_at = datetime.fromisoformat(str(payload["generated_at"])).astimezone(LOCAL_TZ)
    report_date = generated_at.strftime("%Y-%m-%d")
    articles = list(payload["articles"])
    selection = payload.get("selection", {})
    source_counts = Counter(_decoded(article, "source") for article in articles)
    category_counts = Counter(_decoded(article, "category") for article in articles)
    theme_hits = _theme_hits(articles)

    lines: list[str] = []
    lines.append(f"# AI 前沿日报｜{report_date}")
    lines.append("")
    lines.append(f"更新时间：{generated_at.strftime('%Y-%m-%d %H:%M:%S')}（Asia/Shanghai）")
    lines.append("")
    lines.append("> 本报告由 `ai_news_agent` 自动生成，聚焦今天抓到的新技术信号、值得持续跟踪的趋势，以及我认为最值得展开的方向。")
    lines.append("")
    lines.append("## 1. 今日概览")
    lines.append("")
    lines.append(f"- 抓取来源：{len(source_counts)}")
    lines.append(f"- 原始文章数：{payload['total_raw']}")
    lines.append(f"- 去重后文章数：{payload['total_unique']}")
    lines.append(
        "- 类别分布："
        + " / ".join(f"{name or 'unknown'} {count}" for name, count in category_counts.most_common())
    )
    lines.append(
        "- 主要来源："
        + " / ".join(f"{name} {count}" for name, count in source_counts.most_common(6))
    )
    if selection:
        lines.append(
            f"- 最新优先策略：近 {selection.get('recent_window_hours', 72)} 小时内容优先，"
            f"本轮新标题 {selection.get('fresh_article_count', 0)} 条，"
            f"其中近窗内 {selection.get('fresh_recent_count', 0)} 条，"
            f"与上一轮重复 {selection.get('repeated_article_count', 0)} 条"
        )
    lines.append("")
    lines.append("## 2. 当前出现的新技术与新方向")
    lines.append("")

    if not theme_hits:
        lines.append("- 今日抓取内容没有形成足够明显的主题聚类，更适合按来源逐篇浏览。")
    else:
        for index, (rule, matched) in enumerate(theme_hits[:5], start=1):
            sample_titles = "；".join(_decoded(item, "title") for item in matched[:3])
            lines.append(f"{index}. {rule.name}")
            lines.append(f"   {rule.description}")
            lines.append(f"   今日信号：{len(matched)} 条相关内容。样本包括：{sample_titles}")
    lines.append("")
    lines.append("## 3. 我最感兴趣的技术与趋势")
    lines.append("")

    focus_topics = theme_hits[:3]
    if not focus_topics:
        lines.append("- 当前没有足够明显的高密度主题，建议先扩大抓取窗口或补充更多源。")
    else:
        for rule, matched in focus_topics:
            lines.append(f"### {rule.name}")
            lines.append("")
            lines.append(f"我会优先关注这个方向，因为它代表着 {rule.description}")
            lines.append("")
            lines.append("值得展开的原因：")
            lines.append(
                f"- 今天至少出现了 {len(matched)} 条直接相关内容，说明它不是孤立事件，而是持续被多个来源反复提及。"
            )
            lines.append(
                f"- 相关信号横跨 {', '.join(sorted({_decoded(item, 'source') for item in matched[:5]}))}，说明它既有媒体热度，也有研究或产品落地迹象。"
            )
            lines.append(
                "- 如果这个方向继续升温，后续通常会带来产品形态变化、开发者工具更新，或者企业采用方式改变。"
            )
            lines.append("")
            lines.append("今日代表内容：")
            for item in matched[:4]:
                lines.append(f"- {_decoded(item, 'title')}  ")
                lines.append(f"  来源：{_decoded(item, 'source')}  ")
                lines.append(f"  链接：<{item['url']}>")
            lines.append("")

    lines.append("## 4. 重点文章速览")
    lines.append("")
    for article in articles[:12]:
        lines.append(f"- {_decoded(article, 'title')}  ")
        lines.append(f"  来源：{_decoded(article, 'source')} / 分类：{_decoded(article, 'category')}  ")
        lines.append(f"  链接：<{article['url']}>")
    lines.append("")
    lines.append("## 5. 今日结论")
    lines.append("")

    if focus_topics:
        joined = "、".join(rule.name for rule, _ in focus_topics)
        lines.append(
            f"今天最值得持续跟踪的主线是：{joined}。这说明 AI 行业的关注点已经不只是单点模型能力，而是在同步向执行系统、安全治理、科研应用和开发者生态扩展。"
        )
    else:
        lines.append("今天的资讯更分散，没有压倒性的单一主线，但整体仍围绕 AI 落地、研究和生态演进展开。")

    lines.append("")
    lines.append("## 6. 数据文件")
    lines.append("")
    lines.append(f"- JSON：`{payload.get('json_output_path', '')}`")
    return "\n".join(lines)
