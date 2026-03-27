---
platform: Anthropic
label: Claude Agent Skills
source_urls:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/enterprise.md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill.md
  - https://platform.claude.com/docs/en/build-with-claude/skills-guide.md
last_fetched: 2026-03-27
fetch_status: success
notes: Anthropic restructured agents docs from /build-with-claude/agents to /agents-and-tools/agent-skills/. Content consolidated from 6 pages.
---

# Agent Skills (Anthropic)

Agent Skills are modular capabilities that extend Claude's functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that Claude uses automatically when relevant.

> This feature is **not** eligible for Zero Data Retention (ZDR).

---

## Why use Skills

Skills are reusable, filesystem-based resources that provide Claude with domain-specific expertise: workflows, context, and best practices that transform general-purpose agents into specialists. Unlike prompts (conversation-level instructions for one-off tasks), Skills load on-demand and eliminate the need to repeatedly provide the same guidance across multiple conversations.

**Key benefits**:
- **Specialize Claude**: Tailor capabilities for domain-specific tasks
- **Reduce repetition**: Create once, use automatically
- **Compose capabilities**: Combine Skills to build complex workflows

## How Skills work

Skills leverage Claude's VM environment. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials.

This filesystem-based architecture enables **progressive disclosure**: Claude loads information in stages as needed, rather than consuming context upfront.

### Three levels of loading

**Level 1: Metadata (always loaded)**
The Skill's YAML frontmatter — loaded at startup into the system prompt. Lightweight: Claude knows each Skill exists and when to use it, but instructions aren't loaded yet.

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

**Level 2: Instructions (loaded when triggered)**
The main body of SKILL.md — procedural knowledge, workflows, best practices. Claude reads this from the filesystem only when a request matches the Skill's description.

**Level 3: Resources and code (loaded as needed)**
Additional markdown files, executable scripts, and reference materials bundled in the Skill directory. Claude accesses these only when referenced.

```
pdf-skill/
├── SKILL.md          (main instructions)
├── FORMS.md          (form-filling guide)
├── REFERENCE.md      (detailed API reference)
└── scripts/
    └── fill_form.py  (utility script)
```

| Level | When Loaded | Content |
|-------|-------------|---------|
| Metadata | Always (startup) | YAML frontmatter — discovery only |
| Instructions | On-demand | SKILL.md body — workflows, guidance |
| Resources/Code | As needed | Additional .md files, scripts, templates |

## Pre-built Agent Skills

Anthropic provides pre-built Skills for all users on claude.ai and via the API:
- **PowerPoint (pptx):** Create and edit presentations
- **Excel (xlsx):** Create and analyze spreadsheets
- **Word (docx):** Create and edit documents
- **PDF (pdf):** Generate PDF documents

---

## API Quickstart

### Required beta headers
- `code-execution-2025-08-25` — enables code execution (required for Skills)
- `skills-2025-10-02` — enables Skills API
- `files-api-2025-04-14` — for uploading/downloading files

### List available Skills
```python
import anthropic
client = anthropic.Anthropic()

skills = client.beta.skills.list(source="anthropic", betas=["skills-2025-10-02"])
for skill in skills.data:
    print(f"{skill.id}: {skill.display_title}")
```

### Use a Skill (container parameter)
Skills are specified via the `container` parameter (up to 8 Skills per request):

```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]
    },
    messages=[{"role": "user", "content": "Create a presentation about renewable energy with 5 slides"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

### Download generated files
Skills create files during code execution and return `file_id` in the response:

```python
file_id = None
for block in response.content:
    if block.type == "tool_use" and block.name == "code_execution":
        for result_block in block.content:
            if hasattr(result_block, "file_id"):
                file_id = result_block.file_id
                break

if file_id:
    file_content = client.beta.files.download(file_id=file_id, betas=["files-api-2025-04-14"])
    with open("output.pptx", "wb") as f:
        file_content.write_to_file(f.name)
```

### Multi-turn conversations
Reuse the same container across turns by specifying the container ID:

```python
response2 = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "id": response1.container.id,  # Reuse container
        "skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
    },
    messages=messages,
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

### Handle pause_turn for long operations
```python
for i in range(max_retries):
    if response.stop_reason != "pause_turn":
        break
    messages.append({"role": "assistant", "content": response.content})
    response = client.beta.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        betas=["code-execution-2025-08-25", "skills-2025-10-02"],
        container={"id": response.container.id, "skills": [...]},
        messages=messages,
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    )
```

### Skill sources
| Aspect | Anthropic Skills | Custom Skills |
|--------|-----------------|---------------|
| Type value | `anthropic` | `custom` |
| Skill IDs | Short: `pptx`, `xlsx`, `docx`, `pdf` | Generated: `skill_01AbCd...` |
| Version format | Date: `20251013` or `latest` | Epoch timestamp or `latest` |
| Availability | All users | Private to workspace |

