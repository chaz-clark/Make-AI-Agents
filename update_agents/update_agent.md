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

- **Start a refresh run**: See `doc_refresh_agent.md` → Agent Quickstart
- **Start an analysis run**: See `doc_analysis_agent.md` → Agent Quickstart
- **Source cache files**: `source_docs/` folder (9 files: 7 agent/API sources + 2 Google Gems sources)
- **Update targets**: `make_agent.md`, `make_agent.json`, `make_gems/make_gem.md`, `make_gems/make_gem.json`, `make_gems/make_gem_qc.md`, `make_gems/make_gem_qc.json`
