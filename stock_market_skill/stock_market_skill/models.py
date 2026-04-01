from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class IntentType(StrEnum):
    QUOTE = "quote"
    HK_QUOTE = "hk_quote"
    US_QUOTE = "us_quote"
    KLINE_DAY = "kline_day"
    KLINE_TIME = "kline_time"
    NEWS = "news"
    NEWS_DIGEST = "news_digest"
    FX = "fx"
    CHANGE_PERCENT_LIST = "change_percent_list"
    NET_INFLOW_LIST = "net_inflow_list"
    TURNOVER_RATIO_LIST = "turnover_ratio_list"
    SCREEN = "screen"
    LONG_TERM_SCREEN = "long_term_screen"
    MID_LONG_TERM_SCREEN = "mid_long_term_screen"
    SHORT_TERM_SCREEN = "short_term_screen"
    CLARIFICATION = "clarification"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class RouteResult:
    intent: IntentType
    tool_name: str
    params: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    reason: str = ""
    needs_clarification: bool = False
    candidates: list[str] = field(default_factory=list)


@dataclass(slots=True)
class QuoteResult:
    name: str
    code: str
    market: str
    latest_price: float
    change_amount: float
    change_percent: float
    update_time: str
    tool_used: str
    note: str = ""


@dataclass(slots=True)
class NewsItem:
    title: str
    summary: str
    published_at: str
    tag: str = ""


@dataclass(slots=True)
class KLineItem:
    timestamp: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float | None = None


@dataclass(slots=True)
class FxResult:
    pair: str
    rate: float
    quote_time: str
    base_currency: str = ""
    target_currency: str = ""
    note: str = ""


@dataclass(slots=True)
class ListItem:
    name: str
    code: str
    value: float
    metric_label: str
    extra_text: str = ""


@dataclass(slots=True)
class ScreenerCriteria:
    market: str = "CN"
    top_n: int = 10
    min_change_percent: float | None = None
    max_change_percent: float | None = None
    min_turnover_ratio: float | None = None
    max_price: float | None = None
    min_price: float | None = None
    min_net_inflow: float | None = None
    min_market_cap: float | None = None
    max_market_cap: float | None = None
    min_pe_ttm: float | None = None
    max_pe_ttm: float | None = None
    sort_by: str = "change_percent"
    strategy_name: str = ""
    min_news_score: float | None = None


@dataclass(slots=True)
class ScreenedStock:
    name: str
    code: str
    latest_price: float
    change_percent: float
    turnover_ratio: float | None = None
    net_inflow: float | None = None
    pe_ttm: float | None = None
    market_cap: float | None = None
    industry: str = ""
    score: float | None = None
    news_score: float | None = None
    reason_tags: list[str] = field(default_factory=list)
    news_summary: str = ""
    source: str = ""


@dataclass(slots=True)
class ClientResponse:
    tool_name: str
    payload: Any
    message: str = ""
    is_mock: bool = True
