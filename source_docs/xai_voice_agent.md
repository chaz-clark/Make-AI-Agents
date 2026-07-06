#### Model Capabilities

# Voice Agent API

[View as Markdown](</developers/model-capabilities/audio/voice-agent.md>)

[Create API key](<https://console.x.ai/team/default/api-keys>)[Try Playground](<https://console.x.ai/playground/voice/agent>)

Build real-time voice applications powered by Grok. Stream audio and text bidirectionally via WebSocket for voice assistants, phone agents, and interactive voice systems.

## Quick Start

Connect to the Voice Agent API and start a conversation:
    
    
    import asyncio
    import json
    import os
    import websockets
    
    async def voice_agent():
        async with websockets.connect(
            "wss://api.x.ai/v1/realtime?model=grok-voice-latest",
            additional_headers={"Authorization": f"Bearer {os.environ['XAI_API_KEY']}"}
        ) as ws:
            # Configure session
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "voice": "eve",
                    "instructions": "You are a helpful assistant.",
                    "turn_detection": {"type": "server_vad"}
                }
            }))
            
            # Send a text message
            await ws.send(json.dumps({
                "type": "conversation.item.create",
                "item": {"type": "message", "role": "user", 
                         "content": [{"type": "input_text", "text": "Hello!"}]}
            }))
            await ws.send(json.dumps({"type": "response.create"}))
            
            # Receive audio/text responses
            async for msg in ws:
                event = json.loads(msg)
                print(f"Event: {event['type']}")
    
    asyncio.run(voice_agent())
    
    
    
    import WebSocket from "ws";
    
    const ws = new WebSocket("wss://api.x.ai/v1/realtime?model=grok-voice-latest", {
      headers: { Authorization: `Bearer ${process.env.XAI_API_KEY}` },
    });
    
    /* 
    Web browsers do not support WebSocket headers. Instead, pass an
    Ephemeral Token (prefixed with xai-client-secret.) in the WebSocket protocol.
     
    const ws = new WebSocket("wss://api.x.ai/v1/realtime",
      [`xai-client-secret.${XAI_EPHEMERAL_TOKEN}`]);
    */
    
    ws.on("open", () => {
      // Configure session
      ws.send(JSON.stringify({
        type: "session.update",
        session: {
          voice: "eve",
          instructions: "You are a helpful assistant.",
          turn_detection: { type: "server_vad" }
        }
      }));
    
      // Send a text message
      ws.send(JSON.stringify({
        type: "conversation.item.create",
        item: { type: "message", role: "user",
                content: [{ type: "input_text", text: "Hello!" }] }
      }));
      ws.send(JSON.stringify({ type: "response.create" }));
    });
    
    ws.on("message", (data) => {
      const event = JSON.parse(data);
      console.log("Event:", event.type);
    });
    
    

