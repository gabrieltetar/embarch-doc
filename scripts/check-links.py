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

Findings in `inbox/*.md` are WARNINGS, never failures (2026-09-06,
tasks/doc/015). Drops are gitignored, so they exist only in the owner's main
checkout and never in a leg's worktree -- the same pending drop makes the
owner's gate red while every worker's is green. And a drop legitimately does
not resolve: it is written at the depth of the file it will *become*, and it
cites the decision or the commit it is *proposing*. Three shapes seen, all
correct-by-construction: a relative link written from the drop's future home;
a decision number the drop itself proposes; and a citation of a decision that
does exist but on a commit the owner's checkout has not pulled yet -- that
last one self-heals on `git pull` and is why "just drain promptly" was
rejected as the fix.

The hard catch is the drain, not this run: a drained drop stops being
`inbox/` and becomes a committed `tasks/<scope>/NNN-*.md`, at which point
every finding here is an error again. That is not theoretical -- it is how
`tasks/api/023` was caught (tasks/doc/018). So a malformed drop is still
refused, one step later, by the actor who moved it.

Link syntax inside fenced code blocks and inline code spans is IGNORED
(2026-09-06, tasks/doc/018), the way a renderer ignores it. Before this, a doc
that explained a convention by quoting an example reference was reported as a
broken link, because the example resolved relative to the doc *explaining* it
rather than the doc that would carry it. The cheapest response — delete the
example — makes the doc worse, and `DOC-CONVENTIONS.md` and the `tasks/` and
`inbox/` READMEs are exactly the docs that want one. It had already cost a leg
directly: `tasks/api/023` failed this check at its own claim commit, before
its worker changed anything.

The coverage that trade costs was measured, not assumed: **zero.** Across the
whole corpus at the time, no `[text](target)` sat inside a code span or a
fence, so nothing stopped being checked. Re-measure before widening this.

The same strip runs over the *anchor* side, and that direction makes the check
STRICTER rather than looser: a `## heading` quoted inside a fenced example used
to mint a real anchor, so a `doc.md#that-heading` link kept resolving against a
heading no reader can see. Also measured at zero fragment links affected, so it
cost nothing to close and a future one it reddens is a real defect.

**Indented (four-space) code blocks are deliberately NOT stripped.** Telling
one from a list item's continuation paragraph needs a real block parser, and
guessing wrong here silently drops a real link from coverage — the failure
this check exists to prevent. Nothing in the corpus needs it. If that changes,
the fix is a parser, not a heuristic.

**A link out of this repo into a sibling resolves against the suite the repo
really lives in** (2026-10-29, tasks/doc/085). DOC-PROTOCOL.md §2 makes every
sub-project a sibling of this repo, so `../../../embarch-ui/tests/element_ids.rs`
is a real file from the owner's checkout. From a worktree under
`.worktrees/embarch-doc/<name>/` the same link lands beside the worktree, where
nothing is, and the gate went red on every leg and every worker before anyone
wrote a byte -- green for the owner, red for everyone else, which is the kind of
red a supervisor learns to discount. So a target that is missing beside the tree
being checked is looked up again under the directory the MAIN checkout sits in
(`git rev-parse --git-common-dir`), which is where the owner's link pointed. A
target missing there too is still broken. Two cases never get the second look:
a link into this repo by name, which must resolve in the tree being checked, and
**`embarch-fleet`**, which step 0 of `.claude/leg.md` links beside every doc
worktree -- without that link `check-docs.py` SKIPS the two framework checks
quietly, so its absence has to stay loud here. The second instance of this
shape (`embarch-dev-bench/decisions/pd-bench.md`, 2026-10-13) was linked by hand
in `.worktrees/` twelve days later; nothing would have caught the third.

Usage: scripts/check-links.py   (run from anywhere; paths are repo-relative)
Exit status: 0 if every relative link outside inbox/ resolves, 1 otherwise.

