# Repo Update Plan Based on New Docs — 2026-07-06

## Executive Summary

32 new documentation sources reveal significant platform evolution since May 2026. This plan identifies what in our repo needs updating to stay current with:
- **Managed agent platforms** (Anthropic, Google)
- **New execution models** (sandboxes, managed environments)
- **MCP standardization** across platforms
- **Multimodal capabilities** (voice, image, video)
- **Framework updates** (ADK 2.0, OpenAI Sandbox Agents)

---

## New Capabilities Discovered

### 1. Managed Agents Platforms (High Impact)

**Anthropic Claude Managed Agents** (5 new sources)
- Beta: `managed-agents-2026-04-01`
- Fully managed execution environment (bash, files, web, code)
- `agent_toolset_20260401` pre-built tools
- Multi-agent sessions with shared sandbox
- **Advisor Tool**: executor + advisor model pattern

**Google Antigravity Agent** (new)
- General-purpose managed agent
- Secure Linux sandbox hosted by Google
- Powered by Gemini 3.5 Flash
- Single API call for full agent lifecycle

**Google Deep Research Agent** (new)
- Collaborative planning + visualization
- MCP integration
- Two variants: speed vs comprehensiveness

**Impact on our repo**:
- ❌ We don't have templates for managed agents
- ❌ `make-agent.md` assumes self-hosted/API-only execution
- ❌ No guidance on when to use managed vs self-hosted

### 2. Execution Models & Sandboxes (High Impact)

**OpenAI Sandbox Agents** (4 new sources)
- Beta: persistent isolated workspaces
- Multiple backends: Unix, Docker, Blaxel, Cloudflare, E2B, Modal, Runloop, Vercel
- Sandbox memory support (lessons from prior runs)
- `SandboxAgent`, `Manifest`, `SandboxRunConfig`

**Google Interactions API** (GA June 2026)
- Server-side conversation state
- Observable execution steps
- Background execution for long-running tasks
- Replaces older conversation patterns

**Impact on our repo**:
- ❌ `make-orchestrator-agent.md` doesn't cover sandbox orchestration
- ❌ No template for stateful execution environments
- ❌ Missing guidance on backend selection

### 3. MCP Standardization (Medium Impact)

**MCP now supported across**:
- OpenAI: Enhanced MCP with resource management, session resumption
- Google: Public MCP server at gemini-api-docs-mcp.dev
- xAI: (planned but URL 404 - not ready yet)

**Hermes Agent**: Auto-distillation (inspired our `knowledge/learned/`)

**Impact on our repo**:
- ✅ We already reference MCP in places
- ⚠️  Should formalize MCP integration patterns
- ⚠️  Hermes auto-distillation worth deeper integration

### 4. Multimodal Capabilities (Low-Medium Impact)

**xAI Voice/Audio** (4 new sources)
- Voice Agent API with custom voice cloning
- Speech-to-Text (GA, 25 languages)
- Text-to-Speech (GA)
- `grok-voice-think-fast-1.0` model

**xAI Imagine** (new)
- Image/video generation
- Reference-to-video, video extension
- Batch API expansion (chat + multimodal)

**Impact on our repo**:
- ❓ Likely out of scope for current templates (text-focused agents)
- ❓ Could add optional multimodal section to `make-agent.md`

### 5. Framework Updates (Medium Impact)

**ADK 2.0** (GA May/June 2026, 7 new sources)
- Graph-based workflows (vs linear)
- Dynamic workflows (loops, branching)
- Collaborative workflows (coordinator + subagents)
- BigQuery analytics, context management, sessions

**OpenAI Models** (new)
- Default: gpt-5.4-mini with reasoning.effort="none"
- Recommendation: gpt-5.5 for quality
- Realtime API GA: gpt-realtime-1.5

**xAI Grok Build** (new)
- Coding model for agentic workflows
- Grok 4.1 Fast with agent tools
- Grok 4.3 fastest/most intelligent

**Impact on our repo**:
- ⚠️  `make-orchestrator-agent.md` could reference ADK 2.0 graph patterns
- ⚠️  Model recommendations may be stale (check current defaults)

### 6. New Patterns

**Advisor Tool** (Anthropic)
- Fast executor consults high-intelligence advisor mid-generation
- Cost optimization: cheap executor + expensive advisor for strategic decisions

**Google Gemini Interactions API**
- `previous_interaction_id` for server-side state
- Background execution: `background=true`
- Observable execution steps for UI/debugging

**Impact on our repo**:
- ❓ Advisor pattern interesting but niche (optional add)
- ⚠️  Interactions API could replace older conversation state patterns

---

## Current Repo Coverage Analysis

### ✅ What We Cover Well

1. **Basic agent authoring** (`make-agent.md`)
   - Prompt engineering, tool use, structured output
   - Behavioral discipline integration
   - QC framework

2. **Orchestration** (`make-orchestrator-agent.md`)
   - Multi-agent patterns, delegation, handoffs
   - Grounded in OpenAI/Anthropic/ADK patterns

