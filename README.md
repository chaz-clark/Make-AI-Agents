# Make AI Agents

A set of templates that turn the AI tool you already use — Claude Code, Cursor, Codex, Antigravity, GitHub Copilot — into a specialist for the project in your current repo. Drop the templates into your repo, point your AI at them, and your AI behaves like the specialist they describe. No daemon to install, no system to maintain, no vendor account holding the definition hostage.

Built for developers, designers, and faculty who want their AI assistant to consistently behave like a specialist for a specific project — and want that "specialist definition" to live with the code, not in a vendor account.

---

# What you can do with it

- **Generate a new agent spec** without writing JSON yourself — describe the agent in conversation, the AI fills the templates for you
- **Make your project's AI specialist portable** across Claude Code, Cursor, Aider, Antigravity, Codex, and any other tool that reads `AGENTS.md`
- **Validate a spec is production-ready** with a 20-rule QC pass that checks behavior, contracts, pitfalls, and test cases
- **Generate your project's `AGENTS.md`** so every AI tool that opens the repo gets the same project context, automatically
- **Generate runtime knowledge files** — glossaries, principles, or playbooks the agent consults at execution time
- **Document a multi-agent orchestrator** with the same template family the individual specs use
- **Build the same shape Google's Gemini Enterprise Agent Platform standardized on** in April 2026: portable agent definitions as `Markdown + YAML`, versioned in the repo

