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
or in inline code, and otherwise falls back to the file's own sub-project. A
`tasks/<scope>/` file, and a `history/`, `changelog.d/` or `features.d/` file
named for a scope, belongs to that scope's sub-project (SCOPED_BY_NAME). The
suite is a sub-project here too: `suite/decisions/`, cited `suite decision N`.

Four outcomes, and three of them fail:
  * ERROR   -- a citation that names ONE topic file which does not define N.
               The one reference shape that names a file rather than a
               sub-project, and therefore the only one that can go stale while
               still resolving: a mission split moves an entry between topic
               files without renumbering it, so the old path keeps working and
               names the wrong file. `check-links.py` sees a path that exists;
               nothing saw what was in it, and `topology/010` produced exactly
               this on 2026-09-06 (decision 21, `enrollment.md` ->
               `validation.md`). DOC-CONVENTIONS.md's fix is to link
               `<sub>/decisions.md`, the routing table a splitter maintains.
               Added 2026-09-09 for `[decision N](<topic>)` (tasks/doc/027);
               since 2026-10-29 also the number beside the link --
               `[embarch-x](<topic>) decision N`, `[decisions](<topic>) N` -- and
               any relative href, which found 12 stale citations green on main
               (tasks/doc/056). NOT seen: a number cited near a topic path in
               prose that is not adjacent to it, and anything outside `*.md`
               (source comments in the code repos).
  * ERROR   -- attributed by an explicit nearby path, number not defined there.
  * ERROR   -- number defined by NO sub-project anywhere. This is the genuinely
               dangling reference a renumber or a deletion leaves behind, and
               the one a compaction pass must never produce.
  * WARNING -- number missing from the file's own sub-project but defined by
               some other one, with no path nearby to say which. That is
               ambiguous prose, not a broken reference: DOC-CONVENTIONS.md's
               canonical `<sub-project> decision N` form is the fix. Reported,
               does not fail. What is left in it (205 on 2026-10-29, down from
               1,732 before SCOPED_BY_NAME, tasks/doc/060) is root docs, scopes
               with no decisions of their own (`doc`, `fleet`), and a bare
               number crossing into another sub-project -- the last kind is the
               one worth reading.

Entry definitions come from a sub-project's `design.md` decisions section (the
`## N. ...decision...` heading up to the next `## `, so an ordinary numbered
list elsewhere in that doc cannot invent an entry) and, where the extraction of
DOC-PROTOCOL.md §3 has happened, from the whole of its `decisions.md` -- or,
where those outgrew one file, from every `decisions/<topic>.md` under it.

Findings in `inbox/*.md` are WARNINGS, never failures (2026-09-06,
tasks/doc/015), for the same reason and on the same rule as check-links.py --
read that file's header for the argument. The shape this script sees is the
second and third of the three: a drop cites the decision number it is itself
*proposing*, or one that exists on a commit the owner's checkout has not
pulled. Both are correct-by-construction in a drop and both are errors the
moment the drain makes it a committed `tasks/` file.

Usage: scripts/check-decision-refs.py [--verbose] [--warnings]
Exit status: 0 if no errors outside inbox/, 1 otherwise.
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
# `##` counts too (tasks/doc/060, 070): `suite/decisions/<topic>.md` heads its
# entries one level below the file's own title, so until 2026-10-29 the suite
# defined nothing here and every suite citation was unchecked or, named by its
# path, a false red. This pattern is only tried inside a decisions file or a
# design.md's decisions section -- where a `## ` line is a section boundary and
# is consumed before it gets here -- and on 2026-10-29 the only `## N — ` lines
# in any decisions file were the suite's four.
DEF_HEAD = re.compile(r'^#{2,4}\s+(\d+(?:\s*,\s*\d+)*)\s+[-—]\s')

