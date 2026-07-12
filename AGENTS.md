---
name: Make-AI-Agents
description: Build workspace for AI agent + Gemini Gem specs and the meta-templates that generate them. Source of truth for the behavioral discipline every consumer repo inherits.
version: "1.0"
author: chaz-clark
license: MIT
metadata:
  make-ai-agents:
    generated_by: make_AGENTS (self-application 2026-06-17)
    spec_json: make_AGENTS.json
---

# Make-AI-Agents

A build workspace for AI agents and Gemini Gems, plus the meta-templates that generate them. Agents and Gems are drafted here, then moved to their own dedicated repos when ready.

## Project Purpose

**This is**:
- A drafting space for AI agent specs (`make_agent` template family)
- A drafting space for Gemini Gem instructions (`make_gem` template family)
- The home of `knowledge/behavioral-discipline.md/.json` — the Toyota Way + Karpathy discipline that every agent built here inherits
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
├── README.md / README-QC.md / README-Disclosure.md
├── make-agent.md / .json                  # agent spec template (the meta-skill)
├── make-agent-qc.md / .json               # agent spec QC template (20 rules, 17 dimensions)
├── make_AGENTS.md / .json                 # AGENTS.md generation template (sibling)
├── make-orchestrator-agent.md / .json     # multi-agent orchestrator template (sibling, 2026-05-13)
├── make-agent-knowledge.md / .json        # runtime knowledge file template (sibling, 2026-05-13)
├── make-gems/                             # Gemini Gem templates and example Gems
│   ├── make-gem.md / .json
│   ├── make-gem-qc.md / .json
│   ├── README-GEM.md
│   ├── course_info_bot.json               # example Gem (Engineering Statistics course bot)
│   ├── implement-gem.md / .json           # implementation guide for compiled Gems
│   └── gem-instructions/                  # compiled .txt outputs (gitignored)
├── knowledge/                             # source-of-truth + generated knowledge files
│   ├── behavioral-discipline.md / .json   # 10 principles, 5 interaction patterns (v1.4)
│   └── learned/                           # session-end lesson distillation (Sprint B Learning loop landing zone)
├── update-agents/                         # doc refresh + analysis agents + utilities
│   ├── update-agent.md / .json            # entry-point / orchestration
│   ├── doc-refresh-agent.md / .json       # spec for the refresh workflow (uses fetch_doc.py)
│   ├── doc-analysis-agent.md / .json      # spec for the analysis workflow
│   └── fetch_doc.py                       # raw-HTTP doc fetcher (5 modes, 2026-05-13)
├── source-docs/                           # 34 cached platform docs (Anthropic / Google ADK / OpenAI / xAI)
│   └── dropbox/                           # staging folder for manual fetches (gitignored)
├── handoffs/                              # cross-repo handoff documents + parkinglot.md (gitignored)
└── temp/                                  # clone+gitignored: andrej-karpathy-skills (reference; refresh via `cd temp && git pull`; migrated from subtree 2026-05-13)
```

## Working Style

This project follows the behavioral discipline defined in `knowledge/behavioral-discipline.md` and `knowledge/behavioral_discipline.json`. **Read that file before doing non-trivial work in this repo.**

The four no-override principles — **P-001 Read Before Claiming, P-003 Stop on Defect, P-007 Pull Don't Push, P-010 Respect Intent** — apply unconditionally. The other six (P-002, P-004, P-005, P-006, P-008, P-009) have documented override conditions; see the discipline file.

**Where to start reading** (suggested first-pass order for new contributors):
1. This file — project context (you're here)
2. `knowledge/behavioral-discipline.md` — the discipline that governs every change
3. `make-agent.md` — the meta-skill template (read for understanding, not for memorization)
4. An existing artifact in `update-agents/` for an example of a fully-formed agent spec

**Project-specific rules** (carried from the previous CLAUDE.md):

- **No `__init__.py` or init files anywhere** — agents are standalone, not importable modules.
- **No root-level `requirements.txt`** — each agent carries its own dependencies when moved.
- **No packaging or CI/CD config** — this is a drafting space, not a pipeline.
- **When an agent is complete, it moves to its own repo.** The folder here can stay as a reference or be deleted.
- **Gems compile** to a `.txt` file in `make-gems/gem-instructions/` and a `.json` alongside `make-gem.md`.
- **Templates use markdown + YAML frontmatter** — `make_*.md` files contain YAML frontmatter for metadata (following Anthropic Agent Skills pattern). Separate `.json` files were deprecated 2026-07-07 after audit showed 3/5 were 8 weeks stale and zero tooling referenced them. Exception: `knowledge/behavioral-discipline.md/.json` remain paired (the JSON holds structured QC rules referenced by ID from other QC agents).
- **Updates to `make-agent.md` cascade** — every agent spec generated from it after the change should be regenerated or audited against the new template via `make_agent_qc`.
- **Make-AI-Agents is the leverage point; consumer repos are the field for Genchi Genbutsu (P-001).** This repo holds the meta-skills (`make_agent`, `make_orchestrator_agent`, `make_agent_knowledge`, etc.) and the discipline. Consumer repos (canvas-toolbox, AgentJ, course repos) USE the skills to generate real artifacts. When an agent in this repo is invoked to "test the skill on" a consumer repo, the goal is **skill improvement here**, NOT to finish the consumer repo's work. Capture what surfaces, fix the skill, commit the skill fix here, hand the field state back to the consumer repo's own agents/maintainers to commit there. Don't cross the boundary: this repo's commits update meta-skills; consumer-repo commits update generated artifacts.
- **Cascade material changes to consumer repos via handoffs.** When a commit here would materially affect agents working in consumer repos — a new make_AGENTS standard, a behavioral_discipline rule, a new QC check, a new optional section, a sharpened condition — **assess blast radius** before considering the change done. If consumer agents would behave differently with the new version (i.e., generate different AGENTS.md, fail QC under the new rule, gain access to a new pattern), draft a per-consumer handoff doc + proposal file (per the 2026-05-13 sprint pattern documented in this Active Context) and drop into each affected `handoffs/` folder. If the change is cosmetic / internal / non-propagating, skip — and note that skip reasoning in the commit message so future readers know the assessment happened. The cross-repo audit workstreams queued in Active Context are the SYSTEMATIC version of this rule (running it across every consumer at once); day-to-day skill commits should still trigger the lightweight version (assess → drop per affected repo OR explicitly skip with reasoning). The agents in this repo are the **main drivers** of consumer-repo behavior; the propagation discipline is what keeps that driver-relationship trustworthy. Added 2026-05-13.

## Handoff document recognition

This repo participates in the cross-repo `handoff` convention (canonical spec: `handoff/CONVENTION.md`, co-located gitignored clone). When operating in this repo, treat the following file patterns as **handoff documents** — structured artifacts with a lifecycle, NOT prose conversation:

| Path pattern | What it is |
|---|---|
| `handoffs/HANDOFF_<topic>.md` | Outgoing `request`-direction handoff (canonical copy) |
| `handoffs/<YYYY-MM-DD>_<topic>.md` | Incoming `deliver`-direction handoff (canonical consumer record) |
| `<CONSUMER>_HANDOFF_<topic>.md` at repo root | Incoming `request` dropped by another consumer for us to apply |
| `<PRODUCER>_DELIVERS_<topic>.md` at repo root | Visibility copy of an incoming `deliver` (canonical is in `handoffs/`) |
| `handoffs/parkinglot.md` | `internal` handoff — near-term parked ideas; deferred by design |
| `handoffs/long-term-parking.md` | `internal` handoff — far/someday parked ideas; deferred by design |

**Seven rules for handling a handoff document** (canonical at `handoff/AGENTS_snippet.md`):

1. **Read the metadata header first.** Required fields: `Date`, `Author`, `Direction`, `Status`, `Origin`, `Origin-Commit`, `Topic`. Optional: `Sensitivity`, `Companions`. Missing required → STOP and ask.
2. **Act only on `Status: delivered`.** Skip `draft`, `applying`, `applied`, `archived`, `superseded`. Escalate restricted/internal-only handoffs.
3. **Surface before applying.** Summarize the request/delivery — what's asked, what files/repos, what would change. Get per-decision approval.
4. **Update `Status` on apply.** After committing the change, set `Status: applied` and add a `## Lifecycle marker` with apply date (and optionally commit hash).
5. **STOP on missing referenced artifacts.** Files / commits / paths the handoff names that don't exist locally → halt and ask. The `Origin-Commit` field is your traceability anchor.
6. **Before authoring an outbound handoff**, read the target producer's `REPO_CARD.md` if present: confirm `Status: accepting`, intended type is accepted, drop at the named `Drop-location`.
7. **Do not auto-act on `parked` items.** `parkinglot.md` and `long-term-parking.md` (`Direction: internal`) are deferred *by design*. Act only on operator direction or when the item's `Trigger:` condition is met.

