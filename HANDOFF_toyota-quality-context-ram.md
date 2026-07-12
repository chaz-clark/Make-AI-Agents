---
direction: deliver
status: delivered
from_repo: Make-AI-Agents
to_repo: Make-AI-Agents
date_created: 2026-07-12
last_updated: 2026-07-12
trigger: P-011 Toyota Quality Loop + context RAM discipline updates
priority: medium
---

# Handoff: Toyota Quality Loop + Context RAM Discipline

**To**: Make-AI-Agents
**From**: Make-AI-Agents
**Date**: 2026-07-12
**Type**: Framework update delivery

---

## What Changed in Make-AI-Agents

Two framework enhancements delivered to all consumer repos:

### 1. P-011: Toyota Quality Loop (NEW)

**Added to behavioral-discipline.md v1.5** as the 11th principle (NO-OVERRIDE):

```
Prevent (Poka-yoke) → Detect (Jidoka) → Verify (Genchi Gembutsu)
```

**The three principles**:
- **Genchi Gembutsu (現地現物)** - Go and See / Verify with Real Data
  - Don't assume, verify with real data
  - Test with REAL user data, not synthetic fixtures
  - **Trigger**: When you say "probably" or "should" → STOP and verify

- **Jidoka (自働化)** - Built-in Quality / Stop on Defect
  - Write tests WITH code, not after
  - Red tests block progress - fix immediately, don't defer
  - **Trigger**: When you want to say "we'll fix this later" → STOP and fix now
  - Aligns with P-003 Stop on Defect

- **Poka-yoke (ポカヨケ)** - Mistake-Proofing
  - Design so mistakes can't happen
  - Automate validation (no manual steps)
  - **Trigger**: When manual verification required → Design it out

**Why**: Discovered in canvas-toolbox offline mode work - these three prevent defects systematically.

**Source**: canvas-toolbox handoff (2026-07-12), canvas-toolbox commit c7342d2

---

### 2. Context RAM Discipline (UPDATED)

**Updated AGENTS.md size thresholds** in make-AGENTS.md Principle #2:

| Metric | Old | New | Purpose |
|---|---|---|---|
| **Byte size** | - | **30KB target, 40KB max** | Context RAM management |
| **Line count** | 1200 hard | 800 soft, 1200 hard | Auto-include buffer |
| **Token count** | 25k hard | 8k soft, 12k hard | Auto-include limit |

**Context RAM principle**: Bloated AGENTS.md files compete with actual working context (code under edit, test output, error messages), increasing the frequency of context-window exhaustion and conversation resets.

**Pattern**: Extract detailed explanations into knowledge files (e.g., `knowledge/working-style-<project>.md`) and keep only bullet summaries in AGENTS.md with reference links.

**Example**: canvas-toolbox trimmed 43KB → 33KB by extracting Working Style details.

**New QC checks**:
- **AGENTS-QC-010**: File size limits (30KB target, 40KB max)
- **AGENTS-QC-011**: Active Context bloat check (≤5 dated entries, ≤150 lines)
- **AGENTS-QC-012**: Toyota Quality Loop section present

---

## What We Did to Your Repo

### ✅ Added Toyota Quality Loop Section

**Location**: AGENTS.md, positioned after `## Working Style`, before `## Learning loop` or `## Active Context`

**Content**: Full Toyota Quality Loop section with all three principles and behavioral triggers

**Size impact**: ~2KB added (~45 lines)

### ✅ Size Compliance Check

**Your repo**: 27.2 KB

**Status**: ✅ Under 30KB target / ⚠️ Over 30KB target, under 40KB max

---

## What You Should Know

### 1. Toyota Quality Loop is Now Core Discipline

P-011 is a **NO-OVERRIDE** principle (like P-001, P-003, P-007, P-010). Violating the quality loop creates technical debt.

**Behavioral triggers are in your user profile** (`~/.claude/memory/user_chaz.md`) so agents will apply them automatically.

### 2. AGENTS.md Size Budget

**30KB is the target** to preserve working context RAM:
- Every byte in AGENTS.md competes with code, test output, and error messages
- Bloated AGENTS.md increases conversation reset frequency

**If you exceed 30KB** (soft warning):
- Extract detailed explanations to `knowledge/working-style-<repo>.md`
- Keep only bullet summaries in AGENTS.md with reference links
- Move tool catalogs to READMEs or knowledge files
- Trim Active Context to latest 3-5 entries only

**40KB is the hard max** - agents may refuse to work if exceeded.

### 3. Required Sections Updated

AGENTS.md now has **7 required sections** (was 6):
1. Project Name
2. Project Purpose
3. Structure
4. Working Style
5. **Toyota Quality Loop** ← NEW
6. Learning loop
7. Active Context

---

## Examples

### Behavioral Triggers in Action

**Before** (violates P-011):
```
Agent: "This API call should work based on the docs"
```

**After** (follows P-011):
```
Agent: "I'm about to say 'should' - STOP. Let me verify with a real API call first."
[Makes actual API call with test data]
Agent: "Verified: The API returns 200 with this payload."
```

---

**Before** (violates P-011):
```
Agent: "Tests are failing but I'll fix them later"
```

**After** (follows P-011):
```
Agent: "Tests failing - STOP. Fixing now before proceeding."
[Fixes tests]
Agent: "Green tests. Now continuing with next step."
```

---

**Before** (violates P-011):
```
Agent: "Remember to manually validate the export before uploading"
```

**After** (follows P-011):
```
Agent: "Manual validation is required - STOP. Designing automated validation instead."
[Adds validate_export() function with automated checks]
Agent: "Export blocked if validation fails. Upload only happens after automated green light."
```

---

## Related Commits

**Make-AI-Agents**:
- 6ed827c - Add P-011 Toyota Quality Loop to behavioral discipline
- ce058c2 - Add context RAM discipline (30KB target, 40KB max)
- ba54b57 - Add Toyota Quality Loop to Make-AI-Agents AGENTS.md

**Your repo**:
- ba54b57 - Add Toyota Quality Loop section to AGENTS.md

---

## Questions?

This is a **delivered** handoff - changes already applied to your repo.

If you need to trim your AGENTS.md below 30KB, follow the pattern:
1. Create `knowledge/working-style-<repo>.md` with detailed explanations
2. Replace detailed sections in AGENTS.md with bullet summaries + reference link
3. Example: See canvas-toolbox (commit c7342d2) or Make-AI-Agents AGENTS.md

---

## Success Criteria

**This handoff is "applied" when**:
1. ✅ Your AGENTS.md has ## Toyota Quality Loop section (DONE)
2. ✅ Your AGENTS.md is under 40KB hard max (DONE)
3. ⚠️ Your AGENTS.md is under 30KB target (CHECK STATUS ABOVE)

**Action required**: None if under 30KB. If over 30KB, consider trimming per guidance above.

---

**End of Handoff**
