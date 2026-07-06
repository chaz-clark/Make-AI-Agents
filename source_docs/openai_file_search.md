File search is a tool available in the [Responses API](</api/docs/api-reference/responses>). It enables models to retrieve information in a knowledge base of previously uploaded files through semantic and keyword search. By creating vector stores and uploading files to them, you can augment the models’ inherent knowledge by giving them access to these knowledge bases or `vector_stores`.

To learn more about how vector stores and semantic search work, refer to our [retrieval guide](</api/docs/guides/retrieval>).

This is a hosted tool managed by OpenAI, meaning you don’t have to implement code on your end to handle its execution. When the model decides to use it, it will automatically call the tool, retrieve information from your files, and return an output.

## How to use

Prior to using file search with the Responses API, you need to have set up a knowledge base in a vector store and uploaded files to it.

Create a vector store and upload a file

Follow these steps to create a vector store and upload a file to it. You can use [this example file](<https://cdn.openai.com/API/docs/deep_research_blog.pdf>) or upload your own.

#### Upload the file to the File API

Upload a file

python
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    import requests
    from io import BytesIO
    from openai import OpenAI
    
    client = OpenAI()
    
    def create_file(client, file_path):
        if file_path.startswith("http://") or file_path.startswith("https://"):
            # Download the file content from the URL
            response = requests.get(file_path)
            file_content = BytesIO(response.content)
            file_name = file_path.split("/")[-1]
            file_tuple = (file_name, file_content)
            result = client.files.create(
                file=file_tuple,
                purpose="assistants"
            )
        else:
            # Handle local file path
            with open(file_path, "rb") as file_content:
                result = client.files.create(
                    file=file_content,
                    purpose="assistants"
                )
        print(result.id)
        return result.id
    
    # Replace with your own file path or URL
    file_id = create_file(client, "https://cdn.openai.com/API/docs/deep_research_blog.pdf")
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
    32
    33
    34
    import fs from "fs";
    import OpenAI from "openai";
    const openai = new OpenAI();
    
    async function createFile(filePath) {
      let result;
      if (filePath.startsWith("http://") || filePath.startsWith("https://")) {
        // Download the file content from the URL
        const res = await fetch(filePath);
        const buffer = await res.arrayBuffer();
        const urlParts = filePath.split("/");
        const fileName = urlParts[urlParts.length - 1];
        const file = new File([buffer], fileName);
        result = await openai.files.create({
          file: file,
          purpose: "assistants",
        });
      } else {
        // Handle local file path
        const fileContent = fs.createReadStream(filePath);
        result = await openai.files.create({
          file: fileContent,
          purpose: "assistants",
        });
      }
      return result.id;
    }
    
    // Replace with your own file path or URL
    const fileId = await createFile(
      "https://cdn.openai.com/API/docs/deep_research_blog.pdf"
    );
    
    console.log(fileId);

#### Create a vector store

Create a vector store

python
    
    
    1
    2
    3
    4
    vector_store = client.vector_stores.create(
        name="knowledge_base"
    )
    print(vector_store.id)
    
    
    1
    2
    3
    4
    const vectorStore = await openai.vectorStores.create({
        name: "knowledge_base",
    });
    console.log(vectorStore.id);

#### Add the file to the vector store

Add a file to a vector store

python
    
    
    1
    2
    3
    4
    5
    result = client.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=file_id
    )
    print(result)
    
    
    1
    2
    3
    4
    5
    6
    await openai.vectorStores.files.create(
        vectorStore.id,
        {
            file_id: fileId,
        }
    });

#### Check status

Run this code until the file is ready to be used \(i.e., when the status is `completed`\).

Check status

python
    
    
    1
    2
    3
    4
    result = client.vector_stores.files.list(
        vector_store_id=vector_store.id
    )
    print(result)
    
    
    1
    2
    3
    4
    const result = await openai.vectorStores.files.list({
        vector_store_id: vectorStore.id,
    });
    console.log(result);

Once your knowledge base is set up, you can include the `file_search` tool in the list of tools available to the model, along with the list of vector stores in which to search.

File search tool

python
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    from openai import OpenAI
    client = OpenAI()
    
    response = client.responses.create(
        model="gpt-5.5",
        input="What is deep research by OpenAI?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["<vector_store_id>"]
        }]
    )
    print(response)
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    import OpenAI from "openai";
    const openai = new OpenAI();
    
    const response = await openai.responses.create({
        model: "gpt-5.5",
        input: "What is deep research by OpenAI?",
        tools: [
            {
                type: "file_search",
                vector_store_ids: ["<vector_store_id>"],
            },
        ],
    });
    console.log(response);
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    using OpenAI.Responses;
    
    string key = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
    OpenAIResponseClient client = new(model: "gpt-5.5", apiKey: key);
    
    ResponseCreationOptions options = new();
    options.Tools.Add(ResponseTool.CreateFileSearchTool(["<vector_store_id>"]));
    
    OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
        ResponseItem.CreateUserMessageItem([
            ResponseContentPart.CreateInputTextPart("What is deep research by OpenAI?"),
        ]),
    ], options);
    
    Console.WriteLine(response.GetOutputText());

When this tool is called by the model, you will receive a response with multiple outputs:

  1. A `file_search_call` output item, which contains the id of the file search call.
  2. A `message` output item, which contains the response from the model, along with the file citations.

File search response

