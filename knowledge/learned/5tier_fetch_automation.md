---
name: 5-tier hierarchical fetch for documentation automation
observed_in: 2026-07-06 documentation refresh (65 sources, 32 new)
confidence: high
---

# Lesson: 5-Tier Hierarchical Fetch System

## What Happened

Built a 5-tier fetch system for refreshing AI platform documentation sources. Achieved 98.5% automation rate (64 of 65 sources fetched automatically, 1 manual).

## The Pattern

**Tier 1: GitHub API** → Direct markdown fetch for `*.github.io` domains
**Tier 2: HTTP + html2text** → Standard web scraping with content selectors
**Tier 3: Playwright** → Headless browser for JS-rendered SPAs
**Tier 4: Manual logging** → Log failures to `_manual_needed.json` with clear instructions
**Tier 5: Downloads scanner** → Auto-match manually saved HTML files and convert

## Why It Worked

1. **Graceful fallback**: Each tier has a specific failure mode that triggers the next tier
2. **Detect-then-escalate**: Tier 2 detects JS-shells (HTML <2KB, markdown <500 bytes, "loading" keywords) and automatically tries Tier 3
3. **User-friendly manual path**: When all automation fails, log with clickable URL and exact steps for manual save
4. **Auto-recovery**: Tier 5 matches manually saved files and processes them without re-prompting

## Results

- **OpenAI** (12 sources): 100% via Tier 1 (GitHub API)
- **Google Gemini/ADK** (27 sources): 96% via Tier 2 (HTTP), 4% via Tier 3 (Playwright)
- **Anthropic** (12 sources): 33% via Tier 2, 67% via Tier 3 (all `platform.claude.com` are React SPAs)
- **xAI** (10 sources): 100% via Tier 2/manual
- **Nous Hermes** (1 source): 100% via Tier 2

## Suggested Rule

**For any multi-source doc refresh workflow**:
1. Start with fastest/cheapest tier (API if available, else HTTP)
2. Build JS-shell detection into HTTP tier (size heuristics + keyword checks)
3. Have Playwright as optional flag (`--enable-playwright`) for known JS-heavy domains
4. Log failures with actionable user instructions (not just error messages)
5. Provide scanner to auto-process manual saves (close the loop)

**Anti-pattern**: Single-tier approaches fail on mixed content (some static HTML, some JS-rendered). Building detection + fallback up-front is cheaper than debugging why 20% of sources return empty.

## Reusability

Pattern applies to:
- ✅ Documentation refresh workflows (any platform docs)
- ✅ Web scraping with mixed static/dynamic targets
- ✅ Data collection where some sources require browser execution
- ❌ NOT for: single-source, known-format scraping (overkill)
