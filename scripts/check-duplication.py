#!/usr/bin/env python3
"""Report a claim that appears in two of a sub-project's own docs.

Advisory, never a gate. DOC-PROTOCOL.md §3 splits a sub-project into four files
by *when a reader needs it*, and DOC-COMPACTION.md §5's link-don't-restate rule
says a fact lives in exactly one of them. When it does not, the same sentence is
maintained in two places and only one of them gets corrected.

This is worth its own script because the recoverable bytes in this corpus turned
out not to be cold sentences. A 2026-09-04 pass measured 8-14% from §9's
hot/cold test on already-compacted decision files, and ~1.2 KB in one
sub-project from a single duplication: `embarch-umbrella/decisions/doctor.md`
re-argued which `doctor` checks are built, which `spec.md`'s own table already
said. `embarch-dev-bench/decisions/ble.md` closed with a paragraph its
`open.md` carried verbatim. Both are mechanical to find and neither is cold.

**A hit is not a defect.** A spec asserting an invariant a decision explains is
the four-file split working. What the report is for is the case where the two
copies are the same *claim* -- and then the question is which file owns it, per
§3, not which wording is better.

It compares every pair of docs inside one sub-project directory, plus
`suite/features.md` against each `spec.md`, since the inventory is meant to be a
pointer. Matching is on normalised word n-grams, so wording that drifted apart
still matches; the first 5 lines of each file are skipped, because the title,
status and navigation lines are duplicated by convention.

Usage:
  scripts/check-duplication.py                 every sub-project
  scripts/check-duplication.py embarch-api     one of them
  scripts/check-duplication.py --min-words 20  only long overlaps
Exit status: always 0. It reports; it decides nothing.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIN_WORDS = 12          # below this, shared phrasing is idiom rather than a claim
SKIP_LINES = 5          # title, blank, **Status:**, blank, the navigation line
CODE_FENCE = re.compile(r"^```", re.M)
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
NONWORD = re.compile(r"[^a-z0-9 ]+")


def words(path: Path) -> list[str]:
    """The doc as a normalised word list: no markup, no case, no punctuation."""
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")[SKIP_LINES:]
    out, fenced = [], False
    for line in lines:
        if CODE_FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        out.append(line)
    text = LINK.sub(r"\1", "\n".join(out)).lower()
    return NONWORD.sub(" ", text).split()


def runs(a: list[str], b: list[str], n: int) -> list[tuple[int, int, int]]:
    """Maximal (start_in_a, start_in_b, word_length) overlaps of >= n words.

    Matching n-grams that sit on the same diagonal (same b-a offset) and at
    consecutive positions are one overlap, so a shared paragraph is reported
    once rather than as every window inside it.
    """
    if len(a) < n or len(b) < n:
        return []
    pos_b: dict[tuple, list[int]] = defaultdict(list)
    for i in range(len(b) - n + 1):
        pos_b[tuple(b[i:i + n])].append(i)
    by_diag: dict[int, list[int]] = defaultdict(list)
    for i in range(len(a) - n + 1):
        for j in pos_b.get(tuple(a[i:i + n]), ()):
            by_diag[j - i].append(i)
    found = []
    for diag, starts in by_diag.items():
        starts.sort()
        first = prev = starts[0]
        for i in starts[1:] + [None]:
            if i is not None and i == prev + 1:
                prev = i
                continue
            found.append((first, first + diag, prev - first + n))
            if i is not None:
                first = prev = i
    return found


def groups(only: str | None):
    """(label, [paths]) per comparison set."""
    for d in sorted(REPO.glob("embarch-*")):
        if not d.is_dir() or (only and d.name != only):
            continue
        docs = sorted(p for p in d.rglob("*.md") if p.name != "README.md")
        if len(docs) > 1:
            yield d.name, docs
    features = REPO / "suite" / "features.md"
    if features.exists() and not only:
        specs = sorted(REPO.glob("embarch-*/spec.md"))
        if specs:
            yield "suite/features.md vs. each spec.md", [features] + specs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sub_project", nargs="?", help="limit to one embarch-* directory")
    ap.add_argument("--min-words", type=int, default=MIN_WORDS,
                    help="shortest overlap worth reporting (default %(default)s)")
    ap.add_argument("--top", type=int, default=8,
                    help="longest N overlaps per group (default %(default)s)")
    args = ap.parse_args()

    total = 0
    for label, paths in groups(args.sub_project):
        cache = {p: words(p) for p in paths}
        hits = []
        for i, pa in enumerate(paths):
            for pb in paths[i + 1:]:
                # features.md is only compared against a spec, never spec to spec.
                if label.startswith("suite/") and pa != paths[0]:
                    continue
                for sa, sb, ln in runs(cache[pa], cache[pb], args.min_words):
                    hits.append((ln, pa, pb, " ".join(cache[pa][sa:sa + ln])))
        if not hits:
            continue
        hits.sort(reverse=True, key=lambda h: h[0])
        print(f"\n## {label} — {len(hits)} overlap(s)")
        for ln, pa, pb, text in hits[:args.top]:
            ra = pa.relative_to(REPO)
            rb = pb.relative_to(REPO)
            print(f"\n  {ln} words  {ra}\n  {' ' * len(str(ln))}       {rb}")
            print(f"    {text[:300]}{'…' if len(text) > 300 else ''}")
        if len(hits) > args.top:
            print(f"\n  ...{len(hits) - args.top} shorter overlap(s) not shown.")
        total += len(hits)

    if not total:
        print(f"no overlap of {args.min_words}+ words between two docs of one "
              f"sub-project.")
        return 0
    print(f"\n{total} overlap(s). Advisory: a spec asserting an invariant a "
          f"decision explains\nis the four-file split working. Act only where "
          f"the two copies are one claim,\nand then DOC-PROTOCOL.md §3 says "
          f"which file owns it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
