# 2026-04-07 股票筛选日报

更新日期：2026-04-07
数据口径：计划以上一交易日 2026-04-06 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行已成功执行三市场候选工作流并产出最新候选池，但当前环境仍无法访问 `push2his.eastmoney.com`、`query1.finance.yahoo.com` 等历史日线接口，导致 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量均值 / 波动率 / 回撤` 无法按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 完整复算。以下内容以本轮成功生成的候选池缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md) 为主，属于观察名单，不替代正式技术评分结果。

## 1. 今日结论

- 本轮可用结果显示，A 股候选重新出现，主要集中在医药、电池和半导体等高弹性方向；港股相对强势集中在汽车与高波动题材股；美股长线池仍为空，短线池则以极端波动的小市值标的为主，不适合作为中长期优先观察对象。
- 真正基于 `README.md` 定义完成的正式三市场评分工作流，仍卡在历史日线与基准指数不可达这一环节；因此今天的日报更接近“候选池更新 + 风险过滤建议”，而不是完整的 `0-100` 技术评分榜单。

## 2. A 股候选

### 哈药股份（600664）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `4.00`。
- 趋势信号：最新本地候选池显示单日涨幅 `+9.94%`，属于中等市值、估值未过热的强势股，但未能复核 `MA20 / MA60 / MA120` 多头排列。
- 动量信号：短期价格动量较强，但 `RSI14 / MACD` 尚未取得完整历史序列确认。
- 相对强弱：无法对照沪深 300 计算 20 日、60 日超额收益。
- 量能与流动性：候选池显示换手率 `9.64%`、主力净流入约 `2.69 亿`、市值约 `97.47 亿`，具备较好的交易承接。
- 风险提示：接近涨停后的次日承接和回踩质量更关键，若放量冲高回落，容易从中期候选退化成短线脉冲。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

### 蔚蓝锂芯（002245）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `3.50`。
- 趋势信号：候选池显示最新价 `17.91`、单日涨幅 `+8.88%`，并具备一定市值基础，但均线趋势仍待正式复核。
- 动量信号：价格弹性较好，短期动量偏强，`RSI14 / MACD` 未复算。
- 相对强弱：暂未完成相对沪深 300 的超额收益比较。
- 量能与流动性：换手率 `16.78%`、主力净流入约 `7.24 亿`，量能足够，但换手已偏高，不属于低波动趋势推进。
- 风险提示：高换手意味着筹码交换充分，也意味着波动可能显著放大，不宜把单日强势直接等同为稳定趋势。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

### 鹭燕医药（002788）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `3.50`。
- 趋势信号：候选池显示单日涨幅 `+10.02%`，属于医药流通方向的强势标的，但趋势级别仍需均线复核。
- 动量信号：单日动量突出，但未能确认 `RSI14 / MACD` 是否已接近过热区。
- 相对强弱：暂未完成相对沪深 300 的正式比较。
- 量能与流动性：换手率 `23.22%`、主力净流入约 `2.53 亿`，流动性充足，但交易属性明显强于稳态趋势属性。
- 风险提示：高换手叠加大阳线后，后续若无法维持量价配合，回撤速度可能较快。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

## 3. 港股候选

### 吉利汽车（00175.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `6.00`。
- 趋势信号：候选池显示最新价 `23.82`、单日涨幅 `+8.37%`，同时具备较大市值与合理估值，属于港股中更接近中期观察池的标的。
- 动量信号：价格动量较强，但 `RSI14 / MACD` 尚未复核，无法判断是否已进入短期加速末端。
- 相对强弱：未能正式对照恒生指数完成 20 日与 60 日超额收益比较。
- 量能与流动性：换手率 `1.74%`、主力净流入约 `2.52 亿`、市值约 `2572.50 亿`，在港股里兼具流动性与容量。
- 风险提示：汽车板块若缺少持续政策或销量催化，强势股也可能进入横盘消化，节奏上更适合等回踩确认。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

### 长城汽车（02333.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `6.00`。
- 趋势信号：候选池显示最新价 `13.45`、单日涨幅 `+7.34%`，具备与吉利类似的汽车板块强势特征。
- 动量信号：短期动量偏强，但 `RSI14 / MACD` 暂缺。
- 相对强弱：未能正式完成对恒生指数的超额收益比较。
- 量能与流动性：换手率 `1.84%`、主力净流入约 `0.81 亿`、市值约 `1151.03 亿`，流动性与容量优于高波动小盘港股。
- 风险提示：若板块轮动转弱，汽车股可能从趋势观察转为震荡整理，需警惕强势后的回撤。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

### 吉利汽车-R（80175.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `4.00`。
- 趋势信号：价格表现与正股方向一致，但候选池里换手率和主力净流入均为 `0`，数据完整性弱于主板正股。
- 动量信号：动量存在，但辅助指标无法完整确认。
- 相对强弱：未能正式完成相对恒生指数的收益比较。
- 量能与流动性：估值仍合理，市值较大，但成交与资金字段缺失使其不宜优先于正股观察。
- 风险提示：若后续仍缺乏完整量能字段，应在正式评分时降权或剔除。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 规则正式复算。
- 趋势信号：本轮长线候选池为空；短线缓存中的 `AIXI`、`SRTAW`、`PFSA` 均为极端波动小市值标的，不符合中长期趋势基础要求。
- 动量信号：虽然缓存显示这些个股单日涨幅极大，但缺少完整历史日线与 `RSI14 / MACD` 复核，更像事件驱动脉冲而非稳定趋势。
- 相对强弱：未能正式对照标普 500 完成超额收益比较。
- 量能与流动性：短线缓存标的换手率和波动率明显异常，按照硬过滤规则应被重罚或剔除。
- 风险提示：当前美股可见机会更多是高风险交易型脉冲，不适合作为中长期观察池核心候选。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md)

## 5. 风险提醒

- 当前最大风险不是个股本身，而是历史日线与基准指数链路不可用，导致正式技术打分缺失。
- A 股与港股候选当前更多是“工作流候选池”，还需要在恢复联网后补算均线、相对强弱、成交额均值、波动率和回撤，再决定是否保留为正式观察名单。
- 本报告是技术筛选与研究线索，不等于直接买入建议；尤其对单日高换手、高涨幅标的，更应优先防止把情绪脉冲误判为中期趋势。

## 6. 方法说明

- 目标方法：使用 `MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱，以及成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)，随后执行 `python3 -m stock_market_skill.report_workflow --output /tmp/2026-04-07-market-workflow-run.md --top-n 3` 获取最新三市场候选池。
- 阻塞详情：在单独拉取 A 股、港股历史日线时，`EastMoneyAdapter.get_kline_day(...)` 与 `YahooFinanceAdapter.get_kline_day(...)` 均返回 `SourceAdapterError`，错误原因为 `nodename nor servname provided, or not known`，因此无法完成本轮正式技术指标复算。
- 备用依据：引用本轮可复用的候选池缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-07-market-workflow.md) 作为观察性补充，不替代正式技术评分。
