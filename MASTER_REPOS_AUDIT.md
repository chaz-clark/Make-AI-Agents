# Master Repos Knowledge & AGENTS.md Audit

**Date**: 2026-07-08
**Auditor**: Claude Code (Sonnet 4.5)
**Scope**: 6 *-master repos in ~/Documents/GitHub/

---

## Executive Summary

Audited 6 master repos for knowledge folder compliance and AGENTS.md structure. **5 of 6** repos have AGENTS.md files. **5 of 6** have knowledge/ folders, but content varies significantly.

**Key Findings**:
- ⚠️ **cse450-master**: Missing knowledge/ folder entirely
- ⚠️ **ds250-onln-master**: Only has behavioral_discipline (snake_case), missing kebab-case version
- ✅ **ds460-master**: Most compliant - has behavioral-discipline.md (kebab), source-docs-index.md, learned/
- ⚠️ **itm327-master**: Has most files but all in snake_case (needs kebab-case versions)
- ⚠️ **m119-master**: Minimal - only behavioral_discipline + learned/
- ⚠️ **mathcourses-master**: Nearly empty - only learned/ folder

---

## Repo-by-Repo Audit

### 1. cse450-master

**Location**: `~/Documents/GitHub/cse450-master`

**Status**: ⚠️ NEEDS UPDATES

**Findings**:
- ✅ Has `AGENTS.md` (5,931 bytes, updated Jul 2)
- ❌ **Missing `knowledge/` folder entirely**
- References Make-AI-Agents clone's knowledge files in AGENTS.md line 49

**AGENTS.md Structure**:
```
Line 26: lib/agents/knowledge/ ← pedagogy knowledge files
Line 43: Make-AI-Agents/ ... knowledge/behavioral_discipline.md
Line 49: References Make-AI-Agents/knowledge/behavioral_discipline.md
```

**Recommendations**:
1. **Create `knowledge/` folder**
2. **Copy canonical files**:
   - `behavioral-discipline.md` (kebab-case)
   - `learned/` folder (for P-009 Hansei + Yokoten)
3. **Update AGENTS.md** to reference local knowledge/ instead of Make-AI-Agents clone

---

### 2. ds250-onln-master

**Location**: `~/Documents/GitHub/ds250-onln-master`

**Status**: ⚠️ NEEDS UPDATES (Partial compliance)

**Findings**:
- ✅ Has `AGENTS.md` (37,178 bytes, updated Jul 7)
- ✅ Has `knowledge/` folder
- ⚠️ Knowledge contents:
  - `behavioral_discipline.json` (old format)
  - `behavioral_discipline.md` (snake_case naming)
- ❌ Missing `behavioral-discipline.md` (kebab-case)
- ❌ Missing `learned/` folder

**AGENTS.md**: Large file (37KB), likely comprehensive

**Recommendations**:
1. **Add `behavioral-discipline.md`** (kebab-case version)
2. **Create `learned/` folder** (for P-009)
3. **Keep snake_case versions** as symlinks during grace period (6-12 months)
4. **Audit AGENTS.md** for kebab-case references

---

### 3. ds460-master

**Location**: `~/Documents/GitHub/ds460-master`

**Status**: ✅ BEST COMPLIANCE

**Findings**:
- ✅ Has `AGENTS.md` (21,213 bytes, updated Jul 8 - TODAY!)
- ✅ Has `knowledge/` folder (6 items)
- ✅ Knowledge contents (kebab-case!):
  - `behavioral-discipline.md` ✓
  - `source-docs-index.md` ✓
  - `naming-conventions.md` (project-specific)
  - `learned/` folder ✓