Refresh this section when `handoff/CONVENTION.md` versions up — canonical snippet is at `handoff/AGENTS_snippet.md` in the co-located clone.

## Toyota Quality Loop

Every task must complete the quality loop: **Prevent → Detect → Verify**.

### 1. Genchi Gembutsu (現地現物) - Go and See

**Don't assume, verify with real data:**
- Test with REAL user data, not synthetic fixtures
- When uncertain about format, examine actual files
- Verify in real environment, don't trust docs alone
- Read actual code before claiming understanding

**Behavioral trigger**: When you say "probably" or "should" → STOP and verify

### 2. Jidoka (自働化) - Built-in Quality / Stop on Defect

**Build quality in, stop when defect detected:**
- Write tests WITH code, not after
- Red tests block progress - fix immediately, don't defer
- Validation runs automatically (not manual step)
- Can't merge/export with errors (blocked by design)

**Behavioral trigger**: When you want to say "we'll fix this later" → STOP and fix now

**Aligns with**: P-003 Stop on Defect

### 3. Poka-yoke (ポカヨケ) - Mistake-Proofing

**Design so mistakes can't happen:**
- Automate validation (no manual steps)
- Use pre-commit hooks to catch errors
- Type hints catch errors at write-time
- Block operations that would create defects

**Behavioral trigger**: When manual verification required → Design it out