[Get API Key →](<https://console.x.ai/team/default/api-keys?campaign=voice-docs-agent>)[API documentation](</developers/rest-api-reference/inference/voice#realtime>)[Live Voice Demos](<https://x.ai/api/voice>)[Pricing](</developers/pricing#voice-api-pricing>)

### Get Started with Our Tester Apps

  * **[iOS Tester App](<https://github.com/xai-org/xai-cookbook/tree/main/iOS/VoiceTesterApp>)** — A Swift-based iOS app to act as a guide for setting up voice agents in your apps.
  * **[Web Agent \(WebSocket\)](<https://github.com/xai-org/xai-cookbook/tree/main/voice-examples/agent/web>)** — A web app voice agent using WebSocket.
  * **[WebRTC Agent](<https://github.com/xai-org/xai-cookbook/tree/main/voice-examples/agent/webrtc>)** — A web app voice agent using WebRTC.
  * **[Telephony Agent](<https://github.com/xai-org/xai-cookbook/tree/main/voice-examples/agent/telephony>)** — A callable phone agent using Twilio.

## Authentication

Authenticate your WebSocket connection with either method:

  * **[Ephemeral Tokens](</developers/model-capabilities/audio/ephemeral-tokens>)** \(recommended\) — Short-lived tokens for client-side apps \(browsers, mobile\). Keeps your API key off the client.
  * **API Key** — Pass your xAI API key directly in the `Authorization` header. Server-side only.

Read more in our [API documentation](</developers/rest-api-reference/inference/voice#realtime>).

## Events

Once the WebSocket is open, two-way events can begin. Client events are used to provide conversation information and send user audio to the Voice API, while server events include audio and text responses.

[API documentation →](</developers/rest-api-reference/inference/voice#realtime>)

## Model Selection

Pass `model` as a query parameter; use a versioned name to pin to a specific release.
    
    
    MODEL = "grok-voice-latest"
    url = f"wss://api.x.ai/v1/realtime?model={MODEL}"
    
    
    
    const MODEL = "grok-voice-latest";
    const url = `wss://api.x.ai/v1/realtime?model=${MODEL}`;
    

Model| Description|   
---|---|---  
`grok-voice-think-fast-1.0`| Flagship voice model|   
`grok-voice-fast-1.0`| Legacy voice model| deprecated  
  
`grok-voice-latest` always points to the newest model \(currently `grok-voice-think-fast-1.0`\).

## Session Parameters

After the session has been created, clients may send the [session.update](</developers/rest-api-reference/inference/voice#session.update>) event to configure the session.

Parameter| Type| Description  
---|---|---  
`instructions`| string| System prompt  
`reasoning.effort`| `"high"` | `"none"` | optional| Controls whether the model uses reasoning. Defaults to `"high"`. Supported only with `grok-voice-latest` and `grok-voice-think-fast-1.0`.  
`voice`| string| Voice selection: `eve`, `ara`, `rex`, `sal`, `leo`, or a [custom voice ID](</developers/model-capabilities/audio/custom-voices>) \(see Available Voices\)  
`tools`| array| Tools available to the voice agent. Supports `file_search`, `web_search`, `x_search`, `mcp`, and `function` types. See Using Tools.  
`turn_detection.type`| string | null| `"server_vad"` for automatic detection, `null` for manual text turns  
`turn_detection.threshold`| number | optional| VAD activation threshold \(0.1–0.9\). Higher values require louder audio to trigger. Default: `0.85`.  
`turn_detection.silence_duration_ms`| number | optional| How long the user must be silent \(in ms\) before the server ends the turn \(0–10000\). Higher values let users pause longer without being cut off.  
`turn_detection.prefix_padding_ms`| number | optional| Amount of audio \(in ms\) to include before the detected start of speech \(0–10000\). Helps capture the beginning of words that might otherwise be clipped by the VAD. Default: `333`.  
`turn_detection.idle_timeout_ms`| number | optional| When set, the server proactively re-engages the user if no speech is detected for this many milliseconds after the assistant finishes responding. The timer re-arms after every response, so it fires repeatedly each `idle_timeout_ms` until the user speaks. Default: `null`.  
`resumption.enabled`| boolean | optional| Opt in to Session Resumption: the server caches conversation turns keyed by `conversation_id` and replays them on reconnect so the model stays conditioned on prior context. Defaults to `false`. See Session Resumption.  
`audio.input.format.type`| string| Input format: `"audio/pcm"`, `"audio/pcmu"`, or `"audio/pcma"`  
`audio.input.format.rate`| number| Input sample rate \(PCM only\): 8000, 16000, 22050, 24000, 32000, 44100, 48000  
`audio.output.format.type`| string| Output format: `"audio/pcm"`, `"audio/pcmu"`, or `"audio/pcma"`  
`audio.output.format.rate`| number| Output sample rate \(PCM only\): 8000, 16000, 22050, 24000, 32000, 44100, 48000  
`audio.input.transcription.language_hint`| string| BCP-47 language code \(e.g. `"ja"`, `"ar"`, `"es-MX"`, `"pt-BR"`\) to bias ASR transcription toward a specific language. Can be updated mid-session. See Language Hint.  
`audio.output.speed`| number| Playback speed multiplier for assistant audio output. Range: 0.7–1.5. Default: `1.0`. Values below 1.0 slow down speech; values above 1.0 speed it up.  
`replace`| object | optional| Map of phrases to spoken substitutions applied to the model's output before TTS, e.g. `{"Acme Mobile": "Acme Mobull"}`. Fixes pronunciation by changing the spoken audio without altering the transcript. See Pronunciation Replacements.  
  
## Available Voices

Voice| Type| Tone| Description| Sample  
---|---|---|---|---  
**`eve`**|  Female| Energetic, upbeat| Default voice, engaging and enthusiastic|   
**`ara`**|  Female| Warm, friendly| Balanced and conversational|   
**`rex`**|  Male| Confident, clear| Professional and articulate, ideal for business applications|   
**`sal`**|  Neutral| Smooth, balanced| Versatile voice suitable for various contexts|   
**`leo`**|  Male| Authoritative, strong| Decisive and commanding, suitable for instructional content|   
  
### Custom Voices

Need a voice that isn't in this list? Clone any voice from a short reference clip with the [Custom Voices API](</developers/model-capabilities/audio/custom-voices>). The resulting `voice_id` works as the `voice` parameter on `session.update` exactly like a built-in voice.

### Selecting a Voice

Specify the voice in your session configuration using the `voice` parameter:
    
    
    # Configure session with a specific voice
    session_config = {
        "type": "session.update",
        "session": {
            "voice": "eve",  # eve, ara, rex, sal, leo, or custom voice ID
            "instructions": "You are a helpful assistant.",
            # Audio format settings (these are the defaults if not specified)
            "audio": {
                "input": {"format": {"type": "audio/pcm", "rate": 24000}},
                "output": {"format": {"type": "audio/pcm", "rate": 24000}}
            }
        }
    }
    
    await ws.send(json.dumps(session_config))
    
    
    // Configure session with a specific voice
    const sessionConfig = {
      type: "session.update",
      session: {
        voice: "eve", // eve, ara, rex, sal, leo, or custom voice ID
        instructions: "You are a helpful assistant.",
        // Audio format settings (these are the defaults if not specified)
        audio: {
          input: { format: { type: "audio/pcm", rate: 24000 } },
          output: { format: { type: "audio/pcm", rate: 24000 } }
        }
      }
    };
    
    ws.send(JSON.stringify(sessionConfig));

## Audio

When `turn_detection.type` is set to `server_vad`, we'll perform Voice Activity Detection \(VAD\) and automatically detect when the user is finished speaking. If you are using server VAD, you'll only need the [input\_audio\_buffer.append](</developers/rest-api-reference/inference/voice#input_audio_buffer.append>) event.

Otherwise, you'll need to send the [commit](</developers/rest-api-reference/inference/voice#input_audio_buffer.commit>) event once the user is finished speaking, and use [clear](</developers/rest-api-reference/inference/voice#input_audio_buffer.clear>) to discard all audio that has been appended but not committed yet.

### Configuring Audio Format

Specify the audio format and sample rate in the `audio` session parameters. Input and output are specified separately and do not need to match.

Format| Encoding| Container Types| Sample Rate  
---|---|---|---  
**`audio/pcm`** \(Default\)| Linear16, Little-endian| Raw, WAV, AIFF| Configurable \(see below\)  
**`audio/pcmu`**|  G.711 μ-law \(Mulaw\)| Raw| 8000 Hz  
**`audio/pcma`**|  G.711 A-law| Raw| 8000 Hz  
  
When using the `audio/pcm` format, you can configure the sample rate to one of the following supported values:

Sample Rate| Quality| Description  
---|---|---  
**8000 Hz**|  Telephone| Narrowband, suitable for voice calls  
**16000 Hz**|  Wideband| Good for speech recognition  
**22050 Hz**|  Standard| Balanced quality and bandwidth  
**24000 Hz** \(Default\)| High| Recommended for most use cases  
**32000 Hz**|  Very High| Enhanced audio clarity  
**44100 Hz**|  CD Quality| Standard for music / media  
**48000 Hz**|  Professional| Studio-grade audio  
  
You can configure the audio format and sample rate for both input and output in the session configuration:
    
    
    # Configure audio format with custom sample rate for input and output
    session_config = {
        "type": "session.update",
        "session": {
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",  # or "audio/pcmu" or "audio/pcma"
                        "rate": 16000  # Only applicable for audio/pcm
                    }
                },
                "output": {
                    "format": {
                        "type": "audio/pcm",  # or "audio/pcmu" or "audio/pcma"
                        "rate": 16000  # Only applicable for audio/pcm
                    }
                }
            },
            "instructions": "You are a helpful assistant.",
        }
    }
    
    await ws.send(json.dumps(session_config))
    
    
    // Configure audio format with custom sample rate for input and output
    const sessionConfig = {
      type: "session.update",
      session: {
        audio: {
          input: {
            format: {
              type: "audio/pcm", // or "audio/pcmu" or "audio/pcma"
              rate: 16000 // Only applicable for audio/pcm
            }
          },
          output: {
            format: {
              type: "audio/pcm", // or "audio/pcmu" or "audio/pcma"
              rate: 16000 // Only applicable for audio/pcm
            }
          }
        },
        instructions: "You are a helpful assistant.",
      }
    };
    
    ws.send(JSON.stringify(sessionConfig));

### Receiving and Playing Audio

Decode and play base64 PCM16 audio received from the API. Use the same sample rate as configured:
    
    
    import base64
    import numpy as np
    
    # Configure session with 16kHz sample rate for lower bandwidth (input and output)
    session_config = {
        "type": "session.update",
        "session": {
            "instructions": "You are a helpful assistant.",
            "voice": "eve",
            "turn_detection": {
                "type": "server_vad",
            },
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": 16000  # 16kHz for lower bandwidth usage
                    }
                },
                "output": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": 16000  # 16kHz for lower bandwidth usage
                    }
                }
            }
        }
    }
    await ws.send(json.dumps(session_config))
    
    # When processing audio, use the same sample rate
    SAMPLE_RATE = 16000
    
    # Convert audio data to PCM16 and base64
    def audio_to_base64(audio_data: np.ndarray) -> str:
        """Convert float32 audio array to base64 PCM16 string."""
        # Normalize to [-1, 1] and convert to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        # Encode to base64
        audio_bytes = audio_int16.tobytes()
        return base64.b64encode(audio_bytes).decode('utf-8')
    
    # Convert base64 PCM16 to audio data
    def base64_to_audio(base64_audio: str) -> np.ndarray:
        """Convert base64 PCM16 string to float32 audio array."""
        # Decode base64
        audio_bytes = base64.b64decode(base64_audio)
        # Convert to int16 array
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        # Normalize to [-1, 1]
        return audio_int16.astype(np.float32) / 32768.0
    
    
    // Configure session with 16kHz sample rate for lower bandwidth (input and output)
    const sessionConfig = {
      type: "session.update",
      session: {
        instructions: "You are a helpful assistant.",
        voice: "eve",
        turn_detection: { type: "server_vad" },
        audio: {
          input: {
            format: {
              type: "audio/pcm",
              rate: 16000 // 16kHz for lower bandwidth usage
            }
          },
          output: {
            format: {
              type: "audio/pcm",
              rate: 16000 // 16kHz for lower bandwidth usage
            }
          }
        }
      }
    };
    ws.send(JSON.stringify(sessionConfig));
    
    // When processing audio, use the same sample rate
    const SAMPLE_RATE = 16000;
    
    // Create AudioContext with matching sample rate
    const audioContext = new AudioContext({ sampleRate: SAMPLE_RATE });
    
    // Helper function to convert Float32Array to base64 PCM16
    function float32ToBase64PCM16(float32Array) {
      const pcm16 = new Int16Array(float32Array.length);
      for (let i = 0; i < float32Array.length; i++) {
        const s = Math.max(-1, Math.min(1, float32Array[i]));
        pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
      }
      const bytes = new Uint8Array(pcm16.buffer);
      return btoa(String.fromCharCode(...bytes));
    }
    
    // Helper function to convert base64 PCM16 to Float32Array
    function base64PCM16ToFloat32(base64String) {
      const binaryString = atob(base64String);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const pcm16 = new Int16Array(bytes.buffer);
      const float32 = new Float32Array(pcm16.length);
      for (let i = 0; i < pcm16.length; i++) {
        float32[i] = pcm16[i] / 32768.0;
      }
      return float32;
    }

## Pronunciation Replacements

Use the `replace` parameter to fix how the model pronounces specific words or phrases. Each key is matched \(case-insensitively\) in the model's output and swapped for its replacement value **before** text-to-speech — so only the spoken audio changes; the transcript the user sees keeps the original text.

This is useful for brand names, acronyms, or domain terms the model mispronounces. For example, mapping `"Acme Mobile"` to `"Acme Mobull"` makes the audio say it correctly while the transcript still reads "Acme Mobile".
    
    
    await ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "voice": "eve",
            "instructions": "You are a helpful assistant.",
            "replace": {"Acme Mobile": "Acme Mobull"}
        }
    }))
    
    
    
    ws.send(JSON.stringify({
      type: "session.update",
      session: {
        voice: "eve",
        instructions: "You are a helpful assistant.",
        replace: { "Acme Mobile": "Acme Mobull" }
      }
    }));
    

