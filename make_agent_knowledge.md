---
name: make_agent_knowledge
description: Generates knowledge files (.md + .json) consumed by Make-AI-Agents agents at runtime. Reference / Identity / Procedural shapes.
version: "1.1"
author: chaz-clark
license: MIT
metadata:
  make-ai-agents:
    spec_json: make_agent_knowledge.json
    skill_type: meta
---

# make_agent_knowledge Skill Guide

## Skill Instructions
1. Read this for mission, principles, the three knowledge shapes, and pitfalls.
2. Parse `make_agent_knowledge.json` for structured data — required/optional MD sections per shape, JSON skeleton, compact_boilerplate, runtime_strategy rules, validation, and the KNW-QC family.
3. This skill is an **authoring scaffold only**. It produces empty-but-structured MD+JSON templates for the user to fill. It does NOT ingest source material, fetch documents, or auto-populate content from external systems.
4. **Behavioral Discipline is required.** Consult `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The make_agent_knowledge skill operates as `interaction_pattern: single_write_workflow` and follows the integration flow defined in [make_agent.md](make_agent.md) → "## Behavioral Discipline (core)" unchanged.

---

## Mission (core)

**What it does**: Generates a knowledge file pair (`<name>.md` + `<name>.json`) inside `knowledge/` at the project root. The file pair is a **runtime artifact** that one or more agents reference via their `cross_references.knowledge_files[]` array. Three shapes are supported: **reference** (glossary, API ref, policy table), **identity** (principles, values, working-style charters), and **procedural** (playbooks, scenario scripts).

**Why it exists**: Knowledge that an agent needs at runtime — facts, principles, playbooks — does not belong in the agent spec. Embedding it bloats the system prompt; scattering it across `source_docs/` mixes runtime artifacts with research notes. The existing `knowledge/behavioral_discipline.md/.json` pair is the proven exemplar: a stable, structured, agent-consumable file that lives next to the agents that read it. This skill formalizes that pattern so any agent can have its own `behavioral_discipline`-style knowledge file with the same authoring discipline.

**Who uses it**: Engineers adding domain knowledge, identity charters, or playbooks to an agent or set of agents — typically discovered when a `make_agent` invocation reveals "this agent needs to know X, but X is not in the prompt and not in source_docs."

**Example**: "Generate a `knowledge/loan_underwriting_glossary.md/.json` (shape=reference, consumed_by=[loan_classifier_agent.json]) with empty `facts[]` array and the standard provenance block; user fills in the glossary terms in a follow-up edit."

---

## Quickstart (core)

0. **[Pick the shape, then embed discipline]**: Decide reference / identity / procedural BEFORE drafting content (see "## The Three Shapes (core)" below for the decision). This skill is itself `single_write_workflow` — one knowledge file pair per invocation.

1. **[Gather inputs]**: knowledge_name (snake_case), shape, scope (one-line description of what this knowledge covers), `consumed_by` (array of agent spec paths that will reference this file). Optional: provenance source list, owner.

2. **[Parse template]**: Load `make_agent_knowledge.json` → `knowledge_shapes.<shape>` for the per-shape required MD sections and required JSON fields, plus `knowledge_md_required_sections` for the common spine, plus `compact_boilerplate.<shape>` for the body skeleton.

3. **[Propose]**: Present the generated MD + JSON drafts to the user. Per P-002, do not write until confirmed.

4. **[Write]**: Write `knowledge/<knowledge_name>.md` and `knowledge/<knowledge_name>.json`. Both files are written together; the pair is not optional.

5. **[Cross-link]**: Remind the user to add `knowledge/<knowledge_name>.json` to each consuming agent's `cross_references.knowledge_files[]` array. This skill does NOT modify the consuming agent's spec — that is a follow-up step the user (or `make_agent`) performs.

For detailed structure, see `make_agent_knowledge.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- Mission, principles, narrative
- The three shapes — what each is and when to use it
- Runtime loading philosophy
- Common pitfalls

### The JSON File (.json) Contains:
- `knowledge_shapes` — per-shape required MD sections + required JSON fields
- `knowledge_md_required_sections` — the common spine every shape inherits
- `knowledge_json_skeleton` — the JSON template this skill writes
- `compact_boilerplate` — body skeletons per shape + runtime_strategy declaration
- `runtime_strategy_rules` — declarative thresholds for embed vs. read-at-runtime
- `validation.test_cases` and the KNW-QC family

