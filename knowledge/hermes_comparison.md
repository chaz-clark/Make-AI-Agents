---
name: Hermes Agent Learning Loop Comparison
description: Comparison of Hermes Agent auto-distillation vs Make-AI-Agents manual learning, with adoption recommendations
version: "1.0"
created: 2026-07-06
---

# Hermes Agent Auto-Distillation vs Make-AI-Agents Manual Learning

## Executive Summary

Hermes Agent implements a **closed learning loop** with autonomous skill creation, periodic memory nudges, and self-improving skills. Make-AI-Agents uses a **manual Sprint B Learning loop** with session-end lesson distillation to `knowledge/learned/`.

**Key finding**: Hermes automates what we do manually. Adopting selective automation (periodic nudges, skill templates) would improve consistency without sacrificing quality control.

**Recommendation**: Hybrid approach — automate nudges and skill scaffolding, keep human-in-loop for quality and propagation decisions.

---

## Architecture Comparison

### Hermes Agent Learning Loop

**Components**:
1. **Agent-curated memory** - LLM selects what to remember from conversations
2. **Periodic nudges** - System prompts agent at intervals to distill learnings
3. **Autonomous skill creation** - Agent writes skills to filesystem when patterns emerge
4. **Skill self-improvement** - Skills update themselves during use based on failures
5. **FTS5 cross-session recall** - Full-text search with LLM summarization for context retrieval
6. **Honcho dialectic user modeling** - Builds user preference model across sessions

**Flow**:
```
Conversation → Agent notes learnings → Periodic nudge fires → Agent reviews notes →
Agent creates/updates skill → Skill stored → Future sessions auto-load skill →
Skill self-improves on failure → Cycle continues
```

**Automation level**: 90% autonomous (human rarely intervenes)

**Quality control**: Minimal — agent self-governs with constitutional constraints

---

### Make-AI-Agents Learning Loop (Current)

**Components**:
1. **Manual lesson capture** - Human or agent writes to `knowledge/learned/*.md` at session end
2. **Sprint B post-session review** - Human reviews session, identifies patterns, creates lessons
3. **Template updates** - Lessons inform updates to `make_agent.md`, `behavioral_discipline.json`, etc.
4. **Handoff propagation** - Changes cascade to consumer repos via `handoffs/` documents
5. **make_agent_qc validation** - All generated agents pass 20 QC rules before acceptance

**Flow**:
```
Session completes → Human identifies lessons → Writes lesson.md →
Reviews AGENTS.md / make_agent.md → Updates if material → Runs make_agent_qc →
Creates handoffs if cascading → Consumer repos apply → Cycle completes
```

**Automation level**: 10% autonomous (mostly manual)

**Quality control**: High — human reviews every lesson, QC validates every artifact

---

## Feature-by-Feature Comparison

| Feature | Hermes Agent | Make-AI-Agents | Gap |
|---------|--------------|----------------|-----|
| **Memory Persistence** | FTS5 database, LLM-summarized | Markdown files (`knowledge/learned/`) | Hermes: searchable, summarized; Ours: flat files, manual search |
| **Lesson Capture** | Autonomous (periodic nudges) | Manual (Sprint B or explicit writes) | Hermes: automatic; Ours: manual intervention |
| **Skill Creation** | Autonomous (agent writes to filesystem) | Manual (human writes make_*.md templates) | Hermes: creates skills on-the-fly; Ours: templates are hand-crafted |
| **Skill Improvement** | Autonomous (self-modifies on failure) | Manual (human reviews, updates template) | Hermes: self-healing; Ours: requires human diagnosis |
| **Cross-Session Recall** | FTS5 + LLM query | Read `knowledge/learned/` files explicitly | Hermes: auto-retrieves relevant context; Ours: manual file reads |
| **User Modeling** | Honcho dialectic (builds preference model) | None (no user state tracking) | Hermes: adapts to user; Ours: generic |
| **Quality Control** | Constitutional constraints only | make_agent_qc (20 rules, 17 dimensions) | Ours: stronger QC; Hermes: looser |
| **Propagation** | Skills auto-load in future sessions | Handoffs + manual consumer repo application | Ours: explicit propagation; Hermes: implicit |

---

## What We Could Adopt

### 1. Periodic Nudges for Lesson Capture (High Value)

**Hermes pattern**: System prompts agent every N messages or at session end to review conversation and extract learnings.

**Adoption in Make-AI-Agents**:
- Add `post_session_review` hook to agent execution
- Prompt: "Review this session. Identify patterns, failures, or insights worth capturing. Write to `knowledge/learned/<timestamp>_<topic>.md` if material."
- Human reviews auto-generated lesson, approves/edits/rejects
- Reduces forgetting (lessons capture happens automatically)

