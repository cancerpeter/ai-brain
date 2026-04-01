from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import NewsItem, ScreenedStock, ScreenerCriteria
from .plugin_client import PluginClient, PluginClientError


@dataclass(slots=True)
class WorkflowSection:
    market_label: str
    market_code: str
    strategy_label: str
    strategy_code: str
    indicators: list[str]
    headlines: list[NewsItem]
    picks: list[ScreenedStock]


def build_market_report(top_n: int = 3, config_path: str | None = None) -> str:
    client = PluginClient()
    config = load_workflow_config(config_path)
    sections = [collect_section(client, section, top_n) for section in config["sections"]]

    today = datetime.now().strftime("%Y-%m-%d")
    body = [
        f"# {today} 多市场长短线买入推荐工作流测试",
        "",
        "## 说明",
        "",
        "- 本文档由工作流自动生成。",
        f"- 当前任务先读取策略文档：`{config['config_path']}`。",
        "- 每个市场分成长线与短线两类推荐。",
        "- 长线更看重估值、资金、规模与新闻背景。",
        "- 短线更看重涨跌幅强度、换手率、资金动量与盘中热度。",
        "",
    ]
    for section in sections:
        body.extend(render_section(section))
    return "\n".join(body).rstrip() + "\n"


def collect_section(client: PluginClient, section_config: dict[str, Any], top_n: int) -> WorkflowSection:
    market_label = str(section_config["market_label"])
    market_code = str(section_config["market_code"])
    strategy_label = str(section_config["strategy_label"])
    strategy_code = str(section_config["strategy_code"])
    indicators = [str(item) for item in section_config.get("indicators", [])]
    headlines = collect_market_news(client, market_code, count=4)
    picks = collect_market_picks(client, section_config, top_n)
    return WorkflowSection(
        market_label=market_label,
        market_code=market_code,
        strategy_label=strategy_label,
        strategy_code=strategy_code,
        indicators=indicators,
        headlines=headlines,
        picks=picks,
    )


def collect_market_news(client: PluginClient, market_code: str, count: int) -> list[NewsItem]:
    try:
        if market_code == "CN":
            return client.get_live_news(count=count)
        if market_code == "HK":
            return client.yahoo_finance.get_news(count=count)
        return client.stock_analysis.get_news(count=count)
    except Exception:
        return []


def collect_market_picks(client: PluginClient, section_config: dict[str, Any], top_n: int) -> list[ScreenedStock]:
    market_code = str(section_config["market_code"])
    strategy_code = str(section_config["strategy_code"])
    criteria = build_strategy_criteria(section_config, top_n)
    try:
        if strategy_code == "long":
            items = client.screen_long_term_stocks(criteria)
        else:
            items = client.screen_short_term_stocks(criteria)
    except PluginClientError:
        return []

    filtered = [item for item in items if is_workflow_candidate(item, strategy_code)]
    return [decorate_pick(item, market_code, strategy_code, section_config) for item in filtered[:top_n]]


def build_strategy_criteria(section_config: dict[str, Any], top_n: int) -> ScreenerCriteria:
    criteria = dict(section_config.get("criteria", {}))
    criteria["market"] = str(section_config["market_code"])
    criteria["top_n"] = top_n
    return ScreenerCriteria(**criteria)


def decorate_pick(
    item: ScreenedStock,
    market_code: str,
    strategy_code: str,
    section_config: dict[str, Any],
) -> ScreenedStock:
    reasons = list(item.reason_tags)
    reason_phrases = section_config.get("reason_phrases", {})
    if strategy_code == "long":
        if (item.market_cap or 0.0) >= market_cap_threshold(market_code):
            reasons.append(str(reason_phrases.get("market_cap", "市值基础较好")))
        if item.pe_ttm is not None and 0 < item.pe_ttm <= pe_threshold(market_code):
            reasons.append(str(reason_phrases.get("pe_ttm", "估值相对可控")))
        if (item.net_inflow or 0.0) > 0:
            reasons.append(str(reason_phrases.get("net_inflow", "资金面偏正")))
        if market_code == "CN" and 0.8 <= (item.turnover_ratio or 0.0) <= 8.0:
            reasons.append(str(reason_phrases.get("turnover_ratio", "换手结构健康")))
        item.score = round(long_score(item, market_code), 2)
    else:
        if item.change_percent >= 4.0:
            reasons.append(str(reason_phrases.get("change_percent", "动量较强")))
        if (item.turnover_ratio or 0.0) >= short_turnover_threshold(market_code):
            reasons.append(str(reason_phrases.get("turnover_ratio", "换手活跃")))
        if (item.net_inflow or 0.0) > 0:
            reasons.append(str(reason_phrases.get("net_inflow", "资金助推")))
        if item.change_percent <= 12.0:
            reasons.append(str(reason_phrases.get("heat", "尚未极端过热")))
        item.score = round(short_score(item, market_code), 2)
    item.reason_tags = deduplicate(reasons)
    return item


def is_workflow_candidate(item: ScreenedStock, strategy_code: str) -> bool:
    if strategy_code == "long":
        if item.name.startswith("N"):
            return False
        if item.pe_ttm is None or item.pe_ttm <= 0:
            return False
        if item.change_percent > 12.0:
            return False
    return True


