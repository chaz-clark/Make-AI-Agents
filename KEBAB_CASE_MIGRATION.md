# Kebab-Case Migration Plan — Make-AI-Agents

**Status**: Last repo requiring migration to kebab-case standard
**Created**: 2026-07-08
**Estimated Effort**: 9-13 hours
**Risk Level**: Medium (612+ references to update)

---

## Executive Summary

This repo is the last one not migrated to kebab-case for Markdown files. All other repos (canvas-toolbox, gh-issues-agent, handoff) have completed this migration.

**Scope**: 126 items to rename (120 files + 6 folders), 612+ internal references to update.

**Recommended Approach**: Phased migration with symlinks (zero downtime, safe rollback).

---

## Ecosystem Convention Alignment

Per ecosystem-specific naming conventions:
- **Python (.py)**: snake_case ✅ (no changes needed)
- **Markdown (.md)**: kebab-case ❌ (current: snake_case)
- **Rust (.rs)**: snake_case ✅ (N/A - no Rust files)
- **Special files**: UPPERCASE ✅ (README*, AGENTS.md, etc.)

---

## Complete Inventory

### Core Template Files (7 files)

| Current | Target | References |
|---------|--------|------------|
| `make-agent.md` | `make-agent.md` | 192 |
| `make-agent-qc.md` | `make-agent-qc.md` | ~40 |
| `make-agent-knowledge.md` | `make-agent-knowledge.md` | ~30 |
| `make_AGENTS.md` | `make-AGENTS.md` | ~50 (keep AGENTS capitalized) |
| `make-AGENTS-qc.md` | `make-AGENTS-qc.md` | ~25 |
| `make-orchestrator-agent.md` | `make-orchestrator-agent.md` | ~35 |
| `make-managed-agent.md` | `make-managed-agent.md` | ~20 |

### Knowledge Files (9 files)

| Current | Target |
|---------|--------|
| `knowledge/behavioral_discipline.md` | `knowledge/behavioral-discipline.md` |
| `knowledge/hermes_comparison.md` | `knowledge/hermes-comparison.md` |
| `knowledge/json_to_yaml_migration.md` | `knowledge/json-to-yaml-migration.md` |
| `knowledge/mcp_integration_patterns.md` | `knowledge/mcp-integration-patterns.md` |
| `knowledge/source_docs_index.md` | `knowledge/source-docs-index.md` |
| `knowledge/learned/5tier_fetch_automation.md` | `knowledge/learned/5tier-fetch-automation.md` |
| `knowledge/learned/github_api_faster_than_http.md` | `knowledge/learned/github-api-faster-than-http.md` |
| `knowledge/learned/playwright_react_spa_pattern.md` | `knowledge/learned/playwright-react-spa-pattern.md` |

### Update Agents Files (10 files - pairs)

| Current | Target |
|---------|--------|
| `update_agents/doc_analysis_agent.md` | `update-agents/doc-analysis-agent.md` |
| `update_agents/doc_refresh_agent.md` | `update-agents/doc-refresh-agent.md` |
| `update_agents/doc_refresh_workflow.md` | `update-agents/doc-refresh-workflow.md` |
| `update_agents/merge_agent.md` | `update-agents/merge-agent.md` |
| `update_agents/update_agent.md` | `update-agents/update-agent.md` |
| `update_agents/PURGE_PLAN_2026-07-06.md` | `update-agents/PURGE-PLAN-2026-07-06.md` |
| `update_agents/SPRINTS_2026-07-06.md` | `update-agents/SPRINTS-2026-07-06.md` |
| `update_agents/REFRESH_PLAN_2026-07-06.md` | `update-agents/REFRESH-PLAN-2026-07-06.md` |
| `update_agents/REFRESH_COMPLETE_2026-07-06.md` | `update-agents/REFRESH-COMPLETE-2026-07-06.md` |
| `update_agents/REPO_UPDATE_PLAN_2026-07-06.md` | `update-agents/REPO-UPDATE-PLAN-2026-07-06.md` |

**Note**: `fetch_doc.py` stays as-is (Python uses snake_case)

### Make Gems Files (7 files)

