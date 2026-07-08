---
name: MCP Integration Patterns
description: Cross-platform patterns for integrating Model Context Protocol (MCP) servers with AI agents
version: "1.0"
created: 2026-07-06
platforms: [Anthropic, Google, OpenAI, xAI]
---

# MCP Integration Patterns

## What is MCP?

The **Model Context Protocol (MCP)** is an open standard that standardizes how applications expose tools and context to language models. Think of MCP as a USB-C port for AI applications — it provides a standardized way to connect AI models to different data sources and tools.

**Key concepts**:
- **MCP Server**: A service that exposes tools, data sources, or prompts via the MCP protocol
- **MCP Client**: An AI agent or application that consumes tools from MCP servers
- **Transports**: How client and server communicate (stdio, HTTP+SSE, Streamable HTTP)
- **Tools**: Functions the server exposes for the model to call
- **Prompts**: Dynamic instruction templates the server can provide
- **Resources**: Data sources the server makes available

**Benefits**:
- **Reusability**: Write once, use across platforms (OpenAI, Anthropic, Google, etc.)
- **Standardization**: Consistent tool integration pattern
- **Ecosystem**: Growing library of public MCP servers (filesystem, databases, APIs)
- **Decoupling**: Tool implementation separate from agent logic

---

## Platform Comparison

| Platform | MCP Support | Integration Method | Transports | When to Use |
|----------|-------------|-------------------|------------|-------------|
| **OpenAI** | ✅ Full | Local + Hosted | stdio, HTTP+SSE, Streamable HTTP, Hosted | Most flexible; supports all transports; best for MCP-heavy workflows |
| **Anthropic** | ✅ Managed Agents | MCP Connector | Hosted connector | Simplest integration; fully managed; best for quick MCP setup |
| **Google** | ✅ Remote only | Remote MCP servers | Streamable HTTP | Lightweight; remote servers only; best for public MCP servers |
| **xAI** | ⚠️ Limited | (No direct MCP support documented) | N/A | Use platform-specific tools instead |

---

## OpenAI: Comprehensive MCP Support

**Status**: Full MCP support across all transports

### Integration Options

OpenAI provides the most comprehensive MCP support with four integration methods:

#### 1. Hosted MCP Tools

**What**: OpenAI's Responses API calls MCP servers on the model's behalf. Zero client-side execution.

**Best for**: Publicly accessible MCP servers, minimal infrastructure overhead

**Pattern**:
```python
from agents import Agent, HostedMCPTool, Runner

agent = Agent(
    name="Assistant",
    instructions="Use the DeepWiki MCP server to inspect repositories.",
    tools=[
        HostedMCPTool(
            tool_config={
                "type": "mcp",
                "server_label": "deepwiki",
                "server_url": "https://mcp.deepwiki.com/mcp",
                "require_approval": "never",
            }
        )
    ],
)

result = await Runner.run(
    agent,
    "Which language is openai/openai-agents-python written in?",
)
```

**Key capabilities**:
- Zero client infrastructure (OpenAI handles execution)
- Streaming results
- Approval policies (`"always"`, `"never"`, per-tool map)
- Connector-backed servers (Google Calendar, etc.)

**Limitations**:
- Server must be publicly accessible
- OpenAI Responses API only
- No stdio transport

#### 2. Streamable HTTP MCP Servers

**What**: Local SDK connects to MCP servers over streamable HTTP. Full control over transport.

**Best for**: Internal MCP servers, custom infrastructure, low latency

**Pattern**:
```python
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="Streamable HTTP Server",
    params={
        "url": "http://localhost:8000/mcp",
        "headers": {"Authorization": f"Bearer {token}"},
        "timeout": 10,
    },
    cache_tools_list=True,
    max_retry_attempts=3,
) as server:
    agent = Agent(
        name="Assistant",
        instructions="Use MCP tools to answer questions.",
        mcp_servers=[server],
    )
    result = await Runner.run(agent, "Add 7 and 22.")
```