**Rule of Thumb**: If the skill needs to parse it → JSON. If a developer needs to understand the "why" → MD. The same split applies to every knowledge file this skill generates.

---

## Key Principles (core)

### 1. Knowledge Files Are Runtime Artifacts, Not Source Docs
**Description**: `knowledge/*` files are read by the running agent at inference time. `source_docs/*` files are research notes for the human author of a skill or agent. The two do not overlap.
**Why**: An agent that loads `source_docs/anthropic_files.md` at runtime burns context on platform documentation that the agent does not act on. A skill author who edits `knowledge/behavioral_discipline.md` thinking it is research notes corrupts a live runtime file.
**How**: If the content will be referenced by a `cross_references.knowledge_files[]` entry in a deployed agent spec, it belongs in `knowledge/`. If it is documentation cached for the human writing the skill, it belongs in `source_docs/`.

### 2. Pick the Shape Before Filling Content
**Description**: Decide reference / identity / procedural before drafting any body content. Each shape has different required JSON fields (`facts[]` vs. `principles[]` vs. `playbooks[]`) and different validation rules.
**Why**: Shape-shifting mid-draft produces files that fail KNW-QC-003 — a "reference" with no `facts[]` or an "identity" file with `playbooks[]` mixed in. The shape encodes a contract; violating it leaves consumers unable to parse the file reliably.
**How**: Use the decision rubric in "## The Three Shapes (core)". When in doubt between identity and procedural (a common collision), pick identity if the content describes *who the agent is* and procedural if it describes *what the agent does in scenario X*.

### 3. Embed-vs-Retrieve Is a Runtime Tradeoff, Not a Content Decision
**Description**: How the agent loads the knowledge file at runtime (embedded in the system prompt vs. read on demand via a platform Files/Search primitive) is a deployment concern declared in `_metadata.runtime_strategy`. It does not change what the knowledge file contains.
**Why**: A knowledge file written for one strategy and then needed under another (e.g., grew past the embedding threshold, or needs citations) should not require a rewrite. The structured shape stays constant; only the loading mechanism changes.
**How**: This skill writes `_metadata.runtime_strategy` based on the rules in `runtime_strategy_rules` (token count thresholds). The default is `embed` for files under ~2000 tokens and `read_at_runtime` for files over ~8000 tokens, with an "either" band between. Authors can override with rationale.

### 4. Citations Require Structured Source Provenance
**Description**: Any knowledge file whose consumers will cite back to the source (reference shape especially, but also playbooks that quote policy) must carry a `provenance.sources[]` array with non-empty entries identifying where the facts came from.
**Why**: Anthropic Citations, OpenAI file_search citations, and xAI `collections://` URIs all require the runner to resolve a citation back to a source. A knowledge file with no provenance produces "trust me" answers that audit poorly.
**How**: For shape=reference, KNW-QC-005 enforces non-empty `provenance.sources[]`. For shape=identity, provenance is optional (the agent IS the source). For shape=procedural, provenance is recommended when the playbook references an external policy.

### 5. Knowledge Is Per-Agent Unless Cross-Cutting
**Description**: Default to one knowledge file per agent that needs it. Promote to a shared file only when multiple agents would consume the same content unchanged.
**Why**: Shared knowledge files become coupling points — a change for agent A breaks agent B. The exemplar (`behavioral_discipline`) is shared because every agent inherits the same discipline; most domain knowledge is not like that.
**How**: `consumed_by[]` in the generated JSON records who reads the file. If the array has one entry, the file is agent-specific (name it accordingly: `<agent_name>_<topic>.md`). If multiple agents will share it AND the content does not need to diverge, share — otherwise duplicate.

---

## Behavioral Discipline (core)

This skill operates as `interaction_pattern: single_write_workflow` (one knowledge file pair per invocation). Applicable principles: P-001, P-002, P-003, P-004, P-006, P-007, P-008, P-009, P-010 (skip P-005 — single-step workflow, no decomposition).