---

**The Quality Loop in action:**

When you find a defect:
1. **Fix it** (Jidoka - stop and correct)
2. **Verify the fix** (Genchi Gembutsu - test with real data)
3. **Prevent recurrence** (Poka-yoke - add automated check)

## Learning loop

At session end, distill non-obvious lessons from the session into a structured entry under `knowledge/learned/`:

- **File**: `knowledge/learned/YYYY-MM-DD-<short-slug>.md` (or update an existing rolling file like `knowledge/learned/preferences.md` for cumulative patterns).
- **Frontmatter**: `name`, `observed_in: <session-context>`, `confidence: low | med | high`.
- **Body**: the lesson, the trigger, the suggested rule.

What counts: surprises, non-obvious quirks, user-preference signals, system gotchas. What does NOT count: generic "task done" prose. **A lesson must be specific and reusable.**

Future invocations of agents in this repo read `knowledge/learned/` alongside the core knowledge files. This is the closed-loop distillation pattern — **P-009 (Hansei + Yokoten) formalized as a structural artifact**, in the Make-AI-Agents idiom (no DSPy/GEPA, no server — just structured markdown the agent reads next time). Inspired by Hermes Agent's auto-distillation; rebuilt as a single Markdown-directory convention.

## Active Context

_Last updated: 2026-07-08_

**Kebab-case migration completed** (2026-07-08): All markdown files and folders migrated from snake_case to kebab-case naming (e.g., `make_agent.md` → `make-agent.md`, `update_agents/` → `update-agents/`). Backward-compatible symlinks preserved for 6-12 month grace period. All cross-references updated. Migration execution plan: `KEBAB_CASE_MIGRATION.md`.