Matching behavior:

  * Matching is case-insensitive; the replacement is spoken using the casing you provide.
  * Whole-word boundaries are required, so `Acme, Mobile`, `Acme-Mobile`, and `Acme Mobiles` do **not** match.
  * When multiple keys share a prefix, the longest match wins.
  * The map can be updated mid-session with another `session.update`; the applied map is echoed back on `session.updated`.

## Supported Languages

The Voice Agent API supports 20+ languages with native-quality accents. The model automatically detects the input language and responds naturally in the same language — no configuration required.

Language| Code  
---|---  
English| `en`  
Arabic \(Egypt\)| `ar-EG`  
Arabic \(Saudi Arabia\)| `ar-SA`  
Arabic \(United Arab Emirates\)| `ar-AE`  
Bengali| `bn`  
Chinese \(Simplified\)| `zh`  
French| `fr`  
German| `de`  
Hindi| `hi`  
Indonesian| `id`  
Italian| `it`  
Japanese| `ja`  
Korean| `ko`  
Portuguese \(Brazil\)| `pt-BR`  
Portuguese \(Portugal\)| `pt-PT`  
Russian| `ru`  
Spanish \(Mexico\)| `es-MX`  
Spanish \(Spain\)| `es-ES`  
Turkish| `tr`  
Vietnamese| `vi`  
  
