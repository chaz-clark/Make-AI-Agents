---
name: JSON to YAML Frontmatter Migration Guide
description: How to consolidate agent JSON files into markdown YAML frontmatter (following Anthropic Agent Skills pattern)
version: "1.0"
created: 2026-07-06
applies_to: [Make-AI-Agents, canvas-toolbox, consumer repos]
---

# JSON to YAML Frontmatter Migration Guide

## Purpose

This guide helps agents and developers migrate from the MD+JSON pair pattern to the industry-standard markdown-with-YAML-frontmatter pattern used by Anthropic Agent Skills, agentskills.io, and Google ADK.

**When to use this guide**:
- You have `agent_name.md` + `agent_name.json` pairs and want to consolidate
- Your JSON files are stale and not maintained
- You want to align with industry standards
- You're cleaning up unmaintained metadata files

**When NOT to use this guide**:
- Your JSON files are actively maintained and used by tooling (keep them!)
- _Update 2026-07-07: canvas-toolbox completed migration to YAML (v1.5.3) after JSON files became stale_

---

## Should You Migrate?

### Decision Tree

**Check 1: Is your JSON file stale?**
```bash
# Compare last update times
git log -1 --format="%ar" your_agent.md
git log -1 --format="%ar" your_agent.json

# If JSON is >4 weeks older than MD: MIGRATE
# If JSON is current: Keep reading
```

**Check 2: Does any tooling read your JSON files?**
```bash
# Search codebase for JSON references
grep -r "your_agent\.json" . --include="*.py" --include="*.sh"

# If zero references: MIGRATE
# If tooling reads it: Keep JSON OR update tooling first
```

**Check 3: Are you maintaining JSON consistently?**
- Do you update JSON every time you update MD?
- Is JSON content actually different from MD content, or duplicated?
- Is anyone consuming the structured JSON data?

**If NO to all checks above: MIGRATE (save yourself the maintenance)**

---

## Industry Context

### What Platforms Use

| Platform | Pattern | Example |
|----------|---------|---------|
| **Anthropic Agent Skills** | MD + YAML frontmatter | `SKILL.md` with `---\nname: pdf\n---` |
| **agentskills.io** | MD + YAML frontmatter | Standard skill format |
| **Google ADK** | MD only | `AGENTS.md`, `SKILL.md` (no frontmatter) |
| **Hermes Agent** | TXT only | `/llms.txt`, `/llms-full.txt` |
| **Make-AI-Agents (old)** | MD + JSON | `make-agent.md` + `make_agent.json` ❌ |
| **Make-AI-Agents (new)** | MD + YAML frontmatter | `make-agent.md` with YAML ✅ |

**Conclusion**: Zero major platforms use separate JSON files. YAML frontmatter is industry standard.

---

## Migration Steps

### Phase 1: Audit Your JSON Files (15 min)

**For each JSON file, extract**:

1. **Metadata** (always keep - goes to YAML frontmatter):
   ```json
   {
     "_metadata": {
       "template_version": "3.6",
       "last_updated": "2026-05-13",
       "description": "..."
     }
   }
   ```

2. **Structured validation rules** (decision point):
   ```json
   {
     "validation": {
       "pre_run_checklist": [...],
       "commands": [...]
     }
   }
   ```
   - If used by tooling: Keep in JSON OR convert to inline code blocks
   - If never used: Delete

3. **Duplicated content** (delete - already in MD):
   ```json
   {
     "agent_type": {
       "description": "Same as in the MD file..."
     }
   }
   ```

**Create a checklist**:
```markdown
## JSON Audit: agent_name.json

- [ ] Metadata extracted (goes to YAML)
- [ ] Validation rules assessed (keep/convert/delete)
- [ ] Duplicate content identified (delete)
- [ ] Novel JSON-only content identified (decision needed)
```

---

### Phase 2: Add YAML Frontmatter to Markdown (30 min)

**Before** (`agent_name.md`):
```markdown
# Agent Name

Mission: Do the thing.

## How to Use
...
```

**After** (`agent_name.md` with YAML frontmatter):
```markdown
---
name: agent_name
version: "3.6"
last_updated: 2026-05-13
description: One-sentence description of what this agent does
complexity: standard
agent_type: workflow
platforms: [Anthropic, Google, OpenAI]
dependencies:
  - behavioral_discipline
  - make_agent
see_also:
  - source_docs/relevant_doc.md
  - knowledge/relevant_knowledge.md
---

# Agent Name

Mission: Do the thing.

## How to Use
...
```

