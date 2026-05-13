# make_orchestrator_agent Skill Guide

## Skill Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `make_orchestrator_agent.json` for structured data, templates, validation rules, and the orchestrator JSON skeleton.
3. This skill **sits alongside `make_agent`**. Use `make_agent` to generate each specialist first; use this skill to generate the orchestrator that delegates to them.
4. **Behavioral Discipline is required in every generated orchestrator spec.** Consult `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json` and follow the integration flow in [make_agent.md](make_agent.md) → "## Behavioral Discipline (core)". The orchestrator picks its own `interaction_pattern` via the standard decision flow; specialists carry their own.

---

## Mission (core)

**What it does**: Generates an orchestrator agent spec (`.md` + `.json` pair) whose job is to delegate work to specialist subagents.

**Why it exists**: When responsibilities span multiple domains, trust levels, or contexts, a single agent with a 25-tool list and a multi-persona system prompt degrades fast. Four platforms now treat multi-agent topology as a first-class primitive — Anthropic subagents, OpenAI Handoffs / `Agent.as_tool()`, Google ADK `sub_agents`, and xAI Multi Agent Beta (with caveats; see "## Platform Coverage" below). This skill produces a topology spec that runners can map to whichever primitive their platform exposes.

**Who uses it**: Engineers building agents whose scope grew past a clean single-agent design. Detected via `make_agent` Pitfall #4 (tool count > 20) or by a clear domain split in the request.

---

## Quickstart (core)

0. **Choose `interaction_pattern` for the orchestrator** (read_only / single_write_workflow / multi_step_batch / single_call_api / conversational) using the decision flow in [make_agent.md](make_agent.md) → "## Behavioral Discipline (core)". Most orchestrators are `multi_step_batch` (they delegate multiple times) or `conversational` (chat-style routing). Ask the user if composite.

1. **Gather inputs**:
   - Orchestrator name + one-line purpose
   - List of specialist spec paths (e.g., `specialists/researcher.json`, `specialists/writer.json`) — each must already exist
   - Termination criteria (what "done" looks like)
   - File I/O mode (string / file / folder)

