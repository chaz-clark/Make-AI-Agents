# Doc Refresh Agent Guide

## Agent Instructions
1. Read this for mission, principles, quickstart, and pitfalls.
2. Parse `doc_refresh_agent.json` for the source list, fetch configuration, and validation rules.
3. This agent fetches live documentation from AI platform URLs and writes the results to `source_docs/`. It does not analyze content or propose changes — that is the job of `doc_analysis_agent`.

---

## Mission (core)

Keeps the `source_docs/` cache current by fetching live documentation from AI platform developer pages and writing the results to local `.md` files.

**What it does**: Reads the source list from `doc_refresh_agent.json`, checks which cache files are stale or failed, fetches their URLs, and overwrites the corresponding `source_docs/*.md` files with fresh content and updated metadata headers.

**Why it exists**: The analysis agent needs readable, local source files to work offline and reproducibly. Without a dedicated refresh step, stale cache files silently produce outdated proposals.

**Who uses it**: Repo maintainers, run manually before an analysis cycle when sources are known to be outdated (or on a scheduled cadence).

**Example**: "Detects that `source_docs/anthropic_tool_use.md` is 45 days old (over the 30-day threshold), fetches the URL in its header, and overwrites the file with fresh content and `last_fetched: 2026-04-25`."

---

## Agent Quickstart (core)

1. **[Check Staleness]**: Read each `cache_file` in `source_docs/`, parse the header for `last_fetched` and `fetch_status`
   - Flag sources older than `staleness_threshold_days` or with `fetch_status: failed`

2. **[Fetch]**: For each stale or failed source, fetch the `source_url` from the file header
   - Use `Cache-Control: no-cache` to bypass HTTP caching
   - Retry up to `max_retries` times on failure

3. **[Write]**: Overwrite the `cache_file` with a new metadata header + extracted content
   - Update `last_fetched` to today's date
   - Set `fetch_status: success` or `failed` based on result

4. **[Validate]**: Confirm each refreshed file has substantive content and a valid header
   - Check file is not empty and content length exceeds minimum threshold

5. **[Report]**: Output a refresh summary — sources updated, sources still failing, sources skipped

For source list, staleness threshold, and fetch config, see `doc_refresh_agent.json`.

---

## File Organization: JSON vs MD (core)

### This Markdown File (.md) Contains:
- ✅ Mission and philosophy (why refresh is a separate step)
- ✅ What constitutes a successful vs failed fetch
- ✅ How to handle sources that persistently fail
- ✅ Pitfalls when fetching platform documentation

### The JSON File (.json) Contains:
- ✅ Source list: platform, label, URL, cache_file path, section_focus
- ✅ Fetch configuration: staleness threshold, retry count, timeout, headers
- ✅ Content extraction rules (what to strip, what to keep)
- ✅ Validation rules for confirming successful fetches
- ✅ Changelog of past refresh runs

**Rule of Thumb**: If the agent needs to fetch or configure → JSON. Why those choices exist → MD.

---

## Key Principles (core)

### 1. Write Only What You Fetch
**Description**: The refresh agent writes exactly what it fetches — no interpretation, no summarization, no filtering beyond boilerplate removal.

**Why**: The analysis agent is the one that interprets. If the refresh agent edits content, it introduces bias and breaks the audit trail back to the source.

**How**: Strip only obvious navigation chrome (headers/footers/nav menus). Preserve all substantive paragraphs, code blocks, lists, and headers exactly as found.

### 2. Always Preserve the Metadata Header
**Description**: Every `source_docs/` file must begin with the standard metadata block: `platform`, `label`, `source_url`, `last_fetched`, `fetch_status`, `notes`.

**Why**: The analysis agent reads these headers to decide which sources are usable. A missing or malformed header means the source is silently skipped.

**How**: Reconstruct the full header from the source entry in `doc_refresh_agent.json` on every write. Never partially update a header.

### 3. Fail Loudly, Skip Gracefully
**Description**: A failed fetch should be clearly logged and marked in the file — but should not block refreshing other sources.

**Why**: One 403 or 404 is common and shouldn't abort a full refresh run. But silent failure (e.g., writing an empty file with `fetch_status: success`) is worse than a clear failure marker.

**How**: On fetch failure, write the original file back with `fetch_status: failed`, updated `last_fetched`, and a `fetch_error` note. Log clearly to run summary.

