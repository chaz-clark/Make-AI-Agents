---
name: make_AGENTS
description: Generates tool-agnostic AGENTS.md project context files with discipline + handoff recognition + Learning loop baked in. Sibling to make_agent and make_gem.
version: "1.0"
author: chaz-clark
license: MIT
metadata:
  make-ai-agents:
    spec_json: make_AGENTS.json
    skill_type: meta
    propagates: [behavioral_discipline, handoff_recognition, learning_loop]
---

# make_AGENTS — AGENTS.md Generation Skill

## Agent Instructions
1. Read this for mission, structure, principles, and what an AGENTS.md must contain.
2. Parse `make_AGENTS.json` for structured data — required/optional section lists, the AGENTS.md template, behavioral discipline embed, and validation. Do not parse this Markdown for structured rules.
3. Keep generated AGENTS.md files lean. Required sections only by default; add optional sections only when warranted.
4. **Behavioral Discipline is required.** Consult `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The make_AGENTS skill itself operates as `interaction_pattern: single_write_workflow` and embeds discipline language in every AGENTS.md it generates (in the "Working Style" section).

---

## Mission (core)

**What it does**: Generates a tool-agnostic `AGENTS.md` project context file that drives the LLM working in a project. Sibling to `make_agent.md` (which generates agent specs) and `make_gem.md` (which generates Gem instructions); make_AGENTS produces project-level context, not agent-level specs.

**Why it exists**: Every project needs project-level context for the LLM working in it. `CLAUDE.md` is a Claude-only naming; `AGENTS.md` is the tool-agnostic standard readable by Claude Code, Cursor, Aider, Antigravity, and other agentic tools. This skill produces consistent AGENTS.md files across projects, with the behavioral discipline baked in so any LLM working in any project built with these templates inherits the same behavioral standards.

**Who uses it**: Developers setting up a new project, or migrating an existing project from `CLAUDE.md` to `AGENTS.md`.

**Example**: "Generated `AGENTS.md` for the `Make-AI-Agents` repo by reading the existing `CLAUDE.md`, current state of `knowledge/` and `make_agent v3.0`, and writing a tool-agnostic project context file that points to the behavioral discipline."

---

## Agent Quickstart (core)

0. **[Choose interaction_pattern, then embed discipline]**: For most projects, the make_AGENTS skill itself is `single_write_workflow` (one AGENTS.md generated per invocation). Embed behavioral discipline in this skill's MD (after `## Key Principles`), JSON, and any system prompt. **Required.**

1. **[Identify project context]**: Read the existing `CLAUDE.md` if present. Inspect repo root, key files (READMEs, package.json/pyproject.toml/setup.py, top-level folders). Identify whether the project is mid-migration, has special tooling, has domain-heavy vocabulary. **README sanity check (added 2026-05-13)**: before pulling content from `README.md` into the generated AGENTS.md (especially Project Purpose), verify the README is actually project-specific — a common pattern is for a consumer to copy a scaffold README from an upstream toolkit (e.g., the canvas-toolbox README appears verbatim in multiple downstream master repos). If the README reads as generic toolkit prose with no project-specific identifying content (course name, repo-unique mission, project-unique terminology), treat it as a scaffold and do NOT pull content from it. Fall back to CLAUDE.md, repo folder structure, and recent commit messages for project context.

2. **[Parse template]**: Load `make_AGENTS.json` → `agents_md_template` for the section skeleton, `agents_md_required_sections` and `agents_md_optional_sections` for the contract, `compact_boilerplate` for the discipline embed.

3. **[Generate]**: Write `AGENTS.md` at project root. Include all required core sections; add optional sections only if their criteria apply. Embed the behavioral discipline pointer in the "Working Style" section.

