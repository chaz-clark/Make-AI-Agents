# Implement Gem Agent Guide

## Agent Instructions
1. Read this guide for mission, quickstart, and principles.
2. Parse `implement_gem.json` for tool evaluation rules, knowledge file patterns, and output templates.
3. Input is always a `[gemname].txt` file. Output goes in the same folder.

---

## Mission (core)

**What it does**: Reads a completed Gem `.txt` instructions file and produces the implementation package — a `[gemname]_implement.md` file with tool recommendations and knowledge file specs, plus the scaffolded knowledge files themselves — all dropped into the same `gem_instructions/` folder.

**Why it exists**: Creating a Gem's instructions is only 90% of the job. The last 10% — deciding which Gemini tools to enable and what reference knowledge to upload — is often skipped or guessed. This agent makes that step systematic and gem-specific.

**Who uses it**: Anyone who has completed a Gem `.txt` file using the `make_gem` workflow and is ready to configure and deploy it in the Gemini Gem interface.

---

## Agent Quickstart (core)

1. **Load**: Read the target `[gemname].txt` file
2. **Analyze**: Parse the gem's role, task, context, and format to understand what the Gem does and what it needs to operate
3. **Evaluate Tools**: Score each available Gemini tool (Enable / Optional / Not Needed) using the decision rules in `implement_gem.json`
4. **Identify Knowledge Files**: Determine what reference data would improve the Gem's accuracy, specificity, or speed — and whether Claude can generate the content or the user must provide it
5. **Generate Outputs**: Write `[gemname]_implement.md` and scaffold all recommended knowledge files into the same folder as the input `.txt` file

