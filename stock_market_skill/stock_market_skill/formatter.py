from __future__ import annotations

from .models import FxResult, KLineItem, ListItem, NewsItem, QuoteResult, RouteResult, ScreenedStock


def format_clarification(route: RouteResult) -> str:
    candidates = "\n".join(f"- {item}" for item in route.candidates)
    return (
        "我还不能安全判断你具体想查哪只标的，需要你补充更明确的股票名称或代码。\n"
        f"建议输入：\n{candidates}"
    )


def format_quote(result: QuoteResult) -> str:
    conclusion = (
        f"{result.name}（{result.code}）最新价为 {result.latest_price:.2f}，"
        f"较前值{'上涨' if result.change_amount >= 0 else '下跌'} {abs(result.change_amount):.2f} "
        f"（{result.change_percent:+.2f}%）。"
    )
    fields = (
        f"名称：{result.name}\n"
        f"代码：{result.code}\n"
        f"市场：{result.market}\n"
        f"最新价：{result.latest_price:.2f}\n"
        f"涨跌额：{result.change_amount:+.2f}\n"
        f"涨跌幅：{result.change_percent:+.2f}%\n"
        f"更新时间：{result.update_time or '暂无'}"
    )
    note = result.note or "当前结果为统一格式输出。"
    return f"{conclusion}\n\n{fields}\n\n补充说明：{note}"


def format_kline(symbol: str, items: list[KLineItem], limit: int = 5) -> str:
    if not items:
        return f"{symbol} 暂无可用 K 线数据。\n\n关键字段：无\n\n补充说明：可能是插件暂无返回或参数不完整。"

    visible = items[-limit:]
    trend = build_trend_summary(visible)
    rows = "\n".join(
        f"- {item.timestamp} | O:{item.open_price:.2f} H:{item.high_price:.2f} "
        f"L:{item.low_price:.2f} C:{item.close_price:.2f}"
        for item in visible
    )
    return (
        f"{symbol} 最近走势{trend}\n\n"
        f"关键字段：\n{rows}\n\n"
        "补充说明：当前仅展示最近若干条 OHLC 数据，后续可扩展均线、成交量和更多统计。"
    )


def build_trend_summary(items: list[KLineItem]) -> str:
    if len(items) < 2:
        return "数据较少，暂时只能看到单条收盘情况。"

    first_close = items[0].close_price
    last_close = items[-1].close_price
    change = last_close - first_close
    if change > 0:
        return f"偏强，区间收盘上涨 {change:.2f}。"
    if change < 0:
        return f"偏弱，区间收盘下跌 {abs(change):.2f}。"
    return "基本持平。"


def format_news(items: list[NewsItem], limit: int = 10) -> str:
    if not items:
        return "当前没有拿到财经新闻。\n\n关键字段：无\n\n补充说明：可能是新闻源暂时为空。"

    visible = sorted(items, key=lambda item: item.published_at, reverse=True)[:limit]
    lines = "\n".join(
        f"- [{item.published_at}] {item.title} | 标签：{item.tag or '未标注'} | 摘要：{item.summary}"
        for item in visible
    )
    return (
        f"已整理出最近 {len(visible)} 条财经新闻，最新内容优先展示。\n\n"
        f"关键字段：\n{lines}\n\n"
        "补充说明：新闻结果已按时间倒序整理，默认最多展示前 10 条。"
    )


def format_news_digest(items: list[NewsItem], limit: int = 15) -> str:
    if not items:
        return "今日未整理到跨站财经新闻。\n\n关键字段：无\n\n补充说明：可能是新闻站点暂时不可用。"
    visible = items[:limit]
    lines = "\n".join(
        f"- {item.title} | 来源：{item.tag or '未标注'} | 时间：{item.published_at or '未提供'}"
        for item in visible
    )
    return (
        f"已整理今日跨站财经新闻，共输出 {len(visible)} 条重点内容。\n\n"
        f"关键字段：\n{lines}\n\n"
        "补充说明：结果已按来源聚合并做标题去重，适合作为开盘前或盘中资讯摘要。"
    )


def format_fx(result: FxResult) -> str:
    return (
        f"{result.pair} 当前汇率约为 {result.rate:.4f}。\n\n"
        f"关键字段：\n"
        f"币种对：{result.pair}\n"
        f"当前汇率：{result.rate:.4f}\n"
        f"时间：{result.quote_time}\n"
        f"基准币种：{result.base_currency}\n"
        f"目标币种：{result.target_currency}\n\n"
        f"补充说明：{result.note or '汇率结果仅做轻量展示，后续可补充涨跌和换算说明。'}"
    )


