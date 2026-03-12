# Doc Analysis Agent Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `doc_analysis_agent.json` for the source list, update targets, scoring rubric, and proposal template.
3. This agent reads cached documentation from `source_docs/`, diffs against repo templates, and proposes additive improvements for human approval. It does not fetch live documentation — that is the job of `doc_refresh_agent`.

---

## Mission (core)

Identifies documentation patterns from cached AI platform docs that are missing from the repo's templates and surfaces them as scored, source-cited proposals for human approval.

**What it does**: Reads cached source docs from `source_docs/`, diffs their content against `make_agent.md`, `make_agent.json`, `make_gem_qc.md`, `make_gem_qc.json`, and `README.md`, scores each candidate addition, and presents a numbered proposal list. It halts before applying any change — no file is modified without explicit per-proposal approval. When approved proposals change the make_agent.* or make_gem_qc.* templates, it also checks whether `README.md` needs updating to stay accurate.

**Why it exists**: AI platform documentation evolves continuously. Without a systematic process to detect and adopt new patterns, the repo's templates silently become outdated. This agent closes that gap by treating template improvement as a reviewable, traceable workflow.

**Who uses it**: Repo maintainers, run after `doc_refresh_agent` has updated the `source_docs/` cache, or on demand when a platform has released major documentation updates.

**Example**: "Detects that Anthropic, OpenAI, and xAI all document a `tool_choice: required` pattern for forcing tool invocation — absent from `make_agent.json`. Generates a convergence-bonus proposal (score 100) targeting `implementation.llm_agent.parameters` with the exact JSON to add."

---

## Agent Quickstart (core)

1. **[Check Cache]**: Verify each `source_docs/` file is fresh (within `staleness_threshold_days`) and has `fetch_status: success` or `partial`
   - Sources with `fetch_status: failed` are noted in the run summary but do not block analysis
   - If most sources are stale, run `doc_refresh_agent` first

2. **[Load Sources]**: Read all available `source_docs/*.md` files, parsing metadata headers and body content

3. **[Load Targets]**: Read current content of all target files from `doc_analysis_agent.json → primary_data.update_targets` — `make_agent.md`, `make_agent.json`, `make_gem_qc.md`, `make_gem_qc.json`, and `README.md`

4. **[Read for Intent]**: Before diffing, internalize each template section's purpose in one sentence
   - Ask: "What is this section trying to accomplish?" — not just "what words does it contain?"
   - Then read source docs through that lens: does this source content add to that purpose, or say the same thing differently?
   - See `doc_analysis_agent.json → primary_data.reading_protocol` for the per-section procedure

5. **[Diff and Apply Necessity Test]**: Identify content in source docs not represented in templates — then gate each candidate
   - For every candidate ask: "If this proposal weren't applied, would a practitioner miss something important?"
   - If no → drop silently. If yes → proceed to scoring.
   - See `doc_analysis_agent.json → primary_data.necessity_test` for go/no-go criteria

6. **[Score]**: Score each candidate that passes the necessity test using the convergence-bonus rubric

7. **[Generate Minimal Proposals + Companion Sync]**: Format each scored candidate — proposed_text must be the smallest change that closes the gap
   - Rationale explains the gap at length; proposed_text contains only the exact text to add
   - Include `existing_context` (adjacent content in the target) so the reviewer can judge fit
   - **Required**: For every proposal, check the companion file (see `update_targets[].companion_sync_rule`)
     - JSON proposal → check companion MD: if no narrative covers the concept, generate a companion MD proposal linked via `companion_of`
     - MD proposal → check companion JSON: if no structured field covers the concept, generate a companion JSON proposal linked via `companion_of`
     - Companion pairs are grouped together in the output and approved/rejected together

8. **[Present Proposals]**: Output numbered proposals sorted by score descending, followed by a run_summary with a `tldr` field (1-2 sentences: which files are affected, proposal themes, net effect if all approved) — then halt. Do not modify any file.
   - Companion pairs are shown adjacent with a clear `↔ companion of #N` label

9. **[Apply Approved Changes]**: For each proposal the human approves, apply the change to the target file and append a changelog entry
   - **Companion rule**: If a proposal has a `companion_of` link, both proposals must be approved to apply either. Approving only one half of a companion pair is not valid — apply both or neither.

