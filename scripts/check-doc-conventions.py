#!/usr/bin/env python3
"""Check every doc's `**Status:**` line against DOC-PROTOCOL.md §7.1.

The line must be the first non-blank line after the title, and must read:

    **Status:** <state>, <date><anything>

where <state> is exactly one of §7.1's tokens and <date> is ISO yyyy-mm-dd.
Only those two are the machine-readable part; whatever prose follows the date
is free, and most docs here have some.

Why it exists: before 2026-08-31 these lines were free prose. Two spellings of
the label were in use (`**Status:** x` and `**Status: x**`), five docs had no
status line at all, and the state words in play included draft, closed, CLOSED,
done, Paused, Planned, and "in progress" -- so nothing could read a doc's state
mechanically. `scripts/check-staleness.py` is a heuristic over two tables and
embarch-core's own `doctor` check 11 is a stub, both for want of exactly this.

Usage: scripts/check-doc-conventions.py [--verbose]
Exit status: 0 if every doc conforms, 1 otherwise.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATES = ('draft', 'active', 'done', 'planned', 'paused', 'proposal', 'retired')
STATUS_RE = re.compile(
    r'^\*\*Status:\*\* (' + '|'.join(STATES) +
    r'|superseded-by:\S+), (\d{4}-\d{2}-\d{2})(?=[.,;:\s(—]|$)')
ANY_STATUS = re.compile(r'^\*\*Status:', re.I)

# Docs that carry no status: instruction files for tools, not records of state.
EXEMPT = {'README.md', 'CLAUDE.md', 'LICENSE'}
# changelog.d/ holds one-line fragments, not docs (changelog.d/README.md is
# already exempt by name); history/archive/ holds rolled-out windows that carry
# their own status from the roll.
SKIP_DIRS = {'.git', '.github', 'scripts', '.claude', 'changelog.d'}


def md_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith('.md') and name not in EXEMPT:
                yield os.path.join(dirpath, name)


def main():
    verbose = '--verbose' in sys.argv
    problems, ok = [], []

    for path in md_files():
        rel = os.path.relpath(path, REPO_ROOT)
        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n')
        status_lines = [(n, l) for n, l in enumerate(lines[:12], 1)
                        if ANY_STATUS.match(l)]
        if not status_lines:
            problems.append((rel, 0, 'no **Status:** line in the first 12 lines'))
            continue
        lineno, line = status_lines[0]
        m = STATUS_RE.match(line)
        if not m:
            problems.append((rel, lineno,
                             'malformed; want "**Status:** <state>, <yyyy-mm-dd>" '
                             f'with <state> in {{{", ".join(STATES)}}} '
                             f'-- got: {line[:70]}'))
            continue
        ok.append((rel, m.group(1), m.group(2)))

    if verbose:
        width = max(len(r) for r, _, _ in ok) if ok else 0
        for rel, state, date in ok:
            print(f'  {rel:{width}s}  {state:16s} {date}')
        print()

    if problems:
        print(f'{len(problems)} doc(s) violate DOC-PROTOCOL.md §7.1:\n')
        for rel, lineno, why in problems:
            where = f'{rel}:{lineno}' if lineno else rel
            print(f'  {where} -- {why}')
        return 1

    print(f'All {len(ok)} docs carry a conformant **Status:** line '
          f'(DOC-PROTOCOL.md §7.1).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
