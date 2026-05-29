# NGAI Agent Spec Templates

This guide explains how to use documentation templates to create a purpose-built "Agent Spec", turning a General AI into a Non-General AI specialist for a specific task. This guide assumes you are using an AI-powered CLI to assist you.

## First-Time User? Start Here (2 min read)

The workflow in this guide uses a Command-Line Interface (CLI) to have a conversation with an AI, like the one you're using now. If this is your first time working this way, the concept is simple:

1.  **You give a command in plain English.** (e.g., "Create a new agent spec for a translator.")
2.  **The AI understands the goal and uses its tools** to perform actions (e.g., creating files `translator.json` and `translator.md`).
3.  **You review the result** and provide the next instruction.

For a fantastic and detailed visual explanation of how AI works in a CLI, we highly recommend watching this video from Network Chuck. It's the perfect "Level 0" introduction.

➡️ **Watch: [Network Chuck Explains AI in the CLI](https://www.youtube.com/watch?v=placeholder_video_id)** *(Please replace this placeholder link with the actual video URL.)*

Once you're comfortable with the basic idea, this guide's **Quickstart** will be your "Level 1" guide for the specific task of creating agent specs.

## How to Talk to Your AI About Agent Specs (3 min read)

Once you've set up your AI CLI (as Network Chuck explains), you'll be ready to tell it how to use these templates. Think of each `make_agent` template (`make_agent.json` and `make_agent.md`) as defining a **meta-skill** for your AI: the skill of *creating other agent specs*.

You'll guide your AI by telling it to "adopt" this skill and then provide the specific details for the new agent you want to document.

### Common Prompting Patterns:

1.  **To start a new spec (like the Quickstart):**
    > "Use the 'Agent Spec Creation' skill defined by the `make_agent.json` and `make_agent.md` templates. Create a new Tier 1 agent spec for a 'Simple Summarizer'. The agent's code will be in `src/agents/summarizer.py`."

    *Your AI should then begin a conversational flow, asking you for the details required to fill the spec.*

2.  **To edit an existing spec:**
    > "Using the `Agent Spec Creation` skill, load the existing spec for 'MyTranslator' (`translator.json` and `translator.md`). Update the mission in `translator.md` to clarify its purpose for legal documents."

3.  **To ask for validation:**
    > "Using the `Agent Spec Creation` skill, review the `my_agent.json` spec. Does it conform to Tier 2 requirements for a production agent? Provide a concise summary of any missing fields."

4.  **To understand a spec:**
    > "Using the `Agent Spec Reading` skill, summarize the key principles and pitfalls defined in the `my_agent.md` file."

The key is to give your AI a clear directive ("Use this skill...") and then provide the context ("...for this agent..."). The more clearly you define the task, the better your AI can assist you.

---

## Why Per-Repo Agents — and How This Compares to Hermes / OpenClaw

Tools like **Hermes** (Nous Research) and **OpenClaw** are powerful — they're full **agent systems** you install and run: a CLI, a daemon, a gateway process for Telegram/Discord, a centralized skills store in `~/.hermes/` or `~/.openclaw/`. Worth it if you want an unattended assistant that pings you on Telegram from a $5 VPS.

NGAI takes the opposite shape: **portable agent specs that live in your repo and activate in whatever AI tool you already use.**

| | Hermes / OpenClaw | NGAI (this repo) |
|---|---|---|
| **Install** | uv, Python 3.11, Node.js, ffmpeg, MinGit, then the system itself; configure a provider, a gateway, and skills | **Zero.** Use whatever agentic CLI you already have — Claude Code, Cursor, Aider, Antigravity, etc. |
| **Where the agent lives** | A centralized store (`~/.hermes/skills/`) shared across projects | **In your repo,** as `agent.md` + `agent.json`. Each repo's agent is the repo's agent. |
| **Activation** | Run the system, talk to its CLI or gateway | **Open the repo in your tool.** The `AGENTS.md` *is* the agent's role — your tool reads it and acts on it. |
| **Lock-in** | Skills run in Hermes (or OpenClaw via migration) | **Open standard.** `AGENTS.md` is tool-agnostic; the same spec runs anywhere it's read. |
| **Maintenance** | Daemons, gateway processes, upgrades, dependency churn | **None of yours.** The host tool maintains itself. |
| **Unattended automation** (Telegram capture, cron) | ✅ Built-in | ❌ Not in this repo — but the sibling **[AgentJ](https://github.com/chaz-clark/agentj)** runs NGAI specs on a schedule when you want that. |

**The trade is deliberate.** NGAI gives up Hermes-style ambient presence (Telegram bots, gateway processes, $5-VPS daemons) in exchange for three things its audience values more:

- **Zero install for the user.** Non-technical faculty, students, and professionals using whatever AI tool is already on their laptop don't need to set anything up — they clone the repo and open it.
- **Per-project isolation by construction.** No global skill store to clobber across projects; each repo carries its own specialist.
- **True tool-portability.** Google's April 2026 *Gemini Enterprise Agent Platform* standardized on the exact shape NGAI uses — *"subagents as Markdown + YAML in a repo, storable in a repository, enabling teams to standardize and version specialized agents."* The [Hermes Kanban v1 spec](https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf) (§1.3) explicitly names this as a gap in their own approach — *"No portable file artifact yet."* NGAI already has the portable file artifact, deployed at the personal-and-educational scale instead of enterprise.

**Use Hermes / OpenClaw** if you're building an unattended Telegram-pingable assistant on a cloud VM.
**Use NGAI** if you want repos that come with their own AI specialist, run in whatever tool you and your audience already use, and stay portable across tools. For scheduled or background execution, layer in **AgentJ** — it runs the same specs without changing anything in them.

---

## The NGAI Workflow (The "How")

This is a **documentation-driven workflow** where you instruct an AI assistant to generate a complete agent spec for you.

**Your Role**: Provide the core logic and review the AI's output.
**AI's Role**: Generate the boilerplate `.json` and `.md` files, fill in the details based on your instructions, and help you validate.

```
YOU: "Let's create a spec for a new Summarizer agent."
 │
 ▼
AI: Creates `summarizer.json` & `summarizer.md` from templates.
 │
 ▼
YOU: "The agent is an LLM agent. Its input is 'text', output is 'summary'."
 │
 ▼
AI: Fills `agent_type` and `io_contract` in the JSON.
 │
...and so on.
```

**Result**: A complete, consistent, and validated Agent Spec, created via conversation.

## Quickstart: Building Your First Agent Spec with an AI CLI

This 15-minute process guides you in directing an AI assistant to create your agent spec.

### Step 1: Initialize the Spec (Your Prompt to the AI)
> **Your Prompt:**
> "Using the `make_agent` templates, create a new Tier 1 agent spec for a 'Simple Summarizer'. The agent's code will be in `src/agents/summarizer.py`."

### Step 2: Define the Core Contract (A Conversation)
> **AI Asks:** "What is the implementation type for this agent?"
>
> **Your Response:** "This is an `llm_agent`."
>
> **AI Asks:** "What is the I/O contract?"
>
> **Your Response:** "The input is a string named 'text'. The output is a string named 'summary'."

### Step 3: Provide Key Data & Validation
> **Your Prompt:**
> "The primary data is a system prompt: 'You are a very concise summarizer.'"
>
> "For validation, add a test case where the input text is '...' and the expected output is '...'. The command to run the test is `pytest tests/test_summarizer.py`."

### Step 4: Generate the Narrative
> **Your Prompt:**
> "Now, for the `summarizer.md` file: The mission is to summarize long text using GPT-4. Add a pitfall about avoiding texts longer than 10K tokens."

### Step 5: Review and Validate
The AI has now generated both files. Your final step is to review them for accuracy and run the validation command you provided.

---

*The rest of this README provides the detailed context (Tiers, Design Rationale, FAQs) that the AI will use as its own reference to complete your requests.*

## Keeping Templates Current

All `make_*` templates are kept up to date with evolving AI platform best practices using a two-agent documentation update system plus a raw-HTTP fetch utility:

| Component | Files | What it does |
|-------|-------|-------------|
| **Doc Refresh Agent** | `update_agents/doc_refresh_agent.md` / `update_agents/doc_refresh_agent.json` | Spec for the refresh workflow (staleness → fetch → validate → write → report). Uses `fetch_doc.py` as its fetcher. |
| **Doc Analysis Agent** | `update_agents/doc_analysis_agent.md` / `update_agents/doc_analysis_agent.json` | Reads cached docs, diffs against templates using an intent-first reading protocol, and proposes minimal additive improvements — always updating both the `.json` and companion `.md` together |
| **fetch_doc.py** | `update_agents/fetch_doc.py` | Raw-HTTP fetcher with 5 modes (default fetch, `--list-links`, `--batch`, `--from-html`, `--check`). Replaces the prior WebFetch+manual-save flow; validated as a byte-identical drop-in across 5 platforms (2026-05-13). Run via `uv run update_agents/fetch_doc.py <url>`. |

**Typical cadence**: Run `doc_refresh_agent` monthly (or after a major platform release), then run `doc_analysis_agent` to surface any proposals worth adding to the templates.

```
fetch_doc.py       →  raw-HTTP fetcher (or --from-html for JS-rendered sources)
doc_refresh_agent  →  orchestrates fetch_doc.py calls; updates source_docs/ cache
doc_analysis_agent →  proposes scored changes; each JSON change paired with companion MD update
make_agent_qc      →  validates templates (20 rules, 17 dimensions, including MD/JSON companion sync and ORCH-QC + KNW-QC families)
```

Cached source documentation lives in `source_docs/` (35 files as of 2026-05-13, across Anthropic, Google ADK/Gemini, OpenAI, and xAI). See `update_agents/update_agent.md` for a quick navigation guide to both agents and the fetch tool.

---

## What This Is (and Isn't)

**This is a documentation template system** for NGAI agents, designed to be used with an AI assistant.

**You implement**: Your agent's actual code (Python, JS, etc.).
**We provide**: Templates that an AI can fill on your behalf to document your agent consistently.

## Suggested folder layout (your project)
```
project/
├── src/agents/
│   └── <agent>.py                # Your implementation
├── docs/agents/
│   ├── <agent>.json              # Agent definition (this template)
│   └── <agent>.md                # Agent narrative (this template)
└── tests/
    └── test_<agent>.py           # Reference validation.test_cases from JSON
```

## This repo's structure
```
Make-AI-Agents/
├── AGENTS.md                          # project context for any agentic dev tool (canonical)
├── make_agent.md / .json              # Agent spec template (the meta-skill)
├── make_agent_qc.md / .json           # Agent spec QC template (20 rules, 17 dimensions)
├── make_AGENTS.md / .json             # AGENTS.md generation template
├── make_AGENTS_qc.md / .json          # AGENTS.md QC template
├── make_orchestrator_agent.md / .json # Multi-agent orchestrator template (2026-05-13)
├── make_agent_knowledge.md / .json    # Runtime knowledge file template (2026-05-13)
├── make_gems/                         # Gemini Gem templates (sibling to make_agent)
│   ├── make_gem.md / .json
│   └── make_gem_qc.md / .json
├── knowledge/                         # Source-of-truth + generated knowledge files
│   ├── behavioral_discipline.md       # Toyota Way + Karpathy framework — narrative
│   ├── behavioral_discipline.json     # Same — structured rules for skill consumption
│   └── source_docs_index.{md,json}    # Reference-shape catalog of the 35 cached platform docs
├── update_agents/                     # Doc refresh + analysis agents + fetch utility
│   ├── update_agent.md / .json
│   ├── doc_refresh_agent.md / .json
│   ├── doc_analysis_agent.md / .json
│   ├── doc_refresh_workflow.md / .json   # Orchestrator (multi_agent) coordinating the refresh
│   ├── merge_agent.md / .json            # Single agent: merges dropbox stagings → source_docs
│   └── fetch_doc.py                   # Raw-HTTP doc fetcher (5 modes, 2026-05-13)
└── source_docs/                       # 35 cached platform docs (Anthropic/Google ADK/OpenAI/xAI)
```

## Tier System (choose based on your needs)

**Tier 1 (Core)** - *For prototypes, internal tools.* (15 min)
**Tier 2 (Production)** - *For shared, deployed services.* (25 min)
**Tier 3 (Complex)** - *For frameworks, platform components.* (40 min)

(See `make_agent.json` for full details on which fields belong to which tier).

## Behavioral Discipline (baked into every agent)

Every agent built from `make_agent.md` inherits a behavioral discipline drawn from the **Toyota Production System** (system-level discipline) reinforced by **Andrej Karpathy's four coding-agent guidelines** (worker-level habits). The discipline produces agents that are visible, predictable, and correctable — the three properties end users need in order to extend trust.

The source of truth lives in `knowledge/`:

- **`knowledge/behavioral_discipline.md`** — narrative explanation of the 10 principles (P-001 through P-010), the foundation, when to deviate, and how it composes with `karpathy-guidelines`.
- **`knowledge/behavioral_discipline.json`** — structured rules that `make_agent` reads when generating new agents: which principles apply to which agent type, the trust markers QC checks for, override rules, the compact boilerplate template, and non-interactive (cron/webhook) mode mappings.

The discipline includes principles like:
- **Read Before Claiming** (Genchi Genbutsu) — read the actual source, don't theorize from priors
- **Plan Before Acting** (Nemawashi + TBP) — propose the plan, wait for confirmation
- **Stop on Defect** (Jidoka + Andon) — first failure, halt and surface
- **Document the Change** (A3) — structured one-page change reports
- **Reflect, and Tell the User** (Hansei) — name the lesson where future sessions see it

`make_agent` picks the applicable subset based on agent type (read-only vs multi-step batch vs single-call API vs conversational). `make_agent_qc` validates that new agents have adopted the discipline appropriately for their type. See `knowledge/behavioral_discipline.md` → "How agents inherit this" for the full mechanism.

The discipline propagates across the meta-skill family:

- **`make_agent` / `make_agent_qc`** — bake all 10 principles into agent specs based on declared `interaction_pattern`.
- **`make_gem` / `make_gem_qc`** — bake the Gem-tailored subset (P-001, P-003, P-007, P-008, P-009 partial, P-010) into Gemini Gem instructions. See `make_gems/make_gem.md` → "Behavioral Discipline for Gems (core)".
- **`make_AGENTS` / `make_AGENTS_qc`** — embed the discipline pointer in every generated `AGENTS.md` (project-level context file). The Gem and AGENTS QC skills delegate to the same canonical BD-QC checks in `knowledge/behavioral_discipline.json` — no rule duplication.

## Optional sections in agent specs

Beyond the core sections, `make_agent.md` supports several optional sections that earn their place when relevant:

- **Domain Terms** — vocabulary table for agents operating in domains with non-obvious terminology
- **Existing Tooling** — reuse-first inventory when integrating with an existing codebase
- **External System Lessons** — hard-won knowledge about external systems' non-obvious behavior (distinct from agent-design pitfalls)
- **Quality Bar** — per-response professional standards checklist (distinct from validation test cases)
- **File I/O Mode** — declare whether the agent operates on a single text input, a single file, or a folder of files (drives downstream tooling like AgentJ to render the right UI control)

## Why this design (alternatives considered)

### 1. Hybrid Split (JSON + MD)
**Problem**: How to store both structured data AND narrative context?
**Result**: Machines parse JSON for contracts, humans read MD for mission. AI agents process JSON 3x faster.

### 2. Tiered Fields (3 tiers)
**Problem**: How to support simple prototypes AND complex production agents?
**Result**: One template adapts. Reduces completion time by 60% for simple agents.

### 3. One Validation Block (consolidated)
**Pain point**: "Which test is the source of truth?"
**Result**: Single source of truth. Tests stay in sync with agent definition.

## Common Questions (FAQ)

### Q1: How is this different from OpenAPI/Swagger?
**A**: OpenAPI documents REST APIs. This documents entire **agents**, including behavior, prompts, logic, and validation.

### Q2: Do I need an AI CLI to use this?
**A**: No, you can still copy and edit the templates manually. However, the workflow is designed to be **10x faster** when used with an AI assistant that can parse the templates and fill them based on conversation.

### Q3: Where does the "loader" code from the old README go?
**A**: The concept is the same, but the AI assistant will typically handle the loading and instantiation as part of its internal process, guided by your spec. Your `validation.commands` should point to a script that performs a real-world test.