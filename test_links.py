#!/usr/bin/env python3
"""Test all internal links on the MkDocs site.

Usage:
    python3 test_links.py [base_url]

Default base_url: http://127.0.0.1:8000
"""

import sys
import re
import urllib.request
import urllib.error
from collections import defaultdict
from html.parser import HTMLParser


class LinkExtractor(HTMLParser):
    """Extract href attributes from <a> tags."""
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append(value)


def get_page(url):
    """Fetch a page and return its HTML content."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LinkTester/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8", errors="replace"), resp.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception as e:
        return None, str(e)


def normalize_url(base, href):
    """Resolve a relative URL against a base URL."""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("//"):
        return "http:" + href
    if href.startswith("#"):
        return None  # Skip anchors
    if href.startswith("mailto:") or href.startswith("javascript:"):
        return None

    # Handle relative paths
    from urllib.parse import urljoin
    return urljoin(base, href)


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    base_url = base_url.rstrip("/")

    print(f"Testing links starting from: {base_url}/")
    print("=" * 60)

    visited = set()
    broken = []
    queue = [base_url + "/"]
    page_count = 0

    while queue:
        url = queue.pop(0)

        # Only crawl internal pages
        if not url.startswith(base_url):
            continue

        # Strip anchor
        url_no_anchor = url.split("#")[0]
        if url_no_anchor in visited:
            continue
        visited.add(url_no_anchor)

        html, status = get_page(url_no_anchor)
        page_count += 1

        if status != 200:
            broken.append((url_no_anchor, status, "CRAWL"))
            continue

        if page_count % 25 == 0:
            print(f"  ... checked {page_count} pages, {len(broken)} broken so far")

        if not html:
            continue

        # Extract links
        parser = LinkExtractor()
        try:
            parser.feed(html)
        except Exception:
            continue

        for href in parser.links:
            resolved = normalize_url(url_no_anchor, href)
            if resolved is None:
                continue

            # Only test internal links
            if not resolved.startswith(base_url):
                continue

            resolved_clean = resolved.split("#")[0]
            if resolved_clean in visited:
                continue

            # Test the link
            _, link_status = get_page(resolved_clean)
            if link_status != 200:
                broken.append((resolved_clean, link_status, url_no_anchor))
                visited.add(resolved_clean)
            else:
                # Add to crawl queue if it's an HTML page
                queue.append(resolved_clean)

    print()
    print("=" * 60)
    print(f"RESULTS: Checked {page_count} pages, {len(visited)} unique URLs")
    print(f"Broken links: {len(broken)}")
    print()

    if broken:
        # Group by status code
        by_status = defaultdict(list)
        for url, status, source in broken:
            by_status[status].append((url, source))

        for status, items in sorted(by_status.items(), key=lambda x: str(x[0])):
            print(f"--- Status {status} ({len(items)} links) ---")
            for url, source in items[:20]:  # Limit output per status
                # Show relative path for readability
                short = url.replace(base_url, "")
                if source != "CRAWL":
                    source_short = source.replace(base_url, "")
                    print(f"  {short}")
                    print(f"    linked from: {source_short}")
                else:
                    print(f"  {short}")
            if len(items) > 20:
                print(f"  ... and {len(items) - 20} more")
            print()
    else:
        print("All links are working!")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
