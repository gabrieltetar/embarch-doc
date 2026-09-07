#!/usr/bin/env python3
"""Assemble changelog fragments into per-sub-project history files.

Every change that a reader would want to know about drops a fragment in
``changelog.d/`` named ``<scope>-<slug>.<category>.md`` holding **one line** of
reader-facing text. Nothing edits a shared history file directly, which is the
whole point: before 2026-09-02 this repo carried its history as a
``## Changelog`` section inside every doc, and those sections had grown to
642 KB -- 25% of the entire corpus -- against DOC-PROTOCOL.md's own rule that an
entry is "a one-line dated pointer". A section that lives inside the doc it
describes grows without anyone deciding to let it.

    changelog.d/core-rram-runner.changed.md
    changelog.d/ui-grouped-picker.added.md

    scripts/build_changelog.py --window 2026-09      # assemble
    scripts/build_changelog.py --check               # validate only
    scripts/build_changelog.py --only 'api-*'        # assemble just these

**`--only` exists because assembling everything is wrong inside a fold.** A
fold runs this script, and until 2026-09-06 it consumed every pending fragment
rather than the folding unit's -- so a leg swept 15 fragments the owner had
written and not yet folded into `history/` alongside its own one, in the same
`## window` block, with no way to stage its entry without staging his. That is
the legs 004/005 failure reached *without* `git add -A`: `fold-commit.py` stages
by explicit path, the path list was right, and the file at that path had been
rewritten underneath it by a script the fold is required to run. Nothing failed
-- `--check` validates fragment shape, not whether `history/` agrees with what
is pending, and the swept lines read exactly like the unit's own.

So a fold passes `--only '<scope>-*'`, or better the exact fragment names it is
staging, and everything else stays pending. Assembling the whole directory is
still the right default for a human folding deliberately.

Assembling groups each scope's fragments under a dated window heading in
``history/<scope>.md``, then deletes the consumed fragments. When a history file
passes CAP_BYTES its oldest windows roll into ``history/archive/``, so no file
in this repo ever stops being loadable.

Pure standard library.
"""
from __future__ import annotations

import argparse
import datetime
import fnmatch
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FRAGMENTS = REPO / "changelog.d"
HISTORY = REPO / "history"
ARCHIVE = HISTORY / "archive"

CATEGORIES = [
    ("added", "Added"),
    ("changed", "Changed"),
    ("fixed", "Fixed"),
    ("removed", "Removed"),
    ("decided", "Decided"),
]
CATEGORY_SLUGS = {slug for slug, _ in CATEGORIES}

# One line, and short enough that it stays a pointer rather than becoming the
# account. 200 B is about two sentences; the old sections averaged 1,100 B.
MAX_FRAGMENT_BYTES = 200
# No history file may exceed this; older windows roll to history/archive/.
CAP_BYTES = 20 * 1024

FRAGMENT_RE = re.compile(r"^(?P<scope>[a-z0-9]+(?:-[a-z0-9]+)*?)-(?P<slug>[a-z0-9-]+)\.(?P<cat>[a-z]+)\.md$")


def known_scopes() -> set[str]:
    """Sub-project dirs, plus two scopes that aren't directories."""
    scopes = {p.name.replace("embarch-", "") for p in REPO.iterdir()
              if p.is_dir() and p.name.startswith("embarch-")}
    return scopes | {"suite", "doc"}


def parse(path: Path, scopes: set[str]):
    """(scope, category, text) for a fragment, or a reason it is invalid."""
    m = FRAGMENT_RE.match(path.name)
    if not m:
        return None, f"name must be <scope>-<slug>.<category>.md"
    cat = m.group("cat")
    if cat not in CATEGORY_SLUGS:
        return None, f"unknown category '{cat}' (want {'/'.join(sorted(CATEGORY_SLUGS))})"
    # The scope is the longest known prefix, so 'dev-bench-foo' resolves to
    # 'dev-bench' and not to 'dev'.
    name = path.name[: -len(f".{cat}.md")]
    scope = next((s for s in sorted(scopes, key=len, reverse=True)
                  if name == s or name.startswith(s + "-")), None)
    if scope is None:
        return None, f"unknown scope in '{name}' (want one of {', '.join(sorted(scopes))})"
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return None, "empty"
    if "\n" in raw:
        return None, f"must be one line, got {raw.count(chr(10)) + 1}"
    if len(raw.encode()) > MAX_FRAGMENT_BYTES:
        return None, f"{len(raw.encode())} B, over the {MAX_FRAGMENT_BYTES} B limit"
    return (scope, cat, raw), None


