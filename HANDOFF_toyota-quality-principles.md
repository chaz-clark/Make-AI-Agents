# Handoff: Elevate Toyota Quality Principles in AI Agent Work

**To**: Make-AI-Agents core framework
**From**: canvas-toolbox (Chaz Clark)
**Date**: 2026-07-12
**Type**: Framework Enhancement
**Priority**: High

---

## Executive Summary

After building offline mode implementation for Canvas Toolbox, we discovered that three Toyota Production System principles form a **quality loop** that prevents defects in AI agent development work:

1. **Genchi Gembutsu** (現地現物) - Go and See / Verify with Real Data
2. **Jidoka** (自働化) - Built-in Quality / Stop on Defect
3. **Poka-yoke** (ポカヨケ) - Mistake-Proofing / Design Out Errors

These should be **elevated to core behavioral principles** in the Make-AI-Agents framework, not just referenced in passing.

---

## Problem Statement

**Current state**: AI agents reference Toyota principles occasionally but don't enforce them systematically.

**Observed failures** (canvas-toolbox examples):
- Agent assumed .imscc format matched documentation (didn't Genchi Gembutsu)
- Agent deferred fixing test failures to "later" (didn't Jidoka)
- Agent required manual validation steps that could be automated (didn't Poka-yoke)

**Impact**: Defects discovered late, wasted effort, faculty frustration when tools fail.

---

## The Quality Loop

These three principles work together to prevent, detect, and verify quality:

```
         ┌─────────────┐
         │ Poka-yoke   │ ← PREVENT: Can't make mistake
         │ (Prevent)   │
         └──────┬──────┘
                │
                ↓
         ┌─────────────┐
         │ Jidoka      │ ← DETECT: Catch defect immediately
         │ (Detect)    │
         └──────┬──────┘
                │
                ↓
         ┌─────────────┐
         │ Genchi      │ ← VERIFY: Check with real data
         │ Gembutsu    │
         │ (Verify)    │
         └──────┬──────┘
                │
                ↓
         (Back to Prevent - continuous improvement)
```

**Why these three specifically**:
- Genchi Gembutsu without Jidoka → Verify after damage done
- Jidoka without Poka-yoke → Detect same mistakes repeatedly
- Poka-yoke without Genchi Gembutsu → Prevent wrong things

---

## Principle Details

### 1. Genchi Gembutsu (現地現物) - Go and See

**Meaning**: "Real location, real thing" - Don't assume, verify with actual data

**AI Agent Applications**:
- Test with REAL user data, not synthetic fixtures
- When uncertain about file format, download and examine actual file
- Verify behavior in real environment (e.g., Canvas sandbox), don't trust docs alone
- Read actual code before claiming to understand it (aligns with P-001)

**Canvas-toolbox example**:
```python
# ❌ WRONG (assumption):
# "Canvas .imscc uses standard IMS CC identifiers"

# ✅ CORRECT (Genchi Gembutsu):
# Downloaded real .imscc from course 145706
# Examined actual identifiers: "g" + 32 hex chars (Canvas-specific)
# Documented in lib/agents/knowledge/imscc_format_knowledge.md
```

**Behavioral trigger**: When agent says "probably" or "should" → STOP and verify

---

### 2. Jidoka (自働化) - Built-in Quality / Stop on Defect

**Meaning**: "Automation with human intelligence" - Build quality in, stop when defect detected

**AI Agent Applications**:
- Write tests WITH code, not after
- Red tests block progress - fix immediately, don't defer
- Validation runs automatically (not manual step)
- Can't merge/export with errors (blocked by design)

**Canvas-toolbox example**:
```python
# offline_export.py - Jidoka in action

def export_to_imscc(source_dir, output_path):
    # Build .imscc
    build_imscc(source_dir, temp_path)

    # Validate BEFORE writing output (built-in quality)
    errors, warnings = validate_imscc(temp_path)

    if errors:
        # STOP - can't export broken file (Jidoka)
        print(f"✗ Validation failed: {errors}")
        return False  # Export blocked

    # Only write if valid
    shutil.copy(temp_path, output_path)
    return True
```

**Aligns with**: AGENTS.md P-003 "Stop on Defect"

**Behavioral trigger**: When agent says "we'll fix this later" → STOP and fix now

---

### 3. Poka-yoke (ポカヨケ) - Mistake-Proofing

**Meaning**: Design systems so mistakes can't happen (error-proofing)

**AI Agent Applications**:
- Validation runs automatically (no manual step to forget)
- Pre-commit hooks catch errors before commit
- Type hints catch errors at write-time
- Git-ignore patterns prevent PII commits
- Can't merge with red tests (CI blocks it)

**Canvas-toolbox example**:
```python
# .git/hooks/pre-commit (Poka-yoke)
#!/bin/bash
# Can't commit with failing unit tests
pytest tests/unit/ --maxfail=1 || exit 1

# Can't commit PII files
if git diff --cached --name-only | grep -q "\.deid_master\.csv"; then
    echo "ERROR: Attempting to commit FERPA Zone 2 file"
    exit 1
fi
```

**Behavioral trigger**: When manual steps required → Design them out

---

## Proposed Framework Changes

### 1. Add to `AGENTS.md` Template (make_AGENTS)

**New section** (after Behavioral Discipline):

```markdown
## Quality Discipline (Toyota Production System)

AI agents working in this repo must follow three core quality principles:

### 1. Genchi Gembutsu (現地現物) - Go and See

**Don't assume, verify with real data:**
- Test with REAL user data, not synthetic fixtures
- When uncertain about format, examine actual files
- Verify in real environment, don't trust docs alone
- Read actual code before claiming understanding

**Behavioral trigger**: When you catch yourself saying "probably" or "should" → STOP and verify

### 2. Jidoka (自働化) - Built-in Quality / Stop on Defect

**Build quality in, stop when defect detected:**
- Write tests WITH code, not after
- Red tests block progress - fix immediately, don't defer
- Validation runs automatically (not manual step)
- Can't merge/export with errors (blocked by design)

**Behavioral trigger**: When you want to say "we'll fix this later" → STOP and fix now

**Aligns with**: P-003 Stop on Defect

### 3. Poka-yoke (ポカヨケ) - Mistake-Proofing

**Design so mistakes can't happen:**
- Automate validation (no manual steps)
- Use pre-commit hooks to catch errors
- Type hints catch errors at write-time
- Block operations that would create defects

**Behavioral trigger**: When manual verification required → Design it out

---

## Quality Loop

These three work together:

```
Prevent (Poka-yoke) → Detect (Jidoka) → Verify (Genchi Gembutsu)
         ↑______________________________________________|
```

When you find a defect:
1. **Fix it** (Jidoka - stop and correct)
2. **Verify the fix** (Genchi Gembutsu - test with real data)
3. **Prevent recurrence** (Poka-yoke - add automated check)
```

### 2. Add to Behavioral Discipline

**In `knowledge/behavioral_discipline.md`**, add as **Principle 11**:

```markdown
### P-011: Toyota Quality Loop (Override: NEVER)

**The Rule**: Every task must complete the quality loop: Prevent → Detect → Verify

**Prevent** (Poka-yoke):
- Design validation into tools (can't export broken .imscc)
- Use pre-commit hooks (can't commit failing tests)
- Type hints and linting (catch errors at write-time)

**Detect** (Jidoka):
- Red tests block progress
- Validation runs before dangerous operations
- CI blocks merges with errors

**Verify** (Genchi Gembutsu):
- Test with real user data
- Verify in real environment
- Don't trust documentation alone

**Examples**:
- ❌ "Tests are failing but I'll fix them later" → Violates Jidoka
- ❌ "Should work based on docs" → Violates Genchi Gembutsu
- ❌ "User needs to remember to validate" → Violates Poka-yoke
- ✅ "Export blocked until validation passes" → Completes loop

**This is a NO-OVERRIDE principle** - violating the quality loop creates technical debt.
```

### 3. Add to Working Style Guidelines

**In global CLAUDE.md**, add to "Working style" section:

```markdown
### 5. Toyota Quality Loop

**Every task completes**: Prevent → Detect → Verify

Before claiming "done":
- [ ] **Poka-yoke**: Automated validation added (no manual steps)
- [ ] **Jidoka**: Tests pass (no deferred fixes)
- [ ] **Genchi Gembutsu**: Verified with real data (not assumptions)

Don't pass defects forward - fix at the source.
```

---

## Canvas-Toolbox Implementation

We've already implemented this in `docs/offline_mode_sprints.md`:

**Quality Discipline section** includes:
- Three principles explained with examples
- Per-sprint checklist (green before done, regression first, real data)
- Test pyramid (unit/integration/E2E)
- CI/CD integration

**Sprint 4 risk reduction**:
- `validate_imscc.py` tool (Jidoka - built-in validation)
- Failure injection tests (Genchi Gembutsu - test with known bad .imscc)
- Auto-validation in `offline_export.py` (Poka-yoke - can't export broken files)

**Faculty-facing impact**:
- Tools that work reliably (quality built in)
- Clear error messages when validation fails
- Confidence before Canvas upload

---

## Benefits

**For AI Agents**:
- Clear behavioral triggers ("probably" → verify)
- Systematic quality approach (not ad-hoc)
- Aligns with existing P-003 (Stop on Defect)

**For Users**:
- Fewer broken deliverables
- Faster feedback (shift-left validation)
- Trust in tools

**For Framework**:
- Quality becomes default behavior
- Elevates Toyota principles from "nice to have" to "core discipline"
- Complements existing Ten Principles

---

## Implementation Priority

**Phase 1** (Immediate):
- [x] Document in canvas-toolbox (DONE - `docs/offline_mode_sprints.md`)
- [ ] Add to canvas-toolbox AGENTS.md (Quality Discipline section)
- [ ] Update cb_init template (faculty repos get quality-conscious AGENTS.md)

**Phase 2** (Handoff to Make-AI-Agents):
- [ ] Add to make_AGENTS template (Quality Discipline section)
- [ ] Add P-011 to behavioral_discipline.md
- [ ] Add to global CLAUDE.md guidelines
- [ ] Update examples in handoff/examples/

**Phase 3** (Ecosystem):
- [ ] Validate against other Make-AI-Agents consumers
- [ ] Gather feedback on behavioral triggers
- [ ] Refine based on real-world usage

---

## Success Criteria

**Within canvas-toolbox**:
- ✅ Sprint plan includes quality discipline
- ✅ Sprint 4 implements all three principles
- [ ] AGENTS.md includes Quality Discipline section
- [ ] Faculty repos (via cb_init) get quality-conscious defaults

**Within Make-AI-Agents**:
- [ ] P-011 added to behavioral_discipline.md
- [ ] make_AGENTS template includes Quality Discipline section
- [ ] Global CLAUDE.md includes Toyota Quality Loop

**Behavioral change**:
- Agents catch themselves saying "probably" and verify instead
- Agents stop on red tests instead of deferring
- Agents design validation into tools, not as afterthought

---

## Related Work

- **Existing alignment**: P-003 "Stop on Defect" already maps to Jidoka
- **Complements**: P-001 "Read Before Claiming" maps to Genchi Gembutsu
- **New coverage**: Poka-yoke (mistake-proofing) is currently implicit, should be explicit

---

## Questions for Make-AI-Agents Team ✅ ANSWERED

1. **Should P-011 be NO-OVERRIDE** (like P-001, P-003, P-007, P-010)? → ✅ **YES - NO-OVERRIDE**
2. **Should "Toyota Quality Loop" be in every AGENTS.md**, or only for repos with quality-critical work? → ✅ **YES - Every AGENTS.md** (agents should always work with these in mind)
3. **How to surface behavioral triggers in Claude Code UI?** → ✅ **Add to user profile** (~/.claude/memory/user_chaz.md)

---

## Appendix: Canvas-Toolbox Evidence

**Files demonstrating quality loop**:
- `docs/offline_mode_sprints.md` - Quality Discipline section (lines 510-589)
- `lib/agents/knowledge/imscc_format_knowledge.md` - Genchi Gembutsu (documented actual .imscc structure)
- Sprint 4 plan - Jidoka (validate_imscc.py blocks export on errors)
- Sprint 4 plan - Poka-yoke (automated validation, pre-commit hooks)

**Defects prevented**:
- Human-readable identifiers (would cause silent Canvas import failure)
- Missing timezone in dates (would cause time-shift bugs)
- Broken file references (would cause missing images)
- Date constraint violations (would cause Canvas import error)

All caught by validator BEFORE Canvas upload.

---

## Contact

Chaz Clark
canvas-toolbox maintainer
chaz@example.com (replace with actual)

Ready to discuss implementation details or provide additional examples.
