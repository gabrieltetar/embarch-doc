#!/usr/bin/env python3
"""Assemble the suite feature inventory from one fragment per row.

``suite/features.md`` is an inventory of a suite under active development, so a
row lands about as often as a task does. That made it the one doc with no quiet
state: DOC-COMPACTION.md §8 says do not compact a subsystem in flux, and this
one is in flux permanently, so "wait for the flux to pass" was never an
available answer. Measured 2026-09-04, it gained ~200 B per four-unit leg
against 939 B of headroom -- four legs from its cap, with no compaction pass
able to help, because §2 gives it the interfaces cap for the interfaces reason:
every row must be present and the budget is spent on rows.

So it stops being a file anyone edits. Each row is a fragment:

    features.d/<scope>-<NNN>-<slug>.md      one markdown table row, one line

and this assembles them into ``suite/features.md``. The same shape as
``changelog.d/`` -> ``history/`` (see changelog.d/README.md), for the same
reason and with one extra dividend: **a worker can write its own row.**
``suite/features.md`` is outside every worker's ownership row
(embarch-fleet/protocol.md §3), so until now a worker that shipped a feature
dropped a ``status.d/`` fragment and the supervisor hand-folded it into the
table. ``features.d/<its own scope>-*`` is the worker's to write, so the row
lands with the work that earned it.

    scripts/build_features.py            assemble
    scripts/build_features.py --check    verify the file matches the fragments
Exit status: 0 on success; 1 if --check finds a difference or a fragment is
malformed.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FRAGMENTS = REPO / "features.d"
TARGET = REPO / "suite" / "features.md"
HEADER = FRAGMENTS / "HEADER.md"

# One line, four cells. Longer than changelog.d's 200 B because a Status cell
# carries its caveat -- "Shipped -- the verification compared a byte count and
# reported landed through a cancelled elevation" is the row's whole value.
MAX_BYTES = 600
COLUMNS = ("Feature", "Status", "Verified", "Decision")

# Ordered, because the assembled file reads top to bottom and the order is
# editorial: the implemented sub-projects first, then the ones with no repo.
# A section with no fragments is omitted rather than emitted empty.
SECTIONS = [
    ("core", "embarch-core"),
    ("api", "embarch-api"),
    ("dev-bench", "embarch-dev-bench"),
    ("study-designer", "embarch-study-designer"),
    ("outpost", "embarch-outpost"),
    ("topology", "embarch-topology"),
    ("umbrella", "embarch-umbrella"),
    ("ui", "embarch-ui"),
    ("not-yet", "Not yet a sub-project"),
]
SCOPES = [k for k, _ in SECTIONS]
NAME_RE = re.compile(r"^(?P<scope>[a-z-]+)-(?P<order>\d{3})-(?P<slug>[a-z0-9-]+)\.md$")


def fragment_scope(stem: str) -> str | None:
    """Longest matching scope, so `dev-bench-010-x` is not read as `dev`."""
    for s in sorted(SCOPES, key=len, reverse=True):
        if stem.startswith(s + "-"):
            return s
    return None


def read_fragments() -> tuple[dict[str, list[tuple[int, str, str]]], list[str]]:
    rows: dict[str, list[tuple[int, str, str]]] = {k: [] for k in SCOPES}
    problems: list[str] = []
    if not FRAGMENTS.is_dir():
        return rows, [f"{FRAGMENTS.relative_to(REPO)}/ does not exist"]
    for p in sorted(FRAGMENTS.glob("*.md")):
        if p.name in ("README.md", "HEADER.md"):
            continue
        rel = f"features.d/{p.name}"
        m = NAME_RE.match(p.name)
        scope = fragment_scope(p.stem) if m else None
        if not m or scope is None:
            problems.append(f"{rel}: name must be <scope>-<NNN>-<slug>.md, "
                            f"scope one of {', '.join(SCOPES)}")
            continue
        raw = p.read_text(encoding="utf-8")
        if len(raw.encode()) > MAX_BYTES:
            problems.append(f"{rel}: {len(raw.encode())} B over the {MAX_BYTES} B limit")
        line = raw.strip("\n")
        if "\n" in line:
            problems.append(f"{rel}: {line.count(chr(10)) + 1} lines; a row is one line")
            continue
        cells = line.strip().strip("|").split("|")
        if not line.strip().startswith("|") or len(cells) != len(COLUMNS):
            problems.append(f"{rel}: want {len(COLUMNS)} cells "
                            f"(| {' | '.join(COLUMNS)} |), got {len(cells)}")
            continue
        rows[scope].append((int(m.group("order")), p.name, line.strip()))
    for k in rows:
        rows[k].sort()
    dupes = [(k, o) for k, v in rows.items()
             for o in {x[0] for x in v} if [x[0] for x in v].count(o) > 1]
    for k, o in sorted(set(dupes)):
        problems.append(f"features.d/{k}-{o:03d}-*: two fragments share an order number")
    return rows, problems


def assemble(rows: dict[str, list[tuple[int, str, str]]]) -> str:
    if not HEADER.exists():
        raise SystemExit(f"missing {HEADER.relative_to(REPO)}: it carries the title, "
                         f"the **Status:** line and the prose above the first section")
    out = [HEADER.read_text(encoding="utf-8").rstrip("\n"), ""]
    for key, heading in SECTIONS:
        if not rows[key]:
            continue
        out += [f"## {heading}", "",
                "| " + " | ".join(COLUMNS) + " |",
                "|" + "---|" * len(COLUMNS)]
        out += [r[2] for r in rows[key]]
        out.append("")
    return "\n".join(out).rstrip("\n") + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify suite/features.md matches the fragments; write nothing")
    args = ap.parse_args()

    rows, problems = read_fragments()
    if problems:
        print(f"{len(problems)} malformed fragment(s):\n")
        for p in problems:
            print(f"  {p}")
        print(f"\nA row is one markdown table row: | {' | '.join(COLUMNS)} |\n"
              "See features.d/README.md.")
        return 1

    built = assemble(rows)
    total = sum(len(v) for v in rows.values())

    if args.check:
        current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else ""
        if current == built:
            print(f"OK: suite/features.md matches its {total} fragment(s).")
            return 0
        print("suite/features.md does not match features.d/.\n\n"
              "It is assembled, not edited: change the fragment, or add one, and\n"
              "run scripts/build_features.py. A hand-edit here is reverted by the\n"
              "next assemble, silently, which is the failure this replaces.")
        cur, new = current.split("\n"), built.split("\n")
        import difflib
        for line in list(difflib.unified_diff(cur, new, "on disk", "from fragments",
                                              lineterm="", n=0))[:24]:
            print(f"  {line}")
        return 1

    TARGET.write_text(built, encoding="utf-8")
    print(f"suite/features.md  {len(built.encode())} B  {total} row(s) from "
          f"{sum(1 for v in rows.values() if v)} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