def collect(scopes, only=None):
    """Validate every fragment before consuming any of them.

    `only` is a list of globs; a fragment matching none of them is left pending
    and is not validated either -- a malformed fragment belonging to somebody
    else must not fail this unit's fold, which is the same separation the glob
    exists to create.
    """
    good, bad = [], []
    for path in sorted(FRAGMENTS.glob("*.md")):
        if path.name == "README.md":
            continue
        if only and not any(fnmatch.fnmatch(path.name, g) for g in only):
            continue
        parsed, why = parse(path, scopes)
        (good.append((path, *parsed)) if parsed else bad.append((path, why)))
    for path in sorted(FRAGMENTS.rglob("*.md")):
        if path.parent != FRAGMENTS and not only:
            bad.append((path, "in a subdirectory; fragments must sit directly in changelog.d/"))
    return good, bad


WINDOW_RE = re.compile(r"^## (\S+)\s*$")
HEADING_TO_SLUG = {heading: slug for slug, heading in CATEGORIES}


def render_entries(by_cat: dict, window: str) -> str:
    """One window block, categories in CATEGORIES order, rows in the given order."""
    out = [f"## {window}", ""]
    for slug, heading in CATEGORIES:
        rows = by_cat.get(slug) or []
        if not rows:
            continue
        out.append(f"### {heading}")
        out += [f"- {r}" for r in rows]
        out.append("")
    return "\n".join(out)


def render(entries, window: str) -> str:
    by_cat: dict[str, list] = {}
    for cat, text in entries:
        by_cat.setdefault(cat, []).append(text)
    return render_entries({c: sorted(r) for c, r in by_cat.items()}, window)


def split_file(text: str):
    """(header, [(window|None, block_text), ...]) with blocks newest-first."""
    parts = re.split(r"(?m)^(?=## )", text)
    blocks = []
    for block in parts[1:]:
        first = block.splitlines()[0] if block.splitlines() else ""
        m = WINDOW_RE.match(first)
        blocks.append((m.group(1) if m else None, block))
    return parts[0], blocks


def parse_entries(block: str) -> dict:
    """{category slug: [row, ...]} from a rendered window block, in file order."""
    out: dict[str, list] = {}
    cur = None
    for line in block.splitlines():
        m = re.match(r"^### (.+?)\s*$", line)
        if m:
            cur = HEADING_TO_SLUG.get(m.group(1).strip())
            if cur:
                out.setdefault(cur, [])
            continue
        if cur and line.startswith("- "):
            out[cur].append(line[2:])
    return out


def merge_into(text: str, new_entries, window: str) -> str:
    """Fold `new_entries` into this file's `window` block, collapsing duplicates.

    Prepending a fresh block per run -- what this did until 2026-09-06 -- gave
    `history/api.md` 27 `## 2026-09` headings for 30 sections, one per fold,
    since the changelog split on 2026-09-02. No entry was lost or misfiled; what
    was wrong was the structure the file's own header promises, and the roll is
    sized in whole windows, so a per-fold window made the cap roll an arbitrary
    slice of a month rather than a month (`tasks/doc/021`).

    It also collapses same-window blocks it finds, so a file written by the old
    assembler heals on the next fold that touches it rather than needing a
    second repair pass. Order is preserved exactly: this run's entries first
    (sorted among themselves, as before), then each existing block's rows in
    file order, which is newest-first.
    """
    header, blocks = split_file(text)
    by_cat: dict[str, list] = {}
    fresh: dict[str, list] = {}
    for cat, row in new_entries:
        fresh.setdefault(cat, []).append(row)
    for cat, rows in fresh.items():
        by_cat.setdefault(cat, []).extend(sorted(rows))
    kept = []
    for win, block in blocks:
        if win == window:
            for cat, rows in parse_entries(block).items():
                by_cat.setdefault(cat, []).extend(rows)
        else:
            kept.append(block)
    return header.rstrip() + "\n\n" + render_entries(by_cat, window) + "".join(kept)


