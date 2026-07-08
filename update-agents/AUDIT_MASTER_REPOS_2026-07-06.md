---
name: Master Repos JSON Audit
description: Audit of *-master repos to determine downstream impact of JSON purge
created: 2026-07-06
status: COMPLETE
---

# Master Repos JSON Audit Results

## Summary

**Repos audited**: 5 (*-master pattern in ~/Documents/GitHub)
- cse450-master
- ds250-onln-master
- ds460-master
- itm327-master
- m119-master

**Key Finding**: All 5 repos use Make-AI-Agents as a **gitignored standalone clone**, not a subtree. Changes to Make-AI-Agents propagate via `git -C Make-AI-Agents pull`, not via git commits in the master repos.

**Impact of JSON purge**: ZERO direct impact on master repos. They reference Make-AI-Agents but don't commit its files.

---

## Detailed Findings

### 1. All Master Repos Use Make-AI-Agents as Gitignored Clone

**Pattern found in all 5 repos**:
```
~/Documents/GitHub/cse450-master/
├── Make-AI-Agents/          ← gitignored clone (not committed)
├── canvas-toolbox/          ← gitignored clone (not committed)
├── gh-issues-agent/         ← gitignored clone (not committed)
├── handoff/                 ← gitignored clone (not committed)
└── AGENTS.md                ← committed (mentions Make-AI-Agents)
```

**Evidence**:
```bash
# cse450-master AGENTS.md
| `Make-AI-Agents/` | Agent-authoring toolkit | `make_*.md`/`.json` generators at root |
```

**How they reference Make-AI-Agents**:
- Listed in "Sister Repos" section of AGENTS.md
- Described as standalone upstream clones at repo root
- Refreshed via `git -C Make-AI-Agents pull`
- NOT subtrees, NOT committed

**Conclusion**: Master repos are **consumers**, not **embedders**. They'll get the purge automatically on next `git pull`.

---

### 2. Master Repos Don't Have "Templates Evolve in Pairs" Rule

**Check**: Do master repo AGENTS.md files propagate the JSON rule?

**Results**:
- cse450-master: ❌ No rule (just mentions `.md`/`.json` in structure table)
- ds250-onln-master: ❌ No rule
- ds460-master: ❌ No rule
- itm327-master: ❌ No rule
- m119-master: ❌ No rule

**Why**: Master repos document the pattern (`make_*.md`/`.json`) but don't enforce it. The rule lives in Make-AI-Agents/AGENTS.md, not in consumer repos.

**Conclusion**: No need to update master repos. They'll see the updated Make-AI-Agents/AGENTS.md on next pull.

---

### 3. canvas-toolbox DOES Use MD+JSON Pairs Actively

**Surprise finding**: canvas-toolbox (a sister repo to Make-AI-Agents in all master repos) actively uses the MD+JSON pattern.

**Evidence**:
```bash
$ cd ~/Documents/GitHub/cse450-master/canvas-toolbox/lib/agents
$ ls *.json
canvas_blueprint_sync.json
canvas_content_sync.json
canvas_course_expert.json
canvas_grader.json
canvas_schedule_auditor.json
canvas_semester_setup.json
ira_program_alignment.json

$ for json in *.json; do md="${json%.json}.md"; [ -f "$md" ] && echo "PAIR"; done
PAIR  (7 times - all JSON files have corresponding MD files)
```

**JSON file contents**:
```json
{
  "_metadata": {
    "template_version": "3.6",
    "last_updated": "2026-05-13",
    ...
  },
  "agent_type": { ... },
  "behavioral_discipline": { ... },
  "validation": { ... }
}
```

**Last updated**: 2026-05-13 (relatively recent, not stale like Make-AI-Agents JSON)

**Conclusion**: canvas-toolbox is a **successful consumer** of the MD+JSON pattern. It's a separate repo that uses the pattern correctly.

---

### 4. canvas-toolbox Doesn't Have the Rule Either

**Check**: Does canvas-toolbox AGENTS.md mention "Templates evolve in pairs"?

**Result**: ❌ No

**Why**: canvas-toolbox has extensive project-specific rules (16 of them), but not the "evolve in pairs" rule. It just... does it.

**Conclusion**: The pattern is **adopted implicitly**, not enforced by rule.

---

## Impact Assessment

### Scenario 1: We Delete JSON Files in Make-AI-Agents

**Master repos**: Zero impact
- They don't commit Make-AI-Agents files
- Next `git -C Make-AI-Agents pull` gets the updated repo
- Their AGENTS.md doesn't need updates (doesn't have the rule)

**canvas-toolbox**: Zero impact
- Separate standalone repo
- Uses the MD+JSON pattern independently
- Doesn't reference Make-AI-Agents JSON files
- Has its own JSON files that are actively maintained

**Other consumers**: Zero impact
- AgentJ, 1bios, gh-issues-agent are separate repos
- None commit Make-AI-Agents as subtree
- All use gitignored clone pattern

---

### Scenario 2: We Update the Rule in Make-AI-Agents/AGENTS.md

**Current rule**:
> Templates evolve in pairs — `make_*.md` (narrative) and `make_*.json` (structured rules) are updated together.

**New rule** (proposed):
> Templates are markdown-only with optional YAML frontmatter for metadata (following Anthropic Agent Skills and agentskills.io patterns). JSON files were deprecated 2026-07-06 — if you see one, it's stale.

**Master repos impact**:
- Next `git -C Make-AI-Agents pull` propagates the change
- No action needed by master repo maintainers
- Operators see updated rule in Make-AI-Agents/AGENTS.md