| Current | Target |
|---------|--------|
| `make_gems/make_gem.md` | `make-gems/make-gem.md` |
| `make_gems/make_gem_qc.md` | `make-gems/make-gem-qc.md` |
| `make_gems/implement_gem.md` | `make-gems/implement-gem.md` |
| `make_gems/README_GEM.md` | `make-gems/README-GEM.md` |
| `make_gems/gem_instructions/byui_catalog_index.md` | `make-gems/gem-instructions/byui-catalog-index.md` |
| `make_gems/gem_instructions/byui_employer_reference.md` | `make-gems/gem-instructions/byui-employer-reference.md` |
| `make_gems/gem_instructions/byui_gap_analyst_implement.md` | `make-gems/gem-instructions/byui-gap-analyst-implement.md` |
| `make_gems/gem_instructions/example_instructions.md` | `make-gems/gem-instructions/example-instructions.md` |

### README Files (2 files)

| Current | Target |
|---------|--------|
| `README_Disclosure.md` | `README-Disclosure.md` |
| `README_QC.md` | `README-QC.md` |

### QC Reports (7 files)

| Current | Target |
|---------|--------|
| `qc_reports/cse110_qc_report.md` | `qc-reports/cse110-qc-report.md` |
| `qc_reports/cse110_v3_qc_report.md` | `qc-reports/cse110-v3-qc-report.md` |
| `qc_reports/ds150_qc_report.md` | `qc-reports/ds150-qc-report.md` |
| `qc_reports/ds250_qc_report.md` | `qc-reports/ds250-qc-report.md` |
| `qc_reports/ds250_rewritten_qc_report.md` | `qc-reports/ds250-rewritten-qc-report.md` |
| `qc_reports/march_madness_agent_qc_report.md` | `qc-reports/march-madness-agent-qc-report.md` |
| `qc_reports/ME342_TA_qc_report_v2.md` | `qc-reports/ME342-TA-qc-report-v2.md` |

### Handoffs (dated files - keep format)

Date-stamped handoffs use ISO date format (2026-05-22) which already includes hyphens. Topic portion should be kebab-case:

| Current | Target |
|---------|--------|
| `handoffs/2026-05-22_backbone-source-of-truth-sprint.md` | ✅ Already kebab-case |
| `handoffs/2026-05-22_toolkit-steward-sprint-kickoff.md` | ✅ Already kebab-case |
| `handoffs/2026-05-28_agents-md-hermes-sprints-upgrade.md` | ✅ Already kebab-case |
| `handoffs/2026-05-28_hermes-research-and-ecosystem-sprint-proposals.md` | ✅ Already kebab-case |

### Directories (6 folders)

| Current | Target | References |
|---------|--------|------------|
| `make_gems/` | `make-gems/` | 22 |
| `make_gems/gem_instructions/` | `make-gems/gem-instructions/` | ~15 |
| `qc_reports/` | `qc-reports/` | ~20 |
| `source_docs/` | `source-docs/` | ~100 |
| `update_agents/` | `update-agents/` | 57 |
| `.github_issues/` | `.github-issues/` | ~5 |

**TOTAL**: 120 files + 6 folders = **126 items to rename**

---

## Reference Analysis

### High-Impact Files (Most References)

1. **behavioral_discipline** - 206 references
   - Most critical knowledge file
   - Referenced by all templates
   - YAML frontmatter dependencies

2. **make_agent** - 192 references
   - Core template
   - Referenced throughout ecosystem
   - Downstream repos reference this

