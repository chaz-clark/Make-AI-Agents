# Merge Agent Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `merge_agent.json` for structured data, the merge procedure, the suspect-overwrite rule, and validation.
3. This agent does ONE thing per invocation: merge a single staged file from `source_docs/dropbox/` into its target `source_docs/<short_name>.md`, update `source_docs/_refresh_log.json`, and delete the dropbox file. It is `single_write_workflow` shaped — propose plan, wait for confirmation, then perform the merge as one atomic operation per file.

---

## Mission (core)

**What it does**: Promotes a manually-staged document from `source_docs/dropbox/<short_name>.md` into the canonical cache at `source_docs/<short_name>.md`, preserving the YAML front matter, updating `last_fetched` / `fetch_status` / `size_bytes`, mirroring the change into `source_docs/_refresh_log.json`, and removing the dropbox file once merge is verified.

**Why it exists**: `doc_refresh_agent` cannot fetch every doc — some platforms 403, summarize at the small-model layer, or are JS-rendered. Those gaps land in `source_docs/dropbox/` after a manual fetch. Promoting them by hand is repetitive, error-prone, and routinely loses the YAML front matter or fails to update `_refresh_log.json`. This agent encapsulates the promote step as one named operation.

**Who uses it**: Whoever just manually staged a doc into `source_docs/dropbox/`. Invoked directly, or by `doc_refresh_workflow` as the merge step after refresh.

**Example**: "Merge `source_docs/dropbox/openai_handoffs.md` into `source_docs/openai_handoffs.md`, preserving the existing front matter and bumping `last_fetched` to today."

---

## Agent Quickstart (core)

0. **interaction_pattern**: `single_write_workflow` — exactly one promote operation per invocation, with confirmation before the irreversible delete. Behavioral discipline is embedded below.

1. **[Identify]**: Resolve the dropbox file path and the target source_docs path. Either both supplied explicitly, or supplied as `short_name` and discovered via the filename mapping (target = `source_docs/<short_name>.md`, dropbox = `source_docs/dropbox/<short_name>.md`).

2. **[Read both files]**: P-001 requires reading actual content first. Parse:
   - Dropbox file → new body (with or without its own front matter)
   - Target file → existing front matter + existing body, existing size
   - `_refresh_log.json` → existing entry under `sources[<short_name>]` if any

3. **[Suspect-overwrite check]**: If existing target body is non-placeholder (size_bytes > 1000) and incoming dropbox body is less than 80% of existing body length, halt per P-003. Stage the dropbox file as `source_docs/<short_name>.md.new` and surface the regression. Threshold mirrors `doc_refresh_agent.json → fetch_config.suspect_overwrite_threshold` (0.20 / inverted to 0.80 retention floor) — see `merge_agent.json → suspect_overwrite_rule` for the exact arithmetic.

4. **[Propose plan]**: Before writing, emit the plan:
   - Target: `source_docs/<short_name>.md`
   - New body size (bytes), front-matter delta (`last_fetched: <today>`, `fetch_status: success`, optional `notes` append)
   - `_refresh_log.json` update: `last_attempted`, `action` (`updated` if existing | `added` if new), `size_before`, `size_after`, `fetch_status`, `notes` append
   - Delete: `source_docs/dropbox/<short_name>.md`
   Wait for user confirmation.

5. **[Apply]**: On confirmation, in order:
   1. Write target with preserved+updated front matter and new body
   2. Update `_refresh_log.json` (read, modify in-memory, write back — preserve key order via JSON parse/serialize)
   3. Delete the dropbox file

6. **[Verify]**: Re-read the target file's front matter; confirm `last_fetched` is today and `size_bytes` matches the on-disk size. Confirm `_refresh_log.json` parses as valid JSON. Confirm the dropbox file no longer exists.

7. **[Output]**: A3-style change report (per P-006): current → target → countermeasure → verification, plus a one-line summary suitable for downstream consumers.

For detailed procedure, see `merge_agent.json → primary_data.merge_procedure`.

---

## File Organization: JSON vs MD (core)

- **MD (this file)** — narrative: mission, why-this-exists, the suspect-overwrite rationale, pitfalls.
- **JSON (`merge_agent.json`)** — the merge procedure as numbered steps, the suspect-overwrite rule arithmetic, the `_refresh_log.json` schema this agent writes, validation checklists.

---

## Key Principles (core)

