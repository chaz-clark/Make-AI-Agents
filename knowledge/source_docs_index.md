---
name: source_docs_index
version: "1.0"
last_updated: 2026-05-13
description: Lookup table of the 34 cached platform documentation files in source_docs/.
shape: reference
generated_by: make_agent_knowledge v1.0 (dogfood pass 2026-05-13)
runtime_strategy: read_at_runtime
runtime_strategy_rationale: 34 rows × ~5 fields each exceeds the 8000-token embed threshold. Consumers retrieve at runtime via platform file primitives.
consumed_by:
  - update_agents/doc_analysis_agent.json
  - update_agents/merge_agent.json
companion_json_deprecated: "2026-07-08 - consolidated into YAML frontmatter per JSON purge"

facts:
  - id: anthropic_agents
    short_name: anthropic_agents
    platform: Anthropic
    topic_keywords: agent skills, progressive disclosure, skill authoring, enterprise governance, API integration
    source_url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md
    runtime_strategy: platform_cached

  - id: anthropic_tool_use
    short_name: anthropic_tool_use
    platform: Anthropic
    topic_keywords: tool_choice, fallback handling, strict mode, parallel tool use, tool runner, MCP tools
    source_url: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use
    runtime_strategy: platform_cached

  - id: anthropic_agent_sdk
    short_name: anthropic_agent_sdk
    platform: Anthropic
    topic_keywords: agent SDK, agent loop, subagents, sessions, hooks, compaction, permissions
    source_url: https://code.claude.com/docs/en/agent-sdk/overview
    runtime_strategy: platform_cached

  - id: anthropic_subagents
    short_name: anthropic_subagents
    platform: Anthropic
    topic_keywords: AgentDefinition fields, parent_tool_use_id tracking, subagent invocation, stateless context, subagent resumption
    source_url: https://code.claude.com/docs/en/agent-sdk/subagents
    runtime_strategy: platform_cached

  - id: anthropic_prompt_caching
    short_name: anthropic_prompt_caching
    platform: Anthropic
    topic_keywords: cache_control ephemeral, 5m/1h TTLs, tools/system/messages prefix ordering, 4 breakpoints, pre-warming
    source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
    runtime_strategy: platform_cached

  - id: anthropic_citations
    short_name: anthropic_citations
    platform: Anthropic
    topic_keywords: document content block, citations.enabled, cited_text, char/page/block indices, streaming citations_delta, incompatible with structured outputs
    source_url: https://platform.claude.com/docs/en/build-with-claude/citations
    runtime_strategy: platform_cached

  - id: anthropic_files
    short_name: anthropic_files
    platform: Anthropic
    topic_keywords: Files API beta (anthropic-beta files-api-2025-04-14), file_id in document/image blocks, 500MB/file 500GB/org, MIME types
    source_url: https://platform.claude.com/docs/en/build-with-claude/files
    runtime_strategy: platform_cached

  - id: google_gemini_agentic
    short_name: google_gemini_agentic
    platform: Google Gemini
    topic_keywords: function calling, parallel/compositional calling, thinking models, MCP, Google Search built-in tool
    source_url: https://ai.google.dev/gemini-api/docs/function-calling
    runtime_strategy: platform_cached

  - id: google_structured_output
    short_name: google_structured_output
    platform: Google Gemini
    topic_keywords: response_mime_type, response_json_schema, JSON schema features, structured output vs function calling
    source_url: https://ai.google.dev/gemini-api/docs/structured-output
    runtime_strategy: platform_cached

  - id: google_system_instructions
    short_name: google_system_instructions
    platform: Google Gemini
    topic_keywords: system instruction patterns, persona/task/context/format, best practices, Gemini 3 template
    source_url: https://ai.google.dev/gemini-api/docs/system-instructions
    runtime_strategy: platform_cached

  - id: google_files
    short_name: google_files
    platform: Google Gemini
    topic_keywords: client.files.upload, file URI references, 48hr persistence, 50MB PDF / 2GB other, 20GB/project, >100MB threshold
    source_url: https://ai.google.dev/gemini-api/docs/files
    runtime_strategy: platform_cached

  - id: google_caching
    short_name: google_caching
    platform: Google Gemini
    topic_keywords: cachedContent, implicit vs explicit caching, TTL/expire_time, min 1024 (Flash) / 4096 (Pro) tokens
    source_url: https://ai.google.dev/gemini-api/docs/caching
    runtime_strategy: platform_cached

  - id: google_gems_overview
    short_name: google_gems_overview
    platform: Google Gemini
    topic_keywords: Gem creation, 4 pillars (persona/task/context/format), knowledge files, system instructions, sharing
    source_url: https://support.google.com/gemini/answer/15146780
    runtime_strategy: platform_cached

  - id: google_adk_multi_agents
    short_name: google_adk_multi_agents
    platform: Google ADK
    topic_keywords: sub_agents list, parent_agent, transfer_to_agent, AgentTool wrapper, SequentialAgent/ParallelAgent/LoopAgent, output_key, escalate=True
    source_url: https://adk.dev/agents/multi-agents/
    runtime_strategy: platform_cached

  - id: google_adk_a2a
    short_name: google_adk_a2a
    platform: Google ADK
    topic_keywords: Agent2Agent protocol hub page, 7 child page links (navigation only)
    source_url: https://adk.dev/a2a/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_intro
    short_name: google_adk_a2a_intro
    platform: Google ADK
    topic_keywords: A2A protocol overview, AgentCard, Skills, Messages, Tasks, RemoteA2aAgent
    source_url: https://adk.dev/a2a/intro/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_exposing
    short_name: google_adk_a2a_quickstart_exposing
    platform: Google ADK
    topic_keywords: Expose A2A agent (Python) AgentCard authoring, to_a2a wrapper, agent_executor, app_builder
    source_url: https://adk.dev/a2a/quickstart-exposing/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_exposing_go
    short_name: google_adk_a2a_quickstart_exposing_go
    platform: Google ADK
    topic_keywords: Expose A2A agent (Go) — code samples
    source_url: https://adk.dev/a2a/quickstart-exposing-go/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_exposing_java
    short_name: google_adk_a2a_quickstart_exposing_java
    platform: Google ADK
    topic_keywords: Expose A2A agent (Java) — code samples
    source_url: https://adk.dev/a2a/quickstart-exposing-java/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_consuming
    short_name: google_adk_a2a_quickstart_consuming
    platform: Google ADK
    topic_keywords: Consume remote A2A agent (Python) RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH, task lifecycle
    source_url: https://adk.dev/a2a/quickstart-consuming/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_consuming_go
    short_name: google_adk_a2a_quickstart_consuming_go
    platform: Google ADK
    topic_keywords: Consume remote A2A agent (Go) — code samples
    source_url: https://adk.dev/a2a/quickstart-consuming-go/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_quickstart_consuming_java
    short_name: google_adk_a2a_quickstart_consuming_java
    platform: Google ADK
    topic_keywords: Consume remote A2A agent (Java) — code samples
    source_url: https://adk.dev/a2a/quickstart-consuming-java/
    runtime_strategy: platform_cached

  - id: google_adk_a2a_extension
    short_name: google_adk_a2a_extension
    platform: Google ADK
    topic_keywords: ADK extension to A2A state propagation, artifact transfer, ADK metadata in AgentCard
    source_url: https://adk.dev/a2a/a2a-extension/
    runtime_strategy: platform_cached

  - id: openai_agents_sdk
    short_name: openai_agents_sdk
    platform: OpenAI
    topic_keywords: agents, handoffs, guardrails, lifecycle hooks, tool_choice, structured output, MCP, multi-agent patterns
    source_url: https://openai.github.io/openai-agents-python/
    runtime_strategy: platform_cached

  - id: openai_multi_agent
    short_name: openai_multi_agent
    platform: OpenAI
    topic_keywords: Agents-as-tools vs Handoffs decision matrix, LLM-orchestrated vs code-orchestrated, manager-style
    source_url: https://openai.github.io/openai-agents-python/multi_agent/
    runtime_strategy: platform_cached

  - id: openai_handoffs
    short_name: openai_handoffs
    platform: OpenAI
    topic_keywords: Handoff object, tool_name_override (transfer_to_<agent_name>), on_handoff, input_filter, HandoffInputData, RECOMMENDED_PROMPT_PREFIX
    source_url: https://openai.github.io/openai-agents-python/handoffs/
    runtime_strategy: platform_cached

  - id: openai_agents_class
    short_name: openai_agents_class
    platform: OpenAI
    topic_keywords: Agent class, Agent.as_tool() (delegate_to_* peer), tool_use_behavior, dynamic instructions, output_type
    source_url: https://openai.github.io/openai-agents-python/agents/
    runtime_strategy: platform_cached

  - id: openai_running_agents
    short_name: openai_running_agents
    platform: OpenAI
    topic_keywords: Runner.run/run_sync/run_streamed, max_turns/MaxTurnsExceeded, RunConfig, 4 persistence strategies, exception hierarchy
    source_url: https://openai.github.io/openai-agents-python/running_agents/
    runtime_strategy: platform_cached

  - id: openai_tracing
    short_name: openai_tracing
    platform: OpenAI
    topic_keywords: Trace/Span, agent_span, handoff_span, parent_id (peer of Anthropic parent_tool_use_id), sensitive-data controls, 30+ integrations
    source_url: https://openai.github.io/openai-agents-python/tracing/
    runtime_strategy: platform_cached

  - id: openai_file_search
    short_name: openai_file_search
    platform: OpenAI
    topic_keywords: file_search Responses API tool, vector_store_ids, max_num_results, include=file_search_call.results, metadata filters, 22+ formats
    source_url: https://developers.openai.com/api/docs/guides/tools-file-search
    runtime_strategy: platform_cached

  - id: xai_overview
    short_name: xai_overview
    platform: xAI
    topic_keywords: 4 APIs (Responses/Voice/Imagine Images+Video), grok-4.3, OpenAI-compat client, base URL https://api.x.ai/v1
    source_url: https://docs.x.ai/docs/overview
    runtime_strategy: platform_cached

  - id: xai_multi_agent
    short_name: xai_multi_agent
    platform: xAI
    topic_keywords: agent_count=4 or 16, grok-4.20-multi-agent, leader-agent synthesis, use_encrypted_content, built-in-tools-only, Chat Completions incompatible
    source_url: https://docs.x.ai/developers/model-capabilities/text/multi-agent
    runtime_strategy: platform_cached

  - id: xai_grok_multi_agent_model_card
    short_name: xai_grok_multi_agent_model_card
    platform: xAI
    topic_keywords: Grok 4.20 multi-agent model card 2M context, pricing $1.25/$0.20/$2.50 per 1M, 1800 RPM, 10M TPM, us-east-1 + eu-west-1, 6 aliases
    source_url: https://docs.x.ai/developers/models/grok-4.20-multi-agent-0309
    runtime_strategy: platform_cached

  - id: xai_collections
    short_name: xai_collections
    platform: xAI
    topic_keywords: collections_search tool (RAG), citation URI collections://<collection_id>/files/<file_id>, peer of OpenAI file_search
    source_url: https://docs.x.ai/docs/guides/tools/collections-search-tool
    runtime_strategy: platform_cached