def roll_if_over_cap(path: Path, scope: str) -> str | None:
    """Move the oldest windows out until the file fits CAP_BYTES.

    **Never the newest window, even if the file is still over cap after.** The
    roll moves whole windows, so once windows are monthly rather than per-fold
    (`tasks/doc/021`) a single over-cap month is the *only* block -- and rolling
    it archives the entry the fold wrote seconds earlier and leaves the live
    file with a header and nothing else. Reproduced 2026-09-06 at 23,949 B:
    0 entries left. The old per-fold windows masked it, because there was always
    an older block to take instead; `history/doc.md` was at 50% of the cap when
    this was collapsed, so it was weeks away rather than hypothetical.

    A file that cannot fit without moving its newest window says so and stays
    over cap. That is a prompt to shorten entries or split the window, and it is
    strictly better than silently emptying the file nobody re-reads.
    """
    text = path.read_text(encoding="utf-8")
    if len(text.encode()) <= CAP_BYTES:
        return None
    head, *blocks = re.split(r"(?m)^(?=## )", text)
    moved = []
    while len(blocks) > 1 and len(("".join([head] + blocks)).encode()) > CAP_BYTES:
        moved.append(blocks.pop())          # oldest sits last: newest-first file
    if len(("".join([head] + blocks)).encode()) > CAP_BYTES:
        win = re.match(r"## (\S+)", blocks[0]).group(1) if blocks else "?"
        print(f"  history/{scope}.md is over the {CAP_BYTES // 1024} KB cap and its "
              f"newest window ({win}) is the only one left --\n"
              f"    not rolling it: that would archive what this fold just wrote. "
              f"Shorten entries or split the window.")
    if not moved:
        return None
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    windows = [re.match(r"## (\S+)", b).group(1) for b in moved if re.match(r"## (\S+)", b)]
    dest = ARCHIVE / f"{scope}-{windows[-1]}--{windows[0]}.md"
    dest.write_text(f"# {scope}: history {windows[-1]}..{windows[0]}\n\n"
                    f"**Status:** retired, {datetime.date.today()}. Rolled out of "
                    f"[../{scope}.md]({os.path.relpath(path, ARCHIVE)}) at the "
                    f"{CAP_BYTES // 1024} KB cap.\n\n" + "".join(reversed(moved)),
                    encoding="utf-8")
    path.write_text("".join([head] + blocks), encoding="utf-8")
    return str(dest.relative_to(REPO))


OLD_CAP_SENTENCE = (f"Capped at {CAP_BYTES // 1024} KB — older windows roll "
                    f"into [archive/](archive/).")
NEW_CAP_SENTENCE = (f"Capped at {CAP_BYTES // 1024} KB: over that, whole windows roll out of "
                    f"the end, oldest first, until it fits — [archive/](archive/).")


def entry_index(text: str) -> dict:
    """{category: [row, ...]} over the WHOLE file, in file order.

    The invariant a normalize pass must not break. Not global line order --
    collapsing blocks necessarily regroups lines by category, which is the
    point. What must not change is the count, and the order of rows *within* a
    category, since that is the newest-first reading order the file promises.
    """
    out: dict[str, list] = {}
    _, blocks = split_file(text)
    for _, block in blocks:
        for cat, rows in parse_entries(block).items():
            out.setdefault(cat, []).extend(rows)
    return out