**What goes in YAML frontmatter**:
- ✅ `name` (required) - kebab-case identifier
- ✅ `version` (required) - semantic version
- ✅ `last_updated` (required) - YYYY-MM-DD
- ✅ `description` (required) - one sentence
- ✅ `complexity` (optional) - simple|standard|complex
- ✅ `agent_type` (optional) - workflow|llm_agent|orchestrator|etc
- ✅ `platforms` (optional) - list of supported platforms
- ✅ `dependencies` (optional) - required files/agents
- ✅ `see_also` (optional) - related documentation

**What does NOT go in YAML frontmatter**:
- ❌ Long descriptions (keep in markdown body)
- ❌ Code examples (keep in markdown body)
- ❌ Validation rules (convert to inline code blocks OR separate script)
- ❌ Full schemas (too verbose for frontmatter)

---

### Phase 3: Handle Validation Rules (varies)

**Option A: Convert to Inline Code Blocks** (recommended for docs)

**Before** (in JSON):
```json
{
  "validation": {
    "pre_run_checklist": [
      "Agent spec includes behavioral_discipline section",
      "All tools are documented",
      "Examples provided"
    ]
  }
}
```

**After** (in markdown):
```markdown
## Validation Checklist

- [ ] Agent spec includes behavioral_discipline section
- [ ] All tools are documented
- [ ] Examples provided
```

**Option B: Convert to Executable Script** (if used by tooling)

Create `tools/validate_agent.py`:
```python
#!/usr/bin/env python3
"""Validation rules for agent_name."""

CHECKS = [
    "Agent spec includes behavioral_discipline section",
    "All tools are documented",
    "Examples provided"
]

def validate(agent_md_path: str) -> bool:
    content = open(agent_md_path).read()
    results = []

    # Check 1: behavioral_discipline section
    if "## Behavioral Discipline" in content:
        results.append("✅ Has behavioral_discipline section")
    else:
        results.append("❌ Missing behavioral_discipline section")

    # ... more checks

    return all("✅" in r for r in results)

if __name__ == "__main__":
    import sys
    valid = validate(sys.argv[1])
    sys.exit(0 if valid else 1)
```

**Option C: Delete** (if never used)

If `grep -r "validation" .` shows zero references to these rules, just delete them.

---

### Phase 4: Delete JSON File (5 min)

**After confirming**:
1. ✅ YAML frontmatter added to MD
2. ✅ All useful JSON content migrated or deleted
3. ✅ No tooling reads the JSON file

**Delete**:
```bash
git rm agent_name.json
git commit -m "Migrate agent_name.json to YAML frontmatter

Consolidates metadata into agent_name.md following Anthropic Agent Skills pattern.

Changes:
- Added YAML frontmatter with name, version, description
- Converted validation checklist to markdown checklist
- Deleted duplicate content (agent_type description already in MD)

Zero breaking changes - no tooling read the JSON file."
git push
```

---

## Real Example: make_agent.json → make-agent.md

### Before (Separate Files)

**make_agent.json** (525 lines):
```json
{
  "_metadata": {
    "template_version": "3.1",
    "last_updated": "2025-02-05",
    "description": "NGAI agent template...",
    "tier_guidance": {
      "tier_1_core": "Essential for any agent...",
      "tier_2_recommended": "For production...",
      "tier_3_optional": "Only if needed..."
    }
  },
  "agent_type": {
    "_tier": "tier_1_core",
    "type": "class_based|workflow|...",
    "description": "..."
  },
  "behavioral_discipline": {
    "_tier": "tier_1_core",
    "_required": true,
    "interaction_pattern": "read_only|single_write_workflow|..."
  },
  ...
}
```

**make-agent.md** (narrative guide, no frontmatter)

### After (Consolidated)

**make-agent.md** (with YAML frontmatter):
```markdown
---
name: make_agent
version: "3.1"
last_updated: 2025-02-05
description: NGAI agent template with tier guidance
complexity: standard
tier_guidance:
  tier_1_core: Essential for any agent (agent_type, io_contract, validation)
  tier_2_recommended: For production agents (error_handling, logging, config)
  tier_3_optional: Only if needed (patterns, domain_patterns, tests)
interaction_patterns:
  - read_only
  - single_write_workflow
  - multi_step_batch
  - single_call_api
  - conversational
---

# Make Agent Template

## Mission (core)
...
```

**make_agent.json**: ❌ DELETED (all content migrated to YAML or markdown body)

---

## Common Migration Patterns

### Pattern 1: Metadata Only

**If JSON file is just metadata**, migration is trivial:

```json
{
  "_metadata": {
    "version": "1.0",
    "last_updated": "2026-01-15",
    "description": "Does the thing"
  }
}
```

→ becomes:

```markdown
---
version: "1.0"
last_updated: 2026-01-15
description: Does the thing
---
```

**Effort**: 5 minutes

---

### Pattern 2: Metadata + Validation Rules

**If JSON has metadata + rules**, convert rules to checklist:

```json
{
  "_metadata": { ... },
  "validation": {
    "checks": ["Has tests", "Has examples"]
  }
}
```

→ becomes:

```markdown
---
version: "1.0"
---

# Agent Name

## Validation

- [ ] Has tests
- [ ] Has examples
```

**Effort**: 15 minutes

---

### Pattern 3: Metadata + Schema + Examples

**If JSON has extensive schemas**, consider keeping JSON OR breaking into separate files:

**Option A: Keep JSON** (if actively used by validation tooling)
- Update AGENTS.md to document why JSON is kept
- Commit to maintaining MD+JSON in sync

**Option B: Split into Schema File** (if schemas are reusable)
```
agent_name.md        # Narrative + YAML frontmatter
agent_name_schema.json  # Schemas only (for tooling)
```

**Option C: Inline as Code Blocks** (if schemas are docs, not tooling)
```markdown
---
version: "1.0"
---

# Agent Name

## Input Schema

```json
{
  "type": "object",
  "properties": { ... }
}
```
```

**Effort**: 30-60 minutes

---

## QC-Specific Migration

**Special case**: `make_agent_qc.json` has structured rules that are used for validation.

### Before (make_agent_qc.json)

```json
{
  "qc_checks": {
    "BD-QC-001": {
      "name": "Behavioral Discipline Presence",
      "dimension": "completeness",
      "check": "Agent spec includes behavioral_discipline section",
      "severity": "error"
    },
    "BD-QC-002": { ... }
  }
}
```

### After (make-agent-qc.md with YAML frontmatter)

```markdown
---
name: make_agent_qc
version: "3.1"
rules: 20
dimensions: 17
severity_levels: [error, warning, info]
---

# Make Agent QC

## QC Rules

### BD-QC-001: Behavioral Discipline Presence

**Dimension**: completeness
**Severity**: error
**Check**: Agent spec includes behavioral_discipline section

**Why**: Every agent must embed discipline to ensure consistent quality.

**How to check**:
```bash
grep -q "## Behavioral Discipline" agent_spec.md
```

**Fix**: Add behavioral_discipline section following template.

---

### BD-QC-002: ...
```

**Benefits**:
- Single source of truth
- Human-readable and machine-parseable (can extract rules via regex)
- Follows Anthropic pattern
- Easier to maintain

---

## Post-Migration Checklist

After migrating each agent:

- [ ] YAML frontmatter added to MD file
- [ ] All useful JSON content migrated (metadata, rules, etc.)
- [ ] Duplicate content removed (not copied to both MD and YAML)
- [ ] Validation rules converted to checklist OR script OR deleted
- [ ] No tooling reads the old JSON file (grepped codebase)
- [ ] JSON file deleted via `git rm`
- [ ] Commit message explains migration
- [ ] `git push` executed (commit isn't backup until pushed)

**Optional**:
- [ ] Update AGENTS.md to reflect new pattern
- [ ] Update any documentation that referenced JSON files
- [ ] Notify team/consumers of the change

---

## Rollback Plan

**If migration causes issues**:

1. **Restore JSON file from git history**:
   ```bash
   git checkout HEAD~1 agent_name.json
   git add agent_name.json
   git commit -m "Rollback: restore agent_name.json (migration issue)"
   git push
   ```

2. **Keep YAML frontmatter** (it doesn't hurt):
   - YAML frontmatter is invisible to most markdown readers
   - Doesn't break anything
   - Can coexist with JSON file

3. **Investigate issue**:
   - Was JSON file used by tooling you missed?
   - Did validation break?
   - Did consumers expect JSON format?

---

## Special Cases

### Case 1: canvas-toolbox Agents ✅ MIGRATED

**Previous state** (2026-05-13): canvas-toolbox had 7 agents with maintained MD+JSON pairs.

**Status** (2026-07-07): **MIGRATION COMPLETE** (v1.5.3)

**What happened**:
- 5 JSON files became stale (4 weeks behind MD)
- Followed the migration guide decision tree → MIGRATE
- All 7 agents migrated to YAML frontmatter + embedded YAML blocks
- Updated canvas_api_tool.py parser to read from markdown
- Zero functional changes (all smoke tests pass)

**Results**:
- Eliminated 165KB of JSON files
- Consolidated to single .md file per agent
- Aligned with Anthropic Agent Skills + agentskills.io standard
- Reduced maintenance burden (1 file instead of 2)

**Success story**: This migration proves the guide works for production repos with runtime tooling dependencies.

---

### Case 2: QC Agents (make_agent_qc, make_AGENTS_qc)

**Current state**: Have both .md and .json files, JSON is current.

**Recommendation**: **MIGRATE** (consolidate into YAML)

**Why**:
- QC rules are documentation, not runtime config
- Markdown with YAML frontmatter is easier to maintain
- Industry standard (Anthropic Agent Skills)
- Can still parse rules from markdown (regex extraction)

**Migration effort**: 2-3 hours (careful rule migration)

---

### Case 3: Knowledge Files

**If you have knowledge files with JSON**:

```
behavioral-discipline.md
behavioral_discipline.json
```

**Recommendation**: **CONSOLIDATE**

**Pattern**:
```markdown
---
name: behavioral_discipline
version: "1.4"
principles: 10
interaction_patterns: 5
---

# Behavioral Discipline

## The Ten Principles

### P-001: Read Before Claiming
...
```

**Keep structured data inline**:
```markdown
## Interaction Patterns

| Pattern | When to Use | Discipline Focus |
|---------|-------------|------------------|
| read_only | No writes | Accuracy, citation |
| single_write_workflow | One deliverable | Surface-before-apply |
```

---

## Automation Helper

**Script to audit your JSON files**:

```bash
#!/bin/bash
# audit_json_files.sh - Find stale JSON files

echo "=== JSON File Audit ==="

for json in *.json; do
    md="${json%.json}.md"

    if [ ! -f "$md" ]; then
        echo "❌ ORPHAN: $json (no corresponding .md file)"
        continue
    fi

    # Get last update times
    json_date=$(git log -1 --format="%at" "$json" 2>/dev/null)
    md_date=$(git log -1 --format="%at" "$md" 2>/dev/null)

    if [ -z "$json_date" ] || [ -z "$md_date" ]; then
        echo "⚠️  UNKNOWN: $json (not in git)"
        continue
    fi

    # Calculate age difference (seconds)
    diff=$((md_date - json_date))
    weeks=$((diff / 604800))

    if [ $weeks -gt 4 ]; then
        echo "🔴 STALE: $json is $weeks weeks older than $md → MIGRATE"
    elif [ $weeks -gt 1 ]; then
        echo "🟡 AGING: $json is $weeks weeks older than $md → WATCH"
    else
        echo "🟢 CURRENT: $json is up to date"
    fi

    # Check for references
    refs=$(grep -r "$json" . --include="*.py" --include="*.sh" 2>/dev/null | wc -l)
    if [ $refs -eq 0 ]; then
        echo "   └─ Zero code references (safe to delete)"
    else
        echo "   └─ $refs code references (check before deleting)"
    fi
done
```

**Usage**:
```bash
chmod +x audit_json_files.sh
./audit_json_files.sh
```

---

## FAQ

### Q: Can YAML frontmatter and JSON files coexist?

**A**: Yes, temporarily during migration. YAML frontmatter doesn't break anything. Delete JSON after confirming migration is successful.

---

### Q: What if my JSON file has complex nested structures?

**A**: Three options:
1. **Keep JSON** if tooling actively uses it
2. **Inline as code blocks** if it's documentation
3. **Split into separate schema file** if it's reusable validation

Don't force complex structures into YAML frontmatter.

---

### Q: Will this break my QC agents?

**A**: Only if QC agents specifically parse JSON files. Most QC agents read markdown. Update QC logic to parse YAML frontmatter instead:

```python
import yaml

# Before
with open("agent.json") as f:
    data = json.load(f)
    version = data["_metadata"]["version"]

# After
with open("agent.md") as f:
    content = f.read()
    # Extract YAML frontmatter
    if content.startswith("---"):
        yaml_end = content.find("---", 3)
        frontmatter = yaml.safe_load(content[3:yaml_end])
        version = frontmatter["version"]
```

---

### Q: What about consumers who expect JSON?

**A**: If external consumers read your JSON files, provide migration notice:

1. Add deprecation notice to JSON files (keep for 1 release)
2. Update documentation to reference YAML frontmatter
3. Provide parser example (above)
4. Delete JSON in next major version

---

## Resources

**Industry patterns**:
- [Anthropic Agent Skills](https://docs.anthropic.com/en/agents-and-tools/agent-skills) - YAML frontmatter standard
- [agentskills.io](https://agentskills.io) - Community skill format
- [Google ADK Skills](https://ai.google.dev/gemini-api/docs/managed-agents) - SKILL.md pattern

**Make-AI-Agents specific**:
- `update_agents/PURGE_PLAN_2026-07-06.md` - Our migration plan
- `update_agents/AUDIT_MASTER_REPOS_2026-07-06.md` - Downstream impact assessment
- `knowledge/learned/5tier_fetch_automation.md` - Example of YAML frontmatter usage

---

**Version**: 1.0
**Created**: 2026-07-06
**Applies to**: Any repo using MD+JSON agent pairs
**Author**: Make-AI-Agents (learning from industry migration to YAML frontmatter)