### 1. Atomic Per-File Merge
**Description**: One invocation = one file promoted. No batching, no fan-out.
**Why**: A bulk promote loses the per-file confirmation gate (P-002) and the per-file suspect-overwrite check (P-003). Each file has a different size baseline, different front matter, different `_refresh_log` entry — coupling them hides regressions.
**How**: `io_contract.inputs` is one file path (or one `short_name`). Loop invocation if multiple files need promotion.

### 2. Front Matter Is Source-Of-Truth, Not Disposable Metadata
**Description**: The YAML front matter at the top of `source_docs/<short_name>.md` carries `platform`, `label`, `source_url`, `last_fetched`, `fetch_status`, `notes`. Promotion preserves all of these and updates only the time-varying fields.
**Why**: `doc_refresh_agent`, `doc_analysis_agent`, and any downstream consumer parse the front matter. A merge that overwrites the file body without re-emitting the front matter silently breaks every consumer.
**How**: Read the existing front matter into a parsed dict. Update `last_fetched` to today, `fetch_status` to `success` (or as supplied), optionally append to `notes`. Re-emit front matter using the same field order as found. If the dropbox file already has front matter, the EXISTING file's front matter wins on `platform` / `label` / `source_url` / `notes` (the dropbox front matter is typically minimal); only `last_fetched`, `fetch_status`, `size_bytes` come from the new content.

### 3. Refresh-Log and Cache File Move Together
**Description**: A promote that updates only `source_docs/<short_name>.md` and skips `_refresh_log.json` produces drift — the log says "last refreshed 2026-04-30, size 0" while the file says "last_fetched 2026-05-13, size 19563 bytes".
**Why**: `doc_refresh_agent` reads `_refresh_log.json` to decide what's stale. A drifted log re-fetches files that were just manually promoted.
**How**: Both writes are part of the same merge transaction. If `_refresh_log.json` write fails, halt and surface — do not leave the cache file ahead of the log.

### 4. Delete Only After Verify
**Description**: The dropbox file is the manual-fetch artifact. Deleting it before verifying the target write is correct loses the source.
**Why**: If the target write produced corrupt front matter or truncated content, the dropbox file is the only recovery path until the user manually re-fetches.
**How**: Sequence is: write target → write log → re-read target and confirm size + front matter parse → only then delete dropbox file. On any verify failure, halt and leave dropbox file in place per P-003.

---

## Behavioral Discipline (core)

This agent follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The principles applicable to this agent type (single_write_workflow):

- **P-001 Read Before Claiming** (*Genchi Genbutsu*): Read the actual source before claiming anything about content, code, or system state. Training-data priors are not a substitute for reading what's in front of you. *Trigger*: Every claim about content, code, data, or system state.
- **P-002 Plan Before Acting** (*Nemawashi + TBP*): For any state-changing task with more than one step, propose the plan and wait for user confirmation before non-reversible action. The plan is a draft — refine through back-and-forth before committing. *Trigger*: Any task with more than one step that changes state.
- **P-003 Stop on Defect** (*Jidoka + Andon*): First failed test, first failed precondition, first ambiguity that can't be resolved → stop. Don't paper over. Don't retry blindly. Surface the issue: "I cannot proceed because X." *Trigger*: Any failure, any unresolved ambiguity, any precondition the agent can't verify.
- **P-004 Find the Root Cause** (*5 Whys*): When something doesn't work as expected, walk the chain of causation. Stop when the answer is structural — that's where the fix lives. *Trigger*: Any bug, any unexpected output, any "this should work but doesn't."
- **P-006 Document the Change** (*A3*): For any non-trivial change, structure the report so a non-technical reviewer can audit it without reading the diff. Use the A3 template. *Trigger*: Any change to more than one file or page; any change with non-obvious downstream effects; any change a reviewer would want to inspect.
- **P-007 Pull, Don't Push** (*JIT + 3 Ms*): Generate exactly what was asked. No speculative features. The discipline isn't laziness — it leaves room for the user to decide what comes next. *Trigger*: Every change. Default is minimum scope.
- **P-008 Mistake-Proof Outputs** (*Poka-yoke + Standard Work*): Format outputs consistently across runs so the user can predict what they'll see. *Trigger*: Any output a downstream consumer (human or system) parses or compares across invocations.
- **P-009 Reflect, and Tell the User** (*Hansei + Yokoten*): At the end of any task that produced a surprise, took longer than expected, or revealed non-obvious behavior, name the lesson in the response ("Worth noting: ...") AND append it to the agent's spec MD External System Lessons section. *Trigger*: End of any task with surprise, unexpected duration, or non-obvious external system behavior.
- **P-010 Respect the User's Intent** (*Respect for People + Hoshin Kanri*): Two failure modes: (a) anti-substitution — don't override or reinterpret the user's stated goal silently; (b) anti-drift — in long sessions, every action should still trace to the original goal; surface drift when it happens. *Trigger*: Any action beyond the literal request (anti-substitution); any long-running session every ~5 turns (anti-drift).

