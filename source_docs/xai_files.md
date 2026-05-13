---
platform: xAI
label: Grok Files API
source_url: https://docs.x.ai/developers/files
last_fetched: 2026-05-13
fetch_status: success
size_bytes: 8352
notes: Added 2026-05-13 via update_agents/fetch_doc.py (Tier 1 raw HTTP). Sibling source to xai_collections.md. Documents the xAI Files API used by attachment_search server-side tool. 48MB/file limit; agentic-models-only; benefits from prompt caching when reused. Identified in 2026-05-12 research as a gap (xai_collections was prioritized for the knowledge skill grounding). Now cached for completeness of the xAI surface.
---

#### Files & Collections

# Files

[View as Markdown](</developers/files.md>)

Grok can search through and reason over documents you attach to chat messages. You can reference any public file by URL or [upload](</developers/files/managing-files>) private files and reference them by ID; either way, the system automatically activates the `attachment_search` tool and transforms your request into an agentic workflow.

You can view more information at [Files API Reference](</developers/rest-api-reference/files>).

**Looking for Collections?** If you need persistent document storage with semantic search across many documents, see [Collections](</developers/files/collections>). Files are different—they're for attaching documents to chat conversations for immediate context.

* * *

## How Files Work with Chat

Behind the scenes, when you attach files to a chat message, the xAI API implicitly adds the `attachment_search` server-side tool to your request. This means:

  1. **Automatic Agentic Behavior** : Your chat request becomes an agentic request, where Grok autonomously searches through your documents
  2. **Intelligent Document Analysis** : The model can reason over document content, extract relevant information, and synthesize answers
  3. **Multi-Document Support** : You can attach multiple files, and Grok will search across all of them

This seamless integration allows you to simply attach files and ask questions—the complexity of document search and retrieval is handled automatically by the agentic workflow.

* * *

## Understanding Document Search

When you attach files to a chat message, the xAI API automatically activates the `attachment_search` [server-side tool](</developers/tools/overview>). This transforms your request into an [agentic workflow](</developers/tools/overview#how-it-works>) where Grok:

  1. **Analyzes your query** to understand what information you're seeking
  2. **Searches the documents** intelligently, finding relevant sections across all attached files
  3. **Extracts and synthesizes information** from multiple sources if needed
  4. **Provides a comprehensive answer** with the context from your documents

### Agentic Workflow

Just like other agentic tools \(web search, X search, code execution\), document search operates autonomously:

  * **Multiple searches** : The model may search documents multiple times with different queries to find comprehensive information
  * **Reasoning** : The model uses its reasoning capabilities to decide what to search for and how to interpret the results
  * **Streaming visibility** : In streaming mode, you can see when the model is searching your documents via tool call notifications

### Token Usage with Files

File-based chats follow similar token patterns to other agentic requests:

  * **Prompt tokens** : Include the conversation history and internal processing. Document content is processed efficiently
  * **Reasoning tokens** : Used for planning searches and analyzing document content
  * **Completion tokens** : The final answer text
  * **Cached tokens** : Repeated document content benefits from prompt caching for efficiency

The actual document content is processed by the server-side tool and doesn't directly appear in the message history, keeping token usage optimized.

### Pricing

Document search is billed per tool invocation, in addition to standard token costs. Each time the model searches your documents, it counts as one tool invocation. For complete pricing details, see the [Tools Pricing](</developers/pricing#tools-pricing>) table.

* * *

## Getting Started

To use files with Grok, you'll need to:

  1. Get file's **public URL** or learn how to upload, list, retrieve, and delete files via the **[Files API](</developers/files/managing-files>)**.
  2. **[Chat with files](</developers/model-capabilities/files/chat-with-files>)** \- attach files to chat messages and ask questions about your documents

* * *

## Quick Example

Here's a quick example of the complete workflow:
    
    
    import os
    from xai_sdk import Client
    from xai_sdk.chat import user, file
    
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    
    # 1a. Reference a public file by URL
    file_url = "https://example-files.online-convert.com/document/txt/example.txt"
    
    # 1b. Or upload a file and reference by ID
    uploaded_file = client.files.upload(
        b"Employee: Alice Johnson\nDepartment: Engineering",
        filename="employee.txt",
    )
    
    # 2. Chat with files
    chat = client.chat.create(model="grok-4.3")
    chat.append(user(
        "Summarize both documents",
        file(url=file_url),
        file(uploaded_file.id),
    ))
    
    # 3. Get the answer
    response = chat.sample()
    print(response.content)
    
    # 4. Clean up uploaded file
    client.files.delete(uploaded_file.id)
    
    
    
    // 1a. Reference a public file by URL
    const fileUrl = "https://docs.x.ai/assets/api-examples/documents/sales-report.txt";
    
    // 1b. Or upload a file and reference by ID
    const formData = new FormData();
    formData.append("file", new Blob(["Employee: Alice Johnson\nDepartment: Engineering"], { type: "text/plain" }), "employee.txt");
    formData.append("purpose", "assistants");
    
    const uploadRes = await fetch("https://api.x.ai/v1/files", {
      method: "POST",
      headers: { Authorization: `Bearer ${process.env.XAI_API_KEY}` },
      body: formData,
    });
    const uploadedFile = await uploadRes.json();
    
    // 2. Chat with files
    const chatRes = await fetch("https://api.x.ai/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.XAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "grok-4.3",
        input: [
          {
            role: "user",
            content: [
              { type: "input_text", text: "Summarize both documents" },
              { type: "input_file", file_url: fileUrl },
              { type: "input_file", file_id: uploadedFile.id },
            ],
          },
        ],
      }),
    });
    
    // 3. Get the answer
    const chatData = await chatRes.json();
    const lastMessage = chatData.output[chatData.output.length - 1];
    const answer = lastMessage?.content?.find((c) => c.type === "output_text")?.text;
    console.log(answer);
    
    // 4. Clean up
    await fetch(`https://api.x.ai/v1/files/${uploadedFile.id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${process.env.XAI_API_KEY}` },
    });

* * *

## Key Features

### Multiple File Support

Attach [multiple documents](</developers/model-capabilities/files/chat-with-files#multiple-file-attachments>) to a single query and Grok will search across all of them to find relevant information.

### Multi-Turn Conversations

File context persists across [conversation turns](</developers/model-capabilities/files/chat-with-files#multi-turn-conversations-with-files>), allowing you to ask follow-up questions without re-attaching files.

### Code Execution Integration

Combine files with the [code execution tool](</developers/model-capabilities/files/chat-with-files#combining-files-with-code-execution>) to perform advanced data analysis, statistical computations, and transformations on your uploaded data. The model can write and execute Python code that processes your files directly.

## Limitations

  * **File size** : Maximum 48 MB per file
  * **No batch requests** : File attachments with document search are agentic requests and do not support batch mode \(`n > 1`\)
  * **Agentic models only** : Requires models that support agentic tool calling \(e.g., `grok-4.20`, `grok-4.3`\)
  * **Supported file formats** :
    * Plain text files \(.txt\)
    * Markdown files \(.md\)
    * Code files \(.py, .js, .java, etc.\)
    * CSV files \(.csv\)
    * JSON files \(.json\)
    * PDF documents \(.pdf\)
    * And many other text-based formats

* * *

## Next Steps

### [Managing Files →Learn how to upload, list, retrieve, and delete files using the Files API](</developers/files/managing-files>)### [Chat with Files →Explore how to attach files to chat messages and query your documents](</developers/model-capabilities/files/chat-with-files>)

* * *

Last updated: May 11, 2026
