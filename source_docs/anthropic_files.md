---
platform: Anthropic
label: Files API
source_url: https://platform.claude.com/docs/en/build-with-claude/files
last_fetched: 2026-05-12
fetch_status: success
fetch_error: none
notes: Beta feature (anthropic-beta: files-api-2025-04-14). Create-once, use-many model. Upload/list/retrieve-metadata/delete/download endpoints. file_id referenced in document/image/container_upload content blocks. 500MB per file, 500GB per org. File types — PDF (application/pdf → document), plain text (text/plain → document), images (jpeg/png/gif/webp → image), datasets (code execution → container_upload). Files persist until deleted. Only files created by skills or code execution tool are downloadable; uploaded files are not. Free for upload/download/list/metadata/delete. Workspace-scoped. Available on Claude API, Claude Platform on AWS, Microsoft Foundry; NOT on Amazon Bedrock or Vertex AI. Fetched via WebFetch on 2026-05-12.
---
# Files API

---

The Files API lets you upload and manage files to use with the Claude API without re-uploading content with each request. This is particularly useful when using the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool) to provide inputs (e.g. datasets and documents) and then download outputs (e.g. charts). You can also use the Files API to prevent having to continually re-upload frequently used documents and images across multiple API calls. You can [explore the API reference directly](/docs/en/api/files-create), in addition to this guide.

<Note>
The Files API is in beta. Reach out through the [feedback form](https://forms.gle/tisHyierGwgN4DUE9) to share your experience with the Files API.
</Note>

<Note>
This feature is **not** eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). Data is retained according to the feature's standard retention policy.
</Note>

## Supported models

Referencing a `file_id` in a Messages request is supported in all models that support the given file type. For example, [images](/docs/en/build-with-claude/vision) are supported in all Claude 3+ models, [PDFs](/docs/en/build-with-claude/pdf-support) in all Claude 3.5+ models, and [various other file types](/docs/en/agents-and-tools/tool-use/code-execution-tool#supported-file-types) for the code execution tool in Claude Haiku 4.5 plus all Claude 3.7+ models.

The Files API is available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). It is not currently available on Amazon Bedrock or Vertex AI.

## How the Files API works

The Files API provides a simple create-once, use-many-times approach for working with files:

- **Upload files** to Anthropic's secure storage and receive a unique `file_id`
- **Download files** that are created from skills or the code execution tool
- **Reference files** in [Messages](/docs/en/api/messages/create) requests using the `file_id` instead of re-uploading content
- **Manage your files** with list, retrieve, and delete operations

## How to use the Files API

<Note>
To use the Files API, you'll need to include the beta feature header: `anthropic-beta: files-api-2025-04-14`.
</Note>

### Uploading a file

Upload a file to be referenced in future API calls:

```bash cURL
curl -X POST https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -F "file=@/path/to/document.pdf"
```

```python Python
uploaded = client.beta.files.upload(
    file=("document.pdf", open("/path/to/document.pdf", "rb"), "application/pdf"),
)
```

```typescript TypeScript
const uploaded = await anthropic.beta.files.upload({
  file: await toFile(
    fs.createReadStream("/path/to/document.pdf"),
    undefined,
    { type: "application/pdf" },
  ),
});
```

The response from uploading a file will include:

```json Output
{
  "id": "file_011CNha8iCJcU1wXNR6q4V8w",
  "type": "file",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1024000,
  "created_at": "2025-01-01T00:00:00Z",
  "downloadable": false
}
```

### Using a file in messages

Once uploaded, reference the file using its `file_id`:

```bash cURL
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  -H "content-type: application/json" \
  -d @- <<EOF
{
  "model": "claude-opus-4-6",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Please summarize this document for me."
        },
        {
          "type": "document",
          "source": {
            "type": "file",
            "file_id": "$FILE_ID"
          }
        }
      ]
    }
  ]
}
EOF
```

```python Python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please summarize this document for me."},
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file_id,
                    },
                },
            ],
        }
    ],
    betas=["files-api-2025-04-14"],
)
print(response)
```

### File types and content blocks

The Files API supports different file types that correspond to different content block types:

| File Type | MIME Type | Content Block Type | Use Case |
| :--- | :--- | :--- | :--- |
| PDF | `application/pdf` | `document` | Text analysis, document processing |
| Plain text | `text/plain` | `document` | Text analysis, processing |
| Images | `image/jpeg`, `image/png`, `image/gif`, `image/webp` | `image` | Image analysis, visual tasks |
| [Datasets, others](/docs/en/agents-and-tools/tool-use/code-execution-tool#supported-file-types) | Varies | `container_upload` | Analyze data, create visualizations  |

### Working with other file formats

For file types that are not supported as `document` blocks (.csv, .txt, .md, .docx, .xlsx), convert the files to plain text, and include the content directly in your message.

```python Python
import pandas as pd
import anthropic

client = anthropic.Anthropic()

# Example: Reading a CSV file
df = pd.read_csv("data.csv")
csv_content = df.to_string()

# Send as plain text in the message
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Here's the CSV data:\n\n{csv_content}\n\nPlease analyze this data.",
                }
            ],
        }
    ],
)

print(response.content[0].text)
```

<Note>
For .docx files containing images, convert them to PDF format first, then use [PDF support](/docs/en/build-with-claude/pdf-support) to take advantage of the built-in image parsing. This allows using citations from the PDF document.
</Note>

#### Document blocks

For PDFs and text files, use the `document` content block:

```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_011CNha8iCJcU1wXNR6q4V8w"
  },
  "title": "Document Title", // Optional
  "context": "Context about the document", // Optional
  "citations": { "enabled": true } // Optional, enables citations
}
```

#### Image blocks

For images, use the `image` content block:

```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_011CPMxVD3fHLUhvTqtsQA5w"
  }
}
```

### Managing files

#### List files

Retrieve a list of your uploaded files:

```bash cURL
curl https://api.anthropic.com/v1/files \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```python Python
import anthropic

client = anthropic.Anthropic()
files = client.beta.files.list()
```

#### Get file metadata

Retrieve information about a specific file:

```bash
curl "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```python
file = client.beta.files.retrieve_metadata(file_id)
```

#### Delete a file

Remove a file from your workspace:

```bash
curl -X DELETE "https://api.anthropic.com/v1/files/$FILE_ID" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

```python
result = client.beta.files.delete(file_id)
```

### Downloading a file

Download files that have been created by skills or the code execution tool:

```bash
curl -X GET "https://api.anthropic.com/v1/files/$FILE_ID/content" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14" \
  --output downloaded_file.txt
```

```python
file_content = client.beta.files.download(file_id)
file_content.write_to_file("downloaded_file.txt")
```

<Note>
You can only download files that were created by [skills](/docs/en/build-with-claude/skills-guide) or the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool). Files that you uploaded cannot be downloaded.
</Note>

---

## File storage and limits

### Storage limits

- **Maximum file size:** 500 MB per file
- **Total storage:** 500 GB per organization

### File lifecycle

- Files are scoped to the workspace of the API key. Other API keys can use files created by any other API key associated with the same workspace
- Files persist until you delete them
- Deleted files cannot be recovered
- Files are inaccessible via the API shortly after deletion, but they may persist in active `Messages` API calls and associated tool uses
- Files that users delete will be deleted in accordance with Anthropic's [data retention policy](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data).

---

## Data retention

Files uploaded via the Files API are retained until explicitly deleted using the `DELETE /v1/files/{file_id}` endpoint. Files are stored for reuse across multiple API requests.

For ZDR eligibility across all features, see [API and data retention](/docs/en/manage-claude/api-and-data-retention).

## Error handling

Common errors when using the Files API include:

- **File not found (404):** The specified `file_id` doesn't exist or you don't have access to it
- **Invalid file type (400):** The file type doesn't match the content block type (e.g., using an image file in a document block)
- **Exceeds context window size (400):** The file is larger than the context window size (e.g. using a 500 MB plaintext file in a `/v1/messages` request)
- **Invalid filename (400):** Filename doesn't meet the length requirements (1-255 characters) or contains forbidden characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`, `\`, `/`, or unicode characters 0-31)
- **File too large (413):** File exceeds the 500 MB limit
- **Storage limit exceeded (403):** Your organization has reached the 500 GB storage limit

```json Output
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "File not found: file_011CNha8iCJcU1wXNR6q4V8w"
  }
}
```

## Usage and billing

File API operations are **free**:
- Uploading files
- Downloading files
- Listing files
- Getting file metadata
- Deleting files

File content used in `Messages` requests are priced as input tokens. You can only download files created by [skills](/docs/en/build-with-claude/skills-guide) or the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool).

### Rate limits

During the beta period:
- File-related API calls are limited to approximately 100 requests per minute
- [Contact us](mailto:sales@anthropic.com) if you need higher limits for your use case