### 4. Never Modify Template Files
**Description**: This agent only writes to `source_docs/`. It never touches `make_agent.md`, `make_agent.json`, `make_gem_qc.md`, or `make_gem_qc.json`.

**Why**: Separation of concerns. Refresh = fetch + cache. Analysis = diff + propose. Mixing them makes both agents harder to trust.

**How**: Hard constraint — the only write targets are paths matching `source_docs/*.md`.

---

## How to Use This Agent (core)

### Prerequisites
- `doc_refresh_agent.json` present with source list
- `source_docs/` folder exists (will be written to)
- WebFetch or HTTP access to fetch source URLs
- No special API keys required (all sources are public documentation)

### Basic Usage

**Step 1: Check which sources need refreshing**
```python
from pathlib import Path
import json
from datetime import datetime, timedelta

cfg = json.load(open("doc_refresh_agent.json"))
threshold = cfg["fetch_config"]["staleness_threshold_days"]
cutoff = datetime.today() - timedelta(days=threshold)

for source in cfg["sources"]:
    cache = Path(source["cache_file"])
    header = parse_header(cache.read_text())
    if header["fetch_status"] in ("failed", "not_attempted") or \
       datetime.fromisoformat(header["last_fetched"]) < cutoff:
        print(f"[STALE] {source['label']}")
    else:
        print(f"[OK]    {source['label']} ({header['last_fetched']})")
```

**Step 2: Fetch and write**
```python
for source in stale_sources:
    try:
        content = web_fetch(source["url"], headers={"Cache-Control": "no-cache"})
        write_cache_file(source, content, fetch_status="success")
        print(f"[REFRESHED] {source['cache_file']}")
    except Exception as e:
        write_cache_file(source, content=None, fetch_status="failed", error=str(e))
        print(f"[FAILED]    {source['label']}: {e}")
```

**Step 3: Verify outputs**
```python
for source in stale_sources:
    content = Path(source["cache_file"]).read_text()
    assert len(content) > cfg["fetch_config"]["min_content_length"], \
        f"Suspiciously short content: {source['cache_file']}"
    assert "fetch_status: success" in content, \
        f"Header missing or wrong status: {source['cache_file']}"
```

---

## Common Pitfalls and Solutions (core)

### 1. JavaScript-Rendered Pages Return Empty HTML

**Problem**: Some documentation sites render content via JavaScript. The fetched HTML contains only a shell — no actual documentation text.

**Why it happens**: The fetch tool retrieves the raw HTTP response, not the browser-rendered DOM. Pages that load content dynamically via JS will appear empty.

**Solution**: Check the `notes` field in `doc_refresh_agent.json` for each source. Sources flagged as "JS-rendered" require a browser-based fetch or a manual copy-paste workflow. Mark these as `fetch_method: manual` in the source entry.

**Example**:
```
// ❌ Result of fetching a JS-rendered page
File size: 2KB — only a <div id="root"></div> shell

// ✅ What to do
# Open the URL in a browser, copy all text, paste into the cache file
# Set fetch_status: manual in the header
```

### 2. Overwriting a Good Cache with a Failed Response

**Problem**: Agent fetches a URL that now 404s or 403s, and overwrites the previously-good cache file with an empty or error response.

**Why it happens**: The write step doesn't check content quality before overwriting.

**Solution**: Before overwriting, compare new content length to existing content length. If new content is less than 20% of the existing file size, treat as a suspect fetch and write to a `.new` staging file for review rather than overwriting directly.

### 3. Forgetting to Preserve the Notes Field

**Problem**: On refresh, the metadata header is reconstructed from the source entry in JSON — but the `notes` field in the existing file contains useful context added manually (e.g., "this page 404s at redirect, use related pages instead"). That context gets lost.

**Why it happens**: The header template is rebuilt from JSON, which doesn't include manually added notes.

**Solution**: Before overwriting, read the existing file's `notes` field and merge it into the new header. Append new fetch notes rather than replacing.

### 4. Treating Partial Fetches as Failures

**Problem**: A fetch returns some content but not all sections (e.g., a page with tabs where only the first tab is returned). Marking as `failed` means it gets re-fetched endlessly but never improves.

**Why it happens**: Binary success/failure doesn't capture partial content.

