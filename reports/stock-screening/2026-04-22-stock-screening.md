# 2026-04-22 股票筛选日报

更新日期：2026-04-22
数据口径：计划以上一交易日 2026-04-21 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行已按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 与 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md) 执行，并使用 `PYTHONPATH='/Users/peter.chen/Documents/知识库搭建/stock_market_skill' /opt/homebrew/bin/python3 -m stock_market_skill.report_workflow --output '/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md' --top-n 3` 生成候选池文件 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md)。但 A 股、港股、美股公共行情链路均仍无法解析域名，导致无法按规则正式复算 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量均值 / 成交额 / 换手率 / 振幅 / 波动率 / 回撤`；以下内容以执行结果和阻塞信息为主，不替代正式技术评分。

## 1. 今日结论

- 面向 2026-04-21 收盘数据的三市场正式技术筛选本轮仍未完成，问题仍在公开行情接口的 DNS 解析失败，而不是筛选规则、模板或 Git 流程。
- 已成功生成三市场候选池执行痕迹，但 A 股、港股、美股本轮候选池均为空；在无法正式复算 `SCORING.md` 指标时，空名单优于失真名单。
- 本地可复核的历史样本仍只有旧缓存 [`/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/600519-6mo.csv`](/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/600519-6mo.csv) 与 [`/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/AAPL-6mo.csv`](/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/AAPL-6mo.csv)，日期分别停留在 2026-04-15 与 2026-04-14，既不覆盖 2026-04-21，也不覆盖港股，因此不能替代本轮正式筛选。

## 2. A 股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-21 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120` 结构；单独测试 `EastMoneyAdapter().get_kline_day('600519', limit=5)` 时，请求 `push2his.eastmoney.com` 返回 DNS 解析失败。
- 动量信号：无法正式计算 `RSI14 / MACD`。
- 相对强弱：未能对照沪深 300 计算 20 日、60 日超额收益。
- 量能与流动性：无法补算成交量均值、成交额、换手率与振幅；在现有链路下不应强行给出名单。
- 风险提示：如果后续链路恢复后仍连续空名单，说明市场更可能处于趋势确认不足或结构分化阶段，应接受观察而不是补造样本。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md)

## 3. 港股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-21 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120`；单独测试港股市场快照 `_get_market_clist('HK', ...)` 时，请求 `push2.eastmoney.com` 返回 DNS 解析失败。
- 动量信号：无法正式计算 `RSI14 / MACD`，也无法判断是否存在短期过热或背离。
- 相对强弱：未能正式对照恒生指数完成 20 日、60 日超额收益比较。
- 量能与流动性：当前环境没有可用的港股本地历史缓存，无法补算成交量、成交额、换手率、振幅和波动率。
- 风险提示：在缺少完整历史序列与基准对照时，港股更容易把事件驱动脉冲误判成中期趋势，不宜勉强入选。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-21 数据正式复算。
- 趋势信号：无法确认 `MA20 / MA60 / MA120`；单独测试 `YahooFinanceAdapter().get_kline_day('AAPL', range_='3mo', interval='1d')` 时，`query1.finance.yahoo.com` 返回 DNS 解析失败。
- 动量信号：无法正式计算 `RSI14 / MACD`，因此不能判断是否存在有效中期趋势延续。
- 相对强弱：未能正式对照标普 500 完成 20 日、60 日超额收益比较。
- 量能与流动性：本地仅有停留在 2026-04-14 的 [`/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/AAPL-6mo.csv`](/Users/peter.chen/Documents/知识库搭建/reports/stock-screening/AAPL-6mo.csv) 示例缓存，无法代表 2026-04-21 的全市场状态。
- 风险提示：如果缺失完整历史序列与基准对照，美股观察名单更容易被短线情绪扭曲，不适合中长期跟踪。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md)

## 5. 风险提醒

- 当前最大风险仍是三市场历史日线与市场快照链路不完整，导致无法对 2026-04-21 这一前一交易日完成正式技术指标复算和跨市场相对强弱打分。
- 当前候选池三市场均为空，说明在既有阈值与现有链路约束下，没有足够可信的中长期观察对象；空名单优于失真名单。
- 本报告是技术筛选与研究线索，不等于直接买入建议；在 `MA20 / MA60 / MA120 / RSI14 / MACD / 波动率 / 回撤` 无法复核时，应优先控制误判风险。

## 6. 方法说明

- 使用目标：`MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱、成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取工作流文档与评分规则，再使用 `/opt/homebrew/bin/python3` 配合 `PYTHONPATH='/Users/peter.chen/Documents/知识库搭建/stock_market_skill'` 运行 `stock_market_skill.report_workflow` 生成三市场候选池执行痕迹。
- 环境备注：当前公开行情域名 `push2his.eastmoney.com`、`push2.eastmoney.com`、`query1.finance.yahoo.com` 在本环境均返回 `nodename nor servname provided, or not known`，因此候选池只能记录为空结果和阻塞信息。
- 备用依据：引用本轮成功生成但结果为空的候选池文件 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-22-market-workflow.md) 作为执行痕迹，不替代正式技术评分。