3. **Knowledge integration** (`make-agent-knowledge.md`)
   - Files, caching, citations, retrieval
   - Cross-platform (Anthropic, Google, OpenAI, xAI)

4. **Quality control** (`make-agent-qc.md`, `make-AGENTS-qc.md`)
   - Structural validation, compliance checks

5. **Meta-documentation** (`make_AGENTS.md`)
   - AGENTS.md generation framework

### ❌ What We're Missing

1. **Managed agents guidance**
   - When to use managed vs self-hosted
   - Platform comparison (Anthropic vs Google vs OpenAI)
   - Configuration patterns

2. **Sandbox/stateful execution**
   - Persistent workspaces
   - Backend selection criteria
   - Memory patterns across runs

3. **Graph-based workflows** (ADK 2.0)
   - When to use graphs vs linear flows
   - Loop/branch patterns
   - Coordinator-subagent graphs

4. **Multimodal integration** (optional)
   - Voice agents
   - Image/video generation in agent loops

5. **New API patterns**
   - Interactions API (Google)
   - Advisor Tool (Anthropic)
   - Realtime API integration

### ⚠️  What Needs Refresh

1. **Model recommendations**
   - Check if gpt-5.4-mini, gpt-5.5, Gemini 3.5 Flash, Grok 4.3 are mentioned
   - Update defaults in examples

2. **Platform coverage**
   - Ensure all 6 platforms represented (Anthropic, Google, OpenAI, xAI, Nous, ADK)

3. **MCP references**
   - Formalize MCP integration patterns
   - Reference public MCP servers

---

## Proposed Updates (Prioritized)

### Priority 1: High Impact, Low Effort

#### 1.1 Update `make-agent.md` — Add Managed Agents Section
**Why**: Managed agents are a major shift (Anthropic, Google, OpenAI all offer them)
**What**:
- New section: "## Execution Model: Managed vs Self-Hosted"
- Decision matrix: when to use each
- Platform comparison table
- Configuration patterns for each platform

**Effort**: 2-3 hours
**Impact**: High (affects all future agent decisions)

#### 1.2 Update `make-agent-knowledge.md` — Add Interactions API
**Why**: Google Interactions API is GA and recommended for new projects
**What**:
- Update Google section with Interactions API patterns
- Add `previous_interaction_id` server-side state example
- Document background execution pattern

**Effort**: 1-2 hours
**Impact**: Medium-High (Google-specific but important)

#### 1.3 Create `knowledge/learned/` Lessons from This Refresh
**Why**: Dog-food our own learning loop (P-009 Hansei + Yokoten)
**What**:
- Lesson: "5-tier fetch system for documentation automation"
- Lesson: "Playwright required for React SPAs (platform.claude.com pattern)"
- Lesson: "GitHub API faster than HTTP for *.github.io domains"

**Effort**: 30 min
**Impact**: High (demonstrates our learning loop in action)

### Priority 2: Medium Impact, Medium Effort

#### 2.1 Create `make-managed-agent.md` Template
**Why**: New execution model deserves dedicated template
**What**:
- Full template for Anthropic/Google/OpenAI managed agents
- When to use managed vs self-hosted decision tree
- Platform-specific configuration examples
- Sandbox/environment patterns
- Tool integration (pre-built vs custom)

**Effort**: 4-6 hours
**Impact**: High (new capability class)

#### 2.2 Update `make-orchestrator-agent.md` — Add Graph Patterns
**Why**: ADK 2.0 introduces graph-based workflows (vs linear)
**What**:
- New section: "## Workflow Models: Linear vs Graph-Based"
- ADK 2.0 graph examples (SequentialAgent, ParallelAgent, LoopAgent)
- When to use graphs vs delegation
- Coordinator-subagent graph patterns

**Effort**: 2-3 hours
**Impact**: Medium (advanced orchestration pattern)

#### 2.3 Update Model Recommendations Throughout
**Why**: New defaults may be out of date
**What**:
- Audit all make_* templates for model recommendations
- Update to: gpt-5.5 (OpenAI), Gemini 3.5 Flash (Google), Grok 4.3 (xAI), Claude Sonnet 4.5 (Anthropic)
- Add reasoning.effort, verbosity settings where relevant

**Effort**: 1-2 hours
**Impact**: Medium (keeps examples current)

### Priority 3: Low Impact or High Effort

#### 3.1 Add MCP Integration Patterns Doc
**Why**: MCP is now cross-platform
**What**:
- New doc: `knowledge/mcp_integration_patterns.md`
- How to integrate MCP servers (OpenAI, Google, xAI)
- Public MCP servers list (e.g., gemini-api-docs-mcp.dev)
- Custom MCP server patterns

**Effort**: 3-4 hours
**Impact**: Medium (advanced integration topic)

#### 3.2 Add Optional Multimodal Section to `make-agent.md`
**Why**: Voice/image agents are emerging
**What**:
- Optional section: "## Multimodal Capabilities (Optional)"
- Voice agent patterns (xAI)
- Image/video generation integration
- When multimodal is useful vs overkill

