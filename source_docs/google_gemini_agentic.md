---
platform: Google
label: Gemini API Agentic Capabilities (Function Calling)
source_url: https://ai.google.dev/gemini-api/docs/agentic-capabilities
last_fetched: 2026-03-27
fetch_status: success
fetch_error: Original agentic-capabilities URL 404s. Content fetched from https://ai.google.dev/gemini-api/docs/function-calling
notes: Covers function calling modes, parallel/compositional calling, best practices, MCP integration, Gemini 3 model IDs. Upgraded from partial to success on 2026-03-27.
---

# Function Calling with the Gemini API

## Overview

Function calling enables models to determine when to invoke specific functions and provide necessary parameters for real-world actions. The Gemini API supports three primary use cases:

- **Augment Knowledge:** Access external databases, APIs, and knowledge bases
- **Extend Capabilities:** Perform computations and overcome model limitations
- **Take Actions:** Interact with external systems like scheduling or email

## How Function Calling Works

The process involves four key steps:

1. **Define function declarations** describing the function's name, parameters, and purpose
2. **Send the API request** with function declarations alongside user prompts
3. **Execute function code** in your application (the model doesn't execute directly)
4. **Return results** to the model, including the matching function call ID

**Important:** Gemini 3 models now generate unique IDs for every function call. When returning function results, include the matching `id` in your `functionResponse`.

## Function Declarations

Define functions using a JSON subset of OpenAPI schema format, including:

- `name`: Unique, descriptive identifier (e.g., `get_weather_forecast`)
- `description`: Clear explanation of purpose and capabilities
- `parameters`: Input specification with `type`, `properties`, and `required` fields

## Advanced Capabilities

### Parallel Function Calling

Execute multiple independent functions simultaneously. The API maps results to their corresponding calls using IDs, enabling asynchronous execution.

### Compositional Function Calling

Chain multiple function calls sequentially. For example, retrieve location data, then use that location to fetch weather information.

### Function Calling Modes

Control how models use tools:

- `AUTO`: Model decides whether to call functions or respond naturally
- `ANY`: Model always predicts a function call
- `NONE`: Prohibits function calls
- `VALIDATED`: Ensures schema adherence while allowing natural language responses

### Automatic Function Calling (Python SDK)

The Python SDK converts Python functions directly into declarations and automatically handles execution and response cycles.

### Multimodal Function Responses

Gemini 3 models support including images, PDFs, and text within function responses using nested parts with `inlineData`.

### Model Context Protocol (MCP)

Built-in MCP support (Python and JavaScript SDKs) reduces boilerplate by connecting external tools without manual schema construction.

## Best Practices

- Provide extremely clear, specific function and parameter descriptions
- Use strong typing and enums for limited-value parameters
- Limit active tool sets to 10-20 for optimal performance
- Use low temperatures (e.g., 0) for deterministic function calls
- Validate critical function calls before execution
- Check `finishReason` to detect failed function calls
- Implement robust error handling with informative messages
- Prioritize security with proper authentication and authorization
- Be mindful of token limits when using lengthy descriptions

## Supported Models

Function calling is supported across Gemini 3 and 2.5 series models:

- Gemini 3.1 Pro Preview
- Gemini 3 Flash Preview
- Gemini 2.5 Pro, Flash, Flash-Lite
- Gemini 2.0 Flash

## Notes and Limitations

- Function call parts may appear anywhere in the response parts array when combined with built-in tools — iterate through all parts rather than assuming position
- Only a subset of OpenAPI schema is supported
- Large or deeply nested schemas in `ANY` mode may be rejected
- Automatic function calling is Python SDK-only
