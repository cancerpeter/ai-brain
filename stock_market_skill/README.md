# Stock Market Skill

一个轻量、可复用的股票行情 skill / 工具封装项目，用于统一封装现有插件能力，完成自然语言请求的意图识别、工具路由、统一输出和轻量摘要。

## 项目目标

- 对自然语言请求做规则化意图识别与路由
- 自动选择合适的行情 / 新闻 / 榜单 / 汇率工具
- 统一输入输出格式，避免上层直接消费原始 JSON
- 方便后续接入 Coze、workflow、agent skill
- 保持实现轻量、可维护、易扩展

## 当前支持能力

- A 股实时行情
- 港股实时行情
- 美股实时行情
- 日 K 数据
- 分时 / 分钟线数据
- 实时财经新闻
- 跨站财经新闻汇总
- 涨跌幅榜
- 净流入榜
- 换手率榜
- A 股全市场条件筛选
- 长线候选筛选工具
- 中长线候选筛选工具
- 短线候选筛选工具
- 三市场长短线推荐 md 工作流
- 人民币兑外币汇率

## 目录结构

```text
stock_market_skill/
├── AGENTS.md
├── README.md
├── examples.md
├── skill.md
├── stock_market_skill
│   ├── __init__.py
│   ├── formatter.py
│   ├── main.py
│   ├── models.py
│   ├── plugin_client.py
│   ├── router.py
│   └── source_adapters.py
└── tests
    └── test_router.py
```

## 设计概览

项目采用三层轻量结构：

1. `router.py`
   负责从自然语言中识别意图，返回标准化的 `RouteResult`
2. `plugin_client.py`
   负责统一封装底层插件能力，支持私有插件网关与公共行情源两类接入
3. `source_adapters.py`
   负责站点级适配，当前内置 EastMoney、Yahoo Finance、StockAnalysis
4. `formatter.py`
   负责将结构化结果整理成统一、可读、适合 skill / agent 输出的文本

## 如何运行

在项目根目录执行：

```bash
cd /Users/peter.chen/Documents/知识库搭建/stock_market_skill
python3 -m stock_market_skill.main "查腾讯港股实时价"
```

## 如何接入真实行情插件

默认情况下项目使用 mock 数据，便于本地开发。

如果要切到真实插件，请至少配置：

```bash
export STOCK_SKILL_USE_MOCK=0
export STOCK_SKILL_PLUGIN_BASE_URL="https://your-plugin-gateway.example.com"
export STOCK_SKILL_PLUGIN_API_KEY="your-api-key"
```

如果各工具路径不是默认的 `/GetXxx`，可单独覆盖：

```bash
export STOCK_SKILL_PATH_GETLIVENEWS="/plugin/GetLiveNews"
export STOCK_SKILL_PATH_GETSINASTOCKDATA="/plugin/GetSinaStockData"
export STOCK_SKILL_PATH_GETQQSTOCKDATA="/plugin/GetQQStockData"
export STOCK_SKILL_PATH_GETHKSTOCKDATA="/plugin/GetHKStockData"
export STOCK_SKILL_PATH_GETKLINEDAYSTOCKDATA="/plugin/GetKLineDayStockData"
export STOCK_SKILL_PATH_GETKLINETIMESTOCKDATA="/plugin/GetKLineTimeStockData"
export STOCK_SKILL_PATH_GETEXCHANGERATE="/plugin/GetExchangeRate"
export STOCK_SKILL_PATH_GETCHANGEPERCENTLIST="/plugin/GetChangePercentList"
export STOCK_SKILL_PATH_GETNETINFLOWRATELIST="/plugin/GetNetInflowRateList"
export STOCK_SKILL_PATH_GETTURNOVERRATIOLIST="/plugin/GetTurnoverRatioList"
```

如需补充请求头，可设置：

```bash
export STOCK_SKILL_PLUGIN_HEADERS='{"X-App-Id":"demo","X-Env":"prod"}'
```

说明：

- 当前真实接入方式为标准 HTTP `POST` JSON
- 请求体默认直接发送路由后的参数，如 `{"symbol":"600519"}` 或 `{"count":10}`
- 响应优先读取 `{"data": ...}`，也兼容直接返回对象或列表
- A 股实时行情默认先调 `GetSinaStockData`，失败后自动回退 `GetQQStockData`
- 如果你的插件返回字段名不完全一致，可以继续在 `plugin_client.py` 里扩展字段映射

## 公共行情源设计

当前版本也支持直接从公共站点取数：

- A 股：`https://data.eastmoney.com`
- 港股：`https://finance.yahoo.com`
- 美股：`https://stockanalysis.com`

对应代码中的默认来源：