**Effort**: 2-3 hours
**Impact**: Low-Medium (niche use cases)

#### 3.3 Create `make_voice_agent.md` Template (Future)
**Why**: Voice agents are a distinct class
**What**:
- Dedicated template for voice-first agents
- xAI Voice Agent, OpenAI Realtime API patterns
- Speech-to-text, text-to-speech integration
- Conversation flow patterns

**Effort**: 6-8 hours
**Impact**: Medium (emerging capability, niche for now)

#### 3.4 Hermes Auto-Distillation Deep Dive
**Why**: We were inspired by Hermes, should understand it fully
**What**:
- Research deep-dive into Hermes Agent auto-distillation
- Compare with our `knowledge/learned/` pattern
- Identify improvements we could adopt
- Document in `knowledge/hermes_comparison.md`

**Effort**: 4-6 hours
**Impact**: Low-Medium (learning/research value)

---

## Recommended Execution Order

### Phase 1: Quick Wins (Week 1)
1. ✅ Update `make-agent.md` — Add Managed Agents section
2. ✅ Update `make-agent-knowledge.md` — Add Interactions API
3. ✅ Create `knowledge/learned/` lessons from this refresh
4. ✅ Update model recommendations throughout

**Total effort**: ~6-8 hours
**Impact**: Brings repo current with major 2026 platform updates

### Phase 2: New Capabilities (Week 2-3)
5. ✅ Create `make-managed-agent.md` template
6. ✅ Update `make-orchestrator-agent.md` — Graph patterns
7. ✅ Add MCP integration patterns doc

**Total effort**: ~10-13 hours
**Impact**: Adds new template class, advanced orchestration patterns

### Phase 3: Optional/Future (Backlog)
8. ⏸️  Add multimodal section to `make-agent.md`
9. ⏸️  Create `make_voice_agent.md` (if demand emerges)
10. ⏸️  Hermes auto-distillation research

**Total effort**: ~12-17 hours
**Impact**: Niche/emerging capabilities

---

## Platform-Specific Notes

### Anthropic
- **Major update**: Claude Managed Agents platform
- **New pattern**: Advisor Tool (executor + advisor)
- **Action**: Priority 1.1 (managed agents), optional Advisor Tool section

### Google
- **Major update**: Interactions API GA (June 2026)
- **Major update**: Antigravity + Deep Research managed agents
- **Major update**: ADK 2.0 graph workflows
- **Action**: Priority 1.2 (Interactions API), Priority 2.2 (graph patterns)

### OpenAI
- **Major update**: Sandbox Agents beta
- **Major update**: Enhanced MCP
- **Model update**: gpt-5.4-mini/gpt-5.5 defaults
- **Action**: Priority 2.1 (managed agents includes sandboxes), Priority 2.3 (models)

### xAI
- **New**: Voice Agent, Speech APIs (GA)
- **New**: Grok Build coding model
- **Model update**: Grok 4.3
- **Action**: Priority 2.3 (model updates), Priority 3.2 (multimodal - voice)

### Nous Research
- **New**: Hermes Agent (inspired our learning loop)
- **Action**: Priority 3.4 (research deep-dive)

---

## Success Criteria

### Phase 1 Complete When:
- [ ] `make-agent.md` has managed agents decision section
- [ ] `make-agent-knowledge.md` covers Interactions API
- [ ] `knowledge/learned/` has 3+ lessons from this refresh
- [ ] All templates reference current model defaults (gpt-5.5, etc.)

### Phase 2 Complete When:
- [ ] `make-managed-agent.md` exists and covers all 3 platforms
- [ ] `make-orchestrator-agent.md` has graph workflow section
- [ ] MCP integration patterns documented

### Phase 3 Complete When:
- [ ] Multimodal capabilities documented (voice, image/video)
- [ ] Voice agent template exists (if needed)
- [ ] Hermes comparison doc exists

---

## Questions to Resolve

1. **Managed agents scope**: Should `make-managed-agent.md` be a separate template, or fold into `make-agent.md` as a section?
   - **Recommendation**: Separate template (different enough to warrant it)

2. **ADK 2.0 coverage**: Should we create `make_adk_agent.md` specifically for ADK patterns?
   - **Recommendation**: No - fold into `make-orchestrator-agent.md` as an advanced pattern

3. **Multimodal priority**: Is voice/video integration important enough for Priority 2?
   - **Recommendation**: No - keep in Priority 3 until user demand emerges

4. **Hermes deep-dive**: Worth the effort?
   - **Recommendation**: Yes if time permits (learning value), but Priority 3

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Start Phase 1** (quick wins, ~6-8 hours)
3. **Assess impact** after Phase 1, decide if Phase 2 is priority
4. **Iterate** based on user feedback and emerging patterns

---

**Plan created**: 2026-07-06
**Based on**: 65 refreshed sources (32 new, 33 updated)
**Estimated total effort**: 28-38 hours across 3 phases
**Recommended start**: Phase 1 (6-8 hours, high impact)
