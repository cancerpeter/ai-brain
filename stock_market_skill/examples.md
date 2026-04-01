# Examples

以下示例均基于当前工程骨架的自然语言入口设计。

## 1. 查 A 股实时价

```text
输入：查一下贵州茅台现在多少钱
路由：GetSinaStockData
```

## 2. 查港股实时价

```text
输入：查腾讯港股实时价
路由：GetHKStockData
```

## 3. 查日 K

```text
输入：给我看一下宁德时代日K
路由：GetKLineDayStockData
```

## 4. 查分时

```text
输入：看看比亚迪今天分时走势
路由：GetKLineTimeStockData
```

## 5. 查汇率

```text
输入：人民币兑美元汇率
路由：GetExchangeRate
```

## 6. 查财经新闻

```text
输入：给我最新财经新闻，5条
路由：GetLiveNews
```

## 7. 查涨跌幅榜

```text
输入：今天涨跌幅榜前10
路由：GetChangePercentList
```

## 8. 查净流入榜

```text
输入：看一下资金净流入榜
路由：GetNetInflowRateList
```

## 9. 查换手率榜

```text
输入：换手率榜前5
路由：GetTurnoverRatioList
```

## 10. 歧义输入示例

```text
输入：帮我看下这只股票
结果：返回候选提示或澄清，而不是直接瞎猜
```

## 11. 查美股实时价

```text
输入：查一下美股 AAPL
路由：GetUSStockData
来源：stockanalysis.com
```

## 12. 全市场筛选

```text
输入：帮我筛选涨幅大于3换手率大于5前10只股票
路由：ScreenStocks
来源：EastMoney 全市场
```

## 13. 当日财经新闻整理

```text
输入：帮我整理今日财经新闻汇总，前15条
路由：GetDailyNewsDigest
来源：EastMoney + Yahoo Finance + StockAnalysis
```

## 14. 长线候选筛选

```text
输入：帮我挑选适合长线投资的股票前10只
路由：ScreenLongTermStocks
来源：EastMoney 全市场
```

## 15. 短线候选筛选

```text
输入：帮我挑选适合短线投资的股票前10只
路由：ScreenShortTermStocks
来源：EastMoney 全市场
```

## 16. 中长线候选筛选

```text
输入：帮我挑选适合中长线投资的股票前6只
路由：ScreenMidLongTermStocks
来源：EastMoney 全市场 + EastMoney 新闻
```

## 17. 港股长线候选筛选

```text
输入：帮我挑选适合港股长线投资的股票前10只
路由：ScreenLongTermStocks
来源：EastMoney HK 全市场
```

## 18. 美股短线候选筛选

```text
输入：帮我挑选适合美股短线投资的股票前10只
路由：ScreenShortTermStocks
来源：EastMoney US 全市场
```

## 19. 生成三市场长短线推荐 md

```text
命令：python3 -m stock_market_skill.report_workflow --output tests/2026-04-01-market-workflow.md --top-n 3
结果：自动读取 workflow_strategy.md，再生成 A股 / 港股 / 美股 的长线、短线推荐 markdown
```
