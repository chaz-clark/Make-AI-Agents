---
direction: deliver
status: delivered
from_repo: Make-AI-Agents
to_repos: All repos with AGENTS.md files
date_created: 2026-07-09
last_updated: 2026-07-09
trigger: AGENTS-QC-010 threshold update (Issue #19 fixed in df9d833)
priority: low
---

# Handoff: AGENTS.md Size Threshold Update

**To**: All repos consuming Make-AI-Agents AGENTS.md standard
**From**: Make-AI-Agents
**Purpose**: Notify of tightened AGENTS.md size thresholds to match actual tool auto-include behavior

---

## What Changed

**AGENTS-QC-010 thresholds updated** (make-AGENTS.md Principle #2: Concise):

| Threshold | Old Value | New Value |
|---|---|---|
| **Soft warn** | 1200 lines / 12k tokens | **800 lines / 8k tokens** |
| **Hard flag** | 25k tokens | **1200 lines / 12k tokens** |
| **Technical limit** | 25k tokens | **25k tokens** (Read-tool cap — separate concern) |

**Commit**: df9d833 (2026-07-09)
**Issue**: #19 (closed)

---

## Why This Matters

**Problem discovered**: AGENTS.md files passing the old thresholds (under 25k tokens) weren't being auto-included by Claude Code at session start when they exceeded ~12-16k tokens.

**Impact**: Agents didn't read AGENTS.md at session start, causing them to violate documented patterns (e.g., P-008 commit-push-together, project-specific rules) because the file wasn't in their auto-context.

**Evidence**: Real AGENTS.md at 553 lines / ~15.8k tokens showed "contents too large to include" and agent violated documented P-008 six times despite clear documentation in AGENTS.md:182 and behavioral-discipline.md.

**The fix**: Hard flag now matches the **auto-include limit** (what determines whether agents see patterns by default), not just the Read-tool technical limit.

---

## Action Required (Optional, But Recommended)

### 1. Check Your AGENTS.md Size

```bash
# Line count
wc -l AGENTS.md

# Rough token estimate (1 token ≈ 4 chars)
wc -c AGENTS.md | awk '{print int($1/4) " tokens (rough estimate)"}'
```

**Thresholds**:
- **Under 800 lines / ~8k tokens**: ✅ Well within auto-include buffer
- **800-1200 lines / 8k-12k tokens**: ⚠️ Soft warn — consider trimming
- **Over 1200 lines / ~12k tokens**: 🔴 Hard flag — likely NOT auto-included at session start

### 2. If You Exceed Thresholds, Consider Trimming

**Common bloat sources** (from Issue #19):

#### High Bloat Risk
1. **External System Lessons** — Accumulates indefinitely
   - Keep only 5-10 most recent/relevant lessons inline
   - Archive older lessons to `knowledge/learned/external-system-lessons-archive.md`

2. **Tool/Command Catalogs** — Inline documentation for every tool
   - Replace with directory listing: "See `lib/tools/` for full catalog"
   - Keep only 3-5 most-used tools with one-line descriptions
   - Full tool docs belong in docstrings or README

#### Medium Bloat Risk
3. **Active Context** — Dated entries accumulate
   - Remove entries older than 30-60 days
   - Keep only current in-flight work
   - AGENTS-QC-011 flags >5 dated entries or >150 lines

4. **Detailed Examples** — Multi-paragraph workflow examples
   - Move to README.md or dedicated workflow docs
   - Keep only brief snippets inline
   - Link to full examples

5. **Historical Patterns** — "How we used to do X vs. now"
   - Remove unless directly relevant
   - Document current pattern only

#### Low Bloat Risk (But Check)
6. **Working Style Boilerplate** — Copying discipline principles
   - Reference `knowledge/behavioral-discipline.md` instead of duplicating
   - Keep only repo-specific customizations inline
   - Max 2-3 sentence principle summaries

### 3. No Immediate Action Required

This is **not an urgent fix**. Your AGENTS.md continues to work as-is. But if you notice:
- Agents violating documented patterns
- "Contents too large to include" at session start
- AGENTS.md exceeding 1200 lines

...then trimming per the guidance above will restore auto-include behavior.

---

## Scope: Affected Repos

**Confirmed Make-AI-Agents consumers** (6 *-master repos):
- cse450-master
- ds250-onln-master
- ds460-master
- itm327-master
- m119-master
- mathcourses-master

**Sister repos**:
- canvas-toolbox
- gh-issues-agent
- handoff

**Other repos with AGENTS.md** (may or may not follow Make-AI-Agents standard):
- agentj
- repo-steward
- ngai-n8n
- ds250-class-code
- Apache_Airflow
- m119-site
- itm327_anskey
- your-project
- DS250-Course-Polars
- clarkprep
- google-calendar-mcp
- life-pm
- fullbright-fa27

**How to check if this applies to you**: If your AGENTS.md references `make-AGENTS.md` or `knowledge/behavioral-discipline.md`, you're consuming Make-AI-Agents standards and this update applies.

---

## Philosophy: Documentation That Isn't Read Doesn't Guide Behavior

The 25k threshold was about "can this be read in one Read call" — still valid for technical limits. But the **auto-include threshold** is what determines whether agents follow documented patterns **by default**.

If AGENTS.md is too large to auto-include, agents won't see your Working Style, Active Context, or project-specific rules at session start. They have to proactively Read it — and they won't unless prompted.

The hard flag should match the limit that matters for "reads first when working in a project."

---

## Success Criteria

**This handoff is "applied" when**:
1. You've checked your AGENTS.md size
2. If over threshold, you've trimmed or decided to leave as-is with awareness
3. Your AGENTS.md is within auto-include limits (or you're okay with manual Read workflow)

**This handoff is "complete" when**:
- All consumer repos have acknowledged the change
- Any AGENTS.md files exceeding 12k tokens have been reviewed for trimming

---

## Resources

**Issue**: https://github.com/chaz-clark/Make-AI-Agents/issues/19
**Commit**: df9d833 in Make-AI-Agents
**Updated file**: `make-AGENTS.md` line 152 (Principle #2: Concise)

**Trimming guidance**: See "Common bloat sources" in Issue #19 or above section

---

## Questions or Issues?

If you're unsure whether to trim or how to trim:
1. Check your AGENTS.md line count vs. thresholds
2. Review "Common bloat sources" above
3. Trimmed content isn't lost — it moves to README, CHANGELOG, or knowledge/ archives
4. AGENTS.md should be **project context**, not exhaustive documentation

---

**End of Handoff**
