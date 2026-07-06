# Get started with SpaceXAI

Intelligent, fast, and cost-effective models across code, text, voice, image, and video.

[Create API key](<https://console.x.ai/team/default/api-keys>)[Get Started](</developers/quickstart>)
    
    
    curl https://api.x.ai/v1/responses \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "grok-build-0.1",
        "input": "Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}"
      }'
    
    
    import os
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    
    chat = client.chat.create(model="grok-build-0.1")
    chat.append(user("Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}"))
    
    print(chat.sample().content)
    
    
    from openai import OpenAI
    
    client = OpenAI(
        api_key="<YOUR_XAI_API_KEY_HERE>",
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-build-0.1",
        input="Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}",
    )
    
    print(response.output_text)
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-build-0.1"),
      prompt: "Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}",
    });
    
    console.log(text);

## Models

### Grok Build 0.1

New

grok-build-0.1

Our coding model — trained specifically for agentic coding workflows. Use Grok Build for code.

[View model](</developers/models/grok-build-0.1>)

Context256k tokens

Input$1.00 / 1M tokens

Output$2.00 / 1M tokens

### Grok 4.3

grok-4.3

For everything except code, audio, image, and video. The most intelligent and fastest model we’ve built.

Context\- tokens

Input\- / 1M tokens

Output\- / 1M tokens

Reasoning[Configurable](</developers/model-capabilities/text/reasoning#the-reasoning_effort-parameter>)

[View model](</developers/models/grok-4.3>)

### Voice API

Real-time conversations, speech-to-text, and text-to-speech.

Agent$3.00 / hour

TTS$15.00 / 1M chars

STT \(Batch\)$0.10 / hour

STT \(Streaming\)$0.20 / hour

[Read docs](</developers/model-capabilities/audio/voice>)[Try in playground](<https://console.x.ai/playground/voice/agent>)

### Imagine API

Turn ideas into reality with image and video generation.

ModesGeneration & editing

SpeedIndustry-leading

Image · 1K / 2K[\- / image](</developers/pricing#imagine-api-pricing>)

Video · 480p / 720p / 1080p[\- / sec](</developers/pricing#imagine-video-pricing>)

[Read docs](</developers/model-capabilities/imagine>)[Try in playground](<https://console.x.ai/team/default/image>)

## Jump straight in

Try code, text, voice, image, and video models below
    
    
    curl https://api.x.ai/v1/responses \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "grok-build-0.1",
        "input": "Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}"
      }'
    
    
    import os
    from xai_sdk import Client
    from xai_sdk.chat import user
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    
    chat = client.chat.create(model="grok-build-0.1")
    chat.append(user("Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}"))
    
    print(chat.sample().content)
    
    
    from openai import OpenAI
    
    client = OpenAI(
        api_key="<YOUR_XAI_API_KEY_HERE>",
        base_url="https://api.x.ai/v1",
    )
    
    response = client.responses.create(
        model="grok-build-0.1",
        input="Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}",
    )
    
    print(response.output_text)
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateText } from "ai";
    
    const { text } = await generateText({
      model: xai.responses("grok-build-0.1"),
      prompt: "Fix this function and explain the bug: function median(a){a.sort();return a[a.length/2]}",
    });
    
    console.log(text);

### Responses API

Agentic coding with Grok Build on the API—refactor, debug, and build in your own tools.

* * *

  * Agentic coding
  * IDE & tool integrations
  * Early access
  * \- / 1M input tokens
  * \- / 1M output tokens

[Read docs](</build/overview>)

### Get started

[Create an API key](<https://console.x.ai/team/default/api-keys>)[Purchase credits](<https://console.x.ai/team/default/billing>)[Quickstart guide](</developers/quickstart>)[Models](</developers/models>)[Pricing](</developers/pricing>)

### Build

[Function calling](</developers/tools/function-calling>)[Web search](</developers/tools/web-search>)[Structured outputs](</developers/model-capabilities/text/structured-outputs>)[Batch API](</developers/advanced-api-usage/batch-api>)

### Resources

[API reference](</developers/rest-api-reference/inference>)[Community integrations](</developers/community>)[Release notes](</developers/release-notes>)