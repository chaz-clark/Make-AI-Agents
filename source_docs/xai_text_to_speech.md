#### Model Capabilities

# Text to Speech

[View as Markdown](</developers/model-capabilities/audio/text-to-speech.md>)

[Create API key](<https://console.x.ai/team/default/api-keys>)[Try Playground](<https://console.x.ai/playground/voice/text-to-speech>)

Convert text into spoken audio with a single API call. The API supports 5 expressive voices, inline speech tags for fine-grained delivery control, and output formats from high-fidelity MP3 to telephony-optimized μ-law.

## Quick Start

Generate speech with a single API call:
    
    
    curl -X POST https://api.x.ai/v1/tts \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "Hello! Welcome to the xAI Text to Speech API.",
        "voice_id": "eve",
        "language": "en"
      }' \
      --output hello.mp3
    
    
    
    import os
    import requests
    
    response = requests.post(
        "https://api.x.ai/v1/tts",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": "Hello! Welcome to the xAI Text to Speech API.",
            "voice_id": "eve",
            "language": "en",
        },
    )
    response.raise_for_status()
    
    with open("hello.mp3", "wb") as f:
        f.write(response.content)
    
    print(f"Saved {len(response.content):,} bytes to hello.mp3")
    
    
    
    import fs from "fs";
    
    const response = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: "Hello! Welcome to the xAI Text to Speech API.",
        voice_id: "eve",
        language: "en",
      }),
    });
    
    if (!response.ok) throw new Error(`TTS error ${response.status}`);
    
    const buffer = Buffer.from(await response.arrayBuffer());
    fs.writeFileSync("hello.mp3", buffer);
    console.log(`Saved ${buffer.length.toLocaleString()} bytes to hello.mp3`);
    
    
    
    import Foundation
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    let url = URL(string: "https://api.x.ai/v1/tts")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONSerialization.data(withJSONObject: [
        "text": "Hello! Welcome to the xAI Text to Speech API.",
        "voice_id": "eve",
        "language": "en",
    ])
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let fileURL = URL(fileURLWithPath: "hello.mp3")
    try data.write(to: fileURL)
    
    print("Saved \(data.count) bytes to hello.mp3")
    

The response body contains raw audio bytes. Save directly to a file or pipe to an audio player.

[Try the Playground →](<https://console.x.ai/team/default/voice/text-to-speech?campaign=voice-docs-tts>)[Live Voice Demos](<https://x.ai/api/voice>)[Get API Key](<https://console.x.ai/team/default/api-keys?campaign=voice-docs-tts>)

* * *

## Request Body

Parameter| Type| Required| Description  
---|---|---|---  
`text`| string| ✓| The text to convert to speech. Maximum **15,000 characters**. Supports speech tags.  
`voice_id`| string| | Voice to use for synthesis. Defaults to `eve`. See Voices.  
`language`| string| ✓| BCP-47 language code \(e.g. `en`, `zh`, `pt-BR`\) or `auto` for automatic language detection. See Supported Languages.  
`output_format`| object| | Output format configuration. Defaults to MP3 at 24 kHz / 128 kbps. See Output Formats.  
`speed`| number| | Speech speed multiplier. `1.0` is normal speed. Values below `1.0` slow down speech, values above `1.0` speed it up. Range: `0.7` to `1.5`. Defaults to `1.0`.  
`optimize_streaming_latency`| integer| | Latency optimization level for streaming synthesis. `0` \(default\): No optimization — best audio quality. `1`: Reduced first-chunk size for lower time-to-first-audio, with minor quality tradeoff at chunk boundaries. `2`: Further reduced first-chunk size for lowest time-to-first-audio, with more noticeable quality tradeoff at chunk boundaries.  
`text_normalization`| boolean| | Enable text normalization before synthesis. When `true`, the model normalizes written-form text \(e.g. numbers, abbreviations, symbols\) into spoken-form before generating audio. Defaults to `false`.  
`with_timestamps`| boolean| | Return character-level timing metadata alongside the audio. When `true`, the response is a JSON envelope containing base64-encoded audio plus per-character start/end times. Adds latency for the post-synthesis alignment pass. Defaults to `false`. See Character-level timestamps.  
  
### Example with all options

JSON
    
    
    {
      "text": "Hello! This is a high-fidelity text to speech example.",
      "voice_id": "ara",
      "language": "en",
      "output_format": {
        "codec": "mp3",
        "sample_rate": 44100,
        "bit_rate": 192000
      },
      "speed": 1.2
    }
    

* * *

## Voices

Five voices are available, each with a distinct personality. Listen to samples and choose the best fit for your use case:

Voice| Tone| Description| Sample  
---|---|---|---  
**`eve`**|  Energetic, upbeat| Default voice - engaging and enthusiastic|   
**`ara`**|  Warm, friendly| Balanced and conversational|   
**`rex`**|  Confident, clear| Professional and articulate - ideal for business|   
**`sal`**|  Smooth, balanced| Versatile voice for a wide range of contexts|   
**`leo`**|  Authoritative, strong| Commanding and decisive - great for instructional content|   
  
Voice IDs are **case-insensitive** \- `eve`, `Eve`, and `EVE` all work. [Preview all voices in the playground →](<https://console.x.ai/team/default/voice/text-to-speech?campaign=voice-docs-tts>)

### Choosing the right voice

  * **`eve`** \- Great default for demos, announcements, and upbeat content
  * **`ara`** \- Ideal for conversational interfaces, customer support, and warm narration
  * **`rex`** \- Best for business presentations, corporate communications, and tutorials
  * **`sal`** \- Versatile choice for balanced delivery across different content types
  * **`leo`** \- Perfect for authoritative narration, instructions, and educational content

### Custom voices

Clone any voice from a short reference clip with the [Custom Voices API](</developers/model-capabilities/audio/custom-voices>), or create one for free in the [console](<https://console.x.ai/team/default/voice/voice-library?campaign=voice-docs-tts>). To find your custom voice ID in the console, click the three-dot menu on the voice card and select **Copy Voice ID**. Then pass it as `voice_id`:
    
    
    # Replace YOUR_VOICE_ID with your custom voice ID from the console
    # or the GET /v1/custom-voices endpoint.
    curl -X POST https://api.x.ai/v1/tts \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "Hello! This is my custom voice.",
        "voice_id": "YOUR_VOICE_ID",
        "language": "en"
      }' \
      --output hello.mp3
    
    
    
    import os
    import requests
    
    response = requests.post(
        "https://api.x.ai/v1/tts",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": "Hello! This is my custom voice.",
            "voice_id": "YOUR_VOICE_ID",  # replace with your custom voice ID
            "language": "en",
        },
    )
    response.raise_for_status()
    with open("hello.mp3", "wb") as f:
        f.write(response.content)
    
    
    
    import fs from "fs";
    
    const response = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: "Hello! This is my custom voice.",
        voice_id: "YOUR_VOICE_ID", // replace with your custom voice ID
        language: "en",
      }),
    });
    if (!response.ok) throw new Error(`TTS error ${response.status}: ${await response.text()}`);
    fs.writeFileSync("hello.mp3", Buffer.from(await response.arrayBuffer()));
    