The model is also capable of conversing in additional languages beyond those listed above, with varying degrees of accuracy. You can specify a preferred language or accent in your system instructions for consistent multilingual experiences.

### Language Hint

Bias transcription toward a specific language by setting `audio.input.transcription.language_hint` in `session.update`. Use a BCP-47 code from the Supported Languages table. Can be changed mid-session.

For Spanish and Portuguese, you must specify a regional variant \(e.g. `"es-MX"`, `"es-ES"`, `"pt-BR"`, `"pt-PT"`\) — bare `"es"` and `"pt"` are not accepted. Unrecognized codes are silently ignored and fall back to automatic language detection.
    
    
    await ws.send(json.dumps({
        "type": "session.update",
        "session": {
            "audio": {
                "input": {
                    "transcription": {
                        "language_hint": "ja"
                    }
                }
            }
        }
    }))
    
    
    ws.send(JSON.stringify({
      type: "session.update",
      session: {
        audio: {
          input: {
            transcription: {
              language_hint: "ja"
            }
          }
        }
      }
    }));

## Using Tools with Grok Voice Agent API

The Grok Voice Agent API supports various tools that can be configured in your session to enhance the capabilities of your voice agent. Tools can be configured in the `session.update` message.

### Available Tool Types

  * **Collections Search \(`file_search`\)** \- Search through your uploaded document collections
  * **Web Search \(`web_search`\)** \- Search the web for current information
  * **X Search \(`x_search`\)** \- Search X \(Twitter\) for posts and information
  * **Remote MCP Tools \(`mcp`\)** \- Connect to external [MCP \(Model Context Protocol\)](<https://modelcontextprotocol.io/>) servers for custom tools
  * **Custom Functions** \- Define your own function tools with JSON schemas

### Collections Search with `file_search`

Use the `file_search` tool to enable your voice agent to search through document collections. You'll need to create a collection first using the [Collections API](</developers/rest-api-reference/collections>).
    
    
    COLLECTION_ID = "your-collection-id"  # Replace with your collection ID
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "file_search",
                    "vector_store_ids": [COLLECTION_ID],
                    "max_num_results": 10,
                },
            ],
        },
    }
    
    
    const COLLECTION_ID = "your-collection-id"; // Replace with your collection ID
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "file_search",
                    vector_store_ids: [COLLECTION_ID],
                    max_num_results: 10,
                },
            ],
        },
    };

### Web Search and X Search

Configure web search and X search tools to give your voice agent access to current information from the web and X \(Twitter\).
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "web_search",
                },
                {
                    "type": "x_search",
                    "allowed_x_handles": ["elonmusk", "xai"],
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "web_search",
                },
                {
                    type: "x_search",
                    allowed_x_handles: ["elonmusk", "xai"],
                },
            ],
        },
    };

### Remote MCP Tools

Use the `mcp` tool type to connect your voice agent to external [MCP \(Model Context Protocol\)](<https://modelcontextprotocol.io/>) servers. This lets you extend your voice agent with third-party or custom tools without implementing them as client-side functions — xAI manages the MCP server connection and tool execution on your behalf.
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "mcp",
                    "server_url": "https://mcp.example.com/mcp",
                    "server_label": "my-tools",
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "mcp",
                    server_url: "https://mcp.example.com/mcp",
                    server_label: "my-tools",
                },
            ],
        },
    };

#### MCP Tool Parameters

Parameter| Required| Description  
---|---|---  
`server_url`| Yes| The URL of the MCP server. Only Streaming HTTP and SSE transports are supported.  
`server_label`| Yes| A label to identify the server \(used for tool call prefixing\).  
`server_description`| No| A description of what the server provides.  
`allowed_tools`| No| List of specific tool names to allow. If omitted, all tools from the server are available.  
`authorization`| No| A token set in the `Authorization` header on requests to the MCP server.  
`headers`| No| Additional headers to include in requests to the MCP server.  
  
#### Advanced MCP Configuration

You can restrict which tools are available, provide authentication, and add custom headers:
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "mcp",
                    "server_url": "https://mcp.example.com/mcp",
                    "server_label": "my-tools",
                    "server_description": "Custom business tools for order management",
                    "allowed_tools": ["lookup_order", "check_inventory"],
                    "authorization": "Bearer your-token-here",
                    "headers": {
                        "X-Custom-Header": "value"
                    },
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "mcp",
                    server_url: "https://mcp.example.com/mcp",
                    server_label: "my-tools",
                    server_description: "Custom business tools for order management",
                    allowed_tools: ["lookup_order", "check_inventory"],
                    authorization: "Bearer your-token-here",
                    headers: {
                        "X-Custom-Header": "value",
                    },
                },
            ],
        },
    };

#### Multiple MCP Servers

You can connect to multiple MCP servers simultaneously, each providing different capabilities:
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "mcp",
                    "server_url": "https://mcp.deepwiki.com/mcp",
                    "server_label": "deepwiki",
                },
                {
                    "type": "mcp",
                    "server_url": "https://your-tools.example.com/mcp",
                    "server_label": "custom-tools",
                    "allowed_tools": ["search_database", "format_data"],
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "mcp",
                    server_url: "https://mcp.deepwiki.com/mcp",
                    server_label: "deepwiki",
                },
                {
                    type: "mcp",
                    server_url: "https://your-tools.example.com/mcp",
                    server_label: "custom-tools",
                    allowed_tools: ["search_database", "format_data"],
                },
            ],
        },
    };