**Key capabilities**:
- Full transport control
- Tool filtering (`tool_filter` parameter)
- Approval policies (`require_approval`)
- Per-call metadata injection (`tool_meta_resolver`)
- Automatic retries
- Tool caching

#### 3. stdio MCP Servers

**What**: SDK spawns MCP server as local subprocess, communicates over stdin/stdout.

**Best for**: CLI-based MCP servers, local development, npm-packaged servers

**Pattern**:
```python
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

samples_dir = Path("./sample_files")

async with MCPServerStdio(
    name="Filesystem Server via npx",
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", str(samples_dir)],
    },
) as server:
    agent = Agent(
        name="Assistant",
        instructions="Use files in sample directory to answer questions.",
        mcp_servers=[server],
    )
    result = await Runner.run(agent, "List files available.")
```

**Key capabilities**:
- Subprocess lifecycle management
- Works with npm-based servers (`npx -y @modelcontextprotocol/server-*`)
- Local filesystem access
- Same approval/filtering as Streamable HTTP

**Common servers**:
- `@modelcontextprotocol/server-filesystem` - File operations
- `@modelcontextprotocol/server-postgres` - PostgreSQL database
- `@modelcontextprotocol/server-github` - GitHub API

#### 4. HTTP with SSE MCP Servers (Deprecated)

**What**: Server-Sent Events transport (legacy)

**Status**: Deprecated by MCP project. Use Streamable HTTP for new integrations.

### Advanced Features

#### Tool Filtering

**Static filtering** (allow/block lists):
```python
from agents.mcp import create_static_tool_filter

server = MCPServerStdio(
    params={...},
    tool_filter=create_static_tool_filter(
        allowed_tool_names=["read_file", "write_file"],
    ),
)
```

**Dynamic filtering** (context-aware):
```python
from agents.mcp import ToolFilterContext

async def context_aware_filter(context: ToolFilterContext, tool) -> bool:
    if context.agent.name == "ReadOnly" and tool.name.startswith("write_"):
        return False
    return True

server = MCPServerStdio(
    params={...},
    tool_filter=context_aware_filter,
)
```

#### Approval Policies

**Per-tool approval**:
```python
server = MCPServerStreamableHttp(
    name="Filesystem MCP",
    params={"url": "http://localhost:8000/mcp"},
    require_approval={"always": {"tool_names": ["delete_file"]}},
)
```

**Programmatic approval**:
```python
from agents import MCPToolApprovalFunctionResult, MCPToolApprovalRequest

def approve_tool(request: MCPToolApprovalRequest) -> MCPToolApprovalFunctionResult:
    if request.data.name in SAFE_TOOLS:
        return {"approve": True}
    return {"approve": False, "reason": "Escalate to human"}

agent = Agent(
    tools=[HostedMCPTool(tool_config={...}, on_approval_request=approve_tool)],
)
```

#### MCP Server Manager

**Multi-server management**:
```python
from agents.mcp import MCPServerManager

servers = [
    MCPServerStreamableHttp(name="calendar", params={"url": "..."}),
    MCPServerStreamableHttp(name="docs", params={"url": "..."}),
]

async with MCPServerManager(servers) as manager:
    agent = Agent(
        name="Assistant",
        mcp_servers=manager.active_servers,  # Only successfully connected
    )
```

---

## Anthropic: MCP Connector for Managed Agents

**Status**: MCP Connector for Managed Agents (Beta: `managed-agents-2026-04-01`)

### Integration Pattern

Anthropic uses a **connector-based** approach. MCP servers are registered as external connectors, and the managed agent runtime handles execution.

