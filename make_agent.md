---
name: make_agent
description: Generates Make-AI-Agents-spec agents with behavioral discipline baked in. The meta-skill of the ecosystem.
version: "3.6"
last_updated: 2026-07-07
author: chaz-clark
license: MIT
skill_type: meta
platforms:
  - Anthropic
  - Google
  - OpenAI
  - xAI
dependencies:
  - knowledge/behavioral_discipline.md
  - knowledge/behavioral_discipline.json
propagates:
  - behavioral_discipline
see_also:
  - make_managed_agent.md
  - make_orchestrator_agent.md
  - make_agent_knowledge.md
  - make_agent_qc.md
metadata:
  make-ai-agents:
    companion_json_deprecated: "2026-07-07 - use YAML frontmatter instead"
---

# <Your Agent Name> Agent Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `<your_agent_name>.json` for structured data, code/config examples, validation, and operations. Do not parse this Markdown.
3. Keep this file lean. For simple agents, include only Mission, Quickstart, JSON vs MD guidance, Key Principles, **Behavioral Discipline**, How to Use, Pitfalls, Examples, Validation, and Resources.
4. For added complexity, only append the optional sections marked below.
5. **Behavioral Discipline is required in every new agent spec.** Consult `knowledge/behavioral_discipline.md` (narrative) and `knowledge/behavioral_discipline.json` (structured rules) when generating any new agent. The skill MUST look up `agent_type_applicability` for the new agent's type and embed the appropriate principles using `compact_boilerplate`. See "## Behavioral Discipline (core)" below for the integration flow.

---

## Mission (core)

A clear and concise statement of the agent's primary purpose.

**What it does**: [Primary function - what the agent accomplishes]

**Why it exists**: [Problem it solves - the pain point this addresses]

**Who uses it**: [Target audience - developers, data scientists, analysts, etc.]

**Example**: "Summarizes technical documentation using GPT-4, reducing reading time by 80% while preserving key information."

---

## Execution Model: Managed vs Self-Hosted (core)

A fundamental decision that affects agent architecture, deployment, and capabilities.

### What Are Managed Agents?

**Managed agents** run in fully managed execution environments provided by AI platforms (Anthropic, Google, OpenAI). The platform handles:
- Secure sandboxed execution (filesystem, code execution, web browsing)
- Tool orchestration and lifecycle
- State persistence across sessions
- Infrastructure and scaling

**Self-hosted agents** run in your environment (CLI, server, cloud function) with you managing:
- Execution environment and dependencies
- Tool implementation and integration
- State management and persistence
- Infrastructure and deployment

### Decision Matrix

| Factor | Use Managed | Use Self-Hosted |
|--------|-------------|-----------------|
| **Execution needs** | Need sandboxed code execution, file system, web browsing | API-only operations, lightweight tasks |
| **Tool complexity** | Pre-built tools sufficient (bash, web, files) | Custom tools, proprietary integrations |
| **State requirements** | Multi-session persistence needed | Stateless or custom state management |
| **Control level** | Accept platform constraints | Need full control over environment |
| **Deployment speed** | Instant (single API call) | Custom deployment pipeline |
| **Cost model** | Pay per managed execution | Pay per API call only |
| **Security posture** | Trust platform sandbox | Need air-gapped or on-prem execution |

### Platform Comparison

**Anthropic Claude Managed Agents** (Beta: `managed-agents-2026-04-01`)
- **Environment**: Fully managed sandbox (bash, files, web, code)
- **Tools**: `agent_toolset_20260401` (pre-built) + custom tools
- **Multi-agent**: Shared sandbox, isolated session threads
- **Special**: Advisor Tool (executor + advisor model pattern)
- **Best for**: General-purpose autonomous agents, multi-agent systems

**Google Antigravity Agent** (`antigravity-preview-05-2026`)
- **Environment**: Secure Linux sandbox hosted by Google
- **Model**: Gemini 3.5 Flash
- **Tools**: Code execution, file management, web browsing
- **Best for**: General-purpose managed agents, single API call workflows

**Google Deep Research Agent** (`deep-research-preview-04-2026`)
- **Environment**: Collaborative planning + MCP integration
- **Variants**: Standard (speed/efficiency) vs Max (comprehensiveness)
- **Tools**: File Search, visualization, research orchestration
- **Best for**: Research, context gathering, synthesis tasks

**OpenAI Sandbox Agents** (Beta)
- **Environment**: Persistent isolated workspaces
- **Backends**: Unix, Docker, Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, Vercel
- **Memory**: Lessons from prior runs (progressive disclosure)
- **Best for**: Stateful workflows, sandbox memory patterns, multi-backend flexibility

### Configuration Patterns

**Anthropic Managed Agent** (Python):
```python
client = Anthropic()
response = client.beta.agents.messages.create(
    agent_id="agent_123",
    tools=[{"type": "agent_toolset_20260401"}],  # Pre-built tools
    messages=[{"role": "user", "content": "Research X and summarize"}],
    model="claude-sonnet-4-5",
    beta="managed-agents-2026-04-01"
)
```

**Google Antigravity** (Python):
```python
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    base_agent="antigravity-preview-05-2026"
)
response = model.generate_content("Code a web scraper for Y")
```

**OpenAI Sandbox Agent** (Python):
```python
from openai_agents import SandboxAgent, Manifest

agent = SandboxAgent(
    name="research_agent",
    model="gpt-5.5",
    manifest=Manifest(
        sandbox_client="e2b",  # or docker, unix, etc.
        persistent=True
    )
)
result = agent.run("Analyze dataset and generate report")
```

### When to Use Managed Agents

✅ **Use managed when**:
- Agent needs code execution, file operations, or web browsing
- Multi-step workflows requiring persistent state
- Rapid prototyping without infrastructure setup
- Delegating complex sub-tasks to autonomous execution
- Building multi-agent systems with shared resources

❌ **Avoid managed when**:
- Simple API-only operations (e.g., text classification, extraction)
- Need air-gapped or on-premises execution
- Custom tool integrations not supported by platform
- Cost-sensitive workflows (managed execution adds overhead)
- Regulatory requirements prevent cloud execution

### Integration with This Guide

For **self-hosted agents**:
- Follow standard guidance in this document
- Implement tools as functions/APIs
- Manage state in your application layer

