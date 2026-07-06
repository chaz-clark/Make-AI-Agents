#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "requests>=2.31",
#   "html2text>=2024.2.26",
#   "beautifulsoup4>=4.12",
#   "lxml>=5.0",
#   "playwright>=1.40",
# ]
# ///
"""
fetch_doc.py — 5-tier hierarchical doc fetcher with maximum automation.

Architecture:
  Tier 1: GitHub API     → Direct markdown fetch for *.github.io domains
  Tier 2: Raw HTTP       → requests + BeautifulSoup + html2text
  Tier 3: Playwright     → Headless browser for JS-rendered SPAs
  Tier 4: Manual Log     → Logs failures to _manual_needed.json
  Tier 5: Downloads Scan → Auto-processes manually saved HTML files

Workflow:
  1. Run --list-links on a hub URL to discover the child pages
  2. Save the printed list to a urls.txt (curate if needed)
  3. Run --batch urls.txt to fetch each into source_docs/dropbox/
  4. For JS-rendered sites, add --enable-playwright
  5. If manual save needed, follow printed instructions
  6. Run --scan-downloads to process manually saved HTML files
  7. Use merge_dropbox.py to merge into source_docs/<name>.md

Usage:
  # Fetch one URL (tries Tier 1 → 2 → 3 → 4 automatically)
  uv run update_agents/fetch_doc.py https://openai.github.io/openai-agents-python/

  # Enable Playwright for JS-rendered sites
  uv run update_agents/fetch_doc.py <url> --enable-playwright

  # Batch fetch with Playwright enabled
  uv run update_agents/fetch_doc.py --batch urls.txt --enable-playwright

  # Scan Downloads folder for manually saved HTML files (Tier 5)
  uv run update_agents/fetch_doc.py --scan-downloads

  # Convert a local HTML file to markdown (no fetch)
  uv run update_agents/fetch_doc.py --from-html path/to/saved.html

  # Drift check: compare fetched content against existing file
  uv run update_agents/fetch_doc.py <url> --check source_docs/<name>.md

  # Discover child links from a hub page
  uv run update_agents/fetch_doc.py https://adk.dev/a2a/ --list-links --link-prefix /a2a/

Tier Coverage:
  Tier 1 (GitHub API): openai.github.io/*, *.github.io/*
  Tier 2 (HTTP):       adk.dev, code.claude.com, docs.x.ai, ai.google.dev, developers.openai.com
  Tier 3 (Playwright): support.google.com/*, JS-rendered SPAs
  Tier 4+5 (Manual):   Sites with strict WAF/Cloudflare challenges

Manual Save Flow:
  1. Fetch attempt fails → logged to source_docs/_manual_needed.json
  2. Instructions printed: open URL, save as HTML to ~/Downloads/
  3. Run --scan-downloads → auto-matches and processes saved files
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import html2text

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
DEFAULT_DROPBOX = Path("/Users/chazclar/Documents/GitHub/Make-AI-Agents/source_docs/dropbox")

CONTENT_SELECTORS = [
    "main article",
    "article.content",
    "main",
    "article",
    '[role="main"]',
    ".markdown-body",
    ".md-content",
    ".md-content__inner",
    ".body",
    ".main-content",
]

CHROME_SELECTORS = (
    "nav, header, footer, .sidebar, .toc, .navigation, "
    "script, style, .related, .pagination, .edit-page, button, "
    ".md-nav, .md-header, .md-footer, .md-sidebar, "
    ".admonition.example, .admonition.note > .admonition-title"
)


# ─── Tier 1: GitHub API ─────────────────────────────────────────────────────

def is_github_io_url(url):
    """Return True if URL is hosted on *.github.io"""
    parsed = urlparse(url)
    return parsed.netloc.endswith(".github.io")


def parse_github_io_url(url):
    """
    Parse a *.github.io URL into (owner, repo, path).
    Example: https://openai.github.io/openai-agents-python/agents/intro/
    Returns: ("openai", "openai-agents-python", "agents/intro/")
    """
    parsed = urlparse(url)
    if not parsed.netloc.endswith(".github.io"):
        return None

    # Extract owner from subdomain (e.g., "openai" from "openai.github.io")
    owner = parsed.netloc.replace(".github.io", "")

    # Path format: /<repo>/<path> or /<repo>/ or /<repo>
    path_parts = parsed.path.strip("/").split("/")
    if not path_parts or not path_parts[0]:
        return None

    repo = path_parts[0]
    doc_path = "/".join(path_parts[1:]) if len(path_parts) > 1 else ""

    return (owner, repo, doc_path)


def try_github_api_fetch(url, quiet=False):
    """
    Tier 1: Try to fetch content via GitHub API if the URL is *.github.io.
    Returns (success: bool, content: str or None, reason: str)
    """
    if not is_github_io_url(url):
        return (False, None, "not_github_io")

    parsed = parse_github_io_url(url)
    if not parsed:
        return (False, None, "parse_failed")

    owner, repo, doc_path = parsed

    if not quiet:
        print(f"  → Detected GitHub Pages: {owner}/{repo}")

    # Try to map URL path to repo file structure
    # Common patterns:
    # 1. GitHub Pages from /docs/ folder: doc_path maps to docs/<path>
    # 2. GitHub Pages from root: doc_path maps to <path>
    # 3. Many projects use index.md or README.md for directories

    attempts = []
    if doc_path:
        # Try docs/<path>/index.md, docs/<path>.md, <path>/index.md, <path>.md
        attempts = [
            f"docs/{doc_path}/index.md",
            f"docs/{doc_path}.md",
            f"docs/{doc_path}/README.md",
            f"{doc_path}/index.md",
            f"{doc_path}.md",
            f"{doc_path}/README.md",
        ]
    else:
        # Root page: try docs/index.md, docs/README.md, README.md, index.md
        attempts = [
            "docs/index.md",
            "docs/README.md",
            "README.md",
            "index.md",
        ]

    # Try each path via GitHub API
    for file_path in attempts:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
        try:
            headers = {
                "Accept": "application/vnd.github.raw",  # Get raw content directly
                "User-Agent": USER_AGENT,
            }
            r = requests.get(api_url, headers=headers, timeout=10)
            if r.status_code == 200:
                content = r.text
                if not quiet:
                    print(f"  ✓ Found via GitHub API: {file_path} ({len(content)} bytes)")
                return (True, content, f"api:{file_path}")
            elif r.status_code == 404:
                continue  # Try next path
            else:
                if not quiet:
                    print(f"  GitHub API error {r.status_code} for {file_path}")
                continue
        except requests.RequestException as e:
            if not quiet:
                print(f"  GitHub API request failed for {file_path}: {e}")
            continue

    # All attempts failed
    return (False, None, "api_no_match")


# ─── Tier 2: HTTP Fetch ─────────────────────────────────────────────────────

def fetch_url(url, timeout=30, retries=3):
    """HTTP GET with retries on 429/503."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
    }
    last_exc = None
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            if r.status_code in (429, 503):
                sleep = (attempt + 1) * 2
                print(f"  {r.status_code} on attempt {attempt+1}/{retries}, sleeping {sleep}s", file=sys.stderr)
                time.sleep(sleep)
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last_exc = e
            if attempt == retries - 1:
                raise
            time.sleep(2)
    if last_exc:
        raise last_exc
    return None