**Recent shipped (2026-05-28 → 2026-06-17):**

- **Hermes-research synthesis sprints (2026-05-28)** — three meta-template upgrades + corresponding QC checks, motivated by the Nous Research Hermes Agent comparison work:
  - **Sprint F** — `## Handoff document recognition` baked into `make_AGENTS` + AGENTS-QC-008 (handoff recognition fingerprint). Commits `7a0853a` → `81ebc9a`.
  - **Sprint B** — `## Learning loop` as a required AGENTS section + BD-QC-008 (Learning loop structural artifact). `knowledge/learned/` is the closed-loop distillation lane — P-009 (Hansei + Yokoten) formalized as a structural slot.
  - **Sprint A** — agentskills.io frontmatter on every `make_*` skill MD + AGENTS-QC-009 (frontmatter present). Pure portability win across the `make_*` family.
  - Blanket per-repo `deliver` handoff dropped into all 14 chaz-clark consumer repos describing how each applies Sprints A/B/F to its own AGENTS.md.

- **`make_agent_knowledge` v1.0 → v1.1 (2026-06-17, commit `8222d2c`)** — closed `#14` (section order: now `title → scope → provenance → last_updated → body`, matching what the `compact_boilerplate` templates already emitted) and `#15` (optional-sections list documented as NON-EXHAUSTIVE with `_mapping_guidance` for cross-file relationship narrative / orienting frame / references / quick reference / audit tags).

- **README outcome-oriented rewrite (2026-06-17, commit `d3ab08f`)** — benchmarked against `canvas-toolbox/README.md`. 9 surgical edits moving from artifact-noun framing (*"agent specs"*) to outcome-verb framing (*"turn the AI tool you already use into a specialist for your repo"*). New H1, "What you can do with it" bullet list, 3-step IDE / AI / templates onboarding flow with A/B/C setup paths, Hermes/OpenClaw comparison moved out of the onboarding zone.

- **trunk-always-works (`#16` closed, 2026-06-17, commit `33b6322`)** — Genchi Genbutsu confirmed all four named "master" repos have active remotes (`itm327-master` had accumulated 23 unpushed commits over weeks). Replaced the blanket "do NOT push" directive with the per-repo push-policy table preserved below. P-008 `standard_work_extensions[trunk-always-works]` added to `behavioral_discipline.{md,json}`. BD bumped to v1.4.

- **Own AGENTS.md compliance (2026-06-17 evening, commit `29b5952`)** — applied Sprints A/B/F to this file itself, closing the producer-consumer loop. Frontmatter prepended, Handoff Recognition + Learning loop sections inserted, `knowledge/learned/` created. The producer-applies-to-self gap was caught tonight by Chaz observing this file lagged the standard it propagates.

**In flight:** nothing actively in progress. Parked items live in `handoffs/parkinglot.md` (gitignored) with named triggers for revisit.

**Open issues** (chaz-clark/Make-AI-Agents, as of 2026-06-18):

- `#12` Document the agent-as-drafting-partner pattern around `make_agent_knowledge` — **parked.** Trigger: a second use case beyond canvas-toolbox surfaces the pattern, OR Chaz wants to ship the consumer-trigger contract across the `make_*` family.
- `#13` `make_AGENTS`: add generic workflow practices to generated Working Style section — **parked** as "Sprint G" candidate. Trigger: next sprint slot.
- Closed tonight: `#14`, `#15`, `#16`.

**Next likely** (when capacity opens):