For **managed agents**:
- Define agent mission and tools (this doc)
- Configure managed environment (platform-specific)
- Use pre-built tools where possible, custom tools for proprietary logic
- Design for autonomous execution (agent operates independently)

---

## Multimodal Capabilities (optional)

**When to include**: Agent handles voice, images, video, or audio in addition to text.

**When to skip**: Text-only agents.

### Capability Matrix

| Capability | xAI | OpenAI | Google | Anthropic |
|------------|-----|--------|--------|-----------|
| **Real-time voice** | ✅ Voice Agent API | ✅ Realtime API | ❌ | ❌ |
| **Text-to-speech** | ✅ TTS API | ✅ TTS API | ✅ Text-to-Speech | ❌ |
| **Speech-to-text** | ✅ STT API | ✅ Whisper | ✅ Speech-to-Text | ❌ |
| **Image generation** | ✅ Imagine API | ✅ DALL-E | ✅ Imagen | ❌ |
| **Image understanding** | ✅ Vision | ✅ Vision | ✅ Vision | ✅ Vision |
| **Video generation** | ✅ Imagine Video | ❌ | ✅ Veo | ❌ |
| **Video understanding** | ❌ | ✅ Vision | ✅ Vision | ❌ |

### Voice Agents

#### xAI Voice Agent (Real-time WebSocket)

**What**: Bidirectional streaming voice conversations over WebSocket.

**Best for**: Phone agents, voice assistants, interactive voice systems, customer support.

**Key capabilities**:
- Real-time voice input/output
- Server-side VAD (Voice Activity Detection)
- Multiple voices (eve, ara, rex, sal, leo) + custom voice cloning
- Tools integration (file_search, web_search, x_search, MCP, function calling)
- Session resumption
- Language hints for multilingual ASR

**Pattern**:
```python
import asyncio
import json
import websockets

async def voice_agent():
    async with websockets.connect(
        "wss://api.x.ai/v1/realtime?model=grok-voice-latest",
        additional_headers={"Authorization": f"Bearer {xai_api_key}"}
    ) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "voice": "eve",
                "instructions": "You are a helpful assistant.",
                "turn_detection": {"type": "server_vad"},
                "tools": [{"type": "web_search"}],
            }
        }))

        # Send text or audio
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {"type": "message", "role": "user",
                     "content": [{"type": "input_text", "text": "Hello!"}]}
        }))
        await ws.send(json.dumps({"type": "response.create"}))

        # Receive audio/text responses
        async for msg in ws:
            event = json.loads(msg)
            if event["type"] == "response.audio.delta":
                # Play audio chunk
                play_audio(event["delta"])
            elif event["type"] == "response.text.delta":
                print(event["delta"], end="")
```

**Tools integration**: Voice agents can call tools mid-conversation (web search, file search, MCP servers, custom functions). Results are spoken to the user.

**Limitations**:
- Requires WebSocket transport (not HTTP)
- Authentication via API key (server-side) or Ephemeral Tokens (client-side)
- Beta stability

**Documentation**: `source_docs/xai_voice_agent.md`

#### OpenAI Realtime API

**What**: Real-time voice and text streaming via WebSocket.

**Best for**: Voice assistants, conversational AI, speech-to-speech applications.

**Pattern**:
```python
# Similar to xAI Voice Agent, uses WebSocket transport
# See OpenAI Realtime API docs for specifics
```

**Documentation**: Referenced in `source_docs/openai_models.md` (separate from Responses API)

### Voice Integration Patterns

**Standalone voice agent** (agent IS the voice interface):
```python
# xAI Voice Agent or OpenAI Realtime API
# Entire interaction is voice-first
# Tools are called during conversation
```

**Voice + text hybrid** (voice input → text processing):
```python
# Step 1: Speech-to-text (Whisper, xAI STT, Google STT)
audio_file = "user_query.wav"
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
)

# Step 2: Text-based agent processes transcript
agent_response = agent.run(transcript.text)

# Step 3: Text-to-speech (optional)
speech = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=agent_response,
)
speech.stream_to_file("response.mp3")
```

**When to use voice**:
- User interaction is primarily spoken (phone systems, voice assistants)
- Accessibility requirements (vision-impaired users)
- Hands-free operation needed (driving, cooking, manufacturing)
- Natural conversation flow more important than precision

**When NOT to use voice**:
- Complex data entry (addresses, IDs, technical terms)
- Need for permanent written record
- Noisy environments
- Privacy concerns (open office, public spaces)

### Image and Video

#### Image Generation

**xAI Imagine** (image generation and editing):
```python
import xai_sdk

client = xai_sdk.Client()

# Generate image from text
response = client.image.sample(
    prompt="A futuristic city at sunset with flying cars",
    model="grok-imagine-image-quality",
    aspect_ratio="16:9",
    resolution="2K",
    count=4,
)

for url in response.urls:
    download_image(url)

# Edit image with reference images
response = client.image.edit(
    prompt="Add snow and make it nighttime",
    model="grok-imagine-image-quality",
    reference_images=[img1_url, img2_url, img3_url],  # Up to 3 refs
)
```

**OpenAI DALL-E**:
```python
from openai import OpenAI
client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city at sunset",
    size="1792x1024",
    quality="hd",
    n=1,
)
```

**Google Imagen**:
```python
# Available via Google Cloud AI Platform
# See Google documentation for current API patterns
```

#### Video Generation

**xAI Imagine Video** (text-to-video or image-to-video):
```python
# Text to video
response = client.video.generate(
    prompt="A drone flying through a forest",
    model="grok-imagine-video-1.5",
    duration=5,
    resolution="1080p",
)

# Image to video (animate a still image)
response = client.video.animate(
    image_url="https://example.com/first-frame.jpg",
    prompt="Zoom in slowly while the sun rises",
    model="grok-imagine-video-1.5",
)
```

**Google Veo**:
```python
# Available via Google Cloud Vertex AI
# See Google documentation for current API patterns
```

#### Image and Video Understanding

**All platforms support vision** (analyze images/video in agent context):

**OpenAI**:
```python
from agents import Agent, Runner

agent = Agent(
    name="Image Analyzer",
    instructions="Analyze images and provide detailed descriptions.",
)

result = await Runner.run(
    agent,
    [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}},
    ],
)
```