2. **Read each specialist spec** to extract:
   - `_metadata.skill_name` or top-level name
   - One-line purpose (from mission, description, or `_metadata.description`)
   - `behavioral_discipline.interaction_pattern` (so the orchestrator knows what each specialist's contract is)
   - `io_contract.inputs[0].type` (so the orchestrator knows what shape to pass)

3. **Generate `delegate_to_<specialist_name>` tools** — one per specialist. Each tool:
   - Name: `delegate_to_<specialist_name>` (snake_case, derived from specialist name)
   - Description: specialist purpose + when to use it vs. other specialists (Pitfall #7 in [make_agent.md](make_agent.md) applies)
   - Input schema: matches specialist's input contract; default `{ "task": "string" }` if specialist takes string

4. **Compose the orchestrator MD + JSON** from `orchestrator_md_template` and `orchestrator_json_template` in `make_orchestrator_agent.json`. Embed the behavioral discipline using the standard flow.

5. **Propose and wait for confirmation** (P-002). Do not write until the user approves the spec.

6. **Write files** and **run `make_agent_qc`** — confirm ORCH-QC-001 through ORCH-QC-005 pass alongside BD-QC and the standard rules.

---

## File Organization: JSON vs MD (core)

Same convention as [make_agent.md](make_agent.md). MD = the why (mission, topology rationale, routing design narrative). JSON = the what (specialist roster, tool definitions, termination criteria, templates). The generated orchestrator agent follows the same split.

---

## Key Principles (core)

### 1. The Orchestrator Is Its Own Agent

**Description**: The orchestrator is a full agent with its own system prompt, tools, and discipline — not a thin wrapper or a Python `if/else` over specialist calls.

**Why**: Treating it as a wrapper hides the routing logic in code and bypasses the discipline. Treating it as an agent means the routing reasoning is visible (in tool calls), auditable (in `parent_tool_use_id` traces), and subject to the same QC as any other agent.

**How**: `agent_type.type: "multi_agent"` on the generated orchestrator. It has its own `behavioral_discipline` block, its own `interaction_pattern`, its own `system_prompt`. The specialists are tools, not subroutines.

### 2. Specialists Are Decoupled — Referenced By Path

**Description**: The orchestrator JSON references specialists by `spec_path` only. It does NOT inline specialist content.

**Why**: Inlining duplicates spec content (drift), breaks the per-spec QC contract, and prevents reuse. A specialist should be usable standalone, by other orchestrators, or by direct invocation. Path references preserve this.

**How**: `topology.specialists[].spec_path` points to the specialist's `.json`. The skill reads it at generation time to derive the `delegate_to_*` tool, but does not copy its body.

### 3. Routing Decisions Are Visible In Tools, Not Hidden In Prompts

**Description**: Each routing decision is encoded as a `delegate_to_<specialist>` tool call. The orchestrator's prompt does NOT contain `if input mentions X, route to Y` style rules.

**Why**: Tool-based routing produces an auditable trace — every routing decision shows up as a `tool_use` block with arguments and a `tool_result` with the specialist's response. Prompt-based routing produces no such trace; debugging "why did it pick that specialist?" devolves to reading prompts and guessing.

**How**: Generate one `delegate_to_*` tool per specialist. The tool's description carries the "when to use this" guidance. The model chooses tools; the runner executes them; the trace records the choice.

### 4. Termination Is Explicit

**Description**: Every orchestrator declares `termination_criteria` — the condition under which it stops delegating and returns a final answer.

**Why**: Without explicit termination, the orchestrator either loops indefinitely (delegate → result → re-delegate) or terminates on the first specialist call regardless of completeness. Both are bugs. Explicit criteria let the runner enforce `max_turns` correctly and let the model know what "done" means.

**How**: `topology.termination_criteria` is a non-empty string in the generated JSON. The system prompt restates it: "Stop delegating and return your synthesis when: <criteria>."

---

## Behavioral Discipline (core)

This skill itself operates under `interaction_pattern: single_write_workflow` (it proposes one orchestrator spec per invocation, waits for confirmation, writes). The skill's applicable principles: P-001, P-002, P-003, P-004, P-006, P-007, P-008, P-009, P-010 (skip P-005 — single-step workflow).

The **generated orchestrator** inherits its own discipline via the standard decision flow. Most orchestrators land on `multi_step_batch` (multiple specialist delegations per session) or `conversational` (chat-style routing). The orchestrator's discipline is independent of any specialist's discipline — each agent owns its own.

The full integration flow is documented once, in [make_agent.md](make_agent.md) → "## Behavioral Discipline (core)". This skill follows it unchanged. The QC checks BD-QC-001 through BD-QC-007 apply to the generated orchestrator just like any other agent.

---

## File I/O Mode (core)

**This skill's input**: interactive (the user supplies orchestrator name, purpose, specialist paths, and termination criteria conversationally). `io_contract.inputs[0].type: "string"`.

**The generated orchestrator's input**: declared per orchestrator per the same rules as [make_agent.md](make_agent.md) → "## File I/O Mode (core)". String for chat-style orchestrators; file/folder for batch-style.

---

## Platform Coverage

Four platforms support multi-agent topology, but the shape differs. The orchestrator spec this skill emits is intentionally platform-agnostic; runners map it to the host platform's primitive at execution time.

| Platform | Named specialists? | Primitive | Trace field | State default | Maps to this skill |
|---|---|---|---|---|---|
| **Anthropic** (Claude Agent SDK) | Yes | `agents={"name": AgentDefinition(...)}`; invoked via the `Agent` tool | `parent_tool_use_id` | Stateless — subagents do not receive parent history | Direct map: each `topology.specialists[]` entry → one `AgentDefinition` |
| **OpenAI** (Agents SDK) | Yes | `Handoff` (typed) **or** `Agent.as_tool()` (manager pattern) | `parent_id` on `agent_span` / `handoff_span` | Handoffs carry filtered history via `HandoffInputData`; `Agent.as_tool` is stateless | Direct map: choose `Handoff` for fan-out hand-control style, `Agent.as_tool()` for the `delegate_to_*` manager style this skill emits |
| **Google ADK** | Yes | `sub_agents=[...]` list with `parent_agent` auto-set; LLM emits `transfer_to_agent(agent_name=...)` **or** explicit `AgentTool(agent=...)` wrapper | `parent_agent` attribute on `BaseAgent`; `InvocationContext` flows through the tree | Shared `session.state` across the agent tree (stateful) | Direct map: each specialist → one entry in `sub_agents`; `AgentTool` wrapper mirrors this skill's `delegate_to_*` tools |
| **xAI** (Grok Multi-Agent Beta) | **No** | `agent_count=4` or `16` on the `grok-4.20-multi-agent` model; orchestration is server-side | Sub-agent state is **encrypted** unless `use_encrypted_content=true` exposes it to the caller | Stateless from the caller's perspective | **Exception — this skill does not target xAI directly.** xAI's multi-agent runner uses anonymous workers chosen by the leader agent on the server; there are no named specialists and no caller-side `delegate_to_*` equivalent. An xAI deployment uses the underlying model directly with `agent_count` set; a spec generated by this skill won't translate to xAI without a wrapper that flattens the topology into a single-agent call with `agent_count` ≥ 2. |

**Implication for spec generation**: assume the host platform is Anthropic, OpenAI, or Google ADK. The orchestrator spec is portable across those three. For xAI deployments, generate a single-agent spec via `make_agent` and set the model to `grok-4.20-multi-agent` with the appropriate `agent_count` — do not generate an orchestrator spec at all.

---

## A note on the generated MD's structure

The MD this skill emits **does NOT inherit `make_agent.md`'s full "core" section list** (Mission / Quickstart / Key Principles / How to Use / Pitfalls / Examples / etc.). An orchestrator's MD uses the 7 sections defined in `make_orchestrator_agent.json` → `orchestrator_md_required_sections` only: Title, Mission, Topology, Routing Decisions, Cross-Agent State, Termination, Behavioral Discipline. Optional sections (Platform Notes, Failure Routing, Examples) are added per the `include_when` criteria in `orchestrator_md_optional_sections`.

**Why the divergence**: the orchestrator's "principles" are the discipline (embedded in the Behavioral Discipline section) — there's no separate Key Principles content. Pitfalls live in this skill file (`make_orchestrator_agent.md` → Common Pitfalls), not in each generated orchestrator. Quickstart and How-to-Use are about the skill that *generates* orchestrators, not the orchestrators themselves; the runtime entry point for an orchestrator is its JSON system_prompt, not a humans-only quickstart.

If you find yourself wanting to add a Quickstart or Key Principles section to a generated orchestrator, that probably means you should split it into specialists (each of which gets its own full `make_agent.md` treatment) and shrink the orchestrator's scope to pure routing.

---

## Topology Declaration

The `topology` object in the generated orchestrator JSON. Required fields:

```jsonc
"topology": {
  "specialists": [
    {
      "name": "researcher",                          // snake_case; becomes delegate_to_researcher
      "spec_path": "specialists/researcher.json",    // must exist at generation time
      "purpose": "Gathers and summarizes background info on a topic from internal docs.",
      "input_contract": { "task": "string" },        // derived from specialist's io_contract
      "expected_output": "structured findings as markdown"
    }
    // ... more specialists
  ],
  "routing_strategy": "llm_routed",                  // fixed for v1; declarative/hybrid reserved
  "handoff_protocol": {
    "carry": ["user_request"],                       // what context flows orchestrator → specialist
    "format": "tool_call_args"                       // how it's passed
  },
  "return_protocol": {
    "shape": "free_text",                            // what specialist returns
    "orchestrator_post_processing": "synthesize"     // what orchestrator does with it
  },
  "termination_criteria": "All required specialists have returned and the user's original question has a synthesized answer."
}
```

**Constraints**:
- Minimum 2 specialists (one specialist is not an orchestrator — just call it directly)
- Maximum 10 specialists (beyond that, sub-orchestrators are better than a flat fan-out)
- No duplicate specialist names within a single orchestrator
- Specialist `spec_path` must resolve at generation time (P-001)

**Local vs Remote specialists**: this skill assumes specialists run **in-process** with the orchestrator (Anthropic `AgentDefinition`, OpenAI `Agent.as_tool`, Google ADK `sub_agents`). When a specialist is a **separate network service** — different team, different language, different deployment lifecycle — use Google ADK's Agent2Agent (A2A) protocol instead: expose the remote specialist via `to_a2a(root_agent)` and consume it from the orchestrator via `RemoteA2aAgent(name=..., agent_card=...{AGENT_CARD_WELL_KNOWN_PATH})`. The orchestrator spec this skill emits still applies — the specialist's `spec_path` is replaced by an `agent_card` URL — but the runner maps `delegate_to_<specialist>` to a network call rather than an in-process invocation. Do not mix the two casually: A2A adds network overhead, serialization, and an extra failure mode (specialist host unreachable) that local sub-agents do not have. See `source_docs/google_adk_a2a_intro.md` and `source_docs/google_adk_a2a_quickstart_consuming.md` for the protocol details.

---

## Routing Design

The orchestrator does NOT route via prompt heuristics. It routes via tool selection. The skill generates one `delegate_to_<specialist_name>` tool per entry in `topology.specialists`:

```jsonc
{
  "name": "delegate_to_researcher",
  "description": "Use this tool to delegate research tasks to the researcher specialist. Use it when: the user asks for background, factual lookups, or comparison of options. Do NOT use it for: tasks that require writing prose (use delegate_to_writer instead) or tasks already covered by prior delegations in this session.",
  "input_schema": {
    "type": "object",
    "properties": {
      "task": { "type": "string", "description": "The specific subtask for the researcher to perform. Be concrete." }
    },
    "required": ["task"]
  },
  "_meta": { "execution": "client", "specialist_spec_path": "specialists/researcher.json" }
}
```

**Tool description quality is critical** — see Pitfall #7 in [make_agent.md](make_agent.md). The description must answer: what the specialist does, when to use it vs. other specialists in this orchestrator, and what each parameter expects. Thin descriptions produce wrong routing.

**Prompt prefix for handoff-style routing (OpenAI target)**: when the orchestrator will run on the OpenAI Agents SDK with `Handoff` primitives (rather than `Agent.as_tool()`), prepend the SDK's `agents.extensions.handoff_prompt.RECOMMENDED_PROMPT_PREFIX` (or call `prompt_with_handoff_instructions(your_prompt)`) to the orchestrator's `system_prompt`. The prefix teaches the model the handoff semantics — when to transfer, that the receiving agent will see the conversation history, that `transfer_to_<agent>` is a tool, not a method name. Without the prefix, models routinely narrate the handoff in prose ("I'll connect you to billing") instead of emitting the `transfer_to_billing` tool call. This addition is OpenAI-specific; on Anthropic and Google, the equivalent guidance lives in each specialist's `description` field and is read automatically by the runtime. See `source_docs/openai_handoffs.md` (RECOMMENDED_PROMPT_PREFIX section).

**Parallel vs. sequential delegation**: When specialists are independent (e.g., researcher and graph-builder operating on the same input), set `disable_parallel_tool_use: false` so the model can fan out. When specialists depend on each other's output (writer needs researcher's findings), set `disable_parallel_tool_use: true` per Pitfall #8 in [make_agent.md](make_agent.md).

---

## Cross-Agent State

What the orchestrator carries vs. what each specialist sees:

| State | Orchestrator carries | Specialist sees |
|---|---|---|
| Full conversation history | Yes (for synthesis) | No (only the task it was delegated) |
| Prior specialist outputs | Yes (in its own context) | Only if explicitly passed in `task` |
| User identity / session ID | Yes | Only if `handoff_protocol.carry` lists it |
| Domain knowledge files | If listed in its `cross_references.knowledge_files` | Same — per specialist |

**Default**: specialists are stateless w.r.t. each other. The orchestrator is the only place where cross-specialist state accumulates. If a specialist needs prior findings from another specialist, the orchestrator MUST pass them in the `task` argument explicitly.

**Two state-transfer modes — pick one per orchestrator**:
- **Explicit-task** (this skill's default): the orchestrator copies specialist-A's output into the `task` argument of `delegate_to_specialist_b`. Stateless, auditable, portable across all platforms. Use this unless the host platform supports the alternative.
- **Shared-state** (Google ADK only): when running on ADK, specialists in the same `SequentialAgent` / `ParallelAgent` tree share `session.state`. An `LlmAgent` can declare `output_key="capital_city"` to auto-write its final response, and a downstream agent's `instruction` can read it via `{capital_city}` template substitution. This is faster (no copy) and survives mid-pipeline restarts (state is persisted), but it is platform-specific and obscures the data flow in the trace. When generating an ADK-targeted orchestrator using shared-state, declare it explicitly in `topology.handoff_protocol.format: "shared_state"`. Keep `tool_call_args` for explicit-task.

OpenAI handoffs (`HandoffInputData.input_filter`) and Anthropic subagents (`AgentDefinition.prompt`) both require explicit-task — they do not share state. See `source_docs/google_adk_multi_agents.md`, `source_docs/openai_running_agents.md`, `source_docs/anthropic_subagents.md`.

**Memory strategy**: choose `parameters.memory` per the principle "Choose a Memory/State Strategy Before Building" in [make_agent.md](make_agent.md). Orchestrators with long-running sessions typically use `platform_session`; one-shot orchestrators use `stateless`.

---

## Termination

The orchestrator declares termination explicitly in three places:

1. **`topology.termination_criteria`** (JSON) — a one-sentence condition, e.g., "All required specialists have returned and the user's original question has a synthesized answer."
2. **`implementation.llm_agent.system_prompt`** — restates the criteria + names the action: "When this condition is met, stop calling tools and return your final synthesis."
3. **`implementation.llm_agent.parameters.max_turns`** (or runner-side equivalent) — a hard upper bound that catches the case where the criteria are never satisfied.

The three together produce: clear intent (criteria), prompt-level instruction (system prompt), and runtime safety net (max_turns). Missing any one of the three is an orchestrator that either loops or terminates prematurely.

---

## How to Use This Skill

### Prerequisites
- At least 2 specialist agent specs (`.md` + `.json` pairs) already generated via `make_agent`
- `knowledge/behavioral_discipline.json` readable
- Clear orchestrator purpose (one sentence)
- Clear termination criteria (one sentence)

### Basic Usage

1. **Generate specialists first**. For each specialist, run `make_agent` and save the resulting `.md` + `.json` pair in a stable location (e.g., `specialists/`).

2. **Invoke `make_orchestrator_agent`** with:
   - Orchestrator name (snake_case)
   - One-line purpose
   - Specialist paths (list)
   - Termination criteria (one sentence)
   - File I/O mode (string / file / folder)

3. **Review the proposed orchestrator spec**. The skill presents the generated MD + JSON before writing.

4. **Approve to write**. Skill writes `<orchestrator_name>.md` and `<orchestrator_name>.json`.

5. **Run `make_agent_qc`** against the orchestrator. ORCH-QC-001 through ORCH-QC-005 are orchestrator-specific; BD-QC-001 through BD-QC-007 apply normally.

---

## Common Pitfalls and Solutions (core)

### 1. Toolifying Specialists Instead of Agentifying Them

**Problem**: The orchestrator's `tools[]` array contains the specialist's *underlying tools* (e.g., `search_docs`, `write_markdown`) directly, instead of a `delegate_to_<specialist>` wrapper.

**Why it happens**: It looks simpler to expose the specialist's tools to the orchestrator. But this defeats the purpose: the specialist's system prompt, discipline, and decision logic are bypassed, and the orchestrator becomes a mega-agent in disguise.

**Solution**: The orchestrator's tools are `delegate_to_*` wrappers only. Each wrapper hands a task to the specialist, which then runs its own loop with its own tools and returns a result. The orchestrator never sees the specialist's internal tool calls.

### 2. Orchestrator With Only One Specialist

**Problem**: The orchestrator wraps a single specialist. The "orchestrator" adds a layer of indirection with no routing decision to make.

**Why it happens**: Sometimes an orchestrator is generated speculatively — "we might add more specialists later." Until then, every call is a passthrough.

**Solution**: Don't generate an orchestrator until there are at least 2 specialists with a real routing decision between them. ORCH-QC-002 enforces this. If you anticipate growth, just call the specialist directly and add the orchestrator when the second specialist appears.

### 3. Routing Logic In The System Prompt

**Problem**: The orchestrator's system prompt contains paragraphs like "If the user asks about X, call researcher. If they ask about Y, call writer. If X and Y, call researcher first then writer."

**Why it happens**: It's the most natural way to write routing rules in English. But it hides decisions from the trace and tends to bloat as specialists are added.

**Solution**: Put the routing guidance in each tool's `description` field, not in the system prompt. The system prompt should describe the orchestrator's role and termination criteria, not the per-specialist routing logic. The tools' descriptions are what the model reads when deciding which to call.

### 4. No Termination Criteria

**Problem**: The orchestrator loops indefinitely — every specialist response triggers another delegation, with no condition that ends the loop.

**Why it happens**: `termination_criteria` left empty or vague ("done when the user is satisfied"). The model has no observable signal for "satisfied."

**Solution**: Termination must be observable to the model from the conversation state — "all required specialists have returned," "no further questions remain in the user's request," "the synthesis is complete." Then set `max_turns` as a backstop. ORCH-QC-004 enforces non-empty criteria.

### 5. Specialists Sharing An Implicit State Channel

**Problem**: Specialist A modifies a file or external state; specialist B is expected to read it. The orchestrator never passes the state, and B fails silently when the file isn't there.

**Why it happens**: Forgetting that specialists are stateless w.r.t. each other. The orchestrator is the only point where cross-specialist state lives.

**Solution**: Make state transfer explicit. Either the orchestrator carries the state in its context and passes it to B in the `task` argument, or A returns the state location/handle in its response and the orchestrator includes that in B's task. Never assume specialists share state through side effects.

---

## Examples (core)

### Example 1: Research → Write orchestrator

**Scenario**: User asks for a written summary of a complex topic. Researcher specialist gathers facts; writer specialist produces prose.

**Specialists**: `specialists/researcher.json`, `specialists/writer.json`

**Topology**:
```json
{
  "specialists": [
    { "name": "researcher", "spec_path": "specialists/researcher.json", "purpose": "Gathers factual background", "input_contract": { "task": "string" } },
    { "name": "writer", "spec_path": "specialists/writer.json", "purpose": "Produces prose from structured findings", "input_contract": { "task": "string", "findings": "string" } }
  ],
  "routing_strategy": "llm_routed",
  "handoff_protocol": { "carry": ["user_request"], "format": "tool_call_args" },
  "return_protocol": { "shape": "free_text", "orchestrator_post_processing": "synthesize" },
  "termination_criteria": "Writer has returned a finished summary that addresses the user's original question."
}
```

**Flow**: Orchestrator receives "summarize X". Calls `delegate_to_researcher` with `{ task: "research X" }`. Receives findings. Calls `delegate_to_writer` with `{ task: "summarize X", findings: <researcher output> }`. Writer returns prose. Orchestrator returns it.

### Example 2: Triage → Specialist routing

**Scenario**: User submits an issue. Orchestrator routes to one of three specialists based on content (bug, feature, question).

**Specialists**: `specialists/bug_handler.json`, `specialists/feature_planner.json`, `specialists/qa_responder.json`

**Termination**: "The selected specialist has returned a response that addresses the user's submission."

**Flow**: Orchestrator reads submission. Calls one of three `delegate_to_*` tools based on tool description match. Returns specialist's response. (One delegation, then done.)

---

## Validation and Testing (core)

See `make_orchestrator_agent.json` → `validation` for the pre-run / post-run checklists.

The orchestrator-specific QC checks live in [make_agent_qc.json](make_agent_qc.json) under the new ORCH-QC family:

- **ORCH-QC-001**: All `topology.specialists[].spec_path` files exist and are readable
- **ORCH-QC-002**: `topology.specialists` has at least 2 entries
- **ORCH-QC-003**: One `delegate_to_<specialist>` tool exists per specialist in `topology.specialists`, no extras, no duplicates
- **ORCH-QC-004**: `topology.termination_criteria` is non-empty and restated in the system prompt
- **ORCH-QC-005**: No specialist's underlying tools appear directly in the orchestrator's `tools[]` (P-007 + Pitfall #1)

Standard BD-QC-001 through BD-QC-007 and the rest of `make_agent_qc` apply unchanged.

---

## Resources and References

### Skill Files
- `make_orchestrator_agent.json`: Templates, schemas, validation rules
- `make_agent.md` / `make_agent.json`: Sibling skill for specialist generation
- `make_agent_qc.md` / `make_agent_qc.json`: QC pipeline; ORCH-QC family lives here
- `knowledge/behavioral_discipline.md` / `.json`: Discipline source of truth

### Related Concepts
- **Anthropic Agent SDK subagents**: `agents={"name": AgentDefinition(...)}` with `parent_tool_use_id` — see `source_docs/anthropic_subagents.md`
- **OpenAI Agents SDK Handoffs / `Agent.as_tool()`**: typed handoff primitive + manager-as-tool pattern — see `source_docs/openai_handoffs.md`, `source_docs/openai_agents_class.md`, `source_docs/openai_multi_agent.md`
- **Google ADK multi-agents**: `sub_agents=[...]`, `parent_agent`, `transfer_to_agent()`, `AgentTool` wrapper, workflow agents (`SequentialAgent`/`ParallelAgent`/`LoopAgent`) — see `source_docs/google_adk_multi_agents.md`
- **xAI Multi Agent Beta**: server-side runner with `agent_count=4|16`; anonymous workers (see "Platform Coverage") — see `source_docs/xai_multi_agent.md`

The skill targets the first three (named-specialist) platforms. xAI is documented as an exception; an xAI deployment uses `make_agent` with the multi-agent model directly.

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Generates multi-agent orchestrator specs that delegate to specialist subagents |
| **Input** | Orchestrator name, purpose, specialist paths, termination criteria, I/O mode |
| **Output** | `<orchestrator>.md` + `<orchestrator>.json` pair with `agent_type.type: multi_agent` |
| **Skill's own type** (implementation) | workflow |
| **Skill's own pattern** (behavior) | single_write_workflow |
| **Generated orchestrator's typical pattern** | multi_step_batch or conversational |
| **Specialist roster** | File paths to existing `.json` specs; min 2, max 10 |
| **Routing** | LLM-routed via auto-generated `delegate_to_<specialist>` tools |
| **QC** | ORCH-QC-001..005 in make_agent_qc.json |
| **Common Pitfall** | #1 Toolifying specialists instead of agentifying them |
| **Dependencies** | At least 2 pre-existing specialist agent specs |