---

## Skill Authoring Best Practices

### Concise is key

The context window is a public good. Only metadata loads at startup; SKILL.md loads on-demand; but once loaded, every token competes with conversation history.

**Default assumption:** Claude is already very smart. Only add context Claude doesn't already have.

**Good (concise, ~50 tokens):**
```markdown
## Extract PDF text
Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

**Avoid (verbose, ~150 tokens):** Explaining what PDFs are, why you chose the library, etc.

### Set appropriate degrees of freedom

Match specificity to the task's fragility:
- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode with params): Preferred pattern exists, some variation acceptable
- **Low freedom** (specific scripts): Fragile operations, consistency critical, exact sequence required

**Analogy:** Narrow bridge → exact instructions. Open field → general direction.

### SKILL.md frontmatter requirements

| Field | Rules |
|-------|-------|
| `name` | Max 64 chars, lowercase letters/numbers/hyphens only, no XML tags, no "anthropic"/"claude" |
| `description` | Non-empty, max 1024 chars, no XML tags, describe what and when to use |

### Naming conventions

Prefer **gerund form** (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

Avoid: `helper`, `utils`, `tools`, `documents` (too vague)

### Writing effective descriptions

The description field enables discovery. Include:
1. What the Skill does (capabilities)
2. When to use it (trigger conditions)
3. What it produces (outputs)

**Example:**
```yaml
description: >
  Creates, modifies, and analyzes Excel spreadsheets.
  Use when working with tabular data, financial models, or when
  the user mentions Excel, XLSX, or spreadsheets.
  Produces .xlsx files with formulas, charts, and formatted tables.
```

### Progressive disclosure in authoring

- Put the most critical, always-needed info in SKILL.md
- Move detailed reference material to linked files (REFERENCE.md, FORMS.md)
- Move executable operations to scripts
- Use `[link text](file.md)` in SKILL.md to reference additional files

### Evaluation-driven development

Test before deploying. Require 3-5 representative queries per Skill covering:
- Cases where Skill should trigger
- Cases where it should NOT trigger (isolation)
- Edge cases

---

## Enterprise Governance

### Risk tier assessment

| Risk indicator | Concern level |
|---|---|
| Code execution (scripts in Skill dir) | High |
| Instruction manipulation (ignore safety rules, hide actions) | High |
| MCP server references | High |
| Network access (URLs, fetch, curl, requests) | High |
| Hardcoded credentials | High |
| File system access outside Skill dir | Medium |
| Tool invocations (bash, file ops) | Medium |

### Review checklist (before deploying any Skill)

1. Read all Skill directory content (SKILL.md, all referenced files, bundled scripts)
2. Verify script behavior matches stated purpose (run in sandboxed environment)
3. Check for adversarial instructions (ignore safety rules, hide actions, exfiltrate data)
4. Check for external URL fetches or network calls
5. Verify no hardcoded credentials (use environment variables)
6. Identify all tools and commands the Skill instructs Claude to invoke
7. Confirm redirect destinations for external URLs
8. Verify no data exfiltration patterns

> **Warning**: Never deploy Skills from untrusted sources without a full audit. Treat Skill installation with the same rigor as installing software on production systems.

### Skill evaluation dimensions

| Dimension | What it measures |
|---|---|
| Triggering accuracy | Activates for right queries, stays inactive for unrelated ones |
| Isolation behavior | Works correctly on its own |
| Coexistence | Doesn't degrade other Skills |
| Instruction following | Claude follows Skill's instructions accurately |
| Output quality | Correct, useful results |

### Lifecycle management

- Version all Skills in source control
- Define recall procedures (remove Skill from API call, update container spec)
- Review Skills on a regular schedule when underlying models update
- Maintain an inventory of deployed Skills with owners and review dates

---

## Claude API Skill (Open Source)

The `claude-api` skill is an open-source Agent Skill bundled with Claude Code. It provides Claude with detailed, up-to-date reference material for building with the Claude API and Agent SDK across 8 languages: Python, TypeScript, Java, Go, Ruby, C#, PHP, and cURL.

**What it provides:**
- Language-specific SDK documentation
- Tool use guidance with language-specific examples
- Streaming patterns
- Batch processing (50% cost)
- Agent SDK reference (Python, TypeScript)
- Current model information (IDs, context window sizes, pricing)
- Common pitfalls

**Activation:**
- Automatic when Claude detects Anthropic SDK imports (`anthropic`, `@anthropic-ai/sdk`, `claude_agent_sdk`)
- Manual: type `/claude-api` in Claude Code

**Install from skills repository:**
```bash
npx skills add https://github.com/anthropics/skills --skill claude-api
```

Source: https://github.com/anthropics/skills/tree/main/skills/claude-api