**Anthropic**:
```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image in detail."},
            {"type": "image", "source": {"type": "url", "url": image_url}},
        ],
    }],
)
```

**Google**:
```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-3.5-flash")
image = genai.upload_file("path/to/image.jpg")

response = model.generate_content(["Describe this image", image])
```

### Multimodal Agent Patterns

**1. Vision-augmented analyst** (agent processes images as part of analysis):
```python
agent = Agent(
    name="Data Analyst",
    instructions="Analyze charts, graphs, and screenshots. Extract insights and trends.",
    tools=[analyze_chart, extract_table_data],
)

# User sends screenshot of dashboard
result = await Runner.run(
    agent,
    [
        {"type": "text", "text": "Analyze Q4 performance from this dashboard."},
        {"type": "image_url", "image_url": {"url": dashboard_screenshot_url}},
    ],
)
```

**2. Creative assistant** (generates images/video as part of workflow):
```python
agent = Agent(
    name="Marketing Content Creator",
    instructions="Generate social media posts with images and captions.",
    tools=[generate_image, create_video, schedule_post],
)

# Agent calls generate_image tool during execution
# Tool implementation:
def generate_image(prompt: str) -> str:
    response = xai_client.image.sample(
        prompt=prompt,
        model="grok-imagine-image-quality",
    )
    return response.url
```

**3. Voice-first support agent** (handles customer calls):
```python
# xAI Voice Agent with tools
# Session config includes customer context, CRM integration
# Agent answers questions, looks up orders, processes requests via voice
```

### When to Use Multimodal

**Use image generation when**:
- Agent creates marketing materials, presentations, visualizations
- User requests creative content (illustrations, mockups, concepts)
- Workflow includes design/creative output

**Use image understanding when**:
- User inputs are screenshots, photos, diagrams
- Agent analyzes visual data (charts, dashboards, documents)
- OCR or visual inspection is part of the task

**Use voice when**:
- Primary interface is spoken conversation
- Accessibility or hands-free operation required
- Natural conversation flow is critical

**Use video generation when**:
- Agent creates video content (ads, explainers, animations)
- Workflow includes video editing or production

**Use video understanding when**:
- Agent analyzes video content (surveillance, training videos, user demos)
- Extract information from video frames or motion

### Common Pitfalls

**1. Treating voice as transcribed text**

**Problem**: Building voice agent as STT → text agent → TTS pipeline instead of native voice.

**Why it fails**: Misses latency benefits, natural conversation flow, interruption handling.

**Fix**: Use xAI Voice Agent or OpenAI Realtime API for native voice agents. Use STT→Agent→TTS only for asynchronous voice tasks.

**2. Not handling multimodal tool outputs**

**Problem**: Agent generates image URL but user expects inline display.

**Why it fails**: User sees URL string instead of rendered image.

**Fix**: Return structured output with content type markers. Frontend renders based on type.

```python
# Good: Structured output
{
    "type": "image",
    "url": "https://...",
    "description": "Generated marketing banner"
}

# Bad: Raw URL string
"Here is your image: https://..."
```

**3. Ignoring modality costs**

**Problem**: Agent generates 50 images or 10 videos in a single run.

**Why it fails**: Costs explode (xAI Imagine: $0.05/image, $0.08/sec for video).

**Fix**: Set limits on multimodal generation. Require approval for batch generation.

**4. No fallback for unsupported modalities**

**Problem**: Agent requires voice but user's platform doesn't support WebSocket.

**Why it fails**: Agent unusable on restricted networks or mobile browsers.

**Fix**: Provide text fallback. Detect capabilities and degrade gracefully.

---

## Agent Quickstart (core)

A fast-path workflow for getting started with this agent:

0. **[Choose interaction_pattern, then embed discipline]**: Decide whether the agent is `read_only` / `single_write_workflow` / `multi_step_batch` / `single_call_api` / `conversational` (see decision flow in `## Behavioral Discipline (core)` below — ask the user if composite). Then embed the behavioral discipline in MD (after `## Key Principles`), in the JSON `behavioral_discipline` object, and in the system prompt. **Required in every new agent.**

1. **[Identify/Load]**: What the agent identifies or loads first
   - Example: "Load system prompts from `agent.json` primary_data"

2. **[Parse Data]**: Load structured data from `<your_agent_name>.json`
   - Example: "Parse API endpoint mappings from primary_data"

3. **[Apply/Transform]**: Main processing step (constrained by the embedded discipline from step 0)
   - Example: "Send request to OpenAI API with formatted prompt"

4. **[Validate]**: How to verify results — including running `make_agent_qc` to confirm BD-QC-001 through BD-QC-007 pass
   - Example: "Check summary length < 500 tokens, readability score > 60; run make_agent_qc"

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

**Enable Strict Tool Use When Schemas Have Real Constraints**
**Description**: When a tool's `input_schema` contains required fields, enums, or precise format constraints that matter, enable strict tool use so the model is guaranteed to produce schema-conformant arguments.
**Why**: Without strict mode, the model produces arguments that are *usually* valid but occasionally drift — a missing required field, an enum value not in the allowed list, an extra property the runtime doesn't expect. The runtime then has to validate, reject, and retry, or worse, accept the drift silently. Strict mode pushes validation to the model side: invalid arguments are simply never generated. The trade-off is a small latency cost and a hard requirement that your schema be fully specified.
**How**: Set `strict: true` on tool definitions where schema conformance matters. For Anthropic, this is on the tool object. For OpenAI function calling, it is `strict: true` on the function definition. Note that strict mode requires the schema to be exhaustively defined — no implicit optional fields. If the schema is exploratory or evolving, leave strict off; if it is stable and the runtime depends on it, turn it on.

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

**Configure Reasoning Effort for Complex Tasks**
**Description**: For agents that perform multi-step planning, ambiguous tool selection, or chain-of-reasoning over evidence, set a higher reasoning effort (or extended thinking budget) than the default. For simple lookups, leave it at default to save latency and cost.
**Why**: Models with adjustable reasoning effort (Claude extended thinking, OpenAI reasoning_effort, xAI reasoning models) produce noticeably better tool selection and plan quality when given more thinking budget — but at the cost of latency and tokens. The default is tuned for fast turns, not for hard agentic decisions. Agents that fail intermittently on ambiguous inputs often succeed reliably with higher reasoning effort.
**How**: Set the reasoning parameter in `implementation.llm_agent.parameters` to match the agent's typical decision complexity. For Anthropic: `thinking: { type: "enabled", budget_tokens: <value> }`. For OpenAI: `reasoning_effort: "low" | "medium" | "high"`. For agents that mix simple and hard requests, consider routing — short-circuit easy cases to the default and reserve high reasoning for the hard branch.

