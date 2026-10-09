# GEO work playbooks

Read the section matching the request. Platform-specific details must be checked
against the live primary sources listed in [sources.md](sources.md).

## Audit and prioritization

Build an evidence ledger: observation, URL/artifact, date, engine/model or browser
context, finding status, limitation, and affected page/prompt. Start with business-
relevant pages; do not crawl an entire site by default. Compare actual cited sources
for the same questions, including their answer coverage, evidence, and freshness.

Use dependencies to rank work: a confirmed access blocker on a key page precedes
copy refinements; a missing high-value answer precedes polishing low-value boilerplate.
Use high/medium/low effort and confidence rather than invented precision. A score is
an explicit prioritization heuristic, not a measured probability of success.

Example action row:

| Page/prompt | Evidence | Change | Dependency | Acceptance | Outcome hypothesis |
| --- | --- | --- | --- | --- | --- |
| Setup guide / “Does X integrate with Y?” | Current guide omits supported version; verified product docs name it | Add tested version, setup steps, failure conditions, dated source | Confirm integration behavior | Instructions work on stated version; no unsupported compatibility claim | Better coverage may improve citation relevance |

## Technical access

Check relevant live URLs with real GETs, redirects, status, canonical, content type,
robots directives, `X-Robots-Tag`, sitemap, internal links, and HTML text. Inspect CDN/WAF
or login challenges when observed. A browser-only shell or screenshot cannot establish
what a crawler received. Compare rendered and initial HTML when the content depends on
JavaScript; document which was actually inspected.

- Separate **allowed**, **fetched**, **indexed**, **retrieved**, and **cited**. `200`, a
  sitemap entry, a crawl log, or a local build confirms only its respective stage.
- Distinguish search crawlers, training crawlers, and user-triggered fetchers. Preserve
  the site's training/privacy choices. Verify crawler identity against provider
  guidance; a user-agent string can be spoofed.
- For Google AI search, inspect ordinary indexing and snippet eligibility. Verify
  current Google documentation before interpreting Googlebot/Google-Extended controls.
- Keep important answers available as accessible text. Use accurate canonicals and
  language annotations for real localized pages; preserve working URLs and architecture.
- Use suitable Organization, Article, Product, or other schema only when the page
  supports it. JSON-LD must describe visible, current facts. Rich-result eligibility
  differs from schema vocabulary validity and does not guarantee AI citation.
- Treat `llms.txt` as an optional experiment when requested, not a standard inclusion
  requirement. Never disclose private routes, source data, or secrets through it.
- Assess mobile use and performance when they affect access or user experience;
  there is no universal GEO TTFB target to enforce without context.

Verify proposed changes at the appropriate layer: source check, browser behavior,
live HTTP response, and actual provider observations. Do not collapse those checks.

## Content rewrite and writer-ready brief

Map one real question to the page's purpose, audience, and decision. Provide the
answer early, then evidence, conditions, examples, and tradeoffs. Keep comparisons
fair; verify competitors' current prices and capabilities with dated sources.

Use a claim ledger:

| Claim | Supporting source | As-of date | Scope/limitation | Editorial decision |
| --- | --- | --- | --- | --- |
| A feature works with a version | Product docs or reproduced test | Recorded date | Stated platform/version only | State with the condition |
| “Best”, market share, customer count | No supporting evidence | Unknown | Unverifiable | Remove or request evidence |

For quotations, preserve the speaker, original wording, context, URL, and permitted
reuse. For statistics, preserve units, population, timeframe, method, and uncertainty.
An outbound citation must support the adjacent claim, not merely come from a known
domain. Use real original data when available; do not manufacture research for GEO.

A brief should contain target questions, audience/job, intended page type, outline,
direct answer draft, evidence requirements, useful internal links, tradeoffs, CTA,
and acceptance criteria. A rewrite should deliver actual replacement text and explain
material claim changes. Do not impose word quotas, a table on every page, or FAQ schema
on unrelated content. Advance an update date only after a meaningful content review.

For Chinese/English content, map stable names, abbreviations, product terms, units,
currency, and source dates. Retain one underlying fact set; adapt intent, examples,
and audience vocabulary. Avoid asserting region-specific availability without proof.

## Offsite sources

Look for specific relevant pages cited in observed answers, then verify whether they
mention the brand, a competitor, or only the category. Separate independent coverage,
partner material, owner-controlled pages, and sponsored content. Citation frequency
is a sampling observation, not proof that a source is inherently trusted by all models.

Prioritize an opportunity by relevance, observed citation context, factual correction
needed, contribution quality, and practical cost. Deliver URL, date, evidence, angle,
proof package, affiliation disclosure, and a way to observe later changes.

Useful contributions include original data, tested guides, accurate integration
listings, expert explanations, and fair comparisons. Do not recommend fake reviews,
sockpuppets, undisclosed promotion, spam, or buying purported guaranteed AI citations.
Preparing a requested outreach draft is different from sending it. Contact third
parties only with explicit authorization; honor previous authorization for the task.

## Scale: programmatic content

Select a page family only when the dataset contains distinct user value: comparisons,
integrations, use cases, directories, definitions, or genuinely supported locations.
Changing a city/keyword in otherwise identical copy does not create that value.

Define record fields such as entity IDs, audience/question, actual capability,
evidence URLs, review dates, unique facts, limitations, canonical, and language.
Represent unknown facts explicitly. Missing evidence should not become invented text.
Do not present imaginary offices or services as local availability.

Create a small representative pilot, including incomplete/edge records. Verify
accuracy, usefulness, broken links, duplicate intent, canonicals, mobile behavior,
and maintainability. Merge or hold pages that add no distinct answer; expand only
after pilot acceptance and within the authorized scope. No minimum word count or
maximum template percentage substitutes for page usefulness. Use change-aware review
when prices, versions, or availability change.

## AI Overview and zero-click recovery

Match query/page, device, country, date window, and seasonality. Examine impressions,
clicks, CTR, positions, conversions, deployments, indexability, and measurement changes.
Observe whether AI answers actually appear in the sampled context and who they cite.
Stable impressions with lower CTR suggest a problem but do not prove AI causation.
Incognito does not remove localization or all variation.

Compare explanations: ranking change, demand/seasonality, snippet change, technical
issue, tracking change, and answer satisfaction. Search Console's aggregate Web data
must not be presented as an isolated AI Overview traffic report without such a field.

- If cited but clicks fall, test genuinely useful deeper resources/tools and measure
  business outcomes; citation visibility alone is not recovered traffic.
- If relevant competing sources are cited, compare answer completeness and evidence
  and test a targeted improvement; their format is not proof of causation.
- If a query loses business value, reconsider investment using measured outcomes;
  do not automatically abandon informational content or claim a permanent loss.

For a CTR counterfactual, `current impressions × (baseline CTR − current CTR)` estimates
click difference under an assumed unchanged baseline. Label the assumption; it is not
measured AI-attributable loss. Keep visibility, referrals, and conversions separate.
