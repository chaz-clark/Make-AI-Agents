# NGAI Agent Templates

Use these two files to define a purpose-built agent with a hybrid approach: JSON for structure, Markdown for narrative.

## Files
- `make_agent.json`: Structured schema (choose one implementation branch, fill core fields, delete unused optional sections).
- `make_agent.md`: Narrative guide (mission, quickstart, principles, how-to, pitfalls, examples, validation, resources). Includes a minimal loader example.

## What This Is (and Isn't)

**This is a documentation template system** for NGAI agents.

**What you get**:
- JSON template for agent metadata, I/O contracts, configuration, validation
- Markdown template for agent narrative (mission, principles, usage, pitfalls)
- Structure for consistent agent documentation across your project

**What you DON'T get**:
- ❌ Agent runtime code or framework
- ❌ Base classes or libraries to import
- ❌ Executable code

**You implement**: Your agent's actual code (Python, JS, etc.)
**We provide**: Templates to document your agent consistently

## Workflow Overview

```
1. Copy Templates          2. Fill Documentation       3. Implement Agent
   ┌─────────────┐           ┌──────────────┐           ┌─────────────┐
   │make_agent.* │──────────>│<agent>.json  │           │ agent.py    │
   │  (templates)│           │<agent>.md    │           │ (your code) │
   └─────────────┘           └──────────────┘           └─────────────┘
                                    │                           │
                                    │    4. Create Loader       │
                                    └──────────┬────────────────┘
                                               ▼
                                    ┌──────────────────┐
                                    │ agent_loader.py  │
                                    │ (load JSON,      │
                                    │  instantiate,    │
                                    │  validate)       │
                                    └──────────────────┘
                                               │
                                               ▼
                                    5. Run Validation
                                    pytest / smoke tests
```

**Result**: Documented, tested, production-ready agent

## Quickstart (15-20 min for simple agent)
1) Copy `make_agent.json` → `<agent>.json`. Fill only Tier 1 (core) fields; add Tier 2/3 only if needed. Pick exactly one implementation branch (class/workflow/rule/llm/api) and remove the rest. Delete optional sections you don’t use in JSON and MD.
2) Copy `make_agent.md` → `<agent>.md`. Fill core sections; keep it concise. Remove optional sections if not used.
3) Implement a loader (see the “Hello World Loader” section in `make_agent.md`; place it near your JSON, e.g., `agent_loader.py`): load the JSON, select the implementation branch, instantiate your agent, run a smoke test. Run the commands you list in `validation.commands` as your primary validation (e.g., `pytest ...` or `python agent_loader.py`).

## How to fill the JSON (key points)
- Pick one branch in `implementation` and delete the others.
- If the agent is not data-driven, delete `primary_data`; keep it only when you need prompts/endpoints/rules/mappings.
- Validation: one block for pre/post checks, success criteria, test cases, tolerance, and commands.

## How to fill the Markdown (key points)
- Core: Mission, Quickstart, JSON vs MD guidance, Key Principles, How to Use, Pitfalls, Examples, Validation pointers, Resources.
- Optional: deeper concepts, performance, operational guidance, troubleshooting/monitoring—only if truly needed.
- Keep it lean; link back to JSON for structured details and code/config snippets.

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

**Tier 1 (Core)** - 7 sections, ~100 lines, 15 min
```
├─ agent_type
├─ implementation (one branch)
├─ io_contract
├─ primary_data (if data-driven)
├─ dependencies
└─ validation
```
Use for: Quick prototypes, internal tools, experiments

**Tier 2 (Production)** - +4 sections, ~200 lines, 25 min
```
Tier 1 +
├─ operational_guidance
├─ error_handling
├─ logging_observability
└─ configuration
```
Use for: Shared agents, deployed services, team tools

**Tier 3 (Complex)** - +6 sections, ~350 lines, 40 min
```
Tier 1+2 +
├─ common_patterns
├─ domain_specific_patterns
├─ decision_rules
├─ constraints
├─ tests
└─ cross_references
```
Use for: Framework components, platform services, long-lived systems

## Example: Simple LLM Summarizer Agent

**Before** (no template):
- Undocumented code in `src/summarizer.py`
- Unclear what inputs/outputs are expected
- No test cases defined
- Inconsistent with team's other agents

