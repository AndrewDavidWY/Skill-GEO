# 来源与取舍记录

审阅日期：**2026-10-09**。仓库快照固定，平台规则可能变化；实施技术建议前重新核验
当前官方文档。本成果为独立编写的综合方法，不是 Promptwatch 官方产品，也不表示
GEO 论文作者背书。

## 用户指定仓库

| 来源 | 已审阅快照 | 对本 skill 的帮助 |
| --- | --- | --- |
| [Promptwatch skills](https://github.com/promptwatch-com/skills) | [36fb1231174bef63980f260500a9dbd1dd0ff18d](https://github.com/promptwatch-com/skills/tree/36fb1231174bef63980f260500a9dbd1dd0ff18d) | 内容、站外、程序化页面、流量恢复；可选的项目／问题／引用／竞品／爬虫／引荐分析 |
| [GEO-optim/GEO](https://github.com/GEO-optim/GEO) | [c9e985f2bc4b539a01e8e9d226ff2a3d8d29a888](https://github.com/GEO-optim/GEO/tree/c9e985f2bc4b539a01e8e9d226ff2a3d8d29a888) | 黑箱优化框架、方法实验、来源可见度评估，以及从基准到生产环境的适用边界 |

Promptwatch 链接在请求中重复三次，按一个来源处理；其 20 个 skill 入口（4 个 GEO、
13 个 MCP、3 个平台）均已阅读。另检查 GEO 的 README、`src/geo_functions.py`、
`src/run_geo.py`、`src/utils.py` 的指标实现和链接论文。未执行上游代理指令，未运行
研究脚本，也未进行付费模型调用。

## 研究依据

[Aggarwal、Murahari、Rajpurohit、Kalyan、Narasimhan 和 Deshpande，
GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735)，
[2024-06-28 的 v3 全文](https://arxiv.org/html/2311.09735v3)，KDD 2024，
[DOI](https://doi.org/10.1145/3637528.3671900)。

论文研究来源在合成回答中的可见度，包括归属文本长度／位置与主观印象。实验支持测试
相关来源引用、引语、统计与更清晰表达。“最高提升 40%”等结果依赖具体实验与指标，
不能保证当前引擎收录、SEO 排名、点击或销售。领域和引擎差异需在实际环境验证。论文
指出引擎／问题会演变，且未评估这些方法对搜索排名的影响。随附二元结果统计工具用于
日常监测，不是论文指标复现。

## 明确取舍

- 保留有证据的内容、有用的答案覆盖、实体清晰、真实站外佐证与监测迭代。
- 排除 `geo_functions.py` 中允许虚构引用、伪造引语或无证据权威措辞的实验提示。
- 用用户用途、实际架构和测量环境，替代固定字数、FAQ／表格配额、绝对子域名规则和
  通用分数阈值。
- 流量下降归因、“AI 偏爱某种格式”、没有爬虫就判定被屏蔽，均作为需验证假设，不能
  无条件采用。
- 区分搜索、训练和用户触发访问，保留网站所有者的隐私选择。

## 当前平台一手来源

- [Google：AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)。
  常规 SEO、索引和摘要资格适用，无需特殊 AI 文件或 schema；AI 功能表现包含在
  Search Console 的 Web 流量中。
- [OpenAI：爬虫说明](https://developers.openai.com/api/docs/bots)。OAI-SearchBot 用于搜索，
  GPTBot 用于潜在训练，控制独立；用户触发获取另有用途。验证身份需查当前指导。
- [Perplexity：爬虫说明](https://docs.perplexity.ai/docs/resources/perplexity-crawlers)。
  查当前 PerplexityBot 与 Perplexity-User 的用途和访问指导。
- [Agent Skills 规范](https://agentskills.io/specification)。两个目录遵循 SKILL.md／
  frontmatter 和可选资源约定；`agents/openai.yaml` 提供可选 Codex 界面元数据。

增加其他引擎时查询其当前文档，记录真实检索行为；不得把这三家的规则外推给所有引擎。

## 署名与许可

本项目原创指令、翻译和离线工具采用 MIT。Promptwatch 为 MIT，仓库第三方说明保留
其版权与许可通知，适用于工作流改编。GEO-optim/GEO 为 Apache-2.0，本项目仅引用研究，
不分发其代码、数据集、图片或缓存回答。平台文档仅链接与概述，不表示第三方关联。
