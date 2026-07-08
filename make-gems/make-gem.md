# <Your Gem Name> Gem Guide


## Gem Instructions
1. Read this guide to understand the Gem's mission, persona, and core pillars.
2. Use `<your_gem_name>.json` to define the specific instructions for Persona, Task, Context, and Format.
3. **Important**: This spec only defines the *System Instructions* text. File uploads (Knowledge) must be handled separately in the Gem interface.
4. **Behavioral Discipline applies in a Gem-tailored form.** Consult `../knowledge/behavioral-discipline.md` and `../knowledge/behavioral_discipline.json`. Gems can't take actions, so only the response-shaping principles apply: P-001 (Read Before Claiming), P-003 (Stop on Defect — refuse outside knowledge), P-007 (Pull, Don't Push), P-008 (Mistake-Proof Outputs), P-009 (partial — surface knowledge gaps), P-010 (Respect User's Intent). See `## Behavioral Discipline for Gems (core)` below for how to embed in the 4 Pillars.

---

## Mission (core)

A clear and concise statement of the Gem's primary purpose.

**What it does**: [Primary function]
**Role**: [The persona it adopts]
**Target User**: [Who this is for]

**Example**: "Functions as a Writing Editor to polish essays and reports, focusing on grammar, clarity, and structure for high school students."

---

## The 4 Pillars of Gem Instructions

This Gem is defined by four key components in its JSON spec, which map directly to the text you will paste into the Gem's "Instructions" field:

### 1. Persona
*Who is the Gem?*
Defines the role, tone, and perspective.
- **Role**: The character or professional stance (e.g., "Senior Engineer").
- **Tone**: The emotional quality (e.g., "Encouraging", "Strict").
- **Pedagogical Stance**: How it relates to the user (e.g., "Encourage first attempts", "Guide, don't solve").

### 2. Task
*What must the Gem do?*
Defines specific actions and goals.
- **Primary Goals**: The main objectives.
- **Actions**: Specific verbs (e.g., "Debug", "Brainstorm", "Summarize").
- **Output Quality**: Requirements for the result (e.g., "Ensure code is documented", "Cite sources").

### 3. Context
*What does the Gem need to know?*
Defines background, assumptions, and boundaries.
- **Background**: Necessary context about the user or project.
- **Boundaries**: What the Gem should *not* do.
- **Interaction**: How it manages the conversation (e.g., "Always ask clarifying questions first").

### 4. Format
*How should the Gem respond?*
Defines the conversational workflow and visual style.
- **Interaction Chain**: The logical steps the Gem should follow (e.g., "Step 1: Ask Questions -> Step 2: Propose Solution -> Step 3: Generate Code").
- **Formatting**: use of bold, italics, code blocks, lists.

---

## Behavioral Discipline for Gems (core)

Every Gem built from this template inherits a tailored subset of the behavioral discipline defined in `../knowledge/behavioral-discipline.md` and `../knowledge/behavioral_discipline.json`. Gems can't take actions — they respond from knowledge — so the action-oriented principles (P-002 Plan, P-004 Root Cause, P-005 Small Steps, P-006 A3) don't apply. Six principles do:

| Principle | What it means for a Gem | Where to embed in the 4 Pillars |
|---|---|---|
| **P-001 Read Before Claiming** | Answer only from uploaded knowledge files. Don't infer from training data. | **Context** — boundary: "Use only the uploaded knowledge files; do not draw on outside knowledge." |
| **P-003 Stop on Defect** | If the question can't be answered from knowledge, say so. Don't fabricate. | **Context** — fallback line: "If the answer isn't in my materials, I'll say 'That isn't in my knowledge — please check with [authority].'" |
| **P-007 Pull, Don't Push** | Answer only what was asked. No speculative additions or unrelated topic shifts. | **Task** — output quality: "Answer the question asked; don't volunteer unrequested information." |
| **P-008 Mistake-Proof Outputs** | Same response shape every time (citation → answer → optional clarifier). | **Format** — interaction chain + formatting rules. |
| **P-009 Reflect (partial)** | When knowledge gaps appear, name them: "I don't see this covered, but I see X which is related." | **Format** — interaction chain step for partial-knowledge cases. |
| **P-010 Respect User's Intent** | Don't substitute their question for one you'd rather answer. | **Persona** — pedagogical stance: "Answer what was asked, not what should have been asked." |

The four no-override principles from the discipline are P-001, P-003, P-007, P-010 — all applicable to Gems and all should appear in the compiled instructions.

**Compact boilerplate for embedding in the Persona/Context pillars** (paste as a paragraph in the Context section):

> "I operate under a knowledge discipline: I read the uploaded materials before claiming anything (P-001); I stop and say so when the answer isn't in those materials (P-003); I answer only what was asked (P-007); I keep the same response shape across questions (P-008); I name knowledge gaps when I see them (P-009); I never substitute a different question for the one you asked (P-010). Full source: knowledge/behavioral-discipline.md."

For the canonical principle definitions, override rules, and reasoning, see `../knowledge/behavioral-discipline.md`. The discipline file is the source of truth — this section pointers to it, doesn't duplicate.

---

## Quickstart

To use this Gem definition:

1.  **Define the Gem**: Fill out `<your_gem_name>.json` with the 4 Pillars.
2.  **Embed the discipline**: Add the Behavioral Discipline boilerplate (see section above) into the Context pillar. Map each applicable principle to its target pillar per the table above. **Required.**
3.  **Compile Instructions**: Combine the Persona, Task, Context, and Format sections into a single text block. **Use Markdown headers (e.g., `## Persona`) to separate sections.**
4.  **Save as Text**: Save the compiled block as `copy_paste_instructions.txt`.
5.  **Create the Gem**: Copy the content of `copy_paste_instructions.txt` and paste it into the "Instructions" field in the Google Gem interface.
6.  **Add Knowledge (Manual)**: If your Gem needs files, upload them in the "Knowledge" section of the interface (not defined here).
7.  **Test**: Run the test cases defined in `validation`. Verify the Gem refuses cleanly when asked something outside its knowledge (P-003 check).

---

## Examples

Reference these examples when filling out your Gem's JSON.

### Example 1: Brainstormer
*   **Persona**: Creative muse, energetic and enthusiastic.
*   **Task**: Generate original, out-of-the-box ideas. Collaborate to refine them.
*   **Context**: Ask questions to narrow down needs (budget, location). Keep conversation context.
*   **Format**: Numbered lists, easy-to-read, short introductions.

### Example 2: Coding Partner
*   **Persona**: Supportive, patient coding expert.
*   **Task**: Write complete code, teach concepts, explain implementations.
*   **Context**: Assume basic understanding, stay strictly on coding topics.
*   **Format**: Clarifying questions -> Solution Overview -> Code + Instructions.

### Example 3: Writing Editor
*   **Persona**: Constructive critic, high-school level focus.
*   **Task**: Line-by-line edits for grammar/spelling, structural suggestions.
*   **Context**: Explain reasoning behind edits. Positive tone.
*   **Format**: Overview -> Categorized Feedback (Spelling, Grammar, Structure) -> Rewrite Offer.

---

## Common Pitfalls

1.  **Vague Persona**: "Be helpful" is too broad. "Be a cynical 1940s detective" is specific.
2.  **Missing Context**: If you don't tell the Gem *who* the user is (expert vs. novice), it may guess wrong.
3.  **Over-Formatting**: Demanding too rigid a structure can sometimes stifle the model's reasoning. Balance structure with flexibility.
4.  **Ignoring "Boundaries"**: Explicitly stating what *not* to do is often as important as what *to* do.
5.  **Unstructured Instructions for Gemini 3 Models**: Pasting instructions as flowing prose without XML tags or markdown delimiters reduces reliable parsing. For Gemini 3 models, wrap each pillar in consistent tags (e.g., `<role>...</role>`, `<task>...</task>`, `<constraints>...</constraints>`) or use consistent markdown headers. Google explicitly recommends "use consistent structure: employ XML tags or markdown delimiters throughout."
6.  **No Example Outputs in Instructions**: Relying on description alone for output format. Google's official guidance "strongly recommends always including few-shot examples in your prompts." Without examples, the model infers what "structured feedback" or "numbered list" means — and different runs produce different formats. Add 1-3 concrete input/output pairs in the Context or Format pillar to anchor the expected style.
7.  **Burying Critical Constraints**: Placing the most important constraints or role definition deep in the instructions, after secondary content. Google's Gemini 3 guidance explicitly states: "Prioritize critical instructions: place essential constraints and role definitions first." Models attend more reliably to early instruction content. A strict boundary ("Never discuss X") buried after three paragraphs of context may be inconsistently honored.
8.  **Answering From Training Data Instead of Knowledge Files (P-001 violation)**: A Gem responds confidently to a question even though the answer isn't in the uploaded knowledge files — it backfills from training. The response sounds plausible but isn't grounded in the source material the Gem was supposed to use. *Fix*: in the Context pillar, explicitly bound the Gem to the knowledge files: "Use only the uploaded materials; if the answer isn't there, say so." Test this by asking the Gem something close to its domain but absent from its knowledge — it should refuse, not improvise.
9.  **Silently Going Outside Knowledge (P-003 violation)**: Related to #8 but distinct — the Gem doesn't *fabricate*, it just doesn't *flag* the gap. The user thinks the answer came from the materials when it actually came from inference. *Fix*: in the Format pillar's interaction chain, add an explicit step: "If the question isn't covered in the materials, respond with 'That isn't in my knowledge — please check with [authority].' Don't infer from related topics." This is the Gem version of P-003 Stop on Defect.

---

## Validation

Use the `test_cases` in the JSON to verify your Gem.

*   **Input**: The prompt you give the Gem.
*   **Expected Behavior**: Does it adopt the Persona? Did it follow the Format? Did it respect the Context?

---

## Resources

*   **`Gem Instructions.md`**: Official Google guide on writing Gem instructions.
*   **`<your_gem_name>.json`**: The structured definition of this Gem.