**Pattern**:
```python
from anthropic import Anthropic

client = Anthropic()

# Create agent with MCP connector
agent = client.beta.agents.create(
    name="MCP-Enabled Agent",
    model={"id": "claude-sonnet-4-5"},
    system="You are a helpful assistant with access to external tools.",
    tools=[
        {"type": "agent_toolset_20260401"},  # Built-in tools
        {
            "type": "mcp_connector",  # MCP server integration
            "server_url": "https://your-mcp-server.com/mcp",
            "permission_policy": "auto_approve",  # or "require_approval"
        },
    ],
)

# Create environment and session
environment = client.beta.environments.create(
    name="mcp-env",
    config={"type": "cloud", "networking": {"type": "unrestricted"}},
)

session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
)

# Stream events
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{
            "type": "user.message",
            "content": [{"type": "text", "text": "Use MCP tools to..."}],
        }],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                print(event.content)
            case "session.status_idle":
                break
```

**Key capabilities**:
- Fully managed execution (no client-side MCP setup)
- Permission policies (`auto_approve`, `require_approval`)
- Works with cloud sandboxes
- Server-side event streaming

**Limitations**:
- Connector-based only (no stdio or local servers)
- MCP server must be publicly accessible
- Beta stability

**Documentation**: See `source_docs/anthropic_managed_agents_tools.md` for full MCP connector reference.

---

## Google: Remote MCP Servers

**Status**: Remote MCP servers via Streamable HTTP

### Integration Pattern

Google supports **remote MCP servers only** (no stdio or local servers). Register MCP servers in the `tools` array.

**Antigravity Agent**:
```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Use MCP tools to analyze this data.",
    tools=[
        {"type": "code_execution"},  # Built-in tools
        {"type": "google_search"},
        {
            "type": "mcp_server",  # Remote MCP server
            "name": "DataAnalyzer",
            "url": "https://your-mcp-server.com/mcp",
        },
    ],
    environment="remote",
)
```

**Deep Research Agent**:
```python
interaction = client.interactions.create(
    agent="deep-research-preview-04-2026",
    input="Research topic using external data sources.",
    tools=[
        {
            "type": "mcp_server",
            "name": "ExternalKnowledgeBase",
            "url": "https://knowledge-mcp.example.com/mcp",
        },
    ],
    environment="remote",
)
```

**Key capabilities**:
- Simple registration (just URL + name)
- Works with Antigravity and Deep Research agents
- Streamable HTTP transport

**Limitations**:
- Remote servers only (no stdio)
- No built-in approval policies
- No tool filtering at platform level

---

## Public MCP Servers

**Gemini API Docs MCP** (`gemini-api-docs-mcp.dev`):
- **Purpose**: Access Gemini API documentation as MCP tools
- **Tools**: Search docs, get API reference, code examples
- **URL**: `https://gemini-api-docs-mcp.dev/mcp`
- **Platforms**: All (public HTTP endpoint)

**DeepWiki MCP** (`mcp.deepwiki.com`):
- **Purpose**: Repository analysis, code search, documentation
- **Tools**: Read repo structure, search code, ask questions
- **URL**: `https://mcp.deepwiki.com/mcp`
- **Platforms**: OpenAI Hosted, Google, custom clients

**@modelcontextprotocol/server-filesystem** (stdio):
- **Purpose**: Local file operations
- **Tools**: `read_file`, `write_file`, `list_directory`, `search_files`
- **Installation**: `npx -y @modelcontextprotocol/server-filesystem <directory>`
- **Platforms**: OpenAI stdio, custom clients

**@modelcontextprotocol/server-postgres** (stdio):
- **Purpose**: PostgreSQL database access
- **Tools**: Query, schema inspection, data operations
- **Installation**: `npx -y @modelcontextprotocol/server-postgres <connection-string>`
- **Platforms**: OpenAI stdio, custom clients

**@modelcontextprotocol/server-github** (stdio):
- **Purpose**: GitHub API operations
- **Tools**: Repo operations, issues, PRs, commits
- **Installation**: `npx -y @modelcontextprotocol/server-github`
- **Platforms**: OpenAI stdio, custom clients

---

## Custom MCP Server Patterns

### Minimal Python MCP Server (Streamable HTTP)

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ToolRequest(BaseModel):
    name: str
    arguments: dict

@app.post("/mcp")
async def mcp_endpoint(request: ToolRequest):
    if request.name == "get_weather":
        location = request.arguments["location"]
        # Fetch weather data
        return {"temperature": 72, "conditions": "Sunny", "location": location}

    return {"error": f"Unknown tool: {request.name}"}