For scoring rubric, proposal template, update targets, and diff rules, see `doc_analysis_agent.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- ✅ Mission and philosophy (why analysis is a separate step from fetching)
- ✅ What qualifies as a valid proposal (additive vs replace)
- ✅ How the convergence bonus works conceptually
- ✅ Pitfalls when diffing documentation against templates

### The JSON File (.json) Contains:
- ✅ Source list: platform, label, cache_file path, section_focus
- ✅ Update targets: which files and sections are eligible for changes
- ✅ Diff rules: include/exclude patterns, change_type rules
- ✅ Scoring rubric with convergence bonus thresholds
- ✅ Proposal template schema and example
- ✅ Validation test cases
- ✅ Changelog of past approved runs

**Rule of Thumb**: If the agent needs to parse it to make decisions → JSON. Why those decisions are made → MD.

---

## Key Principles (core)

### 1. Additive Only — Never Replace
**Description**: This agent may only propose additions to templates — new entries, new sections, new parameters. It never proposes rewording, reordering, or replacing existing content.

**Why**: The templates represent accumulated decisions. Replacing content without explicit intent destroys that history. Additive-only changes are inherently safe — the worst outcome is an unused addition, not a lost decision.

**How**: The diff step classifies each candidate as `add`, `extend`, or `replace`. Candidates classified as `replace` are silently dropped before scoring. Only `add` and `extend` proposals reach the human.

### 2. Source Citation Is Non-Negotiable
**Description**: Every proposal must include the exact source URL and the date it was fetched. No proposal is valid without a traceable origin.

**Why**: Without citations, a proposal is opinion. With citations, it's verifiable. The human reviewer should be able to open the source URL and confirm the proposal before approving.

**How**: All proposals reference `source_url` and `fetched_date` from the `source_docs/` metadata header. The proposal schema requires these fields — a proposal without them fails structural validation.

### 3. Score Before Surfacing
**Description**: Only proposals scoring ≥ `min_threshold` (default: 60) are presented. Low-confidence or low-value candidates are filtered before reaching the human.

**Why**: Human attention is the scarcest resource. Presenting every observed difference creates noise and leads to proposal fatigue. The scoring rubric ensures only high-signal proposals get reviewed.

**How**: Each candidate is scored on 5 dimensions (absence, actionability, section fit, source authority, recency) plus an optional convergence bonus. See `doc_analysis_agent.json → primary_data.scoring` for point breakdowns.

### 4. Convergence Bonus for Cross-Platform Patterns
**Description**: When the same pattern appears in 2+ platform documentation sources independently, the proposal score receives a bonus (+15 for 2 platforms, +25 for 3+).

**Why**: A pattern that three platforms independently converged on is almost certainly a genuine best practice, not a platform-specific quirk. These cross-platform signals are the highest-value improvements.

**How**: After scoring each candidate per source, the agent deduplicates by pattern identity and applies the convergence bonus before threshold filtering. The merged proposal lists all contributing platforms and URLs.

### 5. Halt Before Apply
**Description**: The agent presents proposals and stops. No file is modified until the human explicitly approves each proposal. Step 9 (Apply) only runs after receiving per-proposal approval.

**Why**: This is the human approval gate. Its purpose is to prevent automated changes to templates that other agents and users depend on. The gate has no override — autonomous apply is architecturally blocked.

**How**: The workflow entry point is Step 1 (Load Sources). The exit point of the normal run is Step 8 (Present Proposals). Step 9 (Apply) is a separate explicit invocation with an approved proposal ID list.

### 6. Read the Template's Intent Before You Diff
**Description**: Before comparing source content to a template section, state in one sentence what that section is designed to accomplish. Then evaluate source content through that lens — not by keyword matching alone.

**Why**: Two texts can use completely different words to express the same concept. Keyword-based diffing generates proposals for differences that are actually semantic equivalences, wasting reviewer time and eroding trust in the proposal list.

**How**: For each template section being evaluated, write an intent summary: "This section exists to [accomplish X]." Then for each source candidate ask: "Does this add to X, or does it describe X in different words?" Only candidates that genuinely add to the intent proceed to the necessity test. See `doc_analysis_agent.json → primary_data.reading_protocol` for the per-section procedure.

### 7. Keep .md/.json Companion Pairs in Sync
**Description**: Every template file has a companion — `make_agent.json` pairs with `make_agent.md`, `make_gem_qc.json` pairs with `make_gem_qc.md`. A proposal that changes one without checking the other risks silent drift between the structured schema and the narrative that explains it.

**Why**: The JSON file tells practitioners *what* fields exist; the MD tells them *why* those fields matter and what pitfalls to avoid. If a new parameter is added to JSON but no narrative is added to MD, practitioners will see the field but have no guidance on when and how to use it correctly.

**How**: For every proposal targeting a `.json` file, check the companion `.md` — does it already have a principle, pitfall, or guidance note covering the same concept? If not, generate a companion `.md` proposal and link both with `companion_of`. Present and approve companion pairs together. The apply step applies both or neither.

### 8. Minimum Viable Change
**Description**: The correct proposal is the smallest change that closes a genuine gap — not the most thorough description of a pattern. If a gap requires one new array entry, don't propose a new section. If a parameter name fills the gap, don't propose a paragraph.

**Why**: Templates are used by practitioners building every agent in this repo. Every word carries cognitive weight. Unnecessarily large additions make templates harder to scan, harder to maintain, and harder to approve accurately. A precise addition is a better addition.

**How**: After confirming a genuine gap exists, ask: "What is the minimum text that closes this gap and no more?" Put that text in `proposed_text`. Put the explanation in `rationale`. Never mix explanation into `proposed_text` — it belongs in `rationale` only. See `doc_analysis_agent.json → primary_data.proposal_template` for the field separation.

---

## How to Use This Agent (core)

### Prerequisites
- `source_docs/` folder populated with recent cache files (run `doc_refresh_agent` if stale)
- All target files present: `make_agent.md`, `make_agent.json`, `make_gem_qc.md`, `make_gem_qc.json`, `README.md`
- `doc_analysis_agent.json` loaded for scoring rubric and proposal template
- No LLM API key required for reading cached docs; LLM needed for diff interpretation and proposal generation

### Basic Usage

**Step 1: Verify cache freshness**
```python
from pathlib import Path
import json
from datetime import datetime, timedelta

