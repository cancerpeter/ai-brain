# 2026-04-14 多市场长短线买入推荐工作流测试

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

- 中信证券：重点推荐所有电子布公司
- 华泰证券：预计今年全国房价二阶导有望转正 建议逐步布局地产股
- 华泰证券：白酒行业供需重构修复渐明 围绕三条主线布局
- 中信建投：当前上市险企估值水平仍有较高安全边际 长期配置价值显著

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## A股短线推荐

### 指标设计

- 涨跌幅强度优先，但不过分追求极端强势
- 换手率明显放大，允许中等活跃度进入观察
- 主力净流入优先，不再作为唯一硬门槛
- 更适合盘中强势跟踪，不适合中线持有

### 相关新闻

- 中信证券：重点推荐所有电子布公司
- 华泰证券：预计今年全国房价二阶导有望转正 建议逐步布局地产股
- 华泰证券：白酒行业供需重构修复渐明 围绕三条主线布局
- 中信建投：当前上市险企估值水平仍有较高安全边际 长期配置价值显著

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股长线推荐

### 指标设计

- 优先大市值和流动性更好的龙头
- PE(TTM) 保持在相对合理区间
- 更关注估值与行业地位，而不是单日弹性
- 过滤单日过热的情绪票

### 相关新闻

- There's no 'exit tax,' but these states can still cost you when you leave
- Why Needham Analysts Slashed Their Price Targets on IBM Stock Ahead of Earnings
- Snowflake (SNOW) Plunges 31% This Year, But Analysts See 60% Upside Today
- CrowdStrike Is Joining Anthropic’s New Project Glasswing. Does That Make CRWD Stock a Buy?

### 推荐列表

#### 1. 中国重汽（03808.HK）

- 行业：工业工程
- 最新价：47.44
- 涨跌幅：+7.23%
- 换手率：0.49%
- 主力净流入：-0.48亿
- PE(TTM)：16.85
- 市值：1309.82亿
- 综合分：4.00
- 推荐理由：港股龙头属性更强, 估值相对可控
- 入手时机：更适合等回踩或横盘消化后分批介入，不建议追高。

#### 2. 建滔积层板（01888.HK）

- 行业：工业工程
- 最新价：24.56
- 涨跌幅：+10.33%
- 换手率：1.58%
- 主力净流入：1.22亿
- PE(TTM)：31.53
- 市值：770.04亿
- 综合分：6.00
- 推荐理由：港股龙头属性更强, 估值相对可控, 资金面偏正
- 入手时机：更适合等回踩或横盘消化后分批介入，不建议追高。

## 港股短线推荐

### 指标设计

- 优先筛选价格动量更强的活跃股
- 换手率明显放大
- 允许更高弹性，但不追求无限制拉升
- 更适合快进快出

### 相关新闻

- There's no 'exit tax,' but these states can still cost you when you leave
- Why Needham Analysts Slashed Their Price Targets on IBM Stock Ahead of Earnings
- Snowflake (SNOW) Plunges 31% This Year, But Analysts See 60% Upside Today
- CrowdStrike Is Joining Anthropic’s New Project Glasswing. Does That Make CRWD Stock a Buy?

### 推荐列表

#### 1. 乐享集团（06988.HK）

- 行业：媒体及娱乐
- 最新价：0.16
- 涨跌幅：+98.75%
- 换手率：6.84%
- 主力净流入：0.01亿
- PE(TTM)：-2.33
- 市值：3.77亿
- 综合分：6.87
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. 滴普科技（01384.HK）

- 行业：软件服务
- 最新价：71.00
- 涨跌幅：+59.19%
- 换手率：20.16%
- 主力净流入：0.51亿
- PE(TTM)：-22.41
- 市值：231.91亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. 不同集团（06090.HK）

- 行业：家庭电器及用品
- 最新价：49.98
- 涨跌幅：+43.54%
- 换手率：29.32%
- 主力净流入：0.09亿
- PE(TTM)：62.51
- 市值：45.12亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

## 美股长线推荐

### 指标设计

- 优先中大市值公司
- PE(TTM) 为正且不过热
- 更重视企业规模和估值约束
- 避免单日过度情绪化拉升个股

### 相关新闻

- Exclusive: United CEO Kirby raised potential tie-up with American in Trump meeting
- Target Leverages Shipt to Scale Next-Day Delivery
- An Amazon warehouse worker died on the job at Oregon facility
- Gold Edges Higher Amid Dollar Weakness

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 美股短线推荐

### 指标设计

- 优先高动量个股
- 允许更高波动，但只适合交易型策略
- 关注当日资金与热度是否同步
- 避免把超高波动票误当成长线标的

### 相关新闻

- Exclusive: United CEO Kirby raised potential tie-up with American in Trump meeting
- Target Leverages Shipt to Scale Next-Day Delivery
- An Amazon warehouse worker died on the job at Oregon facility
- Gold Edges Higher Amid Dollar Weakness

### 推荐列表

#### 1. Real Messenger Corp-A（RMSG）

- 行业：工业
- 最新价：2.70
- 涨跌幅：+475.08%
- 换手率：9705.26%
- 主力净流入：0.05亿
- PE(TTM)：-4.12
- 市值：0.24亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. Real Messenger Corp Wt（RMSGW）

- 行业：-
- 最新价：0.11
- 涨跌幅：+450.00%
- 换手率：0.00%
- 主力净流入：0.00亿
- PE(TTM)：0.00
- 市值：0.00亿
- 综合分：5.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. NextPlat Corp Wt（NXPLW）

- 行业：-
- 最新价：0.01
- 涨跌幅：+204.00%
- 换手率：0.00%
- 主力净流入：0.00亿
- PE(TTM)：0.00
- 市值：0.00亿
- 综合分：4.00
- 推荐理由：动量较强, 换手活跃
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。
