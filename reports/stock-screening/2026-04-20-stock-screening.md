# 2026-04-20 股票筛选日报

更新日期：2026-04-20
数据口径：计划以上一交易日 2026-04-17 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行已按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md) 读取流程，并使用 `PYTHONPATH='/Users/peter.chen/Documents/知识库搭建/stock_market_skill' /opt/homebrew/bin/python3 -m stock_market_skill.report_workflow --output '/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md' --top-n 3` 生成候选池文件 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md)。但 `push2his.eastmoney.com` 与 `query1.finance.yahoo.com` 的历史日线请求仍返回 `nodename nor servname provided, or not known`，因此无法按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 正式复算 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量均值 / 成交额 / 换手率 / 振幅 / 波动率 / 回撤`。以下结论以本轮候选池结果与链路阻塞情况为主，不替代正式技术评分。

## 1. 今日结论

- 面向 2026-04-17 收盘数据的三市场正式技术筛选本轮仍未完成，根因仍是公开行情历史接口的 DNS 解析失败，而不是流程、模板或打分规则缺失。
- A 股、港股、美股的本轮候选池均为空，说明在当前阈值与链路约束下，没有足够可信的中长期观察对象；空名单优于失真名单。

## 2. A 股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-17 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120` 结构；本轮候选池也未筛出满足阈值的 A 股样本。
- 动量信号：无法正式计算 `RSI14 / MACD`。
- 相对强弱：未能对照沪深 300 计算 20 日、60 日超额收益。
- 量能与流动性：无法补算成交量均值、成交额、换手率与振幅的完整约束；在现有条件下不应强行填充名单。
- 风险提示：若链路恢复后仍连续无候选，说明市场更可能处于趋势确认不足或结构分化阶段，应接受空仓观察。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md)

## 3. 港股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-17 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120`；本轮候选池未保留满足当前阈值的港股样本。
- 动量信号：无法正式计算 `RSI14 / MACD`，也无法判断是否存在短期过热或背离。
- 相对强弱：未能正式对照恒生指数完成 20 日、60 日超额收益比较。
- 量能与流动性：本轮连市场新闻也未抓取成功，公开行情链路中断下更不宜把缺数据误判为低风险。
- 风险提示：港股若只看到零散脉冲而无法复核趋势基底，更容易把事件驱动错当成中期趋势。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-17 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120`；本轮候选池未筛出满足当前阈值的美股样本。
- 动量信号：无法正式计算 `RSI14 / MACD`，因此不能判断是否存在有效中期趋势延续。
- 相对强弱：未能正式对照标普 500 完成 20 日、60 日超额收益比较。
- 量能与流动性：无法补算成交量、成交额、换手率、振幅和波动率，不能把空白字段当成通过风控。
- 风险提示：如果缺失完整历史序列与基准对照，美股观察名单更容易被短线情绪扭曲，不适合中长期跟踪。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md)

## 5. 风险提醒

- 当前最大风险仍是历史日线链路不完整，导致无法对 2026-04-17 这一前一交易日完成正式技术指标复算和跨市场相对强弱打分。
- 当前候选池三市场均为空，说明在既有阈值与现有链路约束下，没有足够可信的中长期观察对象；空名单优于失真名单。
- 本报告是技术筛选与研究线索，不等于直接买入建议；在 `MA20 / MA60 / MA120 / RSI14 / MACD / 波动率 / 回撤` 无法复核时，应优先控制误判风险。

## 6. 方法说明

- 使用目标：`MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱、成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)，随后使用 `/opt/homebrew/bin/python3` 运行 `stock_market_skill.report_workflow` 生成三市场候选池。
- 环境备注：`.venv/bin/python` 当前仍不是可兼容 `stock_market_skill` 的解释器，因此本轮继续使用 `/opt/homebrew/bin/python3` 3.14 系列配合 `PYTHONPATH='/Users/peter.chen/Documents/知识库搭建/stock_market_skill'` 执行工作流，避免解释器兼容性误判。
- 阻塞详情：单独测试 `600519` 与 `AAPL` 的历史日线请求时，分别命中 `https://push2his.eastmoney.com/api/qt/stock/kline/get?...` 与 `https://query1.finance.yahoo.com/v8/finance/chart/...` 的 DNS 解析失败，错误均为 `nodename nor servname provided, or not known`。
- 备用依据：引用本轮成功生成但结果为空的候选池文件 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-20-market-workflow.md) 作为执行痕迹，不替代正式技术评分。