# References: "decision 39", "decisions 31/32/33", "decisions 58-62",
# optionally prefixed by a section marker that this convention no longer needs.
# The keyword must start a word, and a hyphen does not start one
# (tasks/doc/068): a byte budget called a per-<keyword> cap is an adjective,
# and the number after it is a size. Without the guard that sentence, in a
# supervisor's claim commit, turned the gate red on `main` for a whole leg.
NUMS = r'(\d+(?:\s*[/,]\s*\d+|\s*[-–—]\s*\d+|\s+and\s+\d+)*)'
REF = re.compile(r'(?<![\w-])decisions?\s+' + NUMS, re.I)
# "4,096" is one number. Read as a list it yielded 4 and 96, and the second
# is a real decision number in some sub-projects -- a size misreported as a
# citation. A comma with exactly three digits after it and no space is a
# thousands separator; a list is written "2, 3" or "2,3".
THOUSANDS = re.compile(r'\b\d{1,3}(?:,\d{3})+(?!\d)')
# A sub-project doc path, in a markdown link or in inline code -- both are used.
# The topic-file arm was added 2026-09-09 (tasks/doc/027): a mission split moves
# an entry between `decisions/<topic>.md` files, and until then a nearby
# `embarch-topology/decisions/enrollment.md` attributed nothing, so the
# reference fell back to the LINKING file's sub-project -- usually the wrong one.
DOC_PATH = re.compile(r'([a-z0-9-]+)/(?:(?:design|decisions)\.md'
                      r'|decisions/[a-z0-9-]+\.md)')

# A LINK whose text cites a decision number and whose href is a topic file:
# `[decision 21](../embarch-topology/decisions/enrollment.md)`. This is the one
# reference shape whose target names a file rather than a sub-project, so it is
# the only one that can go stale while still resolving -- which is exactly what
# neither gate could see. `check-links.py` validates that the path exists;
# nothing checked what the file at the end of it DEFINES.
# The href pattern is ANY `.md`, judged only once it resolves to an indexed
# topic file, and that is not cosmetic. The commonest form is written from
# inside the sub-project as a bare `decisions/<topic>.md`; a decisions file
# citing its sibling writes just `core-link.md`, and a pattern requiring
# `decisions/` in the href missed every one of those (tasks/doc/044:
# `embarch-api/decisions/tests.md` cited decision 55 that way, stale and green).
TOPIC_LINK = re.compile(r'\[([^\]]*?)\]\(([^)\s#]+\.md)(?:#[^)\s]*)?\)')
TOPIC_REL = re.compile(r'([a-z0-9-]+)/decisions/([a-z0-9-]+)\.md$')
# The number may sit OUTSIDE the link (tasks/doc/056). The link text names the
# repo or the topic and the sentence carries the number:
#   [embarch-study-designer](…/decisions/versioning.md) decision 40
#   ([decisions](…/decisions/core-link.md) 62)
# The first needs the keyword after the link. The second -- a bare number --
# counts only when the link text itself says "decision", which is the one way
# an author writes it; anything else is a number that merely follows a link.
AFTER_KW = re.compile(r"(?:'s)?\s*decisions?\s+" + NUMS, re.I)
AFTER_BARE = re.compile(r'\s*' + NUMS)
FENCE = re.compile(r'^\s*(?:```|~~~)')
SECTION_HEAD = re.compile(r'^##\s')
DECISIONS_HEAD = re.compile(r'^##\s+\d+[a-z]?\.\s.*decision', re.I)
SKIP_DIRS = {'.git', '.github', 'scripts', '.claude'}
# Gitignored staging directory. Scanned, but its findings warn rather than fail;
# `inbox/README.md` is committed (.gitignore negates it) so it is NOT exempt.
INBOX = 'inbox/'


def is_drop(rel):
    """True for a gitignored inbox drop; False for inbox/README.md and all else."""
    rel = rel.replace(os.sep, '/')
    return rel.startswith(INBOX) and os.path.basename(rel) != 'README.md'

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
# "suite decision 4" is the same form for the suite (tasks/doc/060): all 40
# such citations on 2026-10-29 named 1-4, so none turned red when it began
# counting -- and without it, one written inside `embarch-ui/` resolved
# silently against embarch-ui's OWN decision 4.
CANONICAL = re.compile(r'\b(embarch-[a-z0-9-]+|[Ss]uite)\W{1,3}$')
# Above this, a "decision" number is a year or a version, not an entry.
MAX_DECISION = 400


def md_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith('.md'):
                yield os.path.join(dirpath, name)


# Files that belong to a scope by NAME rather than by directory (tasks/doc/060):
# `tasks/<scope>/*.md`, and `history/`, `changelog.d/`, `features.d/` files
# named `<scope>.md` or `<scope>-*.md`. A bare `decision N` in one means that
# scope's, exactly as it does in `<sub>/spec.md`. Until 2026-10-29 they fell
# back to their directory, which defines nothing, so every reference in them to
# a real decision was "ambiguous": 1,506 of the 1,732 reported, burying the
# ~200 that really are.
SCOPED_BY_NAME = ('history', 'changelog.d', 'features.d')