The full integration flow is documented once, in [make_agent.md](make_agent.md) → "## Behavioral Discipline (core)". This skill follows it unchanged. The QC checks BD-QC-001 through BD-QC-007 apply to this skill itself.

**Two layers note**: The generated knowledge file does NOT itself carry a `behavioral_discipline` block — knowledge files are not agents. They are read BY agents that carry the discipline. The discipline pointer in a consuming agent already governs how that agent uses any knowledge file it loads.

---

## Retrofit Mode (core)

When a knowledge file already exists as a hand-authored `.md` with no `.json` companion (the common case for repos like `canvas-toolbox/lib/agents/knowledge/`), the make_agent_knowledge skill MUST support retrofitting the file into the MD+JSON pair shape rather than requiring a full regenerate. The output is structurally indistinguishable from a greenfield-generated pair — only the entry point differs.

Retrofit checklist (parallel to the greenfield Quickstart, but starting from an existing `.md`):

1. **Read the existing MD fully** before making any claim about its shape, sections, or gaps. P-001 — don't infer from filename.

2. **Classify the likely shape** using `_classification_guidance.decision_flow` in `make_agent_knowledge.json` → `knowledge_shapes`. Reference for lookup files, identity for principle/charter files (including framework charters — collapse the frame to a single named principle), procedural for trigger-keyed playbooks. **MUST confirm with the user** when ambiguous — don't silently pick.

3. **Detect header convention** in the existing MD. If the file uses `Source:` / `Used by:` / `Companions:` lines at the top (canvas-toolbox form), KEEP that convention — do not rewrite to canonical `**Scope**:` / `**Provenance**:` form just for cosmetic uniformity. Both forms are listed as accepted variants in `make_agent_knowledge.json` → `compact_boilerplate.header_convention_variants` and map equivalently to the JSON companion's structured fields.

4. **Author the `.json` companion** by extracting:
   - `_metadata.knowledge_id` — slug-form of the filename
   - `_metadata.runtime_strategy` — measured from MD body size per `runtime_strategy_rules`; apply a `named_override_patterns` override if applicable (e.g., `selective_load` if the consuming agents read knowledge selectively per task)
   - `shape` — per step 2
   - `scope` — copy from the MD's Scope / first paragraph
   - `consumed_by[]` — extract from the existing `Used by:` line (canvas-toolbox form) or the body prose if named there. Per KNW-QC-006, an empty `consumed_by[]` is a critical fail; if no consumer is named anywhere, halt and ask the user.
   - `provenance.sources[]` — extract from the existing `Source:` line or `**Provenance**:` paragraph. Required for `shape=reference` (KNW-QC-005).
   - `facts[]` / `principles[]` / `playbooks[]` — populate the shape-specific array by parsing the MD body sections. Use stub entries with `id` + `name` + a one-line summary if the source content is dense; the author can expand later.