You can also list voices programmatically with the [Text to speech - List voices](</developers/rest-api-reference/inference/voice#text-to-speech---list-voices>) endpoint:
    
    
    curl -s https://api.x.ai/v1/tts/voices \
      -H "Authorization: Bearer $XAI_API_KEY"
    
    
    
    import os
    import requests
    
    response = requests.get(
        "https://api.x.ai/v1/tts/voices",
        headers={"Authorization": f"Bearer {os.environ['XAI_API_KEY']}"},
    )
    for voice in response.json()["voices"]:
        print(f"{voice['voice_id']:5s}  {voice['name']}")
    
    
    
    const response = await fetch("https://api.x.ai/v1/tts/voices", {
      headers: { Authorization: `Bearer ${process.env.XAI_API_KEY}` },
    });
    const { voices } = await response.json();
    voices.forEach((v) => console.log(`${v.voice_id}  ${v.name}`));
    
    
    
    import Foundation
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    let url = URL(string: "https://api.x.ai/v1/tts/voices")!
    var request = URLRequest(url: url)
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let json = try JSONSerialization.jsonObject(with: data) as! [String: Any]
    let voices = json["voices"] as! [[String: Any]]
    for voice in voices {
        print("\(voice["voice_id"]!)  \(voice["name"]!)")
    }
    

* * *

## Supported Languages

The TTS API supports 20 languages via BCP-47 language codes. Use `auto` for automatic language detection, or specify a language code explicitly for consistent results.

Language code validation is **case-insensitive** — `en`, `EN`, and `En` all work.

Language| Language Code  
---|---  
Auto-detect| `auto`  
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
  
The model is also capable of generating speech in additional languages beyond those listed above, with varying degrees of accuracy.

* * *

## Speech Tags

ExampleFull tag reference →

So I walked in and \[pause\] there it was. \[laugh\] I honestly could not believe it\! <whisper>It was a secret the whole time.</whisper> Pretty cool, right?

Add inline speech tags to your text for expressive delivery. There are two types of tags:

  * **Inline tags** `[tag]` — placed at a specific point in the text to produce a vocal expression \(e.g. a laugh or pause\)
  * **Wrapping tags** `<tag>text</tag>` — wrap a section of text to change how it is delivered \(e.g. whispering, singing\)

### Inline Tags

Insert these where the expression should occur. Click any tag to hear an example:

Category| Tags  
---|---  
**Pauses**|   
**Laughter & crying**|   
**Mouth sounds**|   
**Breathing**|   
  
### Wrapping Tags

Wrap text to change delivery style. Use an opening tag and a matching closing tag. Click any tag to hear an example:

Category| Tags  
---|---  
**Volume & intensity**|   
**Pitch & speed**|   
**Vocal style**|   
  
### Examples
    
    
    # Inline tags
    curl -X POST https://api.x.ai/v1/tts \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "So I walked in and [pause] there it was. [laugh] I honestly could not believe it!",
        "voice_id": "eve",
        "language": "en"
      }' \
      --output expressive.mp3
    
    # Wrapping tags
    curl -X POST https://api.x.ai/v1/tts \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "I need to tell you something. <whisper>It is a secret.</whisper> Pretty cool, right?",
        "voice_id": "eve",
        "language": "en"
      }' \
      --output whisper.mp3
    
    
    
    import os
    import requests
    
    # Inline tags
    response = requests.post(
        "https://api.x.ai/v1/tts",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": "So I walked in and [pause] there it was. [laugh] I honestly could not believe it!",
            "voice_id": "eve",
            "language": "en",
        },
    )
    response.raise_for_status()
    
    with open("expressive.mp3", "wb") as f:
        f.write(response.content)
    
    # Wrapping tags
    response = requests.post(
        "https://api.x.ai/v1/tts",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": "I need to tell you something. <whisper>It is a secret.</whisper> Pretty cool, right?",
            "voice_id": "eve",
            "language": "en",
        },
    )
    response.raise_for_status()
    
    with open("whisper.mp3", "wb") as f:
        f.write(response.content)
    
    
    
    // Inline tags
    const response = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: "So I walked in and [pause] there it was. [laugh] I honestly could not believe it!",
        voice_id: "eve",
        language: "en",
      }),
    });
    
    // Wrapping tags
    const whisperResponse = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: "I need to tell you something. <whisper>It is a secret.</whisper> Pretty cool, right?",
        voice_id: "eve",
        language: "en",
      }),
    });
    
    
    
    import Foundation
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    let url = URL(string: "https://api.x.ai/v1/tts")!
    
    // Inline tags
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONSerialization.data(withJSONObject: [
        "text": "So I walked in and [pause] there it was. [laugh] I honestly could not believe it!",
        "voice_id": "eve",
        "language": "en",
    ])
    
    let (data, _) = try await URLSession.shared.data(for: request)
    try data.write(to: URL(fileURLWithPath: "expressive.mp3"))
    
    // Wrapping tags
    request.httpBody = try JSONSerialization.data(withJSONObject: [
        "text": "I need to tell you something. <whisper>It is a secret.</whisper> Pretty cool, right?",
        "voice_id": "eve",
        "language": "en",
    ])
    
    let (whisperData, _) = try await URLSession.shared.data(for: request)
    try whisperData.write(to: URL(fileURLWithPath: "whisper.mp3"))
    

