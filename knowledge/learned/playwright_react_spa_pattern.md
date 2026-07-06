---
name: Playwright required for React SPAs - platform.claude.com pattern
observed_in: 2026-07-06 documentation refresh (8 Anthropic platform.claude.com sources)
confidence: high
---

# Lesson: React SPAs Require Playwright, Not Simple HTTP

## What Happened

All 8 `platform.claude.com` documentation pages returned ~140 bytes of markdown when fetched via simple HTTP (requests + BeautifulSoup). Content was just "Loading..." repeated 12 times. Switching to Playwright yielded 5-42KB of actual documentation content.

## The Problem

**React SPAs render content client-side**:
- Server returns minimal HTML shell (~700KB-2MB of HTML)
- Actual documentation is injected by JavaScript at runtime
- Standard HTTP + html2text extracts only the loading placeholders

**Detection heuristics** that worked:
- HTML size > 500KB but markdown size < 500 bytes → JS-shell
- Markdown contains "Loading..." keyword in first 200 chars → JS-shell
- HTML/markdown size ratio > 1000:1 → JS-shell

## Platform Patterns Observed

| Platform | Pattern | Needs Playwright? |
|----------|---------|-------------------|
| `platform.claude.com` | React SPA | ✅ Yes (8/8 sources) |
| `code.claude.com` | Server-rendered | ❌ No (4/4 sources worked via HTTP) |
| `ai.google.dev` | Server-rendered | ❌ No (11/11 sources worked) |
| `adk.dev` | Mixed (1 SPA, 15 static) | ⚠️ Mostly no (1/16 needed it) |
| `openai.github.io` | Static GitHub Pages | ❌ No (12/12 via GitHub API) |
| `docs.x.ai` | Server-rendered | ❌ No (10/10 via HTTP) |

**Key insight**: `platform.claude.com` and `code.claude.com` are DIFFERENT. Don't assume subdomains follow the same pattern.

## Implementation

**Playwright setup** (Python):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="networkidle", timeout=30000)
    html = page.content()  # Fully rendered HTML
    browser.close()
```

**Dependencies** (inline script):
```python
# /// script
# dependencies = [
#   "playwright>=1.40",
# ]
# ///
```

Then run: `python -m playwright install chromium` (downloads ~171MB Chrome + 93MB headless shell)

## Suggested Rule

**For documentation fetching**:
1. Try HTTP first (Tier 2) — works for 85% of sources
2. Detect JS-shells using size + keyword heuristics
3. Automatically retry with Playwright if detected (Tier 3)
4. **Known SPA domains**: Add domain-specific config to skip HTTP and go straight to Playwright
   - Example: `platform.claude.com`, `support.google.com/gemini`

**Cost tradeoff**: Playwright adds ~3-5 seconds per fetch vs <1 second for HTTP. Only use when detected/known necessary.

## Why This Matters

**Without this lesson**: Future doc refreshes would retry `platform.claude.com` with HTTP, fail, log for manual retrieval, waste user time.

**With this lesson**: Add `platform.claude.com` to "known SPA domains" list → skip HTTP, go straight to Playwright → 100% automation.

## Reusability

Pattern applies to:
- ✅ Any React/Vue/Angular SPA documentation scraping
- ✅ Platforms that migrated from static to SPA (platform.claude.com did this in 2026)
- ✅ Mixed platforms where you don't control the rendering
- ❌ NOT for: APIs, static sites, server-rendered content
