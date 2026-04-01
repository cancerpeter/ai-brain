from __future__ import annotations

import json
import re
from html import unescape
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib import error, parse, request
from xml.etree import ElementTree

from .models import FxResult, KLineItem, ListItem, NewsItem, QuoteResult, ScreenedStock, ScreenerCriteria


class SourceAdapterError(RuntimeError):
    """Raised when a public market data source cannot be fetched or parsed."""


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)


@dataclass(slots=True)
class HttpClient:
    timeout_seconds: float = 10.0

    def get_json(self, url: str, headers: dict[str, str] | None = None) -> Any:
        text = self.get_text(url, headers=headers)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise SourceAdapterError(f"JSON 解析失败: {url}") from exc

    def get_text(self, url: str, headers: dict[str, str] | None = None) -> str:
        merged_headers = {"User-Agent": USER_AGENT, **(headers or {})}
        req = request.Request(url, headers=merged_headers, method="GET")
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                return response.read().decode("utf-8", errors="ignore")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise SourceAdapterError(f"HTTP {exc.code} for {url}: {detail[:200]}") from exc
        except error.URLError as exc:
            raise SourceAdapterError(f"请求失败 {url}: {exc.reason}") from exc


@dataclass(slots=True)
class NewsContext:
    themes: list[str] = field(default_factory=list)
    theme_summaries: dict[str, str] = field(default_factory=dict)