3. **update_agents/** folder - 57 references
   - Cross-file references within update_agents/
   - Topology specs in orchestrator

4. **source_docs/** folder - ~100 references
   - Cache file paths in agents
   - Refresh log references
   - Dropbox staging paths

5. **make_gems/** folder - 22 references
   - Template references
   - Instruction file paths

### External References (Downstream Impact)

**Repos that reference Make-AI-Agents files**:
1. **canvas-toolbox** - References make-agent pattern in AGENTS.md
2. **gh-issues-agent** - May reference file names
3. **handoff** - AGENTS_snippet.md references
4. **5 master repos** - Reference Make-AI-Agents structure

**Mitigation**: Symlinks provide backward compatibility during transition period.

---

## Migration Strategy: Phased with Symlinks

### Why Phased with Symlinks?

**Pros**:
- ✅ Zero breakage for downstream consumers
- ✅ Gradual transition (can pause/resume)
- ✅ Easy rollback if issues discovered
- ✅ Test each phase independently

**Cons**:
- Cluttered with symlinks temporarily (6-12 months)
- Slightly more complex than "big bang"

**Alternative rejected**: Big bang (all at once) - too risky with 612+ references

---

## Execution Plan

### Phase 1: Core Templates (2-3 hours)

**Rename 7 core template files + create symlinks**

```bash
# Navigate to repo root
cd /Users/chazclar/Documents/GitHub/Make-AI-Agents

# Rename files with git mv (preserves history)
git mv make-agent.md make-agent.md
ln -s make-agent.md make-agent.md

git mv make-agent-qc.md make-agent-qc.md
ln -s make-agent-qc.md make-agent-qc.md

git mv make-agent-knowledge.md make-agent-knowledge.md
ln -s make-agent-knowledge.md make-agent-knowledge.md

git mv make_AGENTS.md make-AGENTS.md
ln -s make-AGENTS.md make_AGENTS.md

git mv make-AGENTS-qc.md make-AGENTS-qc.md
ln -s make-AGENTS-qc.md make-AGENTS-qc.md

git mv make-orchestrator-agent.md make-orchestrator-agent.md
ln -s make-orchestrator-agent.md make-orchestrator-agent.md

git mv make-managed-agent.md make-managed-agent.md
ln -s make-managed-agent.md make-managed-agent.md

# Stage symlinks
git add make-agent.md make-agent-qc.md make-agent-knowledge.md \
        make_AGENTS.md make-AGENTS-qc.md make-orchestrator-agent.md \
        make-managed-agent.md
```

**Update internal references in renamed files** (use sed/manual)

**Commit**:
```bash
git commit -m "Phase 1: Rename core templates to kebab-case (symlinks preserved)"
git push
```

**Verification**:
- All old paths still work via symlinks
- New paths resolve correctly
- Git log follows renamed files

---

### Phase 2: Knowledge Files (2-3 hours)

**Rename knowledge/ files**

```bash
cd knowledge

git mv behavioral_discipline.md behavioral-discipline.md
ln -s behavioral-discipline.md behavioral_discipline.md

git mv hermes_comparison.md hermes-comparison.md
ln -s hermes-comparison.md hermes_comparison.md

git mv json_to_yaml_migration.md json-to-yaml-migration.md
ln -s json-to-yaml-migration.md json_to_yaml_migration.md

git mv mcp_integration_patterns.md mcp-integration-patterns.md
ln -s mcp-integration-patterns.md mcp_integration_patterns.md

git mv source_docs_index.md source-docs-index.md
ln -s source-docs-index.md source_docs_index.md

cd learned
git mv 5tier_fetch_automation.md 5tier-fetch-automation.md
ln -s 5tier-fetch-automation.md 5tier_fetch_automation.md

git mv github_api_faster_than_http.md github-api-faster-than-http.md
ln -s github-api-faster-than-http.md github_api_faster_than_http.md

git mv playwright_react_spa_pattern.md playwright-react-spa-pattern.md
ln -s playwright-react-spa-pattern.md playwright_react_spa_pattern.md

cd ../..
git add knowledge/*.md knowledge/learned/*.md
```

**Update references in templates and agents**

**Commit**:
```bash
git commit -m "Phase 2: Rename knowledge files to kebab-case (symlinks preserved)"
git push
```

---

### Phase 3: Folders (3-4 hours)

**Critical**: Folder renames impact many references. Do carefully.

```bash
# Rename folders (git mv preserves history)
git mv make_gems make-gems
git mv update_agents update-agents
git mv qc_reports qc-reports
git mv source_docs source-docs
git mv .github_issues .github-issues

# Create symlinks
ln -s make-gems make_gems
ln -s update-agents update_agents
ln -s qc-reports qc_reports
ln -s source-docs source_docs
ln -s .github-issues .github_issues

git add make_gems update_agents qc_reports source_docs .github_issues
```

**Update all internal references** (612+ references across repo)

Critical files to update:
- AGENTS.md (structure tree)
- README.md (structure tree)
- All make-*.md templates (dependencies, cross_references)
- All update-agents/*.md files (spec_path, cross_references)
- .gitignore (if folder patterns present)

**Commit**:
```bash
git commit -m "Phase 3: Rename folders to kebab-case (symlinks preserved)"
git push
```

---

### Phase 4: Update Agents Files (1-2 hours)

**Rename files within update-agents/ folder**

```bash
cd update-agents

# Agent specs
git mv doc_analysis_agent.md doc-analysis-agent.md
ln -s doc-analysis-agent.md doc_analysis_agent.md

git mv doc_refresh_agent.md doc-refresh-agent.md
ln -s doc-refresh-agent.md doc_refresh_agent.md

git mv doc_refresh_workflow.md doc-refresh-workflow.md
ln -s doc-refresh-workflow.md doc_refresh_workflow.md

git mv merge_agent.md merge-agent.md
ln -s merge-agent.md merge_agent.md

git mv update_agent.md update-agent.md
ln -s update-agent.md update_agent.md

# Planning docs
git mv PURGE_PLAN_2026-07-06.md PURGE-PLAN-2026-07-06.md
ln -s PURGE-PLAN-2026-07-06.md PURGE_PLAN_2026-07-06.md

git mv SPRINTS_2026-07-06.md SPRINTS-2026-07-06.md
ln -s SPRINTS-2026-07-06.md SPRINTS_2026-07-06.md

git mv REFRESH_PLAN_2026-07-06.md REFRESH-PLAN-2026-07-06.md
ln -s REFRESH-PLAN-2026-07-06.md REFRESH_PLAN_2026-07-06.md

git mv REFRESH_COMPLETE_2026-07-06.md REFRESH-COMPLETE-2026-07-06.md
ln -s REFRESH-COMPLETE-2026-07-06.md REFRESH_COMPLETE_2026-07-06.md

git mv REPO_UPDATE_PLAN_2026-07-06.md REPO-UPDATE-PLAN-2026-07-06.md
ln -s REPO-UPDATE-PLAN-2026-07-06.md REPO_UPDATE_PLAN_2026-07-06.md

cd ..
git add update-agents/*.md
```

**Update topology references in orchestrator**

**Commit**:
```bash
git commit -m "Phase 4: Rename update-agents files to kebab-case"
git push
```

---

### Phase 5: Make Gems Files (1-2 hours)

```bash
cd make-gems

# Core files
git mv make_gem.md make-gem.md
ln -s make-gem.md make_gem.md

git mv make_gem_qc.md make-gem-qc.md
ln -s make-gem-qc.md make_gem_qc.md

git mv implement_gem.md implement-gem.md
ln -s implement-gem.md implement_gem.md

git mv README_GEM.md README-GEM.md
ln -s README-GEM.md README_GEM.md

# Rename gem_instructions folder
git mv gem_instructions gem-instructions
ln -s gem-instructions gem_instructions

cd gem-instructions

git mv byui_catalog_index.md byui-catalog-index.md
ln -s byui-catalog-index.md byui_catalog_index.md

git mv byui_employer_reference.md byui-employer-reference.md
ln -s byui-employer-reference.md byui_employer_reference.md

git mv byui_gap_analyst_implement.md byui-gap-analyst-implement.md
ln -s byui-gap-analyst-implement.md byui_gap_analyst_implement.md

git mv example_instructions.md example-instructions.md
ln -s example-instructions.md example_instructions.md

cd ../..
git add make-gems
```

**Commit**:
```bash
git commit -m "Phase 5: Rename make-gems files to kebab-case"
git push
```

---

### Phase 6: READMEs and QC Reports (1 hour)

```bash
# READMEs
git mv README_Disclosure.md README-Disclosure.md
ln -s README-Disclosure.md README_Disclosure.md

git mv README_QC.md README-QC.md
ln -s README-QC.md README_QC.md

cd qc-reports

git mv cse110_qc_report.md cse110-qc-report.md
ln -s cse110-qc-report.md cse110_qc_report.md

git mv cse110_v3_qc_report.md cse110-v3-qc-report.md
ln -s cse110-v3-qc-report.md cse110_v3_qc_report.md

git mv ds150_qc_report.md ds150-qc-report.md
ln -s ds150-qc-report.md ds150_qc_report.md

git mv ds250_qc_report.md ds250-qc-report.md
ln -s ds250-qc-report.md ds250_qc_report.md

git mv ds250_rewritten_qc_report.md ds250-rewritten-qc-report.md
ln -s ds250-rewritten-qc-report.md ds250_rewritten_qc_report.md

git mv march_madness_agent_qc_report.md march-madness-agent-qc-report.md
ln -s march-madness-agent-qc-report.md march_madness_agent_qc_report.md

git mv ME342_TA_qc_report_v2.md ME342-TA-qc-report-v2.md
ln -s ME342-TA-qc-report-v2.md ME342_TA_qc_report_v2.md

cd ..
git add README*.md qc-reports/*.md
```

**Commit**:
```bash
git commit -m "Phase 6: Rename READMEs and QC reports to kebab-case"
git push
```

---

### Phase 7: Verification & Documentation (1 hour)

**Verification checklist**:
- [ ] All old paths still work via symlinks
- [ ] All new paths resolve correctly
- [ ] Git log follows renamed files (`git log --follow <file>`)
- [ ] No broken links in .md files
- [ ] AGENTS.md structure tree updated
- [ ] README.md structure tree updated
- [ ] .gitignore patterns still match

**Create migration completion notice**:
```bash
# Update AGENTS.md with migration notice
# Document symlink removal timeline (6-12 months)
# Notify downstream repos
```

**Commit**:
```bash
git commit -m "Phase 7: Document kebab-case migration completion"
git push
```

---

### Phase 8: Symlink Removal (6-12 months later)

**When**: After all downstream repos have updated their references

**How**:
```bash
# Remove all symlinks
find . -type l -name "*_*" -delete

git add -A
git commit -m "Remove snake_case symlinks after migration grace period"
git push
```

---

## Risk Assessment & Mitigation

### Risk 1: Broken Git History
**Impact**: `git log make-agent.md` won't show pre-rename history
**Mitigation**: Use `git log --follow make-agent.md` (follows renames)
**Severity**: Low (git handles renames well with `git mv`)

### Risk 2: Downstream Breakage
**Impact**: Repos referencing old file names break
**Mitigation**: Symlinks provide backward compatibility
**Severity**: Zero (with symlinks in place)

### Risk 3: Missed References
**Impact**: Some internal references stay snake_case
**Mitigation**: Automated grep validation after each phase
**Severity**: Medium (annoying but fixable)

### Risk 4: Merge Conflicts
**Impact**: Anyone with PRs in flight gets conflicts
**Mitigation**: Coordinate timing, announce in advance
**Severity**: Medium (no active PRs currently)

### Risk 5: Python Import Breakage
**Impact**: `fetch_doc.py` imports might break
**Mitigation**: Python file stays as-is (Python uses snake_case)
**Severity**: Zero (no rename needed)

---

## Reference Update Strategy

### Automated Find/Replace Patterns

After renaming files, use these patterns to update references:

```bash
# Phase 1: Core templates
find . -name "*.md" -type f -exec sed -i '' 's/make_agent\.md/make-agent.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/make_agent_qc\.md/make-agent-qc.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/make_agent_knowledge\.md/make-agent-knowledge.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/make_AGENTS_qc\.md/make-AGENTS-qc.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/make_orchestrator_agent\.md/make-orchestrator-agent.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/make_managed_agent\.md/make-managed-agent.md/g' {} +

# Phase 2: Knowledge files
find . -name "*.md" -type f -exec sed -i '' 's/behavioral_discipline\.md/behavioral-discipline.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/hermes_comparison\.md/hermes-comparison.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/source_docs_index\.md/source-docs-index.md/g' {} +
find . -name "*.md" -type f -exec sed -i '' 's/mcp_integration_patterns\.md/mcp-integration-patterns.md/g' {} +

# Phase 3: Folders
find . -name "*.md" -type f -exec sed -i '' 's|make_gems/|make-gems/|g' {} +
find . -name "*.md" -type f -exec sed -i '' 's|update_agents/|update-agents/|g' {} +
find . -name "*.md" -type f -exec sed -i '' 's|qc_reports/|qc-reports/|g' {} +
find . -name "*.md" -type f -exec sed -i '' 's|source_docs/|source-docs/|g' {} +
find . -name "*.md" -type f -exec sed -i '' 's|\.github_issues/|.github-issues/|g' {} +

# Phase 4-6: Agent files, gems, READMEs
# (Similar patterns for each phase)
```

**Verification after each sed**:
```bash
# Check diff before committing
git diff

# Spot-check critical files
cat AGENTS.md | grep -E "make_|update_|source_"
```

---

## Testing Strategy

### After Each Phase

1. **Link resolution test**:
   ```bash
   # Test that all markdown links resolve
   # (Manual spot-check or use markdown link checker)
   ```

2. **Symlink test**:
   ```bash
   # Verify old paths work
   cat make-agent.md  # Should resolve via symlink
   cat make-agent.md  # Should resolve to actual file
   ```

3. **Git history test**:
   ```bash
   git log --follow make-agent.md  # Should show full history
   ```

4. **Reference completeness**:
   ```bash
   # Grep for any remaining snake_case references
   grep -r "make_agent\.md" --include="*.md" .
   grep -r "update_agents/" --include="*.md" .
   ```

---

## Decision Points

### 1. AGENTS capitalization in make_AGENTS.md
**Options**:
- A: `make-AGENTS.md` (preserve capitalization)
- B: `make-agents.md` (full lowercase)

**Recommendation**: **Option A** - AGENTS is a proper name/acronym, preserve capitalization

### 2. Date-stamped files in handoffs/
**Current**: `2026-05-28_topic.md`
**Recommendation**: **Keep as-is** - Date format convention uses hyphens already, not snake_case

### 3. Python files (fetch_doc.py)
**Current**: `fetch_doc.py`
**Recommendation**: **Keep as-is** - Python ecosystem uses snake_case

### 4. .github_issues folder
**Current**: `.github_issues`
**Recommendation**: **Rename to `.github-issues`** - It's a directory name, not a Python module

### 5. Git commit granularity
**Options**:
- A: 1 massive commit
- B: 7 commits (one per phase)

**Recommendation**: **Option B** - Easier to review, revert if needed

---

## Timeline & Effort Estimate

| Phase | Hours | Risk Level | Can Pause? |
|-------|-------|------------|------------|
| 1. Core templates | 2-3 | Low | Yes |
| 2. Knowledge files | 2-3 | Low | Yes |
| 3. Folders | 3-4 | Medium | Yes |
| 4. Update agents | 1-2 | Low | Yes |
| 5. Make gems | 1-2 | Low | Yes |
| 6. READMEs & QC | 1 | Low | Yes |
| 7. Verification | 1 | Low | No |
| **TOTAL** | **11-17 hours** | **Medium** | - |

**Recommended schedule**:
- Week 1: Phases 1-3 (7-10 hours)
- Week 2: Phases 4-7 (4-7 hours)

Or complete in one focused session if preferred.

---

## Downstream Communication

**Repos to notify after Phase 7**:

1. **canvas-toolbox**: References make-agent pattern
2. **gh-issues-agent**: May have file path references
3. **handoff**: AGENTS_snippet.md references
4. **5 master repos**: May reference structure

**Message template**:
```
Make-AI-Agents has migrated to kebab-case for all .md files.

Old paths still work via symlinks (grace period: 6-12 months).
New canonical paths use hyphens:
- make-agent.md → make-agent.md
- update_agents/ → update-agents/
- behavioral_discipline.md → behavioral-discipline.md

Update your references when convenient. Symlinks will be removed after [date].
```

---

## Rollback Plan

If critical issues discovered mid-migration:

```bash
# Revert to pre-migration state
git revert <commit-hash>
git push

# Or reset to specific phase
git reset --hard <phase-N-commit>
git push --force-with-lease
```

**Symlinks make rollback safe** - old references continue working.

---

## Post-Migration Maintenance

### Symlink Removal Checklist (6-12 months later)

Before removing symlinks:
- [ ] All downstream repos notified
- [ ] Grace period elapsed (6+ months)
- [ ] No recent references to old paths in logs
- [ ] All known consumers updated

### Future File Naming

**Standard going forward**:
- All new .md files: kebab-case
- All new folders: kebab-case
- Python files: snake_case
- Special files: UPPERCASE

---

## Conclusion

**Go/No-Go Decision**:

**Recommend: GO** ✅

**Reasoning**:
1. This is the last repo requiring migration (ecosystem alignment)
2. Symlink approach provides safety net
3. Phased execution allows pause/resume
4. 11-17 hours is manageable over 1-2 weeks
5. Risk is medium but well-mitigated

**Next step**: Execute Phase 1 (Core Templates) or defer to dedicated sprint

---

**Created**: 2026-07-08
**Author**: Claude Code
**Status**: Ready for execution