5. **Do NOT rewrite the MD body** unless explicitly asked (P-007 Pull Don't Push). The retrofit ADDS the JSON companion; it does not refactor the existing MD. Exception: if the MD is missing a required spine section that KNW-QC-001 will fail (e.g., no `_Last updated_` footer), add the minimum needed — and surface the addition to the user.

6. **Run KNW-QC-001..007** against the retrofitted pair. Use the `_md_only_applicability` clauses on each check to distinguish "fail" from "N/A on this legacy file" — the retrofitted file SHOULD pass most checks now that the JSON is present, but some checks may still need manual disambiguation (e.g., `consumed_by[]` populated but agent specs don't yet reference back via `cross_references.knowledge_files[]` — that's a downstream wiring step).

7. **Report** what was added (the JSON file), what was preserved (the MD body and header convention), and what's queued for follow-up (downstream cross-references in consuming agents).

The retrofit is also the migration path for any pre-`make_agent_knowledge` knowledge files that exist in older repos. Once retrofitted, those knowledge files pass KNW-QC alongside greenfield-generated pairs.

---

## File I/O Mode (core)

**This skill's input**: `string` (interactive — user supplies shape, knowledge_name, scope, owner_agents conversationally).

**The generated knowledge file's I/O mode**: N/A. Knowledge files are read by agents; they are not themselves agents and do not declare an `io_contract`. The consuming agent's `io_contract` governs the workflow that consults the knowledge file.

---

## The Three Shapes (core)

Pick the shape before drafting. Each shape has a different required JSON array and a different MD spine.

### Reference

**What it is**: A lookup file. Glossary, API reference, policy table, term-to-definition map. The agent consults it the way a developer consults a manpage — to resolve a specific term or fetch a specific fact.

**When to use**: The content is a set of discrete, indexable items (terms, entries, rules) that the agent looks up rather than reads end-to-end. Order of entries does not change meaning.

**MD spine**: title, scope, provenance, last_updated, body (table or per-entry sections).

**JSON required**: `facts[]` — array of `{ id, term, definition, citations?[] }` entries. `provenance.sources[]` must be non-empty (KNW-QC-005).

**Example use**: `loan_underwriting_glossary` consumed by a `loan_classifier_agent` that needs to disambiguate "LTV", "DTI", "PMI" against this lender's specific definitions, not the public Wikipedia ones.

### Identity

**What it is**: A principles/values/charter file. Describes WHO the agent is and how it behaves at the system level. The agent loads it once and operates under it for the duration of a session.

**When to use**: The content is a small (5-15) set of named principles, each with a description, rationale, trigger, and trust marker. Order matters (principles are numbered/IDed).

**MD spine**: title, scope, provenance (optional), last_updated, body (one section per principle).

**JSON required**: `principles[]` — array of `{ id, name, compact_statement, trigger, trust_marker, override?{} }` entries. The existing `knowledge/behavioral_discipline.md/.json` is the proven exemplar of this shape — this skill formalizes the pattern it demonstrates.

**Example use**: `behavioral_discipline` itself (the universal example), or an agent-specific identity charter like `loan_classifier_principles` if that agent has discipline beyond the universal BD set.

### Procedural

**What it is**: A playbook file. Describes WHAT the agent does in scenario X — step-by-step procedures keyed by trigger condition. The agent loads it and selects a playbook by matching the current situation against playbook triggers.

**When to use**: The content is a set of named playbooks (typically 3-12), each with a trigger, prerequisites, steps, and a success condition. Order within a playbook matters; order of playbooks does not.

**MD spine**: title, scope, provenance (recommended), last_updated, body (one section per playbook).

**JSON required**: `playbooks[]` — array of `{ id, name, trigger, prerequisites[], steps[], success_condition }` entries.

**Example use**: `incident_response_playbooks` consumed by an `on_call_agent` that picks "playbook_database_outage" vs. "playbook_auth_outage" based on the alert that fires.

---

## Cross-Platform Runtime Loading (core)

The same knowledge file pair maps to four different runtime primitives depending on the host platform. The skill writes `_metadata.runtime_strategy` per the thresholds in `runtime_strategy_rules`; the runner uses it to pick the primitive.

| Platform | Embed primitive | Retrieve primitive | Citation surface | Cache primitive |
|---|---|---|---|---|
| **Anthropic** | Inline content blocks; `cache_control: ephemeral` breakpoint on the knowledge block | Files API (`file_id` in `document`/`image` content blocks; `anthropic-beta: files-api-2025-04-14`) | Citations API — `citations.enabled=true` on the document; runner returns `char_location` / `page_location` blocks | `cache_control` on the embedded block (5-min default TTL, 1-hour beta) |
| **OpenAI** | Inline in the system message | Responses API `file_search` tool over a vector store; create vector store + upload files via File API + add to store | `file_search_call` plus `message.annotations[]` with file citations | Implicit per-prefix caching on Responses API |
| **Google** | Inline in `system_instruction` or first user turn | Files API (`files.upload`, 48-hour retention, 2GB/file, 20GB/project) | No first-class citation block — agent must restate sources in output | `cachedContent` (explicit cache; min 1024-4096 tokens by model; TTL default 1h) |
| **xAI** | Inline in system message | `collections_search` tool over uploaded collections; citation URI pattern `collections://[collection_id]/files/[file_id]` | `collections://` URI in `tool_use` output | No first-class explicit cache primitive at this time |

**What the skill writes**: `_metadata.runtime_strategy` is one of `embed` / `read_at_runtime` / `either`. The runner maps it. For files under ~2000 tokens, embed (cheaper to inline than to retrieve). For files over ~8000 tokens, retrieve (avoid burning context). Between 2000 and 8000, either is acceptable — default `embed` if the file would be a cache-friendly prefix on every call, `read_at_runtime` otherwise.

---

## How to Use This Skill (core)

### Prerequisites
- `knowledge/` folder exists at project root (matches the existing `knowledge/behavioral_discipline.*` convention)
- `make_agent_knowledge.json` readable (for templates)
- The consuming agent's spec exists OR is being generated in the same session — so the cross-link can happen

### Basic Usage
Conversational invocation through any agentic tool. Example prompt:

> "Use `make_agent_knowledge` to generate an identity-shape knowledge file `loan_classifier_principles` consumed by `loan_classifier_agent.json`. Scope: lender-specific risk thresholds and escalation triggers. Five principles. Leave the bodies empty for me to fill in."

The skill responds with a proposed MD + JSON draft, waits for confirmation per P-002, then writes both files into `knowledge/`.

### Cross-linking the consuming agent
After the knowledge file pair is written, the user (or a follow-up `make_agent` invocation) adds the path to the consuming agent's `cross_references.knowledge_files[]`:

```json
"cross_references": {
  "related_agents": [],
  "knowledge_files": ["knowledge/loan_classifier_principles.json"],
  "external_dependencies": [],
  "documentation": []
}
```

This skill does NOT perform that edit — that would couple authoring of the knowledge file to ownership of the consuming agent's spec, which violates P-007 (Pull Don't Push).