MCP tools are server-side tools — xAI handles the connection and execution automatically. Unlike custom function tools, you don't need to handle tool call responses in your client code. For more details on MCP tool configuration, see the [Remote MCP Tools](</developers/tools/remote-mcp>) guide.

### Custom Function Tools

You can define custom function tools with JSON schemas to extend your voice agent's capabilities.
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "function",
                    "name": "generate_random_number",
                    "description": "Generate a random number between min and max values",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min": {
                                "type": "number",
                                "description": "Minimum value (inclusive)",
                            },
                            "max": {
                                "type": "number",
                                "description": "Maximum value (inclusive)",
                            },
                        },
                        "required": ["min", "max"],
                    },
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "function",
                    name: "generate_random_number",
                    description: "Generate a random number between min and max values",
                    parameters: {
                        type: "object",
                        properties: {
                            min: {
                                type: "number",
                                description: "Minimum value (inclusive)",
                            },
                            max: {
                                type: "number",
                                description: "Maximum value (inclusive)",
                            },
                        },
                        required: ["min", "max"],
                    },
                },
            ],
        },
    };

### Combining Multiple Tools

You can combine multiple tool types in a single session configuration, including server-side tools \(web search, X search, collections, MCP\) and client-side function tools:
    
    
    session_config = {
        "type": "session.update",
        "session": {
            ...
            "tools": [
                {
                    "type": "file_search",
                    "vector_store_ids": ["your-collection-id"],
                    "max_num_results": 10,
                },
                {
                    "type": "web_search",
                },
                {
                    "type": "x_search",
                },
                {
                    "type": "mcp",
                    "server_url": "https://mcp.example.com/mcp",
                    "server_label": "my-tools",
                },
                {
                    "type": "function",
                    "name": "generate_random_number",
                    "description": "Generate a random number",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "min": {"type": "number"},
                            "max": {"type": "number"},
                        },
                        "required": ["min", "max"],
                    },
                },
            ],
        },
    }
    
    
    const sessionConfig = {
        type: "session.update",
        session: {
            ...
            tools: [
                {
                    type: "file_search",
                    vector_store_ids: ["your-collection-id"],
                    max_num_results: 10,
                },
                {
                    type: "web_search",
                },
                {
                    type: "x_search",
                },
                {
                    type: "mcp",
                    server_url: "https://mcp.example.com/mcp",
                    server_label: "my-tools",
                },
                {
                    type: "function",
                    name: "generate_random_number",
                    description: "Generate a random number",
                    parameters: {
                        type: "object",
                        properties: {
                            min: { type: "number" },
                            max: { type: "number" },
                        },
                        required: ["min", "max"],
                    },
                },
            ],
        },
    };

Server-side tools \(web search, X search, collections, and MCP\) are executed automatically by xAI — you don't need to handle their responses. Only custom function tools require client-side handling. For more details, see [Collections](</developers/rest-api-reference/collections>), [Web Search](</developers/tools/web-search>), [X Search](</developers/tools/x-search>), and [Remote MCP Tools](</developers/tools/remote-mcp>).

### Handling Function Call Responses

When you define custom function tools, the voice agent will call these functions during conversation. You need to handle these function calls, execute them, and return the results to continue the conversation.

### Function Call Flow

  1. **Agent decides to call a function** → sends `response.function_call_arguments.done` event
  2. **Your code executes the function** → processes the arguments and generates a result
  3. **Send result back to agent** → sends `conversation.item.create` with the function output
  4. **Request continuation** → sends `response.create` to let the agent continue

### Complete Example
    
    
    import json
    import websockets
    
    # Define your function implementations
    def get_weather(location: str, units: str = "celsius"):
        """Get current weather for a location"""
        # In production, call a real weather API
        return {
            "location": location,
            "temperature": 22,
            "units": units,
            "condition": "Sunny",
            "humidity": 45
        }
    
    def book_appointment(date: str, time: str, service: str):
        """Book an appointment"""
        # In production, interact with your booking system
        import random
        confirmation = f"CONF{random.randint(1000, 9999)}"
        return {
            "status": "confirmed",
            "confirmation_code": confirmation,
            "date": date,
            "time": time,
            "service": service
        }
    
    # Map function names to implementations
    FUNCTION_HANDLERS = {
        "get_weather": get_weather,
        "book_appointment": book_appointment
    }
    
    async def handle_function_call(ws, event):
        """Handle function call from the voice agent"""
        function_name = event["name"]
        call_id = event["call_id"]
        arguments = json.loads(event["arguments"])
    
        print(f"Function called: {function_name} with args: {arguments}")
    
        # Execute the function
        if function_name in FUNCTION_HANDLERS:
            result = FUNCTION_HANDLERS[function_name](**arguments)
    
            # Send result back to agent
            await ws.send(json.dumps({
                "type": "conversation.item.create",
                "item": {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": json.dumps(result)
                }
            }))
    
            # Request agent to continue with the result
            await ws.send(json.dumps({
                "type": "response.create"
            }))
        else:
            print(f"Unknown function: {function_name}")
    
    # In your WebSocket message handler
    async def on_message(ws, message):
        event = json.loads(message)
    
        # Listen for function calls
        if event["type"] == "response.function_call_arguments.done":
            await handle_function_call(ws, event)
        elif event["type"] == "response.output_audio.delta":
            # Handle audio response
            pass
    
    
    // Define your function implementations
    const functionHandlers = {
      get_weather: async (args) => {
        // In production, call a real weather API
        return {
          location: args.location,
          temperature: 22,
          units: args.units || "celsius",
          condition: "Sunny",
          humidity: 45
        };
      },
    
      book_appointment: async (args) => {
        // In production, interact with your booking system
        const confirmation = `CONF${Math.floor(Math.random() * 9000) + 1000}`;
        return {
          status: "confirmed",
          confirmation_code: confirmation,
          date: args.date,
          time: args.time,
          service: args.service
        };
      }
    };
    
    // Handle function calls from the voice agent
    async function handleFunctionCall(ws, event) {
      const functionName = event.name;
      const callId = event.call_id;
      const args = JSON.parse(event.arguments);
    
      console.log(`Function called: ${functionName} with args:`, args);
    
      // Execute the function
      const handler = functionHandlers[functionName];
      if (handler) {
        const result = await handler(args);
    
        // Send result back to agent
        ws.send(JSON.stringify({
          type: "conversation.item.create",
          item: {
            type: "function_call_output",
            call_id: callId,
            output: JSON.stringify(result)
          }
        }));
    
        // Request agent to continue with the result
        ws.send(JSON.stringify({
          type: "response.create"
        }));
      } else {
        console.error(`Unknown function: ${functionName}`);
      }
    }
    
    // In your WebSocket message handler
    ws.on("message", (message) => {
      const event = JSON.parse(message);
    
      // Listen for function calls
      if (event.type === "response.function_call_arguments.done") {
        handleFunctionCall(ws, event);
      } else if (event.type === "response.output_audio.delta") {
        // Handle audio response
      }
    });