**Solution**: Use `fetch_status: partial` for content that was fetched but is known to be incomplete. Include a note explaining what's missing. The analysis agent treats `partial` sources as available (with lower confidence).

### 5. Hardcoding URLs Outside the JSON

**Problem**: Source URLs are referenced directly in code or scripts rather than being read from `doc_refresh_agent.json`. When a URL changes, only part of the system gets updated.

**Why it happens**: It's faster to hardcode a URL than to look it up from config.

**Solution**: Always read source URLs from `doc_refresh_agent.json` → `sources[].url`. The JSON is the single source of truth for all fetch targets.

---

## Examples (core)

### Example 1: Routine Monthly Refresh

**Scenario**: 30 days have passed since the last refresh. Running the agent to update all stale sources before a new analysis cycle.

**Input**: All 7 sources in `doc_refresh_agent.json`, `staleness_threshold_days: 30`

**Approach**: Agent checks each `cache_file` header. Finds 5 sources older than 30 days. Fetches each in sequence. Writes updated files.

**Output**:
```
[OK]      anthropic_agents.md — skipped (fetch_status: failed, manual refresh needed)
[REFRESHED] anthropic_tool_use.md — 9.2KB → 11.4KB
[REFRESHED] anthropic_agent_sdk.md — 7.5KB → 8.1KB
[REFRESHED] google_gemini_agentic.md — 4.9KB → 5.3KB
[REFRESHED] google_structured_output.md — 3.8KB → 4.0KB
[REFRESHED] openai_agents_sdk.md — 6.1KB → 7.2KB
[REFRESHED] xai_overview.md — 3.7KB → 3.7KB (no change detected)

Refresh complete: 5 updated, 1 skipped (manual), 0 failed
```

**Code**: See `doc_refresh_agent.json` → `validation.test_cases`

### Example 2: Single Source Refresh After a Platform Update

**Scenario**: Anthropic announces a significant update to their tool use documentation. Refresh only that one source.

**Approach**: Pass the specific `cache_file` as a target. Fetch only `anthropic_tool_use.md`. Compare before/after content length and spot-check key sections.

**Code**: See `doc_refresh_agent.json` → `fetch_config` for selective refresh parameters

### Example 3: Manual Refresh for a Blocked Source

**Scenario**: `openai_agents_sdk.md` starts returning errors because the GitHub Pages URL moved.

**Approach**: Update the `url` field in `doc_refresh_agent.json` to the new location. Re-run the agent for that source only. If still blocked, note the new URL and set `fetch_method: manual`.

**Code**: See `doc_refresh_agent.json` → `sources` for the entry to update

---

## Validation and Testing (core)

### Quick Validation
1. Check that all refreshed files are larger than `min_content_length` bytes
2. Verify each file starts with the `---` metadata header block
3. Confirm `last_fetched` in each header matches today's date
4. Spot-check one file for recognizable documentation content (not a 403 error page)

### Comprehensive Validation
For detailed validation rules, see `doc_refresh_agent.json` → `validation` section.

---

## Resources and References

### Agent Files
- **`doc_refresh_agent.json`**: Source list, fetch config, validation rules
- **`source_docs/`**: Output folder — all cache files written here
- **`doc_analysis_agent.md`**: Downstream agent that reads these files

### Related Agents
- `doc_analysis_agent` — reads the files this agent produces; run after a successful refresh
- `make_agent_qc` — can validate the refresh agent itself against template standards

### How to Use This Documentation System
1. **Start here** (.md) for understanding when and why to refresh
2. **Use JSON** for source URLs, fetch parameters, and validation rules
3. **Check `source_docs/` headers** to see current status of each source

---

## Quick Reference Card

| Aspect | Value |
|--------|-------|
| **Purpose** | Fetch live AI platform docs and update `source_docs/` cache files |
| **Input** | Source list from `doc_refresh_agent.json` |
| **Output** | Updated `source_docs/*.md` files with fresh content and metadata |
| **Agent Type** | workflow |
| **Complexity** | simple |
| **Key Files** | `doc_refresh_agent.json`, `source_docs/` |
| **Quickstart** | Check staleness → fetch stale sources → write cache files → verify |
| **Common Pitfall** | Overwriting good cache with a bad fetch response |
| **Dependencies** | WebFetch (HTTP GET), `source_docs/` folder |
