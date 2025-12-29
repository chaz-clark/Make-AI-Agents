# Agent Quality Control (QC) Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `make_agent_qc.json` for structured data, validation checklists, and scoring criteria.
3. This QC agent validates newly created agents for quality, completeness, and adherence to make_agent standards.

---

## Mission (core)

A systematic quality control agent that validates newly created agents against the make_agent template standards.

**What it does**: Analyzes agent MD and JSON files to verify they meet quality standards, are topic-specific, and have removed unused optional sections.

**Why it exists**: Ensures consistency across agent implementations and prevents incomplete or poorly structured agents from being deployed.

**Who uses it**: Agent developers, team leads, and automated CI/CD pipelines performing agent validation.

**Example**: "Analyzes a new SQL validation agent, scores it across 8 quality dimensions, and provides actionable feedback for improvement."

---

## Agent Quickstart (core)

Fast-path workflow for validating an agent:

1. **[Identify]**: Locate the agent's .md and .json files
   - Example: "Find `sql_validator.md` and `sql_validator.json`"

2. **[Parse Structure]**: Load structured validation rules from `make_agent_qc.json`
   - Example: "Load tier requirements, core section checklist, optional section rules"

3. **[Validate]**: Run all quality checks across 8 dimensions
   - Example: "Check completeness, specificity, cleanup, consistency, examples, validation, dependencies, documentation"

4. **[Score]**: Calculate quality scores and identify issues
   - Example: "Generate 0-100 score per dimension with issue details"

5. **[Output]**: Produce validation report with pass/fail and improvement recommendations
   - Example: "Return structured report: 85/100 with 3 critical issues and 5 recommendations"

For detailed validation rules and scoring criteria, see `make_agent_qc.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- ✅ Mission and validation philosophy
- ✅ Quality principles that guide validation
- ✅ How to interpret validation results
- ✅ Common pitfalls in agent creation
- ✅ Educational context on why each check matters

### The JSON File (.json) Contains:
- ✅ Validation checklists (structured as arrays)
- ✅ Scoring rubrics with weights
- ✅ Pattern matching rules for detection
- ✅ Core vs optional section lists
- ✅ Specific test cases and validation methods
- ✅ Error taxonomy and severity levels

**Rule of Thumb**: Validation logic → JSON. Understanding "why" quality matters → MD.

---

## Key Principles (core)

### 1. Completeness Over Perfection
**Description**: All core sections must be present and filled; optional sections should only exist if needed.

**Why**: A minimally complete agent is better than an incomplete complex one. Core sections ensure basic functionality.

**How**: Check all tier_1_core sections exist with non-placeholder content. Verify optional sections are removed if unused.

### 2. Specificity Over Generics
**Description**: Agent content must be specific to its stated purpose, not filled with template placeholders.

**Why**: Generic agents provide no real value. "YourAgent" and "[Description]" indicate incomplete work.

**How**: Detect placeholder patterns, verify examples contain concrete code/data, ensure principles relate to the specific agent domain.

### 3. JSON-MD Separation
**Description**: Structured data belongs in JSON, narrative explanation in MD.

**Why**: Maintains parseability for automated systems while keeping human-readable context separate.

**How**: Verify JSON contains parseable structures (arrays, objects) and MD explains concepts without duplicating structured data.

### 4. Cleanup Discipline
**Description**: Unused sections must be removed, not left as empty placeholders.

**Why**: Bloat confuses users and suggests incomplete work. Clean agents are maintainable agents.

**How**: Detect optional sections marked as unused but still present. Flag sections with only template text.

### 5. Validation Testability
**Description**: Validation sections must contain actionable tests, not aspirational statements.

**Why**: Untestable agents cannot be verified. "Check if it works" is not a test case.

**How**: Ensure validation section includes specific inputs, expected outputs, and verification methods.

---

## How to Use This Agent (core)

### Prerequisites
- Agent files to validate (both .md and .json)
- Access to make_agent template for comparison
- Understanding of agent tier system (tier_1_core, tier_2_recommended, tier_3_optional)

### Basic Usage

**Step 1: Prepare Agent Files**
```bash
# Ensure both files exist in the same directory
ls my_agent.md my_agent.json
```

**Step 2: Load QC Agent**
```python
# Load QC configuration from JSON
from agent_qc import AgentQualityControl
qc = AgentQualityControl.from_config("make_agent_qc.json")
```

**Step 3: Run Validation**
```python
# Validate agent files
result = qc.validate_agent(
    md_path="my_agent.md",
    json_path="my_agent.json"
)
```

**Step 4: Review Results**
```python
# Check validation report
print(f"Overall Score: {result.overall_score}/100")
print(f"Critical Issues: {len(result.critical_issues)}")
print(f"Status: {result.status}")  # PASS, FAIL, or NEEDS_IMPROVEMENT

