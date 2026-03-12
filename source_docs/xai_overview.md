---
platform: xAI
label: Grok API — Overview, Function Calling, Models
source_url: https://docs.x.ai/docs/overview
last_fetched: 2026-03-11
fetch_status: partial
fetch_error: Main overview page had minimal content. Supplemented with quickstart, function calling, and models pages.
notes: Covers function calling, tool_choice, parallel tool calls, Pydantic tool schemas, model tiers, pricing.
---

## xAI API Overview

The xAI API provides access to Grok models with support for text, image analysis, function calling, structured outputs, and built-in agentic tools (web search, code execution, file attachments).

### Authentication

- Sign up at accounts.x.ai
- Load credits before API usage
- Generate API keys via xAI Console → API Keys page
- Export via environment variable or `.env` file

### SDK Installation

```bash
# Python xAI SDK
pip install xai-sdk

# Python OpenAI compatibility
pip install openai

# JavaScript AI SDK
npm install ai @ai-sdk/xai zod

# JavaScript OpenAI compatibility
npm install openai
```

---

## Function Calling

### How It Works

1. Define tools with a name, description, and JSON schema for parameters
2. Include tools in your request
3. Model returns a `tool_call` when it needs external data
4. Execute the function locally and return the result
5. Model continues with your result

### Tool Choice Options

| Value | Behavior |
|-------|----------|
| `"auto"` | Model decides whether to call a tool (default) |
| `"required"` | Model must call at least one tool |
| `"none"` | Disable tool calling |
| `{"type": "function", "function": {"name": "..."}}` | Force a specific tool |

### Parallel Function Calling

By default, parallel function calling is enabled — the model can request multiple tool calls in a single response. Process all before continuing.

Disable with `parallel_tool_calls: false`.

### Tool Schema Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (max 200 tools per request) |
| `description` | Yes | What the tool does — helps the model decide when to use it |
| `parameters` | Yes | JSON Schema defining function inputs |

### Defining Tools with Pydantic (Type-safe schemas)

```python
tools = [
    tool(
        name="get_temperature",
        description="Get current temperature for a location",
        parameters={...},
    ),
]
```

### Combining with Built-in Tools

"Function calling works alongside built-in agentic tools. The model can use web search, then call your custom function." Built-in tools execute on xAI servers; custom tools return to you for handling.

---

## Built-in Agentic Tools (xAI server-side)

| Tool | Cost per 1,000 calls |
|------|----------------------|
| Web Search | $5 |
| X Search | $5 |
| Code Execution | $5 |
| File Attachments | $10 |
| Collections Search | $2.50 |

---

## Models

### Advanced Models (grok-4.20 series)

- Text and image inputs
- Functions, structured outputs, reasoning
- 2,000,000 token context windows
- Pricing: $2.00 input / $6.00 output (per 1M tokens)

### Fast Models (grok-4-1 series)

- Similar capabilities, reduced pricing: $0.20 input / $0.50 output

### Code Models

- grok-code-fast-1
- Text-only inputs
- 256,000 token context

### Image & Video Generation

- Basic image: $0.02/image
- Professional image: $0.07/image
- Video: $0.050/second

### Voice API

- Real-time Voice Agent: $0.05/minute ($3.00/hour)
- Text-to-Speech: $4.20/1M characters (beta)

### Batch API

- 50% off standard rates
- Typical 24-hour processing

---

## Key Requirements

- Maximum image size: 20MiB (JPG/PNG)
- Knowledge cutoff: November 2024
- For latest features, use model aliases like `<modelname>-latest`
