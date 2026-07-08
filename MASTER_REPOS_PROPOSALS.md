# Master Repos AGENTS.md Update Proposals

**Date**: 2026-07-08
**Context**: Following knowledge folder audit and file copying
**Status**: Ready for review and implementation

---

## Summary of Actions Taken

### ✅ Completed: Knowledge File Distribution

**Phase 1**: Created missing knowledge folders
- ✅ `cse450-master/knowledge/learned/` created

**Phase 2**: Copied `behavioral-discipline.md` to all repos
- ✅ cse450-master
- ✅ ds250-onln-master
- ✅ itm327-master
- ✅ m119-master
- ✅ mathcourses-master

**Phase 3**: Created missing `learned/` folders
- ✅ ds250-onln-master/knowledge/learned/

**Phase 4**: Copied kebab-case knowledge files to itm327-master
- ✅ hermes-comparison.md
- ✅ json-to-yaml-migration.md
- ✅ mcp-integration-patterns.md
- ✅ source-docs-index.md

---

## Repo-Specific AGENTS.md Update Proposals

### 1. cse450-master

**Current Issue**: References Make-AI-Agents clone for behavioral discipline instead of local knowledge/

**Lines to Update**:

**Line 43** (Sister Repos table):
```markdown
CURRENT:
| `Make-AI-Agents/` | Agent-authoring toolkit; source of the Working-Style behavioral discipline | `make_*.md`/`.json` generators at root, `knowledge/behavioral_discipline.md` |

PROPOSED:
| `Make-AI-Agents/` | Agent-authoring toolkit; agent spec templates | `make_*.md` generators at root, templates for agent specs + AGENTS.md |
```

**Line 49** (Working Style section):
```markdown
CURRENT:
This project follows the behavioral discipline defined in `Make-AI-Agents/knowledge/behavioral_discipline.md` — the discipline file lives inside the `Make-AI-Agents/` clone at this repo's root (a gitignored standalone clone of `chaz-clark/Make-AI-Agents`). To refresh the discipline: `git -C Make-AI-Agents pull`. **Read that file before doing non-trivial work in this repo.**

PROPOSED:
This project follows the behavioral discipline defined in `knowledge/behavioral-discipline.md` — the 10 principles + 5 interaction patterns sourced from Make-AI-Agents. **Read that file before doing non-trivial work in this repo.**
```

**Rationale**:
- Now that `knowledge/behavioral-discipline.md` exists locally, reference it directly
- Removes dependency on Make-AI-Agents clone being present
- Uses kebab-case filename
- Simplifies the working style description

**Additional Recommendation**:
Consider adding these sections (following ds460-master gold standard):
- `## Handoff document recognition` (if using handoff convention)
- `## Learning loop` (points to knowledge/learned/)

---

### 2. ds250-onln-master

**Current Issue**: Unknown (file not read yet), but likely references snake_case knowledge files

**Action Required**: Read full AGENTS.md to check for:
1. References to `behavioral_discipline.md` (should be `behavioral-discipline.md`)
2. Presence of `## Learning loop` section
3. YAML frontmatter presence
4. Knowledge file reference patterns

**Tentative Proposal** (pending full read):
```markdown
# Add to Working Style section or as standalone section:

## Learning loop

Lessons learned during agent sessions are distilled into `knowledge/learned/` — structured markdown following P-009 (Hansei + Yokoten). Future invocations read these alongside core knowledge files.
```

**File to check**: `~/Documents/GitHub/ds250-onln-master/AGENTS.md` (37KB)

---

### 3. ds460-master

**Status**: ✅ NO CHANGES NEEDED

**Rationale**: This repo is the **reference implementation**:
- ✅ YAML frontmatter
- ✅ Proper section structure
- ✅ Kebab-case knowledge references
- ✅ `## Handoff document recognition` section
- ✅ `## Learning loop` section
- ✅ `knowledge/behavioral-discipline.md` referenced correctly
- ✅ Last updated: 2026-07-08 (today!)

This is the **gold standard** for other repos to follow.

---

### 4. itm327-master

**Current Issue**: Likely references snake_case knowledge files extensively

