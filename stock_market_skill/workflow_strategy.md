# Workflow Strategy

这份文档用于给 `stock_market_skill.report_workflow` 读取。

目标：

- 明确区分 A 股、港股、美股
- 明确区分长线、短线
- 让任务优先读取文档中的指标设计，再生成推荐 markdown

## 设计原则

- 长线：
  - 更重视市值、估值、资金面、不过热
  - 目标是观察与分批布局，而不是追单日最强
- 短线：
  - 更重视涨跌幅强度、换手、资金动量
  - 目标是找当日强势方向，但仍要求一定过滤

## 工作流配置

```json
{
  "sections": [
    {
      "market_label": "A股",
      "market_code": "CN",
      "strategy_label": "长线",
      "strategy_code": "long",
      "indicators": [
        "大中市值优先，避免纯小票博弈",
        "PE(TTM) 为正且不过热",
        "主力净流入为正",
        "换手率处于健康区间，避免极端情绪票"
      ],
      "criteria": {
        "strategy_name": "long_term",
        "sort_by": "net_inflow",
        "min_market_cap": 5000000000,
        "min_pe_ttm": 0.1,
        "max_pe_ttm": 50.0,
        "min_turnover_ratio": 0.8,
        "min_net_inflow": 0.0,
        "max_change_percent": 12.0
      },
      "reason_phrases": {
        "market_cap": "市值基础较好",
        "pe_ttm": "估值相对可控",
        "net_inflow": "资金面偏正",
        "turnover_ratio": "换手结构健康"
      }
    },
    {
      "market_label": "A股",
      "market_code": "CN",
      "strategy_label": "短线",
      "strategy_code": "short",
      "indicators": [
        "涨跌幅强度优先",
        "换手率明显放大",
        "主力净流入为正",
        "更适合盘中强势跟踪，不适合中线持有"
      ],
      "criteria": {
        "strategy_name": "short_term",
        "sort_by": "change_percent",
        "min_change_percent": 3.0,
        "min_turnover_ratio": 5.0,
        "min_net_inflow": 0.0
      },
      "reason_phrases": {
        "change_percent": "动量较强",
        "turnover_ratio": "换手活跃",
        "net_inflow": "资金助推",
        "heat": "尚未极端过热"
      }
    },
    {
      "market_label": "港股",
      "market_code": "HK",
      "strategy_label": "长线",
      "strategy_code": "long",
      "indicators": [
        "优先大市值和流动性更好的龙头",
        "PE(TTM) 保持在相对合理区间",
        "更关注估值与行业地位，而不是单日弹性",
        "过滤单日过热的情绪票"
      ],
      "criteria": {
        "strategy_name": "long_term",
        "sort_by": "market_cap",
        "min_market_cap": 20000000000,
        "min_pe_ttm": 0.1,
        "max_pe_ttm": 35.0,
        "max_change_percent": 12.0
      },
      "reason_phrases": {
        "market_cap": "港股龙头属性更强",
        "pe_ttm": "估值相对可控",
        "net_inflow": "资金面偏正"
      }
    },
    {
      "market_label": "港股",
      "market_code": "HK",
      "strategy_label": "短线",
      "strategy_code": "short",
      "indicators": [
        "优先筛选价格动量更强的活跃股",
        "换手率明显放大",
        "允许更高弹性，但不追求无限制拉升",
        "更适合快进快出"
      ],
      "criteria": {
        "strategy_name": "short_term",
        "sort_by": "change_percent",
        "min_change_percent": 4.0,
        "min_turnover_ratio": 2.0
      },
      "reason_phrases": {
        "change_percent": "动量较强",
        "turnover_ratio": "换手活跃",
        "net_inflow": "资金助推",
        "heat": "尚未极端过热"
      }
    },
    {
      "market_label": "美股",
      "market_code": "US",
      "strategy_label": "长线",
      "strategy_code": "long",
      "indicators": [
        "优先中大市值公司",
        "PE(TTM) 为正且不过热",
        "更重视企业规模和估值约束",
        "避免单日过度情绪化拉升个股"
      ],
      "criteria": {
        "strategy_name": "long_term",
        "sort_by": "market_cap",
        "min_market_cap": 10000000000,
        "min_pe_ttm": 0.1,
        "max_pe_ttm": 35.0,
        "max_change_percent": 12.0
      },
      "reason_phrases": {
        "market_cap": "公司规模更适合长线观察",
        "pe_ttm": "估值相对可控",
        "net_inflow": "资金面偏正"
      }
    },
    {
      "market_label": "美股",
      "market_code": "US",
      "strategy_label": "短线",
      "strategy_code": "short",
      "indicators": [
        "优先高动量个股",
        "允许更高波动，但只适合交易型策略",
        "关注当日资金与热度是否同步",
        "避免把超高波动票误当成长线标的"
      ],
      "criteria": {
        "strategy_name": "short_term",
        "sort_by": "change_percent",
        "min_change_percent": 4.0
      },
      "reason_phrases": {
        "change_percent": "动量较强",
        "turnover_ratio": "换手活跃",
        "net_inflow": "资金助推",
        "heat": "尚未极端过热"
      }
    }
  ]
}
```
