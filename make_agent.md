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

### 3. [Additional Pitfalls]

Document 3-5 common pitfalls based on expected usage. Focus on mistakes that:
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