---

## Common Pitfalls (core)

### 1. Embedding a 50KB Knowledge File in Every System Prompt

**Problem**: A reference-shape file with 400 glossary entries gets `runtime_strategy: embed` and lands in the system prompt of every call, burning ~12K tokens per request before the user message even renders.

**Why it happens**: Default `embed` was set without re-checking token count, or the file grew past the threshold after generation.

**Solution**: `runtime_strategy_rules` in the JSON declares the thresholds. KNW-QC-004 checks consistency between body size and runtime_strategy. When a file crosses ~8000 tokens, switch to `read_at_runtime` and have the runner use the appropriate platform retrieval primitive.

### 2. Citations Without Source Provenance

**Problem**: A reference shape file has 200 entries and an empty `provenance.sources[]`. The consuming agent emits citations like `[ref: loan_glossary#LTV]` but nothing maps back to a real document.

**Why it happens**: Author treated provenance as optional metadata.

**Solution**: KNW-QC-005 fails generation if shape=reference and provenance.sources[] is empty. For identity shape, provenance is optional (the agent IS the source). For procedural, provenance is recommended when the playbook references external policy.

### 3. Knowledge That Should Be source_docs Instead

**Problem**: A "knowledge" file is created to cache the contents of an external API documentation page. The agent never reads it at runtime — it was a research artifact for the skill author.

**Why it happens**: Confusion between "knowledge for me while I author the skill" (source_docs) and "knowledge for the agent at runtime" (knowledge/).

**Solution**: Apply Principle 1 ("Knowledge files are runtime artifacts, not source docs"). If the file is consumed by `cross_references.knowledge_files[]` in a deployed agent, it belongs in `knowledge/`. Otherwise it belongs in `source_docs/`.

### 4. Identity Shape Used for Procedural Content

**Problem**: A file declares `shape: identity` and `principles[]` but the entries are step-by-step procedures ("Step 1: check the database. Step 2: ..."). The consuming agent fails to load it as principles because the structure is procedural.

**Why it happens**: Author thought "principles" loosely as "things the agent follows." But identity = WHO the agent is; procedural = WHAT the agent does in scenario X.

**Solution**: Apply Principle 2 (Pick the shape before filling content). Re-shape the file to `shape: procedural` and rename `principles[]` to `playbooks[]`. KNW-QC-002 + KNW-QC-003 catch the mismatch.

### 5. Orphan Knowledge File (`consumed_by` Empty)

**Problem**: A knowledge file lives in `knowledge/` with `consumed_by: []`. Nothing references it. It rots quietly.

**Why it happens**: Generated speculatively for an agent that was never built, or the consuming agent was renamed without updating `consumed_by`.

**Solution**: KNW-QC-006 fails when `consumed_by[]` is empty. Either delete the file or wire it to the agent that should consume it.

### 6. Shared Knowledge File That Should Have Been Per-Agent

