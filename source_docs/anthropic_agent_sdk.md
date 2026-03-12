---
platform: Anthropic
label: Claude Agent SDK (formerly Claude Code SDK)
source_url: https://docs.anthropic.com/en/docs/claude-code/sdk
last_fetched: 2026-03-11
fetch_status: success
notes: Now redirects to platform.claude.com/docs/en/agent-sdk/overview. Covers query(), hooks, subagents, MCP, sessions, permissions, compaction.
---

## Agent SDK Overview

The Claude Code SDK has been renamed to the **Claude Agent SDK**. Build AI agents that autonomously read files, run commands, search the web, edit code, and more. Gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript.

---

## Install & Quickstart

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk

# Set API key
export ANTHROPIC_API_KEY=your-api-key
```

**Python quickstart:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

**TypeScript quickstart:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix the bug in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

---

## Agent SDK vs Client SDK

**Key architectural difference:**

```python
# Client SDK: You implement the tool loop
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

**When to use each:**

| Use case | Best choice |
|----------|-------------|
| Interactive development | CLI |
| CI/CD pipelines | SDK |
| Custom applications | SDK |
| One-off tasks | CLI |
| Production automation | SDK |
| Need per-step control/gating | Client SDK (manual loop) |
| Long-running autonomous tasks | Agent SDK (auto loop + compaction) |

---

## Built-in Tools

| Tool | What it does |
|------|--------------|
| Read | Read any file in the working directory |
| Write | Create new files |
| Edit | Make precise edits to existing files |
| Bash | Run terminal commands, scripts, git operations |
| Glob | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| Grep | Search file contents with regex |
| WebSearch | Search the web for current information |
| WebFetch | Fetch and parse web page content |
| AskUserQuestion | Ask the user clarifying questions with multiple choice options |

---

## Permissions — Tool Allowlists

Control exactly which tools your agent can use:

```python
# Read-only agent that can analyze but not modify code
async for message in query(
    prompt="Review this code for best practices",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```

`allowed_tools` pre-approves listed tools. Unlisted tools require human confirmation or are blocked.

---

## Sessions — Context Across Multiple Exchanges

Capture `session_id` from the first query, then pass `resume=session_id` to continue with full context:

```python
session_id = None

# First query: capture the session ID
async for message in query(
    prompt="Read the authentication module",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"]),
):
    if hasattr(message, "subtype") and message.subtype == "init":
        session_id = message.session_id

# Resume with full context from the first query
async for message in query(
    prompt="Now find all places that call it",  # "it" = auth module from prior session
    options=ClaudeAgentOptions(resume=session_id),
):
    if hasattr(message, "result"):
        print(message.result)
```

---

## Hooks — Lifecycle Events

Run custom code at key points in the agent lifecycle.

Available hooks: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`

**Python example — audit log of all file changes:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher
from datetime import datetime

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

async for message in query(
    prompt="Refactor utils.py to improve readability",
    options=ClaudeAgentOptions(
        permission_mode="acceptEdits",
        hooks={
            "PostToolUse": [
                HookMatcher(matcher="Edit|Write", hooks=[log_file_change])
            ]
        },
    ),
):
    pass
```

---

## Subagents — Spawn Specialized Child Agents

Define custom agents with specialized instructions. Include `Agent` in `allowedTools`.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Use the code-reviewer agent to review this codebase",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Agent"],
        agents={
            "code-reviewer": AgentDefinition(
                description="Expert code reviewer for quality and security reviews.",
                prompt="Analyze code quality and suggest improvements.",
                tools=["Read", "Glob", "Grep"],
            )
        },
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```

Messages from within a subagent's context include a `parent_tool_use_id` field for tracking which messages belong to which subagent execution.

---

## MCP — Connect to External Systems

```python
async for message in query(
    prompt="Open example.com and describe what you see",
    options=ClaudeAgentOptions(
        mcp_servers={
            "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
        }
    ),
):
    pass
```

---

## Context Compaction

The tool runner supports **automatic compaction**: generates summaries when token usage exceeds a threshold. Allows long-running agentic tasks to continue beyond context window limits without losing progress.

---

## Authentication Options

Beyond direct API key, the SDK supports:
- **Amazon Bedrock**: `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Google Vertex AI**: `CLAUDE_CODE_USE_VERTEX=1` + Google Cloud credentials
- **Microsoft Azure**: `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials

Note: Do not offer claude.ai login or rate limits for third-party products built on the Agent SDK.

---

## Filesystem-Based Configuration Features

Set `setting_sources=["project"]` to enable:

| Feature | Description | Location |
|---------|-------------|----------|
| Skills | Specialized capabilities in Markdown | `.claude/skills/SKILL.md` |
| Slash commands | Custom commands for common tasks | `.claude/commands/*.md` |
| Memory | Project context and instructions | `CLAUDE.md` or `.claude/CLAUDE.md` |
| Plugins | Extend with custom commands, agents, MCP | Programmatic via `plugins` option |

---

## Branding Guidelines

**Allowed:**
- "Claude Agent" (preferred for dropdown menus)
- "{YourAgentName} Powered by Claude"

**Not permitted:**
- "Claude Code" or "Claude Code Agent"
- Claude Code-branded ASCII art
