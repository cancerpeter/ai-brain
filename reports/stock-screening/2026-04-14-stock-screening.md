# 2026-04-14 股票筛选日报

更新日期：2026-04-14
数据口径：计划以上一交易日 2026-04-13 收盘数据为主，结合历史日线计算技术指标，不构成投资建议。本次运行已按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md) 读取流程，并生成候选池文件 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)。但 `push2his.eastmoney.com` 与 `query1.finance.yahoo.com` 的历史日线请求仍返回 `nodename nor servname provided, or not known`，因此无法按 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md) 正式复算 `MA20 / MA60 / MA120 / RSI14 / MACD / 相对基准强弱 / 成交量均值 / 振幅 / 波动率 / 回撤`。以下结论以本轮候选池、硬过滤规则与流动性约束结合后的观察结果为主，不替代正式技术评分。

## 1. 今日结论

- 面向 2026-04-13 收盘数据的正式三市场技术筛选本轮仍未完成，根因仍是 A 股、港股、美股历史日线接口 DNS 解析失败，而不是规则或模板缺失。
- A 股在当前纪律下依旧没有可保留的正式观察对象；港股相对更强，但长线方向只有中国重汽、建滔积层板接近中期观察逻辑，短线高弹性样本大多波动过高；美股长线池为空，短线池继续被极小市值脉冲股主导，不适合中长期跟踪。

## 2. A 股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-13 数据正式复算。
- 趋势信号：本轮候选池中 A 股长线、短线均为空，且历史日线请求失败，无法确认 `MA20 / MA60 / MA120` 结构。
- 动量信号：无法正式计算 `RSI14 / MACD`。
- 相对强弱：未能对照沪深 300 计算 20 日、60 日超额收益。
- 量能与流动性：在现有纪律下没有可通过流动性与趋势初筛的 A 股标的，不宜为了填充名单而放宽标准。
- 风险提示：若数据链路恢复后仍无候选，说明市场更可能处于结构分化或趋势确认不足阶段，应接受空仓观察而非强行选股。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)

## 3. 港股候选

### 中国重汽（03808.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `4.00`。
- 趋势信号：候选池显示最新价 `47.44`、单日涨幅 `+7.23%`，具备较大市值和正盈利基础，在本轮港股长线样本中更接近稳态趋势观察逻辑，但 `MA20 / MA60 / MA120` 仍待正式补算。
- 动量信号：价格动量偏强，但缺少 `RSI14 / MACD` 历史序列，无法判断是否已进入短期加速末端。
- 相对强弱：未能正式对照恒生指数完成 20 日与 60 日超额收益比较。
- 量能与流动性：换手率 `0.49%`、市值约 `1309.82 亿`，容量较好，但主力净流入约 `-0.48 亿`，说明当天资金并非单边强化。
- 风险提示：若后续没有量能跟进，单日上涨更可能只是阶段性脉冲，正式评分恢复后不一定能维持高优先级。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)

### 建滔积层板（01888.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `6.00`。
- 趋势信号：候选池显示最新价 `24.56`、单日涨幅 `+10.33%`，兼具正盈利、较好市值与正向资金流，在本轮港股长线名单里是更均衡的观察对象，但中期均线结构仍需历史日线确认。
- 动量信号：价格动量较强，但 `RSI14 / MACD` 暂缺，无法判断是否接近短线过热。
- 相对强弱：相对恒生指数大概率偏强，但本轮不能完成正式超额收益记分。
- 量能与流动性：换手率 `1.58%`、主力净流入约 `1.22 亿`、市值约 `770.04 亿`，在本轮港股候选中流动性与容量较平衡。
- 风险提示：单日涨幅已经不小，更适合等待回踩或横盘消化后的承接确认，不适合把当天强势直接视为低风险买点。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)

### 滴普科技（01384.HK）

- 综合评分：暂未按 `SCORING.md` 正式复算；候选工作流综合分为 `8.50`。
- 趋势信号：候选池显示最新价 `71.00`、单日涨幅 `+59.19%`，方向极强，但更偏事件驱动和高弹性交易，不宜直接视为稳定中期趋势样本。
- 动量信号：单日动量极强，但没有 `RSI14 / MACD` 复核，难以判断短线是否已经严重透支。
- 相对强弱：相对恒生指数显著占优的概率较高，但仍无法完成正式超额收益比较。
- 量能与流动性：换手率 `20.16%`、主力净流入约 `0.51 亿`、市值约 `231.91 亿`，活跃度充足，但负 `PE(TTM)` 说明它更接近题材交易标的。
- 风险提示：高涨幅、高换手、负盈利三者叠加，不符合中长期硬过滤的稳态特征，正式评分恢复后更可能被降权甚至剔除。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)

## 4. 美股候选

### 暂无正式候选

- 综合评分：暂缺，未能按 `SCORING.md` 对 2026-04-13 数据正式复算。
- 趋势信号：本轮美股长线候选为空；短线候选中的 `RMSG`、`RMSGW`、`NXPLW` 均属于极小市值高波动样本，不符合中长期趋势基础要求。
- 动量信号：候选池显示这些标的单日涨幅很高，但缺少完整历史日线与 `RSI14 / MACD` 复核，更像事件驱动脉冲。
- 相对强弱：未能正式对照标普 500 完成 20 日和 60 日超额收益比较。
- 量能与流动性：极高换手与极小市值的组合意味着滑点、回撤和失真风险都很高，按硬过滤规则应重罚或直接剔除。
- 风险提示：当前可见的美股强势样本更适合交易型观察，不适合作为中长期观察池核心候选。
- 来源：[`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md)

## 5. 风险提醒

- 当前最大风险仍是历史日线链路不完整，导致无法对 2026-04-13 这一前一交易日完成正式技术指标复算。
- 港股虽然出现了可观察样本，但除中国重汽、建滔积层板外，其余强势股大多兼具高涨幅、高换手或负盈利特征，正式历史日线恢复后未必能够保留在中长期观察名单中。
- 本报告是技术筛选与研究线索，不等于直接买入建议；对单日涨幅异常、换手过高或数据字段缺失的标的，应优先防止把情绪脉冲误判为中期趋势。

## 6. 方法说明

- 使用目标：`MA20 / MA60 / MA120`、`RSI14 / MACD`、相对对应市场基准指数的强弱、成交量、成交额、换手率、振幅、波动率和回撤。
- 本次实际执行：先读取 [`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/README.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/SCORING.md)、[`/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md`](/Users/peter.chen/Documents/知识库搭建/workflows/stock-screening/TEMPLATE.md)，随后执行 `python3 -m stock_market_skill.report_workflow --output /Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md --top-n 3` 生成三市场候选池。
- 阻塞详情：单独测试 `600519`、`0700.HK`、`AAPL` 与 `^GSPC` 的历史日线请求时，分别命中 `https://push2his.eastmoney.com/api/qt/stock/kline/get?...` 与 `https://query1.finance.yahoo.com/v8/finance/chart/...` 的 DNS 解析失败，错误均为 `nodename nor servname provided, or not known`。
- 备用依据：引用本轮成功生成的候选池缓存 [`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md`](/Users/peter.chen/Documents/知识库搭建/stock_market_skill/tests/2026-04-14-market-workflow.md) 作为观察性补充，不替代正式技术评分。