class EastMoneyAdapter:
    BASE_PUSH = "https://push2.eastmoney.com"
    BASE_PUSH_HIS = "https://push2his.eastmoney.com"
    NEWS_PAGE = "https://finance.eastmoney.com/a/ccjdd.html"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def get_quote(self, symbol: str) -> QuoteResult:
        secid = to_eastmoney_secid(symbol)
        fields = "f57,f58,f43,f169,f170,f86"
        url = f"{self.BASE_PUSH}/api/qt/stock/get?secid={parse.quote(secid)}&fields={fields}"
        payload = self.http.get_json(url)
        data = expect_mapping(payload, "data", "EastMoney quote")
        return QuoteResult(
            name=str(data.get("f58") or symbol),
            code=str(data.get("f57") or symbol),
            market="CN",
            latest_price=scaled_money(data.get("f43")),
            change_amount=scaled_money(data.get("f169")),
            change_percent=scaled_percent(data.get("f170")),
            update_time=normalize_eastmoney_time(data.get("f86")),
            tool_used="EastMoney",
            note="source: data.eastmoney.com",
        )

    def get_kline_day(self, symbol: str, limit: int = 30) -> list[KLineItem]:
        secid = to_eastmoney_secid(symbol)
        url = (
            f"{self.BASE_PUSH_HIS}/api/qt/stock/kline/get?"
            f"secid={parse.quote(secid)}&klt=101&fqt=1&end=29991010&lmt={limit}"
            "&fields1=f1&fields2=f51,f52,f53,f54,f55,f56"
        )
        payload = self.http.get_json(url)
        data = expect_mapping(payload, "data", "EastMoney kline day")
        klines = data.get("klines") or []
        return [parse_eastmoney_kline(row) for row in klines]

    def get_kline_time(self, symbol: str, ndays: int = 1) -> list[KLineItem]:
        secid = to_eastmoney_secid(symbol)
        url = (
            f"{self.BASE_PUSH_HIS}/api/qt/stock/trends2/get?"
            f"secid={parse.quote(secid)}&ndays={ndays}&iscr=0"
            "&fields1=f1,f2,f3,f4,f5,f6,f7,f8"
            "&fields2=f51,f52,f53,f54,f55,f56,f57,f58"
        )
        payload = self.http.get_json(url)
        data = expect_mapping(payload, "data", "EastMoney time kline")
        trends = data.get("trends") or []
        return [parse_eastmoney_trend(row) for row in trends]

    def get_live_news(self, count: int = 10) -> list[NewsItem]:
        page = self.http.get_text(self.NEWS_PAGE)
        match = re.search(r'titleList">\s*(.*?)\s*</div>\s*</div>', page, re.S)
        if not match:
            raise SourceAdapterError("EastMoney 新闻页未找到 titleList 片段。")

        block = unescape(match.group(1))
        items: list[NewsItem] = []
        pattern = re.compile(
            r'<li[^>]*>.*?<a[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>.*?<p[^>]*>(?P<summary>.*?)</p>.*?<span[^>]*>(?P<time>.*?)</span>',
            re.S,
        )
        for matched in pattern.finditer(block):
            title = strip_html(matched.group("title")).strip()
            if not title:
                continue
            summary = strip_html(matched.group("summary")).strip()
            published_at = strip_html(matched.group("time")).strip()
            items.append(NewsItem(title=title, summary=summary, published_at=published_at, tag="EastMoney"))
            if len(items) >= count:
                break

        if not items:
            fallback = re.findall(r'<a[^>]+href="https://finance\.eastmoney\.com/a/[^"]+"[^>]*>(.*?)</a>', block, re.S)
            for title in fallback:
                cleaned = strip_html(title).strip()
                if cleaned:
                    items.append(NewsItem(title=cleaned, summary="", published_at="", tag="EastMoney"))
                if len(items) >= count:
                    break

        if not items:
            raise SourceAdapterError("EastMoney 新闻页解析后为空。")
        return items

    def get_change_percent_list(self, top_n: int = 10) -> list[ListItem]:
        rows = self._get_clist(fields="f12,f14,f3")
        return [
            ListItem(
                name=str(row.get("f14") or "未知标的"),
                code=str(row.get("f12") or ""),
                value=to_float(row.get("f3")),
                metric_label="涨跌幅",
                extra_text="source: EastMoney 排行",
            )
            for row in rows[:top_n]
        ]

    def get_turnover_ratio_list(self, top_n: int = 10) -> list[ListItem]:
        rows = self._get_clist(fields="f12,f14,f8")
        return [
            ListItem(
                name=str(row.get("f14") or "未知标的"),
                code=str(row.get("f12") or ""),
                value=to_float(row.get("f8")),
                metric_label="换手率",
                extra_text="source: EastMoney 排行",
            )
            for row in rows[:top_n]
        ]

    def get_net_inflow_rate_list(self, top_n: int = 10) -> list[ListItem]:
        rows = self._get_clist(fields="f12,f14,f62")
        return [
            ListItem(
                name=str(row.get("f14") or "未知标的"),
                code=str(row.get("f12") or ""),
                value=to_float(row.get("f62")),
                metric_label="净流入额",
                extra_text="source: EastMoney 资金流",
            )
            for row in rows[:top_n]
        ]

    def screen_stocks(self, criteria: ScreenerCriteria) -> list[ScreenedStock]:
        rows = self._get_market_clist(
            market=criteria.market,
            fields="f12,f14,f2,f3,f8,f62,f9,f20,f100",
            pz=max(criteria.top_n * 8, 100),
        )
        news_context = build_news_context(self.get_live_news(count=12)) if criteria.strategy_name == "mid_long_term" else NewsContext()
        stocks: list[ScreenedStock] = []
        for row in rows:
            code = normalize_screen_code(str(row.get("f12") or ""), criteria.market)
            item = ScreenedStock(
                name=str(row.get("f14") or "未知标的"),
                code=code,
                latest_price=to_float(row.get("f2")),
                change_percent=to_float(row.get("f3")),
                turnover_ratio=to_float(row.get("f8")),
                net_inflow=to_float(row.get("f62")) if row.get("f62") not in (None, "") else None,
                pe_ttm=to_float(row.get("f9")) if row.get("f9") not in (None, "") else None,
                market_cap=to_float(row.get("f20")) if row.get("f20") not in (None, "") else None,
                industry=str(row.get("f100") or ""),
                source=f"EastMoney {criteria.market} 全市场",
            )
            if criteria.strategy_name == "mid_long_term":
                enrich_mid_long_term_item(item, news_context)
            if not match_screener(item, criteria):
                continue
            stocks.append(item)

        return sort_screened_stocks(stocks, criteria.sort_by)[: criteria.top_n]

    def get_exchange_rate(self, pair: str) -> FxResult:
        yahoo_symbol = fx_pair_to_yahoo_symbol(pair)
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{parse.quote(yahoo_symbol)}"
            "?interval=1m&range=1d&includePrePost=false"
        )
        payload = self.http.get_json(url)
        result = first_yahoo_chart_result(payload)
        meta = result.get("meta", {})
        return FxResult(
            pair=pair,
            rate=to_float(meta.get("regularMarketPrice")),
            quote_time=epoch_to_local_string(meta.get("regularMarketTime")),
            base_currency=pair.split("/")[0],
            target_currency=pair.split("/")[1],
            note="source: Yahoo Finance FX chart",
        )

    def _get_clist(self, fields: str, pz: int = 50) -> list[dict[str, Any]]:
        fs = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23"
        return self._get_clist_by_fs(fs=fs, fields=fields, pz=pz)

    def _get_market_clist(self, market: str, fields: str, pz: int = 50) -> list[dict[str, Any]]:
        if market == "HK":
            fs = "m:128+t:3,m:128+t:4,m:128+t:1,m:128+t:2"
        elif market == "US":
            fs = "m:105,m:106,m:107"
        else:
            fs = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23"
        return self._get_clist_by_fs(fs=fs, fields=fields, pz=pz)

    def _get_clist_by_fs(self, fs: str, fields: str, pz: int = 50) -> list[dict[str, Any]]:
        url = (
            f"{self.BASE_PUSH}/api/qt/clist/get?pn=1&pz={pz}&po=1&np=1&fltt=2&invt=2"
            f"&fid=f3&fs={parse.quote(fs)}&fields={parse.quote(fields)}"
        )
        payload = self.http.get_json(url)
        data = expect_mapping(payload, "data", "EastMoney clist")
        diff = data.get("diff")
        if not isinstance(diff, list):
            raise SourceAdapterError("EastMoney clist 返回结构异常。")
        return [row for row in diff if isinstance(row, dict)]