**Structured Output vs. Function Calling — Different Jobs**
**Description**: Use structured output (`response_format`) when you want the model's final answer in a specific schema. Use function calling (tools) when you need the model to request an action during the conversation.
**Why**: Conflating these leads to over-engineering — defining tools when structured output would suffice, or expecting a formatted final response from a tool-calling loop that produces raw text. The distinction is: structured output shapes the terminal response; function calling shapes intermediate steps.
**How**: If your agent needs to return a structured JSON object as its final answer, set `response_format` in parameters. If your agent needs to take actions (fetch data, write files, call APIs) before producing a final answer, use tools. Some agents need both: tools for the agentic loop, `response_format` for the final structured output.

**Graceful Degradation for Optional Tools**
**Description**: When a tool or external service may not be available in all environments, the agent must adapt — not block.
**Why**: Real deployments are heterogeneous. An MCP server, a local script, or an external API may exist in one environment and not another. An agent that halts with "tool not found" forces manual intervention for what could be a soft fallback.
**How**: For each optional tool, define a fallback in `error_handling.fallbacks`: what the agent does when the tool is unavailable (use an alternate tool, use embedded data, ask the user, or proceed in degraded mode). Document this in the system prompt too: "X may or may not be available — do not block if it is absent, fall back to Y." See `operational_guidance.when_not_to_use` for environment prerequisites.

**Prefer MCP Servers Over Custom Tools When Available**
**Description**: When functionality exists as an MCP (Model Context Protocol) server — official or community-maintained — prefer connecting it via `mcp_servers` over reimplementing the same tools in your agent.
**Why**: MCP servers are maintained outside the agent's lifecycle. Bug fixes, auth updates, and new capabilities flow to the agent for free when depending on an MCP server instead of duplicating its logic in the tool list. The cost of custom tools is not the initial implementation — it is the long-tail maintenance as the underlying API changes. Three platforms (Anthropic, OpenAI, Google) now support MCP as a first-class integration; using it where available reduces duplicated maintenance across the ecosystem.
**How**: Before defining a custom tool, check whether an MCP server already exposes the operation (search the official MCP registry, the platform's MCP catalog, or the underlying service's own documentation). If yes, add it to `implementation.llm_agent.mcp_servers[]` in the JSON. Reserve custom tools in `implementation.llm_agent.tools[]` for: agent-specific logic with no general utility, very small wrappers around internal-only APIs, or cases where the MCP server is unmaintained or missing required features.

**Choose a Memory/State Strategy Before Building**
**Description**: Decide up front whether the agent is stateless (each call independent), keeps state manually in conversation history, or uses a platform-managed session that can be paused, resumed, or forked.
**Why**: Memory strategy is a design-time decision that determines what the agent's runtime must persist, how multi-turn requests behave, and how recovery from interruption works. Picking it after the agent is built almost always means retrofitting either the system prompt, the tool runner, or the surrounding application — none of which is cheap. Anthropic exposes session IDs with `resume=session_id` and `fork=session_id`; OpenAI's Agents SDK has a `Sessions` primitive (SQLAlchemy, Advanced SQLite, Encrypted variants); Google documents manual conversation-history management on the client. All three platforms treat this as a first-class concern, not an implementation afterthought.
**How**: Pick one of three strategies and document it in `implementation.llm_agent.parameters.memory` and in the system prompt:
- **Stateless** — every call is independent; no history carried across calls. Right for `single_call_api` and webhook-style agents.
- **Manual history** — the application appends prior turns to the prompt on each call. Right when you need full control over what's retained, or when running across providers that don't share a session format.
- **Platform-managed session** — store a session ID and resume on subsequent calls. Right for `multi_step_batch` and long-running interactive agents where the platform's session store handles trimming and recovery.

For session-stateful agents, also document when the loop repeats vs. when it ends in `constraints.safety_boundaries.human_in_the_loop` — long sessions accumulate drift, and the agent should know when to terminate the session on its own.

**Propose Before Execute**
**Description**: When a request is open-ended or has irreversible consequences, propose a plan and wait for confirmation before acting. When a request is specific and one-step, execute and report.
**Why**: Anthropic's agentic safety guidance identifies this as the core autonomy calibration: "prefer minimal footprint, confirm before irreversible actions." Agents that always propose are slow; agents that always execute without proposing cause unintended changes. The right behavior depends on request specificity.
**How**: In the system prompt, define both modes explicitly: "When the request is open-ended, present a plan and wait for approval. When the request is a complete, specific, single-step instruction, execute and report outcomes." Map this to your `constraints.safety_boundaries.human_in_the_loop` field. For session-stateful agents, document when the loop repeats vs. when it ends.

---

## Behavioral Discipline (core)

Every agent built from this template inherits a behavioral discipline that produces predictable, trustworthy behavior for end users. The discipline is the source of trust for non-technical users — it makes the agent visible, predictable, and correctable.

The discipline is defined in:
- **`knowledge/behavioral_discipline.md`** — narrative source of truth (Toyota Way + Karpathy synthesis, 10 principles with examples, foundation, override rules, non-interactive mode)
- **`knowledge/behavioral_discipline.json`** — structured rules (canonical principle metadata, agent_type_applicability lookup, trust markers, override rules, compact_boilerplate templates, QC checks, non_interactive_mode mappings)

This template **does not duplicate the discipline** — it wires it into the agent-generation flow and instructs the make_agent skill how to apply it.

### What this section is vs. what Key Principles is

- **Key Principles** (above) = principles that govern *this specific agent's* design (its reliability, observability, etc.). Agent-specific.
- **Behavioral Discipline** (this section) = the shared discipline ALL agents built from this template inherit. Cross-cutting; produced from the knowledge files.

### Two orthogonal classifications — implementation pattern vs. interaction pattern

These are different axes that describe an agent. **Don't conflate them.** Both can be set on the same agent simultaneously.