def subproject_of(path, index=()):
    """The sub-project a file's bare `decision N` means: its top directory, or
    the scope its name carries under tasks/ and SCOPED_BY_NAME. None for a
    root doc."""
    parts = os.path.relpath(path, REPO_ROOT).split(os.sep)
    if len(parts) == 1:
        return None
    named = None
    if parts[0] == 'tasks' and len(parts) == 3:
        named = next((s for s in ('embarch-' + parts[1], parts[1])
                      if s in index), None)
    elif parts[0] in SCOPED_BY_NAME:
        for sub in sorted(index, key=len, reverse=True):   # dev-bench > dev
            scope = sub[len('embarch-'):] if sub.startswith('embarch-') else sub
            if parts[-1].startswith((scope + '.', scope + '-')):
                named = sub
                break
    return named or parts[0]


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


def build_file_index():
    """`<sub>/decisions/<topic>.md` -> the set of numbers THAT FILE defines.

    `build_index()` answers "which sub-project defines N", which is what
    DOC-CONVENTIONS.md says a number addresses. This answers "which file", and
    it exists only to check the one shape that names a file: a `[decision N]`
    link pointed straight at a topic file (tasks/doc/027).
    """
    index = {}
    for path in md_files():
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')
        parts = rel.split('/')
        if len(parts) != 3 or parts[1] != 'decisions':
            continue
        nums = index.setdefault(rel, set())
        with open(path, encoding='utf-8') as f:
            for line in f:
                m = DEF_LIST.match(line) or DEF_HEAD.match(line)
                if m:
                    nums.update(int(n) for n in re.findall(r'\d+', m.group(1)))
    return index


def named_files(rel, line, file_index):
    """(num, target) for every number a citation on this line places in ONE
    topic file (see TOPIC_LINK and AFTER_KW). Numbers above MAX_DECISION kept;
    the caller skips them."""
    out = []
    for m in TOPIC_LINK.finditer(line):
        text, href = m.group(1), m.group(2)
        target = os.path.normpath(
            os.path.join(os.path.dirname(rel), href)).replace(os.sep, '/')
        if target not in file_index:
            continue      # not an indexed topic file; check-links owns it
        ref = REF.search(text)
        after = line[m.end():]
        if not ref:
            ref = AFTER_KW.match(after)
        if not ref and 'decision' in text.lower():
            ref = AFTER_BARE.match(after)
        if ref:
            out += [(num, target) for num in expand(ref.group(1))]
    return out