- **Sprint G — `#13`'s 5 generic Working Style practices** for the `make_AGENTS` template: docs-sync on every change, verify VCS/build state before claiming, single-repo issue scope (conditional), vendored-upstream change protocol (conditional), project-local dep isolation. Conditionally framed so generated AGENTS.md files adapt rather than copy verbatim (same lesson as `#10` about stale subtree language).
- **`make_AGENTS` push-policy bake-in — Yokoten of `#16`** — bake the per-repo push-policy table shape into `make_AGENTS` `compact_boilerplate` so future generated AGENTS.md files include the section by default; pairs with a proposed **AGENTS-QC-010** validating it's declared. Surfaces the new rule via the structure consumers actually read.
- **`#12` drafting-partner pattern** — three coupled pieces (guided fill-in doctrine, consumer-integration trigger contract, upstream-contribution loop). Three open design questions need resolution before it can ship.
- Genchi Genbutsu the new skills further as they're used in canvas-toolbox / AgentJ — any GG findings fold back here.
- Wave 4 doc-analysis cycle when `source_docs/` next refreshes.
- Operationalize `doc_refresh_agent` as a runner (Python) on top of `fetch_doc.py`, enabling scheduled refreshes.
- Refresh `temp/` clone (`cd temp && git pull`) when the upstream `chaz-clark/andrej-karpathy-skills` ships new guidelines.

---

**Completed workstream — cross-repo AGENTS.md audit + regenerate-and-deliver (2026-05-13 → 2026-06-17):**

Original framing: every consumer repo (public + local masters) likely had an AGENTS.md predating current standards (especially AGENTS-QC-006 — discipline files co-located, not just pointed at), OR was still on CLAUDE.md. Executed end-to-end via the **14-repo blanket handoff drop on 2026-06-17** rather than the originally-planned per-target package pass — same outcome, fewer per-target customizations; each consumer applies Sprints A/B/F themselves following the handoff's action list.

**6-step workstream applied per target** (status as of 2026-06-17):

1. ✅ **Enumerate Chaz's repos (public + local masters)** — done 2026-05-13. **GG learning from sprint 2 (added 2026-05-13)**: step 1 must check BOTH the local working tree AND GitHub-side state. The initial enumeration used `gh api repos/<owner>/<repo>/contents/AGENTS.md` which only sees PUSHED state. 2 of 4 sprint-2 targets (`agentj`, `gh-issues-agent`) had local-but-not-pushed `AGENTS.md` files that triggered P-003 halts mid-sprint. Future cross-repo audits should run `ls <local-path>/AGENTS.md` in addition to `gh api`, then reconcile.
2. ✅ **Audit each current-sprint target** — done 2026-06-17 (the 14-repo gap-matrix against AGENTS-QC-001..009 + full required-sections contract).
3. **Generate `AGENTS_updated.md` per behind-the-curve target** — superseded by consumer-side application. Each consumer applies Sprints A/B/F themselves following the handoff's action list (no AGENTS_updated.md artifact produced upstream).
4. **Package `behavioral_discipline.{md,json}` into each target's `knowledge/` folder** — also superseded; consumers fetch from this repo when applying their handoff (per AGENTS-QC-006 condition (a)).
5. ✅ **Deliver via handoff convention** — done 2026-06-17 (14 `deliver` handoffs dropped, all `Status: delivered` at producer end).
6. **Track per-repo state via handoff `Status` enum** — in progress. Make-AI-Agents itself applied its own handoff 2026-06-17 (commit `29b5952`); other consumers apply on their own time.

**Per-repo push policy (canonical, verified 2026-06-17 via Genchi Genbutsu — replaces the prior "Local-only targets … do NOT push" directive; see closed `#16`):**

| Repo | Remote | Active push? | Push after every commit? |
|---|---|---|---|
| `ds250-class-code` | `chaz-clark/ds250-class-code` | yes (last push 6 mo ago — slow but real) | **yes** |
| `ds460-master` | `chaz-clark/ds460-master` | yes (active; concurrent diverge → reconcile first) | **yes** |
| `itm327-master` | `chaz-clark/itm327-master-course` *(remote name differs)* | yes (very active) | **yes** |
| `m119-master` | `chaz-clark/m119-master` | yes (active) | **yes** |
| *(any future repo with no remote)* | — | n/a | **n/a — but say WHY here** |

