# NGAI Agent Quality Control (QC) Specs

This guide explains how to use the **Agent Quality Control (QC)** templates to validate and improve your NGAI agents. While `make_agent` helps you *create* agents, `make_agent_qc` helps you *verify* them against standards.

## First-Time User?

If you are new to the NGAI (Non-General AI) workflow, please start with the main [README.md](./README.md) to understand the core concept of "Agent Specs" and how to use an AI CLI to build them.

This guide focuses specifically on the **validation phase** of the lifecycle.

## How to Talk to Your AI About Agent QC

Think of `make_agent_qc` (`make_agent_qc.json` and `make_agent_qc.md`) as defining a **Quality Assurance** meta-skill for your AI.

You'll guide your AI by telling it to "adopt" this QC skill and then pointing it at an agent you've created.

### Common Prompting Patterns:

1.  **To validate a newly created agent:**
    > "Use the 'Agent Quality Control' skill defined by `make_agent_qc.json` and `make_agent_qc.md`. Validate the 'Simple Summarizer' agent I just created (`summarizer.json` and `summarizer.md`)."

    *Your AI should act as the QC agent, reading your files and producing a pass/fail report based on the rules in the JSON.*

2.  **To check for specific issues:**
    > "Using the QC skill, check `my_agent.md` for 'Specificity' issues. Are there any leftover placeholders?"

3.  **To run a strict audit (e.g., for production):**
    > "Run a strict validation on `production_agent.json`. I need a score of 95+ to proceed."

---

## The QC Workflow

This is a **validation-driven workflow**.

**Your Role**: Create an agent (using `make_agent`).
**AI's Role (as QC)**: Act as a harsh critic/linter, checking your work against the official standards.

```
YOU: "I've finished `writer.json`. Please validate it."
 │
 ▼
AI (QC): Loads `make_agent_qc.json` rules.
       Checks `writer.json` against 8 dimensions.
       "Found 2 issues:
        1. Missing 'io_contract' examples.
        2. Generic description in 'mission'."
 │
 ▼
YOU: "Fix issue 1 by adding this example..."
 │
 ▼
AI: Updates agent and re-validates. "Score: 98/100. PASSED."
```

## Quickstart: Validating Your Agent

### Step 1: Load the QC Skill
> **Your Prompt:**
> "Read `make_agent_qc.json` and `make_agent_qc.md` to understand your role as the Quality Control agent."

### Step 2: Run Validation
> **Your Prompt:**
> "Now validate my current agent files: `src/agents/researcher.json` and `researcher.md`. Provide a summary report with a score out of 100."

### Step 3: Interpret Results
> **AI Response:**
> "Score: 82/100. Status: NEEDS IMPROVEMENT.
> Critical Issue: The 'validation' section is empty.
> Recommendation: Add at least one specific test case."

### Step 4: Fix and Re-verify
> **Your Prompt:**
> "Here is the test case for the validation section: [details]. Add it to the JSON and re-run the QC check."

---

## What This Is

The `make_agent_qc` files define a **standardized validator** for the NGAI ecosystem.

*   **`make_agent_qc.json`**: Contains the *rules*, *scoring weights*, and *logic*. (e.g., "If 'mission' is missing, deduct 20 points.")
*   **`make_agent_qc.md`**: Contains the *philosophy* and *explanations*. (e.g., "Why we value specificity over generic templates.")

## The 15 Quality Dimensions

The QC agent evaluates your work across these key areas (defined in `make_agent_qc.json`):

**Core dimensions** (always checked):

1.  **Completeness**: Are all required sections present?
2.  **Specificity**: Are templates/placeholders (like `[Your Name]`) removed?
3.  **Cleanup**: Are unused optional sections deleted?
4.  **Consistency**: Do JSON and MD files agree (same name, version)?
5.  **Examples**: Are there concrete, runnable examples?
6.  **Validation**: Are there actual test cases?
7.  **Dependencies**: Are packages/files listed?
8.  **Documentation**: Is the narrative clear and helpful?

**Conditional dimensions** (apply when relevant):

9.  **LLM Parameter Completeness** *(llm_agent type only)*: Are `tool_choice`, `response_format`, `disable_parallel_tool_use`, `mcp_servers`, and per-tool `strict` fields present?
10. **MD/JSON Companion Sync**: Does every JSON entry in `known_failures`, `guardrails`, and `best_practices` have matching MD narrative coverage?
11. **Pitfall vs External System Lesson Separation**: Are agent-design mistakes in Pitfalls and external system quirks in External System Lessons — not mixed?
12. **Graceful Degradation Coverage** *(agents with optional tools)*: Do agents with optional dependencies or MCP servers document fallback behavior?
13. **Autonomy Guidance** *(agents with write operations)*: Do write-capable agents document when they propose vs. execute?
14. **I/O Contract Consistency**: When the input type is `file` or `folder`, does the system prompt match — single-file invocation or per-file independence language?
15. **Behavioral Discipline Integration**: Agent embeds the discipline correctly per BD-QC-001 through BD-QC-007 in `knowledge/behavioral_discipline.json`. Critical: P-001/P-003/P-007/P-010 always present; non-interactive agents declare an alert_channel.

For the canonical rule definitions, scoring weights, and severity levels, see `make_agent_qc.json` → `implementation.rule_based.rules` (rule_ids 1–18) and `validation_rules_detailed.dimensions`.

## Why this design?

### 1. Separation of Concerns
**Problem**: It's hard to be creative (making an agent) and critical (auditing it) at the same time.
**Result**: The QC agent is a separate "hat" your AI wears. It switches from "Helpful Creator" to "Strict Auditor."

### 2. Objective Scoring
**Problem**: "Is this agent good?" is subjective.
**Result**: The QC JSON defines specific weights (e.g., `Completeness = 20%`). This gives you a tangible metric (0-100) to target.

### 3. Automated "Code Review"
**Pain point**: Manually checking if you deleted every `[TODO]` is tedious.
**Result**: The QC agent automates the boring "linting" tasks so you focus on logic.

## Common Questions (FAQ)

### Q1: Can I use this on existing agents?
**A**: Yes! It's a great way to "refactor" old specs. Just ask the QC agent to review an old file and suggest modernizations.

### Q2: What if I disagree with the QC score?
**A**: The QC agent is a guide, not a gatekeeper (unless you make it one). You can instruct your AI to "Ignore rule #4 for this specific case because..."

### Q3: How do I change the rules?
**A**: Edit `make_agent_qc.json`. You can adjust weights, add new prohibited patterns, or change severity levels to match your team's standards.