4. **[Package the discipline files alongside]** (REQUIRED — added 2026-05-13): Copy `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json` from this repo (Make-AI-Agents) into the **target project's** `knowledge/` folder. **Without this step, the pointer in Working Style is a broken reference in any project that doesn't already have a Make-AI-Agents clone.** The discipline must travel WITH the AGENTS.md — co-located files, not a remote pointer. **Detection logic before copying**:
   - If the target already has `knowledge/behavioral_discipline.{md,json}` at the canonical path — skip the copy. Optionally check the snapshot header / commit-sha and warn if stale.
   - If the target has the discipline at a cloned-subdirectory path (e.g. `<consumer>/make_ai_agents/knowledge/behavioral_discipline.md` per the clone+gitignore pattern) — update the AGENTS.md Working Style pointer to that path; skip the copy. The clone-and-pull pattern provides freshness; the local copy is redundant. **NOTE — only a full `Make-AI-Agents` clone (or another repo explicitly carrying `knowledge/behavioral_discipline.md` at a known relative path) satisfies condition (b). Single-skill clones like `gh_issues_agent/`, `canvas-toolbox/`, etc. do NOT carry the discipline by default — verify the file actually exists at the cloned-subdirectory path before relying on it. If the only clone present is single-skill and doesn't carry the discipline, fall back to "Otherwise — copy both files" below.**
   - Otherwise — copy both files. Add a 4-field snapshot header to each. **The header form differs by file type** (added 2026-05-13 after the sprint-3 migrations surfaced that HTML comments break strict JSON parsing): for the `.md`, prepend 4 HTML-comment lines: `<!-- SNAPSHOT_FROM: chaz-clark/Make-AI-Agents -->`, `<!-- SNAPSHOT_COMMIT: <sha> -->`, `<!-- SNAPSHOT_DATE: <YYYY-MM-DD> -->`, `<!-- REFRESH: copy the upstream file again to pick up changes -->`. For the `.json`, add 4 underscore-prefixed top-level keys to the existing JSON object: `"_snapshot_from": "chaz-clark/Make-AI-Agents"`, `"_snapshot_commit": "<sha>"`, `"_snapshot_date": "<YYYY-MM-DD>"`, `"_snapshot_refresh": "copy the upstream file again to pick up changes"`. Both forms carry the same information; the JSON form is strict-JSON-valid (no comments needed). Future refreshes detect drift via the `_snapshot_commit` value on the JSON OR the `SNAPSHOT_COMMIT:` line on the MD.

4.5. **[Bake handoff convention recognition + conditionally co-locate `handoff/`]** (REQUIRED — added 2026-05-28, Sprint F):

   **(a) Always bake the snippet into Working Style.** Read `handoff/AGENTS_snippet.md` from this Make-AI-Agents repo (which has the handoff convention repo cloned at `handoff/`). Copy its content from `## Handoff document recognition` through end-of-file **verbatim** into the generated AGENTS.md's Working Style section, immediately after the behavioral discipline pointer subsection. The snippet is **self-contained** — its 7 rules, path-pattern table, and status/direction enums don't depend on `handoff/` being present at runtime, so the AGENTS.md resolves standalone. Prepend a 2-line refresh trace as HTML comments above the section: `<!-- handoff/AGENTS_snippet.md @ <sha> -->` and `<!-- refresh: cd handoff && git pull -->` so a future reader knows when it was baked and how to refresh.

   **(b) Conditionally co-locate the `handoff/` clone.** Detect whether the target repo participates in the cross-repo handoff convention via two signals:
   - **Auto-detect** — does the target repo have a `handoffs/` folder (existing, or pre-created by an earlier step)?
   - **Explicit ask** — prompt the user: *"Will this agent communicate with other agents via the handoff convention?"*

   If **either** signal is yes → `git clone https://github.com/chaz-clark/handoff.git handoff` at the target repo root + add `handoff/` to the target's `.gitignore` (same shape as the discipline / `temp/` / `gh_issues_agent/` clone+gitignore pattern). If **both** are no → skip the clone; the snippet still ships standalone.

   **(c) Surface what was done** in the generation summary: which sha was baked from `handoff/AGENTS_snippet.md`; whether `handoff/` was co-located and the reason (participation signal yes/no).

