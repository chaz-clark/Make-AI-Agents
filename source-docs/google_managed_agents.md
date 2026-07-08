The [Interactions API](</gemini-api/docs/interactions-overview>) is now generally available. We recommend using this API for access to all the latest features and models. 

  * [ Home ](<https://ai.google.dev/>)
  * [ Gemini API ](<https://ai.google.dev/gemini-api>)
  * [ Docs ](<https://ai.google.dev/gemini-api/docs>)

#  Building Managed Agents

Managed agents on the Gemini API let you extend the Antigravity agent with your own instructions, skills, and data. You can customize the agent inline at interaction time, or save the configuration as a managed agent you invoke by ID.

## Customize the Antigravity agent

The fastest way to build a custom agent is to pass your configuration inline while creating a new interaction with no registration step required. You can extend the agent in three ways:

  * **System instructions** : Pass inline text via `system_instruction` to shape behavior.
  * **Tools** : Override default tools \(Code Execution, Search, URL Context\), register remote MCP servers, or define custom functions \(Function Calling\).
  * **Files and skills** : Mount files like `AGENTS.md` and `SKILL.md` into the environment.

Here is an example of passing all three inline:

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        input="Analyze the Q1 revenue data and create a slide deck.",
        system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",        
        environment={
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report.",
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
                },
            ],
        },
    )
    
    print(interaction.output_text)
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
        agent: "antigravity-preview-05-2026",
        input: "Analyze the Q1 revenue data and create a slide deck.",
        system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",        
        environment: {
            type: "remote",
            sources: [
                {
                    type: "inline",
                    target: ".agents/AGENTS.md",
                    content: "Always use matplotlib for charts. Include a summary table in every report.",
                },
                {
                    type: "inline",
                    target: ".agents/skills/slide-maker/SKILL.md",
                    content: "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
                },
            ],
        },
    }, { timeout: 300000 });
    
    console.log(interaction.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "antigravity-preview-05-2026",
        "input": "Analyze the Q1 revenue data and create a slide deck.",
        "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
        "environment": {
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report."
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."
                }
            ]
        }
    }'
    

Everything is defined at interaction time. No need to register anything first. The Antigravity agent harness provides the runtime \(code execution, file management, web access\) and your configuration layers on top.

### Tools and system instructions

You can customize the agent's behavior and capabilities for a specific interaction using the `system_instruction` and `tools` parameters.

  * **System instructions** : Use the `system_instruction` parameter to pass inline text that shapes the agent's behavior. This is ideal for quick tweaks you want to change per call. The `system_instruction` and `AGENTS.md` are additive; both apply when present.
  * **Tools** : By default, the Antigravity agent has access to `code_execution`, `google_search`, and `url_context`. You can override this list by passing the `tools` parameter at interaction time. You can also register [remote MCP servers](</gemini-api/docs/antigravity-agent#mcp-servers>) or define [custom functions \(function calling\)](</gemini-api/docs/antigravity-agent#function-calling>) to connect the agent to your own APIs and databases. For full details on available tools, see [Antigravity Agent: Supported tools](</gemini-api/docs/antigravity-agent#supported-tools>).

### File-based customization

#### Agent directory structure

While you can pass configuration inline, we recommend organizing your agent's files in a structured directory. This makes it easier to manage, version control, and mount into the agent's environment.

**Note:** You can use the experimental open-source [Gemini API CLI](<https://github.com/google-gemini/Gemini-API-CLI>) to automatically scaffold, test, and deploy this directory structure directly from your terminal.

A typical agent project directory looks like this:
    
    
    my-agent/
    ├── AGENTS.md        # Instructions on how the agent should operate
    ├── skills/          # Custom skills (subfolders and SKILL.md files)
    │   └── slide-maker/
    │       └── SKILL.md
    └── workspace/       # Initial data files and knowledge
    

The Antigravity runtime scans `.agents/` \(and the root of the environment\) for these files.

#### AGENTS.md

The agent automatically loads `.agents/AGENTS.md` \(or `/.agents/AGENTS.md`\) from the environment as system instructions on startup. Use `AGENTS.md` for long-form persona definitions, detailed guidelines, and instructions you want to version control alongside your code.

Mount an `AGENTS.md` using an inline source:

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        input="Analyze the Q1 revenue data and create a report.",
        system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",
        environment={
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report.",
                },
            ],
        },
    )
    
    print(interaction.output_text)
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
        agent: "antigravity-preview-05-2026",
        input: "Analyze the Q1 revenue data and create a report.",
        system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",
        environment: {
            type: "remote",
            sources: [
                {
                    type: "inline",
                    target: ".agents/AGENTS.md",
                    content: "Always use matplotlib for charts. Include a summary table in every report.",
                },
            ],
        },
    }, { timeout: 300000 });
    
    console.log(interaction.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "antigravity-preview-05-2026",
          "input": "Analyze the Q1 revenue data and create a report.",
          "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
          "environment": {
              "type": "remote",
              "sources": [
                  {
                      "type": "inline",
                      "target": ".agents/AGENTS.md",
                      "content": "Always use matplotlib for charts. Include a summary table in every report."
                  }
              ]
          }
      }'
    

