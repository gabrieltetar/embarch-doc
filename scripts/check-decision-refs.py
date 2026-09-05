#!/usr/bin/env python3
"""Check that every prose reference to a numbered design decision resolves.

DOC-CONVENTIONS.md: a decision number addresses a *sub-project*, not a file
and not a section. This script builds the set of decision numbers each
sub-project actually defines (from its `design.md`, plus `decisions.md` once
DOC-PROTOCOL.md §3's extraction threshold has moved them there), then walks
every *.md in the repo and resolves every `decision N`-shaped reference
against it.

Why it exists: a grep for `§N decision M`-shaped references returned 1335 hits
on 2026-08-31, and `scripts/check-links.py` structurally cannot see one of
them -- it validates file paths and explicitly skips in-page anchors, and a
prose reference to "decision 39" is not a link at all. Renumbering or dropping
an entry silently invalidates references that nothing checked. This is also
what makes a compaction pass (DOC-COMPACTION.md) verifiable rather than
trusted: it is the check behind that doc's §6 rule against renumbering.

Attribution is a heuristic, and this repo writes one paragraph per line, so
"somewhere on the same line" is far too coarse -- a paragraph routinely names
three sub-projects. So attribution looks backwards a short window (ATTRIB_WINDOW
chars) from the reference for a `<sub-project>/design.md`-shaped path, in a link
or in inline code, and otherwise falls back to the file's own sub-project.

Three outcomes, and only two of them fail:
  * ERROR   -- attributed by an explicit nearby path, number not defined there.
  * ERROR   -- number defined by NO sub-project anywhere. This is the genuinely
               dangling reference a renumber or a deletion leaves behind, and
               the one a compaction pass must never produce.
  * WARNING -- number missing from the file's own sub-project but defined by
               some other one, with no path nearby to say which. That is
               ambiguous prose, not a broken reference: DOC-CONVENTIONS.md's
               canonical `<sub-project> decision N` form is the fix. Reported,
               does not fail.

Entry definitions come from a sub-project's `design.md` decisions section (the
`## N. ...decision...` heading up to the next `## `, so an ordinary numbered
list elsewhere in that doc cannot invent an entry) and, where the extraction of
DOC-PROTOCOL.md §3 has happened, from the whole of its `decisions.md` -- or,
where those outgrew one file, from every `decisions/<topic>.md` under it.

Usage: scripts/check-decision-refs.py [--verbose] [--warnings]
Exit status: 0 if no errors, 1 otherwise.
"""
import glob
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Entry definitions. Pre-compaction list form and post-compaction heading form
# (DOC-CONVENTIONS.md) are both accepted; retired entries still count
# as defined, which is the whole point of a tombstone.
DEF_LIST = re.compile(r'^(\d+)\.\s+(?:~~)?\*\*')
# An entry may own several numbers when decisions were merged under a byte
# budget (DOC-COMPACTION.md §5): '### 20, 21, 25, 27 — Streaming capture'.
# Every listed number stays resolvable, so every reference keeps working.
DEF_HEAD = re.compile(r'^#{3,4}\s+(\d+(?:\s*,\s*\d+)*)\s+[-—]\s')

# References: "decision 39", "decisions 31/32/33", "decisions 58-62",
# optionally prefixed by a section marker that this convention no longer needs.
REF = re.compile(r'decisions?\s+((?:\d+)(?:\s*[/,]\s*\d+|\s*[-–—]\s*\d+|\s+and\s+\d+)*)', re.I)
# A sub-project doc path, in a markdown link or in inline code -- both are used.
DOC_PATH = re.compile(r'([a-z0-9-]+)/(?:design|decisions)\.md')
SECTION_HEAD = re.compile(r'^##\s')
DECISIONS_HEAD = re.compile(r'^##\s+\d+[a-z]?\.\s.*decision', re.I)
SKIP_DIRS = {'.git', '.github', 'scripts', '.claude'}

