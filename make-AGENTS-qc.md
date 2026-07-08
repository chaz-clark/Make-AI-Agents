---
name: make_AGENTS_qc
description: Quality-control checks for generated AGENTS.md files. Validates against the contract defined in make_AGENTS.md and BD-QC rules in behavioral_discipline.json.
version: "1.0"
last_updated: 2026-04-29
author: chaz-clark
license: MIT
optional: true
rules: 11
dimensions: 6
agent_type: rule_based
interaction_pattern: read_only
complexity: simple
applicable_principles:
  - P-001
  - P-003
  - P-007
  - P-008
  - P-009
  - P-010
dependencies:
  - make_AGENTS.md (contract source - see Required/Optional Sections)
  - knowledge/behavioral_discipline.json (discipline source)
when_to_use:
  - After generating a new AGENTS.md via make_AGENTS
  - Before merging a PR that modifies AGENTS.md
  - Quarterly drift audit
  - During CLAUDE.md to AGENTS.md migrations
when_to_skip:
  - Validating agent specs (use make_agent_qc)
  - Validating Gem instructions (use make_gems/make_gem_qc)
  - Real-time editing feedback (too heavyweight)
metadata:
  make-ai-agents:
    skill_type: qc
    companion_json_deprecated: "2026-07-07 - consolidated into YAML frontmatter"
---

# make_AGENTS_qc — AGENTS.md Quality Control

## Agent Instructions
1. Read this for mission, principles, common pitfalls, and how to interpret QC reports.
2. Parse `make_AGENTS_qc.json` for structured rules, scoring weights, and test cases. Do not parse this Markdown for structured rules.
3. This QC validates a single artifact: a project's `AGENTS.md` file. It does not validate agent specs (use `make_agent_qc`) or Gem instructions (use `make_gems/make_gem_qc`).
4. **Behavioral Discipline applies to this skill itself.** This QC operates as `interaction_pattern: read_only` — read the AGENTS.md, read the repo it claims to describe, produce a report. No writes. See `## Behavioral Discipline (core)` below.

---

## Mission (core)