Full template index lives at the bottom of this file under [This repo's structure](#this-repos-structure).

---

# Getting started

Three small choices and the templates are usable:

1. **Pick an IDE** — the app where you open files and talk to your AI assistant.
2. **Pick an AI assistant** — use whichever subscription you already have, so you don't pay twice.
3. **Get the templates into your project** — your AI walks you through it (recommended), or do the steps yourself.

You don't have to be a frameworks expert. The AI handles the structural bits; you describe the agent you want.

---

## Step 1 — Pick your IDE

An **IDE** is the app you'll work in. Pick one, download it, install it like any other application.

| If you… | Use | Free? | Download |
|---|---|---|---|
| **have no strong preference** *(the safe default)* | **Visual Studio Code** — the standard, with the largest selection of AI assistant extensions | yes | [code.visualstudio.com](https://code.visualstudio.com/) |
| **want the AI to drive** *(and want a generous free option built in)* | **Antigravity IDE** — Google's agent-first IDE; Gemini is built in, no separate extension needed | yes (public preview, full Gemini 3 Pro) | [antigravityide.org](https://antigravityide.org/) |
| **work in R / Python / Quarto** | **Positron** — Posit's data-science IDE, with built-in *Positron Assistant* | yes | [positron.posit.co](https://positron.posit.co/download.html) |

> ⚠️ **About Antigravity IDE:** it has Gemini built in and is locked to Gemini — you cannot plug a ChatGPT, Claude, or Copilot subscription into it. Pick Antigravity if you're happy using Gemini. If you have a ChatGPT, Claude, or Copilot subscription you want to use, pick **Visual Studio Code** here and the matching extension in Step 2.

---

## Step 2 — Pick your AI assistant

Use the subscription you **already have** so you don't pay twice. In your IDE, open the **Extensions panel**, search by the name below, click **Install**, then **sign in** when it prompts you.

| You already have… | Install this | Sign in with | Link |
|---|---|---|---|
| **ChatGPT** *(Plus / Pro / Business / Edu / Enterprise)* | **Codex – OpenAI's coding agent** | your ChatGPT account | [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt) |
| **Claude** *(Pro / Team / Max)* | **Claude Code** *(official Anthropic extension)* | your Claude account | [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) |
| **GitHub Copilot** | **GitHub Copilot** + **GitHub Copilot Chat** | your GitHub account | [Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) · [Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) |
| **None of those** | Use **Antigravity IDE** instead of VS Code (from Step 1) — it's free, no extension to install, Gemini is built in | a Google account | [antigravityide.org](https://antigravityide.org/) |

> 💡 **Common mix-up:** GitHub Copilot is a *separate* Microsoft/GitHub subscription — it does **not** connect to a ChatGPT account. If you have ChatGPT Plus, install **Codex** (first row); if you have Copilot, install **Copilot** (third row).

> 📓 **Positron users:** Positron has a built-in **Positron Assistant** — skip Step 2 and go to Step 3.

---

## Step 3 — Get the templates into your project

Pick the path that fits your comfort level. Most people use Option A.

### Option A — Start here: your agent sets it up

Open your existing project in the IDE you set up in Steps 1-2, then give your AI assistant this prompt:

> *"Help me set up Make AI Agents so I can document my project's agents. The templates are at https://github.com/chaz-clark/Make-AI-Agents — please clone the repo into a `Make-AI-Agents/` folder, gitignore it, and read its `AGENTS.md` so you know how to use the templates."*

The agent clones the repo, adds the gitignore line, reads the templates, and is ready to help. You just answer its questions.

### Option B — Manual setup

```bash
git clone https://github.com/chaz-clark/Make-AI-Agents.git
echo "Make-AI-Agents/" >> .gitignore
```

Then open your project in your IDE. Any AI tool that supports the `AGENTS.md` convention (see the table further down) will discover the templates automatically — you just have to ask for them by name in conversation.

### Option C — A colleague is setting it up for you

You just need to describe the agent you want — what it should do, what its input is, what its output is, and a one-sentence mission. They'll do the rest.

---

# Your first agent spec (5-minute walkthrough)

**Goal:** end this walkthrough with two files in your project — `summarizer.json` (the structured contract) and `summarizer.md` (the narrative mission) — that any AI tool can read to make itself act like your "Simple Summarizer" specialist.

**Ask your agent:**

> *"Use the Make AI Agents templates to create a new Tier 1 agent spec for a 'Simple Summarizer'. The implementation will be at `src/agents/summarizer.py`."*

*Tier 1 is the smallest tier — minimal fields, ~15 minutes total to fill. (See the [Tier System](#tier-system) for when to use Tier 2 or 3.)*

Your agent will then start asking for the details. A typical conversation:

> **AI:** "What kind of agent is this — LLM-backed, code-only, or hybrid?"
>
> **You:** "LLM-backed."
>
> **AI:** "What's the input and output contract?"
>
> **You:** "Input is a string named 'text'. Output is a string named 'summary'."
>
> **AI:** "What's the system prompt?"
>
> **You:** "*You are a very concise summarizer.*"
>
> **AI:** "Any validation test cases?"
>
> **You:** "Given a 1000-word article, the summary should be ≤ 200 chars. Test command: `pytest tests/test_summarizer.py`."

Then for the narrative:

> *"For the `summarizer.md` companion: the mission is to summarize long articles using GPT-4. Add a pitfall about texts longer than 10K tokens."*

**Result:** two files now live in your project. Any AI tool that opens the repo reads them and acts as the Simple Summarizer specialist.

To validate the spec is production-ready, ask:

> *"Run the make_agent QC checks against `summarizer.json`."*

That runs 20 quality rules over the spec and reports any gaps.

---

# Common things to ask your agent

Once the templates are in your project, this is the everyday vocabulary. Same pattern: state the outcome, not the file path. The AI finds the template.

| You want to… | Ask your agent (example) |
|---|---|
| **Create a new agent spec** | *"Create a new Tier 1 agent spec for a code reviewer. The implementation will be at `src/agents/code_review.py`."* |
| **Edit an existing spec** | *"In my `translator.md`, update the mission so it focuses on legal documents."* |
| **Validate a spec** | *"Run the make_agent QC checks against `my_agent.json`. Tier 2 production rules."* |
| **Generate or refresh `AGENTS.md`** | *"Generate an `AGENTS.md` for this project."* or *"Refresh the `AGENTS.md` so it reflects recent changes."* |
| **Generate a knowledge file the agent consults at runtime** | *"Create a procedural-shape knowledge file at `knowledge/incident_playbooks` for the on-call agent."* |
| **Understand an existing spec** | *"Summarize the key principles and pitfalls in `my_agent.md`."* |

The pattern is: state what you want to be true, the AI uses the templates to make it true.

---

# Using with AI coding tools

This repo's templates are read by any AI tool that supports the `AGENTS.md` convention. With the `Make-AI-Agents/` clone in your project root, the AI tool discovers the templates when you open the repo.

| Tool | How it loads |
|---|---|
| Claude Code, Cursor, Aider, Antigravity, Codex, Windsurf, Zed, Amp | Automatic — just open the repo |
| VS Code + GitHub Copilot | Set `chat.useAgentsMdFile: true` in user settings (one-time) |
| Gemini Enterprise Agent Platform | Native — Google standardized on this exact shape in April 2026 |

Once loaded, ask in conversation. Outcome-language, not file paths.

---

# What this is (and what it isn't)

**This is** a documentation template system for AI agents — Markdown + JSON files that any agentic AI tool reads as instructions.

- **You implement** the agent's actual code (Python, JavaScript, whatever).
- **The templates** are how the AI tool consistently knows what your agent is, what it does, and how to validate it.

**This is NOT** a runtime. It doesn't ship to production. It doesn't run agents. It doesn't install a daemon. It's a specification layer the AI tool reads — the actual execution happens in your code and your AI tool.

If you need *scheduled / background* execution of the same specs (cron jobs, Telegram bots, webhooks), the sibling project **[AgentJ](https://github.com/chaz-clark/agentj)** runs Make-AI-Agents specs on a schedule without changing anything in them.

---

## Suggested folder layout (your project)

```
project/
├── Make-AI-Agents/                 # the templates (clone-and-gitignore)
├── src/agents/
│   └── <agent>.py                  # your implementation
├── docs/agents/
│   ├── <agent>.json                # agent definition (this template)
│   └── <agent>.md                  # agent narrative (this template)
└── tests/
    └── test_<agent>.py             # references validation.test_cases from JSON
```

## This repo's structure

```
Make-AI-Agents/
├── AGENTS.md                          # project context for any agentic dev tool (canonical)
├── make_agent.md / .json              # agent spec template (the meta-skill)
├── make_agent_qc.md / .json           # agent spec QC template (20 rules, 17 dimensions)
├── make_AGENTS.md / .json             # AGENTS.md generation template
├── make_AGENTS_qc.md / .json          # AGENTS.md QC template
├── make_orchestrator_agent.md / .json # multi-agent orchestrator template (2026-05-13)
├── make_agent_knowledge.md / .json    # runtime knowledge file template (2026-05-13)
├── make_gems/                         # Gemini Gem templates (sibling to make_agent)
│   ├── make_gem.md / .json
│   └── make_gem_qc.md / .json
├── knowledge/                         # source-of-truth + generated knowledge files
│   ├── behavioral_discipline.md       # Toyota Way + Karpathy framework (YAML frontmatter + narrative)
│   └── source_docs_index.{md,json}    # reference-shape catalog of the 35 cached platform docs
├── update_agents/                     # doc refresh + analysis agents + fetch utility
│   ├── update_agent.md / .json
│   ├── doc_refresh_agent.md / .json
│   ├── doc_analysis_agent.md / .json
│   └── fetch_doc.py                   # raw-HTTP doc fetcher (5 modes, 2026-05-13)
└── source_docs/                       # 35 cached platform docs (Anthropic / Google ADK / OpenAI / xAI)
```

---

# Tier system

Pick the tier that matches what you're building. The template adapts:

- **Tier 1 (Core)** — *prototypes, internal tools.* ~15 min to fill.
- **Tier 2 (Production)** — *shared, deployed services.* ~25 min to fill.
- **Tier 3 (Complex)** — *frameworks, platform components.* ~40 min to fill.

See `make_agent.md` YAML frontmatter and tier guidance sections for which fields belong to which tier.

---

# Behavioral discipline (baked into every agent)

Every spec generated by `make_agent` inherits a behavioral discipline drawn from the **Toyota Production System** (system-level) reinforced by **Andrej Karpathy's four coding-agent guidelines** (worker-level habits). The discipline produces agents that are **visible** (you see what they do), **predictable** (no silent claims), and **correctable** (failures halt and surface).

Full detail — the 10 principles (P-001 through P-010), when each applies, when each can be overridden — lives at [`knowledge/behavioral_discipline.md`](knowledge/behavioral_discipline.md). The `make_agent_qc` skill validates new specs against the BD-QC family (BD-QC-001 through BD-QC-009).

The discipline propagates across the meta-skill family:

- **`make_agent` / `make_agent_qc`** — bake all 10 principles into agent specs based on declared `interaction_pattern`.
- **`make_gem` / `make_gem_qc`** — bake the Gem-tailored subset into Gemini Gem instructions.
- **`make_AGENTS` / `make_AGENTS_qc`** — embed the discipline pointer in every generated `AGENTS.md`.

The Gem and AGENTS QC skills delegate to the same canonical BD-QC checks — no rule duplication.

---

# Optional sections in agent specs

Beyond the core sections, `make_agent.md` supports several optional sections that earn their place when relevant:

- **Domain Terms** — vocabulary table for agents in domains with non-obvious terminology
- **Existing Tooling** — reuse-first inventory when integrating with an existing codebase
- **External System Lessons** — hard-won knowledge about external systems' non-obvious behavior (distinct from agent-design pitfalls)
- **Quality Bar** — per-response professional standards checklist (distinct from validation test cases)
- **File I/O Mode** — declare whether the agent operates on a single text input, a single file, or a folder of files (drives downstream tooling like AgentJ to render the right UI control)

---

# Why this design (alternatives considered)

### 1. Hybrid Split (JSON + MD)
**Problem**: How to store both structured data AND narrative context?
**Result**: Machines parse JSON for contracts, humans read MD for mission. AI agents process JSON 3x faster.

### 2. Tiered Fields (3 tiers)
**Problem**: How to support simple prototypes AND complex production agents?
**Result**: One template adapts. Reduces completion time by 60% for simple agents.

### 3. One Validation Block (consolidated)
**Pain point**: "Which test is the source of truth?"
**Result**: Single source of truth. Tests stay in sync with agent definition.

---

# Keeping templates current

All `make_*` templates are kept up to date with evolving AI platform best practices via a two-agent documentation update system plus a raw-HTTP fetch utility:

| Component | Files | What it does |
|---|---|---|
| **Doc Refresh Agent** | `update_agents/doc_refresh_agent.md/.json` | Spec for the refresh workflow (staleness → fetch → validate → write → report). Uses `fetch_doc.py` as its fetcher. |
| **Doc Analysis Agent** | `update_agents/doc_analysis_agent.md/.json` | Reads cached docs, diffs against templates using an intent-first reading protocol, and proposes minimal additive improvements — always updating both the `.json` and companion `.md` together. |
| **fetch_doc.py** | `update_agents/fetch_doc.py` | Raw-HTTP fetcher with 5 modes (default fetch, `--list-links`, `--batch`, `--from-html`, `--check`). Run via `uv run update_agents/fetch_doc.py <url>`. |

**Typical cadence**: run `doc_refresh_agent` monthly (or after a major platform release), then run `doc_analysis_agent` to surface any proposals worth adding to the templates.

Cached source documentation lives in `source_docs/` (35 files as of 2026-05-13, across Anthropic, Google ADK/Gemini, OpenAI, and xAI). See `update_agents/update_agent.md` for a quick navigation guide.

---

# Why per-repo agents — and how this compares to Hermes / OpenClaw

*This section is for evaluators picking between agent systems. Skip if you're just trying to ship.*

Tools like **Hermes** (Nous Research) and **OpenClaw** are full **agent systems** you install and run: a CLI, a daemon, a gateway process for Telegram/Discord, a centralized skills store in `~/.hermes/` or `~/.openclaw/`. Worth it if you want an unattended assistant that pings you on Telegram from a $5 VPS.

Make AI Agents takes the opposite shape: **portable agent specs that live in your repo and activate in whatever AI tool you already use.**

| | Hermes / OpenClaw | Make AI Agents |
|---|---|---|
| **Install** | uv, Python 3.11, Node.js, ffmpeg, MinGit, then the system itself; configure a provider, a gateway, and skills | **Zero.** Use whatever agentic CLI/IDE you already have. |
| **Where the agent lives** | A centralized store (`~/.hermes/skills/`) shared across projects | **In your repo,** as `agent.md` + `agent.json`. Each repo's agent is the repo's agent. |
| **Activation** | Run the system, talk to its CLI or gateway | **Open the repo in your tool.** The `AGENTS.md` is the agent's role — your tool reads it and acts on it. |
| **Lock-in** | Skills run in Hermes (or OpenClaw via migration) | **Open standard.** `AGENTS.md` is tool-agnostic; the same spec runs anywhere it's read. |
| **Maintenance** | Daemons, gateway processes, upgrades, dependency churn | **None of yours.** The host tool maintains itself. |
| **Unattended automation** (Telegram, cron) | ✅ Built-in | ❌ Not in this repo — but the sibling **[AgentJ](https://github.com/chaz-clark/agentj)** runs Make AI Agents specs on a schedule when you want that. |

**The trade is deliberate.** Make AI Agents gives up Hermes-style ambient presence (Telegram bots, gateway processes, VPS daemons) in exchange for three things its audience values more:

- **Zero install for the end user.** Non-technical faculty, students, and professionals using whatever AI tool is already on their laptop don't need to set anything up — they clone the repo and open it.
- **Per-project isolation by construction.** No global skill store to clobber across projects; each repo carries its own specialist.
- **True tool-portability.** Google's April 2026 *Gemini Enterprise Agent Platform* standardized on the exact shape Make AI Agents uses — *"subagents as Markdown + YAML in a repo, storable in a repository, enabling teams to standardize and version specialized agents."* The [Hermes Kanban v1 spec](https://github.com/NousResearch/hermes-agent/blob/main/docs/hermes-kanban-v1-spec.pdf) (§1.3) explicitly names this as a gap in their own approach — *"No portable file artifact yet."*

**Use Hermes / OpenClaw** if you're building an unattended Telegram-pingable assistant on a cloud VM.
**Use Make AI Agents** if you want repos that come with their own AI specialist, run in whatever tool you and your audience already use, and stay portable across tools. For scheduled or background execution, layer in **AgentJ** — it runs the same specs without changing anything in them.

---

# FAQ

### Q1: How is this different from OpenAPI / Swagger?
OpenAPI documents REST APIs. This documents entire **agents**, including behavior, prompts, logic, and validation.

### Q2: Do I need an AI tool to use these templates?
You can copy and edit the templates manually if you prefer. The workflow is designed to be **10× faster** when used with an AI assistant that can parse the templates and fill them based on conversation.

### Q3: What's "NGAI"?
Short for **N**on-**G**eneral **AI**. It's the framing the templates were originally built under — *"turn a general AI into a specialist for one specific job"*. You don't need to know the term to use the templates; it just shows up in some older sibling docs.

### Q4: Where does the "loader" code from the old README go?
The concept is the same, but the AI assistant typically handles loading and instantiation as part of its internal process, guided by your spec. Your `validation.commands` should point to a script that performs a real-world test.
