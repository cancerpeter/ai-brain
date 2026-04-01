from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from typing import Any
from urllib import error, request

from .models import (
    ClientResponse,
    FxResult,
    KLineItem,
    ListItem,
    NewsItem,
    QuoteResult,
    RouteResult,
    ScreenedStock,
    ScreenerCriteria,
)
from .source_adapters import EastMoneyAdapter, SourceAdapterError, StockAnalysisAdapter, YahooFinanceAdapter


class PluginClientError(RuntimeError):
    """Raised when a real plugin call cannot be completed or normalized."""


@dataclass(slots=True)
class PluginSettings:
    use_mock: bool
    base_url: str
    timeout_seconds: float
    api_key: str
    headers: dict[str, str]
    tool_paths: dict[str, str]
    source_mode: str

    @classmethod
    def from_env(cls) -> PluginSettings:
        base_url = os.getenv("STOCK_SKILL_PLUGIN_BASE_URL", "").strip().rstrip("/")
        api_key = os.getenv("STOCK_SKILL_PLUGIN_API_KEY", "").strip()
        timeout_seconds = float(os.getenv("STOCK_SKILL_PLUGIN_TIMEOUT", "10"))
        use_mock = os.getenv("STOCK_SKILL_USE_MOCK", "0").strip().lower() not in {"0", "false", "no"}
        source_mode = os.getenv("STOCK_SKILL_SOURCE_MODE", "public").strip().lower() or "public"

        raw_headers = os.getenv("STOCK_SKILL_PLUGIN_HEADERS", "").strip()
        headers = parse_extra_headers(raw_headers)
        if api_key and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {api_key}"

        tool_paths = {
            "GetLiveNews": os.getenv("STOCK_SKILL_PATH_GETLIVENEWS", "/GetLiveNews"),
            "GetDailyNewsDigest": os.getenv("STOCK_SKILL_PATH_GETDAILYNEWSDIGEST", "/GetDailyNewsDigest"),
            "GetChangePercentList": os.getenv("STOCK_SKILL_PATH_GETCHANGEPERCENTLIST", "/GetChangePercentList"),
            "GetSinaStockData": os.getenv("STOCK_SKILL_PATH_GETSINASTOCKDATA", "/GetSinaStockData"),
            "GetKLineDayStockData": os.getenv("STOCK_SKILL_PATH_GETKLINEDAYSTOCKDATA", "/GetKLineDayStockData"),
            "GetExchangeRate": os.getenv("STOCK_SKILL_PATH_GETEXCHANGERATE", "/GetExchangeRate"),
            "GetQQStockData": os.getenv("STOCK_SKILL_PATH_GETQQSTOCKDATA", "/GetQQStockData"),
            "GetNetInflowRateList": os.getenv("STOCK_SKILL_PATH_GETNETINFLOWRATELIST", "/GetNetInflowRateList"),
            "GetHKStockData": os.getenv("STOCK_SKILL_PATH_GETHKSTOCKDATA", "/GetHKStockData"),
            "GetTurnoverRatioList": os.getenv("STOCK_SKILL_PATH_GETTURNOVERRATIOLIST", "/GetTurnoverRatioList"),
            "GetKLineTimeStockData": os.getenv("STOCK_SKILL_PATH_GETKLINETIMESTOCKDATA", "/GetKLineTimeStockData"),
            "GetUSStockData": os.getenv("STOCK_SKILL_PATH_GETUSSTOCKDATA", "/GetUSStockData"),
            "ScreenStocks": os.getenv("STOCK_SKILL_PATH_SCREENSTOCKS", "/ScreenStocks"),
            "ScreenLongTermStocks": os.getenv("STOCK_SKILL_PATH_SCREENLONGTERMSTOCKS", "/ScreenLongTermStocks"),
            "ScreenMidLongTermStocks": os.getenv("STOCK_SKILL_PATH_SCREENMIDLONGTERMSTOCKS", "/ScreenMidLongTermStocks"),
            "ScreenShortTermStocks": os.getenv("STOCK_SKILL_PATH_SCREENSHORTTERMSTOCKS", "/ScreenShortTermStocks"),
        }
        return cls(use_mock, base_url, timeout_seconds, api_key, headers, tool_paths, source_mode)