**Problem**: One `domain_terms.md` is shared by 4 agents. Agent C needs a slightly different definition of one term; the author edits the shared file; agents A, B, D silently break.

**Why it happens**: Premature sharing — content looked similar at draft time, diverged later.

**Solution**: Principle 5 (Knowledge is per-agent unless cross-cutting). When in doubt, duplicate. Promote to shared only after multiple agents have proven they consume the file *unchanged* for a meaningful period.

### 7. Source Looks Unreadable Without Trying the Right Tool

**Problem**: A source file in `pre_knowledge/` (or wherever raw materials live) appears empty or chrome-only when read directly. Author flags it as "ingestion not possible" and drafts the knowledge file with a gap. The content was actually available — just behind one extra step.

**Why it happens**: Browser-saved HTML for JS-heavy sites (Substack, Medium, ai.google.dev support pages) APPEARS to be a shell when read as raw text — most of the structural HTML is nav/footer/JS-bundle chrome, and the article body is buried under a single deeply-nested content selector. A naive "open the .html and look for prose" pass misses it. Same for PDFs read with the wrong page range. Same for transcripts pasted into files with unusual encoding.

**Solution**: Before declaring a source ingestible, run `uv run update_agents/fetch_doc.py --from-html <path>` (for HTML sources). The tool strips chrome, applies multi-selector content extraction, and produces clean markdown. If `--from-html` output is **> 5KB and looks like article prose**, the source was readable all along — re-ingest. If `--from-html` output is **< 2KB** AND mostly meta-prose (title, author, "JavaScript required" notices), the source is genuinely JS-rendered with no server-side body — fall back to reader-mode browser save or a manual paste. For PDFs, use the Read tool's `pages` parameter and scan the full document, not just early pages. **Empirical example**: in the 2026-05-13 canvas-toolbox dogfood, a saved Hardman Substack HTML was flagged as "chrome-only" by a generator subagent; running `fetch_doc.py --from-html` on the same file extracted 15KB of clean article body. The tool was right; the eyeball was wrong.

### 8. Reference-Shape Knowledge File Consumed Under Structured Output (Anthropic)

**Problem**: A `reference`-shape knowledge file is loaded into an Anthropic agent that also sets `output_config.format` (or the legacy `response_format`) for structured output. At runtime the API returns 400 — citations and structured outputs are not compatible.

**Why it happens**: The reference shape's whole point is citation traceback (Principle 4). Authors then also want a structured JSON final answer from the consuming agent. Both features look orthogonal; in fact they're mutually exclusive on Anthropic because citations interleave citation blocks with text output and structured outputs require strict JSON conformance — the two modes can't share a response body.

**Solution**: Pick one per agent. If citation traceback is required (reference shape with non-empty `provenance.sources[]`), the consuming agent must NOT declare structured output — it returns prose with citation blocks. If structured output is required, drop `citations.enabled` from the document and have the agent restate sources in the prose fields of the structured response (or split into two calls: one citation pass, one extraction pass). Document the choice in the consuming agent's spec so a future maintainer doesn't reintroduce the incompatibility. KNW-QC-007 enforces this at validation time. See `source_docs/anthropic_citations.md`.

---

## Examples (core)

### Example 1: Reference Shape — Glossary

```markdown
# Loan Underwriting Glossary

> Reference. Lender-specific definitions of risk and underwriting terms used by loan_classifier_agent.

**Scope**: Internal glossary for loan_classifier_agent. Definitions reflect this lender's policies; do not substitute public-internet definitions.

**Provenance**: Lender Risk Policy v4.2 (2026-Q1). See `provenance.sources` in the JSON.

_Last updated: 2026-05-13_

## Terms

(filled in by the author — table or per-term sections)
```

JSON skeleton excerpt:
```json
{ "shape": "reference",
  "scope": "Lender-specific underwriting term definitions",
  "consumed_by": ["loan_classifier_agent.json"],
  "facts": [],
  "provenance": { "sources": ["Lender Risk Policy v4.2 (2026-Q1)"] } }
```

### Example 2: Identity Shape — Agent Principles

The proven exemplar is `knowledge/behavioral_discipline.md/.json` — read that file for the pattern this shape formalizes. An agent-specific identity charter follows the same structure with fewer principles (5-7 instead of 10) and tighter scope (one agent or a closely related set instead of all agents).