- A 股实时 / 日 K / 分时 / 新闻 / 排行：`EastMoneyAdapter`
- A 股全市场筛选：`EastMoneyAdapter`
- 港股全市场筛选：`EastMoneyAdapter` 市场快照
- 美股全市场筛选：`EastMoneyAdapter` 市场快照
- 长线候选工具：大市值 / 估值约束 / 适中换手 / 主力净流入
- 中长线候选工具：新闻主题共振 / 估值不过热 / 主力净流入 / 市值与换手结构
- 短线候选工具：涨幅强度 / 高换手 / 主力净流入 / 动量排序
- 港股实时 / 日 K / 分时：`YahooFinanceAdapter`
- 汇率：`Yahoo Finance` chart backend
- 美股实时：`StockAnalysisAdapter`
- 跨站新闻汇总：`EastMoney + Yahoo Finance + StockAnalysis`

推荐配置：

```bash
export STOCK_SKILL_SOURCE_MODE=public
export STOCK_SKILL_USE_MOCK=0
```

说明：

- `STOCK_SKILL_SOURCE_MODE=auto`：若未配置私有插件网关，则优先走公共源
- `STOCK_SKILL_SOURCE_MODE=public`：强制优先走公共源
- `STOCK_SKILL_SOURCE_MODE=plugin`：强制只走你的私有插件网关
- 当前默认配置已经偏向真实事件源，不再默认走 mock
- 公共站点页面和接口可能变化，`source_adapters.py` 预期会持续维护

## 长线与短线工具设计

### 长线候选工具

工具名：`ScreenLongTermStocks`

核心指标：

- 最小市值
- PE(TTM) 上限
- 适中换手率
- 主力净流入为正

适用场景：

- 从 A 股里先找相对稳健、容量更大的候选池
- 适合做中长线观察名单，不直接等同于买入信号
- 当前也支持港股、美股，但港美股筛选更偏全市场快照口径

### 中长线候选工具

工具名：`ScreenMidLongTermStocks`

核心指标：

- 当日新闻主题与行业共振
- PE(TTM) 不过热
- 主力净流入为正
- 中大市值优先
- 换手不过热

适用场景：

- 更适合做 1 到 6 个月维度的候选池，而不是追单日最强涨幅
- 适合把新闻主线、资金流向和估值约束放到一起看
- 当前优先对 A 股效果更完整

### 短线候选工具

工具名：`ScreenShortTermStocks`

核心指标：

- 涨跌幅强度
- 较高换手率
- 主力净流入为正
- 按动量优先排序

适用场景：

- 盘中强势股初筛
- 更适合短线节奏研究，不适合直接当成长线池
- 当前也支持港股、美股，但港美股的换手/资金字段可得性弱于 A 股

查看更多示例：

```bash
python3 -m stock_market_skill.main "看一下人民币兑美元汇率"
python3 -m stock_market_skill.main "给我最新财经新闻，5条"
python3 -m stock_market_skill.main "查贵州茅台日K"
```

运行测试：

```bash
cd /Users/peter.chen/Documents/知识库搭建/stock_market_skill
python3 -m unittest discover -s tests
```

## 生成推荐 md 工作流

如果你想一次性输出 A 股、港股、美股的长线与短线推荐 md，可直接运行：

```bash
cd /Users/peter.chen/Documents/知识库搭建/stock_market_skill
python3 -m stock_market_skill.report_workflow --output tests/2026-04-01-market-workflow.md --top-n 3
```

工作流会自动生成：

- A 股长线推荐
- A 股短线推荐
- 港股长线推荐
- 港股短线推荐
- 美股长线推荐
- 美股短线推荐

每个部分都会包含：

- 市场相关新闻
- 推荐股票列表
- 推荐理由
- 入手时机

当前工作流会先读取：

- `workflow_strategy.md`

这份文档中已经明确拆分了：

- A 股长线指标
- A 股短线指标
- 港股长线指标
- 港股短线指标
- 美股长线指标
- 美股短线指标

如果你要改任务逻辑，优先改文档里的 JSON 配置，而不是直接改脚本。

## 如何扩展新工具

新增工具时，建议按下面步骤接入：

1. 在 `models.py` 中补充对应的数据模型
2. 在 `plugin_client.py` 中新增统一方法封装
3. 在 `router.py` 中补充意图规则和参数抽取逻辑
4. 在 `formatter.py` 中新增该结果类型的输出格式
5. 在 `examples.md` 中增加调用示例
6. 在 `tests/` 中补充路由与格式化测试

## 如何接入 Coze / Skill / Workflow

- Coze / agent skill:
  可把 `main.py` 作为最小演示入口，把 `route_query -> plugin_client -> formatter` 这条链路改造成服务函数或 tool handler
- Workflow:
  可将 `router.py` 的输出作为前置节点，把 `tool_name` 和 `params` 交给后续插件节点执行
- Skill:
  可直接复用 `skill.md` 作为规则说明，把 `formatter.py` 产出的文本作为最终回答

## 当前假设与边界

- 当前版本已支持真实 HTTP 插件接入，也支持从 EastMoney / Yahoo Finance / StockAnalysis 直接取数
- 当前版本优先做规则路由，不引入模型推理和复杂解析器
- 当前版本默认 A 股实时行情优先选择 `GetSinaStockData`，后续可扩展失败回退到 `GetQQStockData`
- 当前版本对“股票名称解析”为轻量实现，只做少量内置映射与代码模式识别，不做完整证券主数据检索
