#### Model Capabilities

# Multi Agent

[View as Markdown](</developers/model-capabilities/text/multi-agent.md>)

[Create API key](<https://console.x.ai/team/default/api-keys>)

This feature is currently in **beta**. The API interface and behavior may change as we iterate. Please bear in mind that the API interface is not final and may include breaking changes down the line.

Realtime Multi-agent Research enables Grok to orchestrate multiple AI agents that work together in real time to perform deep, multi-step research tasks. Agents specialize in particular aspects of the research \(searching the web, analyzing data, synthesizing findings\) and collaborate to deliver comprehensive, well-sourced answers.

* * *

## Overview

Multi-agent research goes beyond single-turn tool use by coordinating a team of specialized agents that can:

  * **Search and gather** information from multiple sources simultaneously
  * **Analyze and cross-reference** findings across different domains
  * **Synthesize** comprehensive answers with citations and supporting evidence
  * **Iterate** on research in real time, refining results based on intermediate findings

* * *

## Getting Started

To use Realtime Multi-agent Research, specify `grok-4.20-multi-agent` as the model name in your API requests. This model is optimized for orchestrating multiple agents that collaborate on research tasks.
    
    
    import os
    
    from xai_sdk import Client
    from xai_sdk.chat import user
    from xai_sdk.tools import web_search, x_search
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model="grok-4.20-multi-agent",
        tools=[web_search(), x_search()],
        include=["verbose_streaming"],
    )
    
    chat.append(user("Research the latest breakthroughs in quantum computing and summarize the key findings."))
    
    is_thinking = True
    for response, chunk in chat.stream():
        if response.usage.reasoning_tokens and is_thinking:
            print(f"\rThinking... ({response.usage.reasoning_tokens} tokens)", end="", flush=True)
        if chunk.content and is_thinking:
            print("\n\nFinal Response:")
            is_thinking = False
        if chunk.content and not is_thinking:
            print(chunk.content, end="", flush=True)
    
    print("\n\nUsage:")
    print(response.usage)
    
    
    
    import os
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-4.20-multi-agent",
        input=[
            {
                "role": "user",
                "content": "Research the latest breakthroughs in quantum computing and summarize the key findings.",
            },
        ],
        tools=[
            {"type": "web_search"},
            {"type": "x_search"},
        ],
    )
    
    print(response)
    
    
    
    import os
    import requests
    
    url = "https://api.x.ai/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    payload = {
        "model": "grok-4.20-multi-agent",
        "input": [
            {
                "role": "user",
                "content": "Research the latest breakthroughs in quantum computing and summarize the key findings."
            }
        ],
        "tools": [
            {"type": "web_search"},
            {"type": "x_search"}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    
    
    
    curl https://api.x.ai/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
      "model": "grok-4.20-multi-agent",
      "input": [
        {
          "role": "user",
          "content": "Research the latest breakthroughs in quantum computing and summarize the key findings."
        }
      ],
      "tools": [
        {"type": "web_search"},
        {"type": "x_search"}
      ]
    }'
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-4.20-multi-agent"),
      prompt:
        "Research the latest breakthroughs in quantum computing and summarize the key findings.",
      tools: {
        web_search: xai.tools.webSearch(),
        x_search: xai.tools.xSearch(),
      },
    });
    
    console.log(text);
    

* * *

## How Multi-agent Works

When you send a request to the multi-agent model, multiple agents are launched to discuss and collaborate on your query. Each agent contributes its own perspective, reasoning, and findings. A designated **leader agent** is responsible for synthesizing the discussion and presenting the final answer back to you.

### Supported Models

  * `grok-4.20-multi-agent`

### Built-in Tools Support

xAI provides a set of built-in tools you can enable in the request to help with the most common use cases, e.g., `web_search`, `x_search`, `code_execution`, `collections_search`. Check out [this doc](</developers/tools/overview>) for more information.

Once you enable those tools in the request, the server will perform the agent loop to invoke those tools on the server side based on your query until the final answer is generated.