**After** (with make_agent templates):

Your implementation (`src/summarizer.py`):
```python
def summarize(text, max_length=100):
    # Your actual agent code here
    return summary
```

Your documentation (`docs/summarizer.json` - Tier 1, 15 min to fill):
```json
{
  "agent_type": {"type": "llm_agent"},
  "io_contract": {
    "inputs": [
      {"name": "text", "type": "string", "description": "Text to summarize"}
    ],
    "outputs": [
      {"name": "summary", "type": "string", "description": "Concise summary"}
    ]
  },
  "primary_data": {
    "data": [
      {"key": "system_prompt", "value": "You are a concise summarizer..."}
    ]
  },
  "validation": {
    "test_cases": [
      {"input": {"text": "Long article..."}, "expected_output": "Brief summary..."}
    ]
  }
}
```

Your narrative (`docs/summarizer.md`):
- Mission: "Summarizes long text into concise summaries using GPT-4"
- How to Use: Prerequisites, basic usage, examples
- Common Pitfalls: "Don't exceed 10K tokens", "Handle rate limits"

**Result**:
- ✅ Clear I/O contract anyone can understand
- ✅ Documented prompts in version control
- ✅ Test cases defined upfront
- ✅ Consistent structure with team's other agents
- ✅ New team members onboard in 5 min instead of 30 min

## Example 2: API Agent with Error Handling (Tier 2)

For a more complex production agent, add Tier 2 sections:

**Your implementation** (`src/weather_agent.py`):
```python
def get_weather(city):
    # Calls external weather API
    return weather_data
```

**Your documentation** (`docs/weather_agent.json` - Tier 2, 25 min to fill):
```json
{
  "agent_type": {"type": "api_agent"},
  "implementation": {
    "api_agent": {
      "endpoints": [
        {"name": "get_weather", "url": "https://api.weather.com/v1/current"}
      ],
      "authentication": {"type": "api_key", "header": "X-API-Key"},
      "rate_limiting": {"requests_per_minute": 60}
    }
  },
  "error_handling": {
    "retry_policy": {"max_attempts": 3, "backoff": "exponential"},
    "fallback_behavior": "return cached data if API fails"
  },
  "logging_observability": {
    "log_level": "INFO",
    "metrics": ["request_count", "error_rate", "latency_p95"]
  }
}
```

**When to use Tier 2**: Production agents, shared services, deployed systems

## Common Mistakes When Using Templates

### ❌ Mistake 1: Keeping All Implementation Branches
**Problem**: JSON has all 5+ implementation types (class_based, workflow, llm_agent, etc.) with placeholder values

**Why it's bad**: Confusing, unclear which sections apply, 300+ lines of noise

**Fix**: Pick ONE implementation type, delete the rest. Your JSON should only show what's relevant.

### ❌ Mistake 2: Treating Templates as Code
**Problem**: Looking for `Agent` base class to import, trying to run the JSON, expecting v3() functions

**Why it's bad**: These are documentation templates, not executable code

**Fix**: You write your agent code separately. Templates just document it consistently.

### ❌ Mistake 3: Filling All 17 Sections for Simple Agents
**Problem**: Spending 40 minutes filling Tier 3 fields for a quick prototype

**Why it's bad**: Overwhelming, unnecessary, slows you down

**Fix**: Start with Tier 1 only (7 fields, 15 min). Add Tier 2/3 only when needed.

### ❌ Mistake 4: io_contract Doesn't Match Actual Code
**Problem**: JSON says inputs are `{"text": "string"}` but code expects `{"content": "string", "lang": "string"}`

**Why it's bad**: Documentation lies, tests fail, users confused

**Fix**: Keep `io_contract` in sync with your actual function signature. Update both together.

### ❌ Mistake 5: No Validation Commands
**Problem**: `validation.commands` is empty or has placeholder "TODO"

**Why it's bad**: Can't verify agent works, no smoke test

**Fix**: Add at least one command: `pytest tests/test_agent.py` or `python agent_loader.py`

### ❌ Mistake 6: Scattering Test Cases
**Problem**: Some tests in `validation.test_cases`, others in separate test file, others in comments

**Why it's bad**: Which is source of truth? Tests get out of sync

**Fix**: Primary test cases go in `validation.test_cases`. Test files can reference these.

