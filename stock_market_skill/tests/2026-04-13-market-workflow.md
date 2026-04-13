# 2026-04-13 多市场长短线买入推荐工作流测试

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

- 十大券商策略：震荡反复后A股有望再起攻势 投资主线有哪些？
- 中信证券：XPO重构可插拔范式 拥抱光互联升级浪潮
- 华泰证券：预计股市波动将对保险公司一季度利润表现形成一定压力
- 华泰证券：美以伊冲突致化工品普涨 若局势趋稳 看好化工景气提升

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## A股短线推荐

### 指标设计

- 涨跌幅强度优先，但不过分追求极端强势
- 换手率明显放大，允许中等活跃度进入观察
- 主力净流入优先，不再作为唯一硬门槛
- 更适合盘中强势跟踪，不适合中线持有

### 相关新闻

- 十大券商策略：震荡反复后A股有望再起攻势 投资主线有哪些？
- 中信证券：XPO重构可插拔范式 拥抱光互联升级浪潮
- 华泰证券：预计股市波动将对保险公司一季度利润表现形成一定压力
- 华泰证券：美以伊冲突致化工品普涨 若局势趋稳 看好化工景气提升

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 港股长线推荐

### 指标设计

- 优先大市值和流动性更好的龙头
- PE(TTM) 保持在相对合理区间
- 更关注估值与行业地位，而不是单日弹性
- 过滤单日过热的情绪票

### 相关新闻

- I Asked ChatGPT the Best Way To Claim Social Security — Then Had a Retirement Planner Review It
- Rimini Street (RMNI) Enters Into a Multi-Year Partnership With South Korea’s Lotte Rental
- Her is What Makes Blend Labs (BLND) Appear so Attractive
- HIVE Digital (HIVE) Betting Big on AI Data Centers

### 推荐列表

#### 1. 中信证券（06030.HK）

- 行业：其他金融
- 最新价：26.90
- 涨跌幅：+8.29%
- 换手率：2.22%
- 主力净流入：0.56亿
- PE(TTM)：11.97
- 市值：3986.73亿
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

- It's Time to Take Profits on These 2 Overbought Energy Stocks
- Weave Communications (WEAV) Acknowledges Partnership With Minted Technology Advisors
- HIVE Digital (HIVE) Betting Big on AI Data Centers
- Rimini Street (RMNI) Enters Into a Multi-Year Partnership With South Korea’s Lotte Rental

### 推荐列表

#### 1. 中国前沿科技集团（01661.HK）

- 行业：旅游及消闲设施
- 最新价：3.24
- 涨跌幅：+89.47%
- 换手率：4.48%
- 主力净流入：0.01亿
- PE(TTM)：-17.01
- 市值：6.17亿
- 综合分：6.40
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. 滴普科技（01384.HK）

- 行业：软件服务
- 最新价：44.60
- 涨跌幅：+48.77%
- 换手率：20.07%
- 主力净流入：0.62亿
- PE(TTM)：-14.08
- 市值：145.68亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. 国泰君安国际（01788.HK）

- 行业：其他金融
- 最新价：3.09
- 涨跌幅：+27.69%
- 换手率：18.56%
- 主力净流入：1.79亿
- PE(TTM)：21.89
- 市值：294.48亿
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

- JBS Reaches Labor Deal With Striking Meatpacking Workers
- Oil prices spike after failed US-Iran peace talks and Trump's blockade of the Strait of Hormuz
- Oil bounces back above $100 after US, Iran talks end in stalemate
- Oil prices surge above $100 as U.S. Navy to blockade Iran's ports after peace talks fail

### 推荐列表

- 今日未筛出满足当前阈值的推荐标的。

## 美股短线推荐

### 指标设计

- 优先高动量个股
- 允许更高波动，但只适合交易型策略
- 关注当日资金与热度是否同步
- 避免把超高波动票误当成长线标的

### 相关新闻

- JBS Reaches Labor Deal With Striking Meatpacking Workers
- Oil prices spike after failed US-Iran peace talks and Trump's blockade of the Strait of Hormuz
- Oil bounces back above $100 after US, Iran talks end in stalemate
- Oil prices surge above $100 as U.S. Navy to blockade Iran's ports after peace talks fail

### 推荐列表

#### 1. Fusemachines Inc（FUSE）

- 行业：信息技术
- 最新价：1.83
- 涨跌幅：+115.29%
- 换手率：438.48%
- 主力净流入：0.03亿
- PE(TTM)：-57.07
- 市值：0.53亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 2. 雷亚电子（RAYA）

- 行业：公用事业
- 最新价：0.95
- 涨跌幅：+107.94%
- 换手率：4301.53%
- 主力净流入：0.02亿
- PE(TTM)：-16.27
- 市值：0.09亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。

#### 3. Smart Powerr Corp（CREG）

- 行业：工业
- 最新价：0.63
- 涨跌幅：+85.41%
- 换手率：1923.05%
- 主力净流入：0.00亿
- PE(TTM)：-5.00
- 市值：0.14亿
- 综合分：8.50
- 推荐理由：动量较强, 换手活跃, 资金助推
- 入手时机：适合只在强势分时回踩不破均线时轻仓跟随，失速就不追。