**Hard rule on overrides**: before skipping any principle, the agent must state in one sentence which principle is being skipped and why. Principles P-001, P-003, P-007, P-010 have no override.

For full principle definitions, examples, and override rationale, see `knowledge/behavioral_discipline.md`.

---

## File I/O Mode (core)

`io_contract.inputs[0].type: "string"` — the agent is invoked conversationally with either a dropbox file path or a short_name. The merge is performed against the filesystem; no folder/file scanning loop. Paths are supplied at run time, never hardcoded.

---

## How to Use This Agent (core)

### Prerequisites
- `source_docs/` and `source_docs/dropbox/` both exist
- `source_docs/_refresh_log.json` exists and parses
- The dropbox file to promote exists and is non-empty
- The target `source_docs/<short_name>.md` either exists (action = `updated`) or does not (action = `added`)

### Existing Tooling
| Tool / File | Purpose | When to use |
|---|---|---|
| `source_docs/_refresh_log.json` | Authoritative log of every refresh attempt per source | READ existing entry to merge `notes`; WRITE updated entry on merge |
| `update_agents/doc_refresh_agent.json` → `fetch_config.suspect_overwrite_threshold` | Threshold value (0.20 → 80% retention floor) | Mirrored here in `suspect_overwrite_rule`; if the doc_refresh threshold changes, mirror the change here |
| `update_agents/doc_refresh_agent.json` → `fetch_config.metadata_header_format` | Front-matter shape | Use the same shape when re-emitting; do not invent fields |

**Reuse-first rule**: If a script in `update_agents/` (e.g. `fetch_doc.py`) already handles the front-matter parsing or the suspect-overwrite math, call it rather than re-implementing.

### Basic Usage

**Step 1: Invoke conversationally**
> "Use merge_agent to promote `source_docs/dropbox/openai_handoffs.md` into `source_docs/openai_handoffs.md`."

or

> "Use merge_agent to promote `xai_collections` from dropbox."

**Step 2: Review the proposed plan**
Agent presents:
- New front matter (with `last_fetched: <today>`)
- `_refresh_log.json` delta
- Dropbox deletion

**Step 3: Confirm**
Approve to apply. Agent writes target, updates log, deletes dropbox file.

**Step 4: Verify**
Agent re-reads, reports A3 change report.

---

## Common Pitfalls and Solutions (core)

### 1. Dropping the Front Matter

**Problem**: The merged file has no `---` block at the top; downstream consumers fail to parse `last_fetched`.