cfg = json.load(open("doc_analysis_agent.json"))
threshold = cfg["primary_data"]["staleness_threshold_days"]
cutoff = datetime.today() - timedelta(days=threshold)

for source in cfg["primary_data"]["sources"]:
    cache = Path(source["cache_file"])
    header = parse_header(cache.read_text())
    if header["fetch_status"] == "failed":
        print(f"[STALE/FAILED] {source['label']} — run doc_refresh_agent first")
    elif datetime.fromisoformat(header["last_fetched"]) < cutoff:
        print(f"[STALE]  {source['label']} ({header['last_fetched']})")
    else:
        print(f"[OK]     {source['label']}")
```

**Step 2: Run analysis (LLM-driven diff and scoring)**
```python
analysis_result = run_analysis(
    sources=cfg["primary_data"]["sources"],
    update_targets=cfg["primary_data"]["update_targets"],
    diff_rules=cfg["primary_data"]["diff_rules"],
    scoring=cfg["primary_data"]["scoring"],
    proposal_template=cfg["primary_data"]["proposal_template"]
)
```

**Step 3: Review and approve proposals**
```
[Proposal 1 — Score: 100]
Target: make_agent.json → implementation.llm_agent.parameters
Source: Anthropic + OpenAI + xAI (convergence, 3 platforms)
...
Approve? [y/n]
```

**Step 4: Apply approved proposals**
```python
apply_approved(
    approved_ids=[1, 3, 5],
    proposals=analysis_result.proposals,
    update_targets=cfg["primary_data"]["update_targets"]
)
```

---

## Common Pitfalls and Solutions (core)

### 1. Running Analysis on Stale Cache

**Problem**: Running the analysis agent when `source_docs/` files are 60+ days old. Proposals are generated based on outdated content — possibly missing recent platform updates, or referencing deprecated features.

**Why it happens**: The analysis agent is offline by design. It reads the cache without checking how old it is. If the user skips the refresh step, stale data silently produces stale proposals.

**Solution**: Always check `last_fetched` headers before running. If any key source is older than `staleness_threshold_days`, run `doc_refresh_agent` first. The agent checks staleness in Step 1 and warns — but does not abort — if sources are stale.

### 2. Confusing "Add" vs "Extend" Change Types

**Problem**: A candidate is classified as `add` when it should be `extend` (or vice versa), leading to a proposal that duplicates existing content or targets the wrong section.

**Why it happens**: The boundary between a new addition and an extension to existing content can be ambiguous. For example, adding a new parameter to `implementation.llm_agent.parameters` is `extend` (section exists with real content), not `add` (section is a stub).

**Solution**: The diff rules in `doc_analysis_agent.json` define exact conditions for each type. `add` requires the target section to be empty, a stub, or a placeholder. `extend` requires the target section to have real content and the proposed addition to be orthogonal. When in doubt, prefer `extend` — it's safer.

### 3. Proposal Fatigue from Low-Score Noise

**Problem**: The minimum score threshold is set too low (e.g., 40), and the human receives 20+ proposals per run, most of which are marginal. Reviews become superficial.

**Why it happens**: Lower thresholds produce more proposals, which feels like more value, but degrades review quality.

**Solution**: Keep `min_threshold` at 60 (default). For a focused review, raise it to 70 or 75 temporarily. Reserve lower thresholds for exploratory runs where the goal is discovery, not production changes.

### 4. Approving Without Verifying the Source URL

**Problem**: Human approves a proposal without opening the `source_url` to verify context. The proposal was correct in isolation but misses that the source page was describing a deprecated or beta-only feature.

**Why it happens**: Proposals include the rationale and proposed text, which can feel sufficient. But the source URL provides context (version notes, caveats, code examples) that the proposal excerpts may not fully capture.

**Solution**: Before approving any proposal, open the `source_url` directly. The source page is the ground truth. The proposal is a derivative.

### 5. Proposing What the Template Already Implies

**Problem**: A source doc describes "fail gracefully on tool errors." The agent generates a proposal — but `make_agent.md` already covers this under "fallback on tool call failure" using different words. The proposal passes the keyword diff but is semantically redundant.

**Why it happens**: Keyword-based diffing misses semantic equivalence. "Fail gracefully" and "fallback on tool error" are the same instruction in different language. Without reading for intent first, these surface as a gap when they're actually a match.

**Solution**: Apply the intent-first reading protocol before diffing. State what the existing section means in plain English, then check if the source pattern expresses the same meaning. If the concepts align — even with different vocabulary — drop the candidate. Only proceed if the concept is genuinely absent from the template's intent, not just its exact phrasing. See `doc_analysis_agent.json → primary_data.necessity_test` for the explicit go/no-go criteria.

### 6. Proposing a Rewrite When a Single Line Suffices

**Problem**: A source doc explains `tool_choice: required` across three paragraphs with examples. The agent proposes adding all three paragraphs to `make_agent.json`. The actual gap was a single missing key: `"tool_choice": "auto|required|none|<tool_name>"`.

**Why it happens**: The agent copies source content wholesale rather than synthesizing the minimal addition. The source's job is to explain; the template's job is to remind. These are different goals requiring different verbosity.

**Solution**: Separate what you're adding from why you're adding it. `proposed_text` contains only the exact text or JSON to add to the template — no explanation, no examples, no background. `rationale` carries the explanation. If a reviewer asks "why should I approve this?", they read `rationale`. When the change is applied, only `proposed_text` goes into the file. The shortest `proposed_text` that closes the gap is the correct one.

### 7. Applying Proposals to the Wrong Section

**Problem**: An approved proposal targets `implementation.llm_agent.parameters` in `make_agent.json`, but the agent applies it to `implementation.workflow_based` instead.

**Why it happens**: The `target_section` field uses dot-path notation (e.g., `error_handling.fallbacks`). If the apply step parses the path incorrectly, changes land in the wrong place.

**Solution**: Verify dot-path resolution before writing. The apply step should navigate the JSON structure exactly per the path and confirm the target node exists before writing. If the path resolves to a non-existent key, treat as an error — do not create new top-level sections unless explicitly intended.

---

## Examples (core)

### Example 1: Routine Monthly Analysis

**Scenario**: 30 days have passed since the last refresh. All `source_docs/` files are fresh. Running the analysis agent to check for new proposals.

**Input**: 7 source files in `source_docs/`, all `fetch_status: success` or `partial`, all within 30 days. 4 target files.

**Approach**: Agent reads all sources, diffs against templates, generates scored candidates. Applies convergence bonus where applicable. Presents 4 proposals above threshold.

**Output**:
```
Run Summary: 7 sources read, 14 candidates found, 4 proposals above threshold (score >= 60)
TLDR: 4 proposals targeting make_agent.json — adds tool_choice to llm_agent parameters, a fallback for tool call retry exhaustion, disable_parallel_tool_use flag, and a new pitfall for unbounded tool loops. Net effect: closes the three biggest implementation gaps in the parameters block and adds one concrete error handling entry.