**Tips for speech tags:**

  * Place inline tags where the expression would naturally occur in conversation
  * Combine tags with punctuation — `"Really? [laugh] That's incredible!"` produces more natural results than stacking tags
  * Use `[pause]` or `[long-pause]` to add dramatic timing or let a thought land
  * Wrapping tags work best around complete phrases — `<whisper>It is a secret.</whisper>` reads more naturally than wrapping individual words
  * Combine styles for effect — `<slow><soft>Goodnight, sleep well.</soft></slow>`

* * *

## Output Formats

Control the audio codec, sample rate, and bit rate with the `output_format` object. When omitted, the default is **MP3 at 24 kHz / 128 kbps**.

### Codecs

Codec| Content-Type| Best for  
---|---|---  
`mp3`| `audio/mpeg`| General use - wide compatibility, good compression  
`wav`| `audio/wav`| Lossless audio - editing, post-production  
`pcm`| `audio/pcm`| Raw audio - real-time processing pipelines  
`mulaw`| `audio/basic`| Telephony \(G.711 μ-law\)  
`alaw`| `audio/alaw`| Telephony \(G.711 A-law\)  
  
### Sample Rates

Rate| Description  
---|---  
`8000`| Narrowband - telephony  
`16000`| Wideband - speech recognition  
`22050`| Standard - balanced quality  
`24000`| High quality - **default** , recommended for most use cases  
`44100`| CD quality - media production  
`48000`| Professional - studio-grade audio  
  
### Bit Rates \(MP3 only\)

Rate| Quality  
---|---  
`32000`| Low - smallest file size  
`64000`| Medium - good for speech  
`96000`| Standard - balanced  
`128000`| High - **default** , recommended  
`192000`| Maximum - highest fidelity  
  
### Example: High-fidelity MP3

JSON
    
    
    {
      "text": "Crystal clear audio at maximum quality.",
      "voice_id": "rex",
      "language": "en",
      "output_format": {
        "codec": "mp3",
        "sample_rate": 44100,
        "bit_rate": 192000
      }
    }
    

### Example: Telephony \(μ-law\)

JSON
    
    
    {
      "text": "Hello, thank you for calling. How can I help you today?",
      "voice_id": "ara",
      "language": "en",
      "output_format": {
        "codec": "mulaw",
        "sample_rate": 8000
      }
    }
    

* * *

## Character-level timestamps

Set `with_timestamps` to `true` to receive per-character start and end timestamps. Ideal for syncing captions, karaoke highlights, real-time lip-sync, or other time-aligned applications.

The response then changes from raw audio bytes to a JSON envelope \(`Content-Type: application/json`\) carrying the base64-encoded audio plus the character timings.

### Requesting timestamps

Add the flag to a normal request. The audio comes back inside the JSON body, not as raw bytes:
    
    
    curl -X POST https://api.x.ai/v1/tts \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "text": "Hello world.",
        "voice_id": "eve",
        "language": "en",
        "with_timestamps": true
      }' \
      --output response.json
    
    
    
    import base64
    import os
    import requests
    
    response = requests.post(
        "https://api.x.ai/v1/tts",
        headers={
            "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "text": "Hello world.",
            "voice_id": "eve",
            "language": "en",
            "with_timestamps": True,
        },
    )
    response.raise_for_status()
    payload = response.json()
    
    # The audio is base64-encoded — decode it exactly like a normal response
    with open("hello.mp3", "wb") as f:
        f.write(base64.b64decode(payload["audio"]))
    
    ts = payload["audio_timestamps"]
    for char, (start, end) in zip(ts["graph_chars"], ts["graph_times"]):
        print(f"{char!r:>5}  {start:.2f}s – {end:.2f}s")
    print(f"duration: {payload['duration']:.2f}s")
    
    
    
    import fs from "fs";
    
    const response = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: "Hello world.",
        voice_id: "eve",
        language: "en",
        with_timestamps: true,
      }),
    });
    if (!response.ok) throw new Error(`TTS error ${response.status}`);
    
    const payload = await response.json();
    
    // The audio is base64-encoded — decode it exactly like a normal response
    fs.writeFileSync("hello.mp3", Buffer.from(payload.audio, "base64"));
    
    const { graph_chars, graph_times } = payload.audio_timestamps;
    graph_chars.forEach((char, i) => {
      const [start, end] = graph_times[i];
      console.log(`${JSON.stringify(char).padStart(5)}  ${start.toFixed(2)}s – ${end.toFixed(2)}s`);
    });
    console.log(`duration: ${payload.duration.toFixed(2)}s`);
    
    
    
    import Foundation
    
    // snake_case JSON keys map to camelCase via the decoder strategy below
    struct TimedTts: Decodable {
        let audio: String
        let contentType: String
        let duration: Double
        let audioTimestamps: AudioTimestamps?
    
        struct AudioTimestamps: Decodable {
            let graphChars: [String]
            let graphTimes: [[Double]]
        }
    }
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    var request = URLRequest(url: URL(string: "https://api.x.ai/v1/tts")!)
    request.httpMethod = "POST"
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    request.httpBody = try JSONSerialization.data(withJSONObject: [
        "text": "Hello world.",
        "voice_id": "eve",
        "language": "en",
        "with_timestamps": true,
    ])
    
    let (data, _) = try await URLSession.shared.data(for: request)
    let decoder = JSONDecoder()
    decoder.keyDecodingStrategy = .convertFromSnakeCase
    let payload = try decoder.decode(TimedTts.self, from: data)
    
    // The audio is base64-encoded — decode it exactly like a normal response
    try Data(base64Encoded: payload.audio)!.write(to: URL(fileURLWithPath: "hello.mp3"))
    
    if let ts = payload.audioTimestamps {
        for (char, time) in zip(ts.graphChars, ts.graphTimes) {
            print(String(format: "%5@  %.2fs – %.2fs", char as NSString, time[0], time[1]))
        }
    }
    print(String(format: "duration: %.2fs", payload.duration))
    