| Classification | Field in agent JSON | Values | Meaning |
|---|---|---|---|
| **Implementation pattern** — how it's built | `agent_type.type` | `class_based`, `llm_agent`, `api_agent`, `data_processor`, `multi_agent`, `workflow`, `rule_based`, `other` | The execution model. Drives which `implementation` branch is filled in. |
| **Interaction pattern** — how it behaves | `behavioral_discipline.interaction_pattern` | `read_only`, `single_write_workflow`, `multi_step_batch`, `single_call_api`, `conversational` | The behavioral profile. Drives which discipline principles apply. |

Examples:
- A documentation Q&A bot is `agent_type.type: llm_agent` + `interaction_pattern: read_only`.
- A data migration tool is `agent_type.type: api_agent` (or `data_processor`) + `interaction_pattern: multi_step_batch`.
- A webhook handler is `agent_type.type: api_agent` + `interaction_pattern: single_call_api`.

The discipline lookup uses `interaction_pattern` only. `agent_type.type` is unrelated to which principles get embedded.

### Integration flow — what the make_agent skill MUST do

When generating a new agent spec, the skill MUST follow this flow. Each step is a hard requirement, not a suggestion:

1. **MUST read** `knowledge/behavioral_discipline.json` directly. Do not infer the contents from training data — open the file. (Verification: tool-trace shows the read.)
2. **MUST determine** the new agent's `interaction_pattern` using this decision flow. **Evaluate top-to-bottom — first matching criterion wins.** If a later criterion would also match (e.g., a read-only Q&A bot also fits "naturally varied prose"), the earlier match resolves it. If two or more criteria of equal priority match (genuine composite case), MUST ask the user.
   1. Does the agent only read/return data with no writes? → `read_only`
   2. Does the agent perform exactly one state change with confirmation? → `single_write_workflow`
   3. Does the agent fire as a one-shot call (webhook, single-fire job) with no future session? → `single_call_api`
   4. Does the agent perform multi-resource workflows, batches, or migrations? → `multi_step_batch`
   5. Is the agent's output naturally varied prose (chat, advisory) and not primarily read-only? → `conversational`
   6. **Genuine composite case** (the workflow legitimately spans multiple patterns, not just overlap from above) → MUST ask the user explicitly which pattern dominates. Do not silently default. Do not pick "the safest over-include" — `multi_step_batch` for a primarily read-only agent over-applies discipline (e.g., A3 documentation on every read) and produces noise the user didn't ask for. The right move is to ask, or to split into sub-agents per pattern.
3. **MUST pull** the `always_include` array of principle IDs (P-001 through P-010) from `agent_type_applicability.types[<interaction_pattern>]`.
4. **MUST embed** the discipline in the new agent's MD using `compact_boilerplate.md_section_template`. Place this section **immediately after `## Key Principles (core)`** in the new agent's MD. Substitute:
   - `{{agent_type}}` — the `interaction_pattern` value
   - `{{applicable_principles_list}}` — formatted list using `applicable_principles_list_format`, one entry per applicable principle pulled from `principles[*]` (id, name, toyota_concept, compact_statement, trigger)
   - `{{no_override_ids}}` — from `override_rules.no_override_principles` (currently `["P-001", "P-003", "P-007", "P-010"]`)
5. **MUST embed** the discipline in the new agent's `implementation.llm_agent.system_prompt` using `compact_boilerplate.system_prompt_template` **when the agent's `implementation` carries the `llm_agent` branch**. Same substitutions. An MD-only embed is a critical failure — both layers must carry the discipline because runtime LLMs read the system prompt, not the MD. **N/A when the agent's `agent_type.type` is `workflow`, `api_agent`, `data_processor`, `class_based`, or `rule_based`** (no llm_agent.system_prompt exists) — in those cases, BD-QC-002 is skipped per its `_applicability` clause in `knowledge/behavioral_discipline.json` → `qc_checks`. Document the skip in the agent's `validation.discipline_validation` with the reason "BD-QC-002 N/A — no llm_agent branch."
6. **MUST populate** the new agent's `behavioral_discipline` JSON object: set `interaction_pattern`, list `applicable_principles` (the IDs), and record any `override_decisions` with reasons.
7. **MUST verify** by running `make_agent_qc` against the generated spec. The check passes when BD-QC-001 through BD-QC-007 all pass: discipline section present (BD-QC-001), system prompt boilerplate present (BD-QC-002), applicability matches interaction_pattern (BD-QC-003), trust markers in test cases (BD-QC-004), override decisions documented (BD-QC-005), no-override principles all present (BD-QC-006, critical), and if `non_interactive_mode: true`, alert_channel declared (BD-QC-007, critical). Self-attestation does NOT count — actually run the QC.

### Deduplication note — Key Principles vs Behavioral Discipline

Some entries in this template's "Recommended Principles for LLM Agents" subsection (above) materially overlap with discipline principles:

| Recommended Principle (Key Principles) | Discipline Principle | Action |
|---|---|---|
| Propose Before Execute | P-002 Plan Before Acting | If P-002 is in the agent's `applicable_principles`, **drop "Propose Before Execute"** from Recommended Principles. Don't double-emit. |
| Graceful Degradation for Optional Tools | P-003 Stop on Defect (NI surface mechanism) | Keep both — Graceful Degradation addresses the *optional tool not present* case, which is distinct from P-003's halt-on-defect. They complement, don't duplicate. |
| Guardrails as a Separate Layer | (no direct discipline analog) | Keep. |
| Explicit Tool Control, Strict Tool Use, Stop Sequence Control, Temperature, Reasoning Effort, Structured Output vs Function Calling, Prefer MCP Servers | (LLM implementation details) | Keep. These are about *how the LLM is configured*, not how the agent behaves toward users. Discipline is silent on them. |

The general rule: **Key Principles is for this-agent-specific design choices and LLM implementation details. Behavioral Discipline is for cross-cutting interaction discipline.** When a Recommended Principle restates a discipline principle in different words, drop the Recommended Principle to avoid generating a system prompt with two copies of the same instruction.

### What the new agent's MD section looks like — worked examples

The skill substitutes `compact_boilerplate.md_section_template` from the knowledge JSON with the agent's interaction_pattern data. Here are two worked examples:

**Example A — `read_only` agent** (e.g., a documentation Q&A bot):