def html_to_md(html):
    """Strip chrome and convert to clean markdown."""
    soup = BeautifulSoup(html, "lxml")
    for el in soup.select(CHROME_SELECTORS):
        el.decompose()
    body = None
    for sel in CONTENT_SELECTORS:
        body = soup.select_one(sel)
        if body:
            break
    if body is None:
        body = soup.body or soup
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_links = False
    h.ignore_images = True
    h.skip_internal_links = True
    h.protect_links = True
    h.unicode_snob = True
    h.escape_snob = True
    h.bypass_tables = False
    md = h.handle(str(body))
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


# ─── Tier 3: Playwright ─────────────────────────────────────────────────────

def try_playwright_fetch(url, quiet=False):
    """
    Tier 3: Use Playwright headless browser to fetch JS-rendered content.
    Returns markdown string on success, None on failure.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        if not quiet:
            print("  ⚠️  Playwright not installed. Install with: uv pip install playwright && playwright install chromium")
        return None

    if not quiet:
        print("  → Launching Playwright headless browser...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Extract HTML after JS has rendered
            html = page.content()
            browser.close()

            if not quiet:
                print(f"  → Rendered HTML: {len(html)} bytes")

            # Convert to markdown using same logic as Tier 2
            md = html_to_md(html)
            return md

    except Exception as e:
        if not quiet:
            print(f"  ⚠️  Playwright error: {e}")
        return None


# ─── Tier 4: Manual Fallback Logging ────────────────────────────────────────

MANUAL_LOG_PATH = Path("source_docs/_manual_needed.json")


def log_manual_needed(url, target_file, reason):
    """
    Tier 4: Log a URL that needs manual retrieval to _manual_needed.json.
    """
    from datetime import datetime, UTC

    # Load existing log
    if MANUAL_LOG_PATH.exists():
        try:
            log_data = json.loads(MANUAL_LOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log_data = []
    else:
        log_data = []

    timestamp = datetime.now(UTC).isoformat()

    # Check if this URL is already logged
    for entry in log_data:
        if entry.get("url") == url:
            # Update existing entry
            entry["attempts"] = entry.get("attempts", 0) + 1
            entry["timestamp"] = timestamp
            entry["reason"] = reason
            break
    else:
        # Add new entry
        entry = {
            "url": url,
            "target_file": str(target_file) if target_file else None,
            "reason": reason,
            "timestamp": timestamp,
            "attempts": 1,
        }
        log_data.append(entry)

    # Write back
    MANUAL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANUAL_LOG_PATH.write_text(json.dumps(log_data, indent=2), encoding="utf-8")

    # Print user-friendly instructions
    print("\n" + "=" * 70)
    print("⚠️  MANUAL RETRIEVAL NEEDED")
    print("=" * 70)
    print(f"URL:  {url}")
    print(f"Reason: {reason}")
    print("\nNext steps:")
    print(f"  1. Open in browser: {url}")
    print(f"  2. Save as HTML to: ~/Downloads/")
    print(f"  3. Run: uv run update_agents/fetch_doc.py --scan-downloads")
    print("=" * 70 + "\n")


# ─── Tier 5: Downloads Folder Scanner ───────────────────────────────────────

def scan_downloads():
    """
    Tier 5: Scan ~/Downloads for manually saved HTML files and match them
    against entries in _manual_needed.json.
    """
    import datetime
    from pathlib import Path

    downloads_dir = Path.home() / "Downloads"
    if not downloads_dir.exists():
        print(f"Downloads directory not found: {downloads_dir}")
        return

    if not MANUAL_LOG_PATH.exists():
        print(f"No manual log found at {MANUAL_LOG_PATH}")
        print("Nothing to process.")
        return

    # Load manual log
    try:
        log_data = json.loads(MANUAL_LOG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Error reading {MANUAL_LOG_PATH}")
        return

    if not log_data:
        print("Manual log is empty. Nothing to process.")
        return

    print(f"→ Scanning {downloads_dir} for manual saves...")
    print(f"  {len(log_data)} entries in manual log")

    # Find recent HTML files (modified in last 7 days)
    cutoff = time.time() - (7 * 24 * 60 * 60)
    html_files = []
    for html_file in downloads_dir.glob("*.html"):
        if html_file.stat().st_mtime >= cutoff:
            html_files.append(html_file)

    print(f"  {len(html_files)} HTML files modified in last 7 days")

    processed = []
    remaining = []

    for entry in log_data:
        url = entry.get("url")
        target_file = entry.get("target_file")
        if not url:
            remaining.append(entry)
            continue

        # Try to find a matching HTML file
        matched_file = None
        parsed = urlparse(url)
        url_slug = parsed.path.strip("/").replace("/", "_") or "index"

        for html_file in html_files:
            # Match by filename containing URL slug
            if url_slug in html_file.stem.lower():
                matched_file = html_file
                break

            # Also try matching by checking HTML meta tags
            try:
                html_content = html_file.read_text(encoding="utf-8", errors="replace")
                # Check for canonical URL or original URL in meta tags
                if url in html_content[:5000]:  # Check first 5KB for meta tags
                    matched_file = html_file
                    break
            except Exception:
                continue

        if matched_file:
            print(f"\n✓ Found match: {matched_file.name}")
            print(f"  URL: {url}")

            # Convert HTML to markdown
            try:
                md = html_to_md(matched_file.read_text(encoding="utf-8", errors="replace"))
                print(f"  → markdown {len(md)} bytes")

                # Determine output path
                if target_file:
                    out_path = Path(target_file)
                else:
                    out_path = DEFAULT_DROPBOX / auto_name(url)

                write_md(md, out_path)
                print(f"  ✓ Written to {out_path}")
                processed.append(entry)

            except Exception as e:
                print(f"  ⚠️  Error converting: {e}")
                remaining.append(entry)
        else:
            remaining.append(entry)

    # Update manual log with remaining entries
    MANUAL_LOG_PATH.write_text(json.dumps(remaining, indent=2), encoding="utf-8")

    # Summary
    print("\n" + "=" * 70)
    print("SCAN COMPLETE")
    print("=" * 70)
    print(f"  Processed:  {len(processed)} files")
    print(f"  Remaining:  {len(remaining)} entries in manual log")
    if remaining:
        print(f"\nStill need manual saves for:")
        for entry in remaining:
            print(f"  - {entry.get('url')}")
    print("=" * 70 + "\n")


def list_links(html, base_url, link_prefix=None):
    """Extract anchor hrefs from a page, resolved against base_url."""
    soup = BeautifulSoup(html, "lxml")
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = (a["href"] or "").strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        full = urljoin(base_url, href).split("#")[0]
        if link_prefix and link_prefix not in full:
            continue
        if full not in seen:
            seen.add(full)
            links.append(full)
    return links


def auto_name(url):
    """Derive a dropbox filename from a URL path."""
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_") or "index"
    host = parsed.netloc.replace(".", "_")
    return f"{host}__{path}.md"


def write_md(content, target_path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")


def fetch_one(url, out_path=None, quiet=False, enable_playwright=False):
    """
    Fetch a URL using the 5-tier fallback strategy.
    Returns the output path where the markdown was written.
    """
    if not quiet:
        print(f"→ {url}")

    # Tier 1: Try GitHub API first if it's a *.github.io domain
    success, content, reason = try_github_api_fetch(url, quiet=quiet)
    if success:
        md = content  # Already markdown from GitHub
        if not quiet:
            print(f"  → markdown {len(md)} bytes (from GitHub API)")
        if out_path is None:
            out_path = DEFAULT_DROPBOX / auto_name(url)
        write_md(md, out_path)
        if not quiet:
            print(f"  ✓ {out_path}")
        return out_path

    # Tier 2: Raw HTTP fetch
    if not quiet and reason != "not_github_io":
        print(f"  → GitHub API failed ({reason}), falling back to HTTP")
    r = fetch_url(url)
    if not quiet:
        print(f"  HTTP {r.status_code}  {len(r.text)} bytes HTML")

    md = html_to_md(r.text)
    md_size = len(md)
    html_size = len(r.text)

    # Detect potential JS-shell (Tier 2 failure → Tier 3)
    is_suspect = False
    if html_size < 2000:
        is_suspect = True
        suspect_reason = f"HTML < 2KB ({html_size} bytes)"
    elif md_size < 500:
        is_suspect = True
        suspect_reason = f"markdown < 500 bytes ({md_size} bytes)"
    elif "loading" in md.lower()[:200] or "javascript" in md.lower()[:200]:
        is_suspect = True
        suspect_reason = "JS-shell keywords detected"

    if is_suspect:
        if not quiet:
            print(f"  ⚠️  Suspect JS-shell detected: {suspect_reason}")

        # Tier 3: Try Playwright if enabled
        if enable_playwright:
            playwright_md = try_playwright_fetch(url, quiet=quiet)
            if playwright_md:
                md = playwright_md
                if not quiet:
                    print(f"  → markdown {len(md)} bytes (from Playwright)")
            else:
                if not quiet:
                    print(f"  ⚠️  Playwright fetch failed")
                # Fall through to Tier 4 (manual logging)
                log_manual_needed(url, out_path, "tier_3_playwright_failed")
        else:
            if not quiet:
                print(f"  → Playwright disabled. Use --enable-playwright or save manually.")
            # Fall through to Tier 4 (manual logging)
            log_manual_needed(url, out_path, "tier_2_js_shell")

    if not quiet:
        print(f"  → markdown {len(md)} bytes")
    if out_path is None:
        out_path = DEFAULT_DROPBOX / auto_name(url)
    write_md(md, out_path)
    if not quiet:
        print(f"  ✓ {out_path}")
    return out_path


def convert_html_file(html_path, out_path=None):
    """Convert a local HTML file to markdown. Same chrome-stripping +
    content-selector logic as fetch_one, no network."""
    html_path = Path(html_path)
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")
    html = html_path.read_text(encoding="utf-8", errors="replace")
    print(f"→ {html_path} ({len(html)} bytes HTML)")
    md = html_to_md(html)
    print(f"  → markdown {len(md)} bytes")
    if out_path is None:
        # Default: same directory as input, .md extension
        out_path = html_path.with_suffix(".md")
        if out_path == html_path:
            out_path = html_path.parent / (html_path.stem + ".converted.md")
    write_md(md, out_path)
    print(f"  ✓ {out_path}")
    return out_path


def strip_front_matter(text):
    """Return body without leading YAML front matter."""
    m = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", text, re.DOTALL)
    return m.group(1).strip() if m else text.strip()


def check_drift(url, target_path):
    """Fetch URL, compare against target file body, report drift only — no write."""
    target = Path(target_path)
    if not target.exists():
        print(f"DRIFT CHECK ERROR: target file not found: {target}")
        return 1
    print(f"→ fetching {url}")
    r = fetch_url(url)
    new_md = html_to_md(r.text)
    new_size = len(new_md.encode("utf-8"))
    existing_body = strip_front_matter(target.read_text(encoding="utf-8"))
    old_size = len(existing_body.encode("utf-8"))

    ratio = new_size / max(old_size, 1)
    delta_pct = (ratio - 1.0) * 100

    print(f"\nDrift report:")
    print(f"  target file:  {target}")
    print(f"  current body: {old_size:,} bytes")
    print(f"  fetched body: {new_size:,} bytes")
    print(f"  delta:        {new_size - old_size:+,} bytes ({delta_pct:+.1f}%)")
    # Cheap structural diff: line count, code-block count
    new_lines = new_md.count("\n")
    old_lines = existing_body.count("\n")
    new_codeblocks = new_md.count("\n    ") + new_md.count("\n```")
    old_codeblocks = existing_body.count("\n    ") + existing_body.count("\n```")
    print(f"  lines:        {old_lines:,} → {new_lines:,} ({new_lines - old_lines:+,})")
    print(f"  code blocks:  {old_codeblocks} → {new_codeblocks} ({new_codeblocks - old_codeblocks:+})")

    # Verdict heuristic
    if abs(delta_pct) < 5:
        print(f"  verdict:      NO_DRIFT (≤ 5% delta)")
        return 0
    if new_size < old_size * 0.8:
        print(f"  verdict:      SUSPECT_REGRESSION (new < 80% of current — possible JS-shell or partial fetch)")
        return 2
    if new_size > old_size * 1.1:
        print(f"  verdict:      MATERIAL_GROWTH (new > 110% — content was added upstream or current cache is partial)")
        return 1
    print(f"  verdict:      MINOR_DRIFT (5–10%; likely cosmetic)")
    return 1


def main():
    p = argparse.ArgumentParser(description="5-tier doc fetcher: API → HTTP → Playwright → Manual → Downloads scan")
    p.add_argument("url", nargs="?", help="URL to fetch (or omit when using --batch / --from-html / --scan-downloads)")
    p.add_argument("--out", help="Output path (default: source_docs/dropbox/<auto-name>.md)")
    p.add_argument("--list-links", action="store_true", help="Print discovered links from the URL instead of fetching")
    p.add_argument("--link-prefix", help="Filter --list-links output to URLs containing this substring (e.g. /a2a/)")
    p.add_argument("--batch", help="Read URLs from this file (one per line, '#' comments allowed)")
    p.add_argument("--sleep", type=float, default=1.0, help="Sleep between batch fetches (default 1s)")
    p.add_argument("--from-html", dest="from_html", help="Convert a local HTML file to markdown (no fetch). Use for browser-saved HTML.")
    p.add_argument("--check", dest="check_target", help="Drift check: fetch URL, compare body against this target file, report only (no write).")
    p.add_argument("--enable-playwright", action="store_true", help="Enable Tier 3: Playwright headless browser for JS-rendered pages")
    p.add_argument("--scan-downloads", action="store_true", help="Tier 5: Scan ~/Downloads for manually saved HTML files")
    args = p.parse_args()

    # --scan-downloads: Tier 5 scanner
    if args.scan_downloads:
        scan_downloads()
        return

    # --from-html: convert local file, no network
    if args.from_html:
        out_path = Path(args.out) if args.out else None
        convert_html_file(args.from_html, out_path)
        return

    # --check: fetch URL, compare against target, no write
    if args.check_target:
        if not args.url:
            p.error("--check requires a URL")
        rc = check_drift(args.url, args.check_target)
        sys.exit(rc)

    # --batch: many URLs into dropbox/
    if args.batch:
        urls = []
        for line in Path(args.batch).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
        print(f"Batch: {len(urls)} URLs from {args.batch}")
        for u in urls:
            fetch_one(u, enable_playwright=args.enable_playwright)
            time.sleep(args.sleep)
        return

    if not args.url:
        p.error("URL required (or use --batch / --from-html / --scan-downloads)")

    if args.list_links:
        r = fetch_url(args.url)
        links = list_links(r.text, args.url, args.link_prefix)
        prefix_note = f" (filtered to contain '{args.link_prefix}')" if args.link_prefix else ""
        print(f"# {len(links)} links from {args.url}{prefix_note}")
        for L in links:
            print(L)
        return

    out_path = Path(args.out) if args.out else None
    fetch_one(args.url, out_path, enable_playwright=args.enable_playwright)


if __name__ == "__main__":
    main()
