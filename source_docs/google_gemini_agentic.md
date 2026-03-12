---
platform: Google
label: Gemini API Agentic Capabilities (Function Calling + Thinking)
source_url: https://ai.google.dev/gemini-api/docs/agentic-capabilities
last_fetched: 2026-03-11
fetch_status: partial
fetch_error: Original URL 404'd. Content retrieved from closely related function calling and thinking documentation pages.
notes: Covers function calling modes, parallel/compositional calling, best practices, thinking models, MCP integration.
---

## Function Calling with the Gemini API

### Core Concept

Function calling enables models to connect with external tools and APIs by determining when to invoke specific functions and supplying necessary parameters, rather than generating text responses.

### Three Primary Use Cases

1. **Augment Knowledge** — Access external databases, APIs, and knowledge bases
2. **Extend Capabilities** — Use external tools for computations beyond model limitations
3. **Take Actions** — Interact with external systems via APIs (scheduling, invoicing, etc.)

---

## How Function Calling Works (4 Steps)

1. Define function declarations (name, parameters, purpose)
2. Send user prompt with function declarations to the model
3. **Model suggests but does not execute functions** — you execute on your side
4. Send function results back to the model for a user-friendly response

---

## Function Declaration Parameters

Each declaration includes:
- **name** — Unique, descriptive identifier without spaces or special characters
- **description** — Clear explanation of purpose and capabilities
- **parameters** — Input specifications with type, description, optional enum values
- **required** — Array of mandatory parameter names

---

## Function Calling Modes

| Mode | Behavior |
|------|----------|
| `AUTO` | Default — model decides whether to generate text or suggest function calls |
| `ANY` | Model must predict a function call; optionally restricted to specified functions |
| `NONE` | Function calling disabled |
| `VALIDATED` | Model predicts either function calls or text with schema adherence |

---

## Key Capabilities

**Parallel Function Calling** — Execute multiple independent functions simultaneously in a single turn

**Compositional Function Calling** — Chain multiple function calls sequentially where outputs feed into subsequent calls

**Automatic Function Calling (Python SDK only)** — SDK converts Python functions to declarations, handles execution, and manages response cycles automatically

---

## Best Practices

"Be extremely clear and specific in your descriptions. The model relies on these to choose the correct function and provide appropriate arguments."

- Use descriptive, specific function names (underscores or camelCase preferred)
- Provide clear parameter descriptions with examples and constraints
- Use enums for fixed value sets rather than descriptions alone
- **Limit active tool sets to 10–20 functions for optimal performance**
- Employ low temperature settings (e.g., 0) for deterministic function calls
  - **Exception**: For Gemini 3 models, keep temperature at its default value of 1.0
- Validate function calls with significant consequences before execution
- Check `finishReason` in responses to handle failed function calls
- Implement robust error handling with informative messages

---

## Multimodal Function Responses

Gemini 3 series models support multimodal content in function response parts:
- Supported MIME types: images (PNG, JPEG, WebP) and documents (PDF, plain text)

---

## MCP Integration

Built-in Model Context Protocol support via Python and JavaScript SDKs — reduces boilerplate for external tool integration.

---

## Supported Models for Function Calling

- Gemini 3.1 Pro Preview
- Gemini 3 Flash Preview
- Gemini 2.5 series (Pro, Flash, Flash-Lite)
- Gemini 2.0 Flash

All support parallel and compositional function calling.

---

## Gemini Thinking

### Thought Summaries

"Thought summaries are summarized versions of the model's raw thoughts" — provide insights into reasoning. Enable with `includeThoughts: true`. Works with both streaming and non-streaming requests.

### Controlling Thinking

**Thinking Levels (Gemini 3 models):**
- `minimal` — Minimizes latency for chat or high throughput applications
- `low`, `medium`, `high`

**Thinking Budgets (Gemini 2.5 series):**
- Set specific token counts (range varies by model)
- Setting to 0 disables thinking
- Setting to -1 enables dynamic thinking

### Thought Signatures

Encrypted representations of the model's internal thought process for maintaining context across multi-turn conversations. The GenAI SDK handles this automatically.

### Best Practices for Thinking

- Review reasoning by analyzing thought summaries when responses don't match expectations
- Constrain thinking amounts in prompts for lengthy outputs
- Task complexity alignment: use thinking levels appropriately (off for simple tasks, maximum for complex coding/math)