json
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
    32
    33
    34
    35
    36
    37
    38
    39
    40
    41
    42
    43
    44
    45
    46
    47
    48
    {
      "output": [
        {
          "type": "file_search_call",
          "id": "fs_67c09ccea8c48191ade9367e3ba71515",
          "status": "completed",
          "queries": ["What is deep research?"],
          "search_results": null
        },
        {
          "id": "msg_67c09cd3091c819185af2be5d13d87de",
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "output_text",
              "text": "Deep research is a sophisticated capability that allows for extensive inquiry and synthesis of information across various domains. It is designed to conduct multi-step research tasks, gather data from multiple online sources, and provide comprehensive reports similar to what a research analyst would produce. This functionality is particularly useful in fields requiring detailed and accurate information...",
              "annotations": [
                {
                  "type": "file_citation",
                  "index": 992,
                  "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
                  "filename": "deep_research_blog.pdf"
                },
                {
                  "type": "file_citation",
                  "index": 992,
                  "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
                  "filename": "deep_research_blog.pdf"
                },
                {
                  "type": "file_citation",
                  "index": 1176,
                  "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
                  "filename": "deep_research_blog.pdf"
                },
                {
                  "type": "file_citation",
                  "index": 1176,
                  "file_id": "file-2dtbBZdjtDKS8eqWxqbgDi",
                  "filename": "deep_research_blog.pdf"
                }
              ]
            }
          ]
        }
      ]
    }

## Retrieval customization

### Limiting the number of results

Using the file search tool with the Responses API, you can customize the number of results you want to retrieve from the vector stores. This can help reduce both token usage and latency, but may come at the cost of reduced answer quality.

Limit the number of results

python
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    response = client.responses.create(
        model="gpt-5.5",
        input="What is deep research by OpenAI?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["<vector_store_id>"],
            "max_num_results": 2
        }]
    )
    print(response)
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    const response = await openai.responses.create({
        model: "gpt-5.5",
        input: "What is deep research by OpenAI?",
        tools: [{
            type: "file_search",
            vector_store_ids: ["<vector_store_id>"],
            max_num_results: 2,
        }],
    });
    console.log(response);

### Include search results in the response

While you can see annotations \(references to files\) in the output text, the file search call will not return search results by default.

To include search results in the response, you can use the `include` parameter when creating the response.

Include search results

python
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    response = client.responses.create(
        model="gpt-5.5",
        input="What is deep research by OpenAI?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["<vector_store_id>"]
        }],
        include=["file_search_call.results"]
    )
    print(response)
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    const response = await openai.responses.create({
        model: "gpt-5.5",
        input: "What is deep research by OpenAI?",
        tools: [{
            type: "file_search",
            vector_store_ids: ["<vector_store_id>"],
        }],
        include: ["file_search_call.results"],
    });
    console.log(response);

### Metadata filtering

You can filter the search results based on the metadata of the files. For more details, refer to our [retrieval guide](</api/docs/guides/retrieval>), which covers:

  * How to [set attributes on vector store files](</api/docs/guides/retrieval#attributes>)
  * How to [define filters](</api/docs/guides/retrieval#attribute-filtering>)

Metadata filtering

python
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    response = client.responses.create(
        model="gpt-5.5",
        input="What is deep research by OpenAI?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": ["<vector_store_id>"],
            "filters": {
                "type": "in",
                "key": "category",
                "value": ["blog", "announcement"]
            }
        }]
    )
    print(response)
    
    
    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    const response = await openai.responses.create({
        model: "gpt-5.5",
        input: "What is deep research by OpenAI?",
        tools: [{
            type: "file_search",
            vector_store_ids: ["<vector_store_id>"],
            filters: {
                type: "in",
                key: "category",
                value: ["blog", "announcement"]
            }
        }]
    });
    console.log(response);

## Supported files

_For`text/` MIME types, the encoding must be one of `utf-8`, `utf-16`, or `ascii`._

File format| MIME type  
---|---  
`.c`| `text/x-c`  
`.cpp`| `text/x-c++`  
`.cs`| `text/x-csharp`  
`.css`| `text/css`  
`.doc`| `application/msword`  
`.docx`| `application/vnd.openxmlformats-officedocument.wordprocessingml.document`  
`.go`| `text/x-golang`  
`.html`| `text/html`  
`.java`| `text/x-java`  
`.js`| `text/javascript`  
`.json`| `application/json`  
`.md`| `text/markdown`  
`.pdf`| `application/pdf`  
`.php`| `text/x-php`  
`.pptx`| `application/vnd.openxmlformats-officedocument.presentationml.presentation`  
`.py`| `text/x-python`  
`.py`| `text/x-script.python`  
`.rb`| `text/x-ruby`  
`.sh`| `application/x-sh`  
`.tex`| `text/x-tex`  
`.ts`| `application/typescript`  
`.txt`| `text/plain`  
  
## Usage notes

API Availability| Rate limits| Notes  
---|---|---  
[Responses](</api/docs/api-reference/responses>)[Chat Completions](</api/docs/api-reference/chat>)[Assistants](</api/docs/api-reference/assistants>)| **Tier 1**  
100 RPM**Tier 2 and 3**  
500 RPM**Tier 4 and 5**  
1000 RPM| [Pricing](</api/docs/pricing#built-in-tools>)   
[ZDR and data residency](</api/docs/guides/your-data>)