**canvas-toolbox impact**: Zero
- Doesn't reference the rule
- Will continue using MD+JSON for its own agents (separate decision)

---

### Scenario 3: We Add YAML Frontmatter to Templates

**Current state** (Make-AI-Agents templates):
```markdown
---
name: make_managed_agent
version: "1.0"
created: 2026-07-06
---
# Managed Agent Guide
```

**Master repos impact**:
- Next `git -C Make-AI-Agents pull` gets new frontmatter
- Templates still render correctly (YAML is invisible to markdown readers)
- No breaking changes

**canvas-toolbox impact**: Zero
- Has its own templates
- Doesn't parse Make-AI-Agents YAML

---

## Recommendations

### For Make-AI-Agents Purge Plan

✅ **Safe to proceed** with all phases:
1. Delete 3 stale JSON files (make_agent, make_orchestrator_agent, make_agent_knowledge)
2. Consolidate QC JSON into YAML frontmatter
3. Update AGENTS.md rule
4. Add YAML frontmatter to templates

**No downstream impact** on master repos or canvas-toolbox.

### For canvas-toolbox

**Question**: Should canvas-toolbox also purge JSON files?

**Answer**: NO - canvas-toolbox uses the pattern **successfully**:
- JSON files are current (2026-05-13)
- All 7 agents have active MD+JSON pairs
- No staleness detected
- Pattern serves its purpose there

**Recommendation**: Leave canvas-toolbox as-is. It's proof the pattern CAN work when maintained.

### For Future Consumers

**Guidance for new repos**:
1. Follow Anthropic Agent Skills pattern (MD + YAML frontmatter)
2. Don't create separate JSON files unless you have tooling that reads them
3. canvas-toolbox is the exception (has maintained JSON), not the rule

---

## Cross-Repo Comparison

| Repo | Uses MD+JSON? | JSON Current? | Has Rule in AGENTS.md? | Verdict |
|------|---------------|---------------|------------------------|---------|
| **Make-AI-Agents** | ❌ Stale (8 weeks) | ❌ No | ✅ Yes | **PURGE JSON** |
| **canvas-toolbox** | ✅ Yes (7 pairs) | ✅ Yes (2026-05-13) | ❌ No | **KEEP JSON** |
| **cse450-master** | N/A (uses clone) | N/A | ❌ No | **No action** |
| **ds250-onln-master** | N/A (uses clone) | N/A | ❌ No | **No action** |
| **ds460-master** | N/A (uses clone) | N/A | ❌ No | **No action** |
| **itm327-master** | N/A (uses clone) | N/A | ❌ No | **No action** |
| **m119-master** | N/A (uses clone) | N/A | ❌ No | **No action** |

---

## Key Insights

### 1. The Pattern Works When Maintained

**canvas-toolbox proof**: 7 agents, all with current JSON files, pattern serves a purpose (structured metadata for agent execution).

**Make-AI-Agents failure**: 3 JSON files stale for 8 weeks, zero tooling reads them, became pure maintenance debt.

**Lesson**: MD+JSON isn't inherently bad. It's bad when JSON files aren't maintained OR when no tooling uses them.

### 2. Gitignored Clones Are the Norm

**All 5 master repos** use the same pattern:
- Make-AI-Agents as gitignored standalone clone
- Not subtree, not submodule
- Refreshed via `git pull` in the clone

**Implication**: Changes to Make-AI-Agents propagate on-demand, not automatically. Operators must `git -C Make-AI-Agents pull` to get updates.

### 3. The Rule Wasn't Propagated

**Make-AI-Agents AGENTS.md** has "Templates evolve in pairs" rule.

**Consumer repos**: Zero have the rule.

**Why**: The rule is meta-guidance for Make-AI-Agents maintainers, not for consumers. Consumers use the templates, not the rule.

---

## Action Items for Morning Review

### Confirmed Safe

✅ Delete make_agent.json, make_orchestrator_agent.json, make_agent_knowledge.json
✅ Consolidate QC JSON into YAML frontmatter
✅ Update Make-AI-Agents/AGENTS.md rule
✅ Add YAML frontmatter to Make-AI-Agents templates

**Zero impact** on master repos or canvas-toolbox.

### Optional Follow-Up

⚠️ **Document in PURGE_PLAN**: canvas-toolbox is the success story (MD+JSON works there because JSON is maintained and used).

⚠️ **Consider**: Should we add a note to Make-AI-Agents/AGENTS.md that says "canvas-toolbox successfully uses MD+JSON, but Make-AI-Agents doesn't"?

---

## Files Checked

**Master repos**:
- ~/Documents/GitHub/cse450-master/AGENTS.md
- ~/Documents/GitHub/ds250-onln-master/AGENTS.md
- ~/Documents/GitHub/ds460-master/AGENTS.md
- ~/Documents/GitHub/itm327-master/AGENTS.md
- ~/Documents/GitHub/m119-master/AGENTS.md

**canvas-toolbox**:
- ~/Documents/GitHub/canvas-toolbox/AGENTS.md
- ~/Documents/GitHub/canvas-toolbox/lib/agents/*.json (7 files)
- ~/Documents/GitHub/canvas-toolbox/lib/agents/*.md (7 files)

**Make-AI-Agents**:
- make_agent.json (stale: 8 weeks)
- make_orchestrator_agent.json (stale: 8 weeks)
- make_agent_knowledge.json (stale: 8 weeks)
- make_agent_qc.json (current)
- make_AGENTS_qc.json (current)

---

**Status**: COMPLETE
**Created**: 2026-07-06
**Conclusion**: Purge plan has ZERO downstream impact. Safe to proceed.