```markdown
## Behavioral Discipline (core)

This agent follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The principles applicable to this agent type (read_only):

- **P-001 Read Before Claiming** (*Genchi Genbutsu*): Read the actual source before claiming anything about content, code, or system state. *Trigger*: Every claim about content, code, data, or system state.
- **P-003 Stop on Defect** (*Jidoka + Andon*): First failed precondition, malformed input, or unresolved ambiguity → stop and surface. *Trigger*: Any failure or unresolved ambiguity.
- **P-007 Pull, Don't Push** (*JIT + 3 Ms*): Generate exactly what was asked. No speculative features. *Trigger*: Every response.
- **P-008 Mistake-Proof Outputs** (*Poka-yoke + Standard Work*): Format outputs consistently across runs. *Trigger*: Any output a downstream consumer parses or compares.
- **P-009 Reflect, and Tell the User** (*Hansei + Yokoten*): At the end of any task that produced a surprise, name the lesson. *Trigger*: End of any task with non-obvious behavior.
- **P-010 Respect the User's Intent** (*Respect for People + Hoshin Kanri*): Don't substitute the goal; flag drift in long sessions. *Trigger*: Any action beyond the literal request.

**Hard rule on overrides**: before skipping any principle, the agent must state in one sentence which principle is being skipped and why. Principles P-001, P-003, P-007, P-010 have no override.

For full principle definitions, examples, and override rationale, see `knowledge/behavioral_discipline.md`.
```

The skill takes the `read_only.always_include` array directly from the JSON — no add-back step, no special handling. The four no-override principles (P-001, P-003, P-007, P-010) are present in EVERY interaction pattern's `always_include`; this is the `_no_override_invariant` documented in the JSON. Trust the array; don't add or subtract.

**Example B — `single_write_workflow` agent** (e.g., a one-step "update this record" handler):

```markdown
## Behavioral Discipline (core)

This agent follows the behavioral discipline defined in `knowledge/behavioral_discipline.md` and `knowledge/behavioral_discipline.json`. The principles applicable to this agent type (single_write_workflow):

- **P-001 Read Before Claiming** (*Genchi Genbutsu*): Read the actual source before claiming anything. *Trigger*: Every claim about state.
- **P-002 Plan Before Acting** (*Nemawashi + TBP*): Propose what will change, wait for confirmation. *Trigger*: Any state-changing action.
- **P-003 Stop on Defect** (*Jidoka + Andon*): First failure → halt and surface. *Trigger*: Any failure or unresolved ambiguity.
- **P-004 Find the Root Cause** (*5 Whys*): Walk the causation chain on bugs. *Trigger*: Any unexpected behavior.
- **P-006 Document the Change** (*A3*): Structured change report on any non-trivial write. *Trigger*: Any change a reviewer would want to inspect.
- **P-007 Pull, Don't Push**: Only what was asked. *Trigger*: Every change.
- **P-008 Mistake-Proof Outputs**: Consistent output shape. *Trigger*: Parseable outputs.
- **P-009 Reflect, and Tell the User**: Name lessons from surprises. *Trigger*: End of task with non-obvious behavior.
- **P-010 Respect Intent**: Don't substitute the goal. *Trigger*: Any action beyond the literal request.

**Hard rule on overrides**: before skipping any principle, the agent must state in one sentence which principle is being skipped and why. Principles P-001, P-003, P-007, P-010 have no override.

For full principle definitions, see `knowledge/behavioral_discipline.md`.
```

P-005 (Small Steps) is the only principle in `skip_unless_applicable` for this pattern — there's only one step, so decomposition doesn't apply.

**Example C — `multi_step_batch` agent** (e.g., a data migration tool): all 10 principles embedded, no overrides — the heaviest discipline. See `knowledge/behavioral_discipline.json` → `agent_type_applicability.types.multi_step_batch`.

### Non-interactive mode

If the user requests a non-interactive (cron, webhook, scheduled batch) agent, set `io_contract.non_interactive_mode: true` in the new agent's JSON. Then:

1. **Verify an `alert_channel` is declared** in the agent's spec (Slack webhook, monitoring endpoint, email, error log path). Without it, P-003's halt has nowhere to surface to. `make_agent_qc` flags missing alert channels as critical.
2. **Use `non_interactive_mode.principle_surface_mechanisms`** from the knowledge JSON for each applicable principle. The discipline does NOT change — only the surface mechanism does (e.g., "wait for confirmation" → "log plan to runlog and proceed if no defect").
3. **Apply the graduation pattern**: non-interactive mode is opt-in only after the agent has been validated interactively. The make_agent skill should warn the user if they request non-interactive mode for a brand-new agent that hasn't been tested in interactive mode.

### Switching non-interactive mode mid-spec

When a user flips `io_contract.non_interactive_mode` after the agent spec has been initially generated (the common case: built and tested interactively, now graduating to cron/webhook/scheduled batch), the make_agent skill MUST re-run discipline embedding rather than just flipping the JSON flag. A flag-flip-only update produces silent corruption: the system prompt still contains interactive surface mechanism language ("wait for confirmation", "ask the user") while the JSON declares non-interactive — the runtime LLM and the runner (e.g., AgentJ) will disagree about how the agent should behave.

The mid-spec flip checklist:

1. **Halt before flipping the flag**. If `io_contract.alert_channel` is not already declared, ask the user to provide one (Slack webhook, monitoring endpoint, email, error log path). Do NOT flip `non_interactive_mode: true` until alert_channel is set. Without an alert channel, P-003 (Stop on Defect) has nowhere to surface to — the agent halts silently and the user never knows.

2. **Re-embed discipline with NI surface mechanisms**. Replace the interactive language in `implementation.llm_agent.system_prompt` with the corresponding NI versions from `knowledge/behavioral_discipline.json` → `non_interactive_mode.principle_surface_mechanisms`. The principles themselves don't change — only the surface mechanism per principle does. Example: P-002 Plan Before Acting under interactive mode says "propose plan and wait for user confirmation"; under NI mode it says "log plan to runlog before acting; proceed if no defects detected."

3. **Update the agent's JSON**: set `io_contract.non_interactive_mode: true`, set `io_contract.alert_channel: <value>`. No structural change to `behavioral_discipline.applicable_principles` is needed (the principles list is the same; only their surface mechanisms differ).

