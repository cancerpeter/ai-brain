# 2026-04-03 多市场长短线买入推荐工作流测试

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
- 主力净流入为正
- 换手率处于健康区间，避免极端情绪票

### 相关新闻

- 中信证券：算力涨价扩散 关注一季报超预期三条线索
- 中原证券：4月A股市场或以震荡为主 聚焦红利防御与能源安全主线
- 中信证券：创新药行业进入密集数据催化期 建议重点关注
- 华泰证券：中东局势扰动市场风险偏好 红利仍然具备底仓价值

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## A股短线推荐

### 指标设计

- 涨跌幅强度优先
- 换手率明显放大
- 主力净流入为正
- 更适合盘中强势跟踪，不适合中线持有

### 相关新闻

- 中信证券：算力涨价扩散 关注一季报超预期三条线索
- 中原证券：4月A股市场或以震荡为主 聚焦红利防御与能源安全主线
- 中信证券：创新药行业进入密集数据催化期 建议重点关注
- 华泰证券：中东局势扰动市场风险偏好 红利仍然具备底仓价值

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股长线推荐

### 指标设计

- 优先大市值和流动性更好的龙头
- PE(TTM) 保持在相对合理区间
- 更关注估值与行业地位，而不是单日弹性
- 过滤单日过热的情绪票

### 相关新闻

- Seagate And Western Digital Rallies Cooled In March. But Wall Street Says AI Demand 'Robust.'
- Greystone (GHI) Q4 2025 Earnings Call Transcript
- BP's New CEO Pledges Consistency as Company Tries to Rebuild Investor Trust
- Should You Buy Micron Stock After Its 32% Decline?

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股短线推荐

### 指标设计

- 优先筛选价格动量更强的活跃股
- 换手率明显放大
- 允许更高弹性，但不追求无限制拉升
- 更适合快进快出

### 相关新闻

- Seagate And Western Digital Rallies Cooled In March. But Wall Street Says AI Demand 'Robust.'
- Greystone (GHI) Q4 2025 Earnings Call Transcript
- BP's New CEO Pledges Consistency as Company Tries to Rebuild Investor Trust
- Should You Buy Micron Stock After Its 32% Decline?

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 美股长线推荐

### 指标设计

- 优先中大市值公司
- PE(TTM) 为正且不过热
- 更重视企业规模和估值约束
- 避免单日过度情绪化拉升个股

### 相关新闻

- Microsoft executive touts Copilot sales traction as AI anxiety weighs on stock
- Why OpenAI Decided to Buy TBPN, Tech's Hottest News Show
- Amazon to Add 3.5% Fulfillment Surcharge as Fuel Costs Rise
- The Wealthy Investors That Powered Private Credit Are Rushing for the Exits

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 美股短线推荐

### 指标设计

- 优先高动量个股
- 允许更高波动，但只适合交易型策略
- 关注当日资金与热度是否同步
- 避免把超高波动票误当成长线标的

### 相关新闻

- Microsoft executive touts Copilot sales traction as AI anxiety weighs on stock
- Why OpenAI Decided to Buy TBPN, Tech's Hottest News Show
- Amazon to Add 3.5% Fulfillment Surcharge as Fuel Costs Rise
- The Wealthy Investors That Powered Private Credit Are Rushing for the Exits

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。