### Function Call Events

Event| Direction| Description  
---|---|---  
`response.function_call_arguments.done`| Server → Client| Function call triggered with complete arguments  
`conversation.item.create` \(function\_call\_output\)| Client → Server| Send function execution result back  
`response.create`| Client → Server| Request agent to continue processing  
  
### Parallel Tool Calling

When the model determines that multiple function calls are needed to fulfill a request, it will emit multiple `response.function_call_arguments.done` events before any audio response. In this case, you must resolve **all** function calls and send their results back before emitting `response.create`.

**Expected behavior:**

  1. Receive multiple `response.function_call_arguments.done` events \(one per function call\)
  2. Execute all functions \(can be done in parallel for performance\)
  3. Send a `conversation.item.create` with `function_call_output` for **each** function call
  4. Only after all function outputs have been sent, emit a single `response.create` to continue

**Important:** Do not send `response.create` until all function call outputs have been submitted. Sending `response.create` prematurely will cause the model to respond without the complete context from all tool results.

## Force Message

Use `force_message` to make the agent speak a **hard-coded, TTS-synthesized line** without involving the model. This is useful for scripted greetings, compliance disclosures \(e.g. "This call is being recorded"\), IVR prompts, or any utterance that must be delivered verbatim.

Send a `conversation.item.create` event with `item.type` set to `"force_message"`:
    
    
    await ws.send(json.dumps({
        "type": "conversation.item.create",
        "item": {
            "type": "force_message",
            "role": "assistant",
            "interruptible": False,
            "content": [{"type": "output_text", "text": "This call is being recorded."}]
        }
    }))
    # Do NOT send response.create — the force_message IS the turn.
    
    
    
    ws.send(JSON.stringify({
      type: "conversation.item.create",
      item: {
        type: "force_message",
        role: "assistant",
        interruptible: false,
        content: [{ type: "output_text", text: "This call is being recorded." }],
      },
    }));
    // Do NOT send response.create — the force_message IS the turn.
    

Field| Required| Default| Description  
---|---|---|---  
`item.type`| Yes| —| Must be `"force_message"`  
`item.content[].text`| Yes| —| Verbatim text to synthesize via TTS  
`item.interruptible`| No| `true`| When `false`, caller audio is dropped until playback completes  
  
The server injects a full response lifecycle \(`response.created` → `response.output_audio.delta` → `response.done`\) so the force message appears to clients like a normal model turn.

`force_message` is an xAI extension. It is not part of the OpenAI Realtime API.

## Per-Response Instructions

Override the session-level system prompt for a single response by setting `instructions` on `response.create`:
    
    
    await ws.send(json.dumps({
        "type": "response.create",
        "response": {
            "instructions": "Respond in Spanish for this turn only."
        }
    }))
    
    
    
    ws.send(JSON.stringify({
      type: "response.create",
      response: {
        instructions: "Respond in Spanish for this turn only.",
      },
    }));
    

The override applies only to this response — subsequent responses revert to the session `instructions`. This is useful for injecting dynamic context \(e.g. CRM data, caller info\) or temporarily changing behavior without updating the session.

## Session Resumption

By default a `/v1/realtime` connection loses its conversation history when the WebSocket closes. **Session resumption** caches each turn and replays the prior context on reconnect, so the model stays conditioned on what was said earlier.

To continue a session across connections, capture the server's `conversation.created.conversation.id` and pass it back as `?conversation_id=<id>` on reconnect \(with the same opt-in\).

  1. **Connect and opt in** by sending `resumption.enabled: true` on `session.update`. Read the assigned id from `conversation.created` and store it.
  2. **Reconnect with that id.** Reopen the WebSocket with `?conversation_id=<id>` and opt in again. The cached turns replay before your first new turn, echoed back as `conversation.item.created` events.

    
    
    import json, websockets
    
    # resume_id is None on a fresh conversation; pass the saved id to resume.
    async def connect(resume_id=None):
        url = f"wss://api.x.ai/v1/realtime?model={MODEL}"
        if resume_id:
            url += f"&conversation_id={resume_id}"
    
        async with websockets.connect(url, additional_headers=headers) as ws:
            # Opt in to resumption (required to cache and to replay).
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {"resumption": {"enabled": True}},
            }))
    
            async for raw in ws:
                event = json.loads(raw)
                if event["type"] == "conversation.created":
                    # Server-assigned id. Save it and pass it as
                    # ?conversation_id= on your next connect to resume.
                    saved_id = event["conversation"]["id"]
                # ... handle the rest of the session
    
    
    
    // resumeId is null on a fresh conversation; pass the saved id to resume.
    function connect(resumeId = null) {
      let url = `wss://api.x.ai/v1/realtime?model=${MODEL}`;
      if (resumeId) url += `&conversation_id=${resumeId}`;
      const ws = new WebSocket(url);
    
      ws.addEventListener("open", () => {
        // Opt in to resumption (required to cache and to replay).
        ws.send(JSON.stringify({
          type: "session.update",
          session: { resumption: { enabled: true } },
        }));
      });
    
      ws.addEventListener("message", (msg) => {
        const event = JSON.parse(msg.data);
        if (event.type === "conversation.created") {
          // Server-assigned id. Save it and pass it as
          // ?conversation_id= on your next connect to resume.
          savedId = event.conversation.id;
        }
        // ... handle the rest of the session
      });
    }
    