**Implementation**:
```python
def post_session_review(session_transcript: str, agent_context: dict):
    """
    Triggered at session end. Agent reviews transcript and auto-drafts lessons.
    """
    prompt = f"""
    Review this session transcript:
    {session_transcript}

    Identify:
    1. New patterns worth documenting
    2. Failures or errors that revealed gaps
    3. Insights applicable to future sessions

    If material, write a lesson to knowledge/learned/ following this template:
    ---
    name: <concise-name>
    observed_in: <session-id>
    confidence: <high/medium/low>
    ---
    # Lesson: <title>
    ## What Happened
    ## The Pattern
    ## Results
    ## When to Apply
    """

    # Agent generates draft lesson
    draft_lesson = agent.run(prompt)

    # Human reviews in next session or async
    save_for_review(draft_lesson, "pending_lessons/")
```

**Benefit**: Captures learnings in-the-moment, reduces manual Sprint B overhead.

**Risk**: Noise (agent may draft non-material lessons). Mitigated by human review gate.

---

### 2. Skill Scaffolding Templates (Medium Value)

**Hermes pattern**: When agent identifies a repeated task, it writes a skill file (markdown + optional code) to a known location. Future sessions auto-load it.

**Adoption in Make-AI-Agents**:
- Don't auto-create `make_*.md` templates (too high-stakes)
- DO auto-create **helper skill snippets** for common tasks
- Example: Agent notices it repeatedly converts HTML to markdown → drafts `html_to_md_snippet.py` → human reviews → promotes to tool if useful

**Implementation**:
```python
# Agent detects pattern
if task_count("html_to_markdown") > 3:
    draft_skill(
        name="html_to_md_snippet",
        description="Extract clean markdown from HTML",
        code="""
        from bs4 import BeautifulSoup
        import html2text

        def html_to_markdown(html: str) -> str:
            soup = BeautifulSoup(html, 'html.parser')
            # ... agent-generated extraction logic
            return markdown
        """,
        save_to="skills/drafts/",
    )
```

**Benefit**: Reduces repetitive manual coding. Agent identifies patterns human might miss.

**Risk**: Generated code quality varies. Mitigated by draft folder + human review.

---

### 3. Cross-Session Context Retrieval (Low Value, but Nice)

**Hermes pattern**: FTS5 database for full-text search across all memory. LLM summarizes search results before injecting into context.

**Adoption in Make-AI-Agents**:
- Add `search_learned_lessons(query: str)` tool
- FTS5 index over `knowledge/learned/*.md`
- Agent calls tool when needed instead of manual "read these files" prompts

**Implementation**:
```python
import sqlite3

# Build FTS5 index
conn = sqlite3.connect("knowledge.db")
conn.execute("CREATE VIRTUAL TABLE lessons USING fts5(filename, content)")

for file in glob("knowledge/learned/*.md"):
    content = open(file).read()
    conn.execute("INSERT INTO lessons VALUES (?, ?)", (file, content))

# Search function
def search_learned_lessons(query: str) -> list[str]:
    results = conn.execute(
        "SELECT filename FROM lessons WHERE lessons MATCH ? ORDER BY rank LIMIT 5",
        (query,)
    ).fetchall()
    return [r[0] for r in results]

# Agent usage
relevant_lessons = search_learned_lessons("documentation refresh patterns")
# Agent reads top 5 files instead of guessing which to read
```

**Benefit**: Faster context retrieval. Agent finds relevant lessons automatically.

**Risk**: Search quality depends on query formulation. Mitigated by LLM summarization layer.

---

### 4. Skill Self-Improvement (Not Recommended)

**Hermes pattern**: Skills modify themselves when they fail. If `search_docs` skill returns empty, it rewrites its search strategy and saves the update.

**Why NOT to adopt**:
- Make-AI-Agents templates are **meta-skills** (they generate other artifacts). Self-modification would break quality control.
- Hermes skills are **procedural** (do one task). Self-modification is safe because scope is narrow.
- Our QC process (`make_agent_qc`, `make_AGENTS_qc`) requires human judgment on propagation.

**Alternative**: Capture failure as lesson, human reviews, updates template manually. Slower but safer.

---

### 5. User Modeling (Not Applicable)

**Hermes pattern**: Honcho tracks user preferences, communication style, domain expertise across sessions. Agent adapts tone, verbosity, technical depth.

**Why NOT to adopt**:
- Make-AI-Agents templates are **multi-user** (consumed by many developers, not one end-user).
- User modeling assumes single user across sessions. Our consumers are diverse.
- Personalization would degrade template generality.