def long_score(item: ScreenedStock, market_code: str) -> float:
    score = 0.0
    if (item.market_cap or 0.0) >= market_cap_threshold(market_code):
        score += 2.0
    if item.pe_ttm is not None and 0 < item.pe_ttm <= pe_threshold(market_code):
        score += 2.0
    if (item.net_inflow or 0.0) > 0:
        score += 2.0
    turnover = item.turnover_ratio or 0.0
    if market_code == "CN":
        if 0.8 <= turnover <= 8.0:
            score += 1.5
        elif turnover > 12.0:
            score -= 0.5
    return score


def short_score(item: ScreenedStock, market_code: str) -> float:
    score = 0.0
    score += min(max(item.change_percent, 0.0), 12.0) / 3.0
    score += min(item.turnover_ratio or 0.0, 15.0) / 5.0
    if (item.net_inflow or 0.0) > 0:
        score += 1.5
    return score


def market_cap_threshold(market_code: str) -> float:
    if market_code == "CN":
        return 50_000_000_000
    if market_code == "HK":
        return 20_000_000_000
    return 10_000_000_000


def pe_threshold(market_code: str) -> float:
    if market_code == "CN":
        return 45.0
    return 35.0


def short_turnover_threshold(market_code: str) -> float:
    if market_code == "CN":
        return 5.0
    if market_code == "HK":
        return 2.0
    return 0.0


def render_section(section: WorkflowSection) -> list[str]:
    lines = [
        f"## {section.market_label}{section.strategy_label}推荐",
        "",
        "### 指标设计",
        "",
    ]
    if section.indicators:
        for indicator in section.indicators:
            lines.append(f"- {indicator}")
    else:
        lines.append("- 当前未配置指标说明。")
    lines.extend(["", "### 相关新闻", ""])
    if section.headlines:
        for item in section.headlines:
            lines.append(f"- {item.title}")
    else:
        lines.append("- 今日未成功拉取该市场新闻。")
    lines.extend(["", "### 推荐列表", ""])

    if not section.picks:
        lines.extend(["- 今日未筛出满足当前阈值的推荐标的。", ""])
        return lines

    for index, item in enumerate(section.picks, start=1):
        lines.extend(
            [
                f"#### {index}. {item.name}（{item.code}）",
                "",
                f"- 行业：{item.industry or '未标注'}",
                f"- 最新价：{item.latest_price:.2f}",
                f"- 涨跌幅：{item.change_percent:+.2f}%",
                f"- 换手率：{format_optional(item.turnover_ratio, suffix='%')}",
                f"- 主力净流入：{format_money(item.net_inflow)}",
                f"- PE(TTM)：{format_optional(item.pe_ttm)}",
                f"- 市值：{format_money(item.market_cap)}",
                f"- 综合分：{format_optional(item.score)}",
                f"- 推荐理由：{', '.join(item.reason_tags) or fallback_reason(section.strategy_code)}",
                f"- 入手时机：{entry_timing(item, section.strategy_code)}",
                "",
            ]
        )
    return lines


def entry_timing(item: ScreenedStock, strategy_code: str) -> str:
    if strategy_code == "long":
        if (item.change_percent or 0.0) > 4.0:
            return "更适合等回踩或横盘消化后分批介入，不建议追高。"
        return "更适合在盘中回落、承接稳定时分批布局。"
    if (item.change_percent or 0.0) >= 8.0:
        return "适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。"
    return "适合观察开盘后 30 到 60 分钟的量价配合，再决定是否跟随。"


def fallback_reason(strategy_code: str) -> str:
    if strategy_code == "long":
        return "估值、资金和规模更适合长线观察"
    return "动量、换手和资金面更适合短线观察"


def format_optional(value: float | None, suffix: str = "") -> str:
    if value is None:
        return "暂无"
    return f"{value:.2f}{suffix}"


def format_money(value: float | None) -> str:
    if value is None:
        return "暂无"
    return f"{value / 100000000:.2f}亿"


def deduplicate(items: list[str]) -> list[str]:
    result: list[str] = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def write_market_report(output_path: str, top_n: int = 3, config_path: str | None = None) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_market_report(top_n=top_n, config_path=config_path), encoding="utf-8")
    return path


def load_workflow_config(config_path: str | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path else default_config_path()
    text = path.read_text(encoding="utf-8")
    config = json.loads(extract_json_code_block(text))
    sections = config.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("workflow strategy config 缺少 sections。")
    config["config_path"] = str(path)
    return config


def default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "workflow_strategy.md"


def extract_json_code_block(text: str) -> str:
    match = re.search(r"```json\s*(\{.*\})\s*```", text, re.S)
    if not match:
        raise ValueError("workflow strategy markdown 中未找到 json 代码块。")
    return match.group(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate multi-market long/short recommendation markdown.")
    parser.add_argument("--output", required=True, help="Output markdown path.")
    parser.add_argument("--top-n", type=int, default=3, help="Number of picks per market/strategy section.")
    parser.add_argument("--config", default="", help="Workflow strategy markdown path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = write_market_report(
        output_path=args.output,
        top_n=max(1, args.top_n),
        config_path=args.config or None,
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