@app.get("/mcp/tools")
async def list_tools():
    return {
        "tools": [
            {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                    },
                    "required": ["location"],
                },
            }
        ]
    }
```

Run: `uvicorn server:app --host 0.0.0.0 --port 8000`

**Connect from OpenAI SDK**:
```python
async with MCPServerStreamableHttp(
    name="Weather MCP",
    params={"url": "http://localhost:8000/mcp"},
) as server:
    agent = Agent(mcp_servers=[server])
```

### Minimal stdio MCP Server (Node.js)

```javascript
#!/usr/bin/env node
const readline = require('readline');

const tools = [
  {
    name: "calculate_sum",
    description: "Add two numbers",
    input_schema: {
      type: "object",
      properties: {
        a: { type: "number" },
        b: { type: "number" },
      },
      required: ["a", "b"],
    },
  },
];

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

rl.on('line', (line) => {
  const request = JSON.parse(line);

  if (request.method === "tools/list") {
    console.log(JSON.stringify({ tools }));
  } else if (request.method === "tools/call") {
    const { name, arguments: args } = request.params;
    if (name === "calculate_sum") {
      const result = args.a + args.b;
      console.log(JSON.stringify({ content: [{ type: "text", text: `Sum: ${result}` }] }));
    }
  }
});
```

Make executable: `chmod +x mcp-server.js`

**Connect from OpenAI SDK**:
```python
async with MCPServerStdio(
    name="Calculator",
    params={"command": "./mcp-server.js", "args": []},
) as server:
    agent = Agent(mcp_servers=[server])
```

---

## Common Pitfalls

### 1. Using Local Servers on Hosted Platforms

**Problem**: Trying to connect Google Antigravity or Anthropic Managed Agents to `localhost` MCP servers.

**Why it fails**: These platforms execute in cloud sandboxes. `localhost` refers to the sandbox, not your machine.

**Fix**: Use publicly accessible MCP servers or deploy your MCP server to a reachable endpoint.

### 2. Forgetting to Enable MCP Tools

**Problem**: MCP server connected, but agent never calls tools.

**Why it fails**: MCP tools must be explicitly listed (OpenAI) or the toolset must include MCP connector (Anthropic).

**Fix**:
- **OpenAI**: Add server to `mcp_servers` list
- **Anthropic**: Include `{"type": "mcp_connector"}` in agent tools
- **Google**: Add `{"type": "mcp_server"}` to tools array

### 3. Tool Name Collisions

**Problem**: Multiple MCP servers expose tools with the same name. Agent calls the wrong one.

**Why it happens**: Default behavior doesn't namespace tools by server.

**Fix (OpenAI)**: Set `mcp_config["include_server_in_tool_names"] = True`. Tools become `servername_toolname`.

### 4. No Tool Descriptions

**Problem**: MCP server exposes tools with minimal or no descriptions. Agent uses them incorrectly.

**Why it happens**: MCP spec doesn't enforce description quality.

**Fix**: Improve MCP server tool descriptions. Follow Anthropic's tool description best practices: 3-4 sentences, explain what/when/how, call out limitations.

### 5. Missing Approval Policies for Destructive Tools

**Problem**: Agent calls destructive MCP tools (`delete_file`, `drop_table`) without human approval.

**Why it happens**: Default is auto-approve for most platforms.

**Fix**:
- **OpenAI**: Set `require_approval` on server or per-tool
- **Anthropic**: Use `permission_policy: "require_approval"` in MCP connector
- **Google**: Implement approval in application logic (no platform-level support)

---

## Best Practices

### 1. Start with Public MCP Servers

**Why**: Fastest path to value. No server implementation needed.

**Examples**: DeepWiki MCP for code repos, Gemini Docs MCP for API documentation.

**Pattern**: Use OpenAI Hosted MCP or Google remote MCP servers.

### 2. Use Approval Policies for Destructive Operations

**Why**: Prevents unintended data loss or security breaches.

**Classify tools**:
- **Always auto-approve**: Read operations (`read_file`, `list_directory`, `query_read_only`)
- **Always require approval**: Destructive operations (`delete_file`, `drop_table`, `execute_code`)
- **Context-dependent**: Write operations (approve based on agent role, user identity)

### 3. Filter Tools to Minimum Needed

**Why**: Reduces model confusion, improves routing accuracy, lowers latency.

**Pattern**: Use `tool_filter` (OpenAI) or disable unwanted tools (Anthropic) rather than exposing full MCP server.

### 4. Cache Tool Lists for Remote Servers

**Why**: Remote `list_tools()` calls add latency. Caching reduces overhead.

**Pattern (OpenAI)**: Set `cache_tools_list=True` on `MCPServerStreamableHttp`.

**Invalidate when**: MCP server deployment changes tool definitions.

### 5. Write Detailed Tool Descriptions

**Why**: Tool description quality is the #1 factor in agent tool selection accuracy.

**Template**:
```
{tool_name}: {what it does}. Use when {conditions}. Do NOT use when {anti-patterns}. Parameters: {param explanations with examples}.
```

**Example**:
```
search_codebase: Searches code files for regex patterns across entire repository. Use when user asks to find functions, classes, or patterns. Do NOT use for reading specific files (use read_file instead). Parameters: pattern (regex, case-sensitive), file_glob (optional filter like "*.py").
```

### 6. Test MCP Integration Independently

**Why**: Debugging agent + MCP integration failures is harder than testing MCP server alone.

**Pattern**:
1. Test MCP server with `curl` or MCP client CLI first
2. Verify `list_tools()` returns expected schema
3. Test `call_tool()` with sample inputs
4. Then integrate with agent

**OpenAI test pattern**:
```python
async with MCPServerStreamableHttp(params={"url": "..."}) as server:
    tools = await server.list_tools()
    print(tools)  # Verify tool definitions

    result = await server.call_tool("tool_name", {"arg": "value"})
    print(result)  # Verify tool execution
