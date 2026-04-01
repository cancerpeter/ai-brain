from __future__ import annotations

import sys

from .formatter import (
    format_clarification,
    format_fx,
    format_kline,
    format_list,
    format_mid_long_term_screen,
    format_news,
    format_news_digest,
    format_quote,
    format_screened_stocks,
    format_strategy_screen,
)
from .models import IntentType
from .plugin_client import PluginClient, PluginClientError
from .router import route_query


def run(query: str) -> str:
    route = route_query(query)

    if route.needs_clarification:
        return format_clarification(route)

    client = PluginClient()
    try:
        response = client.dispatch(route)
    except PluginClientError as exc:
        return f"当前无法获取真实行情结果。\n\n关键字段：{route.tool_name}\n\n补充说明：{exc}"
    payload = response.payload

    if route.intent in {IntentType.QUOTE, IntentType.HK_QUOTE, IntentType.US_QUOTE}:
        return format_quote(payload)
    if route.intent in {IntentType.KLINE_DAY, IntentType.KLINE_TIME}:
        return format_kline(route.params["symbol"], payload)
    if route.intent is IntentType.NEWS:
        return format_news(payload, limit=route.params.get("count", 10))
    if route.intent is IntentType.NEWS_DIGEST:
        return format_news_digest(payload, limit=route.params.get("count", 15))
    if route.intent is IntentType.FX:
        return format_fx(payload)
    if route.intent is IntentType.CHANGE_PERCENT_LIST:
        return format_list("涨跌幅榜", payload, limit=route.params.get("top_n", 10))
    if route.intent is IntentType.NET_INFLOW_LIST:
        return format_list("净流入榜", payload, limit=route.params.get("top_n", 10))
    if route.intent is IntentType.TURNOVER_RATIO_LIST:
        return format_list("换手率榜", payload, limit=route.params.get("top_n", 10))
    if route.intent is IntentType.SCREEN:
        return format_screened_stocks(payload, limit=route.params.get("top_n", 10))
    if route.intent is IntentType.LONG_TERM_SCREEN:
        return format_strategy_screen(
            "长线候选工具",
            ["市值下限", "PE(TTM) 上限", "适中换手率", "主力净流入"],
            payload,
            limit=route.params.get("top_n", 10),
        )
    if route.intent is IntentType.MID_LONG_TERM_SCREEN:
        return format_mid_long_term_screen(payload, limit=route.params.get("top_n", 6))
    if route.intent is IntentType.SHORT_TERM_SCREEN:
        return format_strategy_screen(
            "短线候选工具",
            ["涨跌幅强度", "高换手率", "主力净流入", "价格动量"],
            payload,
            limit=route.params.get("top_n", 10),
        )

    return "暂未识别该请求，请换一种表达方式重试。"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print("用法：python3 -m stock_market_skill.main \"查腾讯港股实时价\"")
        return 1

    query = " ".join(args)
    print(run(query))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