### Response shape

JSON
    
    
    {
      "audio": "<base64-encoded audio in the requested codec>",
      "content_type": "audio/mpeg",
      "duration": 0.92,
      "audio_timestamps": {
        "graph_chars": ["H", "e", "l", "l", "o", " ", "w", "o", "r", "l", "d", "."],
        "graph_times": [
          [0.00, 0.06],
          [0.06, 0.12],
          [0.12, 0.18],
          [0.18, 0.24],
          [0.24, 0.34],
          [0.34, 0.40],
          [0.40, 0.48],
          [0.48, 0.54],
          [0.54, 0.62],
          [0.62, 0.68],
          [0.68, 0.78],
          [0.78, 0.92]
        ]
      }
    }
    

Field| Type| Description  
---|---|---  
`audio`| string| Base64-encoded audio in the requested codec. Decode and play like a normal response.  
`content_type`| string| MIME type of the decoded audio \(e.g. `audio/mpeg`, `audio/wav`\).  
`duration`| number| Total audio duration in seconds.  
`audio_timestamps.graph_chars`| string\[\]| Each input character, in order, including spaces, punctuation, and speech tags.  
`audio_timestamps.graph_times`| number\[\]\[\]| Parallel array of `[start, end]` pairs in seconds.  
  
`graph_chars` and `graph_times` are aligned by index, they match position by position. So graph\_chars\[i\] is the character spoken during the time interval graph\_times\[i\]. For `"Hello world."`:

Text
    
    
    char:    H     e     l     l     o     ␣     w     o     r     l     d     .
    start:  0.00  0.06  0.12  0.18  0.24  0.34  0.40  0.48  0.54  0.62  0.68  0.78
            └──────────── "Hello" ───────────┘     └──────────── "world." ──────────┘
    0s ─────────────────────────────────────────────────────────────────────▶ 0.92s
    

### Special characters

`graph_chars` mirrors your input one-for-one, including spaces, punctuation, and speech tags. When one written token is spoken as several words, its timing is assigned to the first character. The rest of the characters interpolate within that same time span.

This mostly happens with `text_normalization` enabled, which expands symbols and numbers into words. With normalization on, `$5` is spoken as "five dollars" but is still only two characters: the `$` gets the full span for "five dollars", and the `5` gets an interpolated time inside it. So always step through `graph_chars` in order rather than slicing the input text by index.

* * *

## Best Practices

Tips for getting the highest quality output from the TTS API.

### Writing effective text

  * **Use natural punctuation.** Commas, periods, and question marks guide pacing and intonation. `"Wait, really?"` sounds more natural than `"Wait really"`.
  * **Add emotional context.** Exclamation marks and question marks influence delivery - `"That's amazing!"` sounds enthusiastic while `"That's amazing."` is matter-of-fact.
  * **Break long content into paragraphs.** Paragraph breaks create natural pauses and help the model maintain consistent quality across longer text.
  * **Keep unary requests under 15,000 characters.** For longer content, use the bidirectional WebSocket endpoint which has no text length limit, or split into logical segments \(by paragraph or sentence\) and concatenate the audio output.

### Integrating with AI coding assistants

The [Cloud Console playground](<https://console.x.ai/team/default/voice/text-to-speech?campaign=voice-docs-tts>) includes ready-made **agent instructions** you can copy and paste into tools like Cursor, GitHub Copilot, or Windsurf. The instructions are pre-configured with your current voice and format settings - open the playground, tweak your settings, and copy the prompt to get a tailored integration guide for your coding agent.

### Optimizing for production

  * **Proxy requests server-side.** Never expose your API key in client-side code. Route TTS requests through your backend.
  * **Cache generated audio.** If the same text is requested repeatedly, cache the audio bytes to save API calls and reduce latency.
  * **Match the format to the use case.** Use `mulaw` or `alaw` at 8 kHz for telephony; `mp3` at 24 kHz for web; `wav` at 44.1+ kHz for post-production.
  * **Respect concurrent session limits.** The streaming WebSocket endpoint allows up to **50 concurrent sessions per team**. For high-throughput services, pool connections or queue requests to stay within this limit.

* * *

## Browser Playback

To play TTS audio in the browser, proxy the request through your backend and use the Web Audio API or an `<audio>` element:

JavaScript
    
    
    // Client-side: fetch from your backend proxy, then play
    async function speakText(text, voiceId = "eve") {
      const response = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, voice_id: voiceId }),
      });
    
      if (!response.ok) throw new Error("TTS request failed");
    
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
    
      const audio = new Audio(url);
      audio.addEventListener("ended", () => URL.revokeObjectURL(url));
      await audio.play();
    }
    
    // Usage
    await speakText("Hello from the browser!");
    

