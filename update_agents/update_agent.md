---
name: update_agent
version: "1.1"
last_updated: 2026-04-29
description: Doc Update Agent - reads cached source docs, diffs against templates, proposes additive improvements (navigation guide - split into focused agents).
deprecated: true
deprecation_note: Split into doc_refresh_agent and doc_analysis_agent. This file preserved for navigation.
agent_type:
  type: workflow
  description: Two-mode workflow - Analysis (read cache → diff → score → propose) and Refresh (fetch live docs → update cache)
behavioral_discipline:
  interaction_pattern: multi_step_batch
  applicable_principles: [P-001, P-002, P-003, P-004, P-005, P-006, P-007, P-008, P-009, P-010]
metadata:
  companion_json_deprecated: "2026-07-08 - consolidated into YAML frontmatter per JSON purge"
  template_version: "1.0"
---

# Doc Update System — Overview

> **This file is a navigation guide.** The update system has been split into two focused agents. Use the agents below directly.

---

## Two-Agent Architecture + Fetch Tool

The documentation update system uses two separate agents plus one utility:

| Component | Files | What it does |
|-------|-------|-------------|
| **Doc Refresh Agent** | `doc_refresh_agent.md` | Spec for the refresh workflow: staleness check → fetch → validate → write → report. Step 2 (Fetch) uses `fetch_doc.py`. (YAML frontmatter) |
| **Doc Analysis Agent** | `doc_analysis_agent.md` | Reads cached docs, diffs against templates, scores candidates, proposes additive improvements (YAML frontmatter) |
| **fetch_doc.py** | `fetch_doc.py` | Raw-HTTP doc fetcher used by the refresh workflow. 5 modes: default fetch, `--list-links` (discover child URLs), `--batch`, `--from-html` (convert browser-saved HTML for JS-rendered sites), `--check` (drift detection). Added 2026-05-13; validated as drop-in replacement for the prior WebFetch+manual-save flow. |

---

## Workflow

```
1. Run doc_refresh_agent          →   uses fetch_doc.py to refresh source_docs/
                                       (34 sources: agent/API + Gems + ADK A2A child pages)
2. Run doc_analysis_agent         →   presents scored proposals for approval
3. Approve proposals              →   agent applies changes to make_agent.*, make_orchestrator_agent.*,
                                       make_agent_knowledge.*, make_gems/make_gem.*, make_gems/make_gem_qc.*
4. Run make_agent_qc              →   validates updated templates (20 rules, 17 dimensions)
```

Each agent runs independently. Refresh only when sources are stale (default threshold: 30 days). Analysis can run offline on the existing cache. `fetch_doc.py` can also be invoked standalone for ad-hoc fetches.

---

## Why Split?

- **Fetching** and **analyzing** are unrelated responsibilities with different failure modes
- The refresh agent needs HTTP access (now via `fetch_doc.py`); the analysis agent needs only local file reads
- The fetch logic lives in `fetch_doc.py` as a reusable utility so each step has one obvious tool
- Separating them makes each agent simpler, more testable, and easier to audit

---

## Behavioral Discipline (core)

This agent (and the two sub-agents it orchestrates) follows the behavioral discipline defined in `../knowledge/behavioral_discipline.md` and `../knowledge/behavioral_discipline.json`. The principles applicable to this agent type (multi_step_batch — multi-resource workflow with writes):

- **P-001 Read Before Claiming** (*Genchi Genbutsu*): Read the actual source-doc cache files and template files before claiming what's missing or stale. *Trigger*: Every claim about cache state, template gaps, or file content.
- **P-002 Plan Before Acting** (*Nemawashi + TBP*): Surface the proposed refresh/analysis/apply plan and wait for confirmation before any non-reversible step. *Trigger*: Any state-changing action (cache overwrite, template edit).
- **P-003 Stop on Defect** (*Jidoka + Andon*): If a fetch fails, a diff is ambiguous, or an applied proposal would conflict with existing content → stop and surface. *Trigger*: Any failure or unresolved ambiguity.
- **P-004 Find the Root Cause** (*5 Whys*): When a proposal score is wrong or a diff misses a real change, walk the cause chain to the structural fault. *Trigger*: Any incorrect proposal or missed pattern.
- **P-005 Small Steps, Evenly Sized** (*Kaizen + PDCA + Heijunka*): Refresh per source; propose per gap; apply per approved proposal. Each step independently verifiable. *Trigger*: Every multi-step pass.
- **P-006 Document the Change** (*A3*): Each applied proposal logs its rationale, source citation, score, and target. *Trigger*: Every approved proposal applied to a template.
- **P-007 Pull, Don't Push** (*JIT + 3 Ms*): Apply only what was approved. No "while I'm in this file" additions. *Trigger*: Every template write.
- **P-008 Mistake-Proof Outputs** (*Poka-yoke + Standard Work*): Proposal output format is identical across runs (numbered list, score, source, target, proposed_text, rationale). *Trigger*: Every analysis pass.
- **P-009 Reflect, and Tell the User** (*Hansei + Yokoten*): When a source surprises us (new pattern, deprecated guidance), name the lesson and add it to the agent's notes. *Trigger*: End of any analysis with non-obvious findings.
- **P-010 Respect the User's Intent** (*Respect for People + Hoshin Kanri*): Never apply a proposal without per-proposal approval. Per-proposal, not bulk approval. *Trigger*: Every proposal evaluation.

**Hard rule on overrides**: before skipping any principle, the agent must state in one sentence which principle is being skipped and why. Principles P-001, P-003, P-007, P-010 have no override.

For full principle definitions, examples, and override rationale, see `../knowledge/behavioral_discipline.md`.

---

## Quick Links

- **Ad-hoc fetch**: `uv run update_agents/fetch_doc.py <url>` — see `fetch_doc.py` docstring for all 5 modes
- **Start a refresh run**: See `doc_refresh_agent.md` → Agent Quickstart
- **Start an analysis run**: See `doc_analysis_agent.md` → Agent Quickstart
- **Source cache files**: `source_docs/` folder (34 files: 9 original + 17 wave-2 + 8 ADK A2A child pages)
- **Update targets**: `make-agent.md`, `make_agent.json`, `make-orchestrator-agent.md`, `make_orchestrator_agent.json`, `make-agent-knowledge.md`, `make_agent_knowledge.json`, `make_gems/make_gem.md`, `make_gems/make_gem.json`, `make_gems/make_gem_qc.md`, `make_gems/make_gem_qc.json`
