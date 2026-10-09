# GEO-Skill · Generative Engine Optimization

English · [中文](README.md)

Installable Agent Skills in **English and Chinese** for evidence-based AI search
audits, content improvement, citation analysis, technical access, and measurement.

This independent synthesis draws on [Promptwatch skills](https://github.com/promptwatch-com/skills)
and [GEO-optim/GEO](https://github.com/GEO-optim/GEO), checked against primary Google,
OpenAI, and Perplexity documentation. Research gains are not inclusion, traffic, or
business-outcome guarantees.

## Choose a version

| Language | Skill name | Entrypoint |
| --- | --- | --- |
| English | `geo-optimization` | [SKILL.md](skills/geo-optimization/SKILL.md) |
| 中文 | `geo-optimization-zh` | [SKILL.md](skills/geo-optimization-zh/SKILL.md) |

Both versions have the same capabilities and evidence standards, with complete
references and the offline tool in each package. Install your preferred language to
avoid both automatically activating. Version: **1.0.0**; sources reviewed **2026-10-09**.

## Install and invoke

For Agent Skills clients, use the Skills CLI to choose installation destinations:

```bash
npx skills add andrewdavidwy-del/GEO-Skill --skill geo-optimization
```

Chinese version:

```bash
npx skills add andrewdavidwy-del/GEO-Skill --skill geo-optimization-zh
```

Manual Codex installation:

```bash
git clone https://github.com/andrewdavidwy-del/GEO-Skill.git
mkdir -p ~/.codex/skills
cp -R GEO-Skill/skills/geo-optimization ~/.codex/skills/
```

Back up an existing same-name skill before updating. For other clients, use their
supported skill directory and reload as required. You can also read the entrypoints
directly without installing anything.

Example requests:

```text
Use $geo-optimization to audit https://example.com for English-language AI search.
Deliver evidence-backed findings, prioritized tasks, and a measurement plan.

Use $geo-optimization to rewrite this product page, preserving facts and flagging
claims that require evidence.

Use $geo-optimization to analyze this AI response export. Report mentions, owned
citations, recommendations, and factual errors separately.
```

## Capabilities

- Site/brand audits, technical access, and entity clarity.
- Evidence-backed rewrites, content briefs, and bilingual adaptation.
- Verified offsite opportunities, competitor citations, and fair comparisons.
- Programmatic page pilots with distinct data and user value.
- AI Overview/zero-click diagnosis with competing explanations.
- Repeatable prompt panels, cohort metrics, and optional Promptwatch analysis.

No paid account, proprietary MCP, or model API is required. Missing monitoring data
stays explicit. The skill excludes fabricated quotations/statistics, hidden model
instructions, and guaranteed recommendations.

## Offline measurement

Python **3.10+**, standard library only, no network access. Aggregate **already
annotated** JSONL observations from reviewers or existing tools:

```bash
python3 skills/geo-optimization/scripts/score_visibility.py \
  skills/geo-optimization/assets/sample-observations.jsonl --domain example.com
```

The sample is synthetic. Outcomes include mention, recommendation, owned citation,
negative sentiment, and factual error rates, each with its own denominator, unknowns,
and failures. Results are broken down by engine/model/language/market/retrieval.
The tool does not infer brand mentions, verify facts, reproduce paper metrics, or
calculate a vendor score. See [measurement.md](skills/geo-optimization/references/measurement.md).

## Maintenance and validation

Developer validation uses PyYAML; normal skill use and the offline tool do not.

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/validate_repo.py
python3 -m unittest discover -s tests -v
```

Validation covers skill structure, references, UI metadata, and packaging consistency.
Tests cover counts, unknowns, failures, domain ownership, duplicate input, and invalid
records. [Behavioral scenarios](evals/scenarios.md) support future evaluation; passing
structural or tool checks does not establish improved live search outcomes.

## Sources and license

See [sources.md](skills/geo-optimization/references/sources.md) for the research and
adaptation decisions. Original material and the tool use [MIT](LICENSE); upstream
attribution is in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Upstream research code,
datasets, images, and cached answers are not redistributed. Scan the public package
for credentials and private paths before publishing changes.