**Never call the TTS API directly from the browser** \- this would expose your API key. Always proxy through your backend.

### Browser gotchas

**Safari returns`Infinity` for `audio.duration` on blob URLs.** The `loadedmetadata` event fires but `audio.duration` is `Infinity`, breaking seek bars and time displays. Use `AudioContext.decodeAudioData()` instead:

JavaScript
    
    
    async function getAudioDuration(arrayBuffer) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const ctx = new AudioCtx();
      // Clone the buffer - decodeAudioData detaches the original
      const decoded = await ctx.decodeAudioData(arrayBuffer.slice(0));
      const durationMs = Math.round(decoded.duration * 1000);
      await ctx.close();
      return durationMs;
    }
    

**`AudioContext` must be created during a user gesture on Safari.** Safari permanently suspends an `AudioContext` created outside a click/tap handler, with no way to resume it. Chrome is more lenient. Always create or resume the context in your button's click handler, before any `await`:

JavaScript
    
    
    // Create the AudioContext once, in a click handler
    let audioCtx;
    button.addEventListener("click", async () => {
      // This MUST happen synchronously in the click handler for Safari
      if (!audioCtx) audioCtx = new AudioContext();
      if (audioCtx.state === "suspended") await audioCtx.resume();
    
      // Now it's safe to fetch and play audio asynchronously
      const response = await fetch("/api/tts", { /* ... */ });
      const arrayBuffer = await response.arrayBuffer();
      const decoded = await audioCtx.decodeAudioData(arrayBuffer);
      const source = audioCtx.createBufferSource();
      source.buffer = decoded;
      source.connect(audioCtx.destination);
      source.start();
    });
    

**Raw codecs \(pcm, mulaw, alaw\) are not playable in the browser.** `AudioContext.decodeAudioData()` and `<audio>` elements only support container formats like MP3 and WAV. Use `mp3` or `wav` for browser playback. If you're working with raw formats server-side \(e.g., piping to telephony\), estimate duration from byte count:

JavaScript
    
    
    // PCM = 16-bit LE (2 bytes/sample), mulaw/alaw = 8-bit (1 byte/sample)
    const bytesPerSample = codec === "pcm" ? 2 : 1;
    const durationMs = Math.round((byteLength / bytesPerSample / sampleRate) * 1000);
    

**Revoke blob URLs to avoid memory leaks.** Each `URL.createObjectURL()` call allocates memory that persists until explicitly freed. Revoke URLs when playback ends. For downloads, delay revocation so the browser finishes saving the file:

JavaScript
    
    
    // Playback: revoke when done
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.addEventListener("ended", () => URL.revokeObjectURL(url));
    
    // Downloads: delay revocation
    const downloadUrl = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "speech.mp3";
    a.click();
    setTimeout(() => URL.revokeObjectURL(downloadUrl), 10_000);
    

* * *

## Error Handling

Status| Meaning| Action  
---|---|---  
`200`| Success| Audio bytes in the response body  
`400`| Bad request| Check: text is non-empty, under 15,000 chars; codec and sample rate are valid  
`401`| Unauthorized| API key is missing or invalid  
`404`| Not found| Unknown `voice_id` — verify via `GET /v1/tts/voices` \(built-in\) or `GET /v1/custom-voices` \(custom\)  
`429`| Rate limited| Back off and retry with exponential delay  
`503`| Service unavailable| TTS service is temporarily unavailable - retry  
`500`| Server error| Retry with exponential backoff  
  
### Retry with backoff
    
    
    import os
    import time
    import requests
    
    def generate_speech(text, language="en", voice_id="eve", max_retries=3):
        for attempt in range(max_retries):
            response = requests.post(
                "https://api.x.ai/v1/tts",
                headers={
                    "Authorization": f"Bearer {os.environ['XAI_API_KEY']}",
                    "Content-Type": "application/json",
                },
                json={"text": text, "language": language, "voice_id": voice_id},
            )
            if response.ok:
                return response.content
            if response.status_code in (429, 500, 503):
                wait = 2 ** attempt
                time.sleep(wait)
                continue
            response.raise_for_status()  # Non-retryable error
        raise RuntimeError("Max retries exceeded")
    
    
    
    async function generateSpeech(text, language = "en", voiceId = "eve", maxRetries = 3) {
      for (let attempt = 0; attempt < maxRetries; attempt++) {
        const response = await fetch("https://api.x.ai/v1/tts", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${process.env.XAI_API_KEY}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text, language, voice_id: voiceId }),
        });
    
        if (response.ok) return Buffer.from(await response.arrayBuffer());
    
        if ([429, 500, 503].includes(response.status)) {
          await new Promise((r) => setTimeout(r, 2 ** attempt * 1000));
          continue;
        }
        throw new Error(`TTS error ${response.status}: ${await response.text()}`);
      }
      throw new Error("Max retries exceeded");
    }
    
    
    
    import Foundation
    
    func generateSpeech(text: String, language: String = "en", voiceId: String = "eve", maxRetries: Int = 3) async throws -> Data {
        let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
        let url = URL(string: "https://api.x.ai/v1/tts")!
    
        for attempt in 0..<maxRetries {
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = try JSONSerialization.data(withJSONObject: [
                "text": text, "language": language, "voice_id": voiceId,
            ])
    
            let (data, response) = try await URLSession.shared.data(for: request)
            let status = (response as! HTTPURLResponse).statusCode
            if status == 200 { return data }
            if [429, 500, 503].contains(status) {
                try await Task.sleep(nanoseconds: UInt64(pow(2.0, Double(attempt))) * 1_000_000_000)
                continue
            }
            throw URLError(.badServerResponse)
        }
        throw URLError(.timedOut)
    }
    

