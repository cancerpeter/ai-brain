from __future__ import annotations

import unittest

from stock_market_skill.models import IntentType
from stock_market_skill.router import route_query


class RouterTests(unittest.TestCase):
    def test_news_intent(self) -> None:
        result = route_query("给我最新财经新闻，5条")
        self.assertEqual(result.intent, IntentType.NEWS)
        self.assertEqual(result.tool_name, "GetLiveNews")
        self.assertEqual(result.params["count"], 5)

    def test_news_digest_intent(self) -> None:
        result = route_query("帮我整理今日财经新闻汇总，前15条")
        self.assertEqual(result.intent, IntentType.NEWS_DIGEST)
        self.assertEqual(result.tool_name, "GetDailyNewsDigest")
        self.assertEqual(result.params["count"], 15)

    def test_fx_intent(self) -> None:
        result = route_query("人民币兑美元汇率")
        self.assertEqual(result.intent, IntentType.FX)
        self.assertEqual(result.tool_name, "GetExchangeRate")
        self.assertEqual(result.params["pair"], "CNY/USD")

    def test_kline_day_intent(self) -> None:
        result = route_query("查贵州茅台日K")
        self.assertEqual(result.intent, IntentType.KLINE_DAY)
        self.assertEqual(result.tool_name, "GetKLineDayStockData")
        self.assertEqual(result.params["symbol"], "600519")

    def test_kline_time_intent(self) -> None:
        result = route_query("看看比亚迪今天分时走势")
        self.assertEqual(result.intent, IntentType.KLINE_TIME)
        self.assertEqual(result.tool_name, "GetKLineTimeStockData")
        self.assertEqual(result.params["symbol"], "002594")

    def test_hk_quote_intent(self) -> None:
        result = route_query("查腾讯港股实时价")
        self.assertEqual(result.intent, IntentType.HK_QUOTE)
        self.assertEqual(result.tool_name, "GetHKStockData")
        self.assertEqual(result.params["symbol"], "0700.HK")

    def test_default_quote_intent(self) -> None:
        result = route_query("查一下贵州茅台现在多少钱")
        self.assertEqual(result.intent, IntentType.QUOTE)
        self.assertEqual(result.tool_name, "GetSinaStockData")
        self.assertEqual(result.params["symbol"], "600519")

    def test_us_quote_intent(self) -> None:
        result = route_query("查一下美股 AAPL")
        self.assertEqual(result.intent, IntentType.US_QUOTE)
        self.assertEqual(result.tool_name, "GetUSStockData")
        self.assertEqual(result.params["symbol"], "AAPL")

    def test_clarification_when_security_missing(self) -> None:
        result = route_query("帮我看一下日K")
        self.assertTrue(result.needs_clarification)
        self.assertEqual(result.intent, IntentType.CLARIFICATION)

    def test_screen_intent(self) -> None:
        result = route_query("帮我筛选涨幅大于3换手率大于5前8只股票")
        self.assertEqual(result.intent, IntentType.SCREEN)
        self.assertEqual(result.tool_name, "ScreenStocks")
        self.assertEqual(result.params["top_n"], 8)
        self.assertEqual(result.params["min_change_percent"], 3.0)
        self.assertEqual(result.params["min_turnover_ratio"], 5.0)

    def test_long_term_screen_intent(self) -> None:
        result = route_query("帮我挑选适合长线投资的股票前6只")
        self.assertEqual(result.intent, IntentType.LONG_TERM_SCREEN)
        self.assertEqual(result.tool_name, "ScreenLongTermStocks")
        self.assertEqual(result.params["top_n"], 6)
        self.assertEqual(result.params["strategy_name"], "long_term")

    def test_mid_long_term_screen_intent(self) -> None:
        result = route_query("帮我挑选适合中长线投资的股票前5只")
        self.assertEqual(result.intent, IntentType.MID_LONG_TERM_SCREEN)
        self.assertEqual(result.tool_name, "ScreenMidLongTermStocks")
        self.assertEqual(result.params["top_n"], 5)
        self.assertEqual(result.params["strategy_name"], "mid_long_term")

    def test_short_term_screen_intent(self) -> None:
        result = route_query("帮我挑选适合短线投资的股票前5只")
        self.assertEqual(result.intent, IntentType.SHORT_TERM_SCREEN)
        self.assertEqual(result.tool_name, "ScreenShortTermStocks")
        self.assertEqual(result.params["top_n"], 5)
        self.assertEqual(result.params["strategy_name"], "short_term")

    def test_hk_long_term_screen_market(self) -> None:
        result = route_query("帮我挑选适合港股长线投资的股票前6只")
        self.assertEqual(result.intent, IntentType.LONG_TERM_SCREEN)
        self.assertEqual(result.params["market"], "HK")

    def test_us_short_term_screen_market(self) -> None:
        result = route_query("帮我挑选适合美股短线投资的股票前6只")
        self.assertEqual(result.intent, IntentType.SHORT_TERM_SCREEN)
        self.assertEqual(result.params["market"], "US")


if __name__ == "__main__":
    unittest.main()
