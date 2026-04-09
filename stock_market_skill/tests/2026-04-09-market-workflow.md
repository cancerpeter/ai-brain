# 2026-04-09 多市场长短线买入推荐工作流测试

## 说明

- 本文档由工作流自动生成。
- 当前任务先读取策略文档：`/Users/peter.chen/Documents/知识库搭建/stock_market_skill/workflow_strategy.md`。
- 每个市场分成长线与短线两类推荐。
- 长线更看重估值、资金、规模与新闻背景。
- 短线更看重涨跌幅强度、换手率、资金动量与盘中热度。

## A股长线推荐

### 指标设计

- 大中市值优先，避免纯小票博弈
- PE(TTM) 为正且不过热
- 主力净流入优先，但不过度作为硬性门槛
- 换手率处于健康区间，允许轻度放宽以提高覆盖率

### 相关新闻

- 中信证券：伊朗局势的战略方向正在逐渐清晰 全球风险资产的预期锚也将随之明确
- 国盛证券：随着AI算力持续扩张等 滤光片需求弹性显著放大
- 中信建投：若美股出现又一波下跌 建议积极增持
- 中信建投：军工板块业绩分化 关注军转民投资机会

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## A股短线推荐

### 指标设计

- 涨跌幅强度优先，但不过分追求极端强势
- 换手率明显放大，允许中等活跃度进入观察
- 主力净流入优先，不再作为唯一硬门槛
- 更适合盘中强势跟踪，不适合中线持有

### 相关新闻

- 中信证券：伊朗局势的战略方向正在逐渐清晰 全球风险资产的预期锚也将随之明确
- 国盛证券：随着AI算力持续扩张等 滤光片需求弹性显著放大
- 中信建投：若美股出现又一波下跌 建议积极增持
- 中信建投：军工板块业绩分化 关注军转民投资机会

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股长线推荐

### 指标设计

- 优先大市值和流动性更好的龙头
- PE(TTM) 保持在相对合理区间
- 更关注估值与行业地位，而不是单日弹性
- 过滤单日过热的情绪票

### 相关新闻

- This $599 MacBook Could Be Apple's Smartest Move Yet
- TCW Relative Value Mid Cap Fund Exited Flex Limited (FLEX) Due to End Market Uncertainty
- Intel joins Musk's Terafab AI chip project to power humanoid, data center goals
- TCW Exited Seagate Technology Holdings PL (STX) in Q4

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股短线推荐

### 指标设计

- 优先筛选价格动量更强的活跃股
- 换手率明显放大
- 允许更高弹性，但不追求无限制拉升
- 更适合快进快出

### 相关新闻

- This $599 MacBook Could Be Apple's Smartest Move Yet
- TCW Relative Value Mid Cap Fund Exited Flex Limited (FLEX) Due to End Market Uncertainty
- Intel joins Musk's Terafab AI chip project to power humanoid, data center goals
- TCW Exited Seagate Technology Holdings PL (STX) in Q4

### 推荐列表

#### 1. 意力国际（00585.HK）

- 行业：其他金融
- 最新价：1.83
- 涨跌幅：+92.63%
- 换手率：17.47%
- 主力净流入：1.21亿
- PE(TTM)：-332.55
- 市值：15.19亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. 环球战略集团（08007.HK）

- 行业：公用事业
- 最新价：0.48
- 涨跌幅：+83.02%
- 换手率：10.24%
- 主力净流入：0.05亿
- PE(TTM)：-4.89
- 市值：0.91亿
- 综合分：7.55
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. 嘉艺控股（01025.HK）

- 行业：纺织及服饰
- 最新价：0.34
- 涨跌幅：+39.68%
- 换手率：10.01%
- 主力净流入：0.04亿
- PE(TTM)：-4.24
- 市值：1.40亿
- 综合分：7.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

## 美股长线推荐

### 指标设计

- 优先中大市值公司
- PE(TTM) 为正且不过热
- 更重视企业规模和估值约束
- 避免单日过度情绪化拉升个股

### 相关新闻

- FedEx reaches tentative wage deal with pilots after years of talks
- Disney plans to cut 1,000 jobs, WSJ reports
- Federal Court Denies Anthropic's Motion to Lift ‘Supply Chain Risk' Label
- Disney Planning Layoffs Under New CEO D'Amaro

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 美股短线推荐

### 指标设计

- 优先高动量个股
- 允许更高波动，但只适合交易型策略
- 关注当日资金与热度是否同步
- 避免把超高波动票误当成长线标的

### 相关新闻

- FedEx reaches tentative wage deal with pilots after years of talks
- Disney plans to cut 1,000 jobs, WSJ reports
- Federal Court Denies Anthropic's Motion to Lift ‘Supply Chain Risk' Label
- Disney Planning Layoffs Under New CEO D'Amaro

### 推荐列表

#### 1. 优品车（UCAR）

- 行业：非日常生活消费品
- 最新价：2.38
- 涨跌幅：+331.63%
- 换手率：6357.69%
- 主力净流入：0.01亿
- PE(TTM)：-1.86
- 市值：0.12亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. Neuberger Berman High Yield Str（NHSr）

- 行业：-
- 最新价：0.01
- 涨跌幅：+131.67%
- 换手率：0.00%
- 主力净流入：-0.00亿
- PE(TTM)：0.00
- 市值：0.00亿
- 综合分：4.00
- 推荐理由：动量较强, 换手活跃
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. ReNew Energy Global plc Wt（RNWWW）

- 行业：-
- 最新价：0.01
- 涨跌幅：+120.59%
- 换手率：0.00%
- 主力净流入：-0.00亿
- PE(TTM)：0.00
- 市值：0.00亿
- 综合分：4.00
- 推荐理由：动量较强, 换手活跃
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。