**Action Required**: Read full AGENTS.md to check for:
1. References to snake_case knowledge files:
   - `behavioral_discipline.md` → `behavioral-discipline.md`
   - `hermes_comparison.md` → `hermes-comparison.md`
   - `json_to_yaml_migration.md` → `json-to-yaml-migration.md`
   - `mcp_integration_patterns.md` → `mcp-integration-patterns.md`
   - `source_docs_index.md` → `source-docs-index.md`
2. YAML frontmatter presence
3. Section structure compliance

**Expected Changes**: Bulk find-replace of knowledge file references

**Execution Strategy**:
```bash
# In itm327-master repo
cd ~/Documents/GitHub/itm327-master
# Find all references to old snake_case files
grep -n "behavioral_discipline\|hermes_comparison\|json_to_yaml\|mcp_integration\|source_docs_index" AGENTS.md
```

**Proposed Updates**:
- Replace all `behavioral_discipline.md` → `behavioral-discipline.md`
- Replace all `hermes_comparison.md` → `hermes-comparison.md`
- Replace all `json_to_yaml_migration.md` → `json-to-yaml-migration.md`
- Replace all `mcp_integration_patterns.md` → `mcp-integration-patterns.md`
- Replace all `source_docs_index.md` → `source-docs-index.md`

**File to check**: `~/Documents/GitHub/itm327-master/AGENTS.md` (29KB)

---

### 5. m119-master

**Current Issue**: Likely references `behavioral_discipline.md` (snake_case)

**Action Required**: Read full AGENTS.md to check for:
1. References to `behavioral_discipline.md` → update to `behavioral-discipline.md`
2. Presence of `## Learning loop` section
3. YAML frontmatter
4. Knowledge folder structure description

**Tentative Proposal**:
```markdown
# Update Working Style section reference:

CURRENT (expected):
knowledge/behavioral_discipline.md

PROPOSED:
knowledge/behavioral-discipline.md
```

**File to check**: `~/Documents/GitHub/m119-master/AGENTS.md` (20KB)

---

### 6. mathcourses-master

**Current Issue**: Minimal knowledge folder, AGENTS.md likely minimal or references external sources

**Action Required**: Read full AGENTS.md to check for:
1. Whether it references knowledge files at all
2. If it has a `## Working Style` section
3. YAML frontmatter presence
4. Whether it needs a `## Learning loop` section added

**Tentative Proposal**: Add Working Style section if missing:
```markdown
## Working Style

This project follows the behavioral discipline defined in `knowledge/behavioral-discipline.md` — the 10 principles + 5 interaction patterns from the Make-AI-Agents toolkit. **Read that file before doing non-trivial work in this repo.**

The four no-override principles — **P-001 Read Before Claiming, P-003 Stop on Defect, P-007 Pull Don't Push, P-010 Respect Intent** — apply unconditionally; the other six (P-002, P-004, P-005, P-006, P-008, P-009) have documented override conditions in the discipline file.

## Learning loop

Lessons learned during agent sessions are distilled into `knowledge/learned/` — structured markdown following P-009 (Hansei + Yokoten). Future invocations read these alongside core knowledge files.
```

**File to check**: `~/Documents/GitHub/mathcourses-master/AGENTS.md` (12KB)

---

## Execution Plan for AGENTS.md Updates

### Step 1: Read All AGENTS.md Files (10 minutes)

For each repo (excluding ds460):
```bash
# Read and analyze
cat ~/Documents/GitHub/cse450-master/AGENTS.md
cat ~/Documents/GitHub/ds250-onln-master/AGENTS.md
cat ~/Documents/GitHub/itm327-master/AGENTS.md
cat ~/Documents/GitHub/m119-master/AGENTS.md
cat ~/Documents/GitHub/mathcourses-master/AGENTS.md
```

### Step 2: Generate Specific Edit Commands (15 minutes)

For each file, create specific `Edit` tool calls with:
- `old_string`: exact text from file
- `new_string`: kebab-case corrected version
- Context: enough surrounding text to make match unique

### Step 3: Execute Edits (20 minutes)

Apply edits one repo at a time, verify after each.

### Step 4: Commit Per Repo (30 minutes)

For each repo:
```bash
cd ~/Documents/GitHub/<repo-name>
git status
git add knowledge/ AGENTS.md
git commit -m "Update knowledge files and AGENTS.md references to kebab-case

- Added knowledge/behavioral-discipline.md (canonical from Make-AI-Agents)
- Added knowledge/learned/ folder (P-009 Hansei + Yokoten)
- Updated AGENTS.md references from snake_case to kebab-case
- [repo-specific details]

Aligns with Make-AI-Agents kebab-case migration (2026-07-08)"
git push
```

