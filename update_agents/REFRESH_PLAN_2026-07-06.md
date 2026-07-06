# Documentation Refresh Plan — 2026-07-06

## Executive Summary

- **Existing sources**: 35 (all stale, last refresh May 13, 2026 — 54 days ago)
- **New sources discovered**: 32
- **Total sources after refresh**: 67
- **Staleness threshold**: 30 days
- **Method**: 5-tier fetch system (GitHub API → HTTP → Playwright → Manual → Downloads scan)

## Discovery Summary

### Major Platform Updates Since May 2026

1. **Anthropic**: Launched Claude Managed Agents (beta: `managed-agents-2026-04-01`)
2. **Google Gemini**: Interactions API GA (June 2026), Antigravity + Deep Research agents
3. **Google ADK**: Version 2.0 GA (Python May, Go June) with graph-based workflows
4. **OpenAI**: Sandbox Agents beta, gpt-5.4-mini/5.5 defaults, Realtime API GA
5. **xAI**: Voice Agent API, Grok Build (coding model), Remote MCP support, Speech APIs GA
6. **Nous Research**: Hermes Agent (inspired our knowledge/learned/ pattern)

---

## Existing Sources to Refresh (35)

### Anthropic (7)
1. `anthropic_agents.md` — Agent Skills overview
2. `anthropic_tool_use.md` — Tool use guide
3. `anthropic_agent_sdk.md` — Claude Agent SDK
4. `anthropic_subagents.md` — Subagents reference
5. `anthropic_prompt_caching.md` — Prompt caching
6. `anthropic_citations.md` — Citations
7. `anthropic_files.md` — Files API

### Google Gemini API (4)
8. `google_gemini_agentic.md` — Function calling + Google Search
9. `google_structured_output.md` — Structured output
10. `google_files.md` — Files API
11. `google_caching.md` — Context caching

### Google ADK (9)
12. `google_adk_multi_agents.md` — Multi-agent systems
13. `google_adk_a2a.md` — A2A protocol hub
14. `google_adk_a2a_intro.md` — A2A intro
15. `google_adk_a2a_quickstart_exposing.md` — A2A exposing (Python)
16. `google_adk_a2a_quickstart_exposing_go.md` — A2A exposing (Go)
17. `google_adk_a2a_quickstart_exposing_java.md` — A2A exposing (Java)
18. `google_adk_a2a_quickstart_consuming.md` — A2A consuming (Python)
19. `google_adk_a2a_quickstart_consuming_go.md` — A2A consuming (Go)
20. `google_adk_a2a_quickstart_consuming_java.md` — A2A consuming (Java)
21. `google_adk_a2a_extension.md` — A2A extension spec

### Google Gems (2)
22. `google_gems_overview.md` — Gems overview (manual fetch)
23. `google_system_instructions.md` — System instructions

### OpenAI (7)
24. `openai_agents_sdk.md` — Agents SDK overview
25. `openai_multi_agent.md` — Multi-agent orchestration
26. `openai_handoffs.md` — Handoffs
27. `openai_agents_class.md` — Agent class
28. `openai_running_agents.md` — Running agents
29. `openai_tracing.md` — Tracing
30. `openai_file_search.md` — File search tool

### xAI (5)
31. `xai_overview.md` — Grok API overview
32. `xai_multi_agent.md` — Grok multi-agent
33. `xai_grok_multi_agent_model_card.md` — Model card
34. `xai_collections.md` — Collections search tool
35. `xai_files.md` — Files API

---

## New Sources to Add (32)

### Anthropic — Claude Managed Agents (5)
36. `anthropic_managed_agents_overview.md`
    - URL: https://platform.claude.com/docs/en/managed-agents/overview
    - Focus: Managed agents architecture, beta header, use cases

37. `anthropic_managed_agents_quickstart.md`
    - URL: https://platform.claude.com/docs/en/managed-agents/quickstart
    - Focus: Getting started with managed agents

38. `anthropic_managed_agents_tools.md`
    - URL: https://platform.claude.com/docs/en/managed-agents/tools
    - Focus: agent_toolset_20260401, custom tools

39. `anthropic_managed_agents_multi_agent.md`
    - URL: https://platform.claude.com/docs/en/managed-agents/multi-agent
    - Focus: Multi-agent sessions, shared sandbox

40. `anthropic_advisor_tool.md`
    - URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
    - Focus: Executor + advisor model pattern

### Google Gemini API (7)
41. `google_interactions_api.md`
    - URL: https://ai.google.dev/gemini-api/docs/interactions-overview
    - Focus: Interactions API (GA June 2026), server-side state

42. `google_agents_overview.md`
    - URL: https://ai.google.dev/gemini-api/docs/agents
    - Focus: Unified agents overview

43. `google_managed_agents.md`
    - URL: https://ai.google.dev/gemini-api/docs/custom-agents
    - Focus: Building custom managed agents

44. `google_antigravity_agent.md`
    - URL: https://ai.google.dev/gemini-api/docs/antigravity-agent
    - Focus: General-purpose managed agent, secure sandbox

45. `google_deep_research_agent.md`
    - URL: https://ai.google.dev/gemini-api/docs/deep-research
    - Focus: Deep research agent, collaborative planning, MCP

46. `google_coding_agents.md`
    - URL: https://ai.google.dev/gemini-api/docs/coding-agents
    - Focus: Coding assistant with Gemini MCP and Skills

47. `google_mcp_server.md`
    - URL: https://gemini-api-docs-mcp.dev (or docs page describing it)
    - Focus: Public MCP server for Gemini API docs

