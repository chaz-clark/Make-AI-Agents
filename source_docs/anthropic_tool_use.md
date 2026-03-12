---
platform: Anthropic
label: Tool Use with Claude
source_url: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
last_fetched: 2026-03-11
fetch_status: success
notes: Covers client tools, server tools, MCP tools, parallel/sequential tool use, tool_choice, strict mode, tool runner (beta)
---

## Tool use with Claude

Claude is capable of interacting with tools and functions, allowing you to extend Claude's capabilities to perform a wider variety of tasks. Each tool defines a contract: you specify what operations are available and what they return; Claude decides when and how to call them.

**Tip — Guarantee schema conformance with strict tool use:** Add `strict: true` to your tool definitions to ensure Claude's tool calls always match your schema exactly, eliminating type mismatches or missing fields. Perfect for production agents where invalid tool parameters would cause failures.

---

## Two Types of Tools

**Client tools** — Execute on your systems:
- User-defined custom tools you create and implement
- Anthropic-defined tools like computer use and text editor that require client implementation

**Server tools** — Execute on Anthropic's servers:
- Web search, web fetch tools
- Must be specified in the API request but don't require client implementation
- Versioned types (e.g., `web_search_20250305`) ensure compatibility across model versions

---

## Client Tool — 4-Step Integration

1. **Provide tools + prompt**: Define client tools with names, descriptions, and input schemas
2. **Claude decides**: If helpful, Claude constructs a properly formatted tool use request; API response has `stop_reason: "tool_use"`
3. **Execute + return**: Extract tool name/input, run on your system, return results via `tool_result` content block
4. **Claude formulates response**: Claude analyzes tool results to craft final response

Note: Steps 3 and 4 are optional — Claude's tool use request alone may be all you need.

---

## Server Tool — `pause_turn` Handling

The server-side sampling loop has a default limit of 10 iterations. If Claude reaches this limit:
- API returns `stop_reason: "pause_turn"`
- **Action**: Continue the conversation by sending the response back as a new user message to let Claude finish

---

## MCP Tools

If using the Model Context Protocol, convert MCP tools to Claude format:
- Rename `inputSchema` → `input_schema`

```python
from mcp import ClientSession

async def get_claude_tools(mcp_session: ClientSession):
    mcp_tools = await mcp_session.list_tools()
    claude_tools = []
    for tool in mcp_tools.tools:
        claude_tools.append({
            "name": tool.name,
            "description": tool.description or "",
            "input_schema": tool.inputSchema,  # Rename inputSchema to input_schema
        })
    return claude_tools
```

---

## Tool Definition Schema

| Parameter | Description |
|-----------|-------------|
| `name` | Must match `^[a-zA-Z0-9_-]{1,64}$` |
| `description` | Detailed plaintext: what it does, when to use, how parameters affect behavior, caveats |
| `input_schema` | JSON Schema object defining expected parameters |
| `input_examples` | (Optional) Array of example input objects for complex tools |
| `strict` | (Optional) `true` for guaranteed schema validation on inputs |

---

## Best Practices for Tool Definitions

**This is the single most important factor in tool performance.**

- **Provide extremely detailed descriptions** — at least 3–4 sentences per tool. Include: what it does, when to use it (and when NOT to), what each parameter means and how it affects behavior, important caveats and limitations
- **Consolidate related operations into fewer tools** — Rather than `create_pr`, `review_pr`, `merge_pr`, use one `pr_manager` tool with an `action` parameter. Fewer, more capable tools reduce selection ambiguity
- **Use meaningful namespacing in tool names** — Prefix with service name when tools span multiple services (e.g., `github_list_prs`, `slack_send_message`)
- **Design tool responses to return only high-signal information** — Return semantic, stable identifiers (slugs, UUIDs). Include only fields Claude needs to reason about next steps. Bloated responses waste context
- **Use `input_examples` for complex tools** — Especially useful for nested objects or format-sensitive parameters

---

## Controlling Tool Use

### tool_choice options

| Value | Behavior |
|-------|----------|
| `auto` | Claude decides whether to call any tool (default) |
| `any` | Claude must use one of the provided tools |
| `tool` | Forces Claude to always use a specific tool |
| `none` | Prevents Claude from using any tools |

Note: When `tool_choice` is `any` or `tool`, the API prefills the assistant message — Claude will not emit natural language before `tool_use` blocks.

### Parallel Tool Use

Claude can call multiple tools in parallel within a single response. All `tool_use` blocks appear in a single assistant message; all corresponding `tool_result` blocks must be in the subsequent user message.

**Disable parallel tool use:**
- Set `disable_parallel_tool_use: true` with `tool_choice: auto` → Claude uses **at most one** tool
- Set `disable_parallel_tool_use: true` with `tool_choice: any/tool` → Claude uses **exactly one** tool

**Prompt to maximize parallel tool use (Claude 4 models):**
```
For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
```

**Stronger parallel tool use prompt:**
```xml
<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially. Prioritize calling tools in parallel whenever possible.
</use_parallel_tool_calls>
```

Warning: Claude Sonnet 3.7 may be less likely to make parallel tool calls. Use Claude 4 models for improved parallel tool calling.

---

## Sequential Tool Chaining

Some tasks require calling multiple tools in sequence, using the output of one as input to the next. If prompted to call all at once, Claude may guess parameters for downstream tools.

**Pattern**: Let Claude call Tool A first, receive the result, then call Tool B with the actual result.

---

## Chain-of-Thought Prompt for Tool Selection

For Sonnet/Haiku models that may call tools prematurely, use this system prompt to trigger analysis first:

```
Answer the user's request using relevant tools (if they are available). Before calling a tool, do some analysis. First, think about which of the provided tools is the relevant tool to answer the user's request. Second, go through each of the required parameters of the relevant tool and determine if the user has directly provided or given enough information to infer a value. If all of the required parameters are present or can be reasonably inferred, proceed with the tool call. BUT, if one of the values for a required parameter is missing, DO NOT invoke the function and instead ask the user to provide the missing parameters. DO NOT ask for more information on optional parameters if it is not provided.
```

---

## Tool Result Formatting

Critical: In the user message containing tool results, `tool_result` blocks must come **FIRST** in the content array. Any text must come **AFTER** all tool results.

```json
// ✅ Correct
{
  "role": "user",
  "content": [
    { "type": "tool_result", "tool_use_id": "toolu_01" },
    { "type": "text", "text": "What should I do next?" }
  ]
}
```

Tool results can include images alongside text.

---

## Tool Runner (Beta)

An out-of-the-box solution for executing tools. Automatically:
- Executes tools when Claude calls them
- Handles the request/response cycle
- Manages conversation state
- Provides type safety and validation
- Supports automatic compaction when token usage exceeds a threshold (allows long-running tasks to continue beyond context window limits)

**Python with `@beta_tool` decorator:**
```python
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a given location.
    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    """
    return json.dumps({"temperature": "20°C", "condition": "Sunny"})

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[get_weather],
    messages=[{"role": "user", "content": "What's the weather like in Paris?"}],
)
```

---

## Model Guidance

- **Claude Opus 4.6**: Best for complex tools and ambiguous queries; handles multiple tools better, seeks clarification when needed
- **Claude Haiku**: Good for straightforward tools, but may infer missing parameters
- **Claude Sonnet 3.7**: Less likely to make parallel tool calls; upgrade to Claude 4 models for better parallel tool calling