* * *

## Limits

The unary/server-streamed endpoints and the bidirectional WebSocket endpoint have different limits:

| Unary & server-streamed \(`POST /v1/tts`\)| Bidirectional WebSocket \(`wss://api.x.ai/v1/tts`\)  
---|---|---  
**Max text length**|  15,000 characters per request| No limit — individual `text.delta` messages capped at 15,000 characters each  
**Request timeout**|  15 minutes| No timeout \(connection stays open\)  
**Concurrent sessions**|  —| 50 per team  
  
For content exceeding 15,000 characters, use the bidirectional WebSocket endpoint which has no text length limit.

* * *

## Streaming TTS \(WebSocket\)

For real-time audio generation, open a WebSocket connection to the streaming TTS endpoint. Text is streamed in as deltas and audio is streamed back as base64-encoded chunks — ideal for interactive applications where you want audio to start playing before the full text is available.

**Endpoint:** `wss://api.x.ai/v1/tts`

**Never expose your API key in client-side code.** Always proxy WebSocket connections through your backend.

* * *

### Connection

Open a WebSocket connection with query parameters to configure language, voice, and audio format:

Text
    
    
    GET /v1/tts?language=en&voice=eve&codec=mp3&sample_rate=24000&bit_rate=128000
    Upgrade: websocket
    Authorization: Bearer $XAI_API_KEY
    

Parameter| Required| Default| Accepted values  
---|---|---|---  
`voice`| | `eve`| `ara`, `eve`, `leo`, `rex`, `sal`  
`language`| ✓| | `auto` or BCP-47 codes \(e.g. `en`, `zh`, `pt-BR`\). See Supported Languages.  
`codec`| | `mp3`| `mp3`, `wav`, `pcm`, `mulaw` \(or `ulaw`\), `alaw`  
`sample_rate`| | `24000`| `8000`, `16000`, `22050`, `24000`, `44100`, `48000`  
`bit_rate`| | `128000`| `32000`, `64000`, `96000`, `128000`, `192000` \(MP3 only\)  
`speed`| | `1.0`| Speech speed multiplier \(`0.7` to `1.5`\)  
`optimize_streaming_latency`| | `0`| `0` \(off, best quality\), `1` \(moderate, lower time-to-first-audio\), `2` \(aggressive, lowest time-to-first-audio\)  
`text_normalization`| | `false`| `true`, `false`  
`with_timestamps`| | `false`| `true`, `false`. When `true`, each `audio.delta` carries `audio_timestamps` and `audio_duration` for the characters in that chunk.  
  
An invalid `voice`, `language`, `codec`, or `sample_rate` is rejected **before** the WebSocket upgrade with an HTTP 400 or 404.

* * *

### Client → Server Messages

Send text to the server as JSON text frames. Split your text across multiple `text.delta` messages, then signal the end of the utterance with `text.done`:

JSON
    
    
    {"type": "text.delta", "delta": "Here is some text. "}
    {"type": "text.delta", "delta": "More text follows."}
    {"type": "text.done"}
    

Event| Description  
---|---  
`text.delta`| A chunk of text to synthesize. Individual deltas are capped at **15,000 characters**.  
`text.done`| Signals the end of the current utterance. The server will finish generating audio and send `audio.done`.  
`text.clear`| Cancel the current utterance. The server stops generating audio, discards any buffered data, and responds with `audio.clear`.  
  
* * *

### Server → Client Messages

The server responds with base64-encoded audio chunks and a completion event:

JSON
    
    
    {"type": "audio.delta", "delta": "<base64-encoded audio bytes>"}
    {"type": "audio.done", "trace_id": "uuid"}
    {"type": "audio.clear"}
    {"type": "error", "message": "description"}
    

Event| Description  
---|---  
`audio.delta`| A chunk of base64-encoded audio in the codec specified at connection time. Decode and enqueue for playback. When the connection was opened with `with_timestamps=true`, also carries `audio_timestamps` \(`graph_chars` \+ `graph_times`\) and `audio_duration` for the characters in that chunk. See Character-level timestamps.  
`audio.done`| All audio for the current utterance has been sent. Includes a `trace_id` for debugging.  
`audio.clear`| Confirms that the current utterance was cancelled in response to `text.clear`. The connection is ready for the next utterance.  
`error`| An error occurred. The `message` field contains a human-readable description.  
  
* * *

### Multi-Utterance Sessions

The connection stays open after `audio.done`. You can immediately send another round of `text.delta` → `text.done` messages to synthesize additional text without reconnecting. This is useful for conversational UIs where you generate audio for each assistant response in sequence.

**Flow for multi-turn sessions:**

  1. **Turn 1:** Client sends `text.delta` → `text.done`
  2. Server responds with `audio.delta` chunks → `audio.done`
  3. Connection stays open
  4. **Turn 2:** Client sends `text.delta` → `text.done`
  5. Server responds with `audio.delta` chunks → `audio.done`
  6. Repeat as needed

