# Doc Update System — Overview

> **This file is a navigation guide.** The update system has been split into two focused agents. Use the agents below directly.

---

## Two-Agent Architecture

The documentation update system uses two separate agents with distinct responsibilities:

| Agent | Files | What it does |
|-------|-------|-------------|
| **Doc Refresh Agent** | `doc_refresh_agent.md` / `doc_refresh_agent.json` | Fetches live AI platform documentation and writes results to `source_docs/` cache files |
| **Doc Analysis Agent** | `doc_analysis_agent.md` / `doc_analysis_agent.json` | Reads cached docs, diffs against templates, scores candidates, proposes additive improvements |

---

## Workflow

```
1. Run doc_refresh_agent   →   updates source_docs/ cache files (9 sources: agent/API + Gems)
2. Run doc_analysis_agent  →   presents scored proposals for approval
3. Approve proposals       →   agent applies changes to make_agent.*, make_gems/make_gem.*, and make_gems/make_gem_qc.*
4. Run make_agent_qc       →   validates updated templates
```

Each agent runs independently. Refresh only when sources are stale (default threshold: 30 days). Analysis can run offline on the existing cache.

---

## Why Split?

- **Fetching** and **analyzing** are unrelated responsibilities with different failure modes
- The refresh agent needs WebFetch access; the analysis agent needs only local file reads
- Separating them makes each agent simpler, more testable, and easier to audit

---

## Quick Links

- **Start a refresh run**: See `doc_refresh_agent.md` → Agent Quickstart
- **Start an analysis run**: See `doc_analysis_agent.md` → Agent Quickstart
- **Source cache files**: `source_docs/` folder (9 files: 7 agent/API sources + 2 Google Gems sources)
- **Update targets**: `make_agent.md`, `make_agent.json`, `make_gems/make_gem.md`, `make_gems/make_gem.json`, `make_gems/make_gem_qc.md`, `make_gems/make_gem_qc.json`