- ✅ YAML frontmatter in AGENTS.md
- ✅ Proper section structure (## ⚠️ AI Agent FERPA Discipline, ## Working Style, ## Handoff document recognition, ## Learning loop, etc.)

**AGENTS.md Sections**:
```
✅ YAML frontmatter
✅ ## ⚠️ AI Agent FERPA Discipline
✅ ## Project Purpose
✅ ## Structure
✅ ## Sister Repos
✅ ## Working Style
✅ ## Handoff document recognition
✅ ## Learning loop
✅ ## Active Context
✅ ## Domain Terms
✅ ## External System Lessons
```

**Recommendations**:
- **✅ NO ACTION NEEDED** - This repo is the gold standard
- Consider it the reference implementation for other repos

---

### 4. itm327-master

**Location**: `~/Documents/GitHub/itm327-master`

**Status**: ⚠️ NEEDS KEBAB-CASE MIGRATION

**Findings**:
- ✅ Has `AGENTS.md` (29,842 bytes, updated Jul 7)
- ✅ Has `knowledge/` folder (13 items - most comprehensive!)
- ⚠️ Knowledge contents (all snake_case):
  - `behavioral_discipline.json`
  - `behavioral_discipline.md` ← needs kebab version
  - `hermes_comparison.md` ← needs kebab version
  - `json_to_yaml_migration.md` ← needs kebab version
  - `mcp_integration_patterns.md` ← needs kebab version
  - `source_docs_index.json`
  - `source_docs_index.md` ← needs kebab version
  - `learned/` folder ✓
  - `gh-issues/` (submodule or folder?)
  - `agile_sprint_handoff.md`
  - `README.md`

**Observations**:
- Has the MOST complete knowledge set
- Just needs kebab-case versions added
- Has project-specific files (agile_sprint_handoff, gh-issues)

**Recommendations**:
1. **Copy kebab-case versions** from Make-AI-Agents:
   - `behavioral-discipline.md`
   - `hermes-comparison.md`
   - `json-to-yaml-migration.md`
   - `mcp-integration-patterns.md`
   - `source-docs-index.md`
2. **Keep snake_case versions** as symlinks (or just leave both during grace period)
3. **Audit AGENTS.md** for kebab-case references

---

### 5. m119-master

**Location**: `~/Documents/GitHub/m119-master`

**Status**: ⚠️ MINIMAL COMPLIANCE

**Findings**:
- ✅ Has `AGENTS.md` (20,427 bytes, updated Jul 7)
- ✅ Has `knowledge/` folder (5 items)
- ⚠️ Knowledge contents (minimal):
  - `behavioral_discipline.json`
  - `behavioral_discipline.md` (snake_case)
  - `learned/` folder ✓
- ❌ Missing kebab-case version: `behavioral-discipline.md`
- ❌ Missing optional but useful files

**Recommendations**:
1. **Add `behavioral-discipline.md`** (kebab-case)
2. **Optionally add**:
   - `source-docs-index.md` (if repo uses source-docs pattern)
   - Other knowledge files as needed
3. **Keep existing** snake_case as symlinks

---

### 6. mathcourses-master

**Location**: `~/Documents/GitHub/mathcourses-master`

**Status**: ⚠️ NEARLY EMPTY

**Findings**:
- ✅ Has `AGENTS.md` (12,833 bytes, updated Jul 7)
- ✅ Has `knowledge/` folder
- ⚠️ Knowledge contents (nearly empty):
  - `learned/` folder only
- ❌ Missing `behavioral-discipline.md`
- ❌ Missing all other knowledge files

**Recommendations**:
1. **Add `behavioral-discipline.md`** (kebab-case) - CRITICAL
2. **Optionally add**:
   - `source-docs-index.md`
   - Other knowledge files based on project needs

---

## Canonical Knowledge Files (Make-AI-Agents)

### Core Files (should exist in all repos)
1. **`behavioral-discipline.md`** (kebab-case) - 37KB
   - The Toyota Way + Karpathy discipline
   - 10 principles, 5 interaction patterns
   - Version 1.4
   - **Status**: REQUIRED in all repos

2. **`learned/` folder**
   - P-009 (Hansei + Yokoten) landing zone
   - Closed-loop distillation for agent lessons
   - **Status**: REQUIRED in all repos

### Optional Files (copy if relevant)
3. **`source-docs-index.md`** - Platform docs lookup table
4. **`hermes-comparison.md`** - Nous Research Hermes Agent comparison
5. **`json-to-yaml-migration.md`** - JSON → YAML frontmatter migration guide
6. **`mcp-integration-patterns.md`** - Model Context Protocol patterns

### Deprecated (but kept for backward compatibility)
- `behavioral_discipline.md` (snake_case) - symlink to kebab version
- `behavioral_discipline.json` - structured QC rules (still useful for QC agents)

---

## AGENTS.md Compliance Matrix

| Repo | YAML Frontmatter | Working Style | Handoff Recognition | Learning Loop | Active Context |
|------|------------------|---------------|---------------------|---------------|----------------|
| **cse450-master** | ❓ | ❓ | ❓ | ❓ | ❓ |
| **ds250-onln-master** | ❓ | ❓ | ❓ | ❓ | ❓ |
| **ds460-master** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **itm327-master** | ❓ | ❓ | ❓ | ❓ | ❓ |
| **m119-master** | ❓ | ❓ | ❓ | ❓ | ❓ |
| **mathcourses-master** | ❓ | ❓ | ❓ | ❓ | ❓ |

**Note**: ❓ = Needs manual inspection (not checked in this audit pass)

---

## Recommended Actions Summary

### Priority 1: Critical (All Repos)
1. **cse450-master**:
   - Create `knowledge/` folder
   - Copy `behavioral-discipline.md`
   - Create `learned/` folder

2. **ds250-onln-master**:
   - Copy `behavioral-discipline.md` (kebab)
   - Create `learned/` folder

3. **m119-master**:
   - Copy `behavioral-discipline.md` (kebab)

4. **mathcourses-master**:
   - Copy `behavioral-discipline.md` (kebab)

### Priority 2: Kebab-Case Migration
5. **itm327-master**:
   - Copy all kebab-case versions of existing files
   - Keep snake_case as symlinks or legacy

### Priority 3: AGENTS.md Audits
6. **All repos** (except ds460):
   - Audit AGENTS.md for:
     - YAML frontmatter presence
     - Section structure compliance
     - Knowledge file references (kebab-case)
     - Sprints A/B/F compliance (if applicable)

---

## Execution Plan

### Phase 1: Create Missing Knowledge Folders (5 minutes)
```bash
# cse450-master only
mkdir -p ~/Documents/GitHub/cse450-master/knowledge/learned
```

### Phase 2: Copy Core Knowledge Files (10 minutes)

**For all 6 repos**, copy `behavioral-discipline.md`:
```bash
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/cse450-master/knowledge/
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/ds250-onln-master/knowledge/
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/ds460-master/knowledge/  # already has it
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/itm327-master/knowledge/
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/m119-master/knowledge/
cp knowledge/behavioral-discipline.md ~/Documents/GitHub/mathcourses-master/knowledge/
```

### Phase 3: Create Missing `learned/` Folders (5 minutes)
```bash
mkdir -p ~/Documents/GitHub/ds250-onln-master/knowledge/learned
mkdir -p ~/Documents/GitHub/m119-master/knowledge/learned  # might already exist
mkdir -p ~/Documents/GitHub/mathcourses-master/knowledge/learned  # already exists
```

### Phase 4: Copy Optional Knowledge Files to itm327 (5 minutes)
```bash
# itm327 has the most complete set, just needs kebab versions
cp knowledge/hermes-comparison.md ~/Documents/GitHub/itm327-master/knowledge/
cp knowledge/json-to-yaml-migration.md ~/Documents/GitHub/itm327-master/knowledge/
cp knowledge/mcp-integration-patterns.md ~/Documents/GitHub/itm327-master/knowledge/
cp knowledge/source-docs-index.md ~/Documents/GitHub/itm327-master/knowledge/
```

### Phase 5: AGENTS.md Audits (30-60 minutes)

**For each repo** (except ds460, which is compliant):
1. Read AGENTS.md
2. Check for YAML frontmatter
3. Check for required sections
4. Check knowledge/ references (update to kebab-case)
5. Propose updates if needed

---

## Risk Assessment

### Low Risk (Safe to Execute Immediately)
- ✅ Copying `behavioral-discipline.md` to repos
- ✅ Creating `learned/` folders
- ✅ Creating missing `knowledge/` folders

### Medium Risk (Requires Repo-Specific Review)
- ⚠️ Updating AGENTS.md files (each is repo-specific)
- ⚠️ Changing knowledge file references (may break existing workflows)

### No Risk (Already Compliant)
- ✅ ds460-master (reference implementation)

---

## Success Criteria

**After execution, all 6 repos should have**:
1. ✅ `knowledge/` folder exists
2. ✅ `knowledge/behavioral-discipline.md` (kebab-case) exists
3. ✅ `knowledge/learned/` folder exists
4. ✅ AGENTS.md references knowledge files correctly
5. ✅ AGENTS.md has proper structure (frontmatter, sections)

---

## Appendix: File Sizes Reference

**Canonical files in Make-AI-Agents**:
- `behavioral-discipline.md`: ~37KB
- `hermes-comparison.md`: ~15KB
- `json-to-yaml-migration.md`: ~8KB
- `mcp-integration-patterns.md`: ~12KB
- `source-docs-index.md`: ~20KB

**AGENTS.md sizes** (current):
- cse450-master: 5.9KB (small)
- ds250-onln-master: 37KB (large)
- ds460-master: 21KB (medium)
- itm327-master: 29KB (medium-large)
- m119-master: 20KB (medium)
- mathcourses-master: 12KB (small-medium)

---

**End of Audit Report**
