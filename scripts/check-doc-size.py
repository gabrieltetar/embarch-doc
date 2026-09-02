#!/usr/bin/env python3
"""Enforce per-file size caps, as a ratchet that can only tighten.

DOC-COMPACTION.md §2 gives every doc a cap by role -- a spec is 10 KB, a
decisions file 25 KB, an open-questions file 5 KB -- because a doc nobody can
load whole is a doc nobody reads. On 2026-09-02 the corpus was 2.66 MB with
single files at 311 KB, so the caps cannot be enforced outright without failing
every build until the migration finishes.

So this is a ratchet. ``doc-size-baseline.json`` records each over-cap file's size at
the moment it was measured, and that number only ever moves down. A file with a
baseline may grow no larger than it already is; a file without one must sit
under its role's cap. Reaching the cap retires the baseline entry, so the file is
capped from then on. Every migration pass lowers a baseline, and a file that
reaches its cap loses its baseline entry and is capped for good.

Usage:
  scripts/check-doc-size.py              check (CI)
  scripts/check-doc-size.py --update     re-baseline anything now smaller
  scripts/check-doc-size.py --report     show the whole corpus against caps
Exit status: 0 if nothing exceeds min(cap, baseline), 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASELINE = REPO / "scripts" / "doc-size-baseline.json"
KB = 1024

# role -> (cap in bytes, matcher on the repo-relative path)
CAPS = [
    ("spec",        10 * KB, re.compile(r"^embarch-[a-z-]+/spec\.md$")),
    ("decisions",   25 * KB, re.compile(r"^embarch-[a-z-]+/decisions\.md$")),
    ("open",         5 * KB, re.compile(r"^embarch-[a-z-]+/open\.md$")),
    ("interfaces",  15 * KB, re.compile(r"^embarch-[a-z-]+/interfaces\.md$")),
    ("suite-guide", 25 * KB, re.compile(r"^suite/user-guide\.md$")),
    ("suite",       10 * KB, re.compile(r"^suite/[a-z-]+\.md$")),
    ("protocol",    12 * KB, re.compile(r"^DOC-(PROTOCOL|COMPACTION)\.md$")),
    ("history",     20 * KB, re.compile(r"^history/[a-z-]+\.md$")),
    ("reversals",   25 * KB, re.compile(r"^embarch-decision-reversals\.md$")),
    # Anything else still under a sub-project or the root is legacy, and the
    # migration's job is to turn it into one of the roles above.
    ("legacy",      25 * KB, re.compile(r"^(embarch-[a-z-]+/|embarch-|DOC-|README)")),
]
EXEMPT = re.compile(r"(^\.|/\.|^history/archive/|changelog\.d/|^CLAUDE\.md$|^LICENSE$)")


def role_and_cap(rel: str):
    for role, cap, pat in CAPS:
        if pat.search(rel):
            return role, cap
    return None, None


def docs():
    for p in sorted(REPO.rglob("*.md")):
        rel = str(p.relative_to(REPO))
        if EXEMPT.search(rel) or ".git" in p.parts:
            continue
        yield rel, p.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="lower baselines that have shrunk")
    ap.add_argument("--report", action="store_true", help="print the whole corpus")
    args = ap.parse_args()

    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    fails, shrunk, capped, total = [], [], [], 0

    for rel, size in docs():
        role, cap = role_and_cap(rel)
        total += size
        if cap is None:
            continue
        # A file with a baseline is over cap and is allowed up to that
        # baseline, which only ever moves down. A file without one is capped.
        if rel in base:
            limit = base[rel]
            if size < base[rel]:
                shrunk.append((rel, base[rel], size))
            if size <= cap:
                capped.append(rel)      # reached its cap; baseline retires
        else:
            limit = cap
        if size > limit:
            fails.append((rel, role, size, limit, cap))

    if args.update:
        for rel, _, size in shrunk:
            base[rel] = size
        for rel in capped:
            base.pop(rel, None)
        for rel, size in docs():
            role, cap = role_and_cap(rel)
            if cap and size > cap and rel not in base:
                base[rel] = size
        BASELINE.write_text(json.dumps(dict(sorted(base.items())), indent=2) + "\n")
        print(f"baseline updated: {len(base)} file(s) still over cap")
        for rel, was, now in shrunk:
            print(f"  ratcheted {rel}: {was/KB:.0f}K -> {now/KB:.0f}K")
        for rel in capped:
            print(f"  AT CAP, baseline dropped: {rel}")
        return 0

    if args.report:
        print(f"{'file':50s} {'size':>8s} {'cap':>7s} {'baseline':>9s}  role")
        for rel, size in docs():
            role, cap = role_and_cap(rel)
            if cap is None:
                continue
            b = base.get(rel)
            mark = "  OVER" if size > (b or cap) else ""
            print(f"{rel:50s} {size/KB:7.1f}K {cap/KB:6.0f}K "
                  f"{(f'{b/KB:8.1f}K' if b else '        -')}  {role}{mark}")
        over = sum(s for r, s in docs() if (c := role_and_cap(r)[1]) and s > c)
        print(f"\ncorpus {total/KB:.0f} KB; {len(base)} file(s) over cap, "
              f"holding {over/KB:.0f} KB")
        return 0

    if fails:
        print(f"{len(fails)} file(s) over their limit:\n")
        for rel, role, size, limit, cap in fails:
            why = "cap" if limit == cap else "ratchet baseline"
            print(f"  {rel}  {size/KB:.1f}K > {limit/KB:.1f}K ({why}; {role} cap is {cap/KB:.0f}K)")
        print("\nA file may shrink freely. To record progress: scripts/check-doc-size.py --update")
        return 1

    print(f"All {sum(1 for _ in docs())} docs within their limit. "
          f"Corpus {total/KB:.0f} KB; {len(base)} still over cap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