class YahooFinanceAdapter:
    CHART_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"
    NEWS_RSS_URL = "https://finance.yahoo.com/news/rssindex"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def get_quote(self, symbol: str) -> QuoteResult:
        result = first_yahoo_chart_result(self._get_chart(symbol, interval="1m", range_="1d"))
        meta = result.get("meta", {})
        price = to_float(meta.get("regularMarketPrice"))
        prev_close = to_float(meta.get("chartPreviousClose"))
        change_amount = price - prev_close
        change_percent = (change_amount / prev_close * 100.0) if prev_close else 0.0
        return QuoteResult(
            name=str(meta.get("shortName") or meta.get("symbol") or symbol),
            code=str(meta.get("symbol") or symbol),
            market="HK",
            latest_price=price,
            change_amount=change_amount,
            change_percent=change_percent,
            update_time=epoch_to_local_string(meta.get("regularMarketTime")),
            tool_used="YahooFinance",
            note="source: finance.yahoo.com",
        )

    def get_kline_day(self, symbol: str, range_: str = "1mo", interval: str = "1d") -> list[KLineItem]:
        return parse_yahoo_chart_items(self._get_chart(symbol, interval=interval, range_=range_))

    def get_kline_time(self, symbol: str, range_: str = "1d", interval: str = "1m") -> list[KLineItem]:
        return parse_yahoo_chart_items(self._get_chart(symbol, interval=interval, range_=range_))

    def _get_chart(self, symbol: str, interval: str, range_: str) -> Any:
        url = (
            f"{self.CHART_BASE}/{parse.quote(symbol)}?"
            f"interval={parse.quote(interval)}&range={parse.quote(range_)}&includePrePost=false"
        )
        return self.http.get_json(url)

    def get_news(self, count: int = 10) -> list[NewsItem]:
        xml_text = self.http.get_text(self.NEWS_RSS_URL)
        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError as exc:
            raise SourceAdapterError("Yahoo Finance RSS 解析失败。") from exc

        items: list[NewsItem] = []
        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            summary = strip_html((item.findtext("description") or "").strip())
            pub_date = (item.findtext("pubDate") or "").strip()
            if not title:
                continue
            items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    published_at=pub_date,
                    tag="Yahoo Finance",
                )
            )
            if len(items) >= count:
                break
        if not items:
            raise SourceAdapterError("Yahoo Finance RSS 内容为空。")
        return items