def check_topic_links(file_index):
    """(rel, lineno, num, href, defining, excerpt) per stale topic-file citation.

    A mission split moves an entry between a sub-project's decision files
    without renumbering it (DOC-CONVENTIONS.md), so the OLD path keeps
    resolving while naming a file that no longer holds the number.
    `topology/010` did exactly this on 2026-09-06: decision 21 moved
    `enrollment.md` -> `validation.md` and a `history/topology.md` link went on
    pointing at `enrollment.md`.

    Only a citation whose target is a topic file this repo actually indexes is
    judged. A number the sub-project does not define at all is the existing
    check's business, not this one -- reported there, once. Fenced blocks are
    skipped: a task quoting the defective shape is reporting it, not making it.
    """
    bad, checked = [], 0
    for path in md_files():
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
        fenced = False
        for lineno, line in enumerate(lines, 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced or 'decision' not in line.lower():
                continue
            for num, target in named_files(rel, line, file_index):
                if num > MAX_DECISION:
                    continue
                checked += 1
                if num in file_index[target]:
                    continue
                # Where in that sub-project it actually lives, if anywhere.
                sub = TOPIC_REL.search(target).group(1)
                defining = sorted(
                    f for f, nums in file_index.items()
                    if num in nums and f.split('/')[0] == sub)
                bad.append((rel, lineno, num, target, defining,
                            line.strip()[:110]))
    return bad, checked


def expand(numbers_text):
    """'31/32/33' -> [31,32,33]; '58-62' -> [58..62]; '39' -> [39];
    '4,096' -> [4096], which MAX_DECISION then discards as a size."""
    text = THOUSANDS.sub(lambda m: m.group(0).replace(',', ''),
                         numbers_text.strip())
    dash = re.fullmatch(r'(\d+)\s*[-–—]\s*(\d+)', text)
    if dash:
        lo, hi = int(dash.group(1)), int(dash.group(2))
        return list(range(lo, hi + 1)) if 0 < hi - lo < 40 else [lo, hi]
    return [int(n) for n in re.findall(r'\d+', text)]


def resolve_line(line, own, index, defined_anywhere):
    """Every `decision N` on one line -> (num, target, verdict), verdict one of
    'ok', 'warn', or the error text. Numbers above MAX_DECISION are dropped."""
    out = []
    for m in REF.finditer(line):
        # Look back a short window only: these lines are whole
        # paragraphs and routinely name several sub-projects.
        window = line[max(0, m.start() - ATTRIB_WINDOW):m.start()]
        explicit, trusted = None, False
        canonical = CANONICAL.search(window)
        if canonical and canonical.group(1).lower() in index:
            explicit = canonical.group(1).lower()      # §7.3 form: trusted
            trusted = True
        else:
            for hit in DOC_PATH.finditer(window):
                if hit.group(1) in index:
                    explicit = hit.group(1)
        # Prefer the file's own sub-project when it defines the
        # number: a paragraph naming another doc is not a
        # reference to it. Only §7.3's form overrides that -- and until
        # 2026-10-29 it did not: "embarch-b decision 2" inside embarch-a passed
        # on embarch-a's own 2. No such citation existed when this was
        # enforced; every sub-project defines 1-4, so suite citations need it.
        target = explicit or own
        for num in expand(m.group(1)):
            if num > MAX_DECISION:
                continue      # a year or a version, not an entry
            if target is not None and num in index.get(target, ()):
                verdict = 'ok'
            elif not trusted and own is not None and num in index.get(own, ()):
                verdict = 'ok'      # own sub-project defines it
            elif num not in defined_anywhere:
                verdict = 'defined by no sub-project'
            elif explicit is not None:
                verdict = f'not defined by {target}'
            else:
                verdict = 'warn'
            out.append((num, target, verdict))
    return out


# Fixtures for the shapes this script has misread, run on every invocation so
# a regression fails the gate rather than a reviewer. They live here, not in a
# tracked .md, because a doc that spells a misread shape trips the very check
# it describes (tasks/doc/068, tasks/doc/070). Synthetic index: `embarch-a`
# defines 1-3, `embarch-b` defines 96, `suite` defines 4.
SELF_TEST = (
    # tasks/doc/068's reproduction, then each of its two causes alone: a
    # hyphenated compound is not a citation, and a thousands separator does
    # not split one number into two.
    ('embarch-a', 'the per-' + 'decision 4,096 B cap', []),
    ('embarch-a', 'a per-' + 'decision 3 budget', []),
    ('embarch-a', 'a ' + 'decision 4,096 bytes long', []),
    ('embarch-a', 'decisions 2,3 and 1', [(2, 'ok'), (3, 'ok'), (1, 'ok')]),
    ('embarch-a', 'embarch-b ' + 'decision 96', [(96, 'ok')]),
    ('embarch-a', 'embarch-b ' + 'decision 2', [(2, 'not defined by embarch-b')]),
    # tasks/doc/060: "suite decision N" names the suite, so inside a
    # sub-project that also defines N it is not resolved against its own...
    ('embarch-a', 'per [Suite ' + 'decision 4](../../suite/decisions.md)',
     [(4, 'ok')]),
    ('embarch-a', 'suite ' + 'decision 2', [(2, 'not defined by suite')]),
    # ...and tasks/doc/070: naming the suite's topic file is not a false red.
    ('embarch-a', 'the `suite/decisions/placement.md` ' + 'decision 4',
     [(4, 'ok')]),
)


# Citations that name ONE topic file: (citing file, line, [(num, held?)]).
# Synthetic topic files: embarch-a/decisions/x.md holds 1, y.md holds 2 and 3.
SELF_TEST_FILES = (
    # tasks/doc/056: the link text is the repo, the number follows the link.
    ('embarch-b/decisions/z.md', 'surface for [embarch-a]'
     '(../../embarch-a/decisions/x.md) ' + 'decision 2.', [(2, False)]),
    ('history/a.md', '([decisions](../embarch-a/decisions/x.md) 3).',
     [(3, False)]),
    ('history/a.md', '[decisions](../embarch-a/decisions/y.md) 3', [(3, True)]),
    # A bare number after a link whose text does not say "decision" is not one.
    ('embarch-b/spec.md', '[x](../embarch-a/decisions/x.md) 3 times', []),
    # A sibling href, written from inside decisions/, is resolved too.
    ('embarch-a/decisions/y.md', '[' + 'decision 1](x.md)', [(1, True)]),
)


def self_test():
    """A list of failure lines; empty when every fixture reads as recorded."""
    index = {'embarch-a': {1, 2, 3}, 'embarch-b': {96}, 'suite': {4}}
    anywhere = set().union(*index.values())
    files = {'embarch-a/decisions/x.md': {1}, 'embarch-a/decisions/y.md': {2, 3}}
    bad = []
    for own, line, want in SELF_TEST:
        got = [(n, v) for n, _, v in resolve_line(line, own, index, anywhere)]
        if got != want:
            bad.append(f'  {line!r}: want {want}, got {got}')
    for rel, line, want in SELF_TEST_FILES:
        got = [(n, n in files[t]) for n, t in named_files(rel, line, files)]
        if got != want:
            bad.append(f'  {line!r}: want {want}, got {got}')
    return bad


def main():
    verbose = '--verbose' in sys.argv
    show_warnings = '--warnings' in sys.argv
    broken = self_test()
    if broken:
        print('check-decision-refs.py misreads its own fixtures:\n')
        print('\n'.join(broken))
        return 1
    index = build_index()
    defined_anywhere = set().union(*index.values()) if index else set()
    errors, warnings, checked = [], [], 0

    for path in md_files():
        own = subproject_of(path, index)
        rel = os.path.relpath(path, REPO_ROOT)
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                if 'decision' not in line.lower():
                    continue
                for num, target, verdict in resolve_line(
                        line, own, index, defined_anywhere):
                    checked += 1
                    if verdict == 'ok':
                        continue
                    excerpt = line.strip()[:110]
                    if verdict == 'warn':
                        warnings.append((rel, lineno, own, num, excerpt))
                    else:
                        errors.append((rel, lineno, target, num, excerpt,
                                       verdict))

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
    file_index = build_file_index()
    bad_links, links_checked = check_topic_links(file_index)

    # inbox/ drops warn; everything else fails. Split BEFORE any exit decision.
    drop_errors = [e for e in errors if is_drop(e[0])]
    errors = [e for e in errors if not is_drop(e[0])]
    drop_rows = [r for r in bad_rows if is_drop(r[0])]
    bad_rows = [r for r in bad_rows if not is_drop(r[0])]
    drop_links = [b for b in bad_links if is_drop(b[0])]
    bad_links = [b for b in bad_links if not is_drop(b[0])]

    if drop_errors or drop_rows or drop_links:
        # NOTE: is the marker check-docs.py surfaces on an otherwise-green run.
        print(f'NOTE: {len(drop_errors) + len(drop_rows) + len(drop_links)} '
              f'unresolved citation(s) in gitignored inbox/ drops -- warnings, '
              f'not failures; the drain re-checks them as errors.')
        for rel, lineno, target, num, excerpt, why in drop_errors:
            print(f'  (inbox) {rel}:{lineno} decision {num} -- {why}')
        for rel, lineno, num, excerpt in drop_rows:
            print(f'  (inbox) {rel}:{lineno} reversals row {num} -- not defined')
        for rel, lineno, num, target, defining, excerpt in drop_links:
            print(f'  (inbox) {rel}:{lineno} decision {num} -- {target} does '
                  f'not define it')
        print()

    if bad_links:
        print(f'{len(bad_links)} citation(s) naming a topic file that does '
              f'not define the number:\n')
        for rel, lineno, num, target, defining, excerpt in bad_links:
            where = ', '.join(defining) if defining else 'nowhere in that sub-project'
            print(f'  {rel}:{lineno} decision {num} -> {target}')
            print(f'      defined in: {where}')
            print(f'      {excerpt}')
        print('\nA mission split moves an entry between decision files without '
              'renumbering it,\nso the old path keeps resolving while naming the '
              'wrong file -- check-links.py sees\na path that exists and this '
              'used to see a sub-project. DOC-CONVENTIONS.md: LINK THE\nINDEX, '
              'not the topic file. `<sub>/decisions.md` is a routing table its '
              'splitter\nmaintains, so it survives the move; repoint at that, '
              'or drop the link and use the\nbare number.')
        print()

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

    if bad_rows or bad_links:
        return 1

    print(f'All {checked} decision references resolve. '
          f'{len(warnings)} ambiguous (--warnings to list), not an error.')
    print(f'All {links_checked} citation(s) naming a topic file name the '
          f'file that defines the number\n  (DOC-CONVENTIONS.md prefers the '
          f'index: {len(file_index)} topic files indexed).')
    print(f'All {rows_checked} reversal-row citations resolve '
          f'({rows_defined} rows defined).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