# A reversal row is cited as "reversals.md ... row 86" / "rows 83-85". The rows
# live in reversals/rows-<a>-<b>.md and a row number is a permanent identity, so
# a citation resolves against the union of every range file -- not against a
# path. Nothing checked this until 47 rows were deleted with a changelog section
# and fifteen citations went on pointing at them.
ROW_DEF = re.compile(r'^\|\s*(\d+)\s*\|', re.M)
ROW_REF = re.compile(r'reversals(?:/rows-[\d-]+)?\.md\)?[^.]{0,8}?'
                     r'rows?\s+((?:\d+)(?:\s*[,/]\s*\d+|\s*[-\u2013\u2014]\s*\d+'
                     r'|\s+and\s+\d+)*)', re.I)


def reversal_rows():
    """Every row number defined by a reversals/rows-*.md range file."""
    rows = set()
    pattern = os.path.join(REPO_ROOT, 'reversals', 'rows-*.md')
    for path in sorted(glob.glob(pattern)):
        with open(path, encoding='utf-8') as fh:
            rows |= {int(n) for n in ROW_DEF.findall(fh.read())}
    return rows


def check_reversal_rows():
    """Return a list of (rel, lineno, num, excerpt) for rows cited and undefined."""
    defined = reversal_rows()
    if not defined:
        return [], 0, 0
    bad, checked = [], 0
    for path in md_files():
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')
        if rel.startswith('reversals/'):
            continue
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
        for lineno, line in enumerate(lines, 1):
            for m in ROW_REF.finditer(line):
                for num in expand(m.group(1)):
                    checked += 1
                    if num not in defined:
                        excerpt = line[max(0, m.start() - 40):m.end() + 40].strip()
                        bad.append((rel, lineno, num, excerpt))
    return bad, checked, len(defined)
# How far back from a reference to look for an explicit sub-project path.
# Deliberately short: at 140 chars a paragraph's earlier mention of a different
# sub-project hijacked references that belonged to the file's own, which was
# 10 of this script's first 179 reported "errors" -- all of them wrong.
ATTRIB_WINDOW = 44
# DOC-CONVENTIONS.md's canonical cross-project form, which IS unambiguous:
# "embarch-study-designer decision 39". Attribution from this is trusted.
CANONICAL = re.compile(r'\b(embarch-[a-z0-9-]+)\W{1,3}$')
# Above this, a "decision" number is a year or a version, not an entry.
MAX_DECISION = 400


def md_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith('.md'):
                yield os.path.join(dirpath, name)


def subproject_of(path):
    """The sub-project directory a file belongs to, or None for root docs."""
    rel = os.path.relpath(path, REPO_ROOT)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else None


def build_index():
    """sub-project -> set of decision numbers it defines."""
    index = {}
    for path in md_files():
        rel_parts = os.path.relpath(path, REPO_ROOT).split(os.sep)
        is_group = len(rel_parts) == 3 and rel_parts[1] == 'decisions'
        if os.path.basename(path) not in ('design.md', 'decisions.md') and not is_group:
            continue
        sub = rel_parts[0] if len(rel_parts) > 1 else None
        if sub is None:
            continue
        nums = index.setdefault(sub, set())
        # A standalone decisions.md IS the decisions section end to end; inside
        # a design.md, only the numbered section whose heading says "decision".
        whole_file = os.path.basename(path) == 'decisions.md' or is_group
        in_decisions = whole_file
        with open(path, encoding='utf-8') as f:
            for line in f:
                if not whole_file and SECTION_HEAD.match(line):
                    in_decisions = bool(DECISIONS_HEAD.match(line))
                    continue
                if not in_decisions:
                    continue
                m = DEF_LIST.match(line) or DEF_HEAD.match(line)
                if m:
                    nums.update(int(n) for n in re.findall(r'\d+', m.group(1)))
    return index