Each `text.done` flushes the accumulated text to generate audio. Once you receive `audio.done`, you can send more text for the next turn. The audio from each turn is independent — content from turn 1 does not bleed into turn 2.
    
    
    import asyncio
    import base64
    import json
    import os
    
    import websockets  # pip install websockets
    
    XAI_API_KEY = os.environ["XAI_API_KEY"]
    
    async def multi_turn_tts(language: str = "en", voice: str = "eve", codec: str = "mp3"):
        uri = f"wss://api.x.ai/v1/tts?language={language}&voice={voice}&codec={codec}"
    
        async with websockets.connect(
            uri,
            additional_headers={"Authorization": f"Bearer {XAI_API_KEY}"},
        ) as ws:
            # Turn 1
            await ws.send(json.dumps({"type": "text.delta", "delta": "Hello from turn one."}))
            await ws.send(json.dumps({"type": "text.done"}))
    
            turn1_audio = bytearray()
            async for msg in ws:
                event = json.loads(msg)
                if event["type"] == "audio.delta":
                    turn1_audio.extend(base64.b64decode(event["delta"]))
                elif event["type"] == "audio.done":
                    print(f"Turn 1: {len(turn1_audio):,} bytes")
                    break
                elif event["type"] == "error":
                    raise RuntimeError(event["message"])
    
            # Connection is still open — send turn 2
            await ws.send(json.dumps({"type": "text.delta", "delta": "And hello from turn two."}))
            await ws.send(json.dumps({"type": "text.done"}))
    
            turn2_audio = bytearray()
            async for msg in ws:
                event = json.loads(msg)
                if event["type"] == "audio.delta":
                    turn2_audio.extend(base64.b64decode(event["delta"]))
                elif event["type"] == "audio.done":
                    print(f"Turn 2: {len(turn2_audio):,} bytes")
                    break
                elif event["type"] == "error":
                    raise RuntimeError(event["message"])
    
    asyncio.run(multi_turn_tts())
    
    
    
    // npm install ws
    // Node.js 22+ has a built-in WebSocket global — you can skip
    // the "ws" package and remove this import if you're on v22+.
    import WebSocket from "ws";
    
    const apiKey = process.env.XAI_API_KEY;
    const language = "en";
    const voice = "eve";
    const codec = "mp3";
    const uri = `wss://api.x.ai/v1/tts?language=${language}&voice=${voice}&codec=${codec}`;
    
    const ws = new WebSocket(uri, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    
    let turn = 1;
    let audioChunks = [];
    
    ws.on("open", () => {
      // Start turn 1
      ws.send(JSON.stringify({ type: "text.delta", delta: "Hello from turn one." }));
      ws.send(JSON.stringify({ type: "text.done" }));
    });
    
    ws.on("message", (data) => {
      const event = JSON.parse(data);
    
      if (event.type === "audio.delta") {
        audioChunks.push(Buffer.from(event.delta, "base64"));
      } else if (event.type === "audio.done") {
        const audio = Buffer.concat(audioChunks);
        console.log(`Turn ${turn}: ${audio.length.toLocaleString()} bytes`);
        audioChunks = [];
    
        if (turn === 1) {
          // Connection still open — send turn 2
          turn = 2;
          ws.send(JSON.stringify({ type: "text.delta", delta: "And hello from turn two." }));
          ws.send(JSON.stringify({ type: "text.done" }));
        } else {
          ws.close();
        }
      } else if (event.type === "error") {
        console.error("Error:", event.message);
        ws.close();
      }
    });
    
    
    
    import Foundation
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    let language = "en"
    let voice = "eve"
    let codec = "mp3"
    let url = URL(string: "wss://api.x.ai/v1/tts?language=\(language)&voice=\(voice)&codec=\(codec)")!
    
    var request = URLRequest(url: url)
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    
    let task = URLSession.shared.webSocketTask(with: request)
    task.resume()
    
    // Turn 1
    try await task.send(.string("{\"type\":\"text.delta\",\"delta\":\"Hello from turn one.\"}"))
    try await task.send(.string("{\"type\":\"text.done\"}"))
    
    var turn1Audio = Data()
    while true {
        let message = try await task.receive()
        guard case .string(let text) = message,
              let json = try? JSONSerialization.jsonObject(with: Data(text.utf8)) as? [String: Any],
              let type = json["type"] as? String else { continue }
    
        if type == "audio.delta", let delta = json["delta"] as? String,
           let chunk = Data(base64Encoded: delta) {
            turn1Audio.append(chunk)
        } else if type == "audio.done" {
            print("Turn 1: \(turn1Audio.count) bytes")
            break
        } else if type == "error" {
            print("Error: \(json["message"] ?? "unknown")")
            break
        }
    }
    
    // Connection still open — send turn 2
    try await task.send(.string("{\"type\":\"text.delta\",\"delta\":\"And hello from turn two.\"}"))
    try await task.send(.string("{\"type\":\"text.done\"}"))
    
    var turn2Audio = Data()
    while true {
        let message = try await task.receive()
        guard case .string(let text) = message,
              let json = try? JSONSerialization.jsonObject(with: Data(text.utf8)) as? [String: Any],
              let type = json["type"] as? String else { continue }
    
        if type == "audio.delta", let delta = json["delta"] as? String,
           let chunk = Data(base64Encoded: delta) {
            turn2Audio.append(chunk)
        } else if type == "audio.done" {
            print("Turn 2: \(turn2Audio.count) bytes")
            break
        } else if type == "error" {
            print("Error: \(json["message"] ?? "unknown")")
            break
        }
    }
    
    task.cancel(with: .normalClosure, reason: nil)
    

* * *

### Cancellation \(Barge-in\)

Send `text.clear` to cancel the current utterance and start a new one on the same connection — no reconnect needed. This eliminates the WebSocket handshake latency \(~600ms for distant clients\) on every interruption.

**Flow for barge-in:**

  1. Client sends `text.delta` → `text.done`
  2. Server starts streaming `audio.delta` chunks
  3. User interrupts — client sends `text.clear`
  4. Server responds with `audio.clear`
  5. Client sends new `text.delta` → `text.done`
  6. Server streams fresh `audio.delta` chunks → `audio.done`

`text.clear` is safe to send at any time — if no utterance is in progress, the server responds with `audio.clear` immediately. Clear your local audio playback buffer when you receive `audio.clear` to prevent stale audio from playing.
    
    
    import asyncio
    import base64
    import json
    import os
    
    import websockets  # pip install websockets
    
    XAI_API_KEY = os.environ["XAI_API_KEY"]
    
    async def tts_with_barge_in(language: str = "en", voice: str = "eve", codec: str = "mp3"):
        uri = f"wss://api.x.ai/v1/tts?language={language}&voice={voice}&codec={codec}"
    
        async with websockets.connect(
            uri,
            additional_headers={"Authorization": f"Bearer {XAI_API_KEY}"},
        ) as ws:
            # Start first utterance
            await ws.send(json.dumps({"type": "text.delta", "delta": "The answer to your question is a long explanation..."}))
            await ws.send(json.dumps({"type": "text.done"}))
    
            # Wait for audio to start, then cancel
            event = json.loads(await ws.recv())
            print(f"Got {event['type']} — cancelling")
            await ws.send(json.dumps({"type": "text.clear"}))
    
            async for msg in ws:
                if json.loads(msg)["type"] == "audio.clear":
                    break
    
            # New utterance on the same connection
            await ws.send(json.dumps({"type": "text.delta", "delta": "Actually, let me start over."}))
            await ws.send(json.dumps({"type": "text.done"}))
    
            audio = bytearray()
            async for msg in ws:
                event = json.loads(msg)
                if event["type"] == "audio.delta":
                    audio.extend(base64.b64decode(event["delta"]))
                elif event["type"] == "audio.done":
                    print(f"New utterance: {len(audio):,} bytes")
                    break
    
    asyncio.run(tts_with_barge_in())
    
    
    
    // npm install ws
    import WebSocket from "ws";
    
    const apiKey = process.env.XAI_API_KEY;
    const uri = `wss://api.x.ai/v1/tts?language=en&voice=eve&codec=mp3`;
    
    const ws = new WebSocket(uri, {
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    
    let phase = "first-utterance";
    
    ws.on("open", () => {
      ws.send(JSON.stringify({ type: "text.delta", delta: "The answer to your question is a long explanation..." }));
      ws.send(JSON.stringify({ type: "text.done" }));
    });
    
    ws.on("message", (data) => {
      const event = JSON.parse(data);
    
      if (phase === "first-utterance" && event.type === "audio.delta") {
        console.log("Audio started — cancelling");
        ws.send(JSON.stringify({ type: "text.clear" }));
        phase = "waiting-clear";
      } else if (phase === "waiting-clear" && event.type === "audio.clear") {
        phase = "second-utterance";
        ws.send(JSON.stringify({ type: "text.delta", delta: "Actually, let me start over." }));
        ws.send(JSON.stringify({ type: "text.done" }));
      } else if (phase === "second-utterance" && event.type === "audio.done") {
        console.log("New utterance complete");
        ws.close();
      }
    });
    
    
    
    import Foundation
    
    let apiKey = ProcessInfo.processInfo.environment["XAI_API_KEY"]!
    let url = URL(string: "wss://api.x.ai/v1/tts?language=en&voice=eve&codec=mp3")!
    var request = URLRequest(url: url)
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    
    let task = URLSession.shared.webSocketTask(with: request)
    task.resume()
    
    // Start first utterance
    try await task.send(.string("{\"type\":\"text.delta\",\"delta\":\"The answer is a long explanation...\"}"))
    try await task.send(.string("{\"type\":\"text.done\"}"))
    
    // Wait for first audio chunk, then cancel
    if case .string(let text) = try await task.receive(),
       let json = try? JSONSerialization.jsonObject(with: Data(text.utf8)) as? [String: Any],
       json["type"] as? String == "audio.delta" {
        try await task.send(.string("{\"type\":\"text.clear\"}"))
    }
    
    // Wait for audio.clear
    while true {
        guard case .string(let text) = try await task.receive(),
              let json = try? JSONSerialization.jsonObject(with: Data(text.utf8)) as? [String: Any] else { continue }
        if json["type"] as? String == "audio.clear" { break }
    }
    
    // New utterance on the same connection
    try await task.send(.string("{\"type\":\"text.delta\",\"delta\":\"Actually, let me start over.\"}"))
    try await task.send(.string("{\"type\":\"text.done\"}"))
    
    var audio = Data()
    while true {
        guard case .string(let text) = try await task.receive(),
              let json = try? JSONSerialization.jsonObject(with: Data(text.utf8)) as? [String: Any],
              let type = json["type"] as? String else { continue }
        if type == "audio.delta", let d = json["delta"] as? String, let c = Data(base64Encoded: d) { audio.append(c) }
        else if type == "audio.done" { print("New utterance: \(audio.count) bytes"); break }
    }
    
    task.cancel(with: .normalClosure, reason: nil)
    

* * *

### Limits and Behavior

Property| Value  
---|---  
**Total text length**|  No limit — send as many `text.delta` messages as needed  
**Delta size**|  Individual `text.delta` messages capped at 15,000 characters  
**Concurrent sessions**|  50 per team  
**Session permit TTL**|  600 seconds  
**Moderation**|  Runs asynchronously on accumulated text after audio is sent \(fail-open\)  
**Billing**|  Recorded per session based on total input characters  
  
* * *

## Related

  * [TTS Playground](<https://console.x.ai/team/default/voice/text-to-speech?campaign=voice-docs-tts>) \- Try voices and speech tags in your browser
  * [Create an API Key](<https://console.x.ai/team/default/api-keys?campaign=voice-docs-tts>) \- Get started with the API
  * [Voice Overview](</developers/model-capabilities/audio/voice>) \- Overview of all xAI voice capabilities
  * [Voice Agent API](</developers/model-capabilities/audio/voice-agent>) \- Real-time voice conversations via WebSocket
  * [API Reference](</developers/rest-api-reference/inference/voice#text-to-speech---rest>) \- Full TTS endpoint specification
  * [List Voices](</developers/rest-api-reference/inference/voice#text-to-speech---list-voices>) \- Programmatically discover available voices

* * *

Last updated: July 2, 2026