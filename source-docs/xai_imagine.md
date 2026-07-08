#### Model Capabilities

# Imagine Overview

[View as Markdown](</developers/model-capabilities/imagine.md>)

[Create API key](<https://console.x.ai/team/default/api-keys>)

The Imagine API lets you generate and edit images and videos with Grok Imagine models. Use it for image generation, image editing with up to 3 reference images, video generation from text or still images, video editing, and more.

### Image Editing

grok-imagine-image-quality

Edit images with natural language. Supports up to 3 reference images per request.

Pricing$0.05 / image

Resolution1K & 2K

[Read docs](</developers/model-capabilities/images/editing>)[Try in playground](<https://console.x.ai/team/default/image?mode=edit>)

### Image-to-Video

grok-imagine-video-1.5

Animate a still image with a text prompt. The source image becomes the first frame.

Pricing$0.08 / sec

Resolution480p, 720p & 1080p

[Read docs](</developers/model-capabilities/video/image-to-video>)[Try in playground](<https://console.x.ai/team/default/video?mode=first-frame>)

### Image Generation

grok-imagine-image-quality

Generate images from text prompts with configurable aspect ratio, resolution, and count.

Pricing$0.05 / image

Resolution1K & 2K

[Read docs](</developers/model-capabilities/images/generation>)[Try in playground](<https://console.x.ai/team/default/image?mode=generate>)

## Pricing

Image generation uses flat per-image pricing regardless of prompt length. Each generated image incurs a fixed fee. Image edits are billed for both the input image and the generated output image. Video generation uses per-second pricing where both duration and resolution affect the total cost. For full pricing details, see the [pricing page](</developers/pricing#imagine-api-pricing>).

## Image Generation

Generate new images from text prompts with Grok Imagine models. Configure output count \(up to 10 images per request\), aspect ratio, resolution, and response format.

[View docs](</developers/model-capabilities/images/generation>)
    
    
    import xai_sdk
    
    client = xai_sdk.Client()
    
    response = client.image.sample(
        prompt="A collage of London landmarks in a stenciled street‑art style",
        model="grok-imagine-image-quality",
    )
    
    print(response.url)
    
    
    
    curl -X POST https://api.x.ai/v1/images/generations \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
        "model": "grok-imagine-image-quality",
        "prompt": "A collage of London landmarks in a stenciled street‑art style"
      }'
    
    
    
    from openai import OpenAI
    
    client = OpenAI(
        base_url="https://api.x.ai/v1",
        api_key="YOUR_API_KEY",
    )
    
    response = client.images.generate(
        model="grok-imagine-image-quality",
        prompt="A collage of London landmarks in a stenciled street‑art style",
    )
    
    print(response.data[0].url)
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateImage } from "ai";
    
    const { image } = await generateImage({
        model: xai.image("grok-imagine-image-quality"),
        prompt: "A collage of London landmarks in a stenciled street‑art style",
    });
    
    console.log(image.base64);
    

## Image Editing

Edit a source image with natural language. Provide a public image URL or base64-encoded data URI, then describe the change you want Grok Imagine to apply. Multi-image editing supports up to 3 source images in a single request for combining subjects, transferring styles, and composing scenes.

[View docs](</developers/model-capabilities/images/editing>)
    
    
    import base64
    import xai_sdk
    
    client = xai_sdk.Client()
    
    # Load image from file and encode as base64
    with open("photo.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    response = client.image.sample(
        prompt="Render this as a pencil sketch with detailed shading",
        model="grok-imagine-image-quality",
        image_url=f"data:image/png;base64,{image_data}",
    )
    
    print(response.url)
    
    
    
    # Using a public URL as the source image
    curl -X POST https://api.x.ai/v1/images/edits \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
        "model": "grok-imagine-image-quality",
        "prompt": "Render this as a pencil sketch with detailed shading",
        "image": {
          "url": "https://docs.x.ai/assets/api-examples/images/style-realistic.png",
          "type": "image_url"
        }
      }'
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { generateImage } from "ai";
    import fs from "fs";
    
    // Load image and encode as base64
    const imageBuffer = fs.readFileSync("photo.png");
    const base64Image = imageBuffer.toString("base64");
    
    const { image } = await generateImage({
        model: xai.image("grok-imagine-image-quality"),
        prompt: {
            text: "Render this as a pencil sketch with detailed shading",
            images: [`data:image/png;base64,${base64Image}`],
        },
    });
    
    console.log(image.base64);
    

## Image-to-Video

Animate a still image with a text prompt. The source image becomes the starting point for the generated video. Video requests are asynchronous: start a request, poll with the returned request ID, and use the completed video URL when ready. The xAI SDK and AI SDK handle polling for you.

[View docs](</developers/model-capabilities/video/image-to-video>)
    
    
    import os
    import xai_sdk
    
    client = xai_sdk.Client(api_key=os.getenv("XAI_API_KEY"))
    
    response = client.video.generate(
        prompt="Make the water crash down and slowly pan out the camera",
        model="grok-imagine-video-1.5",
        image_url="https://docs.x.ai/assets/api-examples/video/waterfall-still.png",
        duration=12,
    )
    
    print(response.url)
    
    
    
    import { xai } from "@ai-sdk/xai";
    import { experimental_generateVideo as generateVideo } from "ai";
    
    const result = await generateVideo({
        model: xai.video("grok-imagine-video-1.5"),
        prompt: {
            image: "https://docs.x.ai/assets/api-examples/video/waterfall-still.png",
            text: "Make the water crash down and slowly pan out the camera",
        },
        duration: 12,
    });
    
    const videoUrl = result.providerMetadata?.xai?.videoUrl;
    console.log(videoUrl);
    
    
    
    # Start the video generation request
    REQUEST_ID=$(curl -s -X POST https://api.x.ai/v1/videos/generations \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $XAI_API_KEY" \
      -d '{
        "model": "grok-imagine-video-1.5",
        "prompt": "Make the water crash down and slowly pan out the camera",
        "image": {"url": "https://docs.x.ai/assets/api-examples/video/waterfall-still.png"},
        "duration": 12
      }' | jq -r '.request_id')
    
    # Poll until the video is ready
    while true; do
      RESULT=$(curl -s https://api.x.ai/v1/videos/$REQUEST_ID \
        -H "Authorization: Bearer $XAI_API_KEY")
      STATUS=$(echo "$RESULT" | jq -r '.status')
      if [ "$STATUS" = "done" ]; then
        echo "$RESULT" | jq -r '.video.url'
        break
      elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "expired" ]; then
        echo "Request $STATUS"; echo "$RESULT" | jq .
        break
      fi
      sleep 5
    done
    

## More Capabilities

Beyond the top use cases above, the Imagine API supports several additional workflows:

  * **[Multi-Image Editing](</developers/model-capabilities/images/multi-image-editing>)** — Combine up to 3 source images in a single edit for compositing subjects, transferring styles, and building scenes from multiple references.
  * **[Video Generation](</developers/model-capabilities/video/generation>)** — Generate videos from text prompts with configurable duration \(up to 15s\), aspect ratio, and resolution.
  * **[Video Editing](</developers/model-capabilities/video/editing>)** — Modify an existing video with a text prompt while preserving the rest of the scene.
  * **[Reference-to-Video](</developers/model-capabilities/video/reference-to-video>)** — Guide a generated video with one or more reference images that influence the output without forcing the first frame. Requires `grok-imagine-video` — `grok-imagine-video-1.5` does not support this mode.
  * **[Video Extension](</developers/model-capabilities/video/extension>)** — Continue an existing video from its last frame, combining the original and extension into one clip.
  * **[Files API Integration](</developers/model-capabilities/imagine/files>)** — Reference stored files as Imagine inputs by ID, persist generated assets to the Files API, and optionally create a permanent shareable public URL — all in a single request.

* * *

## Enterprise Compliance & Security

The Imagine APIs are built for production workloads with strict security and compliance requirements. Generated media is subject to content policy review and is not used for training.

SOC 2 Type II

Audited controls for security, availability, and confidentiality

HIPAA Eligible

BAA available for healthcare applications handling PHI

GDPR Compliant

Data processing agreements and EU data residency options

Data Residency

Regional processing for compliance requirements

High Availability

Multi-region infrastructure with custom SLAs for enterprise workloads

SSO & RBAC

SAML SSO, role-based access, and audit logging

* * *

Last updated: May 22, 2026