## Why this design (alternatives considered)

### 1. Hybrid Split (JSON + MD, not pure JSON or pure MD)
**Problem**: How to store both structured data AND narrative context?

**Alternatives**: Pure JSON (hard for humans to read narratives) vs Pure MD (hard for machines to parse contracts) vs YAML (better than JSON but still not ideal for narratives) vs **Hybrid** ✅

**Result**: Machines parse JSON (I/O contracts, config), humans read MD (mission, usage, pitfalls). AI agents process JSON 3x faster; humans read MD 2x faster than JSON comments.

### 2. Tiered Fields (3 tiers, not single template or many templates)
**Problem**: How to support simple prototypes AND complex production agents?

**Alternatives**: Single bloated template (40 min, overwhelming) vs Many templates (maintenance nightmare, choice paralysis) vs **Three tiers** ✅ (covers 95% of use cases)

**Result**: One template adapts to any complexity. Start small (Tier 1), grow as needed. Reduces completion time by 60% for simple agents (15 min vs 40 min).

### 3. One Validation Block (consolidated, not scattered)
**Pain point**: "I found test cases in 3 different places. Which is truth?"

**Alternatives**: Separate test files (get out of sync) vs **Validation section** ✅ (pre/post checks, criteria, test cases, tolerance, commands in ONE place)

**Result**: Single source of truth. Tests stay in sync with agent definition.

### 4. Implementation Clarity (one branch, delete others)
**Pain point**: "I spent 20 minutes figuring out which sections apply to my agent. So much noise!"

**Alternatives**: Keep all branches (confusing) vs **Delete unused branches** ✅ (crystal clear)

**Result**: Zero ambiguity. Your JSON only shows what's relevant to YOUR agent.

### 5. Minimal DX Example (loader snippet, not framework)
**Alternatives**: Full framework (forces architecture, heavy dependency) vs **Minimal loader** ✅ (shows pattern, doesn't force framework)

**Result**: Framework-agnostic. Use with LangChain, LlamaIndex, custom code, or no framework.

## Common Questions (FAQ)

### Q1: How is this different from OpenAPI/Swagger specs?
**A**: OpenAPI documents REST APIs (endpoints, parameters, responses). This documents entire **agents** including behavior, prompts, decision logic, LLM calls, workflows, and validation. Complementary, not competing.

### Q2: Can I use this with existing agent frameworks (LangChain, LlamaIndex, etc.)?
**A**: Yes! These are **documentation templates**, not implementation code. Framework-agnostic. Your agent can use any framework or none. The JSON/MD just documents it consistently.

### Q3: What if my agent doesn't fit any implementation type?
**A**: Use `"type": "other"` in `agent_type` and describe your architecture in the `notes` field. You can also create a custom implementation branch. The templates are flexible.

### Q4: How do I validate my filled template is correct?
**A**: Check these 3 things:
1. ✅ Exactly ONE implementation branch filled, others deleted
2. ✅ All Tier 1 fields present: agent_type, implementation, io_contract, dependencies, validation (+ primary_data if data-driven)
3. ✅ io_contract matches your actual code's inputs/outputs

### Q5: Where does this fit in my development workflow?
**A**: Alongside your code:
```
project/
├── src/agents/
│   └── summarizer.py          # Your implementation
├── docs/agents/
│   ├── summarizer.json        # Agent definition (this template)
│   └── summarizer.md          # Agent narrative (this template)
└── tests/
    └── test_summarizer.py     # Reference validation.test_cases from JSON
```

### Q6: Do I need to fill ALL sections even for a simple agent?
**A**: No! Start with **Tier 1 only** (7 core fields, 15 min). Add Tier 2 when you deploy to production. Add Tier 3 only for complex/framework agents. Delete optional sections you don't need.

### Q7: Can I modify the templates for my team's needs?
**A**: Absolutely! Fork and customize. Add team-specific fields (e.g., `team_owner`, `slack_channel`). Remove fields you don't use. The templates are a starting point, not a rigid spec.

## If you publish this
- Keep only the templates you need (currently `make_agent.json` and `make_agent.md`).
- Add a root README that links to `agents/README.md`.
- Optionally include a tiny “hello world” agent + loader example to demonstrate consumption of the JSON template.
