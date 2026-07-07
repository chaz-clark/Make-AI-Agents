---
name: make_managed_agent
description: Generates platform-managed agent specs (Anthropic/Google/OpenAI) with behavioral discipline. For fully managed execution environments with sandboxed tools.
version: "1.0"
created: 2026-07-06
last_updated: 2026-07-07
author: chaz-clark
license: MIT
skill_type: specialized
platforms:
  - Anthropic (Beta: managed-agents-2026-04-01)
  - Google Antigravity (GA)
  - OpenAI Sandbox Agents (Preview)
execution_model: platform_managed
dependencies:
  - make_agent.md
  - knowledge/behavioral_discipline.md
  - knowledge/behavioral_discipline.json
  - source_docs/anthropic_managed_agents_overview.md
  - source_docs/google_managed_agents.md
  - source_docs/openai_sandbox_agents.md
propagates:
  - behavioral_discipline
see_also:
  - make_agent.md
  - knowledge/mcp_integration_patterns.md
metadata:
  make-ai-agents:
    companion_json_not_created: "Uses YAML frontmatter only per 2026-07-07 standard"
---

# Managed Agent Guide

## Agent Instructions
1. Read this for mission, platform selection, quickstart, and pitfalls.
2. Parse `<your_managed_agent_name>.json` for structured data, code/config examples, validation, and operations.
3. **Behavioral Discipline is required.** Consult `knowledge/behavioral_discipline.md` (narrative) and `knowledge/behavioral_discipline.json` (structured rules) when generating any new agent.

---

## Mission (core)

Build autonomous agents that run in fully managed execution environments with sandboxed tools, persistent state, and zero infrastructure overhead.

**What it does**: Creates agents that execute code, manipulate files, browse the web, and perform multi-step tasks in secure, platform-managed sandboxes.

**Why it exists**: Eliminates the need to build agent loops, tool execution layers, sandbox infrastructure, and state persistence. Lets you focus on agent behavior and business logic.

**Who uses it**: Developers building long-running autonomous agents, scheduled workflows, research assistants, coding agents, or any task requiring sandboxed execution.

**Platform options**: Anthropic Claude Managed Agents, Google Antigravity/Deep Research, OpenAI Sandbox Agents.

---

## When to Use Managed Agents (core)

### Use Managed Agents When:

- **Long-running execution**: Tasks that run for minutes or hours with multiple tool calls
- **Sandboxed execution needed**: Code execution, file system access, web browsing required
- **State persistence**: Multi-session workflows where context must be preserved
- **Minimal infrastructure**: You want instant deployment without building agent loops
- **Pre-built tools sufficient**: Bash, files, web, code execution cover your needs
- **Scheduled workflows**: Recurring agent runs on cron schedules

### Use Self-Hosted Instead When:

- **API-only operations**: No code execution or file system needed
- **Custom tools required**: Proprietary integrations, databases, internal APIs
- **Full control needed**: Air-gapped environments, on-prem requirements
- **Lightweight tasks**: Simple request-response patterns under 30 seconds
- **Cost optimization**: High-volume workloads where API calls are cheaper than managed execution

---

## Platform Selection (core)

### Anthropic Claude Managed Agents (Beta: `managed-agents-2026-04-01`)

**Best for**: General-purpose autonomous agents, multi-agent systems, long-running tasks

**Key capabilities**:
- Full agent toolset (bash, files, web search, MCP servers)
- Multi-agent support (shared sandbox, isolated session threads)
- Advisor Tool (executor + advisor model pattern for quality)
- Event-driven streaming (SSE)
- Stateful sessions with server-side history

**Unique strengths**:
- Most mature multi-agent coordination
- Advisor Tool reduces hallucination in tool execution
- Rich event streaming for observability

**Limitations**:
- Beta stability (behaviors may change)
- Not eligible for Zero Data Retention or HIPAA BAA
- Cloud sandbox only (self-hosted sandboxes available but separate config)

**Quickstart pattern**:

```python
from anthropic import Anthropic

client = Anthropic()

# 1. Create agent with pre-built toolset
agent = client.beta.agents.create(
    name="Coding Assistant",
    model={"id": "claude-sonnet-4-5"},
    system="You are a coding assistant. Write clean, well-documented code.",
    tools=[{"type": "agent_toolset_20260401"}],
)

# 2. Create environment (cloud sandbox)
environment = client.beta.environments.create(
    name="quickstart-env",
    config={"type": "cloud", "networking": {"type": "unrestricted"}},
)

# 3. Start session
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Coding task session",
)

# 4. Stream events
with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{
            "type": "user.message",
            "content": [{"type": "text", "text": "Create a Python script that..."}],
        }],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            case "session.status_idle":
                break
```

---

### Google Antigravity Agent (`antigravity-preview-05-2026`)

**Best for**: General-purpose managed agents, single-call workflows, rapid iteration

**Key capabilities**:
- Secure Linux sandbox hosted by Google
- Pre-built tools (code execution, search, URL context)
- AGENTS.md and SKILL.md auto-discovery
- Inline customization (no registration step)
- Server-side state via Interactions API (`previous_interaction_id`)

**Unique strengths**:
- Fastest prototyping (inline everything, no agent.create step)
- Git/GCS source mounting (pull repos directly into sandbox)
- Network allowlisting with credential injection
- Fork-from-environment pattern (iterate interactively, then persist)

**Limitations**:
- Preview status (single base agent: `antigravity-preview-05-2026`)
- No subagent delegation yet
- No agent versioning/rollback

**Quickstart pattern**:

```python
from google import genai

client = genai.Client()

# Inline approach (no registration)
interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Analyze Q1 revenue data and create a slide deck.",
    system_instruction="You are a data analyst. Always include visualizations.",
    environment={
        "type": "remote",
        "sources": [
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": "Always use matplotlib for charts. Include summary tables.",
            },
            {
                "type": "repository",
                "source": "https://github.com/org/templates",
                "target": "/workspace/templates",
            },
        ],
    },
)

print(interaction.output_text)

# Or create managed agent for reuse
agent = client.agents.create(
    id="data-analyst",
    base_agent="antigravity-preview-05-2026",
    system_instruction="You are a data analyst...",
    base_environment={"type": "remote", "sources": [...]},
)

# Invoke by ID
result = client.interactions.create(
    agent="data-analyst",
    input="Analyze Q1 revenue...",
    environment="remote",
)
```

---

### Google Deep Research Agent (`deep-research-preview-04-2026`)

**Best for**: Research tasks, context gathering, synthesis, planning-heavy workflows

**Key capabilities**:
- Collaborative planning before execution
- Standard variant (speed/efficiency) vs Max variant (comprehensiveness)
- File search and visualization tools
- MCP server integration

**Unique strengths**:
- Optimized for research over execution
- Planning-first approach (reduces wasted tool calls)

**Limitations**:
- Narrower use case (research-focused)
- Preview status

**Quickstart pattern**:

```python
from google import genai

client = genai.Client()

# Standard research (speed)
result = client.interactions.create(
    agent="deep-research-preview-04-2026",
    input="Research the state of graph-based agent orchestration in 2026",
    environment="remote",
)

print(result.output_text)

# Max research (comprehensiveness)
result = client.interactions.create(
    agent="deep-research-preview-04-2026",
    input="Comprehensive analysis of Rust async runtime evolution",
    config={"variant": "max"},
    environment="remote",
)
```

---

### OpenAI Sandbox Agents (Beta)

**Best for**: Stateful workflows, sandbox memory patterns, multi-backend flexibility

**Key capabilities**:
- Persistent isolated workspaces
- Memory from prior runs (progressive disclosure)
- Multiple backends: Unix, Docker, Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, Vercel
- Manifest-based file staging
- Lazy skill loading

**Unique strengths**:
- Sandbox memory (lessons learned from previous runs)
- Most flexible backend choice (from local Unix to hosted providers)
- Manifest pattern (explicit file staging)
- Snapshot/resume workflow

**Limitations**:
- Beta stability
- Requires understanding of manifests and capabilities
- More complex setup than single-call alternatives

**Quickstart pattern**:

```python
import asyncio
from pathlib import Path
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.capabilities import Capabilities, LocalDirLazySkillSource, Skills
from agents.sandbox.entries import LocalDir
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient

HOST_REPO_DIR = Path("./repo")
HOST_SKILLS_DIR = Path("./skills")

def build_agent(model: str) -> SandboxAgent[None]:
    return SandboxAgent(
        name="Sandbox engineer",
        model=model,
        instructions=(
            "Read `repo/task.md` before editing. Stay grounded in the repository, "
            "preserve existing behavior, mention verification commands."
        ),
        default_manifest=Manifest(
            entries={"repo": LocalDir(src=HOST_REPO_DIR)}
        ),
        capabilities=Capabilities.default() + [
            Skills(lazy_from=LocalDirLazySkillSource(source=LocalDir(src=HOST_SKILLS_DIR))),
        ],
    )

async def main():
    result = await Runner.run(
        build_agent("gpt-5.5"),
        "Fix the issue in repo/task.md, run the test, summarize the change.",
        run_config=RunConfig(
            sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()),
            workflow_name="Sandbox coding task",
        ),
    )
    print(result.final_output)

asyncio.run(main())
```

---

## Behavioral Discipline (core)

**All managed agents MUST embed behavioral discipline from `knowledge/behavioral_discipline.json`.**

### Integration Flow

1. Read `knowledge/behavioral_discipline.json`
2. Check `agent_type_applicability` for "managed_agent" or relevant sub-type
3. Embed applicable principles using `compact_boilerplate`
4. Add to agent's system instruction or AGENTS.md

### Managed Agent-Specific Principles

From `behavioral_discipline.json`:

- **Think-then-act loops**: Managed agents have tool latency. Reason before tool use.
- **Surgical changes**: Edit only what's needed. Don't refactor unrelated code.
- **Verification**: Run tests/validation after every substantive change.
- **Goal-driven**: Define success criteria at task start, loop until verified.
- **Simplicity**: Minimum code to solve the problem. No speculative features.

**Example compact boilerplate** (for system instruction):

```
You follow these principles:
1. Think before acting. State assumptions. If multiple approaches exist, list tradeoffs.
2. Make surgical changes. Touch only what you must. Match existing style.
3. Verify after changes. Run tests, check output, confirm success.
4. Define success criteria. Loop until verified.
5. Simplicity first. Minimum code. No abstractions for single-use logic.
```

See `knowledge/behavioral_discipline.md` for full rationale and agent-type mappings.

---

## How to Use (core)

### Workflow

1. **Select platform** based on decision matrix above
2. **Choose iteration pattern**:
   - Anthropic: Create agent → environment → session → stream events
   - Google Antigravity: Inline prototype → persist as managed agent
   - Google Deep Research: Single-call research tasks
   - OpenAI Sandbox: Build SandboxAgent → manifest → capabilities → run
3. **Embed behavioral discipline** in system instruction or AGENTS.md
4. **Test interactively** before productionizing
5. **Monitor and iterate** using platform observability (events, logs, status)

### File-Based Customization

**Anthropic**: Upload files via Files API, reference in system prompt or MCP servers

**Google**: Use `environment.sources` with inline, repository, or GCS sources. Auto-loads `.agents/AGENTS.md` and `.agents/skills/*/SKILL.md`

**OpenAI**: Use `Manifest` with `LocalDir`, `GitRepo`, or hosted provider mounts

---

## Key Principles (core)

### 1. Platform-Appropriate Design

**Principle**: Match agent design to platform strengths.

**Anthropic**: Use for event-driven multi-agent systems, Advisor Tool quality patterns, long-running stateful sessions.

**Google Antigravity**: Use for rapid iteration, inline prototyping, fork-from-environment workflows.

**Google Deep Research**: Use for research-first tasks, planning-heavy workflows.

**OpenAI Sandbox**: Use for sandbox memory patterns, multi-backend portability, stateful workspaces.

### 2. Managed vs Self-Hosted Clarity

**Principle**: Managed agents are for sandboxed execution. If you don't need code execution, files, or web tools, use self-hosted (Messages API, generateContent API, or SDK Agents).

**Anti-pattern**: Using managed agents for simple API orchestration (overkill, higher latency, higher cost).

### 3. Behavioral Discipline Integration

**Principle**: All managed agents embed behavioral discipline principles from `knowledge/behavioral_discipline.json` to reduce hallucination, overcomplicated solutions, and unnecessary changes.

