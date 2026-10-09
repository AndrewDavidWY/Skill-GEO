# Sources and decision record

Reviewed: **2026-10-09**. Repository snapshots are immutable; provider rules can change.
Recheck official platform documentation before applying technical recommendations.
This is an independently authored synthesis, not an official Promptwatch product or
an implementation endorsed by the GEO paper's authors.

## Requested repositories

| Source | Reviewed snapshot | What informed this skill |
| --- | --- | --- |
| [Promptwatch skills](https://github.com/promptwatch-com/skills) | [36fb1231174bef63980f260500a9dbd1dd0ff18d](https://github.com/promptwatch-com/skills/tree/36fb1231174bef63980f260500a9dbd1dd0ff18d) | Content, offsite, programmatic pages, traffic recovery; optional project/prompt/citation/competitor/crawler/referral analysis |
| [GEO-optim/GEO](https://github.com/GEO-optim/GEO) | [c9e985f2bc4b539a01e8e9d226ff2a3d8d29a888](https://github.com/GEO-optim/GEO/tree/c9e985f2bc4b539a01e8e9d226ff2a3d8d29a888) | Black-box optimization framework, method experiments, source visibility evaluation, limits of benchmark-to-production transfer |

The Promptwatch URL appeared three times in the request and was reviewed as one
unique source. Its 20 skill entrypoints (4 GEO, 13 MCP, 3 platform) were reviewed.
The GEO README, `src/geo_functions.py`, `src/run_geo.py`, metric implementation in
`src/utils.py`, and linked paper were inspected. No upstream agent instructions were
executed; research scripts were not run and no paid model calls were made.

## Research grounding

[Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, and Deshpande,
GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735),
[v3 text, 2024-06-28](https://arxiv.org/html/2311.09735v3), KDD 2024,
[DOI](https://doi.org/10.1145/3637528.3671900).

The paper studies source visibility in synthesized answers, including attribution
length/position and subjective impressions. Its experiments support testing relevant
source citations, quotations, statistics, and clearer writing. The reported gains,
including “up to 40%”, depend on the experiment and metric; they are not promises of
modern engine inclusion, SEO rank, clicks, or sales. Domain and engine differences
require local validation. The paper notes evolving engines/queries and does not
evaluate the methods' effect on search rankings. The bundled binary-rate tool is
an operational monitoring aid, not a reproduction of those research metrics.

## Explicit adaptations

- Keep source-grounded content, useful answer coverage, entity clarity, real outside
  corroboration, and monitored iteration.
- Reject experimental prompts in `geo_functions.py` that permit invented citations,
  fabricated quotations, or persuasive authority claims without evidence.
- Replace fixed word counts, FAQ/table mandates, blanket subdomain rules, and universal
  score thresholds with user value, actual architecture, and measured context.
- Treat traffic-loss attribution, “AI prefers this format”, and missing-bot diagnoses
  as hypotheses requiring observations, not unconditional rules.
- Distinguish search, training, and user-triggered access; retain owner privacy choices.

## Current primary platform sources

- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features).
  Ordinary SEO/indexing and snippet eligibility apply; special AI files or schema are
  not required. AI-feature performance is included in Search Console's Web traffic.
- [OpenAI: crawler overview](https://developers.openai.com/api/docs/bots).
  OAI-SearchBot serves search, GPTBot serves potential training; controls are independent.
  User-triggered fetching is a separate role. Check live provider verification guidance.
- [Perplexity: crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers).
  Use current role and access guidance for PerplexityBot and Perplexity-User.
- [Agent Skills specification](https://agentskills.io/specification).
  The two folders follow the SKILL.md/frontmatter and optional-resource convention;
  `agents/openai.yaml` supplies optional Codex interface metadata.

For an additional engine, consult its own current documentation and annotate its
actual retrieval behavior. Do not extrapolate these three providers' rules to it.

## Attribution and licensing

Original instructions, translations, and the offline tool use MIT. Promptwatch is MIT;
the repository-level third-party notice retains its copyright and permission notice
for the workflow adaptation. GEO-optim/GEO is Apache-2.0; it is cited as research and
no source code, benchmark dataset, images, or cached responses are redistributed.
Primary documentation is linked and summarized; no third-party affiliation is implied.