# Get recommendations
for recommendation in result.recommendations:
    print(f"- {recommendation}")
```

### Advanced Usage

**Automated CI/CD Integration**
```bash
# Run QC in CI pipeline
python agent_qc_cli.py --agent my_agent --strict --output report.json
exit_code=$?
# exit_code 0 = pass, 1 = fail, 2 = needs improvement
```

**Batch Validation**
```python
# Validate multiple agents
agents = ["sql_validator", "data_processor", "api_client"]
results = qc.validate_batch(agents)

# Generate summary report
summary = qc.generate_summary(results)
```

---

## Common Pitfalls and Solutions (core)

### 1. Leaving Optional Sections Empty

**Problem**: Creator marks optional sections as unused but doesn't remove them from JSON.

**Why it happens**: Confusion about whether to delete or set `"optional": true`. Template contains all sections, creator doesn't realize they should delete.

**Solution**: If a section is truly optional and unused, remove the entire section from JSON. Don't just set flags.

**Example**:
```json
// ❌ Wrong - leaving unused section
"common_patterns": {
  "_tier": "tier_3_optional",
  "optional": true,
  "patterns": []
}

// ✅ Correct - remove entirely
// (section not present in file)
```

### 2. Generic Placeholder Content

**Problem**: Agent passes basic structure checks but contains "[Your description here]" or "YourAgentName" placeholders.

**Why it happens**: Creator fills required fields but doesn't replace template content with specifics.

**Solution**: Search for bracket patterns `[...]`, generic names, and template phrases. Replace with actual agent-specific content.

**Example**:
```python
# ❌ Wrong - generic content
"description": "This agent processes data efficiently."
"example": "agent.process(input_data)"

# ✅ Correct - specific content
"description": "This agent validates SQL queries against PostgreSQL 14 syntax rules and security patterns."
"example": "validator.validate('SELECT * FROM users WHERE id = 1', dialect='postgresql')"
```

### 3. JSON-MD Content Duplication

**Problem**: Same code examples or structured data appear in both JSON and MD files.

**Why it happens**: Creator doesn't understand the separation principle and copies content between files.

**Solution**: Code snippets and structured data go in JSON. Narrative explanation and "why" goes in MD. MD should reference JSON, not duplicate it.

**Example**:
```markdown
<!-- ❌ Wrong - duplicating JSON structure in MD -->
## API Endpoints
- /api/v1/process - Processes data
- /api/v2/validate - Validates input

<!-- ✅ Correct - referencing JSON -->
## API Endpoints
For the complete list of API endpoints with parameters and examples, see `my_agent.json` → `primary_data.endpoints`.
```

### 4. Vague Validation Criteria

**Problem**: Validation section says "check if output is correct" without specifying how.

**Why it happens**: Creator doesn't think through actual testing methodology.

**Solution**: Every validation must specify: input, expected output, comparison method, and pass/fail criteria.

**Example**:
```json
// ❌ Wrong - vague validation
{
  "test_cases": [
    {
      "name": "Basic test",
      "input": "test data",
      "expected_output": "correct result"
    }
  ]
}

