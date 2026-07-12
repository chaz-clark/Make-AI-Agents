---
title: Trunk-Based Development
description: Single-branch development workflow for continuous integration
sources:
  - https://martinfowler.com/articles/branching-patterns.html
  - https://trunkbaseddevelopment.com/
  - https://martinfowler.com/articles/continuousIntegration.html
last_updated: 2026-07-10
---

# Trunk-Based Development

> A source control branching model where developers collaborate on code in a single branch called "trunk" (or "main"), resist any pressure to create long-lived development branches, and employ documented techniques to achieve larger changes.

---

## What This Is

**Trunk-Based Development (TBD)** is synonymous with **Continuous Integration (CI)** — both emphasize frequent integration into a shared mainline rather than long-lived feature branches.

**The core principle:** Everyone commits to the mainline every day. More precisely: developers should never have more than a day's work sitting unintegrated in their local repository.

**Why it works:** Small, frequent merges are substantially easier to manage than occasional large integrations. Frequent integration surfaces conflicts immediately — before they compound into expensive problems.

---

## The Counter-Intuitive Rule

> "If it hurts... do it more often."

High-frequency integration dramatically reduces merge complexity and risk. Research from the State of DevOps Report found that elite teams integrate notably more frequently than low performers, correlating integration frequency with higher software delivery performance and organizational profitability.

---

## Operational Practices

### Daily Integration Cycle

Every developer, every day:

1. **Pull** current mainline into local repository
2. **Merge** changes with colleague contributions
3. **Build & test** — run automated build and test suite (commit suite)
4. **Push** changes back to mainline
5. **Only after push is integration complete** — pulling alone doesn't integrate

**Critical timing:** Integration happens when you push to mainline, not when you pull. The local merge is preparation; the push is commitment.

### Pre-Integration Discipline

Before committing/pushing to trunk:

- Perform full "pre-integrate" build on dev workstation (compile, unit tests, integration tests)
- Verify all tests pass locally
- Never push broken code to mainline
- Build servers verify commits "have not broken the build" after landing

### Mainline Health

**Main must always work.** This is the non-negotiable rule.

- Trunk stays in **releasable health state** at all times
- If a commit breaks the build, fixing it is the top priority (stop-the-line)
- Self-testing code with comprehensive automated tests
- Deployment pipelines catch defects quickly

**A red trunk is the one thing to avoid.**

---

## Branch Patterns

### For Solo Developers or Very Small Teams

**Direct commits to trunk.** No feature branches needed — the overhead isn't worth it.

```bash
# Make change
git add .
git commit -m "..."
git push origin main
```

### For Larger Teams

**Short-lived feature branches** for code review and build checking:

- Branch lifespan: **hours, not days** (typically < 24 hours)
- Branch is "the product of a single dev-workstation" (not shared)
- Delete immediately after merging
- Use pull requests for code review and CI verification

```bash
# Create short-lived branch
git checkout -b fix-validation
# Make focused change
git add .
git commit -m "..."
git push origin fix-validation
# Open PR, get review, merge, delete branch
gh pr create --title "Fix validation" --base main
gh pr merge --squash --delete-branch
```

### Release Branches (Optional)

Two patterns:

1. **Just-in-time release branches:** Cut from trunk when ready to release, "harden" (bug fixes only), then delete after release
2. **Release from trunk:** High-throughput teams release directly from main using "fix forward" strategies for bugs

---

## What to Avoid: Anti-Patterns

### ❌ Long-Lived Development Branches

**Don't:**
- Create permanent development branches (dev, staging, etc.)
- Keep feature branches open for weeks/months
- Use shared branches off mainline at any release cadence

**Why:** They accumulate merge debt and delay conflict discovery until it's expensive to resolve.

### ❌ Batched Integration ("I'll push at the end of the session")

**Don't:**
- Accumulate multiple commits locally before pushing
- Wait until "everything is done" to integrate
- Leave commits sitting in local working tree

**Why:** Local-only commits are not backed up, not visible to the team, and create multi-week debt that surfaces as "23 commits ahead of origin."

### ❌ Merge Hell

