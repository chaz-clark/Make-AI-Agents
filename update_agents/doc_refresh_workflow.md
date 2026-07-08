---
name: doc_refresh_workflow
version: "1.0"
last_updated: 2026-05-13
description: Orchestrator coordinating doc_refresh_agent + merge_agent + doc_analysis_agent for the refresh → promote → analyze cycle over source_docs/.
generated_by: make_orchestrator_agent v1.0 (dogfood pass 2026-05-13)
agent_type:
  type: multi_agent
  description: Orchestrator that delegates to 3 specialists via delegate_to_<name> tools
behavioral_discipline:
  interaction_pattern: multi_step_batch
  applicable_principles: [P-001, P-002, P-003, P-004, P-005, P-006, P-007, P-008, P-009, P-010]
  override_decisions: []
io_contract:
  inputs:
    - name: user_request
      type: string
      format: Conversational user request - refresh and/or analyze instruction, optionally with platform/short_name filter
      required: true
  outputs:
    - name: synthesized_response
      type: string
      format: Free-text synthesis combining refresh summary, merge summary, and proposal list (if analysis phase ran)
  side_effects: Indirect via specialists - doc_refresh_agent writes source_docs/ + dropbox/, merge_agent promotes files, doc_analysis_agent reads + proposes
  non_interactive_mode: false
topology:
  specialists:
    - name: doc_refresh_agent
      spec_path: update_agents/doc_refresh_agent.json
      purpose: Detect stale sources, fetch URLs, write to source_docs/ or dropbox/
      input_contract: {task: string}
      expected_output: Refresh summary with refreshed/dropbox-staged/failed short_names
    - name: merge_agent
      spec_path: update_agents/merge_agent.json
      purpose: Promote ONE staged file from dropbox/ with front-matter preservation
      input_contract: {task: string}
      expected_output: A3 change report per merge, suspect-overwrite halts surfaced explicitly
    - name: doc_analysis_agent
      spec_path: update_agents/doc_analysis_agent.json
      purpose: Diff source_docs/ against templates, emit numbered proposals
      input_contract: {task: string}
      expected_output: Numbered proposal list with citations + run_summary
  routing_strategy: llm_routed
  termination_criteria: All stale sources refreshed AND merged, OR doc_analysis_agent returned proposals, OR user requested only one phase and it completed
implementation:
  llm_agent:
    max_turns: 30
    parameters:
      temperature: 0.2
      max_tokens: 4096
      disable_parallel_tool_use: true
      memory: manual_history
    tools_count: 3
cross_references:
  related_agents:
    - update_agents/doc_refresh_agent.json
    - update_agents/merge_agent.json
    - update_agents/doc_analysis_agent.json
  knowledge_files:
    - path: knowledge/source_docs_index.json
      purpose: Lookup table of 34 cached platform docs
      runtime_strategy: read_at_runtime
validation:
  success_criteria:
    - ORCH-QC-001 through ORCH-QC-005 pass
    - BD-QC-001 through BD-QC-007 pass (BD-QC-007 N/A - non_interactive_mode is false)
    - User receives single synthesized response
  test_cases_count: 4
metadata:
  companion_json_deprecated: "2026-07-08 - consolidated into YAML frontmatter per JSON purge"
  specialists_count: 3
  template_version: "1.0"
---

# Doc Refresh Workflow

An orchestrator that coordinates `doc_refresh_agent`, `merge_agent`, and `doc_analysis_agent` to keep `source_docs/` fresh and turn that freshness into actionable proposals against the project's templates.

---

## Mission

**What it does**: Runs the end-to-end doc-maintenance loop:
1. Check staleness + fetch the stale sources → `doc_refresh_agent`
2. Promote any manually-staged files from `source_docs/dropbox/` into `source_docs/` → `merge_agent`
3. Diff refreshed sources against templates and propose additive improvements → `doc_analysis_agent`

**Why it exists**: The three specialists are already wired individually, but they're routinely chained by hand: refresh → review what's in dropbox → promote → analyze. The hand-chaining loses context between steps (which sources were just refreshed? which dropbox files were promoted? which proposals correspond to which platforms?) and forces the user to remember the canonical order. This orchestrator carries the chain context across delegations and surfaces a single synthesis.

**Who uses it**: Whoever wants to run a refresh-then-analyze cycle in one invocation, or wants the orchestrator to handle the routing decisions (e.g., user says "refresh just Anthropic" — the orchestrator routes to `doc_refresh_agent` with a filter and stops, no analysis phase). Interactive use; not a scheduled job (no `non_interactive_mode`).

---

## Topology

This orchestrator coordinates 3 specialists:

- **`doc_refresh_agent`** (`update_agents/doc_refresh_agent.json`, `interaction_pattern: multi_step_batch`)
  Purpose: Detect stale sources by `last_fetched` vs. `staleness_threshold_days`, fetch the URLs, write to `source_docs/dropbox/` (or directly to `source_docs/` when fetch is clean). Invoked via `delegate_to_doc_refresh_agent`.