// ✅ Correct - specific validation
{
  "test_cases": [
    {
      "name": "Valid SQL query detection",
      "input": "SELECT id, name FROM users WHERE active = true",
      "expected_output": {
        "valid": true,
        "dialect": "postgresql",
        "tables": ["users"],
        "warnings": []
      },
      "validation_method": "exact_match",
      "tolerance": {
        "ignore_whitespace": true,
        "case_sensitive": false
      }
    }
  ]
}
```

### 5. Missing Tier Justification

**Problem**: Agent uses tier_3_optional sections but is marked as "simple" complexity.

**Why it happens**: Creator adds sections without considering whether they're actually needed for the agent's complexity level.

**Solution**: Match complexity to sections used. Simple agents should only have tier_1_core. Standard agents add tier_2. Complex agents may need tier_3.

### 6. Penalizing Empty Dependencies for LLM Agents

**Problem**: Flagging empty `packages: []` array as incomplete when the agent is LLM-based and does text analysis only.

**Why it happens**: Assumption that all agents require code packages, without considering that LLM-based agents doing text analysis need no external dependencies.

**Solution**: Understand the agent type before validating dependencies:
- **LLM/text-based agents**: Empty packages array is correct (e.g., SQL grading by text comparison)
- **Code-based agents**: Should list packages with versions
- **Hybrid agents**: May list optional packages for enhanced features

**Example**:
```json
// ✅ Correct for LLM text analysis agent
"dependencies": {
  "packages": [],  // No code execution needed
  "files": ["answer_key.sql"],
  "note": "LLM-based text analysis, no external packages required"
}

// ✅ Correct for Python implementation
"dependencies": {
  "packages": [
    "pandas>=2.0.0",
    "sqlparse>=0.4.0"
  ],
  "files": ["answer_key.sql"]
}
```

**Validation approach**: Note empty packages as informational, not a penalty. Check that dependencies section exists and files are listed appropriately.

---

## Examples (core)

### Example 1: Validating a Simple Agent

**Scenario**: Checking a newly created SQL query validator agent (simple complexity)

**Input**:
```json
{
  "agent_md_path": "sql_validator.md",
  "agent_json_path": "sql_validator.json",
  "strict_mode": false
}
```

**Approach**: QC agent loads both files, checks against `make_agent_qc.json` validation rules for simple agents (tier_1_core only)

**Output**:
```json
{
  "overall_score": 85,
  "status": "NEEDS_IMPROVEMENT",
  "dimension_scores": {
    "completeness": 95,
    "specificity": 70,
    "cleanup": 90,
    "consistency": 85,
    "examples": 75,
    "validation": 90,
    "dependencies": 100,
    "documentation": 80
  },
  "critical_issues": [
    {
      "dimension": "specificity",
      "severity": "medium",
      "issue": "Generic placeholder '[SQL dialect]' found in io_contract.inputs",
      "location": "sql_validator.json:134",
      "recommendation": "Specify supported SQL dialects explicitly (e.g., 'postgresql|mysql|sqlite')"
    }
  ],
  "recommendations": [
    "Add concrete SQL examples in Examples section",
    "Specify PostgreSQL version in dependencies",
    "Remove empty 'common_patterns' section (tier_3_optional not needed for simple agent)"
  ]
}
```

**Code**: See `make_agent_qc.json` → `validation.test_cases` for complete test suite

### Example 2: Complex Agent Validation

**Scenario**: Validating a multi-agent orchestrator (complex)

**Approach**: QC checks tier_1, tier_2, and tier_3 sections are appropriately used and complete. Validates cross-references exist.

**Code**: See `make_agent_qc.json` → `validation_rules.complex_agent_requirements`

### Example 3: CI/CD Pipeline Integration

**Scenario**: Automated agent validation in GitHub Actions

**Approach**: QC runs in strict mode, fails build if score < 80 or critical issues exist

**Code**: See `make_agent_qc.json` → `operational_guidance.ci_integration`

---

## Validation and Testing (core)

### Quick Validation
1. Run QC on a known-good agent: `qc.validate_agent("reference_agent.md", "reference_agent.json")`
2. Verify score is 95+ with no critical issues
3. Test with a deliberately broken agent to ensure detection works

### Comprehensive Validation
For detailed validation procedures, see `make_agent_qc.json` → `validation` section.

The validation section includes:
- Pre-run checklist (QC agent dependencies, reference templates)
- Post-run checklist (report format, score calculations, issue detection)
- Success criteria (score ranges, issue counts)
- Test cases covering all 8 quality dimensions
- Tolerance levels for different agent complexities

### Quality Dimensions Explained

**8 Core Dimensions** (see JSON for scoring rubrics):

1. **Completeness**: All tier_1_core sections present and filled
2. **Specificity**: Content is agent-specific, not generic templates
3. **Cleanup**: Unused optional sections removed
4. **Consistency**: MD and JSON files align, no contradictions
5. **Examples**: Concrete, runnable examples with real data
6. **Validation**: Actionable test cases with clear pass/fail criteria
7. **Dependencies**: All dependencies explicitly listed and versioned
8. **Documentation**: Clear mission, principles, and usage instructions

### Automated Testing
```bash
# Run QC test suite
pytest test_agent_qc.py -v

