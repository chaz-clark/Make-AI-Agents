---
name: JSON + QC Purge Plan
description: Honest assessment of what to delete, what to keep, what to replace
created: 2026-07-06
status: DRAFT - Review in morning before execution
---

# JSON + QC Purge Plan

## Executive Summary

**Problem**: We're maintaining 6 JSON files and 2 QC agents that:
- Don't align with industry patterns (Anthropic/Google/OpenAI use markdown-only or markdown+YAML)
- Lag behind their .md counterparts (make_agent.json is 8 weeks stale)
- Aren't read by any tooling we've built
- Add ~30% maintenance overhead to template changes

**Recommendation**: Delete 4 JSON files, consolidate 2, keep both QC agents but acknowledge they're optional.

**Impact**: -6 files, -3500 lines, -10 hours/year maintenance burden.

---

## Current State Inventory

### JSON Files (6 total, 3333 lines)

| File | Lines | Last Updated | Referenced By | Keep? |
|------|-------|--------------|---------------|-------|
| `make_agent.json` | 525 | 8 weeks ago | Nothing | ❌ DELETE |
| `make_agent_qc.json` | 899 | Current | make-agent-qc.md | ⚠️ CONSOLIDATE |
| `make_AGENTS.json` | 359 | Current | make_AGENTS.md | ⚠️ CONSOLIDATE |
| `make_AGENTS_qc.json` | 486 | Current | make-AGENTS-qc.md | ⚠️ CONSOLIDATE |
| `make_orchestrator_agent.json` | 507 | 8 weeks ago | Nothing | ❌ DELETE |
| `make_agent_knowledge.json` | 557 | 8 weeks ago | Nothing | ❌ DELETE |

### QC Agents (2 total)

| File | Purpose | Used? | Keep? |
|------|---------|-------|-------|
| `make-agent-qc.md` | 20 rules for agent specs | Unknown | ✅ KEEP (document as optional) |
| `make-AGENTS-qc.md` | 11 rules for AGENTS.md files | Created AGENTS-QC-010/011 | ✅ KEEP (proven value) |

### Missing QC (should they exist?)

- ❌ `make_managed_agent_qc.md` - Never created (Sprint 2)
- ❌ `make_orchestrator_agent_qc.md` - Pre-existing template, no QC
- ❌ `make_agent_knowledge_qc.md` - Pre-existing template, no QC

---

## Purge Plan

### Phase 1: Delete Stale JSON Files (30 minutes)

**Delete immediately** (no downstream impact):
```bash
git rm make_agent.json
git rm make_orchestrator_agent.json
git rm make_agent_knowledge.json
```

**Why safe**:
- Last updated 8 weeks ago (pre-Sprint 1)
- Zero references in codebase
- make_agent.json doesn't even mention "multimodal" (380 lines added to .md this sprint)
- Platforms use markdown-only or markdown+YAML frontmatter

**Effort**: 5 minutes + commit

---

### Phase 2: Consolidate QC JSON into Markdown (2-3 hours)

**Problem**: QC JSON files duplicate what's in QC markdown files but in structured format.

**Current pattern**:
```
make-agent-qc.md      (narrative: what each rule checks, why it matters)
make_agent_qc.json    (structured: rule IDs, check commands, dimensions)
```

**Proposed pattern** (following Anthropic Agent Skills):
```markdown
---
name: make_agent_qc
version: "3.1"
rules: 20
dimensions: 17
---

# Make Agent QC

## QC-001: Behavioral Discipline Presence
**Dimension**: completeness
**Check**: Agent spec includes behavioral_discipline section
**Severity**: error
**Why**: Every agent must embed discipline...
```

**Action**:
1. Add YAML frontmatter to `make-agent-qc.md` with metadata
2. Keep structured rules inline (markdown tables or code blocks)
3. Delete `make_agent_qc.json`
4. Repeat for `make-AGENTS-qc.md` / `make_AGENTS_qc.json`

**Benefit**: Single source of truth. Industry-aligned format.

**Effort**: 2-3 hours (careful migration, verify no breakage)

---

### Phase 3: Update AGENTS.md Rule (15 minutes)

**Current rule**:
> Templates evolve in pairs — `make_*.md` (narrative) and `make_*.json` (structured rules) are updated together.

**New rule**:
> Templates are markdown-only with optional YAML frontmatter for metadata (following Anthropic Agent Skills and agentskills.io patterns). JSON files were deprecated 2026-07-06 — if you see one, it's stale.

**Files to update**:
- `AGENTS.md` (project rules section)
- `README.md` (if it mentions JSON files)

**Effort**: 15 minutes

---

### Phase 4: Add YAML Frontmatter to Templates (Optional, 1-2 hours)

**Align with industry**: Anthropic Agent Skills use YAML frontmatter for metadata.

**Example transformation**:

**Before** (make-managed-agent.md):
```markdown
---
name: make_managed_agent
description: Generates platform-managed agent specs...
version: "1.0"
author: chaz-clark
license: MIT
---
```