```

---

## Decision Matrix

| Scenario | Recommended Platform + Transport |
|----------|----------------------------------|
| **Public MCP server, minimal setup** | Google Antigravity remote MCP or OpenAI Hosted MCP |
| **Custom MCP server, full control** | OpenAI Streamable HTTP |
| **npm-based MCP server (filesystem, postgres, github)** | OpenAI stdio |
| **Fully managed agent with MCP** | Anthropic Managed Agents MCP Connector |
| **Multi-transport flexibility** | OpenAI (supports all transports) |
| **Approval policies critical** | OpenAI (most granular) or Anthropic (managed) |
| **Tool filtering required** | OpenAI (static + dynamic filtering) |
| **Rapid prototyping** | Google Antigravity (inline everything) |

---

## Resources

**MCP Specification**:
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official spec and design docs

**Platform Documentation**:
- **OpenAI**: `source_docs/openai_mcp.md` - Comprehensive MCP guide
- **Anthropic**: `source_docs/anthropic_managed_agents_tools.md` - MCP connector reference
- **Google Antigravity**: `source_docs/google_antigravity_agent.md` - Remote MCP servers
- **Google Deep Research**: `source_docs/google_deep_research_agent.md` - MCP integration

**Public MCP Servers**:
- [MCP Servers Registry](https://github.com/modelcontextprotocol/servers) - Official server list
- Gemini Docs MCP: `https://gemini-api-docs-mcp.dev`
- DeepWiki MCP: `https://mcp.deepwiki.com`

**Examples**:
- OpenAI SDK: `examples/mcp/` and `examples/hosted_mcp/`
- Google ADK: Coding agents with MCP servers
- Anthropic: MCP connector quickstart (coming soon)

---

**Version**: 1.0
**Last Updated**: 2026-07-06
**Covers**: OpenAI Agents SDK (latest), Anthropic Managed Agents (Beta), Google Gemini API (GA), xAI Grok (4.20)
