---
platform: OpenAI
label: OpenAI Agents SDK
source_url: https://openai.github.io/openai-agents-python/
last_fetched: 2026-03-11
fetch_status: success
notes: platform.openai.com returns 403 for all docs URLs. This file uses GitHub Pages docs instead. Covers core primitives (Agents, Handoffs, Guardrails), lifecycle hooks, multi-agent patterns, tool control, structured outputs.
alternate_pages_fetched:
  - https://openai.github.io/openai-agents-python/
  - https://openai.github.io/openai-agents-python/agents/
---

## OpenAI Agents SDK — Overview

The OpenAI Agents SDK is a production-ready Python framework for building agentic AI applications. "A production-ready upgrade of our previous experimentation for agents, Swarm."

**Install:**
```bash
pip install openai-agents
```

---

## Three Core Primitives

1. **Agents** — LLMs equipped with instructions and tools
2. **Handoffs** — Agents delegating to other agents for specific tasks
3. **Guardrails** — Validation mechanisms for agent inputs and outputs

**Design philosophy**: Sufficient functionality to be useful with minimal primitives for quick learning. Excellent out-of-the-box experience with customization options.

---

## Agent Configuration

An agent is configured with instructions, tools, and optional runtime behaviors.

**Agent properties:**

| Property | Required | Description |
|----------|----------|-------------|
| `name` | Yes | Human-readable identifier |
| `instructions` | Yes | System prompt or dynamic callback function |
| `handoffs` | No | Specialist agents to delegate to |
| `model` | No | LLM selection |
| `model_settings` | No | Tuning parameters (temperature, top_p) |
| `tools` | No | Available capabilities |
| `mcp_servers` | No | MCP-backed tools |
| `input_guardrails` | No | Validation checks on user input |
| `output_guardrails` | No | Validation checks on agent output |
| `output_type` | No | Structured output format (Pydantic, TypedDict, etc.) |
| `tool_use_behavior` | No | How tool results are handled |
| `reset_tool_choice` | No | Prevents tool-use loops |
| `handoff_description` | No | Description used when this agent is a handoff target |

---

## Dynamic Instructions

Instructions can be a static string or a function receiving agent and context, returning a prompt string. Both sync and async functions are supported.

---

## Context Management

Agents accept a generic context type for dependency injection. Context objects pass through all agent operations, tools, and handoffs — serves as shared state and dependency container.

---

## Structured Output

Set `output_type` to a Pydantic model, dataclass, TypedDict, or other Pydantic-compatible type. This triggers structured output mode in the underlying model — the agent's final response will conform to the schema.

---

## Multi-Agent Patterns

**Manager Pattern (Orchestrator):** A central orchestrator invokes specialized sub-agents as tools, maintaining conversation control.

**Handoffs (Decentralized):** Peer agents transfer control to specialists who take over conversations entirely.

---

## Lifecycle Hooks

Two hook scopes:
- **RunHooks**: Monitor entire `Runner.run()` invocations across handoffs
- **AgentHooks**: Specific agent instance observations

Hook events: agent start/end, LLM calls, tool invocation, handoffs.

---

## Guardrails

Validation checks run **in parallel** with agent execution — on user input and agent output. Used for relevance screening, safety checks, or other validation. Running in parallel means they don't add latency to the happy path.

---

## Tool Choice Control

| Value | Behavior |
|-------|----------|
| `"auto"` | LLM decides (default) |
| `"required"` | LLM must use a tool |
| `"none"` | LLM cannot use tools |
| specific tool name | Force a particular tool |

Note: The framework auto-resets `tool_choice` to `"auto"` after tool calls to **prevent infinite loops**.

---

## Tool Use Behavior — Four approaches

1. `"run_llm_again"` (default): LLM processes tool results and continues
2. `"stop_on_first_tool"`: First tool output becomes the final response
3. `StopAtTools`: Stops when specified tools are called
4. `ToolsToFinalOutputFunction`: Custom handler deciding whether to continue

---

## MCP Server Integration

Agents support MCP servers via the `mcp_servers` property — provides MCP-backed tools without manual tool definition.

---

## Major SDK Features

- Built-in agent loop handling tool invocation (no manual loop needed)
- Python-first orchestration
- Agent-to-agent delegation (handoffs)
- Input/output validation through guardrails (parallel execution)
- Automatic schema generation for Python functions as tools
- MCP server integration
- Persistent memory layer via sessions
- Human-in-the-loop mechanisms
- Built-in tracing for visualization and debugging
- Realtime voice agent capabilities with interruption detection

---

## Agent Cloning

The `clone()` method duplicates agents with optional property overrides — useful for creating variants of a base agent.
