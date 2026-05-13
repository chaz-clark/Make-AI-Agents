# Source Docs Index

> Reference. Lookup table of the 34 cached platform documentation files in `source_docs/` — keyed by short_name, with platform, topic keywords, and source URL.

**Scope**: Catalogs every doc currently cached in `source_docs/*.md` so consumers (`doc_analysis_agent`, `merge_agent`, future agents) can resolve a short_name to its platform / topic / URL without grepping the cache or re-reading `_refresh_log.json` and `doc_refresh_agent.json` together. Bounds OUT: live-doc fetching (that's `doc_refresh_agent`), proposal generation (that's `doc_analysis_agent`), and any per-doc body content (the cached `.md` files themselves remain the body authority).

**Provenance**: `source_docs/_refresh_log.json` (source keys + fetch_status + size context) and `update_agents/doc_refresh_agent.json` → `primary_data.sources[]` (platform, label, source_url, section_focus). See `provenance.sources` in the JSON companion.

_Last updated: 2026-05-13_

## Audience

- **`doc_analysis_agent`** — looks up a short_name to know which platform's doc it just diffed, which gives it the convergence-platform tag in proposal scoring.
- **`merge_agent`** — looks up a short_name to know the canonical `platform` / `label` / `source_url` for the front matter when promoting a brand-new doc whose target file does not yet exist.
- **Future agents** that need platform-specific doc routing (e.g., "find the Anthropic citation primitive doc" → resolve to `anthropic_citations`).

## Out of Scope

- The doc body itself — read the cached `.md` directly when content is needed.
- Per-doc freshness — that lives in `source_docs/_refresh_log.json` (the canonical refresh log; this index is intentionally derivative and may lag).
- Fetch configuration (URLs to try, suspect-overwrite threshold, retry logic) — that's `doc_refresh_agent.json → fetch_config`.

## Related Knowledge

- `knowledge/behavioral_discipline.{md,json}` — the universal discipline; consumed by every agent including the ones that read this index.

## Entries

The 34 entries are enumerated in JSON `facts[]`. Each entry carries: `short_name`, `platform`, `topic_keywords`, `source_url`, `runtime_strategy` (`platform_cached` for all 34, since each is already cached locally in `source_docs/`).

Below is a per-platform summary for human scanning; the authoritative list is in the JSON.

### Anthropic (7 docs)

- `anthropic_agents` — Agent Skills architecture, progressive disclosure, skill authoring
- `anthropic_agent_sdk` — Agent SDK, agent loop, subagents, sessions, hooks
- `anthropic_subagents` — `AgentDefinition` fields, subagent invocation, `parent_tool_use_id`
- `anthropic_tool_use` — tool_choice, strict mode, parallel tools, MCP connector
- `anthropic_prompt_caching` — `cache_control` ephemeral type, TTLs, breakpoints
- `anthropic_citations` — document content blocks, `citations.enabled`, cited_text
- `anthropic_files` — Files API beta, file_id references, 500MB/file

### Google ADK (10 docs)

- `google_adk_multi_agents` — `sub_agents`, `transfer_to_agent`, `AgentTool`, workflow agents
- `google_adk_a2a` — Agent2Agent protocol hub (navigation only)
- `google_adk_a2a_intro` — A2A overview, AgentCard, Skills, Messages, Tasks
- `google_adk_a2a_quickstart_exposing` — Expose an ADK agent via A2A (Python)
- `google_adk_a2a_quickstart_exposing_go` — Expose A2A (Go)
- `google_adk_a2a_quickstart_exposing_java` — Expose A2A (Java)
- `google_adk_a2a_quickstart_consuming` — Consume a remote A2A agent (Python)
- `google_adk_a2a_quickstart_consuming_go` — Consume A2A (Go)
- `google_adk_a2a_quickstart_consuming_java` — Consume A2A (Java)
- `google_adk_a2a_extension` — ADK extension to A2A protocol

### Google Gemini (6 docs)

- `google_gemini_agentic` — function calling, parallel/compositional, Google Search tool
- `google_structured_output` — `response_mime_type`, `response_json_schema`
- `google_system_instructions` — persona/task/context/format patterns
- `google_files` — Gemini Files API, 48hr persistence, 2GB/file
- `google_caching` — `cachedContent`, implicit vs explicit, TTL/expire_time
- `google_gems_overview` — Gem creation, 4 pillars, knowledge files

### OpenAI (7 docs)

- `openai_agents_sdk` — agents, handoffs, guardrails, lifecycle hooks, MCP
- `openai_multi_agent` — Agents-as-tools vs Handoffs, manager-style orchestration
- `openai_handoffs` — `Handoff` object, `tool_name_override`, `input_filter`
- `openai_agents_class` — `Agent` class, `Agent.as_tool()`, `tool_use_behavior`
- `openai_running_agents` — `Runner.run()`, `max_turns`, persistence strategies
- `openai_tracing` — Trace/Span, `agent_span`, `parent_id`
- `openai_file_search` — `file_search` Responses API tool, vector stores

### xAI (4 docs)

- `xai_overview` — Grok APIs, OpenAI-compat client, base URL
- `xai_multi_agent` — `agent_count=4|16`, `grok-4.20-multi-agent`, leader-agent synthesis
- `xai_grok_multi_agent_model_card` — Grok 4.20 model card, 2M context, pricing
- `xai_collections` — `collections_search` tool, citation URI format

Total: **34 docs** (7 + 10 + 6 + 7 + 4).

## Why this is `read_at_runtime`

With 34 entries each carrying short_name + platform + topic keywords + URL + runtime_strategy, the JSON body comfortably exceeds the 8000-token embed threshold defined in `make_agent_knowledge.json → runtime_strategy_rules`. Consumers should retrieve this file at runtime rather than embed it in the system prompt of every call. See `_metadata.runtime_strategy` in the JSON companion.
