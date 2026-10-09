# GEO-Skill · 生成式引擎优化

[English](README.en.md) · 中文

面向 AI 搜索的可安装 Agent Skill，提供**中文版与英文版**。从网站审计、内容改写、
引用分析到持续测量，帮助网站或品牌形成可核验的 GEO 工作流程。

本项目综合研究 [Promptwatch skills](https://github.com/promptwatch-com/skills) 和
[GEO-optim/GEO](https://github.com/GEO-optim/GEO)，并核对 Google、OpenAI、Perplexity
的一手文档。它是独立成果；研究中的效果数值不构成收录、流量或商业成效承诺。

## 选择版本

| 版本 | Skill 名称 | 入口 |
| --- | --- | --- |
| 中文 | `geo-optimization-zh` | [SKILL.md](skills/geo-optimization-zh/SKILL.md) |
| English | `geo-optimization` | [SKILL.md](skills/geo-optimization/SKILL.md) |

两个版本能力与证据标准一致，各自包含完整材料和离线工具，可独立安装。建议只安装
首选语言，避免两个版本同时自动触发。版本：**1.0.0**；来源审阅：**2026-10-09**。

## 安装与使用

支持 Agent Skills 的客户端可通过 Skills CLI 选择安装位置：

```bash
npx skills add andrewdavidwy-del/GEO-Skill --skill geo-optimization-zh
```

英文版：

```bash
npx skills add andrewdavidwy-del/GEO-Skill --skill geo-optimization
```

手动安装到 Codex：

```bash
git clone https://github.com/andrewdavidwy-del/GEO-Skill.git
mkdir -p ~/.codex/skills
cp -R GEO-Skill/skills/geo-optimization-zh ~/.codex/skills/
```

如果已有同名版本，先备份再更新。其他客户端使用其支持的 skill 目录；安装后按客户端
要求重新加载。仅阅读内容可直接打开上方入口，无需安装工具。

示例请求：

```text
使用 $geo-optimization-zh 审计 https://example.com，目标是中文市场的 AI 搜索引用。
给出有证据的发现、优先任务和测量方案。

使用 $geo-optimization-zh 改写这篇产品介绍。保留真实事实，标出需要补充的证据。

使用 $geo-optimization-zh 分析这份 AI 回答导出，分别报告提及、官网引用、推荐和错误。
```

## 工作范围

- 网站／品牌审计、技术访问与实体清晰度。
- 可核验的内容改写、写作简报与中英文适配。
- 站外来源机会、竞品引用与公平比较。
- 有独立数据价值的程序化页面试点。
- AI Overview／零点击流量诊断与竞争性解释。
- 可重复的问题面板、分组指标、可选 Promptwatch 分析。

不依赖付费账号、专有 MCP 或模型 API。没有监测数据时明确列出缺口，不编造基线。
不采用虚构引语、伪造统计、隐藏模型指令和“保证 AI 推荐”的做法。

## 离线测量工具

Python **3.10+**，仅使用标准库，不访问网络。读取人工或现有工具**已标注**的 JSONL：

```bash
python3 skills/geo-optimization-zh/scripts/score_visibility.py \
  skills/geo-optimization-zh/assets/sample-observations.jsonl --domain example.com
```

样本为模拟数据。工具分别输出提及率、推荐率、官网引用率、负面情绪率、事实错误率，
保留各自分母、未知和失败记录，按引擎／模型／语言／市场／检索模式分组。
它不自动识别品牌或核验事实，不复现论文指标或供应商总分。
数据定义与真实输入方法见 [测量说明](skills/geo-optimization-zh/references/measurement.md)。

## 维护与验证

开发校验需要 PyYAML；skill 正常使用及测量脚本不需要它。

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/validate_repo.py
python3 -m unittest discover -s tests -v
```

校验覆盖两个 skill 的结构、引用文件、界面元数据和打包一致性；测试覆盖计数、缺失值、
失败记录、域名归属、重复输入和错误数据。行为评估用例见 [scenarios.md](evals/scenarios.md)，
不等同于已证明提升真实 AI 搜索成效。

## 来源与许可

完整研究与取舍见 [来源说明](skills/geo-optimization-zh/references/sources.md)。原创内容和
工具采用 [MIT](LICENSE)；上游署名见 [第三方说明](THIRD_PARTY_NOTICES.md)。不分发上游
研究代码、数据集、图片或缓存回答。提交前扫描公开包中的凭据与私人路径。