All four "master" repos have active remotes. The old "apply locally and do NOT push" guidance produced unpushed-commit debt (e.g., `itm327-master` accumulated 23 commits ahead of `origin/main` over weeks before being surfaced 2026-06-17). The trunk-always-works discipline now governs: **when a repo has a remote, every commit is pushed in the same operation as the commit itself** (see `knowledge/behavioral-discipline.md` → P-008 Standard Work). If a repo IS genuinely local-only, that's a deliberate choice — record it in this table with WHY.

## Existing Tooling

Before generating new tools or scripts in this repo, reuse what already exists.

| Tool / File | Purpose | When to use |
|---|---|---|
| `make-agent.md` / `.json` | Generate agent specs (the meta-skill) | Building any new single agent |
| `make-agent-qc.md` / `.json` | Validate agent specs (20 rules, 17 dimensions; covers BD-QC, ORCH-QC, KNW-QC families) | After generating any new agent |
| `make_AGENTS.md` / `.json` | Generate `AGENTS.md` for a project | Setting up a new project, migrating from `CLAUDE.md` |
| `make-orchestrator-agent.md` / `.json` | Generate multi-agent orchestrator specs (`agent_type.type: 'multi_agent'`) that delegate to specialist subagents | When a single agent has > 20 tools or spans multiple domains — split into specialists + orchestrator |
| `make-agent-knowledge.md` / `.json` | Generate runtime knowledge files (MD+JSON pair in `knowledge/`) in three shapes (reference / identity / procedural) | When an agent needs lookup-shaped, principle-shaped, or playbook-shaped knowledge at runtime |
| `make_gems/make_gem.md` / `.json` | Generate Gemini Gem instructions | Building any new Gem |
| `make_gems/make_gem_qc.md` / `.json` | Validate Gem instructions | After generating any new Gem |
| `knowledge/behavioral-discipline.md` / `.json` | Source of truth for the discipline embedded in every generated artifact | Read once for context; reference by path in generated specs |
| `update_agents/doc_refresh_agent.*` | Spec for the refresh workflow (staleness → fetch → validate → write → report) | Monthly or after major platform releases. Step 2 (Fetch) uses `fetch_doc.py` |
| `update_agents/doc_analysis_agent.*` | Diff cached docs against templates and propose updates | After running a refresh — finds convergence-bonus candidates across platforms |
| `update_agents/fetch_doc.py` | Raw-HTTP doc fetcher; 5 modes: default fetch, `--list-links` (discover child URLs), `--batch`, `--from-html` (convert browser-saved HTML), `--check` (drift detection vs an existing source_docs file) | Whenever a `source_docs/` file is stale or new. Run via `uv run update_agents/fetch_doc.py <url>` — PEP 723 inline metadata handles deps |

**Reuse-first rule**: if a template, validation, or knowledge file already covers a needed operation, use it rather than generating new code or new templates.

**How to invoke a meta-skill**: every `make_*.md` file is an LLM prompt-as-skill, not a script. To run one:

1. Open the meta-skill's `.md` and `.json` in your agentic dev tool (Claude Code, Cursor, Aider, Antigravity).
2. State the task, e.g. *"Use `make_agent` to draft a spec for an X agent."* The tool reads the meta-skill files as instructions and applies them to your request.
3. Follow the meta-skill's Quickstart steps with the LLM. For agent specs, that includes choosing an `interaction_pattern` and embedding the behavioral discipline (step 0 of `make-agent.md` Quickstart).
4. Validate the generated artifact with the matching `*_qc` meta-skill. Output goes wherever the LLM writes it; review reports manually or save to `qc_reports/` (gitignored).

There is no CLI or build step. The repo is a knowledge base + prompt library, not a pipeline.

**Worked example** — running `make_agent_qc` against an existing spec:

> *"Use `make-agent-qc.md` (with YAML frontmatter) to validate `update_agents/doc_refresh_agent.md` (with YAML frontmatter). Score against all 18 rules and 15 quality dimensions. Report critical issues first."*