def normalize(apply: bool) -> int:
    """Collapse duplicate window headings in every assembled history file.

    One pass, after the assembler stopped creating them. Refuses to write a file
    whose entries did not survive unchanged -- see `entry_index`.
    """
    files = sorted(HISTORY.glob("*.md"))
    if not files:
        print("no history files.")
        return 0
    changed, failed = 0, 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        header, blocks = split_file(text)
        windows = [w for w, _ in blocks]
        dupes = {w for w in windows if w and windows.count(w) > 1}
        header_stale = OLD_CAP_SENTENCE in header
        if not dupes and not header_stale:
            continue
        new = text
        for win in sorted(dupes):
            new = merge_into(new, [], win)
        if header_stale:
            head, rest = split_file(new)[0], "".join(b for _, b in split_file(new)[1])
            new = head.replace(OLD_CAP_SENTENCE, NEW_CAP_SENTENCE) + rest
        before, after = entry_index(text), entry_index(new)
        if before != after:
            lost = sum(len(v) for v in before.values()) - sum(len(v) for v in after.values())
            print(f"  REFUSED  {path.name}: entries changed "
                  f"({lost:+d} rows, or order moved within a category)")
            failed += 1
            continue
        n = len(windows) - len({w for w in windows})
        print(f"  {path.name}: {len(windows)} window heading(s) -> "
              f"{len(set(windows))}, {sum(len(v) for v in after.values())} entries intact"
              + ("" if apply else "   [dry run]"))
        if apply:
            path.write_text(new, encoding="utf-8")
        changed += 1
    if failed:
        print(f"\n{failed} file(s) refused; nothing written for those.")
        return 1
    print(f"\n{changed} file(s) "
          + ("normalized." if apply else "would change; pass --apply."))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", help="window heading, e.g. 2026-09 (default: this month)")
    ap.add_argument("--check", action="store_true", help="validate fragments, assemble nothing")
    ap.add_argument("--normalize", action="store_true",
                    help="collapse duplicate window headings in history/ (one-off repair)")
    ap.add_argument("--apply", action="store_true", help="with --normalize, write the files")
    ap.add_argument("--only", action="append", metavar="GLOB",
                    help="consume only fragments whose filename matches (repeatable). "
                         "A fold passes its own unit's; everything else stays pending.")
    args = ap.parse_args()

    if args.normalize:
        return normalize(args.apply)

    scopes = known_scopes()
    good, bad = collect(scopes, args.only)
    if bad:
        print(f"{len(bad)} invalid fragment(s); nothing assembled:\n")
        for path, why in bad:
            print(f"  {path.relative_to(REPO)} -- {why}")
        return 1
    if args.check:
        print(f"{len(good)} fragment(s) valid.")
        return 0
    if not good:
        print("No fragments to assemble."
              + (f" (--only matched none of {args.only})" if args.only else ""))
        return 0

    window = args.window or datetime.date.today().strftime("%Y-%m")
    HISTORY.mkdir(exist_ok=True)
    by_scope: dict[str, list] = {}
    for path, scope, cat, text in good:
        by_scope.setdefault(scope, []).append((cat, text))

    for scope, entries in sorted(by_scope.items()):
        path = HISTORY / f"{scope}.md"
        if path.exists():
            path.write_text(
                merge_into(path.read_text(encoding="utf-8"), entries, window),
                encoding="utf-8")
        else:
            block = render(entries, window)
            path.write_text(
                f"# {scope}: history\n\n**Status:** active, {datetime.date.today()}. "
                f"Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; "
                f"newest window first. Capped at {CAP_BYTES // 1024} KB: over that, whole "
                f"windows roll out of the end, oldest first, until it fits — "
                f"[archive/](archive/).\n\n" + block, encoding="utf-8")
        rolled = roll_if_over_cap(path, scope)
        print(f"  history/{scope}.md  += {len(entries)} entr{'y' if len(entries)==1 else 'ies'}"
              + (f"  (rolled {rolled})" if rolled else ""))

    for path, *_ in good:
        path.unlink()
    left = len([q for q in FRAGMENTS.glob("*.md") if q.name != "README.md"])
    print(f"\n{len(good)} fragment(s) consumed into window {window}."
          + (f" {left} left pending." if left else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
