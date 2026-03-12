---
platform: Google
label: Gemini Structured Output
source_url: https://ai.google.dev/gemini-api/docs/structured-output
last_fetched: 2026-03-11
fetch_status: success
notes: Covers response_mime_type, response_json_schema, Pydantic/Zod integration, streaming structured output, JSON Schema subset support, structured output vs function calling distinction.
---

## Google Gemini — Structured Output

The Gemini API enables configuring models to generate responses adhering to a provided JSON Schema, ensuring "predictable, type-safe results and simplifies extracting structured data from unstructured text."

---

## Ideal Use Cases

- **Data extraction**: Pulling specific information (names, dates, entities) from text
- **Structured classification**: Categorizing text into predefined categories
- **Agentic workflows**: Generating structured inputs for tools or APIs

---

## SDK Support

| Language | Schema Format |
|----------|--------------|
| Python | Pydantic models |
| JavaScript | Zod schemas |
| REST API | JSON Schema |

---

## Basic Implementation

Set `response_mime_type` to `"application/json"` and provide a `response_json_schema` in the generation configuration.

```python
# Python with Pydantic
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: str
    prep_time_minutes: int

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Extract the recipe from this text...",
    config={
        "response_mime_type": "application/json",
        "response_schema": Recipe,
    }
)
```

---

## Streaming Support

Structured outputs support streaming. Streamed chunks will be valid partial JSON strings — concatenate to form the final complete JSON object.

---

## Tools Integration (Gemini 3 models)

Can combine structured outputs with:
- Google Search grounding
- URL Context
- Code Execution
- File Search
- Function Calling

---

## Supported JSON Schema Features

| Category | Supported |
|----------|-----------|
| Types | string, number, integer, boolean, object, array, null |
| Descriptive | title, description |
| Object constraints | properties, required, additionalProperties |
| String constraints | enum, format (date-time, date, time) |
| Number constraints | enum, minimum, maximum |
| Array constraints | items, prefixItems, minItems, maxItems |

---

## Model Support

- Gemini 3.1 Pro Preview
- Gemini 3 Flash Preview
- Gemini 2.5 Pro, Flash, Flash-Lite
- Gemini 2.0 Flash series

---

## Structured Outputs vs. Function Calling

| | Structured Outputs | Function Calling |
|--|-------------------|-----------------|
| **Purpose** | Formatting the final response to the user | Taking action during the conversation |
| **When to use** | When you want the model's answer in a specific format | When the model needs to ask you to perform a task |

---

## Best Practices

- Provide clear descriptions for schema properties
- Use specific types and enums for limited value sets
- State extraction requirements explicitly in prompts
- Validate output semantically in application code
- Implement robust error handling

---

## Limitations

- Not all JSON Schema specification features are supported
- Very large or deeply nested schemas may be rejected
- The API ignores unsupported schema properties