4.6. **[Bake Learning loop section + create `knowledge/learned/`]** (REQUIRED — added 2026-05-28, Sprint B):

   **(a) Bake the Learning loop section** into the generated AGENTS.md between the handoff recognition section and Active Context. Paste the canonical text from `make_AGENTS.json` → `compact_boilerplate.learning_loop_template` verbatim. This is the structural form of **P-009 (Hansei + Yokoten)** — agents end sessions by writing distilled lessons to `knowledge/learned/<file>.md` for future invocations to read. Inspired by Hermes Agent's auto-distillation; rebuilt as a Markdown-directory convention (no DSPy/GEPA, no server).

   **(b) Create the directory**: `mkdir -p <target>/knowledge/learned/` and add a `.gitkeep` file so the convention exists in version control even before the agent has written its first lesson.

   **(c) Verified by BD-QC-008** (in `knowledge/behavioral_discipline.json`): agent MD has the `## Learning loop` heading; `knowledge/learned/` exists. Without this slot, P-009 stays prose discipline rather than a self-improving artifact — every invocation re-discovers lessons previous sessions already surfaced.

4.7. **[Prepend agentskills.io frontmatter]** (REQUIRED — added 2026-05-28, Sprint A):

   Prepend YAML frontmatter to the very top of the generated AGENTS.md per `make_AGENTS.json` → `compact_boilerplate.frontmatter_template`. **Required fields**: `name`, `description`, `version`. **Recommended**: `author`, `license`. **Provenance**: `metadata.make-ai-agents.generated_by: make_AGENTS` and `metadata.make-ai-agents.generated_on: <iso-date>`.

   This is the Make-AI-Agents idiom adoption of the **[agentskills.io open standard](https://agentskills.io)** — the same standard Hermes Agent and OpenClaw consume. Generated AGENTS.md files become **drop-in skills** in any agentskills.io-compliant runtime, layered atop the rich `.json` sidecar where one exists. Verified by **AGENTS-QC-009** (delegates to BD-QC-009).

5. **[Validate]**: Run `make_agent_qc` against the generated AGENTS.md if it makes sense — AGENTS.md is structurally similar to an agent spec but not identical. See `## Validation and Testing (core)` for what applies. AGENTS-QC-006 verifies the discipline files are co-located (or the pointer resolves to a cloned-subdirectory path). **On refresh** (existing AGENTS.md as input): AGENTS-QC-007 scans Active Context / Structure / Project-specific rules for stale vendoring-pattern tokens (`git subtree`, `subtree pull/push/add`, `.gitmodules`, `git submodule`) — if any describe the CURRENT posture, propose a rewrite to the canonical clone+gitignore form (see Common Pitfall #1) rather than preserving them under P-007. **AGENTS-QC-008** (added 2026-05-28, Sprint F) verifies the handoff recognition section is structurally complete (heading present, path-pattern table present, all 7 rules present, status enum + direction enum quick-lookups present) AND — conditionally — that if the target repo has a `handoffs/` folder, the `handoff/` clone is co-located and gitignored. **BD-QC-008** (added 2026-05-28, Sprint B, in `knowledge/behavioral_discipline.json`) verifies the `## Learning loop` section is present + `knowledge/learned/` directory exists in the target repo. **AGENTS-QC-009** (added 2026-05-28, Sprint A) verifies the agentskills.io frontmatter is present and has required fields; delegates to **BD-QC-009** in the discipline JSON.

6. **[Output]**: Confirm AGENTS.md location with the user. If migrating from `CLAUDE.md`, propose deletion as a separate step (per P-002 — don't bundle the deletion with the creation).

For detailed structure, see `make_AGENTS.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- Mission and purpose
- Design philosophy and principles
- What an AGENTS.md must contain (narrative)
- Common pitfalls
- Behavioral discipline integration narrative

### The JSON File (.json) Contains:
- `agents_md_required_sections` — structured list of required sections
- `agents_md_optional_sections` — structured list of optional sections with inclusion criteria
- `agents_md_template` — the section-by-section skeleton with placeholders
- `compact_boilerplate` — the behavioral discipline embed string for the "Working Style" section
- `validation.test_cases`
- `behavioral_discipline` object for this skill itself

**Rule of Thumb**: If the make_AGENTS skill needs to parse it programmatically → JSON. If a developer needs to understand the "why" → MD.

---

## Key Principles (core)

### 1. Tool-Agnostic
**Description**: AGENTS.md must be readable by Claude Code, Cursor, Aider, Antigravity, and any other agentic tool that supports the convention. No tool-specific instructions ("only Claude Code does X") in the file body.
**Why**: The whole point of `AGENTS.md` over `CLAUDE.md` is openness. Tool-specific instructions defeat the migration.
**How**: When in doubt, write instructions that any agentic tool could follow. Tool-specific guidance lives in tool-specific config (e.g., `.cursorrules`), not in `AGENTS.md`.

### 2. Concise — Project Context, Not Documentation
**Description**: AGENTS.md is the file the LLM reads first when working in a project. It is project context, not exhaustive documentation. Long AGENTS.md files dilute their own purpose.
**Why**: An LLM that has to read 2000 lines of project context before answering a simple question burns budget and surfaces noise. The first 100 lines do 80% of the work.
**How**: Required sections aim for ~30 lines each. Optional sections only when they earn their presence. Long-form documentation lives in READMEs, not AGENTS.md.

### 3. Active-State-Aware
**Description**: Every AGENTS.md has an "Active Context" section that surfaces in-flight work, recent major changes, and known follow-ups. This is the section that decays fastest and matters most.
**Why**: An LLM that knows the project's current state (e.g., "v3.0 just shipped, AGENTS.md migration in progress") makes better decisions than one that only sees historical structure.
**How**: Generate the Active Context with date stamps and short, current-state-only bullets. Encourage developers to update this section weekly or after major shipped work.

### 4. Migration-Friendly
**Description**: When generating an AGENTS.md for a project that has an existing `CLAUDE.md`, the skill must produce a file that supersedes `CLAUDE.md` cleanly — no content lost, no double-tracking.
**Why**: Half-finished migrations (both CLAUDE.md and AGENTS.md tracked) confuse every agentic tool that reads the project.
**How**: After generating AGENTS.md, propose `git rm CLAUDE.md` and `.gitignore` updates as a separate, follow-up step (per behavioral discipline P-002 — don't bundle).

### Recommended Principles for LLM Agents

This skill is itself an agent. The Recommended Principles for LLM Agents from `make_agent.md` apply: Explicit Tool Control, Guardrails as a Separate Layer, Stop Sequence Control, Temperature by Agent Mode (low for this skill — deterministic generation), Structured Output vs Function Calling, Graceful Degradation for Optional Tools.

---

## Behavioral Discipline (core)

This skill operates as `interaction_pattern: single_write_workflow` and inherits the discipline from `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. Applicable principles: P-001, P-002, P-003, P-004, P-006, P-007, P-008, P-009, P-010 (skip P-005 — single step, no decomposition needed).

The skill MUST follow the integration flow defined in `make_agent.md` → `## Behavioral Discipline (core)`. The same flow applies recursively to make_AGENTS itself.

### What the GENERATED AGENTS.md inherits

Every AGENTS.md this skill generates contains a `## Working Style` section with the behavioral discipline pointer (from `make_AGENTS.json` → `compact_boilerplate.working_style_template`). This is how the discipline propagates from this skill into every project that uses an AGENTS.md generated by it.

### Two layers of discipline

- **This skill's discipline** — applies to `make_AGENTS` when it generates AGENTS.md files (P-002 plan, P-006 document, P-009 reflect, etc.)
- **Generated AGENTS.md discipline pointer** — applies to the LLM working in any project that has an AGENTS.md generated by this skill

Both layers reference the same `knowledge/behavioral_discipline.md` source of truth.

---

## What an AGENTS.md Must Contain (core)

The contract for every AGENTS.md this skill generates.

### Required sections (in this order)

1. **`# <Project Name>`** — title, ~1 line description below
2. **`## Project Purpose`** — what this repo IS and is NOT, ~3-5 bullets each. Includes the audience (who uses this).
3. **`## Structure`** — annotated folder layout. Reference, not exhaustive.
4. **`## Working Style`** — behavioral discipline pointer (the `compact_boilerplate.working_style_template` substituted in), project-specific rules, AND the canonical handoff recognition snippet (baked from `handoff/AGENTS_snippet.md`, per Sprint F / AGENTS-QC-008).
5. **`## Learning loop`** *(added 2026-05-28, Sprint B)* — closed-loop knowledge distillation pattern (P-009 as structural artifact). Baked from `compact_boilerplate.learning_loop_template`. Verified by BD-QC-008 in `knowledge/behavioral_discipline.json`. Target repo gets a `knowledge/learned/` directory (gitkept) for the agent to write distilled lessons.
6. **`## Active Context`** — current state, in-flight work, recent major changes, open issues. Date-stamped.

### Optional sections (when criteria apply)

- **`## Domain Terms`** — when the project has non-obvious vocabulary that LLMs would interpret wrong.
- **`## External System Lessons`** — when the project interacts with external systems (Canvas API, GitHub API, etc.) with non-obvious behaviors.
- **`## Migration Notes`** — when the project is mid-migration (e.g., CLAUDE.md → AGENTS.md, library A → library B). Removed when migration completes.
- **`## Existing Tooling`** — when the project has scripts/utilities that the LLM should reuse before generating new code.

For each optional section, the JSON has explicit inclusion criteria — see `agents_md_optional_sections[].include_when` in `make_AGENTS.json`.

---

## How to Use This Skill (core)

### Prerequisites
- Project root directory accessible
- Existing `CLAUDE.md` readable (if present — used as input for migration)
- `knowledge/behavioral_discipline.md/.json` readable (for the discipline pointer)
- `make_AGENTS.json` readable (for templates)

### Basic Usage
Conversational invocation through any agentic tool. Example prompt:
> "Use the `make_AGENTS` skill to generate an `AGENTS.md` for this repo. Read the existing `CLAUDE.md` for workspace rules, current state from the README and recent git log, and embed the behavioral discipline."

The skill responds with a proposed AGENTS.md draft, waits for confirmation per P-002, then writes the file at project root.

---

## Common Pitfalls and Solutions (core)

### 1. Duplicating discipline content INTO the AGENTS.md prose (vs. packaging the discipline FILES alongside)

**Problem**: There are THREE distinct mistakes that look similar:
- **(a) Inlining the discipline content**: Generated AGENTS.md restates the behavioral discipline in full prose — copies all 10 principles, examples, override rules — into the Working Style section itself. AGENTS.md balloons to 1000+ lines and stays in sync with `knowledge/behavioral_discipline.md` only by manual effort.
- **(b) Failing to package the files**: Generated AGENTS.md is lean (points at `knowledge/behavioral_discipline.md`) but the target repo doesn't actually have that file. The pointer is broken in every project that wasn't explicitly set up with the discipline.
- **(c) Preserving stale vendoring-pattern language under minimum-diff**: A refresh of an older AGENTS.md leaves a stale Active Context (or Structure) bullet that describes the Make-AI-Agents reference as a `git subtree` — language from the pre-2026-05-13 era. The actual local posture is `clone+gitignore` per the current rule, but the bullet wasn't rewritten because P-007 (minimum diff) preserved adjacent code. Result: the AGENTS.md reads as endorsing a vendoring pattern the project no longer uses, and a new agent in that repo will follow the stale instruction (e.g. try to `git subtree pull --prefix=...` on a path that's a regular clone, get a confusing error).

All three kill the propagation — (a) by duplication-drift, (b) by broken-reference, (c) by stale-instruction-drift.

**Why each happens**: (a) Skill writes "comprehensive" output instead of pointers. (b) Skill writes pointer-only output without ensuring the target file exists. (c) Refresh treats vendoring-pattern language as "adjacent code that was correct for its time" and preserves it verbatim — but the canonical posture changed (subtree → clone+gitignore as of 2026-05-13), so the language IS itself the defect, not adjacent code.

**Solution**:
- The AGENTS.md prose is a POINTER — Working Style references `knowledge/behavioral_discipline.md` by file path. The `compact_boilerplate.working_style_template` in `make_AGENTS.json` is a ~3-line summary naming the four no-override principles, not a copy of all 10.
- The FILES are PACKAGED alongside — per Quickstart step 4, `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json` are copied from Make-AI-Agents into the target's `knowledge/` folder (with a snapshot header). The pointer in Working Style then resolves to a local file that exists.
- **During refresh, SCAN for stale vendoring-pattern language and REWRITE** — explicit narrow exception to P-007. If the existing AGENTS.md mentions `git subtree`, `git subtree pull`, `git subtree push`, `subtree add`, `.gitmodules`, or `git submodule` in the Active Context / Structure / Project-specific rules sections, propose a rewrite to the canonical clone+gitignore form. Canonical Active Context bullet template (substitute the repo name for `make-ai-agents`): `\`make-ai-agents\` is a **local clone, gitignored** at \`make-ai-agents/\` (not a subtree, not a submodule — see \`.gitignore\`). Refresh with \`cd make-ai-agents && git pull\`. Re-clone fresh by removing the folder and running \`git clone https://github.com/chaz-clark/Make-AI-Agents.git make-ai-agents\` from the repo root.` Surface each rewrite in the refresh handoff doc so the maintainer sees the change explicitly.
- Together: lean AGENTS.md prose + co-located discipline files + current vendoring-pattern language = discipline propagates correctly without duplication-drift, broken-reference, or stale-instruction-drift.

### 2. Stale Active Context

**Problem**: Six months after generation, the Active Context section still says "v3.0 just shipped" and lists issues that were closed long ago.

**Why it happens**: Active Context isn't owned by the make_AGENTS skill after generation — it's the developer's responsibility to update.

**Solution**: Generate the Active Context section with a date stamp at the top: `_Last updated: YYYY-MM-DD_`. Include a comment in the section explaining when it should be refreshed.

### 3. Tool-Specific Instructions

**Problem**: Generated AGENTS.md contains "When using Claude Code, do X" — defeating the tool-agnostic purpose.

**Why it happens**: Source material (existing CLAUDE.md) had Claude-specific language; skill carries it over verbatim.

**Solution**: When migrating from CLAUDE.md, sanitize tool-specific language. "Claude reads this" → "the LLM reads this." If guidance is genuinely tool-specific, it belongs in tool-specific config (`.cursorrules`, `.aider.conf.yml`), not AGENTS.md.

### 4. Generated AGENTS.md Without Discipline Embed

**Problem**: Skill generates the AGENTS.md but forgets to embed the behavioral discipline pointer in Working Style.

**Why it happens**: Forgetting the propagation layer; treating AGENTS.md as static documentation.

**Solution**: BD-AGENTS-QC-001 (in `make_AGENTS.json`) checks for the discipline pointer in the Working Style section. If missing, regenerate.

---

## Examples (core)

### Example 1: Bare-Bones AGENTS.md

For a small project with no domain-heavy vocabulary, no external systems, and no in-flight migration:

```markdown
# Example Repo

A short Python utility for generating reports.

## Project Purpose

**This is**: A standalone CLI tool that generates weekly reports from a SQL database.

**This is NOT**: A library, a service, or a web app.

**Audience**: Internal data team.

## Structure

```
example-repo/
├── src/                  # Python source
├── tests/                # pytest tests
├── reports/              # Generated reports (gitignored)
└── pyproject.toml        # Dependencies and config
```

## Working Style

This project follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` (if present) or the equivalent ruleset in the LLM's loaded skills. In short: read before claiming, plan before acting, stop on defect, document changes structurally, respect user intent.

Project-specific rules:
- Use `pytest` for tests
- Match existing code style (no new style introductions)

## Active Context

_Last updated: 2026-04-29_

- v1.2 just shipped (added CSV export)
- Open issues: #5 (timezone bug), #7 (PostgreSQL 16 compatibility)
- Next: rewrite the report renderer to support multiple output formats
```

### Example 2: AGENTS.md for a Repo Mid-Migration

See the AGENTS.md generated for this `Make-AI-Agents` repo as a worked example, especially the `## Migration Notes` section documenting CLAUDE.md → AGENTS.md status.

---

## Validation and Testing (core)

### Quick Validation
1. Generated AGENTS.md exists at project root
2. All required sections present in order
3. Working Style section contains the discipline pointer
4. No tool-specific language in the file body
5. Active Context has a date stamp

### Comprehensive Validation
For full structured validation, see `make_AGENTS.json` → `validation.test_cases`. The validation includes:
- Required section checklist
- Discipline embed presence check
- Tool-agnostic language scan
- Optional section criteria audit (if section X is present, criteria for X must apply)

### Does `make_agent_qc` apply to AGENTS.md?

**Partially**. AGENTS.md is structurally similar to an agent spec MD, but it has different required sections and a different audience. Of the 18 rules in `make_agent_qc.json`:
- **Apply directly**: Rules 1, 2, 3, 4, 5, 7, 8 (core completeness, specificity, cleanup, consistency, examples, dependencies, documentation)
- **Don't apply**: Rules 9, 13, 14, 15, 16 (LLM agent-specific or specific to agent spec sections like Domain Terms-the-section)
- **Adapted**: Rule 17 (Behavioral Discipline Compliance) → check the discipline pointer is embedded in Working Style; not the full discipline section
- **Project-specific**: Rule 18 (Non-Interactive Mode) → not applicable to AGENTS.md generation itself

A future `make_AGENTS_qc.md` would be the cleaner long-term solution. For now, manual validation against the checklist in `make_AGENTS.json` works.

---

## Resources and References

### Skill Files
- **`make_AGENTS.json`**: Required/optional section lists, AGENTS.md template, compact_boilerplate, validation
- **`make_agent.md`**: Sibling template for generating agent specs (referenced for the integration flow pattern)
- **`make_gem.md`**: Sibling template for Gemini Gems
- **`knowledge/behavioral_discipline.md` / `.json`**: Source of truth for the discipline embedded in every generated AGENTS.md

### Related Skills
- `make_agent` — generates agent specs
- `make_gem` — generates Gemini Gem instructions
- `make_agent_qc` — validates agent specs (partial applicability to AGENTS.md)

### How to Use This Documentation System
1. Start here (.md) for conceptual understanding
2. Use `make_AGENTS.json` for the template structure
3. Reference `make_agent.md` for the integration flow pattern (recursive — same flow applies to this skill)
4. Reference `knowledge/behavioral_discipline.md` for the discipline that gets embedded

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Generate tool-agnostic AGENTS.md project context files |
| **Input** | Project root directory; optionally an existing CLAUDE.md to migrate from |
| **Output** | AGENTS.md file at project root |
| **Skill Type** | workflow (single AGENTS.md per invocation) |
| **Interaction Pattern** | `single_write_workflow` |
| **Complexity** | simple-to-standard |
| **Key Files** | `make_AGENTS.json`, `make_AGENTS.md`, generates `<project>/AGENTS.md` |
| **Common Pitfall** | Duplicating discipline content instead of pointing to it |
| **Dependencies** | knowledge/behavioral_discipline.md/.json (for the embed) |
