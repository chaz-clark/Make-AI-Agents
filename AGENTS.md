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
├── make_agent.md / .json           # agent spec template (the meta-skill)
├── make_agent_qc.md / .json        # agent spec QC template
├── make_AGENTS.md / .json          # AGENTS.md generation template (sibling)
├── make_gems/                      # Gemini Gem templates and example Gems
│   ├── make_gem.md / .json
│   ├── make_gem_qc.md / .json
│   ├── README_GEM.md
│   ├── course_info_bot.json        # example Gem (Engineering Statistics course bot)
│   ├── implement_gem.md / .json    # implementation guide for compiled Gems
│   └── gem_instructions/           # compiled .txt outputs (gitignored)
├── knowledge/                      # source-of-truth knowledge files
│   └── behavioral_discipline.md / .json   # 10 principles, 5 interaction patterns
├── update_agents/                  # doc refresh + analysis agents
│   ├── update_agent.md / .json     # entry-point / orchestration
│   ├── doc_refresh_agent.md / .json
│   └── doc_analysis_agent.md / .json
├── source_docs/                    # cached platform docs (Anthropic / Google / OpenAI / xAI)
├── handoffs/                       # cross-repo handoff documents (currently empty)
└── temp/                           # subtree: andrej-karpathy-skills (reference, optional pull-back)
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

## Active Context

_Last updated: 2026-04-29_

**Recent shipped**:
- **v3.0** (commit `ebb5ae0`) — behavioral discipline baked into `make_agent` + `make_agent_qc`. 10 principles with stable IDs, 5 interaction patterns, 18 QC rules across 15 quality dimensions, non-interactive mode graduation pattern.
- **Checkpoint** (commit `aaeddc8`) — `knowledge/behavioral_discipline.md/.json` and README updates.

**In flight**:
- `make_AGENTS.md/.json` — bare-bones template just drafted (today). This `AGENTS.md` is its first output.
- `CLAUDE.md` → `AGENTS.md` migration — see Migration Notes below.

**Open issues** (8 total — see GitHub):
- v3.1 polish: #3-#8 (decision flow evaluation order, validation wiring, NI mode mid-spec, legacy migration, etc.)
- #2 — Toyota Way skill in `temp/` subtree (companion to karpathy-guidelines)
- #1 — explicit `.gitignore` for local scratch files (subtree consumer hygiene)

**Next likely**:
- Iterate on `AGENTS.md` (this file) via sub-agent reviews
- Build `make_AGENTS_qc.md/.json` as a sibling QC for AGENTS.md generation
- Discipline integration into `make_gem.md` + `make_gem_qc.md`
- Pop `temp/` subtree updates back upstream when ready

## Migration Notes

**CLAUDE.md → AGENTS.md** (in progress, 2026-04-29):

`AGENTS.md` is the tool-agnostic standard readable by Claude Code, Cursor, Aider, Antigravity, and other agentic dev tools. `CLAUDE.md` is Claude-specific naming. Once `AGENTS.md` is validated and stable, the next step is:

1. `git rm CLAUDE.md`
2. Apply the deferred `.gitignore` line that adds `CLAUDE.md` to ignore (already in working tree, not committed)
3. Verify no references to `CLAUDE.md` remain in repo content (READMEs, etc.)
4. Commit + push as a follow-up minor revision

Until that step lands, both `AGENTS.md` and `CLAUDE.md` exist; `AGENTS.md` is canonical (per the user's global instruction: "If both exist, treat `AGENTS.md` as canonical and the `CLAUDE.md` as a stale shim").

## Existing Tooling

Before generating new tools or scripts in this repo, reuse what already exists.

| Tool / File | Purpose | When to use |
|---|---|---|
| `make_agent.md` / `.json` | Generate agent specs (the meta-skill) | Building any new agent |
| `make_agent_qc.md` / `.json` | Validate agent specs (18 rules, 15 dimensions) | After generating any new agent |
| `make_AGENTS.md` / `.json` | Generate `AGENTS.md` for a project | Setting up a new project, migrating from `CLAUDE.md` |
| `make_gems/make_gem.md` / `.json` | Generate Gemini Gem instructions | Building any new Gem |
| `make_gems/make_gem_qc.md` / `.json` | Validate Gem instructions | After generating any new Gem |
| `knowledge/behavioral_discipline.md` / `.json` | Source of truth for the discipline embedded in every generated artifact | Read once for context; reference by path in generated specs |
| `update_agents/doc_refresh_agent.*` | Fetch latest platform docs (Anthropic/Google/OpenAI/xAI) | Monthly or after major platform releases |
| `update_agents/doc_analysis_agent.*` | Diff cached docs against templates and propose updates | After running `doc_refresh_agent` |

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
| `make_*` | Naming convention for **meta-skills** (templates that generate other things). `make_agent` generates agent specs, `make_gem` generates Gem instructions, `make_AGENTS` generates `AGENTS.md` files. |
| `compact_boilerplate` | Template strings (in the `*.json` of a meta-skill) that get substituted into generated outputs. The discipline propagates through these. |
| `non_interactive_mode` (NI mode) | An agent runs without a synchronous user (cron, webhook, scheduled batch). Opt-in graduation path — agents are validated interactively first. Requires an `alert_channel` (BD-QC-007). |
| `subtree` | Refers to `temp/` — a `git subtree` of `andrej-karpathy-skills` for reference. Updates can be pulled in or pushed back per `git subtree pull` / `git subtree push`. |
| `NGAI` | "Non-General AI" — the project's framing for what this repo produces: purpose-built specialist agents (and Gems) rather than general-purpose chatbots. Each agent built from `make_agent.md` is an NGAI specialist with a specific mission, contract, and behavioral discipline. The term appears in README and historical context (e.g., `README_Disclosure.md`); use it when discussing the project's design philosophy with stakeholders. |

---

_AGENTS.md generated 2026-04-29 using `make_AGENTS.md` v1.0. Maintenance: update Active Context after major shipped work; refresh other sections only when the underlying truth changes._