Persisted and replayed: user and assistant transcripts, assistant tool calls, and your `function_call_output` results.

  * **Opt-in both ways.** No history replays unless the resuming session also sends `resumption.enabled: true`.
  * **Expiry.** History is dropped after 30 minutes of inactivity.

## Best Practices

This section outlines key recommendations for building low-latency, reliable, and natural-feeling voice experiences using the xAI Voice Agent API.

### Minimize perceived latency with parallel initialization

Start the WebSocket connection and microphone input streaming in parallel.

  * Initiate the WebSocket connection \(including authentication via ephemeral token or API key\) **as early as possible** — ideally when the voice interface loads or the user opens the mic-enabled screen.
  * Simultaneously begin capturing microphone audio \(using `getUserMedia` in browsers or equivalent APIs on mobile/native platforms\).
  * Do **not** wait for the WebSocket `open` event before starting to collect microphone samples.

**Audio Buffering Example**

JavaScript
    
    
    // 1. Immediately request mic access and start capturing
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    
    const audioContext = new AudioContext({ sampleRate: 24000 });
    
    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096, 1, 1); // or AudioWorklet for better perf
    
    source.connect(processor);
    processor.connect(audioContext.destination); // optional
    
    // Buffer incoming PCM data immediately
    let earlyAudioBuffer = []; // Float32Array[] or Int16Array[]
    
    processor.onaudioprocess = (e) => {
      const input = e.inputBuffer.getChannelData(0);
      earlyAudioBuffer.push(new Float32Array(input)); // or convert to PCM16
    };
    
    // 2. In parallel – connect WebSocket (may take time)
    const ws = new WebSocket("wss://api.x.ai/v1/realtime?model=grok-voice-latest", [
      `xai-client-secret.${token}`,
    ]);
    
    ws.onopen = () => {
      // Send session.update configuration
      ws.send(JSON.stringify({ type: "session.update", session: { ... } }));
    
      // Flush any buffered audio now that we're connected
      if (earlyAudioBuffer.length > 0) {
        flushBufferedAudioToWS(earlyAudioBuffer);
        earlyAudioBuffer = [];
      }
    };
    

#### Tips for Production

  * Convert to 24 kHz PCM16 little-endian before buffering or flushing.
  * Flush in reasonably sized messages \(100ms samples each\) for smooth transmission.
  * On reconnection, resume buffering immediately.

### Avoid Audio Overlap During Tool Calls

When the model invokes a tool during a voice response, the server delivers all audio deltas first, then the function call events alongside `response.done`. If your client immediately sends `conversation.item.create` \(with the function result\) followed by `response.create`, the server starts generating the next response right away — even if the client is still playing audio from the previous turn. This causes overlapping audio.

**Recommended sequence:**

  1. Receive `response.function_call_arguments.done` → execute your tool
  2. Send `conversation.item.create` with the `function_call_output`
  3. **Wait until audio playback of the current turn is complete** \(or nearly complete\)
  4. Then send `response.create`

While waiting for playback to finish, show a visual "thinking" indicator \(e.g., animated dots\) so the user knows the agent is processing. This creates a natural pause between the model's spoken response and the follow-up after the tool result.

JavaScript
    
    
    ws.on("message", async (message) => {
      const event = JSON.parse(message);
    
      if (event.type === "response.function_call_arguments.done") {
        // 1. Execute the tool
        const result = await executeFunction(event.name, JSON.parse(event.arguments));
    
        // 2. Send the function result immediately
        ws.send(JSON.stringify({
          type: "conversation.item.create",
          item: {
            type: "function_call_output",
            call_id: event.call_id,
            output: JSON.stringify(result),
          },
        }));
    
        // 3. Show a "thinking" indicator in the UI
        showThinkingIndicator();
    
        // 4. Wait for current audio playback to finish
        await waitForPlaybackComplete();
    
        // 5. Now request the next response
        ws.send(JSON.stringify({ type: "response.create" }));
        hideThinkingIndicator();
      }
    });
    
    

### Additional High-Impact Recommendations

  * **Prefer[ephemeral tokens](</developers/model-capabilities/audio/ephemeral-tokens>)** for client-side security.
  * **Enable`server_vad`** for automatic, natural barge-in.
  * **Match input/output format** \(24 kHz PCM\) to avoid resampling.
  * **Stream output audio deltas** \(`response.output_audio.delta`\) to the speaker instantly — do not wait for the full response.
  * **Implement graceful reconnection** while continuing to buffer new audio.
  * **Monitor WebSocket health** and use exponential backoff if needed.

## Built for Enterprise Voice

Telephony Integration

Connect via SIP, WebSocket, or LiveKit. Native G.711 μ-law/A-law codec support — no transcoding overhead.

Tool Calling

CRMs, calendars, databases, and any REST or GraphQL endpoint via function calling during live conversations.

20+ Languages

Natural pronunciation, accent handling, and seamless code-switching between languages in the same conversation.

Domain Expertise

Precise transcription of medical, legal, financial, and technical terminology — names, codes, and addresses.

## SIP phone calls

Route PSTN, contact-center, or PBX calls into a Voice Agent API session. See [SIP Phone Calls](</developers/model-capabilities/audio/voice-agent/sip>) for API integration with `CreatePhoneNumberV2`, call control, DTMF, and telephony provider examples.

## Migrating from OpenAI Realtime

