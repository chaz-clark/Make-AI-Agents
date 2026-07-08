---
direction: deliver
status: parked
from_repo: Make-AI-Agents
to_repo: canvas-toolbox + all *-master repos
date_created: 2026-07-08
last_updated: 2026-07-08
trigger: repo-steward detects gap OR manual decision to standardize
---

# Handoff: Rebuild *-master AGENTS.md via canvas-toolbox Process

**To**: canvas-toolbox agent + 6 *-master repos
**From**: Make-AI-Agents (discovered during master repos audit)
**Purpose**: Rebuild all *-master AGENTS.md files using canvas-toolbox's make-AGENTS.md process to add Canvas-specific grounding

---

## Problem Statement

**Date discovered**: 2026-07-08 during master repos audit

**The gap**: The 6 *-master repos (cse450, ds250-onln, ds460, itm327, m119, mathcourses) have AGENTS.md files that were:
- Hand-written or scaffolded from older templates
- NOT generated using canvas-toolbox's make-AGENTS.md build process
- Missing Canvas-specific context that the build would provide

**What's missing**:
1. Canvas course topology (MASTER / BLUEPRINT / S1-S3 / SANDBOX structure)
2. Course IDs in frontmatter or Active Context
3. Module structure overview (if course is initialized)
4. Canvas-specific domain terms (assignments vs. quizzes vs. pages)
5. FERPA discipline sections (some have it, some don't)
6. Grading workflow context (if repo uses grading tools)

**Why it matters**:
- Agents working in *-master repos lack Canvas grounding
- make-AGENTS.md template has Canvas-aware sections
- canvas-toolbox build mixes template with `canvas-sync --init` knowledge
- Manually-written AGENTS.md files drift from canonical structure

---

## The canvas-toolbox AGENTS.md Build Process

**Location**: canvas-toolbox (needs verification of exact implementation)

**How it works** (expected, based on user statement):
1. User runs `canvas-sync --init` in a *-master repo
2. Sync pulls course structure from Canvas API (modules, assignments, topology)
3. canvas-toolbox extracts metadata:
   - Course ID(s)
   - Topology (MASTER/BLUEPRINT/sections)
   - Module count and structure
   - FERPA-sensitive paths (grading/ folders)
4. canvas-toolbox invokes make-AGENTS.md template
5. Template is **mixed with** extracted Canvas knowledge
6. Output: AGENTS.md with both canonical structure AND Canvas-specific context

**Example output sections** (expected):
```markdown
---
name: ds460-master-agents
metadata:
  canvas_course_id: 123456
  canvas_topology: MASTER + S1 + S2 + S3
  modules_count: 14
---

# ds460-master

Canvas LMS course management for DS 460.

## Course Topology

**Canvas structure**:
- MASTER (id: 123456) — source of truth, pushed to sections
- S1 (id: 123457) — Spring 2026 section 1
- S2 (id: 123458) — Spring 2026 section 2
- S3 (id: 123459) — Spring 2026 section 3

## FERPA Discipline

[Auto-generated based on grading/ folder detection]

## Module Structure

1. Week 1: Introduction to Big Data
2. Week 2: Spark Fundamentals
...
```

---

## Scope

**6 *-master repos** to rebuild:
1. cse450-master
2. ds250-onln-master
3. ds460-master (even though it's the current gold standard — it was hand-written)
4. itm327-master
5. m119-master
6. mathcourses-master

**Prerequisites per repo**:
- Canvas course must be initialized (`canvas-sync --init` already run)
- .env file with course IDs configured
- canvas-toolbox clone present and up-to-date

---

## Execution Plan

### Phase 1: Verify canvas-toolbox Build Exists (1 hour)

**Action**: Check if canvas-toolbox actually has this build process

**Commands**:
```bash
cd ~/Documents/GitHub/canvas-toolbox
grep -r "make-AGENTS\|make_AGENTS" .
ls lib/agents/ | grep -i agents
cat README.md | grep -i "AGENTS.md"
```

**Outcomes**:
- ✅ Build exists → proceed to Phase 2
- ❌ Build doesn't exist → park this handoff, note as "future enhancement"

### Phase 2: Backup Current AGENTS.md Files (15 minutes)

**Action**: Save current AGENTS.md files before regenerating

**Commands**:
```bash
for repo in cse450-master ds250-onln-master ds460-master itm327-master m119-master mathcourses-master; do
  cp ~/Documents/GitHub/$repo/AGENTS.md ~/Documents/GitHub/$repo/AGENTS.md.bak-2026-07-08
done
```

### Phase 3: Run Build Process Per Repo (2-3 hours)

**For each *-master repo**:

```bash
cd ~/Documents/GitHub/cse450-master

# Ensure canvas-toolbox is up-to-date
git -C canvas-toolbox pull

# Ensure course is initialized (already should be for most repos)
uv run python canvas-toolbox/lib/tools/canvas_sync.py --status

# Run make-AGENTS.md build (COMMAND TBD - depends on canvas-toolbox implementation)
# Expected: something like:
uv run python canvas-toolbox/lib/agents/build_agents_md.py --repo cse450-master

# Review generated AGENTS.md
git diff AGENTS.md

# Merge manual customizations from backup if needed
# (e.g., project-specific rules, instructor notes)

# Commit
git add AGENTS.md
git commit -m "Rebuild AGENTS.md via canvas-toolbox make-AGENTS process

- Generated using canvas-toolbox make-AGENTS.md template
- Mixed with Canvas course metadata from canvas-sync
- Preserves manual customizations (TODO: list specifics)

Addresses gap found in 2026-07-08 master repos audit."
```

### Phase 4: Audit Rebuilt AGENTS.md Files (1 hour)

**Check**:
- ✅ YAML frontmatter includes Canvas metadata (course IDs, topology)
- ✅ Course Topology section present with actual course structure
- ✅ Module Structure section (if course initialized)
- ✅ FERPA Discipline section matches grading/ folder presence
- ✅ Domain Terms section includes Canvas-specific terms
- ✅ Manual customizations preserved (instructor TODOs, project rules)

### Phase 5: Push Updates (30 minutes)

**For each repo**:
```bash
git push
```

---

## Integration with repo-steward

**New check**: "Canvas grounding present?"

**Steward should detect**:
1. Repo is a *-master repo (Canvas course management)
2. AGENTS.md exists but lacks Canvas metadata in frontmatter
3. AGENTS.md lacks ## Course Topology section
4. AGENTS.md lacks ## FERPA Discipline section (if grading/ folder present)

**Steward alert example**:
```markdown
## Medium Drift: cse450-master

**Issue**: AGENTS.md lacks Canvas-specific grounding
- Missing `canvas_course_id` in frontmatter
- Missing ## Course Topology section
- Missing ## Module Structure section

**Recommended action**: Rebuild AGENTS.md via canvas-toolbox make-AGENTS process
**Handoff**: See handoffs/HANDOFF_canvas-toolbox-agents-rebuild.md
```

---

## Risk Assessment

### Low Risk (Safe Actions)
- ✅ Backing up current AGENTS.md files
- ✅ Reviewing generated output before committing
- ✅ Running build in one repo as test

### Medium Risk (Requires Care)
- ⚠️ Overwriting hand-written AGENTS.md content
- ⚠️ Losing manual customizations (instructor notes, project-specific rules)
- ⚠️ Build process bugs (if canvas-toolbox build is immature)

### Mitigation
- Backup files before rebuild (Phase 2)
- Manual review of diffs (Phase 3)
- Start with one repo (cse450 or m119, not ds460 gold standard)
- Preserve manual sections via merge or re-add after generation

---

## Success Criteria

**This handoff is "delivered" when**:
1. ✅ canvas-toolbox build process verified to exist and work
2. ✅ At least 1 *-master repo rebuilt successfully (test case)
3. ✅ Generated AGENTS.md includes Canvas metadata
4. ✅ Manual customizations preserved or merged back

**This handoff is "complete" when**:
1. ✅ All 6 *-master repos rebuilt
2. ✅ repo-steward updated to check for Canvas grounding
3. ✅ Chaz reviews at least 3 rebuilt AGENTS.md files and confirms quality

---

## Philosophy: Tight Structure + Individuality

**Tight structure** (enforced by build):
- ✅ YAML frontmatter with Canvas metadata
- ✅ Required sections (## Course Topology, ## FERPA Discipline, ## Working Style, etc.)
- ✅ Kebab-case knowledge file references
- ✅ Canonical section ordering (per make-AGENTS.md)

**Individuality** (allowed per repo):
- ✅ Instructor notes and TODOs (## Active Context customizations)
- ✅ Project-specific rules (## Working Style → Project-specific rules)
- ✅ Domain terms unique to course (## Domain Terms)
- ✅ Existing tooling descriptions (course-specific scripts)
- ✅ Sister repos list (may differ per course)

**Merge strategy**: Generated sections + manual customizations
- Auto-generate: frontmatter, topology, FERPA, structure tree
- Preserve manual: Active Context instructor notes, project rules, custom tooling

---

## Parking Rationale

**Status**: Parked (not urgent)

**Why parked**:
1. Need to verify canvas-toolbox build exists (Phase 1 blocker)
2. Current AGENTS.md files are functional (not broken, just not optimal)
3. repo-steward implementation takes priority (will surface this gap automatically)
4. Can execute as follow-up sprint after steward is running

**Trigger to unpark**:
1. repo-steward detects Canvas grounding gap in weekly audit
2. Chaz decides to standardize all *-master repos
3. canvas-toolbox build confirmed to exist and work
4. One *-master repo needs fresh AGENTS.md (new course setup)

---

## Related Work

**Prior art**:
- make-AGENTS.md template (canonical structure)
- ds460-master AGENTS.md (hand-written gold standard, BUT lacks Canvas grounding)
- MASTER_REPOS_AUDIT.md (2026-07-08 — identified this gap)

**Dependencies**:
- canvas-toolbox make-AGENTS build process (needs verification)
- repo-steward implementation (will auto-detect this gap)

---

## Questions for canvas-toolbox Investigation

1. Does canvas-toolbox have a make-AGENTS.md build?
2. Where is it located? (lib/agents/build_agents_md.py? make_AGENTS.py?)
3. What's the invocation command?
4. What metadata does it extract from canvas-sync?
5. How does it merge template + Canvas knowledge?
6. Does it preserve manual sections or fully regenerate?

**Next action**: Run Phase 1 investigation when capacity allows.

---

**End of Handoff**
