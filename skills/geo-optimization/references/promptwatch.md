# Optional Promptwatch workflow

Promptwatch is an optional measurement provider, not a dependency of this skill.
The source snapshot is recorded in [sources.md](sources.md). Tool names below were
documented there; discover the connected tools and read their current schemas before
use. Do not invent a tool, parameter, metric definition, or successful connection.

## Choose the available route

1. Use an already connected MCP/connector when available. Resolve the actual project,
   target entity, timezone, date range, tracked prompts, and model coverage first.
2. Otherwise accept an existing export, preserving its field and denominator meanings.
3. Otherwise use the manual panel in [measurement.md](measurement.md). Continue useful
   content/technical work without purchasing a subscription or requesting an API key.

Only configure a connection when requested. The reviewed upstream lists
`https://server.promptwatch.com/mcp` and API keys in the application's settings. Verify
current official setup instructions for the target agent; authentication formats are
client-specific. Prefer project-scoped access when sufficient. Use the client's secure
secret mechanism; do not write real credentials to the repo, skill, chat, or report.

## Read-only analysis map

| Question | Example upstream tool names | Evidence to retain |
| --- | --- | --- |
| Project / coverage | `list_projects`, `list_prompts`, `get_responses_summary` | Project, prompts, engines, count, period |
| Visibility / sentiment | `get_visibility_time_series`, `get_sentiment_time_series`, `list_responses` | Current and matched prior period, sample responses |
| Competitors | `get_competitor_heatmap`, `get_top_competitors`, `get_brand_visibility_over_time` | Same panel/period, exact brands and per-model values |
| Content gaps / briefs | `list_content_gap_prompts`, `get_content_gap_recommendations`, `list_query_fanouts` | Prompt, score definition, recommended page, evidence |
| Citations / offsite | `get_citations`, `get_citation_top_pages`, `get_citation_domains_by_llm`, `get_self_citation_frequency` | URLs, observed context, owned/external classification |
| Crawlers | `get_crawler_trend`, `get_top_crawler_pages`, `get_sitemap_progress` | Actual bot role, dates, routes, logging coverage |
| AI referrals | `get_visitor_total`, `get_visitor_referrer_stats` | Attributed visits, analytics definition, missing referrers |

Pull only the data needed for the question; paginate when required and disclose any
truncation. Use matching date windows and inspect underlying responses before turning
a score movement into an explanation. Response counts are not measured search volume.
Vendor coverage, sentiment, and visibility scores are not interchangeable with the
offline tool's binary outcome rates. Preserve provider definitions and label heuristic
thresholds as such; do not treat upstream score bands as universal GEO standards.

An empty dataset is a measurement gap, not zero visibility. Missing crawler events
can reflect logging coverage and do not prove blocking. A weekly report can summarize
matched periods, major evidence-supported changes, next actions, and missing data.
Do not schedule it merely because a report was requested.

Tools such as `create_prompt`, `create_prompts_bulk`, and `create_content` mutate account
state and may consume credits. Use them only within explicit task authorization;
check actual scope/cost and proceed when already authorized, otherwise prepare a
reviewable batch first. Read-only GEO analysis does not authorize these mutations.
