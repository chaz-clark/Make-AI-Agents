#### Key Information

# Models

### Code API Pricing

| Model | Context | Input / 1M tokens | Output / 1M tokens |
| --- | --- | --- | --- |
| grok-build-0.1 | 256k | $1.00 | $2.00 |

*Prices shown per million tokens*

### Chat API Pricing

| Model | Context | Input / 1M tokens | Output / 1M tokens |
| --- | --- | --- | --- |
| grok-4.3 | 1M | $1.25 | $2.50 |
| grok-4.20-0309-reasoning | 1M | $1.25 | $2.50 |
| grok-4.20-0309-non-reasoning | 1M | $1.25 | $2.50 |
| grok-4.20-multi-agent-0309 | 1M | $1.25 | $2.50 |

*Prices shown per million tokens*

### Imagine Pricing

| Model | Cost |
| --- | --- |
| grok-imagine-image | $0.02 / image |
| grok-imagine-image-quality | $0.05 / image |
| grok-imagine-video | $0.050 / sec |
| grok-imagine-video-1.5 | $0.080 / sec |

### Voice Pricing

| Mode | Cost |
| --- | --- |
| Realtime | $0.05 / min ($3.00 / hr) |
| Realtime Text Input | $0.004 / message (every conversation.item.create) |
| Text to Speech | $15.00 / 1M chars |
| Speech to Text | $0.10 / hr (REST), $0.20 / hr (Streaming) |

## Which model should I choose?

Your choice depends on your use case. We have dedicated models and APIs for code, audio, image, and video capabilities. For code, use Grok Build — it is our coding model. For everything else, use Grok 4.3. It is the most intelligent and fastest model we’ve built.

Code: [Grok Build](/developers/models/grok-build-0.1)

Chat: [Grok 4.3](/developers/models/grok-4.3)

Images: [Grok Imagine API](/developers/models/grok-imagine-image-quality)

Videos: [Grok Imagine API](/developers/models/grok-imagine-video)

Voice: [Grok Voice API](/developers/model-capabilities/audio/voice)

## Additional Information Regarding Models

* **No access to realtime events without search tools enabled**
  * Grok has no knowledge of current events or data beyond what was present in its training data.
  * To incorporate realtime data with your request, enable server-side search tools (Web Search / X Search). See [Web Search](/developers/tools/web-search) and [X Search](/developers/tools/x-search).
* **Chat models**
  * No role order limitation: You can mix `system`, `user`, or `assistant` roles in any sequence for your conversation context.
  * `logprobs` and `top_logprobs` are not supported by models `grok-4.20` and newer. These fields will be silently ignored if set.
* **Image input models**
  * Maximum image size: `20MiB`
  * Maximum number of images: No limit
  * Supported image file types: `jpg/jpeg` or `png`.
  * Any image/text input order is accepted (e.g. text prompt can precede image prompt)

> [!NOTE]
>
> The knowledge cut-off date of Grok 3 and Grok 4 is November, 2024.

## Model Aliases

Some models have aliases to help users automatically migrate to the next version of the same model. In general:

* `<modelname>` is aliased to the latest stable version.
* `<modelname>-latest` is aliased to the latest version. This is suitable for users who want to access the latest features.
* `<modelname>-<date>` refers directly to a specific model release. This will not be updated and is for workflows that demand consistency.

For most users, the aliased `<modelname>` or `<modelname>-latest` are recommended, as you would receive the latest features automatically.