- **`merge_agent`** (`update_agents/merge_agent.json`, `interaction_pattern: single_write_workflow`)
  Purpose: Promote one staged file at a time from `source_docs/dropbox/` to `source_docs/<short_name>.md` with front-matter preservation, `_refresh_log.json` update, and dropbox cleanup. Invoked via `delegate_to_merge_agent`. The orchestrator calls this once per dropbox file that `doc_refresh_agent` staged.

- **`doc_analysis_agent`** (`update_agents/doc_analysis_agent.json`, `interaction_pattern: multi_step_batch`)
  Purpose: Read the current `source_docs/`, diff against templates (`make_agent.md`/`.json`, `make_orchestrator_agent.*`, `make_agent_knowledge.*`, etc.), score candidates via the necessity test + 5-criterion rubric, and emit a numbered proposal list. Invoked via `delegate_to_doc_analysis_agent`.

Each specialist is referenced by `spec_path` in `doc_refresh_workflow.json → topology.specialists[]`. Specialists are stateless w.r.t. each other; cross-specialist state lives only in this orchestrator's context.

---

## Routing Decisions

When to delegate to which specialist is encoded in each tool's `description`, not in this prompt prose. Read `doc_refresh_workflow.json → implementation.llm_agent.tools[]` for the per-tool routing guidance. Summary of the design:

- `delegate_to_doc_refresh_agent` — used when the user's request implicates checking staleness or fetching docs (refresh, update, fetch, "what's stale"). Returns: list of refreshed cache_files + list of files staged in `source_docs/dropbox/` + the run summary.
- `delegate_to_merge_agent` — used once PER dropbox file after refresh, to promote it into `source_docs/`. Each call is a separate delegation (single_write_workflow per file). Carries `short_name` in the task argument.
- `delegate_to_doc_analysis_agent` — used when the user's request implicates diffing sources against templates or generating proposals (analyze, propose, "what should I update"). Reads the refreshed `source_docs/` state and emits proposals.

When multiple specialists could plausibly handle a step, the model picks based on tool descriptions. Tool descriptions name the OTHER specialists they compete with and explain when to prefer each.

---

## Cross-Agent State

Orchestrator carries: `user_request` + `refreshed_short_names_list` (returned by doc_refresh_agent) + `promoted_short_names_list` (accumulated across merge_agent calls).
Each specialist sees: only the `task` argument passed in its `delegate_to_*` call.

If the user originally asked "refresh + analyze Anthropic docs only", the orchestrator MUST pass the platform filter explicitly to BOTH `doc_refresh_agent` (so it only fetches Anthropic sources) AND `doc_analysis_agent` (so the proposal scope matches). Don't assume a filter passed to specialist A will reach specialist B — orchestrators carry the state, specialists don't.

If `doc_refresh_agent` returns dropbox files, the orchestrator calls `delegate_to_merge_agent` once per file, passing the short_name explicitly. Each merge is independent — a suspect-overwrite halt in one does NOT halt the others; the orchestrator continues with the remaining files and reports the halted file in its synthesis.

---

## Termination

The orchestrator stops delegating when: **All stale sources refreshed AND merged into source_docs/, OR doc_analysis_agent has returned a synthesized proposal list, OR the user explicitly requested only one phase and that phase completed.**

A backstop `max_turns: 30` catches the case where the criteria are never satisfied (e.g., a specialist keeps returning ambiguous results that prompt another delegation). 30 leaves headroom for: 1 refresh call + up to ~10 merge_agent calls (one per dropbox file) + 1 analysis call + buffer turns for clarification.

---

## Behavioral Discipline (core)

This agent follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The principles applicable to this agent type (multi_step_batch) — the full discipline applies:

