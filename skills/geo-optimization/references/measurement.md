# Measuring GEO outcomes

## Design the panel

Use real audience questions across discovery, definitions, comparisons, use cases,
evaluation, and branded support when relevant. Keep branded and unbranded questions
separate. Select a small panel appropriate to budget; there is no universal prompt
count or funnel percentage. Record exact prompt text, stable ID, intent, language,
market, engine/product, model if exposed, retrieval mode, settings, date, and timezone.

Do not force the brand into every question, supply its pages to a purported organic
visibility test, or tell a model to recommend it. Supplied-source experiments can test
answer extraction, but label them separately from live retrieval. `retrieval=off` is
a closed-book result and cannot establish current search inclusion.

Preserve the full response, displayed citation URLs, and screenshot/export when
available. A tracking system's response volume is not consumer search demand.
Use fresh conversations and repeat observations when affordable. A single result is
a spot check. Record failures and unknowns rather than treating them as negative answers.

## Outcome definitions

| Outcome | Numerator | Denominator | What it does not prove |
| --- | --- | --- | --- |
| Mention rate | Successful responses that explicitly identify the target | Successful responses with a known mention label | Recommendation, citation, or consumer demand |
| Recommendation rate | Successful responses that endorse the target for the specified need | Successful responses with a known recommendation label | Accuracy or conversion |
| Owned citation rate | Responses with at least one displayed citation on an owned domain | Successful responses with a known citation list | That the cited source supports every claim |
| Negative sentiment rate | Negative target assessments | Target-mention responses with a known sentiment label | A product defect without examining the cited facts |
| Factual error rate | Responses containing a verified target-related factual error | Target-mention responses whose accuracy was checked | Accuracy of unchecked responses |

Owned domains include explicit subdomains; specify them carefully if a host serves
unrelated tenants. A third-party page mentioning the brand is an external corroboration
opportunity, not an owned citation. Count each answer once per outcome regardless of
repeated aliases or duplicated URLs. Resolve entity ambiguity manually. Mention and
recommendation labels refer to answer text; a cited URL alone does not set them true.

Keep top-position recommendation, supported-citation rate, share of voice, referral
sessions, and conversion measures separate if collected. Define their units and
denominators explicitly. Prefer an outcome vector to an unexplained composite score.

## Included offline tool

`scripts/score_visibility.py` aggregates **already annotated** JSONL records. It uses
only Python 3.10+ standard libraries and makes no network requests. It does not call
AI engines, discover citations, verify claims, infer mentions, or reproduce the paper's
position-adjusted word-count / subjective-impression metrics or Promptwatch's score.

Run from the installed skill directory:

```bash
python3 scripts/score_visibility.py assets/sample-observations.jsonl --domain example.com
python3 scripts/score_visibility.py /path/to/observations.jsonl --domain brand.example --output /path/to/report.json
```

The bundled sample is synthetic and must not be presented as a brand's result.
The JSON output gives numerator, denominator, rate in [0,1] or `null`, and unknown
count for every outcome. It includes failures, time range, prompt counts, and cohorts
by engine/model/language/market/retrieval. Overall rates pool responses and are not a
balanced model or prompt average. The tool warns about missing labels and unequal
successful repetitions; inspect cohorts before comparing time periods.

Each nonblank input line is an object:

| Field | Format / meaning |
| --- | --- |
| `run_id` | Unique observation ID; duplicates fail instead of inflating counts |
| `prompt_id` | Stable ID referring to saved exact prompt text |
| `engine`, `model`, `language`, `market` | Nonempty strings; use `unknown` for an undisclosed model |
| `observed_at` | ISO 8601 timestamp with timezone, e.g. `2026-10-09T09:00:00+07:00` |
| `retrieval` | `web`, `off`, `supplied`, or `unknown` |
| `status` | `ok` or `error`; a failure is excluded from outcome denominators |
| `target_mentioned` | Boolean, or `null` if not annotated |
| `target_recommended` | Boolean, or `null`; `true` requires mention `true` |
| `cited_urls` | Displayed HTTP(S) citation strings, `[]` if confirmed absent, `null` if unknown |
| `sentiment` | `positive`, `neutral`, `negative`, `mixed`, or `null`; label only when target is mentioned |
| `factual_error` | Boolean after verification, or `null`; label only when target is mentioned |

All five annotation fields are required for `ok` records so missing data is explicit.
For `error`, omit them or set all to `null`. Extra fields such as `response_path`,
`prompt_text`, `intent`, `reviewer`, `source`, and `verification_notes` are preserved in
the original input but not interpreted by the tool. Retain them for evidence review.
Do not feed raw vendor exports without mapping their units and fields to this schema.

## Compare and interpret

Compare the same questions, engines, model versions, markets, languages, retrieval
modes, repetitions, and equal date windows. If composition changes, compare the
intersection or report separate cohorts, not a misleading pooled improvement.
Exclude failed/unknown labels from the relevant denominator and disclose coverage.
For a change from 20% to 30%, report **+10 percentage points**, or **+50% relative**
with the baseline; if the baseline is zero, relative change is undefined.

Small repeated panels are not independent random samples of users. Show numerator /
denominator, repetition variability, and missingness. Do not claim statistical
significance from the summary alone. Check negative assessments and factual errors
against original sources, not only a sentiment classifier.

Before/after movement is an observation. For stronger attribution, change a specific
component, keep a matched control where feasible, log deployment and recrawl dates,
and examine competing explanations. Citation counts, referrals, leads, and revenue
can move differently. Referrer loss and untracked AI use limit traffic attribution.