def expand(numbers_text):
    """'31/32/33' -> [31,32,33]; '58-62' -> [58..62]; '39' -> [39]."""
    text = numbers_text.strip()
    dash = re.fullmatch(r'(\d+)\s*[-–—]\s*(\d+)', text)
    if dash:
        lo, hi = int(dash.group(1)), int(dash.group(2))
        return list(range(lo, hi + 1)) if 0 < hi - lo < 40 else [lo, hi]
    return [int(n) for n in re.findall(r'\d+', text)]


def main():
    verbose = '--verbose' in sys.argv
    show_warnings = '--warnings' in sys.argv
    index = build_index()
    defined_anywhere = set().union(*index.values()) if index else set()
    errors, warnings, checked = [], [], 0

    for path in md_files():
        own = subproject_of(path)
        rel = os.path.relpath(path, REPO_ROOT)
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                if 'decision' not in line.lower():
                    continue
                for m in REF.finditer(line):
                    # Look back a short window only: these lines are whole
                    # paragraphs and routinely name several sub-projects.
                    window = line[max(0, m.start() - ATTRIB_WINDOW):m.start()]
                    explicit = None
                    canonical = CANONICAL.search(window)
                    if canonical and canonical.group(1) in index:
                        explicit = canonical.group(1)      # §7.3 form: trusted
                    else:
                        for hit in DOC_PATH.finditer(window):
                            if hit.group(1) in index:
                                explicit = hit.group(1)
                    # Prefer the file's own sub-project when it defines the
                    # number: a paragraph naming another doc is not a
                    # reference to it. Only §7.3's form overrides that.
                    target = explicit or own
                    for num in expand(m.group(1)):
                        if num > MAX_DECISION:
                            continue      # a year or a version, not an entry
                        checked += 1
                        if target is not None and num in index.get(target, ()):
                            continue
                        if own is not None and num in index.get(own, ()):
                            continue      # own sub-project defines it
                        excerpt = line.strip()[:110]
                        if num not in defined_anywhere:
                            errors.append((rel, lineno, target, num, excerpt,
                                           'defined by no sub-project'))
                        elif explicit is not None:
                            errors.append((rel, lineno, target, num, excerpt,
                                           f'not defined by {target}'))
                        else:
                            warnings.append((rel, lineno, own, num, excerpt))

    if verbose:
        print('Decision entries defined per sub-project:')
        for sub in sorted(index):
            nums = index[sub]
            print(f'  {sub:28s} {len(nums):3d} entries'
                  f' (1..{max(nums) if nums else 0})')
        print()

    if show_warnings and warnings:
        print(f'{len(warnings)} ambiguous reference(s) -- number not in the '
              f"file's own sub-project, defined elsewhere, no path nearby.")
        print(f'Name the sub-project per DOC-CONVENTIONS.md. Not an error.\n')
        for rel, lineno, own, num, excerpt in warnings:
            print(f'  {rel}:{lineno} decision {num} (not in {own})')
            print(f'      {excerpt}')
        print()

    bad_rows, rows_checked, rows_defined = check_reversal_rows()
    if bad_rows:
        print(f'{len(bad_rows)} citation(s) of a reversal row no range file '
              f'defines (of {rows_defined} rows present):\n')
        for rel, lineno, num, excerpt in bad_rows:
            print(f'  {rel}:{lineno} reversals row {num} -- not defined')
            print(f'      {excerpt}')
        print()

    if errors:
        print(f'{len(errors)} unresolved decision reference(s):\n')
        for rel, lineno, target, num, excerpt, why in errors:
            print(f'  {rel}:{lineno} decision {num} -- {why}')
            print(f'      {excerpt}')
        print(f'\n{checked} references checked, {len(warnings)} ambiguous '
              f'(--warnings to list).')
        return 1

    if bad_rows:
        return 1

    print(f'All {checked} decision references resolve. '
          f'{len(warnings)} ambiguous (--warnings to list), not an error.')
    print(f'All {rows_checked} reversal-row citations resolve '
          f'({rows_defined} rows defined).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