The LLM reads the QC meta-skill, reads the target spec, runs the rule set, and returns a structured report. Save the report to `qc_reports/` if you want to keep it.

## Domain Terms

| Term | Definition |
|---|---|
| `interaction_pattern` | The behavioral profile of an agent — drives which discipline principles apply. One of: `read_only`, `single_write_workflow`, `multi_step_batch`, `single_call_api`, `conversational`. Distinct from `agent_type.type` (which is the implementation pattern). See `knowledge/behavioral_discipline.json` → `agent_type_applicability.types`. |
| `agent_type.type` | The **implementation** pattern of an agent (`class_based`, `llm_agent`, `api_agent`, `data_processor`, `multi_agent`, `workflow`, `rule_based`, `other`). Orthogonal to `interaction_pattern`. |
| `P-001` … `P-010` | Stable IDs for the ten behavioral discipline principles. P-001 = Read Before Claiming, P-003 = Stop on Defect, P-007 = Pull Don't Push, P-010 = Respect Intent — these four are no-override. See `knowledge/behavioral-discipline.md` → "The Ten Principles". |
| `BD-QC-001` … `BD-QC-007` | Stable IDs for behavioral discipline QC checks. Defined in `knowledge/behavioral_discipline.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_ids 17 and 18. |
| `ORCH-QC-001` … `ORCH-QC-005` | Stable IDs for orchestrator-spec QC checks. Defined in `make_orchestrator_agent.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_id 19. Applies only when `agent_type.type: 'multi_agent'`. |
| `KNW-QC-001` … `KNW-QC-006` | Stable IDs for knowledge-file QC checks. Defined in `make_agent_knowledge.json` → `qc_checks`; referenced by `make_agent_qc.json` rule_id 20. Applies only when an agent has non-empty `cross_references.knowledge_files[]`. |
| `make_*` | Naming convention for **meta-skills** (templates that generate other things). `make_agent` generates single agents, `make_orchestrator_agent` generates multi-agent orchestrators, `make_agent_knowledge` generates runtime knowledge files, `make_gem` generates Gem instructions, `make_AGENTS` generates `AGENTS.md` files. |
| `compact_boilerplate` | Template strings (in the `*.json` of a meta-skill) that get substituted into generated outputs. The discipline propagates through these. |
| `non_interactive_mode` (NI mode) | An agent runs without a synchronous user (cron, webhook, scheduled batch). Opt-in graduation path — agents are validated interactively first. Requires an `alert_channel` (BD-QC-007). |
| clone+gitignore | The canonical vendored-upstream consumption pattern in this repo (per the 2026-05-13 cross-project rule). Vendored repos are cloned at the host root and listed in `.gitignore`, so the host's tracked tree stays clean and refreshes are just `cd <clone> && git pull`. Currently in use: `temp/` (andrej-karpathy-skills), `gh-issues-agent/`. NOT used: `git subtree` — migrated away 2026-05-13 because subtree mechanics noise up the host's `git pull` and `git log`. |
| `NGAI` | "Non-General AI" — the project's framing for what this repo produces: purpose-built specialist agents (and Gems) rather than general-purpose chatbots. Each agent built from `make-agent.md` is an NGAI specialist with a specific mission, contract, and behavioral discipline. The term appears in README and historical context (e.g., `README_Disclosure.md`); use it when discussing the project's design philosophy with stakeholders. |

---

_AGENTS.md last revised 2026-06-18. Generated 2026-04-29 using `make_AGENTS.md` v1.0; revised in-place for the wave-2 additions (make_orchestrator_agent, make_agent_knowledge, fetch_doc.py, source_docs 9 → 34); brought to Hermes-sprint compliance 2026-06-17 (Sprints A/B/F applied via commit `29b5952`, eat-the-cooking moment); Active Context fully refreshed 2026-06-18 to reflect 2026-05-28 sprint synthesis + 2026-06-17 v1.1 fixes / README rewrite / trunk-always-works / own-compliance work. Maintenance: update Active Context after major shipped work; refresh other sections only when the underlying truth changes._
