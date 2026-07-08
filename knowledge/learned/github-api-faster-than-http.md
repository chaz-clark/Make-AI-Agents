---
name: GitHub API faster than HTTP for *.github.io domains
observed_in: 2026-07-06 documentation refresh (12 OpenAI sources)
confidence: high
---

# Lesson: GitHub API Provides Direct Markdown for *.github.io

## What Happened

All 12 OpenAI documentation sources (`openai.github.io/openai-agents-python/*`) were fetched via GitHub API as raw markdown instead of HTTP + html2text conversion. Result: **instant markdown, no conversion needed, zero failures**.

## The Pattern

**GitHub Pages (`*.github.io`) are backed by GitHub repos**:
- URL pattern: `https://{owner}.github.io/{repo}/{path}`
- Maps to: `https://github.com/{owner}/{repo}` (usually `docs/` folder)
- GitHub API endpoint: `https://api.github.com/repos/{owner}/{repo}/contents/{path}`

**Fetch flow**:
1. Parse URL: `openai.github.io/openai-agents-python/agents/` → owner: `openai`, repo: `openai-agents-python`, path: `agents/`
2. Try GitHub API paths in order:
   - `docs/{path}/index.md`
   - `docs/{path}.md`
   - `{path}/index.md`
   - `{path}.md`
3. First match returns raw markdown (API header: `Accept: application/vnd.github.raw`)

**Speed**: <1 second per fetch (vs 2-3 seconds for HTTP + html2text)

## Results

| Source | HTTP + Conversion | GitHub API |
|--------|-------------------|------------|
| `openai_agents_sdk.md` | Would work, ~3s | ✅ 5.6KB markdown, <1s |
| `openai_handoffs.md` | Would work, ~3s | ✅ 10.6KB markdown, <1s |
| `openai_sandbox_guide.md` | Would work, ~3s | ✅ 48.2KB markdown, <1s |

**12/12 sources**: 100% success rate via GitHub API

**Why it's better**:
- No HTML → markdown conversion (lossy, requires tuning content selectors)
- No chrome removal (navigation, footers already excluded from source markdown)
- Byte-identical to source documentation (what docs team wrote, not what rendered)
- Faster (no browser rendering, no HTML parsing)

## Implementation

**URL detection**:
```python
def is_github_io_url(url):
    parsed = urlparse(url)
    return parsed.netloc.endswith(".github.io")
```

**Parse pattern**:
```python
def parse_github_io_url(url):
    # https://openai.github.io/openai-agents-python/agents/intro/
    # → owner: "openai", repo: "openai-agents-python", path: "agents/intro/"
    parsed = urlparse(url)
    owner = parsed.netloc.replace(".github.io", "")
    path_parts = parsed.path.strip("/").split("/")
    repo = path_parts[0]
    doc_path = "/".join(path_parts[1:]) if len(path_parts) > 1 else ""
    return (owner, repo, doc_path)
```

**Fetch** (with fallback paths):
```python
attempts = [
    f"docs/{doc_path}/index.md",
    f"docs/{doc_path}.md",
    f"{doc_path}/index.md",
    f"{doc_path}.md",
]

for file_path in attempts:
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    r = requests.get(api_url, headers={"Accept": "application/vnd.github.raw"})
    if r.status_code == 200:
        return r.text  # Raw markdown
```

## When GitHub API Fails

**Failure modes observed**:
- 404: Path doesn't match any of the 4 common patterns → fall back to HTTP
- 403: Rate limit (60/hour unauthenticated, 5000/hour with token)
- Repo is private (rare for docs)

**Fallback**: If GitHub API returns 404 for all 4 path attempts, fall back to Tier 2 (HTTP + html2text). Still works, just slower.

## Suggested Rule

**For any `*.github.io` documentation source**:
1. Always try GitHub API first (Tier 1)
2. Parse URL to extract owner/repo/path
3. Try 4 common path patterns (docs/* variants, root/* variants, index.md vs direct)
4. Fall back to HTTP only if all 4 return 404

**Known patterns** (from this refresh):
- OpenAI: `docs/{path}.md` (12/12 sources)
- Others: Likely similar, test on first fetch

**Cost**: GitHub API is free (60/hour limit), faster, and higher quality than HTTP scraping.

## Reusability

Pattern applies to:
- ✅ Any GitHub Pages documentation (`*.github.io`)
- ✅ Multi-repo organizations (owner is extracted from subdomain)
- ✅ Documentation hosted in non-root paths
- ❌ NOT for: Non-GitHub-Pages sites (even if they look like markdown)

## Impact

**Before**: HTTP + html2text on all sources → 2-3 seconds each, content selector tuning required
**After**: GitHub API on `*.github.io` → <1 second each, byte-identical markdown
**Time saved**: 12 sources × 2 seconds = 24 seconds (not huge, but adds up over 65 sources)
**Quality improvement**: No conversion artifacts, no missed content due to bad selectors
