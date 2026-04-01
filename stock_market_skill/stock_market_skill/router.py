from __future__ import annotations

import re

from .models import IntentType, RouteResult

NEWS_KEYWORDS = ("新闻", "快讯", "财经消息", "最新消息")
NEWS_DIGEST_KEYWORDS = ("新闻汇总", "新闻整理", "汇总新闻", "整理新闻", "今日财经新闻汇总", "各网站新闻")
FX_KEYWORDS = ("汇率", "人民币兑", "美元兑", "外汇")
KLINE_TIME_KEYWORDS = ("分时", "分钟线", "分钟k", "分钟K")
KLINE_DAY_KEYWORDS = ("日k", "日K", "日线", "k线", "K线")
CHANGE_PERCENT_KEYWORDS = ("涨跌幅榜", "涨幅榜", "跌幅榜")
NET_INFLOW_KEYWORDS = ("净流入榜", "资金净流入", "主力净流入")
TURNOVER_RATIO_KEYWORDS = ("换手率榜", "换手率")
HK_KEYWORDS = ("港股", ".hk", ".HK", "hk", "HK", "腾讯", "小米", "阿里港股")
US_KEYWORDS = ("美股", "纳斯达克", "纽交所", "NASDAQ", "NYSE")
QUOTE_HINTS = ("行情", "股价", "价格", "现在多少钱", "实时价", "报价")
SCREEN_KEYWORDS = ("筛选", "选股", "找出", "条件股", "符合条件")
MID_LONG_TERM_KEYWORDS = ("中长线", "中长期", "稳健配置", "中线偏长", "中长期投资")
LONG_TERM_KEYWORDS = ("长线", "长期投资", "价值投资")
SHORT_TERM_KEYWORDS = ("短线", "打板", "强势股", "超短", "短期交易")
STOP_WORDS = (
    "查一下",
    "查",
    "看看",
    "看一下",
    "给我",
    "帮我",
    "现在",
    "今天",
    "实时",
    "走势",
    "最新",
    "一下",
    "前",
)

KNOWN_STOCK_ALIASES = {
    "贵州茅台": "600519",
    "宁德时代": "300750",
    "比亚迪": "002594",
    "腾讯": "0700.HK",
    "腾讯控股": "0700.HK",
    "小米": "1810.HK",
    "苹果": "AAPL",
    "英伟达": "NVDA",
    "特斯拉": "TSLA",
}

FX_PAIRS = {
    "人民币兑美元": "CNY/USD",
    "美元兑人民币": "USD/CNY",
    "人民币兑港币": "CNY/HKD",
    "人民币兑日元": "CNY/JPY",
    "人民币兑欧元": "CNY/EUR",
}


