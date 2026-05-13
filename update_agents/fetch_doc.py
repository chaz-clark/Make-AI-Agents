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

Limitations (Tier 1 — server-rendered HTML only):
  * JS-rendered SPAs (ai.google.dev support pages, parts of platform.openai.com)
    return shells without content. Use the Playwright tier (not yet built)
    or a browser manual save for those.
  * Sites with Cloudflare anti-bot challenges may return 403 or 503; the
    User-Agent below mimics Chrome but is not enough for strict WAFs.

If --batch returns small files (< 2KB) repeatedly, the site is likely
JS-rendered and Tier 1 isn't enough. Fall back to manual save for that
domain and note it in source_docs/_refresh_log.json.
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


def main():
    p = argparse.ArgumentParser(description="Tier-1 raw HTTP fetcher for docs → source_docs/dropbox/")
    p.add_argument("url", nargs="?", help="URL to fetch (or omit when using --batch)")
    p.add_argument("--out", help="Output path (default: source_docs/dropbox/<auto-name>.md)")
    p.add_argument("--list-links", action="store_true", help="Print discovered links from the URL instead of fetching")
    p.add_argument("--link-prefix", help="Filter --list-links output to URLs containing this substring (e.g. /a2a/)")
    p.add_argument("--batch", help="Read URLs from this file (one per line, '#' comments allowed)")
    p.add_argument("--sleep", type=float, default=1.0, help="Sleep between batch fetches (default 1s)")
    args = p.parse_args()

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
        p.error("URL required (or use --batch)")

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