#### Skills: SKILL.md

Skills are files that extend the agent's capabilities. Place them under `.agents/skills/<skill-name>/SKILL.md` and the harness auto-discovers and registers them.
    
    
    .agents/
    ├── AGENTS.md
    └── skills/
        └── slide-maker/
            └── SKILL.md
    

Mount a skill using an inline source:

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        input="Create a presentation about our Q1 results.",
        system_instruction="You create presentations from data.",
        environment={
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html",
                },
            ],
        },
    )
    
    print(interaction.output_text)
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
        agent: "antigravity-preview-05-2026",
        input: "Create a presentation about our Q1 results.",
        system_instruction: "You create presentations from data.",
        environment: {
            type: "remote",
            sources: [
                {
                    type: "inline",
                    target: ".agents/skills/slide-maker/SKILL.md",
                    content: "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html",
                },
            ],
        },
    }, { timeout: 300000 });
    
    console.log(interaction.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "antigravity-preview-05-2026",
          "input": "Create a presentation about our Q1 results.",
          "system_instruction": "You create presentations from data.",
          "environment": {
              "type": "remote",
              "sources": [
                  {
                      "type": "inline",
                      "target": ".agents/skills/slide-maker/SKILL.md",
                      "content": "---\nname: slide-maker\ndescription: Create HTML slide decks\n---\n# Slide Maker\n\nWhen asked to create a presentation:\n1. Analyze the input data\n2. Create an HTML slide deck with reveal.js\n3. Save to /workspace/output/slides.html"
                  }
              ]
          }
      }'
    

Skills loaded from `.agents/skills/` and `/.agents/skills/` are both discovered automatically.

## Create a managed agent

Once you've iterated on your configuration, you can create it as a managed agent with `agents.create`. This lets you invoke the agent by ID without repeating the configuration each time.

### From sources

Specify `base_agent`, `id`, `system_instruction` and `base_environment` with sources. The platform provisions a fresh sandbox with your files on every invocation. See [Environments](</gemini-api/docs/agent-environment>) for available source types \(Git, GCS, inline\).

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    agent = client.agents.create(
        id="data-analyst",
        base_agent="antigravity-preview-05-2026",
        system_instruction="You are a data analyst. Always include visualizations and export results as PDF.",
        base_environment={
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report.",
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
                },
                {
                    "type": "repository",
                    "source": "https://github.com/my-org/analysis-templates",
                    "target": "/workspace/templates",
                },
            ],
        },
    )
    
    print(f"Created agent: {agent.id}")
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const agent = await client.agents.create({
        id: "data-analyst",
        base_agent: "antigravity-preview-05-2026",
        system_instruction: "You are a data analyst. Always include visualizations and export results as PDF.",
        base_environment: {
            type: "remote",
            sources: [
                {
                    type: "inline",
                    target: ".agents/AGENTS.md",
                    content: "Always use matplotlib for charts. Include a summary table in every report.",
                },
                {
                    type: "inline",
                    target: ".agents/skills/slide-maker/SKILL.md",
                    content: "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results.",
                },
                {
                    type: "repository",
                    source: "https://github.com/my-org/analysis-templates",
                    target: "/workspace/templates",
                },
            ],
        },
    });
    
    console.log(`Created agent: ${agent.id}`);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "id": "data-analyst",
        "base_agent": "antigravity-preview-05-2026",
        "system_instruction": "You are a data analyst. Always include visualizations and export results as PDF.",
        "base_environment": {
            "type": "remote",
            "sources": [
                {
                    "type": "inline",
                    "target": ".agents/AGENTS.md",
                    "content": "Always use matplotlib for charts. Include a summary table in every report."
                },
                {
                    "type": "inline",
                    "target": ".agents/skills/slide-maker/SKILL.md",
                    "content": "---\nname: slide-maker\n---\n# Slide Maker\nCreate HTML slide decks from data analysis results."
                },
                {
                    "type": "repository",
                    "source": "https://github.com/my-org/analysis-templates",
                    "target": "/workspace/templates"
                }
            ]
        }
    }'
    

