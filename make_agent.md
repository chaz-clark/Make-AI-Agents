# <Your Agent Name> Agent Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `<your_agent_name>.json` for structured data, code/config examples, validation, and operations. Do not parse this Markdown.
3. Keep this file lean. For simple agents, include only Mission, Quickstart, JSON vs MD guidance, Key Principles, How to Use, Pitfalls, Examples, Validation, and Resources.
4. For added complexity, only append the optional sections marked below.

---

## Mission (core)

A clear and concise statement of the agent's primary purpose.

**What it does**: [Primary function - what the agent accomplishes]

**Why it exists**: [Problem it solves - the pain point this addresses]

**Who uses it**: [Target audience - developers, data scientists, analysts, etc.]

**Example**: "Summarizes technical documentation using GPT-4, reducing reading time by 80% while preserving key information."

---

## Agent Quickstart (core)

A fast-path workflow for getting started with this agent:

1. **[Identify/Load]**: What the agent identifies or loads first
   - Example: "Load system prompts from `agent.json` primary_data"

2. **[Parse Data]**: Load structured data from `<your_agent_name>.json`
   - Example: "Parse API endpoint mappings from primary_data"

3. **[Apply/Transform]**: Main processing step
   - Example: "Send request to OpenAI API with formatted prompt"

4. **[Validate]**: How to verify results
   - Example: "Check summary length < 500 tokens, readability score > 60"

5. **[Output]**: What the agent produces
   - Example: "Return formatted markdown summary"

For detailed operational procedures and structured data, see `<your_agent_name>.json`.

---

## File Organization: JSON vs MD (core)

Understanding what content belongs in each file type:

### This Markdown File (.md) Contains:
- ✅ Mission and purpose (the "why")
- ✅ Design philosophy and principles
- ✅ Conceptual explanations (e.g., "How the agent makes decisions")
- ✅ Educational context and narrative
- ✅ Common pitfalls (explained narratively with context)
- ✅ Resources and external references
- ✅ High-level strategy and workflow

### The JSON File (.json) Contains:
- ✅ Structured data (arrays, objects, mappings)
- ✅ Code snippets and syntax examples
- ✅ Configuration parameters
- ✅ Quick reference lookups (e.g., API endpoints, prompts, rules)
- ✅ Validation checklists and test cases
- ✅ Operational procedures (step-by-step data)
- ✅ Before/after code pairs

**Rule of Thumb**: If an agent needs to parse it → JSON. If a human needs to understand the "why" → MD.

---

## Key Principles (core)

The design principles behind this agent. These guide all decisions and implementations.

### 1. [Principle Name]
**Description**: [What this principle means]

**Why**: [Rationale - why this principle matters]

