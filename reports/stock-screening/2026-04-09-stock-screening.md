# 2026-04-09 股票筛选日报

更新日期：2026-04-09
数据口径：计划以上一交易日 2026-04-08 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行已按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md) 读取流程并尝试抓取三市场最新历史日线，但当前终端环境对 `push2.eastmoney.com`、`push2his.eastmoney.com`、`query1.finance.yahoo.com` 等行情域名仍返回 `nodename nor servname provided, or not known`，因此无法按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 正式复算 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量均值 / 波动率 / 回撤`。以下内容以最近一次本地候选池缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md) 为主，仅作为观察线索。

## 1. 今日结论

- 2026-04-09 这轮自动化未能完成面向 2026-04-08 收盘数据的正式三市场技术筛选，核心阻塞仍是 shell 环境无法解析公开行情域名，而不是筛选规则本身。
- 最近一次本地候选池显示，A 股仍未出现满足纪律的正式候选；港股相对更强，仍以汽车链龙头为主；美股长线池继续为空，短线强势股大多是超小市值高波动样本，不适合中长期观察。

## 2. A 股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-08 数据正式复算。
- 趋势信号：由于 A 股历史日线未拉取成功，无法确认 `MA20 / MA60 / MA120` 结构。
- 动量信号：无法正式计算 `RSI14 / MACD`。
- 相对强弱：未能对照沪深 300 计算 20 日、60 日超额收益。
- 量能与流动性：最近一次本地候选池中，A 股长短线均为空，说明在既有纪律下没有可直接继承为正式技术观察对象的标的。
- 风险提示：在没有通过完整量价和趋势约束之前，不应为了“有名单”而放宽过滤条件。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md)

## 3. 港股候选

### 吉利汽车（00175.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；最近一次本地候选池综合分为 `6.00`。
- 趋势信号：缓存显示最新价 `23.82`、单日涨幅 `+8.37%`，具备较大市值与较完整资金承接，但 `MA20 / MA60 / MA120` 仍待正式复核。
- 动量信号：价格动量仍偏强，但无法确认 `RSI14 / MACD` 是否接近短期过热。
- 相对强弱：未能正式对照恒生指数完成 20 日与 60 日超额收益比较。
- 量能与流动性：缓存显示换手率 `1.74%`、主力净流入约 `2.52 亿`、市值约 `2572.50 亿`，在港股里兼具容量与流动性。
- 风险提示：若汽车链后续缺少销量或政策催化，强势股容易转入横盘或回踩消化，不适合追高。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md)

### 长城汽车（02333.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；最近一次本地候选池综合分为 `6.00`。
- 趋势信号：缓存显示最新价 `13.45`、单日涨幅 `+7.34%`，属于港股里更接近中期趋势观察的汽车龙头样本，但均线结构待补算。
- 动量信号：短期动量偏强，`RSI14 / MACD` 暂缺正式确认。
- 相对强弱：未能正式完成对恒生指数的超额收益比较。
- 量能与流动性：换手率 `1.84%`、主力净流入约 `0.81 亿`、市值约 `1151.03 亿`，交易承接优于多数题材性港股。
- 风险提示：若板块轮动转弱，涨幅较大的汽车股可能较快进入震荡整理，节奏上更适合等回踩验证。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md)

### 吉利汽车-R（80175.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；最近一次本地候选池综合分为 `4.00`。
- 趋势信号：价格表现与正股方向一致，但量能与资金字段缺失较多，趋势确认度弱于正股。
- 动量信号：存在价格弹性，但无法用完整历史序列复核 `RSI14 / MACD`。
- 相对强弱：未能正式完成相对恒生指数的收益比较。
- 量能与流动性：缓存中换手率和主力净流入均为 `0`，数据完整性不足，应低于正股优先级。
- 风险提示：若后续量能字段仍持续缺失，正式评分时更适合降权或剔除。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 规则正式复算。
- 趋势信号：最近一次本地候选池中的美股长线候选为空；短线强势样本主要为 `AIXI`、`HCAI`、`QNCX` 一类超小市值高波动个股，不符合中长期趋势基础要求。
- 动量信号：虽然缓存显示这些个股单日涨幅很大，但缺少完整历史日线与 `RSI14 / MACD` 复核，更像事件驱动脉冲而非稳定趋势。
- 相对强弱：未能正式对照标普 500 完成 20 日和 60 日超额收益比较。
- 量能与流动性：缓存中的高换手与极小市值组合意味着滑点、回撤和失真风险都很高，按硬过滤规则应重罚或剔除。
- 风险提示：当前美股可见机会更多是交易型高波动样本，不适合作为中长期观察池核心候选。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md)

## 5. 风险提醒

- 当前最大风险仍是数据链路不可用，导致无法对 2026-04-08 这一前一交易日数据完成正式技术复算。
- 港股观察名单当前更接近“候选池延续”而不是正式技术评分榜；待历史日线恢复后，应重新计算均线、相对强弱、成交额均值、波动率和回撤，再决定是否保留。
- 本报告是技术筛选与研究线索，不等于直接买入建议；对单日涨幅大、换手异常高或数据字段缺失的标的，应优先防止把情绪脉冲误判为中期趋势。

## 6. 方法说明

- 目标方法：使用 `MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱，以及成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)，随后尝试通过 `stock_market_skill` 的公开行情适配层拉取三市场全市场列表与历史日线。
- 阻塞详情：A 股、港股、美股列表以及日线请求均返回 `SourceAdapterError`，底层错误为 `nodename nor servname provided, or not known`；因此无法完成本轮正式筛选、打分和排序。
- 备用依据：引用最近一次可用的本地候选池缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-08-market-workflow.md) 作为观察性补充，不替代正式技术评分。