### From an existing environment \(fork\)

Iterate with the base Antigravity agent until the environment is right \(packages installed, files in place\), then fork it into a managed agent.

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    # Step 1: set up the environment interactively
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        input="Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
        environment="remote",
    )
    
    # Step 2: fork that environment into a managed agent
    
    agent = client.agents.create(
        id="my-data-analyst",
        base_agent="antigravity-preview-05-2026",
        system_instruction="You are a data analyst. Use the template at /workspace/template.py for all reports.",
        base_environment=interaction.environment_id,
    )
    
    print(f"Forked agent successfully: {agent.id}")
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
        agent: "antigravity-preview-05-2026",
        input: "Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
        environment: "remote",
    }, { timeout: 300000 });
    
    const agent = await client.agents.create({
        id: "my-data-analyst",
        base_agent: "antigravity-preview-05-2026",
        system_instruction: "You are a data analyst. Use the template at /workspace/template.py for all reports.",
        base_environment: interaction.environment_id,
    });
    
    console.log(`Forked agent successfully: ${agent.id}`);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "antigravity-preview-05-2026",
          "input": "Install pandas, matplotlib, and seaborn. Create an analysis template at /workspace/template.py.",
          "environment": "remote"
      }'
    

### With network rules

You can lock down outbound access or inject credentials when saving a managed agent. For the full allowlist schema, credential patterns, and wildcards, see [Environments: Network configuration](</gemini-api/docs/agent-environment#network-configuration>).

The following example creates an `issue-resolver` agent that can only access GitHub and PyPI, with credentials injected for GitHub:

### Python
    
    
    from google import genai
    
    client = genai.Client()
    
    agent = client.agents.create(
        id="issue-resolver",
        base_agent="antigravity-preview-05-2026",
        system_instruction="You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
        base_environment={
            "type": "remote",
            "sources": [
                {
                    "type": "repository",
                    "source": "https://github.com/my-org/backend",
                    "target": "/workspace/repo",
                }
            ],
            "network": {
                "allowlist": [
                    {
                        "domain": "api.github.com",
                        "transform": {
                            "Authorization": "Basic YOUR_BASE64_TOKEN"
                        },
                    },
                    {"domain": "pypi.org"},
                ]
            },
        },
    )
    
    print(f"Created issue-resolver agent successfully: {agent.id}")
    

### JavaScript
    
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const agent = await client.agents.create({
        id: "issue-resolver",
        base_agent: "antigravity-preview-05-2026",
        system_instruction: "You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
        base_environment: {
            type: "remote",
            sources: [
                {
                    type: "repository",
                    source: "https://github.com/my-org/backend",
                    target: "/workspace/repo",
                }
            ],
            network: {
                allowlist: [
                    {
                        domain: "api.github.com",
                        transform: {
                            "Authorization": "Basic YOUR_BASE64_TOKEN"
                        },
                    },
                    { domain: "pypi.org" },
                ]
            }
        },
    });
    
    console.log(`Created issue-resolver agent successfully: ${agent.id}`);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/agents" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "id": "issue-resolver",
          "base_agent": "antigravity-preview-05-2026",
          "system_instruction": "You resolve GitHub issues. Clone the repo, find the bug, write the fix, run the tests, and open a PR.",
          "base_environment": {
              "type": "remote",
              "sources": [
                  {
                      "type": "repository",
                      "source": "https://github.com/my-org/backend",
                      "target": "/workspace/repo"
                  }
              ],
              "network": {
                  "allowlist": [
                      {
                          "domain": "api.github.com",
                          "transform": {
                              "Authorization": "Basic YOUR_BASE64_TOKEN"
                          }
                      },
                      {"domain": "pypi.org"}
                  ]
              }
          }
      }'
    

