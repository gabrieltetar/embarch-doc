#!/usr/bin/env python3
"""Print every "Open questions" section across the suite's design docs, in one place.

Added 2026-08-15, closing item 63 of that day's design-improvement review
(.claude/design-improvements-2026-08-15.md, local working notes): open
questions are spread across six-plus docs' own §7/§10/§12-equivalent
sections, with no suite-wide index — this fits the existing scripts/
tooling pattern (check-links.py, check-staleness.py) exactly, per that
review's own suggestion.

Walks every sub-project's open.md -- the four-file layout's home for open
questions -- plus any legacy design.md still carrying its own section, plus
embarch-token.md. Until 2026-09-03 it read design.md ONLY, which after the
migration meant it saw 10 questions across 3 docs while 88 sat unread in eight
open.md files. Every refill sweep since the migration has been mostly blind, and
a dream would have proposed from that same blind view. It walks
Two rules, by filename:

  open.md   -- the whole file IS the open-questions doc under the four-file
               split, so EVERY top-level bullet counts, whatever heading it
               sits under. Requiring an "open question" heading here left
               embarch-ui, embarch-topology and embarch-umbrella printing zero
               bullets while 22 sat in them (fixed 2026-09-05, tasks/doc/003);
               those three title their file "<name>: open", and the five that
               printed did so only because their own title happened to contain
               the word "questions". DOC-CONVENTIONS.md §2 records that open.md
               needs no heading for this script.
  design.md, embarch-token.md
            -- a section doc, so only bullets under a heading whose text
               contains "open question" (case-insensitive -- headings vary:
               "Open questions / future work", "Open questions").

Bullets are grouped by doc.

This is a reporting tool, not a CI gate — unlike check-links.py/
check-staleness.py, an "open question" existing isn't a failure, so this
always exits 0. Run it locally when you want the suite-wide view; nothing
currently runs it automatically.

Usage: scripts/collect-open-questions.py   (run from anywhere; paths are repo-relative)
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADING_RE = re.compile(r'^(#{1,3})\s+(.*)$')
BULLET_RE = re.compile(r'^-\s+(.*)$')


def find_design_docs(root):
    """design.md files plus any root-level doc that carries its own open-questions section."""
    docs = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for name in filenames:
            if name in ('open.md', 'design.md'):
                docs.append(os.path.join(dirpath, name))
    for extra in ('embarch-token.md',):
        path = os.path.join(root, extra)
        if os.path.exists(path):
            docs.append(path)
    return sorted(docs)


def extract_open_questions(path):
    """Every top-level bullet that counts as an open question in this doc.

    In an open.md the whole file qualifies; elsewhere only the bullets under an
    'open question(s)' heading do. See the module docstring.
    """
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    whole_file = os.path.basename(path) == 'open.md'
    bullets = []
    in_section = whole_file
    section_level = None
    for line in lines:
        heading_match = HEADING_RE.match(line)
        if heading_match:
            if whole_file:
                continue
            level = len(heading_match.group(1))
            title = heading_match.group(2)
            if 'open question' in title.lower():
                in_section = True
                section_level = level
                continue
            if in_section and level <= section_level:
                in_section = False
            continue
        if in_section:
            bullet_match = BULLET_RE.match(line)
            if bullet_match:
                bullets.append(bullet_match.group(1).strip())
    return bullets


def main():
    docs = find_design_docs(REPO_ROOT)
    total = 0
    print("# Suite-wide open questions\n")
    print("Collected from every sub-project's open.md in full, plus the \"Open questions\" section "
          "of any design.md that still carries one — those remain the source of truth; this is a "
          "read-only index, not a copy to edit.\n")

    for path in docs:
        bullets = extract_open_questions(path)
        if not bullets:
            continue
        rel = os.path.relpath(path, REPO_ROOT)
        print(f"## {rel}\n")
        for b in bullets:
            print(f"- {b}")
            total += 1
        print()

    print(f"---\n{total} open question(s) across {sum(1 for p in docs if extract_open_questions(p))} doc(s).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