4. **Re-run make_agent_qc**. Specifically rule 18 (BD-QC-007) — confirm alert_channel is declared and non-empty. Rule 17 should still pass since applicable_principles are unchanged.

5. **Apply the graduation warning**. If `validation.test_cases` is empty or all test cases describe interactive scenarios (no NI runlog format), warn the user that the agent has not been validated under NI mode and propose interactive validation first. NI mode is opt-in only after observed correct behavior under direct supervision.

This produces a deterministic spec state that downstream runners (AgentJ in particular) can consume reliably: `non_interactive_mode: true` + `alert_channel` set + system prompt language matches NI surface mechanisms + QC passing. A spec missing any of these is ambiguous and should not be deployed unattended.

### Retrofit mode: applying the discipline to a pre-discipline agent

When an agent spec exists from before v3.0 (the discipline framework landed in v3.0; agents authored earlier lack the `## Behavioral Discipline (core)` section in MD and the `behavioral_discipline` object in JSON), the make_agent skill MUST support retrofitting the discipline into the existing spec rather than requiring a regenerate. The output is structurally indistinguishable from a greenfield-generated agent — only the entry point differs.

Retrofit checklist (parallel to the integration flow above, but starting from an existing spec):

1. **Read the existing agent fully** — MD + JSON. Note current section structure (some pre-discipline agents use non-standard section names; that's fine, retrofit doesn't rewrite them).

2. **Determine `interaction_pattern`** using the decision flow above. **MUST ask the user to confirm** the pattern rather than silently default. Pre-discipline agents have no declared pattern, so the right value depends on the author's intent — which the user knows and the spec doesn't capture.

3. **Insert `## Behavioral Discipline (core)` in the MD** immediately after `## Key Principles (core)` (or, if Key Principles is absent or named differently, after the section that most closely plays that role — e.g., a "Two-Agent Architecture" or "Workflow" section in a navigation-style spec). Use `compact_boilerplate.md_section_template` from the knowledge JSON, substituted with the confirmed `interaction_pattern`.

4. **Add the `behavioral_discipline` object to JSON** at the top level alongside `agent_type`, `implementation`, `io_contract`, etc. Populate `interaction_pattern`, `applicable_principles` (from `agent_type_applicability.types[<pattern>].always_include`), and `override_decisions` (empty unless overrides apply).

5. **Embed the boilerplate in `implementation.llm_agent.system_prompt`** when the agent type is `llm_agent`. For non-llm types (workflow, api_agent, class_based, etc.), skip this and document the skip in the retrofit report — BD-QC-002 applies only to llm_agent.

6. **Run `make_agent_qc`**. Specifically rules 17 (BD-QC-001 through BD-QC-006) and 18 (BD-QC-007 if non-interactive). Other rules already passed at original generation; the retrofit only adds discipline content.

7. **Don't rewrite anything else**. Per P-007 (Pull, Don't Push), retrofit ONLY adds the discipline section and JSON object. Do not refactor existing pitfalls, reorganize sections, modernize prose, or "improve" anything that wasn't asked. The pre-discipline agent was correct for its time; retrofit makes it discipline-compliant without rewriting it.

The retrofit is also the migration path for `update_agents/*` agents authored before v3.0 (currently failing BD-QC-006 and -001 if make_agent_qc rule 17 is run against them). Once retrofitted, those agents pass BD-QC alongside any greenfield-generated agent.

### When the discipline is over- or under-applied

- **Over-application** (e.g., a read-only inspection agent with full A3 documentation) is a low-severity warning — the agent works, just with unnecessary structure.
- **Under-application** (e.g., a multi-step batch agent missing Stop on Defect) is a high-severity failure. The four no-override principles must be present in every agent regardless of type.

When uncertain about applicability, **default to including all 10 principles with override-when-applicable** rather than skipping principles upfront. Better to over-include (the agent applies overrides) than under-include (the agent never knows the principle existed).

### Where the structured data lives (quick reference)

| What you need | Source |
|---|---|
| Principles by ID with metadata | `knowledge/behavioral_discipline.json` → `principles` |
| Which principles for which agent type | `knowledge/behavioral_discipline.json` → `agent_type_applicability` |
| Boilerplate templates for embedding | `knowledge/behavioral_discipline.json` → `compact_boilerplate` |
| Override rules and no-override list | `knowledge/behavioral_discipline.json` → `override_rules` |
| Non-interactive mode mappings | `knowledge/behavioral_discipline.json` → `non_interactive_mode` |
| Narrative explanation of any principle | `knowledge/behavioral_discipline.md` |

---

## File I/O Mode (core)

Every agent built from this template must declare how it consumes input. AgentJ (the runner) reads this declaration to render the right UI control — textarea, single file picker, or folder picker. **Paths are never hardcoded** in the spec; the user supplies them at run time.

Answer one question during spec building:

> **Does this agent operate on a single text input, a single file, or a folder of files?**

The answer drives the `io_contract.inputs[].type` value in the JSON and the system-prompt boilerplate at the top of this MD.

| Mode | `type` value | System prompt boilerplate |
|------|--------------|---------------------------|
| Single text input (default) | `"string"` | No boilerplate needed — agent receives text directly |
| Single file | `"file"` | "You will be invoked once with the contents of a single file passed as your user input. Process it and return your output as plain text." |
| Folder of files | `"folder"` | "You will be invoked once per file in the input folder. The contents of one file will be passed as your user input on each invocation. Process that single file and return your output. Do not assume context from other files — each invocation is independent." |

**For folder mode**, also declare a `file_filter` glob pattern (e.g. `"*.docx,*.pdf"`) so AgentJ skips non-matching files. See `<your_agent_name>.json` → `io_contract.inputs[]` for the schema.

> **Why this matters**: A folder-mode agent whose system prompt is written as if it sees the whole folder will produce wrong output on every invocation. The mode declaration in JSON and the boilerplate in MD must match — QC enforces this.

---

## Domain Terms (optional — use for domain-heavy agents)
Define non-obvious vocabulary the agent and user must share before work starts. Omit for simple agents with self-evident terminology. Include when ambiguous terms would cause the agent to make wrong assumptions (e.g., custom index names, external system IDs, domain-specific labels).