This exists because embarch-doc is a web of cross-linked docs
(DOC-PROTOCOL.md §5's "link, don't restate" rule) — a renamed or moved file
silently breaks every doc that pointed at it, and that class of drift has
bitten this repo before (embarch-roadmap.md's changelog, 2026-08-05: two
dangling cross-references to a "Next"/"Later" bucket that didn't exist yet).
"""
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(REPO_ROOT)
# The framework repo: linked beside every doc worktree by leg.md step 0, and
# never re-rooted, so a worktree missing that link stays red (see header).
FRAMEWORK = 'embarch-fleet'


def main_checkout():
    """The main checkout this tree belongs to: itself, or a worktree's origin."""
    r = subprocess.run(['git', '-C', REPO_ROOT, 'rev-parse', '--path-format=absolute',
                        '--git-common-dir'], capture_output=True, text=True)
    if r.returncode != 0:
        return REPO_ROOT
    return os.path.dirname(os.path.normpath(r.stdout.strip()))


MAIN = main_checkout()
SUITE = os.path.dirname(MAIN)


def in_suite(resolved):
    """`resolved` re-rooted from this tree's parent onto the suite's, for a
    sibling-repo target that is missing beside the tree being checked."""
    if SUITE == PARENT or resolved.startswith(REPO_ROOT + os.sep):
        return resolved
    rel = os.path.relpath(resolved, PARENT)
    first = rel.split(os.sep)[0]
    if first in (os.pardir, FRAMEWORK, os.path.basename(MAIN)):
        return resolved
    return os.path.join(SUITE, rel)


# Gitignored staging directory; its findings warn rather than fail (see header).
# The exemption is exactly .gitignore's `inbox/*.md` MINUS its `!inbox/README.md`
# negation: that README is committed, is rendered from a framework template, and
# is a doc like any other -- exempting the whole directory would stop checking it.
INBOX = 'inbox/'


def is_drop(rel):
    """True for a gitignored inbox drop; False for inbox/README.md and all else."""
    rel = rel.replace(os.sep, '/')
    return rel.startswith(INBOX) and os.path.basename(rel) != 'README.md'


LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
# An opening or closing fence: three or more backticks or tildes, optionally
# indented. The info string after an opener is ignored.
FENCE_RE = re.compile(r'^\s*(`{3,}|~{3,})')
# An inline code span: a run of N backticks closed by another run of exactly N.
# Confined to one line on purpose -- CommonMark lets a span cross lines, but a
# stray unpaired backtick then swallows everything after it, and losing links
# to a typo is worse than the rare multi-line span this misses.
CODE_SPAN_RE = re.compile(r'(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)')
EXPLICIT_ID_RE = re.compile(r'<a\s+id="([^"]+)"', re.I)
HEADING_RE = re.compile(r'^#{1,6}\s+(.*?)\s*$', re.M)


def strip_code(content):
    """`content` with fenced blocks and inline code spans blanked out.

    Line count is preserved (a stripped line becomes empty) and a code span is
    replaced by spaces of the same width, so anything reported against the
    result still lines up with the file on disk.
    """
    out, fence = [], None
    for line in content.split('\n'):
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                out.append('')
                continue
        else:
            # Only a run of the SAME character, at least as long, closes it.
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            out.append('')
            continue
        out.append(CODE_SPAN_RE.sub(lambda mm: ' ' * len(mm.group(0)), line))
    return '\n'.join(out)


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
    # Headings from the stripped body: one quoted inside a fenced example is not
    # an anchor, and used to make a link to a nonexistent heading pass.
    found |= {slug(h) for h in HEADING_RE.findall(strip_code(body))}
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
            content = strip_code(f.read())
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
                resolved = in_suite(resolved)
            if not os.path.exists(resolved):
                missing.append((os.path.relpath(path, REPO_ROOT), target))
            elif frag and resolved.endswith('.md') and frag not in anchors_of(resolved):
                missing.append((os.path.relpath(path, REPO_ROOT),
                                f"{target}  (file exists; nothing named '{frag}' in it)"))

    hard = [f for f in missing if not is_drop(f[0])]
    soft = [f for f in missing if is_drop(f[0])]

    if soft:
        # NOTE: is the marker check-docs.py surfaces on an otherwise-green run.
        print(f"NOTE: {len(soft)} unresolved link(s) in gitignored inbox/ drops "
              f"-- warnings, not failures; the drain re-checks them as errors.")
        for src, target in soft:
            print(f"  (inbox) {src} -> {target}")
        print()

    if hard:
        print(f"Found {len(hard)} broken relative link(s):\n")
        for src, target in hard:
            print(f"  {src} -> {target}")
        return 1

    print("All relative links resolve (inbox/ drops excepted).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
