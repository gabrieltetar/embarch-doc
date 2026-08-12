#!/usr/bin/env python3
"""Check that every relative Markdown link in this repo resolves to a real file.

Walks all *.md files, extracts `[text](target)` links, and reports any
relative target (link or embedded anchor target) that doesn't resolve on
disk. http(s) links and bare in-page anchors (`#section`) are skipped.

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
            file_part = target.split('#', 1)[0]
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), file_part))
            if not os.path.exists(resolved):
                missing.append((os.path.relpath(path, REPO_ROOT), target))

    if missing:
        print(f"Found {len(missing)} broken relative link(s):\n")
        for src, target in missing:
            print(f"  {src} -> {target}")
        return 1

    print("All relative links resolve.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