JSON skeleton excerpt:
```json
{ "shape": "identity",
  "scope": "Working-style principles specific to loan_classifier_agent",
  "consumed_by": ["loan_classifier_agent.json"],
  "principles": [],
  "provenance": { "sources": [] } }
```

### Example 3: Procedural Shape — Playbooks

```markdown
# On-Call Incident Playbooks

> Procedural. Trigger-keyed response playbooks for on_call_agent.

**Scope**: Incident-response playbooks for production database, auth, and API outages.

_Last updated: 2026-05-13_

## Playbooks

(filled in by the author — one section per playbook)
```

JSON skeleton excerpt:
```json
{ "shape": "procedural",
  "scope": "Incident-response playbooks for on_call_agent",
  "consumed_by": ["on_call_agent.json"],
  "playbooks": [],
  "provenance": { "sources": ["Runbook v2026.04"] } }
```

---

## Validation and Testing (core)

### Quick Validation
1. Both `knowledge/<name>.md` and `knowledge/<name>.json` exist
2. MD contains all sections required by `knowledge_md_required_sections` plus the shape-specific extensions
3. JSON `shape` field is one of `reference` / `identity` / `procedural`
4. Shape-specific required array is present (`facts[]` / `principles[]` / `playbooks[]`)
5. `_metadata.runtime_strategy` is set
6. `consumed_by[]` is non-empty

### Comprehensive Validation
See `make_agent_knowledge.json` → `validation.test_cases` and the `qc_checks` array. The skill's KNW-QC family (KNW-QC-001 through KNW-QC-006) is designed to merge into `make_agent_qc.json` as a downstream step — that merge is NOT done by this skill, it is done in main context by the user.

---

## Resources and References

### Skill Files
- **`make_agent_knowledge.json`**: Required/optional sections per shape, JSON skeleton, runtime_strategy rules, KNW-QC family, validation
- **`make_agent.md` / `make_agent.json`**: Consumer side — how the generated agent references the knowledge file via `cross_references.knowledge_files[]`
- **`knowledge/behavioral_discipline.md` / `.json`**: The proven exemplar of the identity shape — this skill formalizes the pattern that file demonstrates

### Source Docs Referenced
- `source_docs/anthropic_files.md` — Anthropic Files API (beta) primitives
- `source_docs/anthropic_prompt_caching.md` — `cache_control` breakpoints
- `source_docs/anthropic_citations.md` — Citation block surface
- `source_docs/openai_file_search.md` — Responses API `file_search` over vector stores
- `source_docs/google_files.md` — Gemini Files API
- `source_docs/google_caching.md` — `cachedContent` explicit cache
- `source_docs/xai_collections.md` — `collections_search` tool

### Related Skills
- `make_agent` — generates agent specs that consume knowledge files via `cross_references.knowledge_files[]`
- `make_AGENTS` — generates project-level context (different concern; sibling skill pattern)
- `make_orchestrator_agent` — orchestrator specs whose specialists may consume knowledge files
- `make_agent_qc` — validates agent specs; the KNW-QC family in this skill's JSON merges here downstream

### How to Use This Documentation System
1. Start here (.md) for the conceptual frame and the three shapes
2. Use `make_agent_knowledge.json` for the per-shape template structure
3. Reference `knowledge/behavioral_discipline.md` to see the identity shape in production use

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Generate knowledge file pairs (.md + .json) that agents reference at runtime |
| **Input** | shape, knowledge_name, scope, consumed_by[] (interactive) |
| **Output** | `knowledge/<name>.md` + `knowledge/<name>.json` |
| **Skill Type** | workflow (one knowledge file pair per invocation) |
| **Interaction Pattern** | `single_write_workflow` |
| **Complexity** | simple-to-standard |
| **Shapes** | reference / identity / procedural |
| **Key Files** | `make_agent_knowledge.md`, `make_agent_knowledge.json`, generates `knowledge/<name>.{md,json}` |
| **Common Pitfall** | Treating shape as a label after the fact instead of a contract chosen up front |
| **Dependencies** | knowledge/ folder; consuming agent's spec (for cross-link follow-up) |