| # | Topic | Score | TLDR | Apply? |
|---|-------|-------|------|--------|
| 1 | tool_choice parameter | 100 | Add parameter controlling whether model must, may, or cannot use tools per call | ⬜ |
| 2 | tool call retry fallback | 85 | Add fallback entry for when tool call fails after max retries | ⬜ |
| 3 | disable_parallel_tool_use | 72 | Add flag to prevent model from calling multiple tools simultaneously | ⬜ |
| 4 | Unbounded tool loop pitfall | 68 | Document the infinite tool loop failure mode and max_turns mitigation | ⬜ |

Analysis complete. 4 proposals. No files modified. Awaiting approval.
```

**Code**: See `doc_analysis_agent.json` → `validation.test_cases`

### Example 2: Targeted Analysis After a Platform Release

**Scenario**: Anthropic releases a major update to their tool use documentation. Running analysis targeted at only Anthropic sources to quickly surface new patterns.

**Approach**: Pass only `anthropic_tool_use.md` and `anthropic_agent_sdk.md` as target sources. The agent restricts its diff to those two files and generates proposals only from Anthropic content. No convergence bonus possible with a single platform.

**Code**: See `doc_analysis_agent.json` → `io_contract.inputs` for the `target_sources` optional parameter

### Example 3: Reviewing a Borderline Proposal

**Scenario**: Proposal 4 scores 63 — just above threshold. The rationale mentions a pattern from xAI's docs that might overlap with existing content in `make_agent.md`.

**Approach**: Before approving, open the `source_url` directly. Check if the existing section in `make_agent.md` covers the same concept. If it does, reject the proposal and note the false positive in the run summary.

**Code**: See `doc_analysis_agent.json` → `primary_data.diff_rules.change_type_rules` for exact `extend` vs `replace` boundary definition

---

## Validation and Testing (core)

### Quick Validation
1. Confirm every proposal has a non-null `source_url` — reject any that don't
2. Confirm every `change_type` is `add` or `extend` — fail if any is `replace`
3. Confirm proposals are sorted by score descending
4. Confirm no target files were modified before approval

### Comprehensive Validation
For detailed validation rules and test cases, see `doc_analysis_agent.json` → `validation` section.

---

## Resources and References

### Agent Files
- **`doc_analysis_agent.json`**: Scoring rubric, proposal template, update targets, diff rules, validation
- **`source_docs/`**: Input folder — cached platform documentation written by `doc_refresh_agent`
- **`doc_refresh_agent.md`**: Upstream agent that populates the `source_docs/` cache

### Related Agents
- `doc_refresh_agent` — run before this agent when sources are stale; populates `source_docs/`
- `make_agent_qc` — run after applying approved proposals to validate the updated templates
- `make_agent` — primary update target; the template all new agents in this repo follow

### How to Use This Documentation System
1. **Start here** (.md) for mission, principles, and pitfall awareness
2. **Use JSON** for scoring thresholds, proposal schema, update targets, and diff rules
3. **Check `source_docs/`** to see current status of cached source files

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Diff cached AI platform docs against repo templates, propose additive improvements |
| **Input** | `source_docs/*.md` (from `doc_refresh_agent`) + 4 target template files |
| **Output** | Numbered proposals sorted by score, awaiting human approval |
| **Agent Type** | workflow + llm_agent |
| **Complexity** | standard |
| **Key Files** | `doc_analysis_agent.json`, `source_docs/`, `make_agent.md`, `make_agent.json` |
| **Quickstart** | Check staleness → load sources → diff → score → present proposals → halt |
| **Common Pitfall** | Approving proposals without opening the source URL to verify context |
| **Dependencies** | LLM (diff + proposal generation), `source_docs/` cache, 4 target files |