provenance:
  sources:
    - source_docs/_refresh_log.json (sources keys + fetch_status + size context for all 34 cached docs)
    - update_agents/doc_refresh_agent.json → primary_data.sources[] (platform, label, source_url, section_focus)
  last_reviewed: 2026-05-13

metadata:
  facts_count: 34
  platforms: [Anthropic, Google Gemini, Google ADK, OpenAI, xAI]
  platform_breakdown:
    Anthropic: 7
    Google ADK: 10
    Google Gemini: 6
    OpenAI: 7
    xAI: 4
---

# Source Docs Index

> Reference. Lookup table of the 34 cached platform documentation files in `source_docs/` — keyed by short_name, with platform, topic keywords, and source URL.

**Scope**: Catalogs every doc currently cached in `source_docs/*.md` so consumers (`doc_analysis_agent`, `merge_agent`, future agents) can resolve a short_name to its platform / topic / URL without grepping the cache or re-reading `_refresh_log.json` and `doc_refresh_agent.json` together. Bounds OUT: live-doc fetching (that's `doc_refresh_agent`), proposal generation (that's `doc_analysis_agent`), and any per-doc body content (the cached `.md` files themselves remain the body authority).

**Provenance**: See YAML frontmatter → `provenance` block.

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

- `knowledge/behavioral_discipline.md` — the universal discipline (YAML frontmatter + narrative); consumed by every agent including the ones that read this index.

## Entries

The 34 entries are enumerated in YAML frontmatter → `facts[]`. Each entry carries: `short_name`, `platform`, `topic_keywords`, `source_url`, `runtime_strategy` (`platform_cached` for all 34, since each is already cached locally in `source_docs/`).

Below is a per-platform summary for human scanning; the authoritative list is in the frontmatter.

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

With 34 entries each carrying short_name + platform + topic keywords + URL + runtime_strategy, the frontmatter body comfortably exceeds the 8000-token embed threshold. Consumers should retrieve this file at runtime rather than embed it in the system prompt of every call. See `runtime_strategy` in the YAML frontmatter.
