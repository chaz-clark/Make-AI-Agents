# <Your Gem Name> Gem Guide

## Gem Instructions
1. Read this guide to understand the Gem's mission, persona, and core pillars.
2. Use `<your_gem_name>.json` to define the specific instructions for Persona, Task, Context, and Format.
3. **Important**: This spec only defines the *System Instructions* text. File uploads (Knowledge) must be handled separately in the Gem interface.

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

## Quickstart

To use this Gem definition:

1.  **Define the Gem**: Fill out `<your_gem_name>.json` with the 4 Pillars.
2.  **Compile Instructions**: Combine the Persona, Task, Context, and Format sections into a single text block. **Use Markdown headers (e.g., `## Persona`) to separate sections.**
3.  **Save as Text**: Save the compiled block as `copy_paste_instructions.txt`.
4.  **Create the Gem**: Copy the content of `copy_paste_instructions.txt` and paste it into the "Instructions" field in the Google Gem interface.
5.  **Add Knowledge (Manual)**: If your Gem needs files, upload them in the "Knowledge" section of the interface (not defined here).
6.  **Test**: Run the test cases defined in `validation`.

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

---

## Validation

Use the `test_cases` in the JSON to verify your Gem.

*   **Input**: The prompt you give the Gem.
*   **Expected Behavior**: Does it adopt the Persona? Did it follow the Format? Did it respect the Context?

---

## Resources

*   **`Gem Instructions.md`**: Official Google guide on writing Gem instructions.
*   **`<your_gem_name>.json`**: The structured definition of this Gem.