**What it does**: Validates an `AGENTS.md` file (and optionally the repo it describes) against the contract defined in `make_AGENTS.md` (see **## Contract: Required Sections** and **## Contract: Optional Sections**). Scores across 6 quality dimensions and surfaces specific issues with severity and recommendations.

**Why it exists**: An AGENTS.md is the first file an agentic dev tool reads when entering a project. Drift between AGENTS.md and the actual repo state silently misleads every LLM that reads it. The QC catches drift before it lands.

**Who uses it**: Developers who have generated or updated an AGENTS.md (e.g., via `make_AGENTS`), or who are auditing an existing AGENTS.md before a migration or major version push.

**Example**: "Validated `Make-AI-Agents/AGENTS.md` against the make_AGENTS contract. Score: 96/100. One medium issue: Active Context date stamp is 90+ days stale. Two info notes: optional Domain Terms section could be tightened. No critical issues."

---

## Quickstart (core)

A fast-path validation flow:

1. **[Locate]**: Find the target `AGENTS.md` and (optionally) the repo root it describes.
   - Example: `AGENTS.md` at `/path/to/project/AGENTS.md`; repo root is `/path/to/project/`.

2. **[Parse rules]**: Load structured rules from `make_AGENTS_qc.json` — the 11 rules, their weights, and severity levels.

3. **[Read sources]**: Read the AGENTS.md fully. If repo root is provided, read the discipline source at `knowledge/behavioral-discipline.md/.json` (or equivalent) and run `git ls-files` for the structure check.

4. **[Validate]**: Run all applicable rules. Each rule produces pass/fail + a severity-tagged finding if failed.

5. **[Score]**: Calculate dimension scores (0-100 each) and overall score (weighted average). Map score to status: ≥95 PASS, 80-94 NEEDS_IMPROVEMENT, <80 FAIL.

6. **[Report]**: Output a structured report with critical issues first, then recommendations.

For detailed rules and scoring, see `make_AGENTS_qc.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- Mission and validation philosophy
- The six quality dimensions explained narratively
- How to interpret report severity
- Common pitfalls in AGENTS.md authorship
- Worked examples of good and broken AGENTS.md files

### The JSON File (.json) Contains:
- The 11 numbered rules with conditions, actions, weights, severity
- Quality dimension definitions with weights
- Severity levels (critical / high / medium / low)
- Test cases and expected outputs
- Pattern matching rules (placeholder detection, tool-specific language detection)

**Rule of Thumb**: Validation logic and scoring → JSON. Why each check matters → MD.

---

## Key Principles (core)

### 1. Validate Against the Contract, Not Aesthetics
**Description**: The contract is defined in `make_AGENTS.md` → **## Contract: Required Sections** (6 sections) and **## Contract: Optional Sections** (5 sections with `include_when` criteria). The QC validates that contract — not stylistic preferences.

**Why**: An AGENTS.md is a contract between project state and the LLM reading it. If it satisfies the contract and accurately reflects the repo, it's a good AGENTS.md regardless of aesthetic.

**How**: Reference the contract sections in `make_AGENTS.md` when applying rules. If a check seems to require a stylistic judgment, raise it as a recommendation, not a rule violation.

### 2. Genchi Genbutsu — Verify Claims Against Reality
**Description**: AGENTS.md makes claims about the repo (Structure, file paths, recent commits, open issues). When the repo is accessible, verify those claims by going to the source. Flag drift.

**Why**: An AGENTS.md that says the repo has `gem_instructions/` when it doesn't, or claims "v3.0 just shipped" when the latest commit is unrelated, silently misleads every LLM that reads it. This is the failure mode the QC exists to catch.

**How**: When a repo path is provided, run `git ls-files`, `git log --oneline -1`, and `gh issue list --state open` (if applicable). Compare claims in AGENTS.md to actual output. Flag mismatches.

### 3. Pointer, Not Duplicate
**Description**: AGENTS.md should *point to* the behavioral discipline (`knowledge/behavioral-discipline.md`), not paraphrase or duplicate it.

**Why**: Duplication rots. When the discipline updates, every paraphrase becomes stale. A pointer stays current automatically.

**How**: Rule 6 (Discipline Pointer Quality) flags Working Style sections that contain more than ~3 sentences of original prose about the discipline. The discipline pointer should be a reference, not a summary.

### 4. Currency Matters More Than Coverage
**Description**: A short, current Active Context section is worth more than a long, stale one.

**Why**: Active Context is the section that decays fastest and is most consulted by LLMs deciding what to do next. Stale Active Context is worse than absent — it confidently misleads.

**How**: Rule 8 (Active Context Currency) flags missing date stamps as high-severity and flags stamps older than 90 days as medium. The QC does not check whether the *content* of Active Context is current (that requires domain knowledge); it checks the date and structure.

### 5. Tool-Agnostic Discipline
**Description**: AGENTS.md is the standard for any agentic dev tool. Tool-specific instructions belong in tool-specific config files, not in AGENTS.md.

**Why**: The whole point of AGENTS.md (over CLAUDE.md, .cursorrules, etc.) is that any tool can read it. Tool-specific instructions defeat the migration.

**How**: Rule 4 (Tool-Specific Language) scans for directive phrases ("when using Claude Code do X", "in Cursor only", "Aider should..."). Naming tools as a *list of consumers* is fine ("readable by Claude Code, Cursor, Aider, Antigravity"). Naming a tool as the *actor* is not.

---

## Behavioral Discipline (core)

This QC skill operates under the discipline defined in `knowledge/behavioral-discipline.md` and `knowledge/behavioral_discipline.json`. The applicable interaction pattern for this skill is `read_only`:

- **P-001 Read Before Claiming**: read the actual AGENTS.md and the actual repo state. Don't infer either from training priors.
- **P-003 Stop on Defect**: if a critical rule fails (Rules 1, 2, or 6), surface the failure prominently and recommend fixing before considering other rules.
- **P-007 Pull, Don't Push**: produce only the validation report — no speculative recommendations beyond what the rules require.
- **P-008 Mistake-Proof Outputs**: every QC report uses the same structured format (see `make_AGENTS_qc.json` → `output_format.report_template`). No prose-vs-JSON variance.
- **P-009 Reflect, and Tell the User**: if a validation surfaces a non-obvious AGENTS.md authorship pitfall, end the report with a `Worth noting:` line.
- **P-010 Respect the User's Intent**: don't editorialize beyond what the rules say. The user asked for validation; don't substitute opinions.

P-002, P-004, P-005, P-006 are skipped per `read_only.skip_unless_applicable` — no state changes, no multi-step work, no documentation artifact to produce beyond the report.

---

## How to Use This Skill (core)

### Prerequisites
- Target `AGENTS.md` file accessible
- Repo root accessible (optional but recommended for Genchi Genbutsu rules)
- `make_AGENTS_qc.json` readable (for rules and scoring)
- `make_AGENTS.md` readable (for the contract definitions in Required/Optional Sections)
- `knowledge/behavioral-discipline.md/.json` readable (for the discipline reference)

### Basic Usage

Conversational invocation — this is a meta-skill, not a script. Example prompt to your agentic dev tool:

> "Use `make-AGENTS-qc.md` and `make_AGENTS_qc.json` to validate `<path>/AGENTS.md` against the make_AGENTS contract. The repo root is `<path>/`. Apply all 11 rules. Output a scored report with critical issues first."

The skill responds with a structured report (see `make_AGENTS_qc.json` → `output_format`).

### Strict Mode

For pre-merge validation or release gates, ask the skill to run in strict mode:

> "Run make_AGENTS_qc on AGENTS.md in strict mode — fail on any critical or high-severity issue."

Strict mode does not change the rules; it changes the pass threshold (default 80 → strict 95) and the failure response (failed checks halt the run rather than producing a report).

---

## Common Pitfalls (core)

### 1. AGENTS.md drifts from repo state silently

**Problem**: AGENTS.md was generated correctly months ago, but the repo has changed: new top-level folders, removed example agents, renamed files. AGENTS.md still claims the old structure.

**Why it happens**: AGENTS.md isn't owned by an automated process after generation; developers update repo content but forget to refresh AGENTS.md.

**Solution**: Rule 7 (Structure Accuracy) catches this when the repo is accessible. Run `make_AGENTS_qc` before any release or major branch merge. Better long-term: regenerate AGENTS.md via `make_AGENTS` quarterly or after major shipped work.

### 2. Working Style duplicates the discipline instead of pointing

**Problem**: Working Style section paraphrases the 10 principles inline ("Read before claiming, plan before acting, ..."). The paraphrase rots when the discipline file updates.

**Why it happens**: First-pass `make_AGENTS` outputs sometimes inline a summary because the LLM treats "context" as "include everything."

**Solution**: Rule 6 (Discipline Pointer Quality) flags Working Style sections with >3 sentences of original discipline prose. Replace with a pointer + the no-override IDs only.

### 3. Active Context is a static log

**Problem**: Active Context section reads like a changelog ("v1.0 shipped, v1.1 shipped, v1.2 shipped") instead of current state ("v3.0 just shipped; AGENTS.md migration in flight").

**Why it happens**: Authors append rather than overwrite. Old "Recent shipped" items accumulate; nothing flags what's *current*.

**Solution**: Active Context should describe **current** state — what shipped most recently (1-3 items max), what's in flight, what's next. Older history lives in `git log` and the changelog, not here. Rule 8 doesn't catch this directly (the QC can't judge "current"), but the principle informs Rule 8's date-stamp check: if the stamp is fresh, the content should be too.

### 4. Tool-specific language creeps in via migrated CLAUDE.md content

**Problem**: When migrating from CLAUDE.md to AGENTS.md, the source had "When Claude does X, ..." phrases. These get carried over verbatim, defeating the tool-agnostic purpose.

**Why it happens**: CLAUDE.md was Claude-specific by name; the prose often was too. Migration without sanitization preserves the bias.

**Solution**: Rule 4 (Tool-Specific Language) scans for directive phrases. The fix is mechanical: replace tool names used as actors with "the LLM" or "your agentic tool".

### 5. Optional sections padded in without earning their place

**Problem**: AGENTS.md includes a Domain Terms table with placeholder rows like `[TERM] | [Definition]` because the author saw it in the template.

**Why it happens**: Authors interpret "optional" as "include if you can fill it" rather than "include only if criteria apply".

**Solution**: Rule 5 (Optional Section Justification) checks each optional section against its `include_when` criterion in `make_AGENTS.md` → **## Contract: Optional Sections**. If the criterion isn't met, the section gets flagged for removal. Empty/placeholder rows count as failure to meet criterion.

---

## Examples (core)

### Example 1: Validating a Strong AGENTS.md

**Scenario**: A new developer just generated `AGENTS.md` for the `Make-AI-Agents` repo using `make_AGENTS`. They want to validate it before committing.

**Input**:
- `agents_md_path`: `/Users/chazclar/Documents/GitHub/Make-AI-Agents/AGENTS.md`
- `repo_root`: `/Users/chazclar/Documents/GitHub/Make-AI-Agents`
- `strict_mode`: false

**Approach**: Skill loads rules from `make_AGENTS_qc.json`, reads AGENTS.md, runs `git ls-files` to verify Structure section, scores all rules.

**Output (excerpt)**:
```
Score: 96/100 — PASS
Dimensions:
  Completeness: 100
  Specificity: 95
  Discipline Integration: 100
  Currency: 95
  Tool-Agnosticism: 100
  Optional Section Justification: 90
Critical issues: 0
High-severity issues: 0
Medium-severity issues: 1
  - AGENTS-QC-005: Domain Terms entry "non_interactive_mode" is borderline non-obvious. Consider whether it earns its place or move to README.
Recommendations:
  - Fresh-as-of-today; nothing actionable.
```

### Example 2: Validating a Drifting AGENTS.md

**Scenario**: An AGENTS.md generated 6 months ago. Repo has since moved several agents to their own repos and added a new top-level folder.

**Input**: same form, different repo.

**Output (excerpt)**:
```
Score: 71/100 — NEEDS_IMPROVEMENT
Critical issues: 1
  - AGENTS-QC-007 (Structure Accuracy): AGENTS.md claims `canvas_course_expert/` exists at top level; repo does not contain this folder. Drift confirmed via git ls-files.
High-severity issues: 2
  - AGENTS-QC-008 (Active Context Currency): Date stamp is 187 days old.
  - AGENTS-QC-006 (Discipline Pointer Quality): Working Style contains 8 sentences of original prose paraphrasing the 10 principles. Should be a pointer.
Medium-severity issues: 1
  - AGENTS-QC-005: Optional "Migration Notes" section claims migration is in flight but no evidence of migration in repo.
Recommendations:
  - Regenerate AGENTS.md via make_AGENTS using current repo state.
  - At minimum, fix Structure section and refresh Active Context date stamp.
```

### Example 3: AGENTS.md Without Repo Access

**Scenario**: Validating an AGENTS.md from a different team's project where you only have the file, not the repo.

**Approach**: Skill applies Rules 1, 2, 3, 4, 5, 6, 8, 9, 10, 11 (the rules that don't require repo access). Skips Rule 7 (Structure Accuracy) and any deep verification. Notes the limitation in the report header.

---

## Validation and Testing (core)

### Quick Validation
1. Run on a known-good AGENTS.md (e.g., this repo's): score should be ≥95.
2. Run on a deliberately broken AGENTS.md (placeholder rows, wrong dates, missing sections): score should be <70 with specific issues called out.
3. Run on the same AGENTS.md twice: identical output (deterministic per P-008).

### Comprehensive Validation
For full structured tests, see `make_AGENTS_qc.json` → `validation.test_cases`. Tests cover:
- All 5 required sections present in order (Rule 1)
- Discipline pointer present in Working Style (Rule 2)
- Date stamp present and parseable (Rule 3)
- No tool-specific directive language (Rule 4)
- Optional sections meet inclusion criteria (Rule 5)
- Discipline pointer is a pointer, not a duplicate (Rule 6)
- Structure section matches `git ls-files` output (Rule 7, requires repo access)
- Active Context date stamp ≤ 90 days old (Rule 8)
- No template placeholders in body (Rule 9)
- Total file size within thresholds (Rule 10)
- Active Context is current-state-only, not append-only log (Rule 11)

### Quality Dimensions (6)

1. **Completeness** — All 5 required sections present and in order. Weight: 0.25
2. **Specificity** — No placeholders or template artifacts in non-template sections. Weight: 0.15
3. **Discipline Integration** — Working Style points to the discipline file and does not duplicate. Weight: 0.20
4. **Currency** — Date stamp present, parseable, and within freshness threshold. Weight: 0.15
5. **Tool-Agnosticism** — No tool-specific directive language in body. Weight: 0.10
6. **Optional Section Justification** — Each present optional section meets its `include_when` criterion. Weight: 0.15

For canonical scoring weights and rule-to-dimension mapping, see `make_AGENTS_qc.json` → `validation_rules_detailed.dimensions`.

### Scoring Interpretation
- **95-100**: PASS. Ship-ready.
- **80-94**: NEEDS_IMPROVEMENT. Address recommendations before next major commit touching AGENTS.md.
- **<80**: FAIL. Critical or multiple high-severity issues. Regenerate or substantively revise.

---

## Operational Guidance

### When to Use This QC

**Use for**:
- After generating a new AGENTS.md via `make_AGENTS`
- Before merging a PR that updates AGENTS.md
- Periodic audit (recommended: quarterly) to catch drift
- During CLAUDE.md → AGENTS.md migrations
- When an LLM reading AGENTS.md gives clearly wrong answers about the project — drift is the likely cause

**Don't use for**:
- Validating agent specs (use `make_agent_qc`)
- Validating Gem instructions (use `make_gems/make_gem_qc`)
- Validating arbitrary markdown documentation
- Real-time editing feedback (too heavyweight; use IDE linting)

### Best Practices
1. Run with repo access whenever possible — Rule 7 is the highest-value drift catcher.
2. Use non-strict mode during development; strict mode for release gates only.
3. Fix critical issues first. Most other issues are easier to fix once Structure and Discipline Integration are correct.
4. Don't argue with Rule 7 — if the repo state and AGENTS.md disagree, the repo wins.

---

## Resources and References

### Skill Files
- **`make_AGENTS_qc.json`**: Rules, scoring weights, test cases, output format
- **`make_AGENTS.md` / `.json`**: The contract this QC validates against
- **`knowledge/behavioral-discipline.md` / `.json`**: The discipline this skill itself operates under (and that AGENTS.md files reference)

### Related Skills
- `make_AGENTS` — generates AGENTS.md (this QC validates its output)
- `make_agent_qc` — sibling QC for agent specs
- `make_gems/make_gem_qc` — sibling QC for Gem instructions

### How to Use This Documentation System
1. **Start here** (.md) for validation philosophy and pitfalls
2. **Use JSON** for the structured rules and scoring
3. **Reference `make_AGENTS.json`** for the contract being validated

---

## Quick Reference Card

| Aspect | Value |
|---|---|
| **Purpose** | Validate AGENTS.md files against the make_AGENTS contract |
| **Input** | Path to target `AGENTS.md`; optional repo root for Genchi Genbutsu rules |
| **Output** | Scored report (0-100) with severity-tagged issues and recommendations |
| **Skill Type** | rule_based, validation-only |
| **Interaction Pattern** | `read_only` |
| **Complexity** | simple-to-standard |
| **Key Files** | `make_AGENTS_qc.json`, `make-AGENTS-qc.md` |
| **Common Pitfall** | Running without repo access — skips highest-value drift detection |
| **Dependencies** | knowledge/behavioral-discipline.md/.json, make_AGENTS.md |