**Implementation**: Add compact boilerplate to system instruction or AGENTS.md.

### 4. State Management Awareness

**Principle**: Understand each platform's state model.

**Anthropic**: Server-side event history, persistent sessions.

**Google Antigravity**: Server-side state via `previous_interaction_id`, forked environments.

**OpenAI Sandbox**: Snapshot/resume, sandbox memory (lessons from prior runs).

---

## Common Pitfalls (core)

### 1. Using Managed Agents for Simple Tasks

**Problem**: Invoking managed agent for tasks that don't need sandboxed execution (e.g., "summarize this text").

**Impact**: Higher latency, higher cost, wasted sandbox resources.

**Fix**: Use self-hosted agent (Messages API, generateContent, SDK Agent) for API-only operations.

**Detection**: If the agent never uses tools like bash, file operations, or web browsing, it shouldn't be managed.

### 2. Ignoring Platform State Models

**Problem**: Treating all platforms the same for state management.

**Example**: Expecting Google Antigravity to persist session state without `previous_interaction_id`, or expecting OpenAI Sandbox to auto-resume without snapshot config.

**Impact**: Lost context, repeated work, failed multi-turn workflows.

**Fix**: Read platform-specific state patterns. Anthropic uses sessions, Google uses `previous_interaction_id`, OpenAI uses snapshots.

### 3. Skipping Behavioral Discipline

**Problem**: Launching managed agent without embedding behavioral discipline principles.

**Impact**: Agent makes unnecessary changes, refactors unrelated code, skips verification, produces overcomplicated solutions.

**Fix**: Always embed `compact_boilerplate` from `knowledge/behavioral_discipline.json` in system instruction.

### 4. Overcomplicating Manifests/Environments

**Problem**: Staging entire repos, installing 50 packages, mounting 10 directories when task needs 3 files.

**Example**: Mounting full monorepo when agent only needs `docs/` folder.

**Impact**: Slower sandbox startup, higher token usage, harder debugging.

**Fix**: Manifest only what's needed. Start minimal, add incrementally.

### 5. Not Testing Sandbox Limits

**Problem**: Assuming managed sandbox has infinite resources (disk, memory, network, timeout).

**Impact**: Agent hits limits mid-execution, fails silently or with unclear errors.

**Fix**: Test sandbox limits explicitly. Anthropic cloud sandboxes have disk/memory caps. Google sandboxes have timeout limits. OpenAI backends vary by provider.

---

## Validation (core)

### Pre-Deployment Checklist

- [ ] Platform selected matches use case (long-running → Anthropic, rapid iteration → Google, multi-backend → OpenAI)
- [ ] Behavioral discipline embedded in system instruction or AGENTS.md
- [ ] Manifest/environment includes only necessary files/repos
- [ ] Agent tested with representative tasks end-to-end
- [ ] State management pattern understood (sessions, interactions, snapshots)
- [ ] Tool usage verified (agent uses tools only when needed)
- [ ] Error handling tested (network failures, timeout, disk full)
- [ ] Cost projected (managed execution cost vs API-only alternatives)

### Success Metrics

- **Tool efficiency**: Agent uses tools only when needed, no unnecessary bash/file calls
- **State persistence**: Multi-turn workflows resume correctly
- **Behavioral adherence**: No overcomplicated solutions, no unnecessary refactoring
- **Verification**: Agent confirms success after changes (runs tests, checks output)

---

## Examples (core)

### Anthropic: Coding Assistant with Verification Loop

```python
from anthropic import Anthropic

client = Anthropic()

agent = client.beta.agents.create(
    name="Test-Driven Coder",
    model={"id": "claude-sonnet-4-5"},
    system=(
        "You write code following test-driven principles. Behavioral discipline:\n"
        "1. Read task requirements fully before coding\n"
        "2. Write tests first, then implementation\n"
        "3. Make surgical changes only\n"
        "4. Run tests after every change\n"
        "5. Confirm success criteria met\n"
    ),
    tools=[{"type": "agent_toolset_20260401"}],
)

environment = client.beta.environments.create(
    name="tdd-env",
    config={"type": "cloud", "networking": {"type": "unrestricted"}},
)

session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="TDD task",
)

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{
            "type": "user.message",
            "content": [{
                "type": "text",
                "text": "Implement a binary search tree with insert, search, and delete. Write tests first.",
            }],
        }],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="")
            case "agent.tool_use":
                print(f"\n[{event.name}]")
            case "session.status_idle":
                break
```

