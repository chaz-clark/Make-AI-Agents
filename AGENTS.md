# Make-AI-Agents

A build workspace for AI agents and Gemini Gems, plus the meta-templates that generate them. Agents and Gems are drafted here, then moved to their own dedicated repos when ready.

## Project Purpose

**This is**:
- A drafting space for AI agent specs (`make_agent` template family)
- A drafting space for Gemini Gem instructions (`make_gem` template family)
- The home of `knowledge/behavioral_discipline.md/.json` — the Toyota Way + Karpathy discipline that every agent built here inherits
- The home of `make_AGENTS.md/.json` — the template that generates project-level `AGENTS.md` files (this file is its first output)
- A reference repo: completed agents leave for their own repos but the templates and discipline stay

**This is NOT**:
- A deployable package — no `__init__.py`, `setup.py`, `pyproject.toml`, or root-level `requirements.txt`
- A monorepo — no shared imports between agent folders
- A deployment target — nothing here ships directly to production

**Audience**: Developers building AI agents that serve non-technical end users (instructors, analysts, support staff, line-of-business folks). The templates are tool-agnostic but the discipline assumes the end-user trust problem.

## Structure

Tracked content only (gitignored files like `GEMINI.md`, `gpt.qmd`, and `qc_reports/` are not listed here).

```
Make-AI-Agents/
├── AGENTS.md                       # this file — project context for any agentic dev tool
├── README.md / README_QC.md / README_Disclosure.md
├── make_agent.md / .json                  # agent spec template (the meta-skill)
├── make_agent_qc.md / .json               # agent spec QC template (20 rules, 17 dimensions)
├── make_AGENTS.md / .json                 # AGENTS.md generation template (sibling)
├── make_orchestrator_agent.md / .json     # multi-agent orchestrator template (sibling, 2026-05-13)
├── make_agent_knowledge.md / .json        # runtime knowledge file template (sibling, 2026-05-13)
├── make_gems/                             # Gemini Gem templates and example Gems
│   ├── make_gem.md / .json
│   ├── make_gem_qc.md / .json
│   ├── README_GEM.md
│   ├── course_info_bot.json               # example Gem (Engineering Statistics course bot)
│   ├── implement_gem.md / .json           # implementation guide for compiled Gems
│   └── gem_instructions/                  # compiled .txt outputs (gitignored)
├── knowledge/                             # source-of-truth knowledge files
│   └── behavioral_discipline.md / .json   # 10 principles, 5 interaction patterns
├── update_agents/                         # doc refresh + analysis agents + utilities
│   ├── update_agent.md / .json            # entry-point / orchestration
│   ├── doc_refresh_agent.md / .json       # spec for the refresh workflow (uses fetch_doc.py)
│   ├── doc_analysis_agent.md / .json      # spec for the analysis workflow
│   └── fetch_doc.py                       # raw-HTTP doc fetcher (5 modes, 2026-05-13)
├── source_docs/                           # 34 cached platform docs (Anthropic / Google ADK / OpenAI / xAI)
│   └── dropbox/                           # staging folder for manual fetches (gitignored)
├── handoffs/                              # cross-repo handoff documents (currently empty)
└── temp/                                  # subtree: andrej-karpathy-skills (reference, optional pull-back)
```

## Working Style

This project follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. **Read that file before doing non-trivial work in this repo.**

The four no-override principles — **P-001 Read Before Claiming, P-003 Stop on Defect, P-007 Pull Don't Push, P-010 Respect Intent** — apply unconditionally. The other six (P-002, P-004, P-005, P-006, P-008, P-009) have documented override conditions; see the discipline file.

