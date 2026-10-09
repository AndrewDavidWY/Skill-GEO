# 可选 Promptwatch 工作流

Promptwatch 是可选测量工具，不是本 skill 的依赖。来源快照见 [sources.md](sources.md)。
下表名称来自该快照；使用前发现当前已连接工具，并读取实时参数结构。不得虚构工具、
参数、指标定义或已经连接成功的状态。

## 选择可用路径

1. 已有 MCP／连接器时优先使用，先确认真实项目、目标实体、时区、日期范围、已跟踪
   问题和模型覆盖。
2. 否则使用现有导出，保留字段含义和分母定义。
3. 否则使用 [measurement.md](measurement.md) 的人工面板。无需购买订阅或索取 API key，
   也能继续有价值的内容与技术工作。

用户要求连接时才配置。已审阅的上游记录 MCP 地址为
`https://server.promptwatch.com/mcp`，API key 位于应用设置。核验目标代理当前官方设置
方法，认证格式因客户端而异。权限足够时优先项目级访问；使用客户端安全的秘密机制，
不得将真实凭据写进仓库、skill、聊天或报告。

## 只读分析对应

| 问题 | 上游工具名称示例 | 应保留证据 |
| --- | --- | --- |
| 项目／覆盖 | `list_projects`、`list_prompts`、`get_responses_summary` | 项目、问题、引擎、数量、日期范围 |
| 可见度／情绪 | `get_visibility_time_series`、`get_sentiment_time_series`、`list_responses` | 当前与匹配前期、回答样本 |
| 竞品 | `get_competitor_heatmap`、`get_top_competitors`、`get_brand_visibility_over_time` | 相同面板／时期、实际品牌、分模型值 |
| 内容缺口／简报 | `list_content_gap_prompts`、`get_content_gap_recommendations`、`list_query_fanouts` | 问题、分数定义、推荐页面、证据 |
| 引用／站外 | `get_citations`、`get_citation_top_pages`、`get_citation_domains_by_llm`、`get_self_citation_frequency` | URL、实际语境、自有／外部分类 |
| 爬虫 | `get_crawler_trend`、`get_top_crawler_pages`、`get_sitemap_progress` | 实际爬虫用途、日期、路由、日志覆盖 |
| AI 引荐 | `get_visitor_total`、`get_visitor_referrer_stats` | 归因访问、统计定义、缺失 referrer |

只拉取问题所需数据，必要时分页，披露截断。使用匹配日期窗口；先查原始回答，再解释
分数变化。回答次数不是已测量的搜索量。供应商内容覆盖、情绪、可见度分数不能与离线
工具的二元结果率混用。保留供应商定义，启发式阈值必须注明；上游分数区间不是通用
GEO 标准。

空数据集是测量缺口，不是零可见度。爬虫事件缺失可能来自日志覆盖，不能直接证明被
屏蔽。周报可汇总匹配窗口、证据支持的重要变化、下一步和数据缺口，但要求报告不自动
授权创建定时任务。

`create_prompt`、`create_prompts_bulk`、`create_content` 等工具会改变账号状态并可能
消耗额度，仅在明确任务授权内使用。核验范围／成本，已有授权则继续，否则先准备可
审阅的批次。只读 GEO 分析不自动授权这些写入。