def format_list(title: str, items: list[ListItem], limit: int = 10) -> str:
    if not items:
        return f"{title} 当前没有可展示的数据。\n\n关键字段：无\n\n补充说明：可能是榜单结果为空。"

    visible = items[:limit]
    metric = visible[0].metric_label
    lines = "\n".join(
        f"- {index}. {item.name}（{item.code}） {metric}：{item.value:.2f} | {item.extra_text}"
        for index, item in enumerate(visible, start=1)
    )
    return (
        f"{title} 已整理完成，当前展示前 {len(visible)} 项。\n\n"
        f"关键字段：\n{lines}\n\n"
        "补充说明：后续可以在该格式上继续叠加行业、成交额、连板等补充信息。"
    )


def format_screened_stocks(items: list[ScreenedStock], limit: int = 10) -> str:
    if not items:
        return "当前没有筛选出满足条件的股票。\n\n关键字段：无\n\n补充说明：可以放宽涨幅、换手率或价格条件后重试。"
    visible = items[:limit]
    lines = "\n".join(
        f"- {item.name}（{item.code}） 现价：{item.latest_price:.2f} | 涨跌幅：{item.change_percent:+.2f}%"
        f" | 换手率：{(item.turnover_ratio if item.turnover_ratio is not None else 0.0):.2f}%"
        f" | 净流入：{(item.net_inflow if item.net_inflow is not None else 0.0):.0f}"
        f" | PE(TTM)：{(item.pe_ttm if item.pe_ttm is not None else 0.0):.2f}"
        f" | 市值：{(item.market_cap if item.market_cap is not None else 0.0):.0f}"
        f"{f' | 行业：{item.industry}' if item.industry else ''}"
        f"{f' | 综合分：{item.score:.2f}' if item.score is not None else ''}"
        f"{f' | 理由：{', '.join(item.reason_tags)}' if item.reason_tags else ''}"
        for item in visible
    )
    return (
        f"已从全市场筛出 {len(visible)} 只更匹配当前条件的股票。\n\n"
        f"关键字段：\n{lines}\n\n"
        "补充说明：当前筛选器优先支持 A 股全市场，适合做盘中初筛而不是直接代替交易决策。"
    )


def format_strategy_screen(title: str, indicators: list[str], items: list[ScreenedStock], limit: int = 10) -> str:
    indicator_line = "、".join(indicators)
    if not items:
        return f"{title} 当前没有筛出合适标的。\n\n关键字段：无\n\n补充说明：本工具当前使用 {indicator_line} 作为核心指标，可适当放宽阈值后重试。"
    body = format_screened_stocks(items, limit=limit)
    market_hint = items[0].source if items else "全市场"
    return body.replace("已从全市场筛出", f"{title} 已筛出").replace(
        "补充说明：",
        f"补充说明：本工具核心指标为 {indicator_line}；当前数据源为 {market_hint}。"
    )


def format_mid_long_term_screen(items: list[ScreenedStock], limit: int = 6) -> str:
    if not items:
        return (
            "中长线候选工具当前没有筛出合适标的。\n\n"
            "关键字段：无\n\n"
            "补充说明：该工具更强调估值、资金、规模与新闻主题共振，而不是单日涨幅。"
        )

    visible = items[:limit]
    lines = "\n".join(
        f"- {item.name}（{item.code}）"
        f" | 行业：{item.industry or '未标注'}"
        f" | 综合分：{(item.score or 0.0):.2f}"
        f" | PE(TTM)：{format_optional_number(item.pe_ttm, 2)}"
        f" | 市值：{format_billions(item.market_cap)}"
        f" | 净流入：{format_billions(item.net_inflow)}"
        f" | 换手率：{format_optional_number(item.turnover_ratio, 2, suffix='%')}"
        f" | 理由：{', '.join(item.reason_tags) or '估值与资金更匹配中长线'}"
        f"{f' | 新闻：{item.news_summary}' if item.news_summary else ''}"
        for item in visible
    )
    return (
        f"已筛出 {len(visible)} 只更适合中长线观察与分批跟踪的股票，排序更看重估值、资金、规模和新闻主题，而不是单日涨幅。\n\n"
        f"关键字段：\n{lines}\n\n"
        "补充说明：中长线工具优先保留估值不过热、主力资金为正、容量较大且与当日新闻主线存在共振的标的。"
    )


def format_optional_number(value: float | None, digits: int = 2, suffix: str = "") -> str:
    if value is None:
        return "暂无"
    return f"{value:.{digits}f}{suffix}"


def format_billions(value: float | None) -> str:
    if value is None:
        return "暂无"
    return f"{value / 100000000:.2f}亿"