### Google ADK 2.0 (7)
48. `google_adk_2_0_overview.md`
    - URL: https://adk.dev/2.0/
    - Focus: ADK 2.0 features, graph-based workflows

49. `google_adk_tools_integrations.md`
    - URL: https://adk.dev/integrations/
    - Focus: Tools and integrations catalog

50. `google_adk_streaming.md`
    - URL: https://adk.dev/streaming/
    - Focus: Gemini Live API Toolkit

51. `google_adk_context.md`
    - URL: https://adk.dev/context/
    - Focus: Context management

52. `google_adk_sessions.md`
    - URL: https://adk.dev/sessions/session/
    - Focus: Session tracking for conversations

53. `google_adk_bigquery_analytics.md`
    - URL: https://adk.dev/integrations/bigquery-agent-analytics/
    - Focus: BigQuery Agent Analytics plugin

54. `google_adk_data_agents.md`
    - URL: https://adk.dev/integrations/data-agent/
    - Focus: Google Cloud Data Agents tool

### OpenAI Agents SDK (5)
55. `openai_sandbox_agents.md`
    - URL: https://openai.github.io/openai-agents-python/sandbox_agents/
    - Focus: Sandbox agents beta, persistent workspaces

56. `openai_mcp.md`
    - URL: https://openai.github.io/openai-agents-python/mcp/
    - Focus: Model Context Protocol integration

57. `openai_realtime_api.md`
    - URL: https://openai.github.io/openai-agents-python/ (realtime section)
    - Focus: Realtime API, gpt-realtime-1.5 GA

58. `openai_models.md`
    - URL: https://openai.github.io/openai-agents-python/models/
    - Focus: Model defaults (gpt-5.4-mini, gpt-5.5)

59. `openai_sandbox_guide.md`
    - URL: https://openai.github.io/openai-agents-python/sandbox/guide/
    - Focus: Sandbox concepts and guide

### xAI (7)
60. `xai_voice_agent.md`
    - URL: https://docs.x.ai/developers/model-capabilities/audio/voice-agent
    - Focus: Voice Agent API, custom voices

61. `xai_grok_build.md`
    - URL: https://docs.x.ai/ (Grok Build docs)
    - Focus: Coding model for agentic workflows (beta)

62. `xai_remote_mcp.md`
    - URL: https://docs.x.ai/ (Remote MCP Tools docs)
    - Focus: Remote MCP server integration

63. `xai_speech_to_text.md`
    - URL: https://docs.x.ai/ (STT API docs)
    - Focus: Speech to Text API (GA, 25 languages)

64. `xai_text_to_speech.md`
    - URL: https://docs.x.ai/ (TTS API docs)
    - Focus: Text to Speech API (GA)

65. `xai_imagine.md`
    - URL: https://docs.x.ai/developers/model-capabilities/imagine
    - Focus: Image/video generation, reference-to-video

66. `xai_batch_api.md`
    - URL: https://docs.x.ai/ (Batch API docs)
    - Focus: Batch API with image/video generation

### Nous Research (1)
67. `nous_hermes_agent.md`
    - URL: https://hermes-agent.nousresearch.com/docs/
    - Focus: Auto-distillation, persistent memory, training trajectories

---

## Fetch Strategy by Platform

### Tier 1: GitHub API (Fast, Direct Markdown)
- OpenAI sources (55-59): `openai.github.io` → GitHub API fetch

### Tier 2: Raw HTTP (Most sources)
- Anthropic (36-40)
- Google Gemini (41-47)
- Google ADK (48-54)
- xAI (60-66)
- Nous Hermes (67)

### Tier 3: Playwright (JS-rendered)
- `google_gems_overview.md` (22) — known JS-rendered page

### Tier 4+5: Manual Fallback
- Any source that fails Tier 2/3 → logged to `_manual_needed.json`

---

## Execution Plan

### Phase 1: Add New Sources to doc_refresh_agent.json
Add 32 new source entries with proper metadata

### Phase 2: Refresh in Batches
1. **Batch 1**: OpenAI (12 sources) — test Tier 1 GitHub API
2. **Batch 2**: Anthropic (12 sources) — test Tier 2 HTTP
3. **Batch 3**: Google Gemini API (11 sources)
4. **Batch 4**: Google ADK (16 sources)
5. **Batch 5**: xAI (12 sources)
6. **Batch 6**: Nous Hermes (1 source)
7. **Batch 7**: Google Gems (1 source) — manual or Playwright

### Phase 3: Verify and Report
- Check all files > 500 bytes
- Verify metadata headers
- Report any Tier 4 (manual needed) entries
- Update `_refresh_log.json`

---

## Expected Outcomes

- **All 35 existing sources refreshed** with current content (July 2026)
- **32 new sources added** covering major 2026 platform updates
- **Total: 67 sources** providing comprehensive multi-agent orchestration coverage
- **Updated coverage**:
  - Managed agents (Anthropic, Google)
  - MCP integration (OpenAI, Google, xAI)
  - Voice/audio agents (xAI)
  - Sandbox execution (OpenAI, Google)
  - Graph-based workflows (ADK 2.0)
  - Auto-distillation patterns (Hermes)

---

## Next Steps

1. Review and approve this plan
2. Add new source entries to `doc_refresh_agent.json`
3. Execute batch refresh using `fetch_doc.py`
4. Review results and handle any manual-needed cases
5. Update AGENTS.md Active Context with refresh completion

---

_Plan created: 2026-07-06_
_Execution target: 2026-07-06_
