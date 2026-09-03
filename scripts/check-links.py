#!/usr/bin/env python3
"""Check that every relative Markdown link in this repo resolves to a real file.

Walks all *.md files, extracts `[text](target)` links, and reports any
relative target (link or embedded anchor target) that doesn't resolve on
disk, **and any `file.md#fragment` whose fragment names nothing in that
file**. http(s) links and bare in-page anchors (`#section`) are skipped.

The fragment half was added 2026-09-02: a link like `embarch.md#6-index`
kept "resolving" after that heading was renamed or removed, because only the
filename was ever validated. That is reversals row 50's shape -- a bounded
check that cannot report the thing it does not look at. A fragment resolves
against an explicit `<a id="...">` or a GitHub-style heading slug.

Usage: scripts/check-links.py   (run from anywhere; paths are repo-relative)
Exit status: 0 if every relative link resolves, 1 otherwise.

This exists because embarch-doc is a web of cross-linked docs
(DOC-PROTOCOL.md §5's "link, don't restate" rule) — a renamed or moved file
silently breaks every doc that pointed at it, and that class of drift has
bitten this repo before (embarch-roadmap.md's changelog, 2026-08-05: two
dangling cross-references to a "Next"/"Later" bucket that didn't exist yet).
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
EXPLICIT_ID_RE = re.compile(r'<a\s+id="([^"]+)"', re.I)
HEADING_RE = re.compile(r'^#{1,6}\s+(.*?)\s*$', re.M)


def slug(text):
    """GitHub's heading-slug rules, close enough for this repo's headings."""
    text = re.sub(r'`', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)   # link -> its text
    text = re.sub(r'[*_]', '', text)
    text = text.lower().strip()
    text = re.sub(r'[^\w\- ]', '', text)
    return re.sub(r'\s+', '-', text)


_anchor_cache = {}


def anchors_of(path):
    if path in _anchor_cache:
        return _anchor_cache[path]
    try:
        with open(path, encoding='utf-8') as f:
            body = f.read()
    except OSError:
        _anchor_cache[path] = set()
        return _anchor_cache[path]
    found = set(EXPLICIT_ID_RE.findall(body))
    found |= {slug(h) for h in HEADING_RE.findall(body)}
    _anchor_cache[path] = found
    return found


def find_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for name in filenames:
            if name.endswith('.md'):
                yield os.path.join(dirpath, name)


def main():
    missing = []
    for path in find_md_files(REPO_ROOT):
        with open(path, encoding='utf-8') as f:
            content = f.read()
        for match in LINK_RE.finditer(content):
            target = match.group(1).strip()
            if target.startswith(('http://', 'https://', 'mailto:')):
                continue
            if target.startswith('#'):
                continue  # in-page anchor, not checked here
            file_part, _, frag = target.partition('#')
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(resolved):
                missing.append((os.path.relpath(path, REPO_ROOT), target))
            elif frag and resolved.endswith('.md') and frag not in anchors_of(resolved):
                missing.append((os.path.relpath(path, REPO_ROOT),
                                f"{target}  (file exists; nothing named '{frag}' in it)"))

    if missing:
        print(f"Found {len(missing)} broken relative link(s):\n")
        for src, target in missing:
            print(f"  {src} -> {target}")
        return 1

    print("All relative links resolve.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
