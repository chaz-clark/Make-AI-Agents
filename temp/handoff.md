# Handoff — Toyota Way Agent Skill (Proposed)

> Status: design proposal, not yet implemented.
> Author: Chaz Clark (downstream user / fork maintainer).
> Audience: maintainer of `forrestchang/andrej-karpathy-skills`, the `make-ai-agents` repo this will be implemented into, and downstream users (including `canvas_toolbox`) who will subtree the result.

## What this proposes

Add a sibling skill alongside `skills/karpathy-guidelines/` that captures **Toyota Production System / Toyota Way / Toyota Business Practices** principles as concrete agent behaviors.

The four Karpathy principles teach an LLM to act like a *senior individual coder*. Toyota Way teaches an LLM to act like a *quality-disciplined production worker* — explicit plan before execution, small reversible steps, stop-on-defect, root-cause analysis, and standardized handoffs. They compose. Karpathy gives the worker-level habits; Toyota gives the system-level discipline that makes those habits stick under pressure.

## The trust gap this fills

The Karpathy guidelines target experienced developers using AI coding agents. They prevent the agent from *embarrassing* the developer. They do not, by themselves, give a *non-technical user* enough visible structure to extend trust to the agent.

Non-technical users (instructors, analysts, course designers, line-of-business folks) need an agent that:

- **States the plan before executing.** Trust comes from predictability, not from clever output.
- **Confirms understanding before acting.** The agent restating the goal in its own words makes mistakes catchable before they ship.
- **Takes small, named steps.** Each step has a verifiable result before the next begins.
- **Stops on the first defect.** A test fails → don't paper over it. A precondition isn't met → name it and pause.
- **Surfaces tradeoffs explicitly.** "I can do X or Y; X is faster but loses Z. Which?"
- **Documents the change as a structured artifact** (current state → target → countermeasure → verification), not a wall of free text.

This is what the Toyota Way already systematizes for human factory workers. The same discipline, ported to AI agents, produces an agent a non-technical user can learn to trust.

## How this complements karpathy-guidelines

| Layer | Karpathy's 4 | Toyota Way adds |
|---|---|---|
| Worker-level discipline | Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution | — |
| System-level discipline | — | Genchi Genbutsu, Jidoka, A3, 5 Whys, Kaizen, Hansei, Pull, Standard Work, Nemawashi, Catchball, Yokoten, Heijunka, Andon, Poka-yoke, 3 Ms, Respect for People, PDCA, Hoshin Kanri, TBP 8-step |

Mapping the four Karpathy principles to their reinforcing Toyota concepts:

| Karpathy | Reinforced by |
|---|---|
| Think Before Coding | Genchi Genbutsu (read the actual file/output, don't theorize) + 5 Whys (don't accept the surface symptom) + Nemawashi (build understanding before changing) |
| Simplicity First | Pull system / JIT (only what's pulled, no overproduction) + 3 Ms (eliminate Muda — wasted work) |
| Surgical Changes | Standard Work (consistent process across invocations) + Poka-yoke (don't introduce new failure surface) |
| Goal-Driven Execution | A3 (current → target → verify) + Jidoka (stop on defect, surface immediately) + PDCA (Plan-Do-Check-Act loop) |

## Scope decisions — what's included and what's not

This is the comprehensive Toyota inventory I considered. Each entry is marked **IN** (proposed for the skill) or **OUT** (explicitly excluded, with reasoning) so each "OUT" decision can become an issue for review.

### Foundation / philosophy

| Concept | In/Out | Reasoning |
|---|---|---|
| **Genchi Genbutsu** (go and see) | **IN** | The most important one. "Read the actual file, run the actual test, don't summarize from priors." Anti-hallucination. |
| **Hansei** (relentless reflection) | **IN** | Self-critique after every task. "What went wrong? What would I do differently?" Drives the agent to learn within a session. |
| **Respect for People** | **IN** | Don't override the user's intent. Ask rather than assume. Surface tradeoffs. Maps perfectly to "the user is the customer." |
| **Kaizen** (continuous improvement) | **IN** | Small reversible steps over big rewrites. Iterative improvement with feedback at each step. |
| **Yokoten** (horizontal deployment) | **IN** | Lessons from one session apply to others. Maps to Antigravity's Knowledge Items, Claude Code's memory system. |

### Quality pillars

| Concept | In/Out | Reasoning |
|---|---|---|
| **Jidoka** (built-in quality / stop on defect) | **IN** | First failed test = stop. Don't paper over. The single most impactful Toyota concept for agent reliability. |
| **Poka-yoke** (mistake-proofing) | **IN** | Structured outputs, type signatures, validation. Make wrong outputs hard to produce. |
| **Andon** (pull the cord) | **IN** | "I cannot proceed because X" — surface blockers immediately, don't guess your way through them. |
| **Standard Work** | **IN** | Consistent agent behavior across invocations. Maps to specifications / SKILL.md / AGENTS.md. |

### Pull / flow

| Concept | In/Out | Reasoning |
|---|---|---|
| **JIT / Pull system / Kanban** | **IN** | "Only what was asked, when it was asked." Reinforces Karpathy's Simplicity First. |
| **3 Ms — Muda, Mura, Muri** | **IN** | Waste (unused output), unevenness (inconsistent quality across invocations), overburden (context window saturation). Useful diagnostic vocabulary. |
| **Heijunka** (level-loading) | **IN** | Break large tasks into evenly-sized pieces. Avoid one giant atomic operation that's hard to verify. |

### Problem solving

| Concept | In/Out | Reasoning |
|---|---|---|
| **TBP 8-step** | **IN** | The structural backbone. Every non-trivial agent task should follow: clarify → break down → target → root cause → countermeasures → execute → evaluate → standardize. |
| **A3 reporting** | **IN** | The structured one-page artifact for any change. Current → target → gap → root → countermeasure → verification. |
| **5 Whys** | **IN** | Bug fixes target root cause, not symptom. Pairs with Genchi Genbutsu. |
| **PDCA** (Plan-Do-Check-Act) | **IN** | The fundamental task loop. PDCA is the engine; A3 is the documentation of one PDCA cycle. |

### Decision-making / coordination

| Concept | In/Out | Reasoning |
|---|---|---|
| **Nemawashi** (build consensus before deciding) | **IN** | Propose the plan and surface tradeoffs *before* acting. "Lay the roots." This is exactly the trust-building behavior non-technical users need. |
| **Catchball** (back-and-forth refinement) | **IN** | The propose → feedback → revise loop. First plan is a draft, not a commitment. |
| **Hoshin Kanri** (strategy deployment) | **IN** | Every action traces to the larger goal. Prevents agent drift in long sessions. |

### Excluded — for transparency

| Concept | In/Out | Reasoning |
|---|---|---|
| **5S** (Sort/Set in order/Shine/Standardize/Sustain) | **OUT** | Workplace organization. Could be metaphorically mapped to "keep your workspace clean" — but it's a stretch. Standard Work already covers consistency. *Issue candidate: should 5S map to repo cleanliness practices (no orphan files, organized imports)?* |
| **Obeya** (the big room) | **OUT** | Co-located cross-functional teams sharing physical workspace. Maps to multi-agent systems with shared context, but stretched for single-agent skills. *Issue candidate: revisit when multi-agent orchestration patterns emerge.* |
| **TWI — Job Instruction / Job Methods / Job Relations** | **OUT** | Training-within-industry methodology for human workers. Could apply to how agents learn from sessions, but indirect — Yokoten already covers cross-session knowledge transfer. *Issue candidate: revisit if "training agents on agents" becomes a pattern.* |
| **OEE** (Overall Equipment Effectiveness) | **OUT** | Measurement framework, not a behavioral practice. Useful for evaluation harnesses but doesn't shape agent behavior directly. *Issue candidate: track separately as part of evaluation/observability.* |
| **Heijunka card / Mizusumashi / Genba kaizen events / Quality Circles** | **OUT** | Operational practices specific to factory floor; no clear single-agent mapping. *Issue candidate: revisit at multi-agent scale.* |

The "OUT" decisions are not final — they're starting points. Each is suitable as a separate GitHub issue once the fork's issue tracker is enabled, so the community can argue for re-inclusion case-by-case.

## Proposed SKILL.md structure

This is the implementation outline, not the implementation. The maintainer (or `make-ai-agents`) writes the actual file from this skeleton.

```
---
name: toyota-way-agents
description: System-level discipline for AI coding agents — quality at every
  step, plan before execution, stop on defect, root-cause over symptom.
  Composes with karpathy-guidelines (worker-level discipline) to produce an
  agent non-technical users can learn to trust.
license: MIT
---

# Toyota Way for AI Agents

[Brief intro — system discipline that complements karpathy-guidelines.
The "trust gap" framing for non-technical users.]

## How this fits with karpathy-guidelines

[Mapping table from this handoff.]

## The Discipline

### 1. Genchi Genbutsu — Go and see
[Don't theorize. Read the actual file. Run the actual test. Inspect the
actual output. The closer to the source, the truer the input.]

### 2. Plan before execution (Nemawashi + TBP)
[State the plan. Confirm understanding. Wait for buy-in on non-trivial
changes. Don't ship the first plan — propose, get feedback, revise.]

### 3. Stop on defect (Jidoka + Andon)
[First failed test, first failed precondition, first ambiguity → stop.
Surface the issue. Don't keep going on a broken foundation.]

### 4. Find root cause (5 Whys)
[Bug fixes target the root, not the symptom. Ask "why" until the answer
is structural, not incidental.]

### 5. Small steps, verified (Kaizen + PDCA)
[Each change is small enough to verify. Each step has a check before
the next begins. Reversibility is a feature.]

### 6. Document as A3
[For any non-trivial change: current state → target → gap → root cause →
countermeasure → verification. Not as bureaucracy — as the structure that
makes the change reviewable.]

### 7. Pull, don't push (JIT + 3 Ms)
[Only generate what was asked. No speculative features. Eliminate Muda
(waste), Mura (inconsistency), Muri (overload).]

### 8. Mistake-proof outputs (Poka-yoke + Standard Work)
[Structured output schemas. Type-checked returns. Consistent format
across invocations. Make the wrong output hard to produce.]

### 9. Reflect after (Hansei + Yokoten)
[At task end: what went well, what would I do differently, what should
the next session know? Surface lessons explicitly.]

### 10. Respect the user's intent (Respect for People + Hoshin Kanri)
[The user named the goal. Every action traces to that goal. Don't
override their judgment. Ask before reinterpreting.]

## What "good" looks like

[Concrete agent behaviors — this is where the trust angle pays off:
- Plans are stated in plain language, not technical jargon
- Each step has a check-in or a verifiable result
- Failures surface immediately as "I cannot proceed because X"
- Tradeoffs are presented as "X or Y, here's the difference"
- Long tasks decompose visibly into small reversible pieces
- Final output includes a verification check, not just a claim of success]

## When to apply this skill

[Always — this is system discipline, not task-specific. Pairs with
karpathy-guidelines. The two together are the recommended baseline
for any production agent serving non-technical users.]
```

## Concrete agent behaviors — the trust payoff

For non-technical users, the visible difference between a "with Toyota Way" agent and a "without" agent looks like this:

| User experience | Without Toyota Way | With Toyota Way |
|---|---|---|
| Asks for a change | Agent immediately starts editing files | Agent restates the goal, names the steps, surfaces tradeoffs, asks for go-ahead |
| Hits a failing test | Agent retries or works around it | Agent stops, names the failure, asks how to proceed |
| Multi-step task | One large monolithic operation | Visibly decomposed into named steps with verification between each |
| Bug fix | Patch on the symptom | "The symptom was X, the root cause is Y, here's the structural fix" |
| Long session | Drift from original goal | Every action references the original goal; agent flags if it's changed |
| Final report | "Done." | Current → target → countermeasure → verification — auditable structure |

This is the behavior that earns trust from a non-technical user. Karpathy's guidelines prevent obvious failures. Toyota Way produces the *visible discipline* that lets a user predict what the agent will do next.

## Implementation path

```
1. handoff.md (this file)              ← in the andrej-karpathy-skills fork
        ↓
2. Issues opened on the fork           ← one per excluded concept; one for the skill itself
        ↓
3. SKILL.md drafted in make-ai-agents  ← the actual implementation
        ↓
4. PR upstream to forrestchang/...     ← contribute back to the source
        ↓
5. Subtree pull into canvas_toolbox    ← apply the discipline to the canvas audit agents
        ↓
6. AGENTS.md / CLAUDE.md influence     ← cascade the principles into baseline project context
```

Step 6 is downstream impact: once the skill exists, the canvas_toolbox `AGENTS.md` and any project's `CLAUDE.md` should reference it as the recommended companion to karpathy-guidelines. For non-technical Canvas instructors using AI to audit their courses, this is the layer that makes the audit agent trustworthy.

## Open questions — issue candidates

When the fork's issue tracker is enabled, these are natural starting issues:

1. **Skill scope** — single comprehensive `toyota-way-agents` skill, or split into `toyota-philosophy/`, `toyota-quality/`, `toyota-problem-solving/`, `toyota-pull-flow/`?
2. **5S inclusion** — does it map meaningfully to repo cleanliness or is it a stretch?
3. **Obeya inclusion** — when multi-agent patterns emerge, what's the right framing?
4. **TWI / training-the-agent** — should we have a sibling skill on agent self-improvement?
5. **A3 template format** — should the skill ship a literal A3 template the agent fills in, or just the prose principles?
6. **Trust-for-non-tech-users framing** — is this the primary angle, or a secondary one? (Maintainer may have a different positioning preference.)
7. **Composition with karpathy-guidelines** — should the SKILL.md `description` mention karpathy-guidelines explicitly, or rely on host-tool ordering?

## Related context

- The closest existing synthesis is [`TheRealSeanDonahoe/agents-md`](https://github.com/TheRealSeanDonahoe/agents-md), which combines Karpathy's four with Boris Cherny's Claude Code workflow. It does not include Toyota Way / TPS principles. This proposal is genuinely additive, not duplicative.
- Toyota's own AI program (GAIA, launched 2025) is ["rooted in Jidoka"](https://www.klover.ai/toyota-ai-strategy-analysis-of-ai-driven-dominance-in-automative/), confirming that TPS principles do transfer cleanly to AI deployment — but no public AGENTS.md / SKILL.md captures this for the coding-agent ecosystem yet.
- A downstream consumer (`canvas_toolbox`) is documented at [`agents/AGENT_LAYERS.md`](https://github.com/chaz-clark/canvas_toolbox/blob/main/agents/AGENT_LAYERS.md) — taxonomy of runtime / capability / specification agent layers. This proposed skill operates at the **specification** layer.
- The [`toyota_gap_analysis_knowledge.md`](https://github.com/chaz-clark/canvas_toolbox/blob/main/agents/knowledge/toyota_gap_analysis_knowledge.md) in canvas_toolbox already applies A3 + Genchi Genbutsu to Canvas course auditing — proof-of-concept that the principles port cleanly into a domain-specific agent.

## Out of scope for this handoff

- Writing the actual SKILL.md content (the maintainer / `make-ai-agents` does this).
- Modifying the existing `karpathy-guidelines` skill — it stands on its own and should remain intact.
- Modifying the existing `CLAUDE.md` at the root of this repo — again, separate skill, separate file, additive.

---

**Next step:** enable issues on this fork, then convert the open questions above into individual issues for community discussion. The skill itself should be drafted in `make-ai-agents`, then PR'd back here once stable.
