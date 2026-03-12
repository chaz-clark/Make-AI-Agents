---
platform: Anthropic
label: Claude Agents Overview
source_url: https://docs.anthropic.com/en/docs/build-with-claude/agents
last_fetched: 2026-03-11
fetch_status: failed
fetch_error: URL 404s at redirect destination (platform.claude.com). Content distributed across tool-use and agent-sdk pages.
notes: See anthropic_tool_use.md and anthropic_agent_sdk.md for current content. Manually re-fetch when this URL becomes stable.
---

## Status

This page could not be fetched on 2026-03-11. The URL redirects to platform.claude.com where the `/agents` path returns 404.

The agents overview content appears to be distributed across:
- **anthropic_tool_use.md** — tool patterns, best practices, tool_choice, parallel/sequential
- **anthropic_agent_sdk.md** — Agent SDK, subagents, sessions, hooks, compaction

## How to Update This File

1. Visit: https://docs.anthropic.com/en/docs/build-with-claude/agents
2. If the page is now live, copy the substantive content here
3. Update `last_fetched` and `fetch_status` in the header
4. Re-run the update_agent analysis

## Key Concepts Expected Here (from prior knowledge)

When available, this page should cover:
- Agent orchestration patterns (single-agent vs multi-agent)
- When to use agents vs simple API calls
- Agent design principles (minimal footprint, human checkpoints)
- Memory patterns (in-context, external, knowledge base)
- Safety and guardrail recommendations
