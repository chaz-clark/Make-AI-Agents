# 5-Tier Fetch Architecture Design

## Overview

Hierarchical fallback for fetching platform documentation with maximum automation.

## Tiers (in execution order)

### Tier 1: API Layer
**When**: Platform provides official API access to docs
**How**:
- GitHub API for `*.github.io` domains (e.g., `openai.github.io/openai-agents-python`)
- Google ADK: Check if hosted on GitHub (likely `github.com/google/adk-docs`)
- xAI: Check if hosted on GitHub
**Return**: Raw markdown or structured content
**Success**: Full content via API
**Failure → Tier 2**

### Tier 2: Raw HTTP (existing)
**When**: Standard server-rendered HTML
**How**: `requests` + BeautifulSoup + html2text
**Detect JS-shell**:
- Fetched content < 2KB
- Fetched content < 20% of expected size (from drift check)
- Body contains "Loading..." or "JavaScript required" patterns
**Success**: Full HTML→markdown conversion
**Failure → Tier 3**

### Tier 3: Playwright Headless Browser
**When**: Tier 2 returns JS-shell or suspect regression
**How**:
- Install `playwright` as optional dependency
- Launch headless Chromium
- Navigate to URL
- Wait for network idle OR content selector visible
- Extract via same selectors as Tier 2
**Success**: Rendered content extracted
**Failure → Tier 4**

### Tier 4: Manual Fallback Logging
**When**: All automated tiers fail
**How**:
- Write entry to `source_docs/_manual_needed.json`:
  ```json
  {
    "url": "https://...",
    "target_file": "source_docs/foo.md",
    "reason": "tier_3_playwright_failed",
    "direct_link": "https://...",
    "timestamp": "2026-06-29T18:30:00Z",
    "attempts": 3
  }
  ```
- Print user-friendly message:
  ```
  ⚠️  Manual retrieval needed for: foo.md
  📄 Open in browser: https://...
  💾 Save as HTML to: ~/Downloads/foo.html
  🔄 Then run: uv run update_agents/fetch_doc.py --scan-downloads
  ```
**Success**: User notified with clear next steps
**Completion → Tier 5**

### Tier 5: Downloads Folder Scanner
**When**: User runs `--scan-downloads` after manual save
**How**:
- Read `_manual_needed.json`
- Scan `~/Downloads/*.html` (modified in last 7 days)
- Match by:
  - Filename contains URL slug (e.g., `openai-agents-python` from URL)
  - HTML meta tags match source URL
- For each match:
  - Convert via `--from-html`
  - Write to `target_file` with metadata header
  - Remove from `_manual_needed.json`
- Report success/remaining

## Implementation Plan

### Phase 1: Tier 3 (Playwright)
- Add optional `playwright>=1.40` to PEP 723 deps (commented out by default)
- Add `--enable-playwright` flag
- Detect JS-shell in `check_drift()` and `fetch_one()`
- If detected → try Playwright before failing

### Phase 2: Tier 4 (Manual Log)
- Create `_manual_needed.json` schema
- Write on tier 3 failure
- Pretty-print instructions to stderr

### Phase 3: Tier 5 (Downloads Scanner)
- Add `--scan-downloads` command
- Match logic: fuzzy filename + HTML meta tag check
- Auto-convert + remove from manual list

### Phase 4: Tier 1 (API Layer)
- Detect GitHub-hosted docs by domain pattern
- Use `gh api repos/:owner/:repo/contents/:path` for direct markdown
- Fall back to Tier 2 if API fails

## Usage Examples

```bash
# Standard flow (tries all tiers automatically)
uv run update_agents/fetch_doc.py https://openai.github.io/openai-agents-python/

# Tier 1: API fetch (if GitHub-hosted)
→ Detected GitHub-hosted docs, fetching via API
✓ openai_agents_sdk.md (via GitHub API)

# Tier 2: HTTP fetch (if server-rendered)
→ fetching https://code.claude.com/docs/en/agent-sdk/overview
✓ anthropic_agent_sdk.md

# Tier 3: Playwright fallback (if JS-rendered)
→ fetching https://adk.dev/agents/multi-agents/
⚠️  Suspect JS-shell detected (67 bytes)
→ Retrying with Playwright headless browser...
✓ google_adk_multi_agents.md (via Playwright)

# Tier 4: Manual needed
→ fetching https://support.google.com/gemini/...
⚠️  All automated methods failed
📝 Logged to _manual_needed.json
📄 Open: https://support.google.com/gemini/...
💾 Save HTML to ~/Downloads/

# Tier 5: Scan downloads
uv run update_agents/fetch_doc.py --scan-downloads
→ Scanning ~/Downloads for manual saves...
✓ Found: gemini-gems-overview.html → google_gems_overview.md
✓ 1 file processed, 0 remaining in manual queue
```

## Configuration

Add to `doc_refresh_agent.json`:

```json
{
  "fetch_tiers": {
    "tier_1_api": {
      "enabled": true,
      "platforms": {
        "github": {
          "pattern": "*.github.io",
          "api_base": "https://api.github.com"
        }
      }
    },
    "tier_2_http": {
      "enabled": true,
      "js_shell_threshold_bytes": 2000,
      "regression_threshold_pct": 0.2
    },
    "tier_3_playwright": {
      "enabled": true,
      "timeout_ms": 30000,
      "wait_for": "networkidle"
    },
    "tier_4_manual_log": {
      "log_path": "source_docs/_manual_needed.json",
      "max_age_days": 30
    },
    "tier_5_downloads_scan": {
      "scan_path": "~/Downloads",
      "max_age_days": 7,
      "auto_remove_source": false
    }
  }
}
```

## Success Metrics

- **Tier 1**: 40% of fetches (GitHub-hosted docs)
- **Tier 2**: 50% of fetches (server-rendered)
- **Tier 3**: 8% of fetches (JS-rendered)
- **Tier 4+5**: 2% of fetches (manual required)

Target: <5% manual intervention rate after Playwright is enabled.