class StockAnalysisAdapter:
    BASE = "https://stockanalysis.com/stocks"
    NEWS_URL = "https://stockanalysis.com/news/all-stocks/"

    def __init__(self, http: HttpClient | None = None) -> None:
        self.http = http or HttpClient()

    def get_quote(self, symbol: str) -> QuoteResult:
        page = self.http.get_text(f"{self.BASE}/{symbol.lower()}/")
        return parse_stockanalysis_quote(page, fallback_symbol=symbol)

    def get_news(self, count: int = 10) -> list[NewsItem]:
        page = self.http.get_text(self.NEWS_URL)
        matches = re.findall(
            r'<h3[^>]*>\s*<a[^>]+href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>\s*</h3>.*?<p[^>]*>(?P<summary>.*?)</p>',
            page,
            re.S,
        )
        items: list[NewsItem] = []
        for _, title, summary in matches:
            cleaned = strip_html(title).strip()
            if len(cleaned) < 8:
                continue
            items.append(
                NewsItem(
                    title=cleaned,
                    summary=strip_html(summary).strip(),
                    published_at="",
                    tag="StockAnalysis",
                )
            )
            if len(items) >= count:
                break
        if not items:
            raise SourceAdapterError("StockAnalysis 新闻页解析后为空。")
        return items


def to_eastmoney_secid(symbol: str) -> str:
    if symbol.endswith(".SH"):
        return f"1.{symbol.split('.')[0]}"
    if symbol.endswith(".SZ"):
        return f"0.{symbol.split('.')[0]}"
    if symbol.startswith(("6", "9")):
        return f"1.{symbol}"
    return f"0.{symbol}"


def parse_eastmoney_kline(row: str) -> KLineItem:
    parts = row.split(",")
    if len(parts) < 5:
        raise SourceAdapterError(f"EastMoney K 线数据格式异常: {row}")
    return KLineItem(
        timestamp=parts[0],
        open_price=to_float(parts[1]),
        close_price=to_float(parts[2]),
        high_price=to_float(parts[3]),
        low_price=to_float(parts[4]),
        volume=to_optional_float(parts[5] if len(parts) > 5 else None),
    )


def parse_eastmoney_trend(row: str) -> KLineItem:
    parts = row.split(",")
    if len(parts) < 2:
        raise SourceAdapterError(f"EastMoney 分时数据格式异常: {row}")
    price = to_float(parts[1])
    return KLineItem(
        timestamp=parts[0],
        open_price=price,
        high_price=price,
        low_price=price,
        close_price=price,
        volume=to_optional_float(parts[5] if len(parts) > 5 else None),
    )