**How**: [Implementation approach - how it's achieved in practice]

**Example**:
```
Reliability
Description: Agent must handle failures gracefully without data loss
Why: Users depend on consistent results for production workflows
How: Implement retry logic with exponential backoff, cache intermediate results, validate all inputs
```

### 2. [Principle Name]
[Same structure as above]

### 3. [Additional Principles]
Common principles across successful agents:
- **Simplicity**: Easy to understand and use
- **Reliability**: Handles errors gracefully
- **Performance**: Fast enough for the use case
- **Observability**: Easy to debug and monitor
- **Security**: Protects sensitive data

### Recommended Principles for LLM Agents

**Explicit Tool Control**
**Description**: Always set `tool_choice` intentionally — don't rely on the model default.
**Why**: Default (`auto`) is correct for conversational agents, but agentic loops often need `required` to prevent the model skipping tool calls, or a specific tool name to force a deterministic step.
**How**: Set `tool_choice` in `implementation.llm_agent.parameters`. Use `required` only when you know a tool call is mandatory; reset to `auto` after the first forced call to avoid infinite loops.

**Guardrails as a Separate Layer**
**Description**: Input validation and output validation belong outside the agent's core logic — not inside system prompts or tool implementations.
**Why**: Embedding safety checks in prompts makes them invisible to reviewers and easy to override. A dedicated guardrail layer is auditable, replaceable, and testable independently.
**How**: Implement pre/post hooks (Anthropic pattern) or parallel guardrail checks (OpenAI pattern). Document them in `constraints.safety_boundaries.guardrails` in the JSON.

**Observability via Lifecycle Hooks**
**Description**: Instrument agent behavior at defined lifecycle points rather than scattering logging inside tools.
**Why**: Hooks (on_tool_call, on_tool_result, on_agent_end) give a consistent, auditable trace of every agent run without coupling observability logic to business logic.
**How**: Register hooks for metrics, logging, and guardrail triggers. See `operational_guidance.best_practices` in the JSON for the hook pattern.

**Stop Sequence Control**
**Description**: Set `stop_sequences` explicitly for agents that produce structured or delimited output.
**Why**: Without stop sequences, the model may generate beyond intended boundaries in multi-step structured outputs — appending extra JSON, continuing past delimiter tokens, or producing redundant responses. Stop sequences provide a hard boundary that is more reliable than prompting the model to "stop here."
**How**: Define one or more stop sequences in `implementation.llm_agent.parameters.stop_sequences` that match your expected output boundaries (e.g., `["</output>", "###"]`). Leave empty `[]` if not needed — the parameter should be present so practitioners remember it exists.

**Temperature by Agent Mode**
**Description**: Set temperature differently for tool-calling agents vs. conversational agents — they have opposite needs.
**Why**: Tool selection and parameter generation require consistency across runs. At temperature 0.7 (the template default), a model may choose different tools or generate different parameter values for identical inputs. This causes non-deterministic agentic behavior that is difficult to debug. Conversational agents benefit from higher temperature for natural variation.
**How**: For tool-calling agents, set `temperature: 0.0–0.2` in `implementation.llm_agent.parameters`. For conversational agents, the default 0.7 is appropriate. Document the choice in the parameters section. Three platforms (Anthropic, Google, xAI) independently recommend low temperature for deterministic tool use.

**Structured Output vs. Function Calling — Different Jobs**
**Description**: Use structured output (`response_format`) when you want the model's final answer in a specific schema. Use function calling (tools) when you need the model to request an action during the conversation.
**Why**: Conflating these leads to over-engineering — defining tools when structured output would suffice, or expecting a formatted final response from a tool-calling loop that produces raw text. The distinction is: structured output shapes the terminal response; function calling shapes intermediate steps.
**How**: If your agent needs to return a structured JSON object as its final answer, set `response_format` in parameters. If your agent needs to take actions (fetch data, write files, call APIs) before producing a final answer, use tools. Some agents need both: tools for the agentic loop, `response_format` for the final structured output.

---

## Core Concepts (optional for complex agents)
Add only if the agent needs deeper narrative explanation (2–4 concepts). Otherwise omit.

---

## How to Use This Agent (core)

### Prerequisites
- [Required knowledge, tools, or environment setup]
- [Dependencies or API keys needed]
- [Data sources or files required]

### Basic Usage

**Step 1: [Setup]**
```bash
# Installation or setup commands
pip install -r requirements.txt
export API_KEY=your_key_here
```

**Step 2: [Load Configuration]**
```python
# Load agent configuration from JSON
from agent import YourAgent
agent = YourAgent.from_config("<your_agent_name>.json")
```

**Step 3: [Execute]**
```python
# Basic usage pattern
result = agent.process(input_data)
print(result)
```

**Step 4: [Verify]**
- Check output format matches `io_contract` in JSON
- Validate results against test cases in JSON `validation` section

### Advanced Usage (optional)
Include only if needed; otherwise omit.

## Hello World Loader (example)
Minimal pattern for wiring an agent with the JSON:
```python
# agent_loader.py
import json
from agent import YourAgent

def load_agent(config_path: str) -> YourAgent:
    cfg = json.loads(open(config_path).read())
    # pick the right implementation branch from cfg["implementation"]
    return YourAgent.from_config(cfg)

if __name__ == "__main__":
    agent = load_agent("my_agent.json")
    print(agent.process({"text": "hello"}))
```
Run: `python agent_loader.py`

---

## Common Pitfalls and Solutions (core)

Mistakes to avoid when using this agent, with explanations and fixes.

### 1. [Pitfall Name]

**Problem**: [What goes wrong - describe the error or issue]

**Why it happens**: [Root cause - explain the underlying reason]

**Solution**: [How to avoid or fix it]

**Example**:
```python
# ❌ Wrong
result = agent.process(large_input)  # May timeout

# ✅ Correct
result = agent.process(large_input, timeout=120, batch_size=100)
```

### 2. [Pitfall Name]

[Same structure as above]

### 3. Infinite Tool Loop

**Problem**: The agent repeatedly calls tools without reaching a stopping condition, consuming tokens and budget indefinitely.

**Why it happens**: When `tool_choice` is set to `required`, the model is forced to call a tool on every turn — including turns where it would otherwise return a final answer. Without a `max_turns` limit, this produces an infinite loop.

**Solution**: Set a `max_turns` limit in your agent runner. Use `tool_choice=required` only for the specific turn that needs it, then reset to `auto`. Implement loop detection (e.g., track repeated tool calls with identical arguments). Document this in `error_handling.known_failures` in your JSON.

### 4. Too Many Tools Per Agent

**Problem**: Agent performance degrades noticeably when the tool list grows beyond 20 entries — the model struggles to select the right tool and may hallucinate tool names.

**Why it happens**: Large tool sets increase the model's decision space. The model must reason across all available tools on every call, and beyond a threshold (empirically 10-20 tools per Google's documentation), this overhead hurts selection accuracy.

