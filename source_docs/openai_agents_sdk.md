---
platform: OpenAI
label: OpenAI Agents SDK Documentation
source_url: https://openai.github.io/openai-agents-python/
last_fetched: 2026-05-12
fetch_status: success
fetch_error: none
notes: Production framework for agentic AI: agents (LLMs+instructions+tools), handoffs (agent-to-agent), guardrails. Includes built-in agent loop, sandbox agents, sessions, tracing, voice. URL unchanged; manual fetch on 2026-05-12 needed because 2026-04-30 WebFetch returned summarized content.
---
Skip to content 

[ ](. "OpenAI Agents SDK")

OpenAI Agents SDK 

Intro 

  * [ English ](/openai-agents-python/)
  * [ 日本語 ](/openai-agents-python/ja/)
  * [ 한국어 ](/openai-agents-python/ko/)
  * [ 简体中文 ](/openai-agents-python/zh/)



Initializing search 




[ openai-agents-python  ](https://github.com/openai/openai-agents-python "Go to repository")

[ ](. "OpenAI Agents SDK") OpenAI Agents SDK 

[ openai-agents-python  ](https://github.com/openai/openai-agents-python "Go to repository")

  * Intro  [ Intro  ](.) Table of contents 
    * Why use the Agents SDK 
    * Agents SDK or Responses API? 
    * Installation 
    * Hello world example 
    * Start here 
    * Choose your path 
  * [ Quickstart  ](quickstart/)
  * [ Configuration  ](config/)
  * Documentation  Documentation 
    * [ Agents  ](agents/)
    * Sandbox agents  Sandbox agents 
      * [ Quickstart  ](sandbox_agents/)
      * [ Concepts  ](sandbox/guide/)
      * [ Sandbox clients  ](sandbox/clients/)
      * [ Agent memory  ](sandbox/memory/)
    * [ Models  ](models/)
    * [ Tools  ](tools/)
    * [ Guardrails  ](guardrails/)
    * [ Running agents  ](running_agents/)
    * [ Streaming  ](streaming/)
    * [ Agent orchestration  ](multi_agent/)
    * [ Handoffs  ](handoffs/)
    * [ Results  ](results/)
    * [ Human-in-the-loop  ](human_in_the_loop/)
    * Sessions  Sessions 
      * [ Overview  ](sessions/)
      * [ SQLAlchemy session  ](sessions/sqlalchemy_session/)
      * [ Advanced SQLite session  ](sessions/advanced_sqlite_session/)
      * [ Encrypted session  ](sessions/encrypted_session/)
    * [ Context management  ](context/)
    * [ Usage  ](usage/)
    * [ Model context protocol (MCP)  ](mcp/)
    * [ Tracing  ](tracing/)
    * Realtime agents  Realtime agents 
      * [ Quickstart  ](realtime/quickstart/)
      * [ Transport  ](realtime/transport/)
      * [ Guide  ](realtime/guide/)
    * Voice agents  Voice agents 
      * [ Quickstart  ](voice/quickstart/)
      * [ Pipeline  ](voice/pipeline/)
      * [ Tracing  ](voice/tracing/)
    * [ Agent visualization  ](visualization/)
    * [ REPL utility  ](repl/)
    * [ Examples  ](examples/)
    * [ Release process/changelog  ](release/)
  * API Reference  API Reference 
    * Agents  Agents 
      * [ Agents module  ](ref/)
      * [ Agent  ](ref/agent/)
      * [ Runner  ](ref/run/)
      * [ Run config  ](ref/run_config/)
      * [ Run state  ](ref/run_state/)
      * Sandbox  Sandbox 
        * [ Overview  ](ref/sandbox/)
        * [ SandboxAgent  ](ref/sandbox/sandbox_agent/)
        * [ Manifest  ](ref/sandbox/manifest/)
        * [ Permissions  ](ref/sandbox/permissions/)
        * [ SnapshotSpec  ](ref/sandbox/snapshot/)
        * [ Workspace entries  ](ref/sandbox/entries/)
        * Capabilities  Capabilities 
          * [ Capabilities  ](ref/sandbox/capabilities/capabilities/)
          * [ Capability  ](ref/sandbox/capabilities/capability/)
          * [ Filesystem  ](ref/sandbox/capabilities/filesystem/)
          * [ Shell  ](ref/sandbox/capabilities/shell/)
          * [ Memory  ](ref/sandbox/capabilities/memory/)
          * [ Skills  ](ref/sandbox/capabilities/skills/)
          * [ Compaction  ](ref/sandbox/capabilities/compaction/)
        * [ Sandbox clients  ](ref/sandbox/session/sandbox_client/)
        * [ SandboxSession  ](ref/sandbox/session/sandbox_session/)
        * [ SandboxSessionState  ](ref/sandbox/session/sandbox_session_state/)
        * [ Unix local sandbox  ](ref/sandbox/sandboxes/unix_local/)
        * [ Docker sandbox  ](ref/sandbox/sandboxes/docker/)
      * [ Responses WebSocket session  ](ref/responses_websocket_session/)
      * [ Run error handlers  ](ref/run_error_handlers/)
      * [ Memory  ](ref/memory/)
      * [ REPL  ](ref/repl/)
      * [ Tools  ](ref/tool/)
      * [ Tool context  ](ref/tool_context/)
      * [ Results  ](ref/result/)
      * [ Streaming events  ](ref/stream_events/)
      * [ Handoffs  ](ref/handoffs/)
      * [ Lifecycle  ](ref/lifecycle/)
      * [ Items  ](ref/items/)
      * [ Run context  ](ref/run_context/)
      * [ Usage  ](ref/usage/)
      * [ Exceptions  ](ref/exceptions/)
      * [ Guardrails  ](ref/guardrail/)
      * [ Prompts  ](ref/prompts/)
      * [ Model settings  ](ref/model_settings/)
      * [ Strict schema  ](ref/strict_schema/)
      * [ Tool guardrails  ](ref/tool_guardrails/)
      * [ Computer  ](ref/computer/)
      * [ Agent output  ](ref/agent_output/)
      * [ Function schema  ](ref/function_schema/)
      * [ Model interface  ](ref/models/interface/)
      * [ OpenAI Chat Completions model  ](ref/models/openai_chatcompletions/)
      * [ OpenAI Responses model  ](ref/models/openai_responses/)
      * [ OpenAI provider  ](ref/models/openai_provider/)
      * [ Multi provider  ](ref/models/multi_provider/)
      * [ MCP servers  ](ref/mcp/server/)
      * [ MCP util  ](ref/mcp/util/)
      * [ MCP manager  ](ref/mcp/manager/)
    * Tracing  Tracing 
      * [ Tracing module  ](ref/tracing/)
      * [ Creating traces/spans  ](ref/tracing/create/)
      * [ Traces  ](ref/tracing/traces/)
      * [ Spans  ](ref/tracing/spans/)
      * [ Processor interface  ](ref/tracing/processor_interface/)
      * [ Processors  ](ref/tracing/processors/)
      * [ Scope  ](ref/tracing/scope/)
      * [ Setup  ](ref/tracing/setup/)
      * [ Span data  ](ref/tracing/span_data/)
      * [ Util  ](ref/tracing/util/)
    * Realtime  Realtime 
      * [ RealtimeAgent  ](ref/realtime/agent/)
      * [ RealtimeRunner  ](ref/realtime/runner/)
      * [ RealtimeSession  ](ref/realtime/session/)
      * [ Events  ](ref/realtime/events/)
      * [ Configuration  ](ref/realtime/config/)
      * [ Model  ](ref/realtime/model/)
    * Voice  Voice 
      * [ Pipeline  ](ref/voice/pipeline/)
      * [ Workflow  ](ref/voice/workflow/)
      * [ Input  ](ref/voice/input/)
      * [ Result  ](ref/voice/result/)
      * [ Pipeline config  ](ref/voice/pipeline_config/)
      * [ Events  ](ref/voice/events/)
      * [ Exceptions  ](ref/voice/exceptions/)
      * [ Model  ](ref/voice/model/)
      * [ Utils  ](ref/voice/utils/)
      * [ OpenAI voice model provider  ](ref/voice/models/openai_provider/)
      * [ OpenAI STT  ](ref/voice/models/openai_stt/)
      * [ OpenAI TTS  ](ref/voice/models/openai_tts/)
    * Extensions  Extensions 
      * [ Handoff filters  ](ref/extensions/handoff_filters/)
      * [ Handoff prompt  ](ref/extensions/handoff_prompt/)
      * Third-party adapters  Third-party adapters 
        * [ Any-LLM model  ](ref/extensions/models/any_llm_model/)
        * [ Any-LLM provider  ](ref/extensions/models/any_llm_provider/)
        * [ LiteLLM model  ](ref/extensions/models/litellm_model/)
        * [ LiteLLM provider  ](ref/extensions/models/litellm_provider/)
      * [ Tool output trimmer  ](ref/extensions/tool_output_trimmer/)
      * [ SQLAlchemySession  ](ref/extensions/memory/sqlalchemy_session/)
      * [ Async SQLite session  ](ref/extensions/memory/async_sqlite_session/)
      * [ RedisSession  ](ref/extensions/memory/redis_session/)
      * [ MongoDBSession  ](ref/extensions/memory/mongodb_session/)
      * [ DaprSession  ](ref/extensions/memory/dapr_session/)
      * [ EncryptedSession  ](ref/extensions/memory/encrypt_session/)
      * [ AdvancedSQLiteSession  ](ref/extensions/memory/advanced_sqlite_session/)



Table of contents 

  * Why use the Agents SDK 
  * Agents SDK or Responses API? 
  * Installation 
  * Hello world example 
  * Start here 
  * Choose your path 



# OpenAI Agents SDK

The [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of our previous experimentation for agents, [Swarm](https://github.com/openai/swarm/tree/main). The Agents SDK has a very small set of primitives:

  * **Agents** , which are LLMs equipped with instructions and tools
  * **Agents as tools / Handoffs** , which allow agents to delegate to other agents for specific tasks
  * **Guardrails** , which enable validation of agent inputs and outputs



In combination with Python, these primitives are powerful enough to express complex relationships between tools and agents, and allow you to build real-world applications without a steep learning curve. In addition, the SDK comes with built-in **tracing** that lets you visualize and debug your agentic flows, as well as evaluate them and even fine-tune models for your application.

## Why use the Agents SDK

The SDK has two driving design principles:

  1. Enough features to be worth using, but few enough primitives to make it quick to learn.
  2. Works great out of the box, but you can customize exactly what happens.



Here are the main features of the SDK:

  * **Agent loop** : A built-in agent loop that handles tool invocation, sends results back to the LLM, and continues until the task is complete.
  * **Python-first** : Use built-in language features to orchestrate and chain agents, rather than needing to learn new abstractions.
  * **Agents as tools / Handoffs** : A powerful mechanism for coordinating and delegating work across multiple agents.
  * **Sandbox agents** : Run specialists inside real isolated workspaces with manifest-defined files, sandbox client choice, and resumable sandbox sessions.
  * **Guardrails** : Run input validation and safety checks in parallel with agent execution, and fail fast when checks do not pass.
  * **Function tools** : Turn any Python function into a tool with automatic schema generation and Pydantic-powered validation.
  * **MCP server tool calling** : Built-in MCP server tool integration that works the same way as function tools.
  * **Sessions** : A persistent memory layer for maintaining working context within an agent loop.
  * **Human in the loop** : Built-in mechanisms for involving humans across agent runs.
  * **Tracing** : Built-in tracing for visualizing, debugging, and monitoring workflows, with support for the OpenAI suite of evaluation, fine-tuning, and distillation tools.
  * **Realtime Agents** : Build powerful voice agents with `gpt-realtime-2`, automatic interruption detection, context management, guardrails, and more.



## Agents SDK or Responses API?

The SDK uses the Responses API by default for OpenAI models, but it adds a higher-level runtime around model calls.

Use the Responses API directly when:

  * you want to own the loop, tool dispatch, and state handling yourself
  * your workflow is short-lived and mainly about returning the model's response



Use the Agents SDK when:

  * you want the runtime to manage turns, tool execution, guardrails, handoffs, or sessions
  * your agent should produce artifacts or operate across multiple coordinated steps
  * you need a real workspace or resumable execution through [Sandbox agents](sandbox_agents/)



You do not need to choose one globally. Many applications use the SDK for managed workflows and call the Responses API directly for lower-level paths.

## Installation
    
    
    pip install openai-agents
    

## Hello world example
    
    
    from agents import Agent, Runner
    
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")
    
    result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
    

(_If running this, ensure you set the`OPENAI_API_KEY` environment variable_)
    
    
    export OPENAI_API_KEY=sk-...
    

## Start here

  * Build your first text-based agent with the [Quickstart](quickstart/).
  * Then decide how you want to carry state across turns in [Running agents](running_agents/#choose-a-memory-strategy).
  * If the task depends on real files, repos, or isolated per-agent workspace state, read the [Sandbox agents quickstart](sandbox_agents/).
  * If you are deciding between handoffs and manager-style orchestration, read [Agent orchestration](multi_agent/).



## Choose your path

Use this table when you know the job you want to do, but not which page explains it.

Goal | Start here  
---|---  
Build the first text agent and see one complete run | [Quickstart](quickstart/)  
Add function tools, hosted tools, or agents as tools | [Tools](tools/)  
Run a coding, review, or document agent inside a real isolated workspace | [Sandbox agents quickstart](sandbox_agents/) and [Sandbox clients](sandbox/clients/)  
Decide between handoffs and manager-style orchestration | [Agent orchestration](multi_agent/)  
Keep memory across turns | [Running agents](running_agents/#choose-a-memory-strategy) and [Sessions](sessions/)  
Use OpenAI models, websocket transport, or non-OpenAI providers | [Models](models/)  
Review outputs, run items, interruptions, and resume state | [Results](results/)  
Build a low-latency voice agent with `gpt-realtime-2` | [Realtime agents quickstart](realtime/quickstart/) and [Realtime transport](realtime/transport/)  
Build a speech-to-text / agent / text-to-speech pipeline | [Voice pipeline quickstart](voice/quickstart/)