If you have an existing application built on the [OpenAI Realtime API](<https://developers.openai.com/api/docs/guides/realtime-conversations>), switching to the Grok Voice Agent API requires only a few changes: update the base URL, swap your API key, and choose a Grok voice model.

### Step 1 — Update the Base URL and API Key

#### Using the OpenAI SDK

If you are using the official OpenAI SDK, point the client at the xAI endpoint and supply your xAI API key:
    
    
    import asyncio
    from openai import AsyncOpenAI
    
    # Before (OpenAI)
    # client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    # After (xAI)
    client = AsyncOpenAI(
        api_key=os.environ["XAI_API_KEY"],
        base_url="https://api.x.ai/v1",
    )
    
    async def main():
        async with client.realtime.connect(
            model="grok-voice-latest"
        ) as conn:
            await conn.session.update(session={
                "voice": "eve",
                "instructions": "You are a helpful assistant.",
                "turn_detection": {"type": "server_vad"},
            })
            # ... rest of your application code
    
    asyncio.run(main())
    
    
    
    import OpenAI from "openai";
    import { OpenAIRealtimeWS } from "openai/realtime/ws";
    
    // Before (OpenAI)
    // const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    
    // After (xAI)
    const client = new OpenAI({
      apiKey: process.env.XAI_API_KEY,
      baseURL: "https://api.x.ai/v1",
    });
    
    // Pass the configured client so the connection uses the xAI base URL and key
    const rt = new OpenAIRealtimeWS({ model: "grok-voice-latest" }, client);
    
    rt.on("session.created", () => {
      rt.send({
        type: "session.update",
        session: {
          voice: "eve",
          instructions: "You are a helpful assistant.",
          turn_detection: { type: "server_vad" },
        },
      });
    });
    
    rt.on("error", (err) => {
      console.error("Realtime error:", err);
    });
    
    // ... rest of your application code
    

#### Using a Raw WebSocket

If you connect directly via WebSocket, change the URL and `Authorization` header:
    
    
    import os
    import websockets
    
    # Before (OpenAI)
    # url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    # headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
    
    # After (xAI)
    url = "wss://api.x.ai/v1/realtime?model=grok-voice-latest"
    headers = {"Authorization": f"Bearer {os.environ['XAI_API_KEY']}"}
    
    async with websockets.connect(url, additional_headers=headers) as ws:
        # Your existing event handling code works as-is
        pass
    
    
    
    import WebSocket from "ws";
    
    // Before (OpenAI)
    // const url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview";
    // const headers = { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` };
    
    // After (xAI)
    const url = "wss://api.x.ai/v1/realtime?model=grok-voice-latest";
    const headers = { Authorization: `Bearer ${process.env.XAI_API_KEY}` };
    
    const ws = new WebSocket(url, { headers });
    
    ws.on("open", () => {
      // Your existing event handling code works as-is
    });
    

### Step 2 — Choose a Model

Pass the model name when you establish the connection:
    
    
    # Pass the model in connect()
    async with client.realtime.connect(model="grok-voice-latest") as conn:
        ...
    
    
    
    // Pass the model in the OpenAIRealtimeWS constructor
    const rt = new OpenAIRealtimeWS({ model: "grok-voice-latest" }, client);
    

### Step 3 — Model-Specific Best Practices

#### `grok-voice-think-fast-1.0` \(Recommended\)

This is the flagship voice model. Use `grok-voice-latest` for new integrations so your app tracks the current recommended model. When migrating:

  * **Simplify your system prompt.** The model is significantly more capable, so your prompt should be much shorter. Ask Grok to generalize your existing system prompt rather than porting it verbatim.
  * **Remove workaround prompting.** Prompt hacks and edge-case fixes needed for GPT models are unnecessary. Strip out instructions added solely to patch bugs or limitations of the previous model.
  * **Reasoning is enabled by default.** The default `reasoning.effort` is `"high"` for complex multi-step instructions, nuanced tone, and ambiguous queries. Set it to `"none"` to disable reasoning.

#### Deprecated model

This model remains available for existing integrations, but new applications should use `grok-voice-latest`.

  * `grok-voice-fast-1.0`: Legacy voice model with similar prompting characteristics to GPT realtime models.

The deprecated model follows the same client and server event flow as `grok-voice-latest`, so existing integrations can pin to it while migrating.

`grok-voice-latest` always points to the newest model \(currently `grok-voice-think-fast-1.0`\). Pin to a versioned model name in production for stability.

## OpenAI Realtime API Compatibility

The Grok Voice Agent API is compatible with the [OpenAI Realtime API](<https://developers.openai.com/api/docs/guides/realtime-conversations>). Most OpenAI client libraries and SDKs work with the xAI endpoint by changing the base URL to `wss://api.x.ai/v1/realtime`. This section documents event naming differences and unsupported events.

### Event Naming Differences

The xAI API uses different event names for a few events with different payloads:

  * OpenAI's `conversation.item.input_audio_transcription.delta` is named `conversation.item.input_audio_transcription.updated` in the xAI API. The `updated` event contains the cumulative transcript \(which may include corrections to previous updates\), rather than an incremental delta. Only emitted when `audio.input.transcription.model` is set to `"grok-transcribe"`.

### Unsupported Client Events

OpenAI Event| Notes  
---|---  
`conversation.item.retrieve`| Not supported.  
`output_audio_buffer.clear`| WebRTC/SIP only.  
  
### Unsupported Server Events

OpenAI Event| Notes  
---|---  
`conversation.item.done`| Not emitted.  
`conversation.item.input_audio_transcription.failed`| Not emitted.  
`conversation.item.input_audio_transcription.segment`| Not supported.  
`conversation.item.retrieved`| Not supported.  
`output_audio_buffer.started`| WebRTC/SIP only.  
`output_audio_buffer.stopped`| WebRTC/SIP only.  
`output_audio_buffer.cleared`| WebRTC/SIP only.  
`rate_limits.updated`| Not emitted.  
  
### xAI Extensions

These events and features are xAI-specific and not part of the OpenAI Realtime API:

Event / Feature| Description  
---|---  
`force_message`| New `conversation.item.create` item type for TTS-synthesized scripted utterances. See Force Message.  
`resumption`| Field on `session.update` that caches conversation turns and replays them on reconnect. See Session Resumption.  
`replace`| Field on `session.update` that maps phrases to spoken substitutions applied before TTS to fix pronunciation without changing the transcript. See Pronunciation Replacements.  
  
* * *

Last updated: June 29, 2026