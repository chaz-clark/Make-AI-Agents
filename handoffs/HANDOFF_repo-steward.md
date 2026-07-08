---
direction: deliver
status: active
from_repo: Make-AI-Agents
to_repo: (future) repo-steward agent
date_created: 2026-07-08
last_updated: 2026-07-08
---

# Handoff: Repo Stewardship and Drift Detection

**To**: Future `repo-steward` agent or workflow
**From**: Make-AI-Agents (source of truth for behavioral discipline + templates)
**Purpose**: Establish automated drift detection for all repos consuming Make-AI-Agents standards

---

## Mission

Create an automated stewardship agent that audits all repos in `~/Documents/GitHub/` that use Make-AI-Agents templates, knowledge files, or behavioral discipline, and notifies Chaz when any repo drifts from current standards.

---

## Context

**Date**: 2026-07-08

**Trigger**: After completing kebab-case migration + master repos audit, discovered:
- 6 *-master repos consume Make-AI-Agents knowledge files
- Multiple sister repos (canvas-toolbox, gh-issues-agent, handoff) reference Make-AI-Agents
- Standards evolve (kebab-case migration, YAML frontmatter, Sprint A/B/F upgrades)
- Manual audits don't scale — need automated drift detection

**Recent changes**:
- Kebab-case migration (snake_case → kebab-case for all .md files/folders)
- JSON purge (companion .json files deprecated, YAML frontmatter now canonical)
- Sprints A/B/F (YAML frontmatter, Learning loop, Handoff recognition)
- behavioral-discipline.md v1.4 (trunk-always-works extension)

**Pain point**: Standards evolve in Make-AI-Agents, but consumer repos lag. Example: itm327-master still had all snake_case knowledge file references after kebab-case migration.

---

## What the Repo Steward Should Do

### 1. Discovery Phase

**Scan ~/Documents/GitHub/ for repos that consume Make-AI-Agents**:
- Has `knowledge/` folder
- Has `AGENTS.md` file
- References Make-AI-Agents in AGENTS.md
- Has gitignored Make-AI-Agents clone as sister repo

**Output**: List of managed repos with metadata:
```json
{
  "repo_name": "ds460-master",
  "path": "~/Documents/GitHub/ds460-master",
  "has_agents_md": true,
  "has_knowledge_folder": true,
  "references_make_ai_agents": true,
  "last_audited": "2026-07-08",
  "compliance_score": 10
}
```

### 2. Audit Phase (Per Repo)

For each discovered repo, check:

#### A. Knowledge Folder Compliance
- ✅ `knowledge/behavioral-discipline.md` exists (kebab-case)
- ✅ `knowledge/learned/` folder exists
- ⚠️ Old snake_case files still present (expected during grace period)
- ⚠️ Missing optional files (source-docs-index.md, etc.) — flag if repo would benefit

**Scoring**:
- 2 points: Has behavioral-discipline.md (kebab)
- 1 point: Has learned/ folder
- 1 point: No missing critical files

#### B. AGENTS.md Structure Compliance
- ✅ Has YAML frontmatter
- ✅ Has `## Working Style` section
- ✅ Has `## Learning loop` section
- ✅ Has `## Handoff document recognition` section (if uses handoff convention)
- ✅ References knowledge files with kebab-case naming
- ⚠️ Still references Make-AI-Agents clone for discipline (should reference local knowledge/)

**Scoring**:
- 2 points: YAML frontmatter present
- 1 point: Each required section present (Working Style, Learning loop)
- 1 point: Kebab-case knowledge references
- 1 point: References local knowledge/ instead of Make-AI-Agents clone
- 1 point: Handoff recognition section (if applicable)

#### C. Behavioral Discipline Version Check
- Compare local `knowledge/behavioral-discipline.md` against canonical Make-AI-Agents version
- Flag if local is >30 days stale
- Flag if local is missing recent principles (check version number in frontmatter)

**Scoring**:
- 2 points: Up to date (within 30 days)
- 1 point: Slightly stale (30-90 days)
- 0 points: Very stale (>90 days) — ALERT

#### D. Git Hygiene Check
- Check if `knowledge/` folder is committed (not gitignored)
- Check if AGENTS.md is committed
- Check if repo has unpushed commits on main

**Scoring**:
- 1 point: knowledge/ committed
- 1 point: AGENTS.md committed
- Warn (not scored): Unpushed commits detected

### 3. Drift Detection

**Compare current state against canonical Make-AI-Agents**:
- Knowledge files: Hash compare against `Make-AI-Agents/knowledge/behavioral-discipline.md`
- AGENTS.md structure: Section presence check
- Naming conventions: Scan for snake_case references to knowledge files