**Solution**: Keep each agent's tool count to 10-20. If you need more tools, split them across specialized sub-agents and use a multi-agent routing pattern. Document the split in `cross_references.related_agents`.

### 5. Missing Input Examples for Complex Tools

**Problem**: Tools with nested parameters or format-sensitive inputs are called with incorrect or guessed values, causing silent failures or API errors.

**Why it happens**: Without `input_examples`, the model infers how to call a tool from its description and parameter schema alone. For complex nested objects or parameters with precise format requirements (e.g., date strings, coordinate pairs), inference is insufficient — the model guesses and often guesses wrong.

**Solution**: Add `input_examples` to tool definitions for any tool with non-trivial parameter structures. The examples teach the model the expected call format directly. Anthropic documentation identifies this as a key reliability improvement for tool-heavy agents.

### 6. Wrong Order in Tool Result Messages

**Problem**: The API returns an error or unexpected behavior when tool results are sent back in the wrong order within the user message content array.

**Why it happens**: When returning tool results, the `tool_result` content blocks must come **first** in the user message's `content` array. Any accompanying text (e.g., "What should I do next?") must come **after** all tool results. This ordering is a hard API requirement, not a style preference — violating it causes API errors that can be difficult to trace.

**Solution**: Always structure tool result messages as: `[tool_result_block_1, tool_result_block_2, ..., text_block]`. Never interleave text before tool results. Validate content array ordering in your tool runner before sending.

### 7. Thin Tool Descriptions

**Problem**: Tools are called with wrong parameters or skipped entirely because the model doesn't understand when or how to use them.

**Why it happens**: Tool descriptions are the model's only guide to tool selection and parameter filling. Anthropic documentation identifies thin descriptions as "the single most important factor in tool performance." A description like "Gets data" tells the model almost nothing. The model must infer use cases, parameter meanings, and edge cases — and will guess wrong.

**Solution**: Write tool descriptions that answer: (1) what this tool does, (2) when to use it vs. similar tools, (3) what each parameter means and its expected format. For parameters with precise formats (dates, enums, coordinates), include examples directly in the parameter description. Test each tool description by asking: "Could the model call this tool correctly from the description alone?"

### 8. Parallel Prompt for Sequential Tool Chains

**Problem**: Prompting the model to "invoke all tools simultaneously" for a sequential workflow causes the model to guess parameter values for downstream tools before upstream results are available.

**Why it happens**: Parallel tool use prompts (e.g., "for maximum efficiency, invoke all relevant tools simultaneously") work well for independent operations. For dependent chains — where Tool B's input is Tool A's output — the model either refuses to call B in parallel or invents its B parameters. Both outcomes break the workflow.

**Solution**: Use parallel tool calls only for genuinely independent operations. For sequential chains, prompt the model to complete one step at a time and wait for results before proceeding. Set `disable_parallel_tool_use: true` in `implementation.llm_agent.parameters` when your workflow is strictly sequential.