def route_query(query: str) -> RouteResult:
    text = normalize_text(query)

    if contains_any(text, MID_LONG_TERM_KEYWORDS) and ("选股" in text or "挑选" in text or "推荐" in text or "筛选" in text):
        criteria = build_mid_long_term_criteria(text)
        return RouteResult(
            intent=IntentType.MID_LONG_TERM_SCREEN,
            tool_name="ScreenMidLongTermStocks",
            params=criteria,
            confidence=0.98,
            reason="命中中长线选股关键词",
        )

    if contains_any(text, LONG_TERM_KEYWORDS) and ("选股" in text or "挑选" in text or "推荐" in text or "筛选" in text):
        criteria = build_long_term_criteria(text)
        return RouteResult(
            intent=IntentType.LONG_TERM_SCREEN,
            tool_name="ScreenLongTermStocks",
            params=criteria,
            confidence=0.97,
            reason="命中长线选股关键词",
        )

    if contains_any(text, SHORT_TERM_KEYWORDS) and ("选股" in text or "挑选" in text or "推荐" in text or "筛选" in text):
        criteria = build_short_term_criteria(text)
        return RouteResult(
            intent=IntentType.SHORT_TERM_SCREEN,
            tool_name="ScreenShortTermStocks",
            params=criteria,
            confidence=0.97,
            reason="命中短线选股关键词",
        )

    if contains_any(text, NEWS_DIGEST_KEYWORDS):
        count = extract_count(text, default=15)
        return RouteResult(
            intent=IntentType.NEWS_DIGEST,
            tool_name="GetDailyNewsDigest",
            params={"count": count},
            confidence=0.99,
            reason="命中新闻汇总关键词",
        )

    if contains_any(text, NEWS_KEYWORDS):
        count = extract_count(text, default=10)
        return RouteResult(
            intent=IntentType.NEWS,
            tool_name="GetLiveNews",
            params={"count": count},
            confidence=0.98,
            reason="命中新闻关键词",
        )

    if contains_any(text, FX_KEYWORDS):
        pair = extract_fx_pair(text)
        return RouteResult(
            intent=IntentType.FX,
            tool_name="GetExchangeRate",
            params={"pair": pair},
            confidence=0.97,
            reason="命中汇率关键词",
        )

    if contains_any(text, CHANGE_PERCENT_KEYWORDS):
        top_n = extract_count(text, default=10)
        return RouteResult(
            intent=IntentType.CHANGE_PERCENT_LIST,
            tool_name="GetChangePercentList",
            params={"top_n": top_n},
            confidence=0.96,
            reason="命中涨跌幅榜关键词",
        )

    if contains_any(text, NET_INFLOW_KEYWORDS):
        top_n = extract_count(text, default=10)
        return RouteResult(
            intent=IntentType.NET_INFLOW_LIST,
            tool_name="GetNetInflowRateList",
            params={"top_n": top_n},
            confidence=0.96,
            reason="命中净流入榜关键词",
        )

    if contains_any(text, TURNOVER_RATIO_KEYWORDS) and "股票" not in text:
        top_n = extract_count(text, default=10)
        return RouteResult(
            intent=IntentType.TURNOVER_RATIO_LIST,
            tool_name="GetTurnoverRatioList",
            params={"top_n": top_n},
            confidence=0.95,
            reason="命中换手率榜关键词",
        )

    if contains_any(text, SCREEN_KEYWORDS):
        criteria = extract_screen_criteria(text)
        return RouteResult(
            intent=IntentType.SCREEN,
            tool_name="ScreenStocks",
            params=criteria,
            confidence=0.94,
            reason="命中筛选 / 选股关键词",
        )

    security = extract_security(text)

    if contains_any(text, KLINE_TIME_KEYWORDS):
        return build_security_route(
            text=text,
            security=security,
            intent=IntentType.KLINE_TIME,
            tool_name="GetKLineTimeStockData",
            reason="命中分时 / 分钟线关键词",
        )

    if contains_any(text, KLINE_DAY_KEYWORDS):
        return build_security_route(
            text=text,
            security=security,
            intent=IntentType.KLINE_DAY,
            tool_name="GetKLineDayStockData",
            reason="命中日K / 日线关键词",
        )

    if contains_any(text, HK_KEYWORDS):
        return build_security_route(
            text=text,
            security=security,
            intent=IntentType.HK_QUOTE,
            tool_name="GetHKStockData",
            reason="命中港股特征，优先走港股行情工具",
            market="HK",
        )

    if contains_any(text, US_KEYWORDS) or looks_like_us_ticker(text):
        return build_security_route(
            text=text,
            security=security or extract_us_ticker(text),
            intent=IntentType.US_QUOTE,
            tool_name="GetUSStockData",
            reason="命中美股特征，走美股行情源",
            market="US",
        )

    if security or contains_any(text, QUOTE_HINTS) or "股票" in text:
        return build_security_route(
            text=text,
            security=security,
            intent=IntentType.QUOTE,
            tool_name="GetSinaStockData",
            reason="未命中更强规则，默认走 A 股实时行情",
            market="CN",
        )

    return RouteResult(
        intent=IntentType.UNKNOWN,
        tool_name="",
        confidence=0.2,
        reason="未识别到明确意图",
        needs_clarification=True,
        candidates=[
            "查贵州茅台现在多少钱",
            "查腾讯港股实时价",
            "给我最新财经新闻，5条",
            "人民币兑美元汇率",
        ],
    )


def build_security_route(
    text: str,
    security: str | None,
    intent: IntentType,
    tool_name: str,
    reason: str,
    market: str | None = None,
) -> RouteResult:
    if not security:
        return RouteResult(
            intent=IntentType.CLARIFICATION,
            tool_name=tool_name,
            confidence=0.55,
            reason=f"{reason}，但证券标的不明确",
            needs_clarification=True,
            candidates=[
                "请补充股票名称，例如：贵州茅台、宁德时代",
                "请补充股票代码，例如：600519、0700.HK",
            ],
        )

    params = {"symbol": security}
    if market:
        params["market"] = market

    return RouteResult(
        intent=intent,
        tool_name=tool_name,
        params=params,
        confidence=0.9,
        reason=reason,
    )


def normalize_text(query: str) -> str:
    return re.sub(r"\s+", "", query).strip()


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def extract_count(text: str, default: int) -> int:
    matched = re.search(r"(\d{1,2})条|前(\d{1,2})|(\d{1,2})个", text)
    if not matched:
        return default

    numbers = [group for group in matched.groups() if group]
    if not numbers:
        return default

    return max(1, min(int(numbers[0]), 50))


def extract_fx_pair(text: str) -> str:
    for phrase, pair in FX_PAIRS.items():
        if phrase in text:
            return pair
    return "CNY/USD"


