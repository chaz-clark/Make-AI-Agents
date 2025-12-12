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

## What This Is (and Isn't)

**This is a documentation template system** for NGAI agents, designed to be used with an AI assistant.

**You implement**: Your agent's actual code (Python, JS, etc.).
**We provide**: Templates that an AI can fill on your behalf to document your agent consistently.

## Suggested folder layout
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

## Tier System (choose based on your needs)

**Tier 1 (Core)** - *For prototypes, internal tools.* (15 min)
**Tier 2 (Production)** - *For shared, deployed services.* (25 min)
**Tier 3 (Complex)** - *For frameworks, platform components.* (40 min)

(See `make_agent.json` for full details on which fields belong to which tier).

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