### Google Antigravity: Data Analyst with Git Repo

```python
from google import genai

client = genai.Client()

# Inline prototype
interaction = client.interactions.create(
    agent="antigravity-preview-05-2026",
    input="Analyze sales trends in data/Q1_sales.csv and create a matplotlib chart.",
    system_instruction=(
        "You are a data analyst. Behavioral discipline:\n"
        "1. Read data files before analysis\n"
        "2. Use simple, clear visualizations\n"
        "3. Verify output files exist after generation\n"
    ),
    environment={
        "type": "remote",
        "sources": [
            {
                "type": "repository",
                "source": "https://github.com/company/sales-data",
                "target": "/workspace/data",
            },
            {
                "type": "inline",
                "target": ".agents/AGENTS.md",
                "content": "Use matplotlib. Save charts to /workspace/output/. Include summary stats.",
            },
        ],
    },
)

print(interaction.output_text)

# Persist as managed agent after testing
agent = client.agents.create(
    id="sales-analyst",
    base_agent="antigravity-preview-05-2026",
    system_instruction=interaction.system_instruction,
    base_environment=interaction.environment_id,  # Fork from tested environment
)
```

### OpenAI Sandbox: Stateful Workflow with Memory

```python
import asyncio
from pathlib import Path
from agents import Runner
from agents.run import RunConfig
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.capabilities import Capabilities, Memory
from agents.sandbox.entries import LocalDir
from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient

def build_agent(model: str) -> SandboxAgent[None]:
    return SandboxAgent(
        name="Research Assistant",
        model=model,
        instructions=(
            "You research technical topics and build knowledge incrementally.\n"
            "Behavioral discipline:\n"
            "1. Check memory for prior learnings before research\n"
            "2. Cite sources, verify facts\n"
            "3. Summarize findings, save to memory\n"
        ),
        default_manifest=Manifest(entries={"workspace": LocalDir(src=Path("./workspace"))}),
        capabilities=Capabilities.default() + [Memory()],
    )

async def run_research_task(task: str):
    result = await Runner.run(
        build_agent("gpt-5.5"),
        task,
        run_config=RunConfig(
            sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()),
            workflow_name="Research task",
        ),
    )
    return result.final_output

# Run tasks across sessions, sandbox memory persists learnings
asyncio.run(run_research_task("Research Rust async runtimes"))
asyncio.run(run_research_task("Compare tokio vs async-std based on prior research"))
```

---

## Resources (core)

**Anthropic Claude Managed Agents**:
- [Overview](https://docs.anthropic.com/en/managed-agents/overview)
- [Quickstart](https://docs.anthropic.com/en/managed-agents/quickstart)
- [Tools](https://docs.anthropic.com/en/managed-agents/tools)

**Google Antigravity**:
- [Building Managed Agents](https://ai.google.dev/gemini-api/docs/managed-agents)
- [Antigravity Agent](https://ai.google.dev/gemini-api/docs/antigravity-agent)
- [Agent Environments](https://ai.google.dev/gemini-api/docs/agent-environment)

**Google Deep Research**:
- [Deep Research Agent](https://ai.google.dev/gemini-api/docs/deep-research)

**OpenAI Sandbox Agents**:
- [Sandbox Agents Quickstart](https://openai.github.io/openai-agents-python/agents/sandbox/)
- [Sandbox Guide](https://openai.github.io/openai-agents-python/agents/sandbox/guide/)
- [Sandbox Clients](https://openai.github.io/openai-agents-python/agents/sandbox/clients/)

**Cross-Platform**:
- `knowledge/behavioral_discipline.md` (narrative principles)
- `knowledge/behavioral_discipline.json` (structured rules)
- `make_agent.md` (general agent patterns, execution model decision matrix)

---

## Version History

**v1.0** (2026-07-06): Initial template covering Anthropic, Google (Antigravity + Deep Research), and OpenAI Sandbox Agents based on 2026 platform updates.
