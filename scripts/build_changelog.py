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

Assembling groups each scope's fragments under a dated window heading in
``history/<scope>.md``, then deletes the consumed fragments. When a history file
passes CAP_BYTES its oldest windows roll into ``history/archive/``, so no file
in this repo ever stops being loadable.

Pure standard library.
"""
from __future__ import annotations

import argparse
import datetime
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


def collect(scopes):
    """Validate every fragment before consuming any of them."""
    good, bad = [], []
    for path in sorted(FRAGMENTS.glob("*.md")):
        if path.name == "README.md":
            continue
        parsed, why = parse(path, scopes)
        (good.append((path, *parsed)) if parsed else bad.append((path, why)))
    for path in sorted(FRAGMENTS.rglob("*.md")):
        if path.parent != FRAGMENTS:
            bad.append((path, "in a subdirectory; fragments must sit directly in changelog.d/"))
    return good, bad


def render(entries, window: str) -> str:
    out = [f"## {window}", ""]
    for slug, heading in CATEGORIES:
        rows = [t for c, t in entries if c == slug]
        if not rows:
            continue
        out.append(f"### {heading}")
        out += [f"- {r}" for r in sorted(rows)]
        out.append("")
    return "\n".join(out)


def roll_if_over_cap(path: Path, scope: str) -> str | None:
    """Move the oldest windows out until the file fits CAP_BYTES."""
    text = path.read_text(encoding="utf-8")
    if len(text.encode()) <= CAP_BYTES:
        return None
    head, *blocks = re.split(r"(?m)^(?=## )", text)
    moved = []
    while blocks and len(("".join([head] + blocks)).encode()) > CAP_BYTES:
        moved.append(blocks.pop())          # oldest sits last: newest-first file
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", help="window heading, e.g. 2026-09 (default: this month)")
    ap.add_argument("--check", action="store_true", help="validate fragments, assemble nothing")
    args = ap.parse_args()

    scopes = known_scopes()
    good, bad = collect(scopes)
    if bad:
        print(f"{len(bad)} invalid fragment(s); nothing assembled:\n")
        for path, why in bad:
            print(f"  {path.relative_to(REPO)} -- {why}")
        return 1
    if args.check:
        print(f"{len(good)} fragment(s) valid.")
        return 0
    if not good:
        print("No fragments to assemble.")
        return 0

    window = args.window or datetime.date.today().strftime("%Y-%m")
    HISTORY.mkdir(exist_ok=True)
    by_scope: dict[str, list] = {}
    for path, scope, cat, text in good:
        by_scope.setdefault(scope, []).append((cat, text))

    for scope, entries in sorted(by_scope.items()):
        path = HISTORY / f"{scope}.md"
        block = render(entries, window)
        if path.exists():
            text = path.read_text(encoding="utf-8")
            head, sep, rest = text.partition("\n## ")
            path.write_text(head.rstrip() + "\n\n" + block + (("## " + rest) if sep else ""),
                            encoding="utf-8")
        else:
            path.write_text(
                f"# {scope}: history\n\n**Status:** active, {datetime.date.today()}. "
                f"Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; "
                f"newest window first. Capped at {CAP_BYTES // 1024} KB — older windows roll "
                f"into [archive/](archive/).\n\n" + block, encoding="utf-8")
        rolled = roll_if_over_cap(path, scope)
        print(f"  history/{scope}.md  += {len(entries)} entr{'y' if len(entries)==1 else 'ies'}"
              + (f"  (rolled {rolled})" if rolled else ""))

    for path, *_ in good:
        path.unlink()
    print(f"\n{len(good)} fragment(s) consumed into window {window}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