### 9. [Additional Pitfalls]

Document common pitfalls based on expected usage. Focus on mistakes that:
- Are easy to make
- Have non-obvious causes
- Can be explained better in narrative than in code alone

---

## Examples (core)

Practical examples demonstrating the agent in action.

### Example 1: [Common Use Case]

**Scenario**: [Description of the situation]

**Input**:
```json
{
  "text": "Long technical document...",
  "max_length": 500
}
```

**Approach**: [How the agent handles it, referencing `<your_agent_name>.json` for data]

**Output**:
```json
{
  "summary": "Concise summary...",
  "key_points": ["Point 1", "Point 2"]
}
```

**Code**: See `<your_agent_name>.json` → `common_patterns` for structured examples

### Example 2: [Edge Case]

**Scenario**: [Description of edge case]

**Approach**: [How the agent handles this unusual situation]

**Code**: See `<your_agent_name>.json` → `error_handling` for failure recovery

### Example 3: [Integration Example]

**Scenario**: [How to integrate with other systems or agents]

**Code**: See `<your_agent_name>.json` → `cross_references` for related agents

---

## Validation and Testing (core)

How to verify the agent is working correctly.

### Quick Validation
1. Run a simple test case: `agent.process(test_input)`
2. Verify output matches expected format
3. Check logs for any errors or warnings

### Comprehensive Validation
For detailed validation procedures, see `<your_agent_name>.json` → `validation` section.

The validation section in the JSON includes:
- Pre-run checklist (dependencies, config, credentials)
- Post-run checklist (output format, values, side effects)
- Success criteria (what "correct" looks like)
- Test cases with expected outputs
- Tolerance levels for numeric/string/structural comparisons

### Automated Testing
If the agent has automated tests, see `<your_agent_name>.json` → `tests` section for commands to run.

---

## Performance Considerations (optional)
Include only if performance is a goal. Otherwise omit.

## Operational Guidance (optional)
Include only if this helps distinguish when to use/not use the agent. Otherwise omit.

## Troubleshooting (optional)
Keep brief; link to JSON error_handling. Omit if not needed.

## Monitoring and Observability (optional)
Only for production agents that log/alert. Omit for prototypes.

---

## Resources and References

### Agent Files
- **`<your_agent_name>.json`**: Structured data, code examples, and operational details
- **`<path/to/implementation>`**: Source code implementation (if applicable)
- **`<comprehensive_guide>.md`**: Full narrative guide (if applicable)

### Related Agents
See `<your_agent_name>.json` → `cross_references.related_agents` for agents that:
- Use this agent's output
- Complement this agent's functionality
- Provide alternative approaches

### External Documentation
- [Official library/tool documentation]
- [API reference]
- [Research papers or technical specifications]

### How to Use This Documentation System
1. **Start here** (.md) for conceptual understanding and "why"
2. **Use JSON** for implementation details, code examples, and "what"
3. **Reference source code** for deep implementation dive (if applicable)
4. **Check related agents** for ecosystem context

---

## Contributing and Maintenance

### Updating This Agent

**When to update the JSON**:
- Adding new code patterns or examples
- Adding new validation test cases
- Changing structured data or mappings
- Adding new operational procedures
- Updating configuration parameters

**When to update the MD**:
- Clarifying concepts or principles
- Adding new pitfall explanations
- Updating examples with new scenarios
- Improving educational narrative
- Updating troubleshooting guidance

### Version History
See `<your_agent_name>.json` → `changelog` for detailed version history.

---

## Quick Reference Card

A one-page summary for experienced users:

| Aspect | Value |
|--------|-------|
| **Purpose** | [One sentence] |
| **Input** | [What it takes] |
| **Output** | [What it produces] |
| **Agent Type** | [class_based\|workflow\|llm_agent\|etc.] |
| **Complexity** | [simple\|standard\|complex] |
| **Key Files** | `<your_agent_name>.json`, `<your_agent_name>.md` |
| **Quickstart** | `agent = Agent.from_config('agent.json'); result = agent.process(input)` |
| **Common Pitfall** | [#1 mistake to avoid] |
| **Dependencies** | [Key packages or APIs] |

For detailed information, see sections above and `<your_agent_name>.json`.