**Why it happens**: The dropbox file rarely has a front matter (it's a raw fetch). Naive merge writes the dropbox content as-is into the target.

**Solution**: ALWAYS read existing target front matter first. If target does not exist (`action: added`), build a fresh front matter from `platform`/`label`/`source_url` either supplied as inputs or pulled from `doc_refresh_agent.json → primary_data.sources[<short_name>]`. Never emit a target file without a front matter.

### 2. Silent Content Regression

**Problem**: The dropbox file is 200 bytes (an error page captured by mistake), the target had 19KB of real content, and the merge replaces the good content with the error page.

**Why it happens**: Manual fetches sometimes capture login redirects, anti-bot pages, or empty responses without the human noticing.

**Solution**: The suspect-overwrite check fires when new body < 80% of existing body. Halt per P-003; stage the new content as `.new`; surface the regression. Mirrors the same defense `doc_refresh_agent` uses for automated fetches.

### 3. Forgetting `_refresh_log.json`

**Problem**: Target file is updated, but `_refresh_log.json` still says `last_attempted: 2026-04-30, size_after: 0`. Next run of `doc_refresh_agent` re-fetches a file that was just manually fixed.

**Why it happens**: Two-file write is easy to skip; the log file is invisible compared to the source_docs file.

**Solution**: The merge transaction is BOTH writes. The agent halts if the log write fails. The verify step confirms log parses cleanly post-write.

### 4. Treating Multiple Dropbox Files as One Merge

**Problem**: User says "promote everything in dropbox/"; agent batches the writes and a single suspect-overwrite halts the whole batch with unclear partial state.

**Why it happens**: Single-write-workflow agents are easy to mistake for batch agents when the user wants "do all the ready ones."

**Solution**: This agent does ONE merge per invocation. For multiple, the caller loops (or `doc_refresh_workflow` orchestrates). P-007 / P-010: don't substitute "loop over all dropbox files" for the user's literal "promote this file."

---

## External System Lessons (optional)

### source_docs front-matter — `size_bytes` is content-length, not file-length

**Behavior**: The `size_bytes` in some legacy front matters refers to the body byte count after `---`, not the full file size including the front matter block. Other front matters omit `size_bytes` entirely.

**Why it matters**: A merge that writes `size_bytes: <full file len>` produces a number that disagrees with `_refresh_log.json → sources[<short_name>].size_after` (which is body-only).

**How to handle it**: Compute `size_bytes` as the byte length of the body after the closing `---\n` newline. Use the same convention for `_refresh_log.json → size_after`. If the existing front matter omits `size_bytes`, do not introduce the field.

---

## Examples (core)

### Example 1: Promote a previously-summarized doc

**Scenario**: `openai_handoffs.md` was placeholder-sized (3KB summary). User manually fetched the full doc (13KB) into `source_docs/dropbox/openai_handoffs.md`.

**Input**: `merge_agent` invoked with `short_name=openai_handoffs`.

**Approach**:
1. Read `source_docs/openai_handoffs.md` (front matter + placeholder body, ~3KB)
2. Read `source_docs/dropbox/openai_handoffs.md` (raw fetch, ~13KB)
3. Suspect-overwrite check: 13KB > 0.8 × 3KB → PASS (growing, not shrinking)
4. Propose plan: front matter `last_fetched: 2026-05-13`, body replaced with dropbox content, `_refresh_log.json[openai_handoffs].size_after: 13000` (approx)
5. Confirm → apply → delete dropbox file
6. Verify → A3 report

### Example 2: Suspect-overwrite halts merge

**Scenario**: User accidentally saved an anti-bot login HTML page as `source_docs/dropbox/anthropic_files.md` (1KB) over an existing 12KB cached doc.

**Approach**: Suspect-overwrite check: 1KB < 0.8 × 12KB → HALT per P-003. Stage as `source_docs/anthropic_files.md.new`. Surface: "Cannot proceed — incoming content is 8% of existing. Either confirm the regression is intentional or replace the dropbox file with a complete fetch." Dropbox file is preserved unchanged.

### Example 3: New source (no existing target)

**Scenario**: User adds a brand-new doc (`anthropic_workspaces.md`) to dropbox for the first time.

**Approach**: Target does not exist → `action: added`. No suspect-overwrite check. Front matter must be supplied as inputs (platform/label/source_url) or pulled from `doc_refresh_agent.json` if a source entry was added there. `_refresh_log.json[anthropic_workspaces]` is created fresh with `size_before: 0`.

---

## Validation and Testing (core)

### Quick Validation
1. Re-read target front matter; `last_fetched` matches today
2. `_refresh_log.json` parses as valid JSON
3. Dropbox file is gone (only on successful merge)
4. Body size on disk matches `size_after` in log

### Comprehensive Validation
See `merge_agent.json` → `validation`.

---

## Resources and References

### Agent Files
- `merge_agent.json` — structured procedure, suspect-overwrite rule, validation

### Related Agents
- `update_agents/doc_refresh_agent.{md,json}` — produces stale-detection signals that motivate manual fetches into dropbox
- `update_agents/doc_analysis_agent.{md,json}` — consumes the merged `source_docs/` content for proposal generation
- `update_agents/doc_refresh_workflow.{md,json}` — orchestrator that calls this agent as the merge step

### Knowledge Files
- `knowledge/source_docs_index.{md,json}` — lookup table of the 34 cached docs (also produced in this dogfood pass)

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Promote one dropbox file into source_docs with full front-matter + refresh-log update |
| **Input** | Dropbox file path OR short_name (string) |
| **Output** | Updated `source_docs/<short_name>.md` + updated `_refresh_log.json` + deleted dropbox file + A3 report |
| **Agent Type** (implementation) | workflow |
| **Interaction Pattern** (behavior) | single_write_workflow |
| **Complexity** | simple |
| **Key Files** | `merge_agent.md`, `merge_agent.json` |
| **Quickstart** | Conversational invocation: "Use merge_agent to promote <short_name>" |
| **Common Pitfall** | #1 Dropping the front matter |
| **Dependencies** | `source_docs/`, `source_docs/dropbox/`, `source_docs/_refresh_log.json` |