| Term | Definition |
|------|------------|
| `[TERM]` | [What it means in this agent's context — not the dictionary definition] |
| `[TERM]` | [Include any aliases or common confusions] |

**When to add a term**: If the agent could interpret the word two different ways and choose the wrong one, it belongs here.

---

## Core Concepts (optional for complex agents)
Add only if the agent needs deeper narrative explanation (2–4 concepts). Otherwise omit.

---

## How to Use This Agent (core)

### Prerequisites
- [Required knowledge, tools, or environment setup]
- [Dependencies or API keys needed]
- [Data sources or files required]

### Existing Tooling (include when integrating with an existing codebase)
Before building new tools, document what already exists that this agent should reuse. This prevents reinventing wheels and tells the agent which files are authoritative.

| Tool / File | Purpose | When to use |
|---|---|---|
| `[script or file path]` | [What it does] | [When the agent should call or reference it] |

**Reuse-first rule**: If a script, template, or utility already exists in the project that covers a needed operation, use it rather than generating new code. Document any flags or options the agent needs to know (e.g., `--strip-reader` mode, `--dry-run`).

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

### 9. Conflating Server Tools and Client Tools

**Problem**: An agent that uses both server tools (e.g., Anthropic's `web_search`, `code_execution`) and client tools (custom tools the caller implements) treats them identically — and breaks when the runtime behavior differs.

**Why it happens**: Server tools execute on the platform side and return results within a single API turn. Client tools require the agent to halt, return a `tool_use` block to the caller, wait for the caller's runtime to execute the tool, and resume with a `tool_result` block. Mixing them without recognizing the distinction leads to: client-tool calls that never resume because the runtime didn't implement the handler; server-tool results being re-executed by the client runtime; or `tool_choice` forcing a client tool that is actually a server tool name (or vice versa).

**Solution**: In `implementation.llm_agent.tools[]`, mark each tool with its execution location (server vs. client) — either as a `_meta.execution` field or by separating them into two arrays. In the system prompt, distinguish them when behavior matters ("the `web_search` tool returns results in this turn; the `fetch_from_db` tool will pause execution for the runtime to fetch"). When configuring `tool_choice` to a specific tool name, verify which side executes it before setting it.

### 10. Lowering Temperature on Gemini 3 Models

**Problem**: Following the "Temperature by Agent Mode" principle (set 0.0–0.2 for tool-calling agents), a practitioner sets `temperature: 0.1` on a Gemini 3 model. The agent then loops on multi-step reasoning, returns degraded output on math-heavy tasks, or fails intermittently in ways that are absent at the default temperature.

**Why it happens**: Gemini 3 was tuned at the default temperature of 1.0. Google's text-generation and function-calling docs both carry an explicit warning: "When using Gemini 3 models, we strongly recommend keeping the `temperature` at its default value of 1.0. Changing the temperature (setting it below 1.0) may lead to unexpected behavior, such as looping or degraded performance, particularly in complex mathematical or reasoning tasks." The "Temperature by Agent Mode" recommendation reflects convergent guidance from Anthropic, Google (pre-Gemini-3), and xAI for deterministic tool selection — it does not apply to Gemini 3 specifically.

**Solution**: Treat the temperature recommendation as model-family-conditional. For Anthropic, OpenAI, xAI, and Gemini ≤ 2.5 tool-calling agents, low temperature (0.0–0.2) is correct. For Gemini 3 tool-calling agents, leave `temperature` at the default 1.0 unless you have measured that lowering it improves your specific workload — and even then, document the choice with a test result. Record the model and chosen temperature in `implementation.llm_agent.parameters` so the choice is auditable.

### 11. [Additional Pitfalls]

Document common pitfalls based on expected usage. Focus on mistakes that:
- Are easy to make
- Have non-obvious causes
- Can be explained better in narrative than in code alone

> **Note**: Pitfalls describe agent design and usage mistakes. Non-obvious quirks of external systems the agent interacts with (API behavior, data format surprises, undocumented edge cases) belong in **External System Lessons** below, not here. Mixing them dilutes both.

---

## External System Lessons (optional — use when agent interacts with external APIs or systems)

Hard-won knowledge about the external systems this agent operates on. These are not agent design mistakes — they are non-obvious behaviors of external systems that will cause silent failures or wrong results if the agent doesn't know about them. Discovered through real usage, not documentation.

### [System Name] — [Topic]

**Behavior**: [What the system does that is surprising]

**Why it matters**: [What goes wrong if the agent doesn't know this]

**How to handle it**: [The correct approach]

**Example**:
```
Classic quiz points (Canvas API): Creating a quiz sets points_possible to 0 on the linked
assignment until you explicitly PUT the quiz with points_possible. The gradebook shows 0
until this second call is made — it is not a bug, it is a required second step.
```

> Add one entry per non-obvious external system behavior. Sourced from real failures, not guessed from docs.

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

## Quality Bar (optional — use for agents with output standards)

The minimum standard every response from this agent must meet before it is considered done. This is not a test suite — it is a professional checklist the agent applies to itself on every turn. Distinct from validation test cases, which are run once to verify the agent works.

Include this section when the agent produces output that instructors, students, colleagues, or systems will consume directly and quality drift would cause real harm.

- [ ] [Output standard 1 — concrete and checkable, e.g. "No duplicate content between two locations"]
- [ ] [Output standard 2 — e.g. "All dates include timezone"]
- [ ] [Output standard 3 — e.g. "Spot-check ambiguous API responses before reporting success"]
- [ ] [Output standard 4]

> Keep this list short (3–6 items). If it grows beyond 6, the agent's scope is too broad.

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
| **Agent Type** (implementation) | [class_based\|workflow\|llm_agent\|api_agent\|data_processor\|multi_agent\|rule_based\|other] |
| **Interaction Pattern** (behavior) | [read_only\|single_write_workflow\|multi_step_batch\|single_call_api\|conversational] — see `## Behavioral Discipline (core)` for the orthogonal-classifications table and decision flow |
| **Complexity** | [simple\|standard\|complex] |
| **Key Files** | `<your_agent_name>.json`, `<your_agent_name>.md` |
| **Quickstart** | `agent = Agent.from_config('agent.json'); result = agent.process(input)` |
| **Common Pitfall** | [#1 mistake to avoid] |
| **Dependencies** | [Key packages or APIs] |

For detailed information, see sections above and `<your_agent_name>.json`.
