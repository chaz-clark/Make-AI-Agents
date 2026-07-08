# Gem Quality Control (QC) Guide

## Gem Instructions
1. Read this guide to understand how to validate Google Gems.
2. Parse `make_gem_qc.json` for the validation rules and scoring rubric.
3. This QC Gem acts as a strict editor, ensuring your Gem **System Instructions** are "Production Ready."

---

## Mission (core)

To ensure every Gem definition is specific, actionable, and robust by validating it against the "4 Pillars" standard.

**What it does**: specificy strict validation rules to Gem JSON/MD files.
**Why it exists**: Weak instructions (e.g., "Be helpful") lead to generic AI behavior. Strong instructions lead to specialized experts.
**Who uses it**: Gem creators who want to polish their prompts.
**Scope**: This QC process validates the **text instructions only**. It does not check file uploads (Knowledge Base).

---

## The 4 Pillars of Quality

The QC agent evaluates Gems based on these key dimensions:

### 1. Persona Depth
**Rule**: A Persona must have a clear `Role` and `Tone`.
**Bad**: "You are a coding assistant."
**Good**: "You are a Senior Site Reliability Engineer who values safety and idempotent code. Your tone is professional but cautious."

### 2. Task Actionability
**Rule**: Tasks must clearly define `Actions` and `Primary Goals`.
**Bad**: "Help the user code."
**Good**: "Debug Python scripts, refactor for PEP8 compliance, and generate unit tests."

### 3. Context & Boundaries
**Rule**: A Gem must know what *not* to do.
**Bad**: (Empty context)
**Good**: "Assume the user is a beginner. Do not use advanced C++ features. Explain every step."

### 4. Format Specificity
**Rule**: The Gem must know the *Workflow* (Interaction Chain), not just the visuals.
**Bad**: "Use bold text."
**Good**: "Step 1: Ask clarifying questions. Step 2: Present 3 options. Step 3: Refine the choice."

### 5. Interaction Depth (New)
**Rule**: The Gem should have a stance on *how* it interacts, not just *what* it knows.
**Bad**: "I answer math questions."
**Good**: "I guide students to the answer by asking Socratic questions. I encourage them to try first."

### 6. Behavioral Discipline Integration
**Rule**: Every Gem must embed the Gem-tailored behavioral discipline (per `make_gem.md` → `## Behavioral Discipline for Gems (core)`). The six applicable principles — P-001 (Read Before Claiming), P-003 (Stop on Defect), P-007 (Pull Don't Push), P-008 (Mistake-Proof Outputs), P-009 partial (Reflect on knowledge gaps), P-010 (Respect Intent) — must be reflected in the appropriate pillars. The four no-override principles (P-001, P-003, P-007, P-010) are required.

**Bad**: A Gem with rich Persona/Task/Context/Format but no language about staying within knowledge sources, no fallback for out-of-knowledge questions, and no constraint against substituting the user's question.

**Good**: A Gem whose Context pillar explicitly bounds answers to uploaded materials (P-001), names the fallback phrase for out-of-knowledge cases (P-003), and whose Format pillar specifies a consistent response shape (P-008).

The canonical rules live in `knowledge/behavioral_discipline.json` → `qc_checks` and are referenced by rule_id 9 in this skill's `make_gem_qc.json` — no duplication.

---

## How to Use This QC Skill

### Basic Validation
1.  **Load**: Give the QC agent access to your `<gem>.json` and `<gem>.md`.
2.  **Run**: Ask the QC agent to "Audit this Gem."
3.  **Review**: Look at the Score (0-100) and the Critical Issues list.

### Interpreting the Score
*   **100**: Perfect. No placeholders, strong persona, clear boundaries.
*   **80-99**: Good. Minor tweaks needed (e.g., more specific tone).
*   **60-79**: Needs Work. Likely missing a boundary or using generic verbs.
*   **< 60**: Draft. Contains placeholders like `[Your Name]` or missing entire pillars.

---

## Common Pitfalls

### The "Boring Assistant" Trap
*   **Issue**: Persona is just "Helpful Assistant."
*   **Fix**: Give it a job title. "You are an investigative journalist."

### The "Wandering Gem"
*   **Issue**: No boundaries defined.
*   **Fix**: Add negative constraints. "Do not summarize; always quote full text."

### The "Wall of Text"
*   **Issue**: Format is undefined.
*   **Fix**: Request specific structures (Lists, Tables, Code Blocks).

### The "Free-Floating Knowledge Gem" (Discipline Failure)
*   **Issue**: Gem instructions don't bound answers to uploaded knowledge files. The Gem confidently answers from training data, sounds plausible, but isn't grounded in the source material the Gem was supposed to use. Or it goes outside knowledge silently — no fallback phrase, no flag.
*   **Fix**: Embed the discipline boilerplate from `make_gem.md` → `## Behavioral Discipline for Gems (core)` into the Context pillar. Specifically: bound the Gem to uploaded materials (P-001), declare a fallback phrase for out-of-knowledge questions (P-003). Verify with a test prompt deliberately outside the knowledge base — the Gem should refuse, not improvise.

---

## Validation Rules (Technical)
See `make_gem_qc.json` for the exact logic.
- **Pillar Completeness**: 25% weight. Checks for the *presence* of Role, Task, Context, and Format concepts, even if grouped under headers like "Behaviors and Rules" or "Purpose".
- **Specificity**: 20% weight.
- **Persona/Task/Context/Format**: 10-15% weight each.
- **Behavioral Discipline Integration** (rule_id 9): 15% weight. Validates that the Gem-tailored discipline (P-001, P-003, P-007, P-008, P-009 partial, P-010) is embedded in the appropriate pillars per `make_gem.md` → `## Behavioral Discipline for Gems (core)`. Delegates to BD-QC checks in `knowledge/behavioral_discipline.json`. Critical failure if any of the four no-override principles (P-001, P-003, P-007, P-010) is missing.

## Resources
- `make_gem.json`: The schema being validated.
- `Gem Instructions.md`: The official Google guide.