Using built-in tools will incur an additional cost. Please review the [pricing details for built-in tools](</developers/pricing#tools-pricing>).

### Output Behavior

Only the **tool calls** and the **final response** from the leader agent are sent back to the user. All sub-agent state — including their intermediate reasoning, tool calls, and outputs — is encrypted and included in the response only when `use_encrypted_content` is set to `True` in the xAI SDK. This keeps the default response clean and focused while still allowing you to preserve the full multi-agent context for multi-turn conversations.

* * *

## Configuration

You can configure how many agents collaborate on a request. The two available setups are **4 agents** and **16 agents**. More agents means deeper, more thorough research at the cost of higher token usage and latency.

SDK / API| Parameter| 4 Agents| 16 Agents  
---|---|---|---  
xAI SDK| `agent_count`| `4`| `16`  
OpenAI SDK| `reasoning.effort`| `"low"` or `"medium"`| `"high"` or `"xhigh"`  
Vercel AI SDK| `reasoningEffort`| `"low"` or `"medium"`| `"high"` or `"xhigh"`  
REST API| `reasoning.effort`| `"low"` or `"medium"`| `"high"` or `"xhigh"`  
  
**Best For:** Use 4 agents for quick research and focused queries. Use 16 agents for deep research and complex multi-faceted topics.

### 4-Agent Setup
    
    
    import os
    
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model="grok-4.20-multi-agent",
        agent_count=4,
    )
    
    chat.append(user("What are the key differences between TCP and UDP?"))
    for response, chunk in chat.stream():
        if chunk.content:
            print(chunk.content, end="", flush=True)
    
    
    
    import os
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-4.20-multi-agent",
        reasoning={"effort": "low"},
        input=[
            {
                "role": "user",
                "content": "What are the key differences between TCP and UDP?",
            },
        ],
    )
    
    print(response.output_text)
    
    
    
    import os
    import requests
    
    url = "https://api.x.ai/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    payload = {
        "model": "grok-4.20-multi-agent",
        "reasoning": {"effort": "low"},
        "input": [
            {
                "role": "user",
                "content": "What are the key differences between TCP and UDP?"
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    
    
    
    curl https://api.x.ai/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
      "model": "grok-4.20-multi-agent",
      "reasoning": {"effort": "low"},
      "input": [
        {
          "role": "user",
          "content": "What are the key differences between TCP and UDP?"
        }
      ]
    }'
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-4.20-multi-agent"),
      prompt: "What are the key differences between TCP and UDP?",
      providerOptions: {
        xai: { reasoningEffort: "low" },
      },
    });
    
    console.log(text);
    

### 16-Agent Setup
    
    
    import os
    
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model="grok-4.20-multi-agent",
        agent_count=16,
    )
    
    chat.append(user("Analyze the design trade-offs in modern programming languages: compare Rust's ownership model, Go's simplicity philosophy, and Haskell's pure functional approach. Cover memory safety, concurrency, developer productivity, and ecosystem maturity."))
    for response, chunk in chat.stream():
        if chunk.content:
            print(chunk.content, end="", flush=True)
    
    
    
    import os
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-4.20-multi-agent",
        reasoning={"effort": "high"},
        input=[
            {
                "role": "user",
                "content": "Analyze the design trade-offs in modern programming languages: compare Rust's ownership model, Go's simplicity philosophy, and Haskell's pure functional approach. Cover memory safety, concurrency, developer productivity, and ecosystem maturity.",
            },
        ],
    )
    
    print(response.output_text)
    
    
    
    import os
    import requests
    
    url = "https://api.x.ai/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    payload = {
        "model": "grok-4.20-multi-agent",
        "reasoning": {"effort": "high"},
        "input": [
            {
                "role": "user",
                "content": "Analyze the design trade-offs in modern programming languages: compare Rust's ownership model, Go's simplicity philosophy, and Haskell's pure functional approach. Cover memory safety, concurrency, developer productivity, and ecosystem maturity."
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    
    
    
    curl https://api.x.ai/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
      "model": "grok-4.20-multi-agent",
      "reasoning": {"effort": "high"},
      "input": [
        {
          "role": "user",
          "content": "Analyze the design trade-offs in modern programming languages: compare Rust'\''s ownership model, Go'\''s simplicity philosophy, and Haskell'\''s pure functional approach. Cover memory safety, concurrency, developer productivity, and ecosystem maturity."
        }
      ]
    }'
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-4.20-multi-agent"),
      prompt:
        "Analyze the design trade-offs in modern programming languages: compare Rust's ownership model, Go's simplicity philosophy, and Haskell's pure functional approach. Cover memory safety, concurrency, developer productivity, and ecosystem maturity.",
      providerOptions: {
        xai: { reasoningEffort: "high" },
      },
    });
    
    console.log(text);
    

The 16-agent setup uses significantly more tokens than the 4-agent setup. Choose the agent count based on the complexity of your research task — use 4 agents for focused queries and 16 agents when you need comprehensive, multi-perspective analysis.

* * *

## Common Patterns

### Without Built-in Tools