def extract_screen_criteria(text: str) -> dict[str, float | int | str]:
    criteria: dict[str, float | int | str] = {
        "market": "CN",
        "top_n": extract_count(text, default=10),
        "sort_by": "change_percent",
    }

    if "港股" in text:
        criteria["market"] = "HK"
    elif "美股" in text:
        criteria["market"] = "US"

    min_change = extract_threshold(text, ("涨幅大于", "涨跌幅大于", "涨幅超过", "涨幅>", "涨跌幅>"))
    if min_change is not None:
        criteria["min_change_percent"] = min_change

    min_turnover = extract_threshold(text, ("换手率大于", "换手率超过", "换手率>", "高换手"))
    if min_turnover is not None:
        criteria["min_turnover_ratio"] = min_turnover

    max_price = extract_threshold(text, ("价格低于", "股价低于", "价格小于", "股价<", "价格<"))
    if max_price is not None:
        criteria["max_price"] = max_price

    min_price = extract_threshold(text, ("价格高于", "股价高于", "价格>", "股价>"))
    if min_price is not None:
        criteria["min_price"] = min_price

    net_inflow = extract_threshold(text, ("净流入大于", "主力净流入大于", "净流入超过", "净流入>"))
    if net_inflow is not None:
        if "亿" in text:
            net_inflow *= 100000000
        criteria["min_net_inflow"] = net_inflow

    if "换手率排序" in text or "按换手率" in text:
        criteria["sort_by"] = "turnover_ratio"
    elif "净流入排序" in text or "按净流入" in text:
        criteria["sort_by"] = "net_inflow"

    return criteria


def build_long_term_criteria(text: str) -> dict[str, float | int | str]:
    criteria = extract_screen_criteria(text)
    market = str(criteria.get("market", "CN"))
    if market == "CN":
        criteria.update(
            {
                "strategy_name": "long_term",
                "sort_by": "net_inflow",
                "min_market_cap": 5_000_000_000,
                "max_pe_ttm": 60.0,
                "min_turnover_ratio": 1.0,
                "min_net_inflow": 0.0,
            }
        )
    else:
        criteria.update(
            {
                "strategy_name": "long_term",
                "sort_by": "market_cap",
                "min_market_cap": 10_000_000_000,
                "max_pe_ttm": 80.0,
            }
        )
    criteria.setdefault("top_n", extract_count(text, default=10))
    return criteria


def build_mid_long_term_criteria(text: str) -> dict[str, float | int | str]:
    criteria = extract_screen_criteria(text)
    market = str(criteria.get("market", "CN"))
    if market == "CN":
        criteria.update(
            {
                "strategy_name": "mid_long_term",
                "sort_by": "score",
                "min_market_cap": 8_000_000_000,
                "max_pe_ttm": 45.0,
                "min_turnover_ratio": float(criteria.get("min_turnover_ratio", 0.5)),
                "min_net_inflow": float(criteria.get("min_net_inflow", 50_000_000.0)),
                "min_news_score": 0.5,
                "max_change_percent": float(criteria.get("max_change_percent", 9.5)),
            }
        )
    else:
        criteria.update(
            {
                "strategy_name": "mid_long_term",
                "sort_by": "score",
                "min_market_cap": 10_000_000_000,
                "max_pe_ttm": 50.0,
            }
        )
    criteria.setdefault("top_n", extract_count(text, default=6))
    return criteria


def build_short_term_criteria(text: str) -> dict[str, float | int | str]:
    criteria = extract_screen_criteria(text)
    market = str(criteria.get("market", "CN"))
    if market == "CN":
        criteria.update(
            {
                "strategy_name": "short_term",
                "sort_by": "change_percent",
                "min_change_percent": float(criteria.get("min_change_percent", 3.0)),
                "min_turnover_ratio": float(criteria.get("min_turnover_ratio", 5.0)),
                "min_net_inflow": float(criteria.get("min_net_inflow", 0.0)),
            }
        )
    else:
        criteria.update(
            {
                "strategy_name": "short_term",
                "sort_by": "change_percent",
                "min_change_percent": float(criteria.get("min_change_percent", 0.05)),
            }
        )
    criteria.setdefault("top_n", extract_count(text, default=10))
    return criteria


def extract_threshold(text: str, prefixes: tuple[str, ...]) -> float | None:
    for prefix in prefixes:
        matched = re.search(re.escape(prefix) + r"(\d+(?:\.\d+)?)", text)
        if matched:
            return float(matched.group(1))
    return None


def extract_security(text: str) -> str | None:
    for alias, symbol in KNOWN_STOCK_ALIASES.items():
        if alias in text:
            return symbol

    matched = re.search(r"\b\d{6}\b", text)
    if matched:
        return matched.group(0)

    matched = re.search(r"\b\d{4,5}\.HK\b", text, flags=re.IGNORECASE)
    if matched:
        return matched.group(0).upper()

    us_ticker = extract_us_ticker(text)
    if us_ticker:
        return us_ticker

    cleaned = text
    for token in STOP_WORDS:
        cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace("港股", "").replace("美股", "").replace("日K", "").replace("日k", "")
    cleaned = cleaned.replace("日线", "").replace("K线", "").replace("k线", "")
    cleaned = cleaned.replace("分时", "").replace("分钟线", "")
    cleaned = cleaned.replace("行情", "").replace("股价", "").replace("价格", "")
    cleaned = cleaned.replace("实时价", "").replace("报价", "").replace("股票", "")

    if 1 < len(cleaned) <= 8 and re.fullmatch(r"[\u4e00-\u9fffA-Za-z]+", cleaned):
        return cleaned

    return None


def looks_like_us_ticker(text: str) -> bool:
    return extract_us_ticker(text) is not None


def extract_us_ticker(text: str) -> str | None:
    matched = re.search(r"[A-Z]{2,5}", text)
    if matched:
        return matched.group(0)
    return None