## Invoke the agent

Call your managed agent with your agent ID by creating a new interaction. Each invocation forks the base environment, so every run starts clean.

### Python
    
    
    result = client.interactions.create(
        agent="data-analyst",
        input="Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
        environment="remote",
    )
    
    print(result.output_text)
    

### JavaScript
    
    
    const result = await client.interactions.create({
        agent: "data-analyst",
        input: "Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
        environment: "remote",
    }, { timeout: 300000 });
    
    console.log(result.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "data-analyst",
          "input": "Analyze Q1 revenue data from /workspace/templates/sample.csv and create a slide deck.",
          "environment": "remote"
      }'
    

For multi-turn conversations and streaming, see the [Quickstart](</gemini-api/docs/managed-agents-quickstart>). The same `previous_interaction_id` and `environment` patterns apply to managed agents.

Managed agents also support background execution and cancellation. For details and code examples, see [Antigravity Agent: Background execution](</gemini-api/docs/antigravity-agent#background-execution>).

## Overriding configuration at invocation

You can override the agent's default `system_instruction`, `tools`, and `environment` network configuration when creating an interaction. This lets you modify the agent's behavior, capabilities, or credentials for a specific run without changing the stored agent definition.

### Override system instruction and tools

### Python
    
    
    result = client.interactions.create(
        agent="data-analyst",
        input="Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
        system_instruction="You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
        tools=[{"type": "code_execution"}], # Override to only use code execution
        environment="remote",
    )
    print(result.output_text)
    

### JavaScript
    
    
    const result = await client.interactions.create({
        agent: "data-analyst",
        input: "Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
        system_instruction: "You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
        tools: [{ type: "code_execution" }], // Override to only use code execution
        environment: "remote",
    }, { timeout: 300000 });
    
    console.log(result.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "data-analyst",
          "input": "Analyze Q1 revenue data, but do not create a slide deck. Just output a summary table.",
          "system_instruction": "You are a data analyst. Focus ONLY on summary tables. Ignore default instructions about slides.",
          "tools": [{"type": "code_execution"}],
          "environment": "remote"
      }'
    

### Override network configuration \(refresh credentials\)

If your managed agent has network credentials baked into its `base_environment`, you can override them at invocation time to refresh expired tokens or rotate API keys. Pass an `environment` object with a new `network` configuration. The new network rules fully replace the previous ones for that interaction. The base environment's sources \(files, repositories\) are preserved.

### Python
    
    
    # Invoke the agent with a fresh token, overriding the base_environment credentials
    result = client.interactions.create(
        agent="issue-resolver",
        input="Fix issue #42 and open a PR.",
        environment={
            "type": "remote",
            "network": {
                "allowlist": [
                    {
                        "domain": "api.github.com",
                        "transform": {
                            "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                        },
                    },
                    {"domain": "pypi.org"},
                ]
            },
        },
    )
    
    print(result.output_text)
    

### JavaScript
    
    
    // Invoke the agent with a fresh token, overriding the base_environment credentials
    const result = await client.interactions.create({
        agent: "issue-resolver",
        input: "Fix issue #42 and open a PR.",
        environment: {
            type: "remote",
            network: {
                allowlist: [
                    {
                        domain: "api.github.com",
                        transform: {
                            "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                        },
                    },
                    { domain: "pypi.org" },
                ]
            },
        },
    }, { timeout: 300000 });
    
    console.log(result.output_text);
    

### REST
    
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "Content-Type: application/json" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -d '{
          "agent": "issue-resolver",
          "input": "Fix issue #42 and open a PR.",
          "environment": {
              "type": "remote",
              "network": {
                  "allowlist": [
                      {
                          "domain": "api.github.com",
                          "transform": {
                              "Authorization": "Bearer ghp_REFRESHED_TOKEN"
                          }
                      },
                      {"domain": "pypi.org"}
                  ]
              }
          }
      }'
    

## Manage agents

You can list, get, and delete agents.

### List agents

### Python
    
    
    agents = client.agents.list()
    for a in agents.agents:
        print(f"{a.id}: {a.description}")
    

### JavaScript
    
    
    const agents = await client.agents.list();
    if (agents.agents) {
        for (const a of agents.agents) {
            console.log(`${a.id}: ${a.description}`);
        }
    }
    

### REST
    
    
    curl -X GET "https://generativelanguage.googleapis.com/v1beta/agents" \
      -H "x-goog-api-key: $GEMINI_API_KEY"
    

### Get an agent

### Python
    
    
    agent = client.agents.get(id="data-analyst")
    print(agent)
    

### JavaScript
    
    
    const agent = await client.agents.get("data-analyst");
    console.log(agent);
    

### REST
    
    
    curl -X GET "https://generativelanguage.googleapis.com/v1beta/agents/data-analyst" \
      -H "x-goog-api-key: $GEMINI_API_KEY"
    

### Delete an agent

Deleting removes the configuration. Existing environments and interactions created by the agent are not affected.

### Python
    
    
    client.agents.delete(id="data-analyst")
    

### JavaScript
    
    
    await client.agents.delete("data-analyst");
    

### REST
    
    
    curl -X DELETE "https://generativelanguage.googleapis.com/v1beta/agents/data-analyst" \
      -H "x-goog-api-key: $GEMINI_API_KEY"
    

## Agent definition reference

Field | Type | Required | Description  
---|---|---|---  
`id` | string | Yes | Unique agent identifier. Used to invoke the agent.  
`description` | string | No | Human-readable description of the agent.  
`base_agent` | string | Yes | Base agent ID \(e.g., `antigravity-preview-05-2026`\).  
`system_instruction` | string | No | System prompt defining behavior and persona.  
`tools` | array | No | Tools the agent can use. If omitted, defaults to `code_execution`, `google_search`, and `url_context`. Supported tools include `code_execution`, `google_search`, `url_context`, `mcp_server`, and custom `function` definitions.  
`base_environment` | string or object | No | `"remote"`, an `environment_id`, or a config object with `sources` and `network`. See Environments.  
  
## Iteration workflow

  1. **Prototype** with the base Antigravity agent. Pass system instruction and environment sources inline. Test instructions, skills, and environment setup interactively.
  2. **Stabilize** the environment. Install packages, mount sources, verify everything works.
  3. **Persist** as a managed agent by creating a new agent, either from sources or by forking the environment.
  4. **Update** the agent definition. Change system instruction, swap skills, or add sources. The next invocation picks up the new configuration.

## Limitations

  * **Preview status** : Managed agents are in preview. Features and schemas may change.
  * **Base agent** : Only `antigravity-preview-05-2026` is supported as `base_agent`.
  * **No versioning** : Agent versioning and rollback are not yet available.
  * **No subagent nesting** : Subagent delegation is not yet supported.
  * You can have up to 1000 managed agents.

## What's next

  * [Agents Overview](</gemini-api/docs/agents>): Learn about the core concepts of managed agents.
  * [Quickstart](</gemini-api/docs/managed-agents-quickstart>): Start building with multi-turn conversations and streaming.
  * [Antigravity Agent](</gemini-api/docs/antigravity-agent>): Explore capabilities, tools, and pricing for the default agent.
  * [Agent Environments](</gemini-api/docs/agent-environment>): Configure sandboxes, sources, and networking.
  * [Managed Agents API on Agent Platform](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents>): For creating agents with built-in organizational governance.