**Where to start reading** (suggested first-pass order for new contributors):
1. This file — project context (you're here)
2. `knowledge/behavioral_discipline.md` — the discipline that governs every change
3. `make_agent.md` — the meta-skill template (read for understanding, not for memorization)
4. An existing artifact in `update_agents/` for an example of a fully-formed agent spec

**Project-specific rules** (carried from the previous CLAUDE.md):

- **No `__init__.py` or init files anywhere** — agents are standalone, not importable modules.
- **No root-level `requirements.txt`** — each agent carries its own dependencies when moved.
- **No packaging or CI/CD config** — this is a drafting space, not a pipeline.
- **When an agent is complete, it moves to its own repo.** The folder here can stay as a reference or be deleted.
- **Gems compile** to a `.txt` file in `make_gems/gem_instructions/` and a `.json` alongside `make_gem.md`.
- **Templates evolve in pairs** — `make_*.md` (narrative) and `make_*.json` (structured rules) are updated together. Same applies to `knowledge/behavioral_discipline.md/.json`.
- **Updates to `make_agent.md` cascade** — every agent spec generated from it after the change should be regenerated or audited against the new template via `make_agent_qc`.
- **Make-AI-Agents is the leverage point; consumer repos are the field for Genchi Genbutsu (P-001).** This repo holds the meta-skills (`make_agent`, `make_orchestrator_agent`, `make_agent_knowledge`, etc.) and the discipline. Consumer repos (canvas-toolbox, AgentJ, course repos) USE the skills to generate real artifacts. When an agent in this repo is invoked to "test the skill on" a consumer repo, the goal is **skill improvement here**, NOT to finish the consumer repo's work. Capture what surfaces, fix the skill, commit the skill fix here, hand the field state back to the consumer repo's own agents/maintainers to commit there. Don't cross the boundary: this repo's commits update meta-skills; consumer-repo commits update generated artifacts.

## Active Context

_Last updated: 2026-05-13_

**Recent shipped (2026-05-12 → 2026-05-13)**:
- **`make_orchestrator_agent`** (commit `e539532`) — new sibling skill that generates multi-agent orchestrator specs. Specialists declared by `spec_path`; LLM-routed via auto-generated `delegate_to_<specialist>` tools. Platform coverage: Anthropic subagents / OpenAI Handoffs / Google ADK `sub_agents` as direct targets; xAI documented as exception (anonymous server-side workers).
- **`make_agent_knowledge`** (commit `e539532`) — new sibling skill that generates runtime knowledge files (`knowledge/*.md` + `.json` pairs). Three shapes: reference, identity, procedural. Authoring scaffold only. `_metadata.runtime_strategy` declares embed vs read-at-runtime per body-size thresholds.
- **`make_agent_qc`** rules 19 (`ORCH-QC-001..005`) + 20 (`KNW-QC-001..006`) — extends QC to cover the new artifact types. Total: 20 rules, 17 quality dimensions.
- **`make_agent.json` v3.4–v3.6** — applied 6 doc-analysis proposals (strict tool use, reasoning effort, MCP preference, server/client tool pitfall, memory/state strategy, Gemini-3 temperature exception). `cross_references.knowledge_files[]` field added.
- **`update_agents/fetch_doc.py`** (commit `a38de4e`, `49f1374`) — raw-HTTP doc fetcher with 5 modes (default, `--list-links`, `--batch`, `--from-html`, `--check`). Replaces the WebFetch+manual-save workflow that was producing small-model summaries. Validated 2026-05-13: byte-identical to manual saves on 11 of 11 sources from 5 platforms.
- **`source_docs/` 9 → 34 sources** — wave-2 added 17 sources to ground the 2 new skills; the new tool then snagged 8 ADK A2A child pages and refreshed `google_adk_multi_agents` (+20% from upstream language tabs).
- **`doc_refresh_agent.json` v1.3** — Step 2 (Fetch) rewritten to recommend `fetch_doc.py`; `--from-html` documented as the manual fallback.

**In flight**: nothing — all queued work in this wave landed.

**Open issues** (check GitHub for current state — `gh issue list`): the v3.0–v3.6 polish series (issues #1–#9) is closed. New work would open new issues.

**Next likely**:
- **🔝 NEXT QUEUED — Cross-repo AGENTS.md audit + regenerate-and-deliver workstream** (queued 2026-05-13 after commit `63bd64e` raised the make_AGENTS bar): every consumer repo (public + local masters) likely has an AGENTS.md that predates the current standards (especially AGENTS-QC-006 — discipline files co-located, not just pointed at), OR is still on CLAUDE.md. Step 1 (enumeration) completed 2026-05-13.

  **Current-sprint scope (5 targets — audit/migrate existing context):**
  - `handoff` (GitHub) — has AGENTS.md (9 KB, seed stage); audit against AGENTS-QC-001..006; deliver via handoff convention
  - `ds460-master` (local) — has AGENTS.md (9.9 KB); audit + package discipline locally (no push)
  - `ds250-onln-master` (local) — CLAUDE.md (21.9 KB) → AGENTS.md migration; canvas_toolbox/ clone present; local only
  - `itm327-master` (local) — CLAUDE.md (11.7 KB) → AGENTS.md migration; gh_issues_agent/ clone present; local only
  - `m119-master` (local) — CLAUDE.md (2.7 KB, sparse) → AGENTS.md migration; canvas_toolbox/ clone present; local only

  **Next-sprint scope (4 targets — optional creates, no existing context to preserve):**
  - `agentj` (GitHub) — no AGENTS.md, no CLAUDE.md; AI agent runtime, peer repo mentioned in handoff/canvas-toolbox docs as a subtree consumer
  - `m119-site` (GitHub) — no AGENTS.md, no CLAUDE.md; BYU-Idaho course site, recent activity
  - `DS250-Course-Polars` (GitHub) — no AGENTS.md, no CLAUDE.md; DS250 course; agents likely work on it without project context today
  - `gh-issues-agent` (GitHub) — no AGENTS.md, no CLAUDE.md, BUT already carries a `knowledge/` folder with 6 topic files (agile_sprint, canvas_api_gotchas, gh_issues_agent_mission, github_issues_reference, semantic_versioning, sprint_qc). Adding AGENTS.md would (a) give agents working on the tool itself project context, (b) make it a model "agent skill" repo with the discipline embedded, and (c) document it as a consumable-by-other-repos skill for cross-clone reuse. Should also package behavioral_discipline.{md,json} into its existing knowledge/ folder per AGENTS-QC-006 condition (a). Sprint-1 step-2 audit added it post-hoc after the maintainer flagged the omission 2026-05-13.

  **Skipped (out of scope):**
  - `Make-AI-Agents` — source of truth, passes AGENTS-QC-006 by construction
  - `canvas-toolbox` — already audited 2026-05-13, passes via condition (b)
  - Tutorial repos / forks / legacy single-purpose repos / `andrej-karpathy-skills` (upstream CLAUDE.md intentional)

  **6-step workstream applied per target:**
  1. ✅ Enumerate Chaz's repos (public + local masters) — done 2026-05-13. **GG learning from sprint 2 (added 2026-05-13)**: step 1 must check BOTH the local working tree AND GitHub-side state. The initial enumeration used `gh api repos/<owner>/<repo>/contents/AGENTS.md` which only sees PUSHED state. 2 of 4 sprint-2 targets (`agentj`, `gh-issues-agent`) had local-but-not-pushed `AGENTS.md` files that triggered P-003 halts mid-sprint. Future cross-repo audits should run `ls <local-path>/AGENTS.md` in addition to `gh api`, then reconcile (a missing GitHub-side AGENTS.md does NOT imply a missing local one). The P-003 halts caught the discrepancy cleanly — subagents were re-launched with the correct refresh framing — but pre-enumeration verification would have avoided the halt-and-relaunch cycle.
  2. Audit each current-sprint target against AGENTS-QC-001..006 + the full required-sections contract.
  3. For each behind-the-curve target, run current make_AGENTS to generate `AGENTS_updated.md` (suffixed to avoid overwriting; preserves OG Active Context / Domain Terms / Existing Tooling / project-specific rules).
  4. Package `behavioral_discipline.{md,json}` into each target's `knowledge/` folder per AGENTS-QC-006 (snapshot header for traceability).
  5. **Public targets:** deliver via handoff convention (per `chaz-clark/handoff` issue #6 — producer-delivers direction) — handoff doc + `AGENTS_updated.md` + discipline files. **Local-only targets** (ds*-master, itm327-master, m119-master): apply directly in the local working tree; do NOT push.
  6. Track per-repo state via the handoff convention's Status enum (proposed in handoff issue #3) for the public targets; local targets just need a commit in their own repo.
- Genchi Genbutsu (GG) the new skills further as they're used in canvas-toolbox / AgentJ — any GG findings fold back here.
- Wave 4 doc-analysis cycle when source_docs next refreshes.
- Operationalize `doc_refresh_agent` as a runner (Python) on top of `fetch_doc.py`, enabling scheduled refreshes.
- Pop `temp/` subtree updates back upstream when ready (or migrate `temp/` from subtree → clone+gitignore per the 2026-05-13 cross-project rule).

## Existing Tooling

Before generating new tools or scripts in this repo, reuse what already exists.

| Tool / File | Purpose | When to use |
|---|---|---|
| `make_agent.md` / `.json` | Generate agent specs (the meta-skill) | Building any new single agent |
| `make_agent_qc.md` / `.json` | Validate agent specs (20 rules, 17 dimensions; covers BD-QC, ORCH-QC, KNW-QC families) | After generating any new agent |
| `make_AGENTS.md` / `.json` | Generate `AGENTS.md` for a project | Setting up a new project, migrating from `CLAUDE.md` |
| `make_orchestrator_agent.md` / `.json` | Generate multi-agent orchestrator specs (`agent_type.type: 'multi_agent'`) that delegate to specialist subagents | When a single agent has > 20 tools or spans multiple domains — split into specialists + orchestrator |
| `make_agent_knowledge.md` / `.json` | Generate runtime knowledge files (MD+JSON pair in `knowledge/`) in three shapes (reference / identity / procedural) | When an agent needs lookup-shaped, principle-shaped, or playbook-shaped knowledge at runtime |
| `make_gems/make_gem.md` / `.json` | Generate Gemini Gem instructions | Building any new Gem |
| `make_gems/make_gem_qc.md` / `.json` | Validate Gem instructions | After generating any new Gem |
| `knowledge/behavioral_discipline.md` / `.json` | Source of truth for the discipline embedded in every generated artifact | Read once for context; reference by path in generated specs |
| `update_agents/doc_refresh_agent.*` | Spec for the refresh workflow (staleness → fetch → validate → write → report) | Monthly or after major platform releases. Step 2 (Fetch) uses `fetch_doc.py` |
| `update_agents/doc_analysis_agent.*` | Diff cached docs against templates and propose updates | After running a refresh — finds convergence-bonus candidates across platforms |
| `update_agents/fetch_doc.py` | Raw-HTTP doc fetcher; 5 modes: default fetch, `--list-links` (discover child URLs), `--batch`, `--from-html` (convert browser-saved HTML), `--check` (drift detection vs an existing source_docs file) | Whenever a `source_docs/` file is stale or new. Run via `uv run update_agents/fetch_doc.py <url>` — PEP 723 inline metadata handles deps |

**Reuse-first rule**: if a template, validation, or knowledge file already covers a needed operation, use it rather than generating new code or new templates.

**How to invoke a meta-skill**: every `make_*.md` file is an LLM prompt-as-skill, not a script. To run one:

1. Open the meta-skill's `.md` and `.json` in your agentic dev tool (Claude Code, Cursor, Aider, Antigravity).
2. State the task, e.g. *"Use `make_agent` to draft a spec for an X agent."* The tool reads the meta-skill files as instructions and applies them to your request.
3. Follow the meta-skill's Quickstart steps with the LLM. For agent specs, that includes choosing an `interaction_pattern` and embedding the behavioral discipline (step 0 of `make_agent.md` Quickstart).
4. Validate the generated artifact with the matching `*_qc` meta-skill. Output goes wherever the LLM writes it; review reports manually or save to `qc_reports/` (gitignored).

There is no CLI or build step. The repo is a knowledge base + prompt library, not a pipeline.

**Worked example** — running `make_agent_qc` against an existing spec:

> *"Use `make_agent_qc.md` and `make_agent_qc.json` to validate `update_agents/doc_refresh_agent.md` and `update_agents/doc_refresh_agent.json`. Score against all 18 rules and 15 quality dimensions. Report critical issues first."*

The LLM reads the QC meta-skill, reads the target spec, runs the rule set, and returns a structured report. Save the report to `qc_reports/` if you want to keep it.

## Domain Terms

| Term | Definition |
|---|---|
| `interaction_pattern` | The behavioral profile of an agent — drives which discipline principles apply. One of: `read_only`, `single_write_workflow`, `multi_step_batch`, `single_call_api`, `conversational`. Distinct from `agent_type.type` (which is the implementation pattern). See `knowledge/behavioral_discipline.json` → `agent_type_applicability.types`. |
| `agent_type.type` | The **implementation** pattern of an agent (`class_based`, `llm_agent`, `api_agent`, `data_processor`, `multi_agent`, `workflow`, `rule_based`, `other`). Orthogonal to `interaction_pattern`. |
| `P-001` … `P-010` | Stable IDs for the ten behavioral discipline principles. P-001 = Read Before Claiming, P-003 = Stop on Defect, P-007 = Pull Don't Push, P-010 = Respect Intent — these four are no-override. See `knowledge/behavioral_discipline.md` → "The Ten Principles". |
| `BD-QC-001` … `BD-QC-007` | Stable IDs for behavioral discipline QC checks. Defined in `knowledge/behavioral_discipline.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_ids 17 and 18. |
| `ORCH-QC-001` … `ORCH-QC-005` | Stable IDs for orchestrator-spec QC checks. Defined in `make_orchestrator_agent.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_id 19. Applies only when `agent_type.type: 'multi_agent'`. |
| `KNW-QC-001` … `KNW-QC-006` | Stable IDs for knowledge-file QC checks. Defined in `make_agent_knowledge.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_id 20. Applies only when an agent has non-empty `cross_references.knowledge_files[]`. |
| `make_*` | Naming convention for **meta-skills** (templates that generate other things). `make_agent` generates single agents, `make_orchestrator_agent` generates multi-agent orchestrators, `make_agent_knowledge` generates runtime knowledge files, `make_gem` generates Gem instructions, `make_AGENTS` generates `AGENTS.md` files. |
| `compact_boilerplate` | Template strings (in the `*.json` of a meta-skill) that get substituted into generated outputs. The discipline propagates through these. |
| `non_interactive_mode` (NI mode) | An agent runs without a synchronous user (cron, webhook, scheduled batch). Opt-in graduation path — agents are validated interactively first. Requires an `alert_channel` (BD-QC-007). |
| `subtree` | Refers to `temp/` — a `git subtree` of `andrej-karpathy-skills` for reference. Updates can be pulled in or pushed back per `git subtree pull` / `git subtree push`. |
| `NGAI` | "Non-General AI" — the project's framing for what this repo produces: purpose-built specialist agents (and Gems) rather than general-purpose chatbots. Each agent built from `make_agent.md` is an NGAI specialist with a specific mission, contract, and behavioral discipline. The term appears in README and historical context (e.g., `README_Disclosure.md`); use it when discussing the project's design philosophy with stakeholders. |

---

_AGENTS.md last revised 2026-05-13. Generated 2026-04-29 using `make_AGENTS.md` v1.0; revised in-place for the wave-2 additions (make_orchestrator_agent, make_agent_knowledge, fetch_doc.py, source_docs 9 → 34). Maintenance: update Active Context after major shipped work; refresh other sections only when the underlying truth changes._