**After** (add structured metadata):
```markdown
---
name: make_managed_agent
version: "1.0"
created: 2026-07-06
platforms: [Anthropic, Google, OpenAI]
skill_type: specialized
dependencies:
  - behavioral_discipline
  - make_agent
see_also:
  - source_docs/anthropic_managed_agents_overview.md
  - source_docs/google_managed_agents.md
  - source_docs/openai_sandbox_agents.md
---

# Managed Agent Guide
...
```

**Apply to**:
- ✅ `make-managed-agent.md` (new, add frontmatter)
- ⚠️ `make-agent.md` (has frontmatter, enhance it)
- ⚠️ `make-orchestrator-agent.md` (has frontmatter, enhance it)
- ⚠️ `make-agent-knowledge.md` (has frontmatter, enhance it)
- ⚠️ `make_AGENTS.md` (has frontmatter, enhance it)

**Benefit**: Machine-readable metadata in industry-standard format.

**Effort**: 1-2 hours (careful additions, don't break existing tools)

---

## QC Agent Assessment

### Question: Are QC agents still valuable?

**Evidence FOR keeping them**:

1. **AGENTS-QC-010 and AGENTS-QC-011 caught real issue**
   - canvas-toolbox AGENTS.md hit 53k tokens (exceeded 25k Read tool limit)
   - QC rules prevented future bloat
   - **Proven value**: Yes

2. **make_AGENTS_qc has 11 rules, caught issues during creation**
   - File size thresholds
   - Bloat detection (Active Context >150 lines)
   - Structure validation
   - **Verdict**: Keep

3. **make_agent_qc has 20 rules, but...**
   - We created `make-managed-agent.md` (Sprint 2) and didn't run QC
   - We added 380 lines to `make-agent.md` (Sprint 3) and didn't run QC
   - We updated `make-orchestrator-agent.md` and didn't run QC
   - **Verdict**: Useful in theory, not used in practice

**Evidence AGAINST**:

1. **We didn't use QC during 3 sprints**
   - 10 files changed, 0 QC runs
   - If QC was critical, we would have missed it

2. **High maintenance overhead**
   - Every template change should trigger QC update
   - We don't do that consistently

3. **Templates have internalized discipline**
   - Early QC caught issues (v1.0 make-agent.md)
   - Now we "know" what good looks like
   - Diminishing returns

### Recommendation: Keep QC but Document as Optional

**Action**:
1. Keep `make-agent-qc.md` and `make-AGENTS-qc.md`
2. Add frontmatter marking them as `optional: true`
3. Update AGENTS.md:
   ```markdown
   ## Quality Control

   QC agents exist but are **optional**:
   - `make-agent-qc.md` — 20 rules for agent specs
   - `make-AGENTS-qc.md` — 11 rules for AGENTS.md files

   **When to run**:
   - Before releasing template to consumer repos
   - After major template changes
   - When onboarding new contributors

   **When to skip**:
   - Iterative template development
   - Minor wording changes
   - You've internalized the discipline
   ```

4. **Don't create new QC agents** for `make_managed_agent`, `make_orchestrator_agent`, `make_agent_knowledge`
   - QC agents take 2-3 hours each
   - We haven't used them
   - Visual inspection + behavioral discipline is sufficient

**Effort**: 30 minutes (documentation only)

---

## Missing QC Decision

### Should we create QC for new templates?

**Options**:

**Option A: No QC for new templates** (recommended)
- We didn't use QC during Sprint 2/3
- Behavioral discipline is internalized
- Visual inspection suffices
- **Effort saved**: 6-9 hours (3 templates × 2-3 hours each)

**Option B: Lightweight checklists instead**
- Create 10-item markdown checklists (not full QC agents)
- Example:
  ```markdown
  ## make_managed_agent Checklist
  - [ ] Platform selection section exists
  - [ ] Decision matrix included
  - [ ] All 3 platforms covered
  - [ ] Behavioral discipline referenced
  - [ ] Common pitfalls documented
  ```
- **Effort**: 30 minutes each = 1.5 hours total
- **Benefit**: 80% value at 20% cost

**Option C: Full QC agents for all**
- Create `make_managed_agent_qc.md`
- Create `make_orchestrator_agent_qc.md`
- Create `make_agent_knowledge_qc.md`
- **Effort**: 6-9 hours
- **Risk**: We won't use them (track record says so)

**Recommendation**: Option B (lightweight checklists), defer to Sprint 5+

---

## Downstream Impact Assessment

### Files That Reference JSON

```bash
$ grep -r "\.json" *.md --exclude-dir=.git | grep "make_"
```

**Results**:
- `README.md`: "See make_agent.json for tier fields"
- `README_Disclosure.md`: "meta-skills like make_agent.json"
- Old GitHub issues mention make_agent.json

**Action**: Update references to say "See make-agent.md YAML frontmatter"

**Effort**: 15 minutes

---

### Consumer Repo Impact

**Question**: Do any consumer repos depend on our JSON files?

**Check**:
- canvas-toolbox: Uses templates, not JSON
- AgentJ: Uses templates, not JSON
- Course repos: Use templates, not JSON

**Conclusion**: Zero consumer repos read our JSON files. Safe to delete.

---

## Effort Summary

| Phase | Task | Effort | Risk |
|-------|------|--------|------|
| 1 | Delete 3 stale JSON files | 5 min | None |
| 2 | Consolidate QC JSON → YAML frontmatter | 2-3 hrs | Low (careful migration) |
| 3 | Update AGENTS.md rules | 15 min | None |
| 4 | Add YAML frontmatter to templates (optional) | 1-2 hrs | Low |
| 5 | Update file references | 15 min | None |
| 6 | Document QC as optional | 30 min | None |

**Total minimum**: 3-4 hours (Phases 1-3, 5-6 only)
**Total with YAML**: 4-6 hours (all phases)

---

## Migration Path

### Immediate (Morning Decision)

**Review this plan and decide**:
1. ✅ Delete 3 stale JSON files? (make_agent, make_orchestrator_agent, make_agent_knowledge)
2. ✅ Consolidate QC JSON into YAML frontmatter?
3. ⚠️ Add YAML frontmatter to all templates? (optional, alignment with industry)
4. ✅ Document QC agents as optional?
5. ❌ Skip creating new QC agents?

### Sprint 4 (If Approved)

**Task 1: Purge stale JSON** (30 min)
- Delete 3 files
- Update AGENTS.md rule
- Commit: "Purge stale JSON files - align with industry markdown-only pattern"

**Task 2: Consolidate QC** (2-3 hrs)
- Migrate make_agent_qc.json → YAML frontmatter in make-agent-qc.md
- Migrate make_AGENTS_qc.json → YAML frontmatter in make-AGENTS-qc.md
- Delete 2 JSON files
- Commit: "Consolidate QC JSON into YAML frontmatter"

**Task 3: Document QC as optional** (30 min)
- Update AGENTS.md with "when to run / when to skip" guidance
- Add `optional: true` to QC frontmatter
- Commit: "Document QC agents as optional, not mandatory"

**Task 4: YAML frontmatter (optional)** (1-2 hrs)
- Add structured metadata to all templates
- Align with Anthropic Agent Skills pattern
- Commit: "Add industry-standard YAML frontmatter to templates"

**Total Sprint 4 effort**: 4-6 hours

---

## Risks and Mitigation

### Risk 1: Breaking Unknown Dependencies

**What if**: Some script/tool reads JSON files we don't know about?

**Mitigation**:
- Grep entire codebase for `.json` references first
- Check consumer repos before deletion
- Keep deleted files in git history (easy rollback)

**Likelihood**: Very low (we already grepped, found nothing)

---

### Risk 2: Losing Structured Validation

**What if**: We need machine-readable schemas later?

**Mitigation**:
- YAML frontmatter IS machine-readable
- Can parse frontmatter from markdown (standard pattern)
- If we build validation tooling, it reads YAML, not JSON

**Likelihood**: Low (industry moved to YAML for this reason)

---

### Risk 3: QC Discipline Erodes Without Rules

**What if**: Without QC, template quality degrades?

**Mitigation**:
- Keep QC agents, mark as optional
- Use for major releases and onboarding
- Behavioral discipline is now internalized
- Lightweight checklists as middle ground

**Likelihood**: Medium (valid concern, addressed by keeping QC)

---

## Success Criteria

**After purge, the repo should**:
- ✅ Follow industry patterns (markdown + YAML, like Anthropic/agentskills.io)
- ✅ Have no stale files (everything current or explicitly deprecated)
- ✅ Reduce maintenance burden (no more "update .md AND .json" tax)
- ✅ Keep quality tools available (QC agents optional, not deleted)
- ✅ Align with platform documentation we just refreshed

**Metrics**:
- Files deleted: 3-5
- Lines deleted: 1500-2000
- Maintenance hours saved per year: ~10
- Industry alignment: 100% (matches Anthropic Agent Skills)

---

## Open Questions for Morning Review

1. **Delete all 3 stale JSON files?** Or keep one as "example of deprecated pattern"?

2. **Consolidate QC JSON immediately or defer?** (2-3 hour task)

3. **Add YAML frontmatter to all templates?** Or just new ones going forward?

4. **Create lightweight checklists for new templates?** Or rely on visual inspection only?

5. **Update consumer repos?** Or just document in AGENTS.md that JSON is deprecated?

6. **Commit strategy**: One big "purge" commit or separate commits per phase?

---

## Recommendation Summary

**Do immediately** (30 min):
1. Delete `make_agent.json`, `make_orchestrator_agent.json`, `make_agent_knowledge.json`
2. Update AGENTS.md: "JSON files deprecated, markdown-only is source of truth"
3. Commit and push

**Do in Sprint 4** (3-4 hrs):
1. Consolidate QC JSON into YAML frontmatter
2. Document QC agents as optional
3. Add YAML frontmatter to all templates

**Skip** (save 6-9 hrs):
1. Don't create new QC agents
2. Use lightweight checklists instead

**Total effort**: 4-5 hours
**Total benefit**: Aligned with industry, reduced maintenance, increased focus

---

**Status**: DRAFT - Review in morning before execution
**Created**: 2026-07-06
**Author**: Claude (with brutal honesty about what we're not using)