def expect_mapping(payload: Any, key: str, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SourceAdapterError(f"{label} 返回不是对象。")
    data = payload.get(key)
    if not isinstance(data, dict):
        raise SourceAdapterError(f"{label} 缺少 {key} 对象。")
    return data


def scaled_money(value: Any) -> float:
    return to_float(value) / 100.0


def scaled_percent(value: Any) -> float:
    return to_float(value) / 100.0


def normalize_eastmoney_time(value: Any) -> str:
    raw = str(value or "")
    if len(raw) == 14 and raw.isdigit():
        return datetime.strptime(raw, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    return raw


def first_yahoo_chart_result(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SourceAdapterError("Yahoo Finance 返回不是对象。")
    chart = payload.get("chart")
    if not isinstance(chart, dict):
        raise SourceAdapterError("Yahoo Finance 缺少 chart。")
    if chart.get("error"):
        raise SourceAdapterError(f"Yahoo Finance 返回错误: {chart['error']}")
    result = chart.get("result")
    if not isinstance(result, list) or not result or not isinstance(result[0], dict):
        raise SourceAdapterError("Yahoo Finance 缺少 result。")
    return result[0]


def parse_yahoo_chart_items(payload: Any) -> list[KLineItem]:
    result = first_yahoo_chart_result(payload)
    timestamps = result.get("timestamp") or []
    quote_list = result.get("indicators", {}).get("quote", [])
    if not quote_list:
        raise SourceAdapterError("Yahoo Finance 缺少 indicators.quote。")
    quote = quote_list[0]
    opens = quote.get("open") or []
    highs = quote.get("high") or []
    lows = quote.get("low") or []
    closes = quote.get("close") or []
    volumes = quote.get("volume") or []

    items: list[KLineItem] = []
    for index, ts in enumerate(timestamps):
        close_value = safe_index(closes, index)
        if close_value in (None, ""):
            continue
        items.append(
            KLineItem(
                timestamp=epoch_to_local_string(ts),
                open_price=to_float(safe_index(opens, index, close_value)),
                high_price=to_float(safe_index(highs, index, close_value)),
                low_price=to_float(safe_index(lows, index, close_value)),
                close_price=to_float(close_value),
                volume=to_optional_float(safe_index(volumes, index)),
            )
        )
    return items


def parse_stockanalysis_quote(page: str, fallback_symbol: str) -> QuoteResult:
    name_match = re.search(r"<title>(.+?)\s+\(([A-Z.\-]+)\)\s+Stock Price", page)
    price_match = re.search(r'"price"\s*:\s*([\d.]+)', page)
    change_match = re.search(r'"change"\s*:\s*([+-]?[\d.]+)', page)
    change_percent_match = re.search(r'"changesPercentage"\s*:\s*([+-]?[\d.]+)', page)

    if not name_match or not price_match:
        raise SourceAdapterError("StockAnalysis 页面结构可能已变化，未能解析美股报价。")

    return QuoteResult(
        name=name_match.group(1).strip(),
        code=name_match.group(2).strip() or fallback_symbol,
        market="US",
        latest_price=to_float(price_match.group(1)),
        change_amount=to_float(change_match.group(1)) if change_match else 0.0,
        change_percent=to_float(change_percent_match.group(1)) if change_percent_match else 0.0,
        update_time="",
        tool_used="StockAnalysis",
        note="source: stockanalysis.com",
    )


def epoch_to_local_string(value: Any) -> str:
    if value in (None, ""):
        return ""
    return datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")


def safe_index(values: list[Any], index: int, default: Any = None) -> Any:
    if 0 <= index < len(values):
        return values[index]
    return default


def to_float(value: Any) -> float:
    if value in (None, "", "-", "--", "null"):
        return 0.0
    return float(value)


def to_optional_float(value: Any) -> float | None:
    if value in (None, "", "-", "--", "null"):
        return None
    return float(value)


def fx_pair_to_yahoo_symbol(pair: str) -> str:
    mapping = {
        "CNY/USD": "USDCNY=X",
        "USD/CNY": "USDCNY=X",
        "CNY/HKD": "HKDCNY=X",
        "CNY/JPY": "JPYCNY=X",
        "CNY/EUR": "EURCNY=X",
    }
    return mapping.get(pair, "USDCNY=X")


def build_news_context(items: list[NewsItem]) -> NewsContext:
    context = NewsContext()
    theme_mapping = {
        "电力能源修复": ("电力", "能源", "公用事业", "光伏", "风电", "火电"),
        "黄金资源配置": ("黄金", "贵金属", "有色", "资源"),
        "消费酒旅修复": ("白酒", "消费", "食品饮料", "商贸零售", "旅游"),
        "非银低估值": ("券商", "保险", "多元金融", "非银"),
        "高端制造": ("高端制造", "轨交", "工业", "设备", "机器人", "算力", "服务器", "电子"),
        "宏观稳增长": ("稳增长", "经济", "基建", "物流", "家电"),
    }
    for item in items:
        haystack = f"{item.title} {item.summary}"
        for theme, keywords in theme_mapping.items():
            if any(keyword in haystack for keyword in keywords):
                if theme not in context.themes:
                    context.themes.append(theme)
                    context.theme_summaries[theme] = item.title
    return context


def enrich_mid_long_term_item(item: ScreenedStock, news_context: NewsContext) -> None:
    reason_tags: list[str] = []
    score = 0.0

    market_cap = item.market_cap or 0.0
    pe_ttm = item.pe_ttm
    turnover = item.turnover_ratio or 0.0
    net_inflow = item.net_inflow or 0.0
    descriptor = f"{item.name} {item.industry}"

    if market_cap >= 100_000_000_000:
        score += 2.5
        reason_tags.append("大市值")
    elif market_cap >= 30_000_000_000:
        score += 1.5
        reason_tags.append("中大市值")

    if pe_ttm is not None and 0 < pe_ttm <= 25:
        score += 2.0
        reason_tags.append("估值相对合理")
    elif pe_ttm is not None and pe_ttm <= 45:
        score += 1.0
        reason_tags.append("估值可接受")

    if net_inflow >= 300_000_000:
        score += 2.0
        reason_tags.append("资金净流入强")
    elif net_inflow >= 50_000_000:
        score += 1.0
        reason_tags.append("资金净流入为正")

    if 1.0 <= turnover <= 8.0:
        score += 1.5
        reason_tags.append("换手健康")
    elif 0.3 <= turnover < 1.0:
        score += 0.8
        reason_tags.append("换手偏稳")
    elif turnover > 15.0:
        score -= 0.8
        reason_tags.append("换手偏热")

    theme_hits: list[str] = []
    for theme in news_context.themes:
        if theme_matches_stock(theme, descriptor):
            theme_hits.append(theme)
            score += 1.2
    if theme_hits:
        reason_tags.append("新闻主题共振")
        item.news_summary = "；".join(news_context.theme_summaries[theme] for theme in theme_hits[:2])

    if -3.0 <= item.change_percent <= 6.0:
        score += 0.8
        reason_tags.append("未明显过热")
    elif item.change_percent > 9.0:
        score -= 1.2
        reason_tags.append("涨幅偏热")

    item.reason_tags = deduplicate_strings(reason_tags)
    item.news_score = float(len(theme_hits))
    item.score = round(score, 2)


def theme_matches_stock(theme: str, descriptor: str) -> bool:
    mapping = {
        "电力能源修复": ("电力", "能源", "光伏", "风电", "火电", "储能"),
        "黄金资源配置": ("黄金", "贵金属", "资源", "有色"),
        "消费酒旅修复": ("白酒", "消费", "食品饮料", "旅游", "酒店"),
        "非银低估值": ("券商", "保险", "金融"),
        "高端制造": ("工业", "高端制造", "轨交", "设备", "算力", "电子", "机器人", "通信"),
        "宏观稳增长": ("基建", "物流", "家电", "铁路", "工程", "制造"),
    }
    return any(keyword in descriptor for keyword in mapping.get(theme, ()))


def deduplicate_strings(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def match_screener(item: ScreenedStock, criteria: ScreenerCriteria) -> bool:
    if criteria.min_change_percent is not None and item.change_percent < criteria.min_change_percent:
        return False
    if criteria.max_change_percent is not None and item.change_percent > criteria.max_change_percent:
        return False
    if criteria.min_turnover_ratio is not None and (item.turnover_ratio or 0.0) < criteria.min_turnover_ratio:
        return False
    if criteria.max_price is not None and item.latest_price > criteria.max_price:
        return False
    if criteria.min_price is not None and item.latest_price < criteria.min_price:
        return False
    if criteria.min_net_inflow is not None and (item.net_inflow or 0.0) < criteria.min_net_inflow:
        return False
    if criteria.min_market_cap is not None and (item.market_cap or 0.0) < criteria.min_market_cap:
        return False
    if criteria.max_market_cap is not None and (item.market_cap or 0.0) > criteria.max_market_cap:
        return False
    if criteria.min_pe_ttm is not None and (item.pe_ttm or 0.0) < criteria.min_pe_ttm:
        return False
    if criteria.max_pe_ttm is not None and (item.pe_ttm or 0.0) > criteria.max_pe_ttm:
        return False
    if criteria.min_news_score is not None and (item.news_score or 0.0) < criteria.min_news_score:
        return False
    return True


def sort_screened_stocks(items: list[ScreenedStock], sort_by: str) -> list[ScreenedStock]:
    key_map = {
        "change_percent": lambda item: item.change_percent,
        "turnover_ratio": lambda item: item.turnover_ratio or 0.0,
        "net_inflow": lambda item: item.net_inflow or 0.0,
        "market_cap": lambda item: item.market_cap or 0.0,
        "pe_ttm": lambda item: -(item.pe_ttm or 0.0),
        "score": lambda item: item.score or 0.0,
        "news_score": lambda item: item.news_score or 0.0,
    }
    key_fn = key_map.get(sort_by, key_map["change_percent"])
    return sorted(items, key=key_fn, reverse=True)


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def normalize_screen_code(code: str, market: str) -> str:
    if market == "HK":
        return f"{code}.HK" if code and not code.endswith(".HK") else code
    if market == "US" and "." in code:
        return code.split(".", 1)[1]
    return code