**Alert triggers**:
1. **Critical drift** (score < 5/10): Missing behavioral-discipline.md, no AGENTS.md, very stale knowledge
2. **Medium drift** (score 5-7/10): Missing sections, snake_case references, stale knowledge
3. **Minor drift** (score 8-9/10): Missing optional sections, slightly stale
4. **Compliant** (score 10/10): Reference implementation (ds460-master is current gold standard)

### 4. Notification Phase

**When drift detected**, notify Chaz via:
- Console output (if running interactively)
- Markdown report written to `~/.claude/memory/repo_steward_alerts.md`
- Optional: GitHub issue in Make-AI-Agents repo (for tracking)

**Notification format**:
```markdown
# Repo Stewardship Alert — 2026-07-08

## Critical Drift Detected: m119-master

**Compliance score**: 4/10

**Issues**:
- ❌ Missing YAML frontmatter in AGENTS.md
- ❌ AGENTS.md still references Make-AI-Agents/knowledge/behavioral_discipline.md (snake_case)
- ⚠️ knowledge/behavioral-discipline.md is 45 days stale

**Recommended actions**:
1. Copy latest behavioral-discipline.md from Make-AI-Agents
2. Add YAML frontmatter to AGENTS.md
3. Update knowledge file references to kebab-case

**Auto-fix available**: Yes — run `repo-steward fix m119-master`
```

### 5. Auto-Fix Mode (Optional Advanced Feature)

If steward can make low-risk fixes automatically:
- Copy latest behavioral-discipline.md
- Create missing learned/ folders
- Add missing AGENTS.md sections (with placeholders)
- Update snake_case → kebab-case references