**Don't:**
- Delay integration until feature completion
- Work in isolation for extended periods
- Accumulate large changesets before merging

**Why:** The longer you wait, the more painful integration becomes. Frequency is the antidote to merge pain.

---

## Techniques for Larger Changes

When changes genuinely need days/weeks to complete:

### Branch by Abstraction

Introduce an abstraction layer, migrate incrementally behind the abstraction, then remove the old implementation — all while keeping main green.

**Example:** Replacing a database layer:
1. Introduce abstraction interface
2. Implement new database layer behind interface
3. Gradually migrate code to use abstraction
4. Remove old implementation
5. Each step commits to main

### Feature Flags

Deploy incomplete features to production behind toggles:

```python
if feature_flags.new_grading_engine:
    return new_grading_engine.grade(submission)
else:
    return legacy_grader.grade(submission)
```

- Code goes to main immediately
- Feature activates when ready
- Can roll back by flipping flag (no code deployment)

---

## Critical Dependencies

Trunk-based development requires:

1. **Self-testing code** — comprehensive automated test suite
2. **Fast build/test cycles** — commit suite runs in minutes, not hours
3. **Deployment pipeline** — CI/CD catches defects quickly
4. **Trusted team** — everyone committed to keeping main green
5. **Good modularity** — "Feature branching is a poor man's modular architecture" (if your architecture requires branching, fix the architecture)

---

## Comparison: Trunk-Based vs. Feature Branching

| Factor | Trunk-Based Development | Feature Branching |
|--------|-------------------------|-------------------|
| Integration trigger | Hourly/daily progress | Feature completion |
| Merge complexity | Small, manageable | Large, risky |
| Conflict detection | Immediate | Delayed |
| Refactoring | Encouraged (continuous) | Discouraged (merge risk) |
| Release readiness | Constant | Intermittent |
| Mental model | "Main is truth" | "Many sources of truth" |
| Time to wrong answer | Slower (more checking) | Faster |
| Time to right answer | Faster (no rework) | Slower (rework loops) |

---

## When Feature Branching Makes Sense

**Context matters.** Trunk-based development works best within:

- Full-time, trusted teams
- Shared codebase ownership
- Commitment to healthy codebases
- Fast feedback loops

**Feature branching is appropriate for:**

- Open-source projects with occasional contributors
- External contributions requiring pre-integration review
- Teams without trust relationships established
- Projects without automated testing infrastructure

---

## The P-008 Connection

Canvas-toolbox's **P-008 (Standard Work for commits)** operationalizes trunk-based development:

```bash
# P-008 pattern: commit + push as atomic operation
git add . && git commit -m "..." && git push
```

**Why:** Local-only commits violate the trunk-based principle. Integration happens when you push. Commits without pushes accumulate as hidden technical debt.

**Goal:** `git log --branches --not --remotes` shows **zero commits** at all times.

---

## Migration Path

If your team isn't doing trunk-based development yet:

1. **Start measuring integration frequency** — how often does each developer push to main?
2. **Reduce branch lifespan** — aim for < 24 hours, then < 8 hours
3. **Invest in test automation** — trunk-based development without tests is reckless
4. **Speed up CI/CD** — slow pipelines discourage frequent integration
5. **Cultural shift** — "main always works" becomes team religion

**If you can't keep main releasable yet:** Use release branches temporarily while building toward continuous delivery capability. But keep main as your integration point — don't create permanent development branches as a workaround.

---

## Key Quotes

> "Everyone commits to the mainline every day." — Martin Fowler

> "If it hurts, do it more often." — Counter-intuitive rule for integration

> "Feature branching is a poor man's modular architecture." — If you need branches to manage complexity, fix the architecture

> "A red trunk is the one thing to avoid." — Mainline health is non-negotiable

---

## Further Reading

- **Martin Fowler: Patterns for Managing Source Code Branches**
  https://martinfowler.com/articles/branching-patterns.html

- **Martin Fowler: Continuous Integration**
  https://martinfowler.com/articles/continuousIntegration.html

- **Trunk Based Development (trunkbaseddevelopment.com)**
  https://trunkbaseddevelopment.com/

- **State of DevOps Report** — Research linking integration frequency to delivery performance