Multi-agent works without any built-in tools — the agents rely purely on their collective knowledge and reasoning to collaborate on a response.
    
    
    import os
    
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(
        model="grok-4.20-multi-agent",
        include=["verbose_streaming"],
    )
    
    chat.append(user("Compare the major approaches to distributed consensus in computer science: Paxos, Raft, and Byzantine fault tolerance. Analyze the trade-offs in safety guarantees, performance, and implementation complexity."))
    
    is_thinking = True
    for response, chunk in chat.stream():
        if response.usage.reasoning_tokens and is_thinking:
            print(f"\rThinking... ({response.usage.reasoning_tokens} tokens)", end="", flush=True)
        if chunk.content and is_thinking:
            print("\n\nFinal Response:")
            is_thinking = False
        if chunk.content and not is_thinking:
            print(chunk.content, end="", flush=True)
    
    print("\n\nUsage:")
    print(response.usage)
    
    
    
    import os
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-4.20-multi-agent",
        input=[
            {
                "role": "user",
                "content": "Compare the major approaches to distributed consensus in computer science: Paxos, Raft, and Byzantine fault tolerance. Analyze the trade-offs in safety guarantees, performance, and implementation complexity.",
            },
        ],
    )
    
    print(response)
    
    
    
    import os
    import requests
    
    url = "https://api.x.ai/v1/responses"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }
    payload = {
        "model": "grok-4.20-multi-agent",
        "input": [
            {
                "role": "user",
                "content": "Compare the major approaches to distributed consensus in computer science: Paxos, Raft, and Byzantine fault tolerance. Analyze the trade-offs in safety guarantees, performance, and implementation complexity."
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    
    
    
    curl https://api.x.ai/v1/responses \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
      "model": "grok-4.20-multi-agent",
      "input": [
        {
          "role": "user",
          "content": "Compare the major approaches to distributed consensus in computer science: Paxos, Raft, and Byzantine fault tolerance. Analyze the trade-offs in safety guarantees, performance, and implementation complexity."
        }
      ]
    }'
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-4.20-multi-agent"),
      prompt:
        "Compare the major approaches to distributed consensus in computer science: Paxos, Raft, and Byzantine fault tolerance. Analyze the trade-offs in safety guarantees, performance, and implementation complexity.",
    });
    
    console.log(text);
    

### Multi-turn Conversation

Multi-agent research supports multi-turn conversations using `previous_response_id`, just like any other model. You can ask follow-up questions to refine or expand on previous research results, and the agents will use the prior context to deliver more targeted answers.

For the full multi-turn conversation pattern with reusable functions and code examples, see [Chaining the conversation](</developers/model-capabilities/text/generate-text#chaining-the-conversation>).

* * *

## Pricing

All tokens consumed by both the **leader agent** and **sub-agents** are billed, including input tokens, output tokens, and reasoning tokens. Similarly, all **server-side tool calls** made by any agent — whether the leader or a sub-agent — count toward your tool usage and are billed accordingly.

Because multiple agents may run in parallel and each can independently invoke tools, a single multi-agent request may use significantly more tokens and tool calls than a standard single-agent request. You can monitor your usage via the `usage` and `server_side_tool_usage` fields in the response.

For detailed pricing information, see the [Pricing](</developers/pricing>) page and the [Tool Pricing](</developers/pricing#tools-pricing>) page.

* * *

## Prompting Guide

Getting the most out of multi-agent research starts with how you frame your request. Here are patterns that work well:

**Set the scope and depth explicitly**

Rather than asking a broad question, tell the agents exactly what dimensions to cover:

Text
    
    
    ❌  "Tell me about electric vehicles."
    ✅  "Compare the top 3 EV manufacturers by battery technology, range, charging infrastructure, and 2025 sales projections."
    

**Ask for structured output**

Multi-agent research excels when you request organized, structured responses:

Text
    
    
    ✅  "Research the pros and cons of microservices vs monolithic architecture. Present your findings as a comparison table with categories: scalability, complexity, deployment, and team size requirements."
    

**Specify sources or perspectives**

Guide the agents toward the types of evidence you value:

Text
    
    
    ✅  "Analyze the environmental impact of large language model training, citing recent academic papers and industry reports from 2024-2025."
    

**Break complex research into a conversation**

For deep topics, start broad and narrow down with follow-ups rather than packing everything into one prompt:

Text
    
    
    Turn 1: "What are the leading approaches to carbon capture technology?"
    Turn 2: "Which of those has the best cost-per-ton economics today?"
    Turn 3: "What are the main engineering challenges preventing that approach from scaling?"
    

**Provide context when relevant**

If your research builds on prior knowledge or specific constraints, include that context in the prompt:

Text
    
    
    ✅  "I'm building a fintech app targeting Southeast Asian markets. Research the regulatory requirements for digital payments in Singapore, Indonesia, and the Philippines."
    

* * *

## Limitations

  * **Only leader agent output is exposed:** Only the leader agent's output is returned, including its tool calls and response content. Sub-agent state is encrypted and only included when `use_encrypted_content` is enabled — see Output Behavior for details.
  * **No client-side or custom tools:** Client-side tools \(function calling\) and custom tools are not currently supported by the multi-agent model variant. We do support a set of built-in tools \(e.g., `web_search`, `x_search`\) and remote MCP tools. See our [built-in tool docs](</developers/tools/overview>) for more details.
  * **Chat Completions API not supported:** The multi-agent model does **not** work with the OpenAI Chat Completions API. Use the [xAI SDK](<https://github.com/xai-org/xai-sdk-python>) or the [Responses API](</developers/model-capabilities/text/generate-text>) instead.
  * **`max_tokens` is not supported:** The `max_tokens` parameter is not currently supported by the multi-agent model variant.

* * *

Last updated: July 2, 2026