# Test against reference agents
python test_qc_on_references.py --suite comprehensive
```

---

## Operational Guidance

### When to Use This QC Agent

**Use for**:
- All newly created agents before first deployment
- Agent updates that modify structure or core sections
- Automated CI/CD quality gates
- Pre-merge validation in pull requests
- Periodic audits of existing agent quality

**Don't use for**:
- Validating non-agent documentation
- Checking implementation code (only validates MD/JSON structure)
- Real-time development feedback (too heavyweight)

### Best Practices

1. **Run early and often**: Validate during development, not just before deployment
2. **Use non-strict mode during development**: Strict mode for CI/CD only
3. **Fix critical issues first**: Focus on critical/high severity before medium/low
4. **Iterate on specificity**: First pass often flags generic content
5. **Keep reference agents**: Maintain 100-scoring agents as examples

### Scoring Interpretation

- **95-100**: Excellent, ready for production
- **85-94**: Good, minor improvements needed
- **70-84**: Needs improvement, address recommendations
- **Below 70**: Significant issues, major revision required

### Alternatives

- **Manual review**: Use checklist from JSON for human review
- **Linting tools**: For syntax validation only (doesn't check semantics)
- **Peer review**: Complements automated QC, doesn't replace it

---

## Resources and References

### Agent Files
- **`make_agent_qc.json`**: Validation rules, scoring rubrics, and test cases
- **`make_agent.md`**: Reference template for agent creation
- **`make_agent.json`**: Reference template structure

### Related Agents
See `make_agent_qc.json` → `cross_references.related_agents` for agents that:
- Create new agents (make_agent)
- Deploy agents (agent_deployer)
- Monitor agent performance (agent_monitor)

### External Documentation
- Agent Design Best Practices (internal wiki)
- Tier System Guidelines
- JSON Schema Validation Standards

### How to Use This Documentation System
1. **Start here** (.md) for understanding validation philosophy
2. **Use JSON** for validation rules, scoring rubrics, and test cases
3. **Reference make_agent template** to understand what's being validated
4. **Check example reports** to see what good/bad validation looks like

---

## Contributing and Maintenance

### Updating This QC Agent

**When to update the JSON**:
- Adding new validation rules or checks
- Adjusting scoring weights based on feedback
- Adding test cases for new edge cases
- Updating severity levels for issues

**When to update the MD**:
- Clarifying validation philosophy
- Adding new pitfall examples
- Updating usage guidance
- Improving troubleshooting advice

### Validation Rule Evolution

As agent patterns evolve, update validation rules to match. Keep backward compatibility when possible.

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Validates newly created agents for quality and adherence to standards |
| **Input** | Agent .md and .json file paths |
| **Output** | Validation report with score, issues, and recommendations |
| **Agent Type** | rule_based with structured validation logic |
| **Complexity** | standard |
| **Key Files** | `make_agent_qc.json`, `make_agent_qc.md` |
| **Quickstart** | `qc = AgentQC.from_config('make_agent_qc.json'); result = qc.validate_agent('agent.md', 'agent.json')` |
| **Common Pitfall** | Running in strict mode during active development (too noisy) |
| **Dependencies** | json, re (regex), pathlib |

For detailed information, see sections above and `make_agent_qc.json`.