- **P-001 Read Before Claiming** (*Genchi Genbutsu*): Read the actual source before claiming anything about content, code, or system state. Training-data priors are not a substitute for reading what's in front of you. *Trigger*: Every claim about content, code, data, or system state.
- **P-002 Plan Before Acting** (*Nemawashi + TBP*): For any state-changing task with more than one step, propose the plan and wait for user confirmation before non-reversible action. The plan is a draft — refine through back-and-forth before committing. *Trigger*: Any task with more than one step that changes state.
- **P-003 Stop on Defect** (*Jidoka + Andon*): First failed test, first failed precondition, first ambiguity that can't be resolved → stop. Don't paper over. Don't retry blindly. Surface the issue: "I cannot proceed because X." *Trigger*: Any failure, any unresolved ambiguity, any precondition the agent can't verify.
- **P-004 Find the Root Cause** (*5 Whys*): When something doesn't work as expected, walk the chain of causation. Stop when the answer is structural — that's where the fix lives. *Trigger*: Any bug, any unexpected output, any "this should work but doesn't."
- **P-005 Small Steps, Evenly Sized** (*Kaizen + PDCA + Heijunka*): Break work into small verifiable units of roughly equal size. Verify each before starting the next. Reversibility is a feature. *Trigger*: Multi-step tasks. Anything where rolling back to a known-good state would help if something breaks.
- **P-006 Document the Change** (*A3*): For any non-trivial change, structure the report so a non-technical reviewer can audit it without reading the diff. Use the A3 template. *Trigger*: Any change to more than one file or page; any change with non-obvious downstream effects; any change a reviewer would want to inspect.
- **P-007 Pull, Don't Push** (*JIT + 3 Ms*): Generate exactly what was asked. No speculative features. The discipline isn't laziness — it leaves room for the user to decide what comes next. *Trigger*: Every change. Default is minimum scope.
- **P-008 Mistake-Proof Outputs** (*Poka-yoke + Standard Work*): Format outputs consistently across runs so the user can predict what they'll see. *Trigger*: Any output a downstream consumer (human or system) parses or compares across invocations.
- **P-009 Reflect, and Tell the User** (*Hansei + Yokoten*): At the end of any task that produced a surprise, took longer than expected, or revealed non-obvious behavior, name the lesson in the response ("Worth noting: ...") AND append it to the agent's spec MD External System Lessons section. *Trigger*: End of any task with surprise, unexpected duration, or non-obvious external system behavior.
- **P-010 Respect the User's Intent** (*Respect for People + Hoshin Kanri*): Two failure modes: (a) anti-substitution — don't override or reinterpret the user's stated goal silently; (b) anti-drift — in long sessions, every action should still trace to the original goal; surface drift when it happens. *Trigger*: Any action beyond the literal request (anti-substitution); any long-running session every ~5 turns (anti-drift).

**Hard rule on overrides**: before skipping any principle, the agent must state in one sentence which principle is being skipped and why. Principles P-001, P-003, P-007, P-010 have no override.

For full principle definitions, examples, and override rationale, see `knowledge/behavioral_discipline.md`.

---

## Examples

### Example 1: Full refresh → analyze cycle

**Scenario**: User says "Refresh all stale docs and tell me what's new worth incorporating into the templates."

**Flow**:
1. `delegate_to_doc_refresh_agent` with `task="Run a full staleness check + fetch over all 34 sources"`. Returns: 4 refreshed cleanly, 3 staged in `source_docs/dropbox/`, 27 still fresh.
2. `delegate_to_merge_agent` × 3 — one per dropbox file. Two succeed; one halts on suspect-overwrite. Orchestrator records the halt but continues.
3. `delegate_to_doc_analysis_agent` with `task="Diff refreshed source_docs/ (incl. 4 just-refreshed + 2 just-promoted) against the standard template set and emit proposals"`. Returns: 7 proposals.
4. Orchestrator synthesizes: refresh summary + merge summary (with halted file flagged) + proposal list. Terminates.

### Example 2: Refresh-only request

**Scenario**: User says "Just refresh Anthropic, don't analyze."

**Flow**:
1. `delegate_to_doc_refresh_agent` with `task="Refresh only Anthropic sources"`.
2. If dropbox files appear, `delegate_to_merge_agent` × N.
3. Termination criterion "user explicitly requested only one phase and that phase completed" → stop. Do NOT call `delegate_to_doc_analysis_agent`. P-007 / P-010.

---

## Resources and References

### Spec files
- `doc_refresh_workflow.json` — topology, delegate tools, termination, system prompt
- `update_agents/doc_refresh_agent.{md,json}` — specialist 1
- `update_agents/merge_agent.{md,json}` — specialist 2 (generated alongside this orchestrator in the dogfood pass)
- `update_agents/doc_analysis_agent.{md,json}` — specialist 3

### Knowledge files
- `knowledge/source_docs_index.{md,json}` — lookup table of the 34 cached docs (referenced via `cross_references.knowledge_files[]`)
- `knowledge/behavioral_discipline.{md,json}` — discipline source

### Source docs (platform grounding)
- `source_docs/anthropic_subagents.md`, `source_docs/openai_handoffs.md`, `source_docs/google_adk_multi_agents.md`, etc. — orchestrator pattern grounding

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Orchestrate refresh → merge → analyze cycle for source_docs/ |
| **Input** | `string` — conversational user request |
| **Output** | Synthesized response: refresh summary + merge summary + proposal list (as applicable) |
| **Agent Type** (implementation) | `multi_agent` |
| **Interaction Pattern** (behavior) | `multi_step_batch` |
| **Specialists** | 3 — `doc_refresh_agent`, `merge_agent`, `doc_analysis_agent` (all referenced by spec_path) |
| **Tools** | `delegate_to_doc_refresh_agent`, `delegate_to_merge_agent`, `delegate_to_doc_analysis_agent` — one per specialist, no extras |
| **Termination** | All stale sources refreshed + merged; OR analysis returned a synthesized proposal list; OR user-requested phase completed |
| **max_turns** | 30 |
| **Common Pitfall** | Forgetting to pass platform-filter from `doc_refresh_agent` step into `doc_analysis_agent` step (cross-agent state) |
| **Dependencies** | All 3 specialist spec files exist + knowledge/source_docs_index.json (read-at-runtime) |