def parse_extra_headers(raw: str) -> dict[str, str]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PluginClientError("STOCK_SKILL_PLUGIN_HEADERS 不是合法 JSON 对象。") from exc
    if not isinstance(parsed, dict):
        raise PluginClientError("STOCK_SKILL_PLUGIN_HEADERS 必须是 JSON 对象。")
    return {str(key): str(value) for key, value in parsed.items()}


class PluginClient:
    """Unified adapter for private plugins and public market sources."""

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or PluginSettings.from_env()
        self.eastmoney = EastMoneyAdapter()
        self.yahoo_finance = YahooFinanceAdapter()
        self.stock_analysis = StockAnalysisAdapter()

    def dispatch(self, route: RouteResult) -> ClientResponse:
        tool_name = route.tool_name

        if tool_name == "GetLiveNews":
            payload = self.get_live_news(count=route.params.get("count", 10))
        elif tool_name == "GetDailyNewsDigest":
            payload = self.get_daily_news_digest(count=route.params.get("count", 15))
        elif tool_name == "GetExchangeRate":
            payload = self.get_exchange_rate(pair=route.params.get("pair", "CNY/USD"))
        elif tool_name == "GetKLineDayStockData":
            payload = self.get_kline_day(symbol=route.params["symbol"])
        elif tool_name == "GetKLineTimeStockData":
            payload = self.get_kline_time(symbol=route.params["symbol"])
        elif tool_name == "GetHKStockData":
            payload = self.get_hk_quote(symbol=route.params["symbol"])
        elif tool_name == "GetUSStockData":
            payload = self.get_us_quote(symbol=route.params["symbol"])
        elif tool_name == "GetChangePercentList":
            payload = self.get_change_percent_list(top_n=route.params.get("top_n", 10))
        elif tool_name == "GetNetInflowRateList":
            payload = self.get_net_inflow_rate_list(top_n=route.params.get("top_n", 10))
        elif tool_name == "GetTurnoverRatioList":
            payload = self.get_turnover_ratio_list(top_n=route.params.get("top_n", 10))
        elif tool_name == "ScreenStocks":
            payload = self.screen_stocks(ScreenerCriteria(**route.params))
        elif tool_name == "ScreenLongTermStocks":
            payload = self.screen_long_term_stocks(ScreenerCriteria(**route.params))
        elif tool_name == "ScreenMidLongTermStocks":
            payload = self.screen_mid_long_term_stocks(ScreenerCriteria(**route.params))
        elif tool_name == "ScreenShortTermStocks":
            payload = self.screen_short_term_stocks(ScreenerCriteria(**route.params))
        elif tool_name in {"GetSinaStockData", "GetQQStockData"}:
            payload = self.get_stock_quote(symbol=route.params["symbol"], preferred_tool=tool_name)
        else:
            raise NotImplementedError(f"Unsupported tool: {tool_name}")

        return ClientResponse(tool_name=tool_name, payload=payload, message=self._response_message(), is_mock=self.settings.use_mock)

    def get_live_news(self, count: int = 10) -> list[NewsItem]:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_live_news(count=count)
            except SourceAdapterError as exc:
                if not self.settings.use_mock:
                    raise PluginClientError(f"EastMoney 新闻源调用失败: {exc}") from exc

        if self.settings.use_mock:
            return [
                NewsItem("央行开展公开市场操作", "公开市场操作保持流动性合理充裕。", "2026-03-31 09:30:00", "宏观"),
                NewsItem("新能源板块盘中活跃", "新能源产业链多只个股走强。", "2026-03-31 09:18:00", "A股"),
            ][:count]

        raw = self._call_tool("GetLiveNews", {"count": count})
        return [self._normalize_news_item(item) for item in ensure_list_payload(raw, "GetLiveNews")]

    def get_daily_news_digest(self, count: int = 15) -> list[NewsItem]:
        source_buckets: list[list[NewsItem]] = []
        errors: list[str] = []

        for label, loader in (
            ("EastMoney", lambda: self.eastmoney.get_live_news(count=count)),
            ("Yahoo Finance", lambda: self.yahoo_finance.get_news(count=count)),
            ("StockAnalysis", lambda: self.stock_analysis.get_news(count=count)),
        ):
            try:
                source_buckets.append(loader())
            except SourceAdapterError as exc:
                errors.append(f"{label}: {exc}")

        items = interleave_news(source_buckets, count=count)
        if items:
            return deduplicate_news(items)[:count]

        if self.settings.use_mock:
            return [NewsItem("示例新闻", "公共源暂时不可用，当前为演示数据。", "2026-03-31 09:00:00", "mock")]

        raise PluginClientError("新闻聚合失败；".join(errors) or "所有新闻源均不可用。")

    def get_stock_quote(self, symbol: str, preferred_tool: str = "GetSinaStockData") -> QuoteResult:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_quote(symbol=symbol)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"EastMoney A 股行情调用失败: {exc}") from exc

        if self.settings.use_mock and not self.settings.base_url:
            return QuoteResult(symbol, symbol, "CN", 0.0, 0.0, 0.0, "", preferred_tool, "mock disabled sources unavailable")

        return self._normalize_quote(self._call_tool(preferred_tool, {"symbol": symbol}), fallback_symbol=symbol, market="CN", tool_used=preferred_tool)

    def get_hk_quote(self, symbol: str) -> QuoteResult:
        if self._prefer_public_sources():
            try:
                return self.yahoo_finance.get_quote(symbol=symbol)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"Yahoo Finance 港股行情调用失败: {exc}") from exc

        if self.settings.use_mock and not self.settings.base_url:
            return QuoteResult(symbol, symbol, "HK", 0.0, 0.0, 0.0, "", "GetHKStockData", "mock disabled sources unavailable")

        return self._normalize_quote(self._call_tool("GetHKStockData", {"symbol": symbol}), fallback_symbol=symbol, market="HK", tool_used="GetHKStockData")

    def get_us_quote(self, symbol: str) -> QuoteResult:
        if self._prefer_public_sources():
            try:
                return self.stock_analysis.get_quote(symbol=symbol)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"StockAnalysis 美股行情调用失败: {exc}") from exc

        if self.settings.use_mock and not self.settings.base_url:
            return QuoteResult(symbol, symbol, "US", 0.0, 0.0, 0.0, "", "GetUSStockData", "mock disabled sources unavailable")

        return self._normalize_quote(self._call_tool("GetUSStockData", {"symbol": symbol}), fallback_symbol=symbol, market="US", tool_used="GetUSStockData")

    def get_kline_day(self, symbol: str) -> list[KLineItem]:
        if self._prefer_public_sources():
            try:
                if symbol.upper().endswith(".HK"):
                    return self.yahoo_finance.get_kline_day(symbol=symbol)
                return self.eastmoney.get_kline_day(symbol=symbol)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"公共日 K 数据源调用失败: {exc}") from exc

        raw = self._call_tool("GetKLineDayStockData", {"symbol": symbol})
        return [self._normalize_kline_item(item) for item in ensure_list_payload(raw, "GetKLineDayStockData")]

    def get_kline_time(self, symbol: str) -> list[KLineItem]:
        if self._prefer_public_sources():
            try:
                if symbol.upper().endswith(".HK"):
                    return self.yahoo_finance.get_kline_time(symbol=symbol)
                return self.eastmoney.get_kline_time(symbol=symbol)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"公共分时数据源调用失败: {exc}") from exc

        raw = self._call_tool("GetKLineTimeStockData", {"symbol": symbol})
        return [self._normalize_kline_item(item) for item in ensure_list_payload(raw, "GetKLineTimeStockData")]

    def get_exchange_rate(self, pair: str) -> FxResult:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_exchange_rate(pair=pair)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"公共汇率源调用失败: {exc}") from exc

        if self.settings.use_mock and not self.settings.base_url:
            return FxResult(pair, 0.0, "", pair.split("/")[0], pair.split("/")[1], "mock disabled sources unavailable")

        return self._normalize_fx(self._call_tool("GetExchangeRate", {"pair": pair}), pair)

    def get_change_percent_list(self, top_n: int = 10) -> list[ListItem]:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_change_percent_list(top_n=top_n)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"EastMoney 涨跌幅榜调用失败: {exc}") from exc
        raw = self._call_tool("GetChangePercentList", {"top_n": top_n}) if self.settings.base_url else []
        return [self._normalize_list_item(item, "涨跌幅") for item in ensure_list_payload(raw, "GetChangePercentList")] if raw else []

    def get_net_inflow_rate_list(self, top_n: int = 10) -> list[ListItem]:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_net_inflow_rate_list(top_n=top_n)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"EastMoney 净流入榜调用失败: {exc}") from exc
        raw = self._call_tool("GetNetInflowRateList", {"top_n": top_n}) if self.settings.base_url else []
        return [self._normalize_list_item(item, "净流入率") for item in ensure_list_payload(raw, "GetNetInflowRateList")] if raw else []

    def get_turnover_ratio_list(self, top_n: int = 10) -> list[ListItem]:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.get_turnover_ratio_list(top_n=top_n)
            except SourceAdapterError as exc:
                if not self.settings.use_mock and not self.settings.base_url:
                    raise PluginClientError(f"EastMoney 换手率榜调用失败: {exc}") from exc
        raw = self._call_tool("GetTurnoverRatioList", {"top_n": top_n}) if self.settings.base_url else []
        return [self._normalize_list_item(item, "换手率") for item in ensure_list_payload(raw, "GetTurnoverRatioList")] if raw else []

    def screen_stocks(self, criteria: ScreenerCriteria) -> list[ScreenedStock]:
        if self._prefer_public_sources():
            try:
                return self.eastmoney.screen_stocks(criteria)
            except SourceAdapterError as exc:
                raise PluginClientError(f"{criteria.market} 全市场筛选失败: {exc}") from exc
        raw = self._call_tool("ScreenStocks", asdict(criteria))
        return [self._normalize_screened_stock(item) for item in ensure_list_payload(raw, "ScreenStocks")]

    def screen_long_term_stocks(self, criteria: ScreenerCriteria) -> list[ScreenedStock]:
        criteria.strategy_name = criteria.strategy_name or "long_term"
        if self._prefer_public_sources():
            try:
                return self.eastmoney.screen_stocks(criteria)
            except SourceAdapterError as exc:
                raise PluginClientError(f"{criteria.market} 长线筛选失败: {exc}") from exc
        raw = self._call_tool("ScreenLongTermStocks", asdict(criteria))
        return [self._normalize_screened_stock(item) for item in ensure_list_payload(raw, "ScreenLongTermStocks")]

    def screen_mid_long_term_stocks(self, criteria: ScreenerCriteria) -> list[ScreenedStock]:
        criteria.strategy_name = criteria.strategy_name or "mid_long_term"
        if self._prefer_public_sources():
            try:
                return self.eastmoney.screen_stocks(criteria)
            except SourceAdapterError as exc:
                raise PluginClientError(f"{criteria.market} 中长线筛选失败: {exc}") from exc
        raw = self._call_tool("ScreenMidLongTermStocks", asdict(criteria))
        return [self._normalize_screened_stock(item) for item in ensure_list_payload(raw, "ScreenMidLongTermStocks")]

    def screen_short_term_stocks(self, criteria: ScreenerCriteria) -> list[ScreenedStock]:
        criteria.strategy_name = criteria.strategy_name or "short_term"
        if self._prefer_public_sources():
            try:
                return self.eastmoney.screen_stocks(criteria)
            except SourceAdapterError as exc:
                raise PluginClientError(f"{criteria.market} 短线筛选失败: {exc}") from exc
        raw = self._call_tool("ScreenShortTermStocks", asdict(criteria))
        return [self._normalize_screened_stock(item) for item in ensure_list_payload(raw, "ScreenShortTermStocks")]

    def _prefer_public_sources(self) -> bool:
        return self.settings.source_mode in {"auto", "public"} and not self.settings.base_url

    def _response_message(self) -> str:
        if self._prefer_public_sources():
            return "public market source response"
        if self.settings.use_mock and not self.settings.base_url:
            return "mock response"
        return "real plugin response"

    def _call_tool(self, tool_name: str, params: dict[str, Any]) -> Any:
        if not self.settings.base_url:
            raise PluginClientError("未配置真实插件地址，且当前请求未命中公共源。")
        path = self.settings.tool_paths.get(tool_name)
        if not path:
            raise PluginClientError(f"未找到工具 {tool_name} 的 path 配置。")
        url = f"{self.settings.base_url}{path}"
        body = json.dumps(params).encode("utf-8")
        headers = {"Content-Type": "application/json", **self.settings.headers}
        req = request.Request(url=url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.settings.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise PluginClientError(f"{tool_name} HTTP {exc.code}: {detail or exc.reason}") from exc
        except error.URLError as exc:
            raise PluginClientError(f"{tool_name} 请求失败: {exc.reason}") from exc
        parsed = json.loads(payload)
        if isinstance(parsed, dict) and "data" in parsed:
            return parsed["data"]
        return parsed

    def _normalize_quote(self, raw: Any, fallback_symbol: str, market: str, tool_used: str) -> QuoteResult:
        item = ensure_mapping_payload(raw, tool_used)
        return QuoteResult(
            name=str(pick_first(item, "name", "stock_name", "stockName", default=fallback_symbol)),
            code=str(pick_first(item, "code", "symbol", "stock_code", "stockCode", default=fallback_symbol)),
            market=str(pick_first(item, "market", default=market)),
            latest_price=to_float(pick_first(item, "latest_price", "latestPrice", "price", "current_price", "now")),
            change_amount=to_float(pick_first(item, "change_amount", "changeAmount", "change", "updown")),
            change_percent=to_float(pick_first(item, "change_percent", "changePercent", "percent", "pct_chg")),
            update_time=str(pick_first(item, "update_time", "updateTime", "time", "timestamp", default="")),
            tool_used=tool_used,
            note="real plugin response normalized",
        )

    def _normalize_news_item(self, raw: Any) -> NewsItem:
        item = ensure_mapping_payload(raw, "GetLiveNews")
        return NewsItem(
            title=str(pick_first(item, "title", "headline", default="未命名新闻")),
            summary=str(pick_first(item, "summary", "content", "brief", default="")),
            published_at=str(pick_first(item, "published_at", "publishedAt", "time", "datetime", default="")),
            tag=str(pick_first(item, "tag", "category", "label", default="")),
        )

    def _normalize_kline_item(self, raw: Any) -> KLineItem:
        item = ensure_mapping_payload(raw, "KLine")
        return KLineItem(
            timestamp=str(pick_first(item, "timestamp", "time", "date", "datetime", default="")),
            open_price=to_float(pick_first(item, "open_price", "open", default=0)),
            high_price=to_float(pick_first(item, "high_price", "high", default=0)),
            low_price=to_float(pick_first(item, "low_price", "low", default=0)),
            close_price=to_float(pick_first(item, "close_price", "close", "price", default=0)),
            volume=to_optional_float(pick_first(item, "volume", "vol", default=None)),
        )

    def _normalize_fx(self, raw: Any, pair: str) -> FxResult:
        item = ensure_mapping_payload(raw, "GetExchangeRate")
        base_currency, target_currency = split_pair(pair)
        return FxResult(
            pair=str(pick_first(item, "pair", "symbol", default=pair)),
            rate=to_float(pick_first(item, "rate", "exchange_rate", "price", default=0)),
            quote_time=str(pick_first(item, "quote_time", "quoteTime", "time", "timestamp", default="")),
            base_currency=str(pick_first(item, "base_currency", "baseCurrency", default=base_currency)),
            target_currency=str(pick_first(item, "target_currency", "targetCurrency", default=target_currency)),
            note="real plugin response normalized",
        )

    def _normalize_list_item(self, raw: Any, metric_label: str) -> ListItem:
        item = ensure_mapping_payload(raw, metric_label)
        return ListItem(
            name=str(pick_first(item, "name", "stock_name", "stockName", default="未知标的")),
            code=str(pick_first(item, "code", "symbol", "stock_code", "stockCode", default="")),
            value=to_float(pick_first(item, "value", "metric", "ratio", "percent", "change_percent", default=0)),
            metric_label=str(pick_first(item, "metric_label", "metricLabel", default=metric_label)),
            extra_text=str(pick_first(item, "extra_text", "extraText", "note", "comment", default="")),
        )

    def _normalize_screened_stock(self, raw: Any) -> ScreenedStock:
        item = ensure_mapping_payload(raw, "ScreenStocks")
        return ScreenedStock(
            name=str(pick_first(item, "name", "stock_name", default="未知标的")),
            code=str(pick_first(item, "code", "symbol", default="")),
            latest_price=to_float(pick_first(item, "latest_price", "price", default=0)),
            change_percent=to_float(pick_first(item, "change_percent", "percent", default=0)),
            turnover_ratio=to_optional_float(pick_first(item, "turnover_ratio", "turnover", default=None)),
            net_inflow=to_optional_float(pick_first(item, "net_inflow", "main_net_inflow", default=None)),
            pe_ttm=to_optional_float(pick_first(item, "pe_ttm", "pe", default=None)),
            market_cap=to_optional_float(pick_first(item, "market_cap", "marketCap", default=None)),
            industry=str(pick_first(item, "industry", default="")),
            score=to_optional_float(pick_first(item, "score", default=None)),
            news_score=to_optional_float(pick_first(item, "news_score", "newsScore", default=None)),
            reason_tags=parse_reason_tags(pick_first(item, "reason_tags", "reasonTags", default=[])),
            news_summary=str(pick_first(item, "news_summary", "newsSummary", default="")),
            source=str(pick_first(item, "source", default="plugin")),
        )

    @staticmethod
    def to_dict(payload: object) -> object:
        if isinstance(payload, list):
            return [asdict(item) for item in payload]
        return asdict(payload)


def deduplicate_news(items: list[NewsItem]) -> list[NewsItem]:
    seen: set[str] = set()
    result: list[NewsItem] = []
    for item in items:
        key = item.title.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def interleave_news(buckets: list[list[NewsItem]], count: int) -> list[NewsItem]:
    result: list[NewsItem] = []
    index = 0
    while len(result) < count:
        progressed = False
        for bucket in buckets:
            if index < len(bucket):
                result.append(bucket[index])
                progressed = True
                if len(result) >= count:
                    break
        if not progressed:
            break
        index += 1
    return result


def ensure_mapping_payload(raw: Any, tool_name: str) -> dict[str, Any]:
    if isinstance(raw, list):
        if not raw:
            raise PluginClientError(f"{tool_name} 返回空列表。")
        raw = raw[0]
    if not isinstance(raw, dict):
        raise PluginClientError(f"{tool_name} 返回格式无法解析，预期对象，实际为 {type(raw).__name__}。")
    return raw


def ensure_list_payload(raw: Any, tool_name: str) -> list[Any]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("items", "list", "rows", "result"):
            value = raw.get(key)
            if isinstance(value, list):
                return value
    raise PluginClientError(f"{tool_name} 返回格式无法解析，预期列表。")


def pick_first(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return mapping[key]
    return default


def to_float(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def to_optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def split_pair(pair: str) -> tuple[str, str]:
    if "/" in pair:
        return tuple(pair.split("/", 1))
    return "", ""


def parse_reason_tags(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return []
