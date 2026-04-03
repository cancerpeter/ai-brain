# 2026-04-03 股票筛选日报

更新日期：2026-04-03
数据口径：计划以上一交易日 2026-04-02 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行因当前环境访问公开行情源时出现远端断开与连接失败，未能重新抓取 A 股、港股、美股的完整历史日线与基准指数序列；以下内容以最新本地缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md) 为主，仅作为观察线索，不替代按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 正式复算后的结果。

## 1. 今日结论

- 本次自动化仍未完成按 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量 / 成交额 / 换手率 / 振幅 / 波动率 / 回撤` 的正式三市场筛选、打分和排序；本轮主要阻塞从昨日的 DNS 失败变为 `EastMoney` 连接阶段被远端断开，三市场新鲜数据链路仍不可用。
- 最新本地缓存延续了近期的结构性结论：A 股在当前阈值下暂无明确中长期候选；港股仍以医药和贵金属方向相对占优；美股缓存里的高弹性个股更接近事件驱动型交易，不符合中长期技术筛选的风险约束。

## 2. A 股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 规则复算。
- 趋势信号：本次运行未能重新拉取 2026-04-02 的 A 股历史日线，无法确认 `MA20 / MA60 / MA120` 结构。
- 动量信号：本次运行未能重新抓取技术序列，无法确认 `RSI14 / MACD`。
- 相对强弱：未能重新对照沪深 300 完成 20 日和 60 日超额收益比较。
- 量能与流动性：最新本地缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md) 显示，A 股长线与短线工作流当次均未筛出满足阈值的标的。
- 风险提示：当前空结果更可能来自筛选阈值偏严叠加数据链路中断，不能外推为 A 股整体缺乏趋势机会。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md)

## 3. 港股候选

### 三生制药（01530.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；缓存长线工作流综合分为 `6.00`。
- 趋势信号：缓存显示对应最新价 `25.32`、单日涨幅 `+11.84%`，仍属于港股长线工作流入选标的，但未能复核 `MA20 / MA60 / MA120` 多头结构。
- 动量信号：单日强势明显，但缺少 `RSI14 / MACD` 历史序列复核，无法判断是否已接近短期过热。
- 相对强弱：缓存未提供相对恒生指数的 20 日和 60 日超额收益，正式评分待联网后补齐。
- 量能与流动性：缓存显示换手率 `2.91%`、主力净流入约 `1.10 亿`、市值约 `642.62 亿`，流动性与承接优于多数中小市值港股。
- 风险提示：单日涨幅较大，若后续缺少板块跟随或回踩承接不足，容易退化为高波动情绪票。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md)

### 灵宝黄金（03330.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；缓存长线工作流综合分为 `6.00`。
- 趋势信号：缓存显示最新价 `28.50`、单日涨幅 `+10.47%`，属于港股长线工作流入选标的，但均线多头结构仍待正式确认。
- 动量信号：贵金属方向动量强，但缺少 `RSI14 / MACD` 复核，无法判断是趋势延续还是阶段性加速。
- 相对强弱：未能重新对照恒生指数完成 20 日和 60 日超额收益比较。
- 量能与流动性：缓存显示换手率 `2.73%`、主力净流入约 `0.60 亿`、市值约 `385.43 亿`，成交活跃度优于多数传统资源股。
- 风险提示：资源股对金价和地缘情绪敏感，若外部扰动缓和，回撤速度可能较快。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md)

### 康龙化成（03759.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；缓存长线工作流综合分为 `6.00`。
- 趋势信号：缓存显示最新价 `20.88`、单日涨幅 `+10.95%`，属于港股长线工作流入选标的，但未能复核 `MA20 / MA60 / MA120`。
- 动量信号：医药外包方向的单日动量较强，正式 `RSI14 / MACD` 判断待补齐。
- 相对强弱：未能重新对照恒生指数完成 20 日和 60 日超额收益比较。
- 量能与流动性：缓存显示换手率 `4.61%`、主力净流入约 `0.88 亿`、市值约 `382.11 亿`，量价活跃度高于多数防御型医药股。
- 风险提示：若后续板块共振不足，单日大阳线之后可能进入高波动消化阶段。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 规则复算。
- 趋势信号：本地缓存中的美股强势股主要是 `GABr`、`CYCN`、`ELAB` 一类极端波动标的，不符合中长期趋势基础要求。
- 动量信号：虽然缓存显示这些个股单日涨幅很大，但缺少完整历史日线与 `RSI14 / MACD` 复核，无法判断是否具备持续性。
- 相对强弱：未能重新对照标普 500 完成 20 日和 60 日超额收益比较。
- 量能与流动性：缓存显示部分个股换手率异常高，更接近事件驱动或投机性脉冲，不适合作为中长期观察池核心候选。
- 风险提示：按照 `SCORING.md` 的硬过滤规则，这类单日异常拉升标的大概率应被剔除或重罚。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md)

## 5. 风险提醒

- 当前核心风险仍是数据链路失效而不是市场本身；在未恢复外网行情源访问前，日报不能替代正式筛选结果。
- 本报告当前更适合作为执行日志和缓存观察记录，不等于直接买入建议；待联网后应重新计算均线、相对强弱、成交量、成交额、换手率、振幅、波动率和回撤，再决定是否保留上述港股观察名单。

## 6. 方法说明

- 目标方法：使用 `MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱，以及成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)，随后尝试运行 `python3 -m stock_market_skill.report_workflow --output tests/2026-04-03-market-workflow.md --top-n 3` 以获取最新三市场候选。
- 阻塞详情：工作流在 `EastMoneyAdapter._get_market_clist(...)` 阶段失败，抛出 `http.client.RemoteDisconnected: Remote end closed connection without response`，因此无法完成本轮正式复算。
- 备用依据：引用最新本地缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-02-market-workflow.md) 作为观察性补充，不替代正式技术评分。
