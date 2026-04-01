from __future__ import annotations

import unittest

from stock_market_skill.models import ScreenedStock
from stock_market_skill.report_workflow import (
    build_strategy_criteria,
    decorate_pick,
    load_workflow_config,
)


class ReportWorkflowTests(unittest.TestCase):
    def test_build_strategy_criteria_for_cn_long(self) -> None:
        config = load_workflow_config()
        section = next(
            item
            for item in config["sections"]
            if item["market_code"] == "CN" and item["strategy_code"] == "long"
        )
        criteria = build_strategy_criteria(section, 3)
        self.assertEqual(criteria.market, "CN")
        self.assertEqual(criteria.strategy_name, "long_term")
        self.assertEqual(criteria.sort_by, "net_inflow")

    def test_decorate_pick_adds_long_reasons(self) -> None:
        config = load_workflow_config()
        section = next(
            item
            for item in config["sections"]
            if item["market_code"] == "CN" and item["strategy_code"] == "long"
        )
        item = ScreenedStock(
            name="示例公司",
            code="000001",
            latest_price=12.3,
            change_percent=2.5,
            turnover_ratio=1.2,
            net_inflow=200_000_000,
            pe_ttm=18.0,
            market_cap=80_000_000_000,
            industry="银行",
            source="test",
        )
        result = decorate_pick(item, "CN", "long", section)
        self.assertIsNotNone(result.score)
        self.assertIn("市值基础较好", result.reason_tags)
        self.assertIn("估值相对可控", result.reason_tags)
        self.assertIn("资金面偏正", result.reason_tags)


if __name__ == "__main__":
    unittest.main()