---

## Priority Order

**Priority 1** (Quick wins):
1. ✅ cse450-master - Two simple reference updates
2. m119-master - Likely minimal changes
3. mathcourses-master - Possibly add missing sections

**Priority 2** (Medium complexity):
4. ds250-onln-master - Medium file, unknown structure
5. m119-master - Medium file with likely some references

**Priority 3** (Most complex):
6. itm327-master - Largest knowledge set, bulk find-replace needed

**Already Complete**:
- ✅ ds460-master (reference implementation)

---

## Risk Assessment

### Low Risk (Safe Edits)
- ✅ Updating `behavioral_discipline.md` → `behavioral-discipline.md`
- ✅ Adding `## Learning loop` section (additive, doesn't break existing)
- ✅ Updating Sister Repos table descriptions

### Medium Risk (Requires Testing)
- ⚠️ Bulk find-replace in itm327 (verify no false positives)
- ⚠️ Changing knowledge file paths (ensure agents can still find files)

### No Risk (Symlinks as Fallback)
- Both snake_case and kebab-case versions exist in some repos (behavioral_discipline.md + behavioral-discipline.md)
- Symlinks provide backward compatibility if needed

---

## Success Criteria

**After all updates**, each repo should:
1. ✅ Have `knowledge/behavioral-discipline.md` (kebab-case)
2. ✅ Have `knowledge/learned/` folder
3. ✅ Reference kebab-case knowledge files in AGENTS.md
4. ✅ Have `## Learning loop` section (or equivalent)
5. ✅ Match ds460-master structure quality (where applicable)

---

## Next Actions

**Immediate**:
1. **Read remaining AGENTS.md files** to finalize proposals
2. **Execute cse450-master updates** (easiest, well-defined)
3. **Generate specific Edit commands** for other repos
4. **Execute and commit** one repo at a time

**Within 1 hour**:
- All 6 repos updated and committed

---

## Appendix: cse450-master Specific Edits (Ready to Execute)

### Edit 1: Sister Repos Table (Line 43)

```markdown
OLD:
| `Make-AI-Agents/` | Agent-authoring toolkit; source of the Working-Style behavioral discipline | `make_*.md`/`.json` generators at root, `knowledge/behavioral_discipline.md` |

NEW:
| `Make-AI-Agents/` | Agent-authoring toolkit; agent spec templates | `make_*.md` generators at root, templates for agent specs + AGENTS.md |
```

### Edit 2: Working Style Section (Line 49-51)

```markdown
OLD:
This project follows the behavioral discipline defined in `Make-AI-Agents/knowledge/behavioral_discipline.md` — the discipline file lives inside the `Make-AI-Agents/` clone at this repo's root (a gitignored standalone clone of `chaz-clark/Make-AI-Agents`). To refresh the discipline: `git -C Make-AI-Agents pull`. **Read that file before doing non-trivial work in this repo.**

The four no-override principles — **P-001 Read Before Claiming, P-003 Stop on Defect, P-007 Pull Don't Push, P-010 Respect Intent** — apply unconditionally; the other six (P-002, P-004, P-005, P-006, P-008, P-009) have documented override conditions in the discipline file.

NEW:
This project follows the behavioral discipline defined in `knowledge/behavioral-discipline.md` — the 10 principles + 5 interaction patterns sourced from Make-AI-Agents. **Read that file before doing non-trivial work in this repo.**

The four no-override principles — **P-001 Read Before Claiming, P-003 Stop on Defect, P-007 Pull Don't Push, P-010 Respect Intent** — apply unconditionally; the other six (P-002, P-004, P-005, P-006, P-008, P-009) have documented override conditions in the discipline file.
```

### Optional Edit 3: Add Learning Loop Section (After Active Context)

```markdown
INSERT AFTER LINE 66 (after Active Context section):

## Learning loop

Lessons learned during agent sessions are distilled into `knowledge/learned/` — structured markdown following P-009 (Hansei + Yokoten). Future invocations read these alongside core knowledge files.

What counts: surprises, non-obvious quirks, user-preference signals, system gotchas. What does NOT count: generic "task done" prose. **A lesson must be specific and reusable.**
```

---

**End of Proposals Document**