**Constraints**:
- Never delete files
- Never modify project-specific content
- Always create git commits (don't auto-push)
- Log all changes for review

---

## Canonical Files to Monitor

**From Make-AI-Agents/knowledge/**:
1. `behavioral-discipline.md` (v1.4 as of 2026-07-08)
   - Version tracked in YAML frontmatter
   - 10 principles, 5 interaction patterns
   - ~37KB

**From Make-AI-Agents/**:
2. `make-AGENTS.md` (AGENTS.md generator template)
   - Defines required sections
   - Sprint A/B/F standards
   - YAML frontmatter format

**Naming conventions**:
3. Markdown files: kebab-case
4. Python files: snake_case
5. Special files: UPPERCASE

---

## Repos to Monitor (Initial Scope)

### High Priority (*-master repos)
1. **cse450-master** — Canvas course management
2. **ds250-onln-master** — Canvas course management
3. **ds460-master** — Canvas course management (REFERENCE IMPLEMENTATION ✅)
4. **itm327-master** — Canvas course management
5. **m119-master** — Canvas course management
6. **mathcourses-master** — Canvas course management

### Medium Priority (Sister repos)
7. **canvas-toolbox** — Canvas LMS toolkit
8. **gh-issues-agent** — GitHub Issues helper
9. **handoff** — Cross-repo handoff convention (may be exempt — it's the canonical spec)

### Low Priority (Consumer repos)
10. Any other repo with `knowledge/` or `AGENTS.md` in ~/Documents/GitHub/

---

## Success Criteria for Steward

**Steward is working if**:
1. ✅ Discovers all repos with Make-AI-Agents dependencies
2. ✅ Audits each repo and assigns compliance score
3. ✅ Detects drift within 7 days of Make-AI-Agents changes
4. ✅ Notifies Chaz with actionable report
5. ✅ (Optional) Auto-fixes low-risk issues and creates commits

**Steward has high quality if**:
- Zero false positives (doesn't flag compliant repos)
- Clear, actionable notifications
- Fast execution (<5 seconds per repo)
- Generates audit log for historical tracking

---

## Execution Frequency

**Options**:
1. **On-demand** — Chaz runs `repo-steward audit` manually
2. **Post-commit hook** — Runs after Make-AI-Agents commits (detects new standards)
3. **Weekly cron** — Sunday night, generates Monday morning report
4. **GitHub Action** — Runs in Make-AI-Agents repo, posts results

**Recommendation**: Start with on-demand, graduate to weekly cron.

---

## Implementation Hints

### Discovery Script (Bash)
```bash
#!/bin/bash
# Find all repos with AGENTS.md or knowledge/
find ~/Documents/GitHub -maxdepth 2 -name "AGENTS.md" -o -name "knowledge" -type d | \
  sed 's|/AGENTS.md||' | sed 's|/knowledge||' | sort -u
```

### Compliance Checker (Python)
```python
def audit_repo(repo_path):
    score = 0
    issues = []

    # Check knowledge/behavioral-discipline.md
    if (repo_path / "knowledge" / "behavioral-discipline.md").exists():
        score += 2
    else:
        issues.append("Missing knowledge/behavioral-discipline.md")

    # Check knowledge/learned/
    if (repo_path / "knowledge" / "learned").is_dir():
        score += 1
    else:
        issues.append("Missing knowledge/learned/ folder")

    # Check AGENTS.md frontmatter
    agents_md = repo_path / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text()
        if content.startswith("---"):
            score += 2
        else:
            issues.append("Missing YAML frontmatter in AGENTS.md")

    return {"score": score, "max": 10, "issues": issues}
```

### Drift Detector (File Hash)
```python
import hashlib

def is_stale(local_file, canonical_file):
    """Compare file hashes"""
    local_hash = hashlib.sha256(local_file.read_bytes()).hexdigest()
    canonical_hash = hashlib.sha256(canonical_file.read_bytes()).hexdigest()
    return local_hash != canonical_hash
```

---

## Handoff Acceptance Criteria

**This handoff is "delivered" when**:
1. ✅ repo-steward agent spec exists (`repo_steward.md` or similar)
2. ✅ Steward can discover all managed repos
3. ✅ Steward can audit one repo and generate compliance score
4. ✅ Steward can detect drift in knowledge/behavioral-discipline.md
5. ✅ Steward can write notification report

**This handoff is "complete" when**:
1. ✅ Steward runs on all 6 *-master repos
2. ✅ Steward generates clean report (no errors)
3. ✅ Chaz reviews first report and confirms accuracy
4. ✅ (Optional) Auto-fix mode tested on one repo

---

## Related Work

**Prior art**:
- `MASTER_REPOS_AUDIT.md` (2026-07-08) — Manual audit of 6 repos, THIS is what steward should automate
- `MASTER_REPOS_PROPOSALS.md` (2026-07-08) — Specific fixes needed, this is the notification format steward should generate
- `KEBAB_CASE_MIGRATION.md` — Example of standards evolution that triggers drift

**Reference implementations**:
- `ds460-master` — Gold standard compliance (score: 10/10)
- `Make-AI-Agents/AGENTS.md` — Source of truth for structure

---

## Questions for Chaz ✅ ANSWERED

1. **Notification preference**: ✅ **GitHub issue** in Make-AI-Agents repo
2. **Auto-fix permission**: ✅ **Propose only** — write proposed fixes as notes in GitHub issue, don't auto-commit
3. **Frequency**: ✅ **Weekly cron** — Sunday night, generates Monday morning GitHub issue
4. **Compliance threshold**: ✅ **Start with <5** for critical alerts, adjust week-over-week based on audit results
5. **Philosophy**: ✅ **Tight control on structure and updates, but allow for individuality** — enforce canonical structure (YAML frontmatter, required sections, kebab-case) while permitting repo-specific content

---

## Critical Context: canvas-toolbox AGENTS.md Generation Gap

**Important discovery (2026-07-08)**: The 6 *-master repos' AGENTS.md files were **NOT** built using the canvas-toolbox make-AGENTS.md process.

**The gap**:
- canvas-toolbox has a build process that runs `make-AGENTS.md` mixed with knowledge gained during `canvas-sync --init`
- This process generates AGENTS.md with Canvas-specific context (course IDs, topology, module structure)
- The current *-master AGENTS.md files are hand-written or scaffolded from older templates
- They lack the Canvas-specific grounding that the canvas-toolbox build would provide

**Implications for repo-steward**:
1. **Don't enforce 100% compliance** on *-master AGENTS.md structure — they may legitimately differ from make-AGENTS.md standard if built via canvas-toolbox
2. **Flag missing canvas-sync context** — if a *-master repo references Canvas but lacks course IDs, topology, or module structure sections, recommend rebuilding
3. **New check**: "Was AGENTS.md built via canvas-toolbox?" — check for Canvas-specific metadata in frontmatter
4. **Proposed action**: Add to steward scope — "Detect *-master repos that should rebuild AGENTS.md via canvas-toolbox build"

**Example**:
- ds460-master AGENTS.md has FERPA discipline section ✅
- But may lack Canvas topology details that canvas-toolbox build would add
- Steward should propose: "Consider rebuilding via canvas-toolbox make-AGENTS process to add Canvas grounding"

**Recommendation**: Future sprint should rebuild all 6 *-master AGENTS.md files using canvas-toolbox, then audit against THAT output (not raw make-AGENTS.md).

---

## Status

**Handoff created**: 2026-07-08
**Handoff status**: ✅ Active (answers received, ready for implementation)
**Next action**: Create `repo_steward.md` agent spec or implement as standalone Python script

**Implementation decisions**:
- **Notification**: GitHub issue in Make-AI-Agents (one issue per weekly run)
- **Auto-fix**: Propose only (fixes written as notes in issue, not committed)
- **Frequency**: Weekly cron (Sunday night → Monday morning issue)
- **Threshold**: Critical alert if score <5, adjust based on audit trends
- **Scope**: 6 *-master + 3 sister repos initially, expand as needed