For tool decision rules and knowledge file patterns, see `implement_gem.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- Mission and purpose
- Quickstart workflow
- Principles for tool evaluation and knowledge file design
- Common pitfalls

### The JSON File (.json) Contains:
- Tool evaluation rules (one entry per Gemini tool)
- Knowledge file pattern library (reusable patterns by gem type)
- Output file templates
- Validation checklist

---

## Key Principles (core)

### 1. Tools Must Earn Their Place
**Description**: Only recommend enabling a tool if the Gem's core task requires it. Don't enable tools speculatively.

**Why**: Each enabled tool adds UI surface area and potential distraction. A Gem that generates images when the user just wants career advice creates confusion.

**How**: For each tool, ask "Would this Gem fail or be meaningfully worse without this tool?" If yes → Enable. If it would help occasionally → Optional. If no clear use case → Not Needed.

### 2. Knowledge Files Should Be Stable Reference Data
**Description**: Knowledge files are for information the Gem will consult repeatedly that doesn't change often — lookup tables, catalogs, lists, domain guides. They are not for conversation history or dynamic data.

**Why**: The Gem can search the web for current information. Knowledge files should provide what web search can't: institution-specific data, curated lists, proprietary context, or structured reference tables that benefit from pre-loading.

**How**: Ask "Is this information stable, specific to this Gem's domain, and unavailable or unreliable via web search?" If yes, it belongs in a knowledge file.

### 3. Generate What You Can, Flag What You Can't
**Description**: Scaffold every recommended knowledge file. For files where content can be generated (company lists, process guides, example tables), generate it. For files requiring proprietary or institution-specific data, create the file with clear placeholder instructions.

**Why**: Blank file recommendations get ignored. A scaffolded file with real structure and a few example rows gets filled in.

**How**: Use the knowledge file patterns in `implement_gem.json` to generate starter content. Mark user-fill sections with `<!-- USER: add your [X] here -->` comments.

### 4. Output Naming is Deterministic
**Description**: Always name the implementation file `[gemname]_implement.md` where `[gemname]` matches the `.txt` filename exactly (without extension).

**Why**: Predictable naming keeps the `gem_instructions/` folder navigable and makes the pairing between `.txt` and `_implement.md` obvious.

**How**: Strip the `.txt` extension from the input filename and append `_implement.md`.

---

## How to Use This Agent (core)

### Prerequisites
- A completed `[gemname].txt` file in a `gem_instructions/` folder
- Access to `implement_gem.json` for tool rules and knowledge patterns

### Basic Usage

**Step 1: Invoke the agent**
```
Read implement_gem.md and implement_gem.json.
Then run the implement_gem workflow on: make_gems/gem_instructions/byui_gap_analyst.txt
```

**Step 2: Agent reads and analyzes the gem**
The agent reads the `.txt` file and identifies:
- What the Gem's core task is (from `<task>`)
- What data the Gem needs at runtime (from `<context>` and `<format>`)
- Whether the Gem needs live information (triggers Google Search / Deep Research)
- Whether the Gem produces visual, musical, or document output (triggers Image / Music / Canvas)
- Whether the Gem teaches or coaches step-by-step (triggers Guided Learning)

**Step 3: Agent writes outputs**
Produces in the same folder as the input `.txt`:
- `[gemname]_implement.md` — tool recommendations + knowledge file manifest
- One scaffolded `.md` file per recommended knowledge file

**Step 4: User reviews and fills gaps**
- Review tool recommendations and enable/disable in the Gemini Gem interface
- Fill in any `<!-- USER: -->` sections in knowledge files
- Upload knowledge files in the Gem's Knowledge section

---

## Available Gemini Tools Reference (core)

These are the tools available to evaluate for any Gem. Decision logic lives in `implement_gem.json`.

| Tool | What It Does | Enable When |
|------|-------------|-------------|
| **Google Search** | Real-time web search | Gem needs current info: job postings, news, prices, live URLs, catalog pages |
| **Deep Research** | Extended multi-source research with synthesis | Gem needs thorough research across many sources, not just a quick lookup |
| **Canvas** | Collaborative document/code editing in-session | Gem produces documents, reports, or code the user will iterate on together |
| **Image Generation** | Creates images via Imagen | Gem involves visual output: design, art, illustration, diagrams |
| **Create Music** | Generates music via Lyria | Gem involves music creation, audio, or sound design |
| **Guided Learning** | Step-by-step learning mode with checkpoints | Gem teaches, tutors, or coaches users through a learning sequence |

---

## Common Pitfalls (core)

### 1. Enabling Google Search When Deep Research Is the Right Tool
**Problem**: The Gem needs thorough multi-source research but only Google Search is enabled — results are shallow.
**Why it happens**: Google Search is the default recommendation for "needs web access." Deep Research is overlooked.
**Solution**: If the Gem's task involves synthesizing information from many sources (industry reports, academic content, multi-company comparisons), recommend Deep Research. If it just needs to fetch a URL or find a quick fact, Google Search is sufficient.

### 2. Recommending Knowledge Files for Dynamic Data
**Problem**: A knowledge file is created for data that changes frequently (e.g., current job postings, live course schedules), making it stale on day one.
**Solution**: Dynamic data belongs to Google Search, not knowledge files. Knowledge files should contain stable reference data: program lists, company rosters, domain glossaries, evaluation rubrics.

### 3. Scaffolding Knowledge Files With No Real Content
**Problem**: Knowledge files are created as empty shells — the user sees a blank file and doesn't know what to put in it.
**Solution**: Always generate at least 3-5 real example rows or entries. Use publicly available information where possible. Mark the user-fill sections clearly.

### 4. Wrong Output Location
**Problem**: The `_implement.md` and knowledge files are written to a different folder than the `.txt` file.
**Solution**: Always derive the output path from the input file path. If input is `make_gems/gem_instructions/byui_gap_analyst.txt`, all outputs go to `make_gems/gem_instructions/`.

---

## Examples (core)

### Example 1: Career/Research Gem (like byui_gap_analyst)
- **Google Search**: Enable — needs live job postings and catalog pages
- **Deep Research**: Optional — useful if student wants thorough industry analysis
- **Canvas**: Optional — gap analysis report could be iterated collaboratively
- **Image Generation**: Not Needed
- **Create Music**: Not Needed
- **Guided Learning**: Not Needed — the Gem's own 9-step workflow handles sequencing
- **Knowledge Files**: Program directory (stable catalog URLs), employer reference list

### Example 2: Design/Art Gem
- **Google Search**: Optional
- **Image Generation**: Enable — core to the Gem's output
- **Canvas**: Optional — for design briefs
- **Create Music**: Not Needed
- **Deep Research**: Not Needed
- **Guided Learning**: Not Needed

### Example 3: Tutoring/Teaching Gem
- **Google Search**: Optional
- **Guided Learning**: Enable — core to the Gem's pedagogy
- **Canvas**: Enable — collaborative problem solving
- **Image Generation**: Optional — diagrams
- **Create Music**: Not Needed
- **Deep Research**: Not Needed

---

## Validation (core)

Before finalizing outputs, check:
- [ ] Output filename matches `[gemname]_implement.md` exactly
- [ ] All 6 tools have a recommendation (Enable / Optional / Not Needed) with rationale
- [ ] Every recommended knowledge file has been scaffolded (not just listed)
- [ ] No knowledge file contains data that would be better fetched live
- [ ] All outputs are in the same folder as the input `.txt` file
- [ ] `<!-- USER: -->` markers are present wherever institution-specific data is required

---

## Resources and References

### Agent Files
- **`implement_gem.json`**: Tool decision rules, knowledge file patterns, output templates
- **`make_gem.md` / `make_gem.json`**: The upstream Gem definition workflow this agent completes
- **`make_gem_qc.md`**: Run QC before running implement_gem to ensure the `.txt` is production-ready

### Related Agents
- **make_gem** → builds the `.txt` instructions file (run first)
- **make_gem_qc** → validates the `.txt` before implementation (run second)
- **implement_gem** → this agent (run third)

### Quick Reference

| Aspect | Value |
|--------|-------|
| **Input** | `[gemname].txt` in any `gem_instructions/` folder |
| **Output** | `[gemname]_implement.md` + scaffolded knowledge files, same folder |
| **Agent Type** | workflow |
| **Complexity** | simple |
| **Key Files** | `implement_gem.json`, `implement_gem.md` |
| **Run Order** | make_gem → make_gem_qc → implement_gem |
| **Common Pitfall** | Recommending knowledge files for dynamic data that should be fetched live |
