---
platform: Google
label: Gemini API System Instructions
source_url: https://ai.google.dev/gemini-api/docs/system-instructions
last_fetched: 2026-03-27
fetch_status: partial
fetch_error: system-instructions page sparse (code examples only, no best practices). Supplemented with https://ai.google.dev/gemini-api/docs/prompting-strategies which covers system instruction design, persona, task, context, format patterns.
notes: Primary reference for make_gem.md Key Principles and make_gem.json gem_instructions fields. Covers system instruction API usage + comprehensive prompting strategy guidance.
---

# System Instructions in the Gemini API

## Basic Usage

Pass system instructions via `GenerateContentConfig`:

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."),
    contents="Hello there"
)
```

System instructions guide the behavior of Gemini models by passing a `GenerateContentConfig` object. For comprehensive guidance on writing effective system instructions, see Prompt Design Strategies below.

---

# Prompt Design Strategies for Gemini API

Source: https://ai.google.dev/gemini-api/docs/prompting-strategies

## Core Concepts

**Prompt design** involves crafting natural language requests that elicit accurate, high-quality responses from language models. The process is iterative, requiring experimentation and refinement based on observed results.

## Key Strategy Areas

### Clear and Specific Instructions

Effective customization comes through providing explicit guidance. Instructions can take multiple forms:

- **Question input**: Direct queries the model answers
- **Task input**: Specific operations to perform
- **Entity input**: Items the model processes
- **Completion input**: Partial content the model completes

### Constraints and Response Formatting

Specify limitations on response generation — length, style, or structure. For example, requesting a summary in one sentence or a bulleted list establishes boundaries that guide output. Response format can be tables, elevator pitches, keywords, or paragraphs.

### Few-Shot vs. Zero-Shot Prompting

Few-shot prompts include examples demonstrating desired patterns, while zero-shot prompts provide none. Strongly recommended: "always include few-shot examples in your prompts." Consistent formatting across examples prevents undesired output structures.

### Context Integration

Provide necessary information within the prompt rather than assuming model knowledge. Contextual information helps the model understand the constraints and details of the task.

### Breaking Down Complex Prompts

For intricate requests:
- Create single-instruction prompts rather than combining multiple directives
- Chain sequential prompts where outputs feed into subsequent inputs
- Aggregate parallel operations on different data portions

## Parameter Optimization

Adjust model behavior through:

- **Max output tokens**: Limits response length (roughly 60-80 words per 100 tokens)
- **Temperature**: Controls randomness (0 = deterministic; higher = more creative)
- **topK**: Selects from top-K probable tokens
- **topP**: Samples tokens until probability sum reaches threshold
- **stop_sequences**: Halts generation at specified character sequences

## Gemini 3 Specific Guidance

### Core Principles

- **Be direct**: State goals clearly without unnecessary persuasion
- **Use consistent structure**: Employ XML tags or markdown delimiters throughout
- **Define parameters**: Explain ambiguous terms explicitly
- **Control verbosity**: Request detailed responses when needed; models default to efficiency
- **Prioritize critical instructions**: Place essential constraints and role definitions first
- **Structure long contexts**: Supply all context before specific questions

### System Instruction Template

```
<role>
You are a helpful assistant.
</role>

<constraints>
1. Be objective.
2. Cite sources.
</constraints>

<context>
[Insert User Input Here]
</context>

<task>
[Insert the specific user request here]
</task>
```

### Enhanced Reasoning

Leverage advanced thinking capabilities through:
- Explicit planning prompts requesting sub-task parsing
- Self-critique instructions reviewing outputs against constraints

## Agentic Workflows

Complex agents benefit from explicit behavioral steering across three dimensions:

**Reasoning and Strategy**: Control logical decomposition depth, problem diagnosis thoroughness, and information analysis scope.

**Execution and Reliability**: Define adaptability to new data, self-correction persistence, and risk assessment logic.

**Interaction and Output**: Specify when assumptions are permitted versus requiring user clarification, verbosity levels, and output precision requirements.

## Things to Avoid

- Relying on models for factual information generation
- Using models cautiously for mathematics and logic problems
- Assuming models have current information without explicit grounding