**Exception**: If Make-AI-Agents becomes a **service** (not just templates), user modeling per consumer could be valuable.

---

## Recommendations

### Adopt Now (Sprint 3 Extension or Sprint 4)

**1. Post-Session Lesson Nudge**
- **What**: Auto-prompt agent at session end to draft lesson
- **Effort**: 2-3 hours (add hook + prompt template)
- **Impact**: High (reduces forgetting, improves Sprint B throughput)
- **Implementation**: Add to `make_agent.md` as optional post-session hook

**2. FTS5 Lesson Search Tool**
- **What**: Index `knowledge/learned/` for full-text search
- **Effort**: 3-4 hours (build index + search tool)
- **Impact**: Medium (faster context retrieval)
- **Implementation**: Standalone script + agent tool registration

### Consider Later (Sprint 5+)

**3. Skill Scaffolding for Helper Functions**
- **What**: Agent drafts reusable code snippets when patterns emerge
- **Effort**: 6-8 hours (pattern detection + draft generation)
- **Impact**: Medium (reduces manual coding for common tasks)
- **Risk**: Code quality varies, requires review gate

### Do NOT Adopt

**4. Skill Self-Modification**
- **Reason**: Meta-skill templates require stability and QC
- **Alternative**: Manual review + update cycle

**5. User Modeling**
- **Reason**: Multi-user template consumers (not single end-user)
- **Exception**: Revisit if Make-AI-Agents becomes a service

---

## Implementation Plan (Sprint 3 Extension)

### Task 1: Post-Session Lesson Nudge (3 hours)

**Deliverable**: Add optional post-session hook to `make_agent.md`

**Pattern**:
```markdown
## Post-Session Learning (optional)

**When to include**: Long-running agents that should capture learnings automatically.

**Implementation**:
1. Add post-session hook to agent execution loop
2. Prompt agent: "Review session. Draft lesson if material."
3. Save draft to `knowledge/learned/pending/<timestamp>_<topic>.md`
4. Human reviews in next session or async

**Example**:
```python
def post_session_hook(session_transcript: str):
    draft = agent.run(POST_SESSION_REVIEW_PROMPT, context=session_transcript)
    if draft.is_material:
        save_draft(draft, "knowledge/learned/pending/")
```
```

### Task 2: FTS5 Lesson Search (4 hours)

**Deliverable**: Standalone script + agent tool

**Files**:
- `tools/search_learned_lessons.py` - FTS5 index builder + search function
- `tools/search_learned_lessons_tool.json` - Tool registration for agents

**Usage**:
```python
# In agent execution
results = search_learned_lessons("documentation refresh patterns")
# Returns: ["5tier_fetch_automation.md", "playwright_react_spa_pattern.md", ...]

# Agent reads top N results for context
```

**Index rebuild**: Run `python tools/search_learned_lessons.py --rebuild` after new lessons added.

---

## Key Differences Philosophy

**Hermes Agent**:
- **Optimize for**: Autonomous operation, minimal human intervention
- **Use case**: Personal assistant, long-running workflows, exploratory tasks
- **Trade-off**: Speed and autonomy > strict quality control

**Make-AI-Agents**:
- **Optimize for**: Quality, reproducibility, cascading correctness
- **Use case**: Template generation, meta-skills, multi-consumer artifacts
- **Trade-off**: Quality control and propagation discipline > speed

**Conclusion**: Hermes patterns fit our workflow when they **augment** human judgment (nudges, search), not when they **replace** it (self-modification, user modeling).

---

## Resources

**Hermes Agent**:
- Main site: https://hermes-agent.nousresearch.com/
- GitHub: https://github.com/NousResearch/hermes-agent
- Docs: https://hermes-agent.nousresearch.com/docs

**Nous Research**:
- Company: https://nousresearch.com
- Models: Hermes, Nomos, Psyche

**Make-AI-Agents Current State**:
- Behavioral Discipline: `knowledge/behavioral_discipline.md`
- Learned Lessons: `knowledge/learned/*.md`
- Learning Loop: Sprint B (manual post-session review)
- Quality Control: `make_agent_qc.md` (20 rules, 17 dimensions)

**Related**:
- Our `knowledge/learned/` pattern was inspired by Hermes but implemented manually
- Hermes `/llms.txt` and `/llms-full.txt` patterns are worth studying for doc distribution

---

**Version**: 1.0
**Last Updated**: 2026-07-06
**Status**: Research complete, recommendations ready for Sprint 3 extension or Sprint 4
