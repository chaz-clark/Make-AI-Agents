#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "requests>=2.31",
#   "html2text>=2024.2.26",
#   "beautifulsoup4>=4.12",
#   "lxml>=5.0",
# ]
# ///
"""
fetch_doc.py — Raw HTTP doc fetcher for source_docs/dropbox/ staging.

Bypasses the WebFetch summarization that produces small-model summaries
on platform docs. Uses requests + bs4 + html2text directly so the cached
file contains the verbatim page body, not a paraphrase.

Workflow:
  1. Run --list-links on a hub URL to discover the child pages
  2. Save the printed list to a urls.txt (curate if needed)
  3. Run --batch urls.txt to fetch each into source_docs/dropbox/
  4. Use merge_dropbox.py (or the doc_refresh_agent merge step) to roll
     each dropbox/<name>.md into the corresponding source_docs/<name>.md
     with metadata header preserved

Usage:
  # Fetch one URL into dropbox/
  uv run update_agents/fetch_doc.py https://adk.dev/a2a/intro/

  # Fetch with explicit output name
  uv run update_agents/fetch_doc.py <url> --out source_docs/dropbox/foo.md

  # Discover child links from a hub page (prints URLs, doesn't fetch)
  uv run update_agents/fetch_doc.py https://adk.dev/a2a/ --list-links --link-prefix /a2a/

  # Batch fetch from a list (one URL per line, # comments allowed)
  uv run update_agents/fetch_doc.py --batch urls.txt --sleep 1.0

  # Convert an already-saved HTML file to markdown (no fetch)
  uv run update_agents/fetch_doc.py --from-html path/to/saved.html [--out foo.md]

  # Drift check: fetch URL, compare against an existing source_docs file, report only
  uv run update_agents/fetch_doc.py <url> --check source_docs/<name>.md

Coverage (validated 2026-05-13 against 11 sources from 5 platforms):
  * adk.dev, code.claude.com, platform.claude.com, openai.github.io,
    docs.x.ai, ai.google.dev/gemini-api/docs/*, developers.openai.com —
    all return full server-rendered bodies via raw HTTP. Tier 1 is a
    byte-identical drop-in replacement for "WebFetch + manual save".

Known exceptions (use --from-html with a browser save instead):
  * support.google.com/* — JS-rendered SPA (the Google Gems pages)
  * platform.openai.com/* — 403-gated by Cloudflare; deprecated anyway
  * Sites with strict Cloudflare/WAF anti-bot — User-Agent mimics Chrome
    but won't pass JS challenges

If --batch returns small files (< 2KB) repeatedly, fall back to
--from-html with a browser-saved HTML file and note the domain in
source_docs/_refresh_log.json. A Tier-2 (Playwright) path is not built
because empirical evidence (Phase A validation 2026-05-13) shows Tier 1
covers all current docs sources; --from-html handles the rare exception.
"""
import argparse
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


def fetch_one(url, out_path=None, quiet=False):
    if not quiet:
        print(f"→ {url}")
    r = fetch_url(url)
    if not quiet:
        print(f"  HTTP {r.status_code}  {len(r.text)} bytes HTML")
    md = html_to_md(r.text)
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
    p = argparse.ArgumentParser(description="Tier-1 raw HTTP fetcher for docs → source_docs/dropbox/")
    p.add_argument("url", nargs="?", help="URL to fetch (or omit when using --batch / --from-html)")
    p.add_argument("--out", help="Output path (default: source_docs/dropbox/<auto-name>.md)")
    p.add_argument("--list-links", action="store_true", help="Print discovered links from the URL instead of fetching")
    p.add_argument("--link-prefix", help="Filter --list-links output to URLs containing this substring (e.g. /a2a/)")
    p.add_argument("--batch", help="Read URLs from this file (one per line, '#' comments allowed)")
    p.add_argument("--sleep", type=float, default=1.0, help="Sleep between batch fetches (default 1s)")
    p.add_argument("--from-html", dest="from_html", help="Convert a local HTML file to markdown (no fetch). Use for browser-saved HTML.")
    p.add_argument("--check", dest="check_target", help="Drift check: fetch URL, compare body against this target file, report only (no write).")
    args = p.parse_args()

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
            fetch_one(u)
            time.sleep(args.sleep)
        return

    if not args.url:
        p.error("URL required (or use --batch / --from-html)")

    if args.list_links:
        r = fetch_url(args.url)
        links = list_links(r.text, args.url, args.link_prefix)
        prefix_note = f" (filtered to contain '{args.link_prefix}')" if args.link_prefix else ""
        print(f"# {len(links)} links from {args.url}{prefix_note}")
        for L in links:
            print(L)
        return

    out_path = Path(args.out) if args.out else None
    fetch_one(args.url, out_path)


if __name__ == "__main__":
    main()
