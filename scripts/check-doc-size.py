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
capped from then on -- and gets no allowance thereafter.

The one exception, bounded and always printed: --update may RAISE a still-over-cap
file's baseline by up to RENAME_ALLOWANCE, because a cross-cutting rename grows
every doc that links to the renamed file by a few bytes each, and blocking that
would block changes that shrink the corpus enormously. Every migration pass lowers a baseline, and a file that
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
# An over-cap file may have its baseline RAISED by at most this much, and only
# through an explicit --update, which prints every raise. Cross-cutting renames
# (embarch-core/design.md -> decisions.md grew 15 pending-migration files by
# ~100 B each) would otherwise block a change that shrank the corpus by 190 KB.
# A file that has reached its cap gets no allowance at all: it is capped for good.
RENAME_ALLOWANCE = 1 * KB

# role -> (cap in bytes, matcher on the repo-relative path)
CAPS = [
    ("spec",        10 * KB, re.compile(r"^embarch-[a-z-]+/spec\.md$")),
    # A sub-project whose decisions outgrow one file splits them by mission into
    # decisions/<topic>.md, and decisions.md becomes the index (DOC-COMPACTION.md §3).
    ("decision-group", 12 * KB, re.compile(r"^embarch-[a-z-]+/decisions/[a-z-]+\.md$")),
    ("decisions",   25 * KB, re.compile(r"^embarch-[a-z-]+/decisions\.md$")),
    ("open",         5 * KB, re.compile(r"^embarch-[a-z-]+/open\.md$")),
    # An interface reference that outgrows one file splits the same way decisions do.
    ("interface-group", 12 * KB, re.compile(r"^embarch-[a-z-]+/interfaces/[a-z-]+\.md$")),
    ("interfaces",  15 * KB, re.compile(r"^embarch-[a-z-]+/interfaces\.md$")),
    ("suite-guide", 25 * KB, re.compile(r"^suite/(user|studies)-guide\.md$")),
    # A complete inventory table gets the interfaces cap, for the interfaces
    # reason: every row must be present, and the budget is spent on rows.
    ("suite-inventory", 15 * KB, re.compile(r"^suite/(features|roadmap)\.md$")),
    ("suite",       10 * KB, re.compile(r"^suite/[a-z-]+\.md$")),
    ("protocol",    12 * KB, re.compile(r"^DOC-(PROTOCOL|COMPACTION)\.md$")),
    ("history",     20 * KB, re.compile(r"^history/[a-z-]+\.md$")),
    # The reversals page split the way any over-cap doc does: an index plus stable
    # numeric ranges (DOC-COMPACTION.md §3). A range never re-splits an existing row.
    ("reversal-group", 20 * KB, re.compile(r"^reversals/rows-\d+-\d+\.md$")),
    # A proposal keeps only what is still proposed: an accepted half belongs in the
    # living docs, and restating it here makes a second source of truth.
    ("proposal",    15 * KB, re.compile(r"^embarch-[a-z-]+-proposal\.md$")),
    ("reversals",   10 * KB, re.compile(r"^embarch-decision-reversals\.md$")),
    # Anything else still under a sub-project or the root is legacy, and the
    # migration's job is to turn it into one of the roles above.
    ("legacy",      25 * KB, re.compile(r"^(embarch-[a-z-]+/|embarch-|DOC-|README)")),
]
EXEMPT = re.compile(r"(^\.|/\.|^history/archive/|changelog\.d/|^CLAUDE\.md$|^LICENSE$)")


# A sub-project whose decisions have been reduced to their hot half
# (DOC-COMPACTION.md §9) is held at a tighter cap than one that has not, so a
# finished migration cannot drift back. Default caps above apply to the rest;
# add a sub-project here the moment its pass lands, never before.
TIGHTENED = {
    "embarch-outpost": {"decision-group": 8 * KB},
}


def role_and_cap(rel: str):
    for role, cap, pat in CAPS:
        if pat.search(rel):
            sub = rel.split("/")[0]
            return role, TIGHTENED.get(sub, {}).get(role, cap)
    return None, None


def docs():
    for p in sorted(REPO.rglob("*.md")):
        rel = str(p.relative_to(REPO))
        if EXEMPT.search(rel) or ".git" in p.parts:
            continue
        yield rel, p.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="record progress: lower baselines that shrank")
    ap.add_argument("--adopt", action="store_true",
                    help="pin files that are newly over cap (bootstrap only; --update refuses to)")
    ap.add_argument("--report", action="store_true", help="print the whole corpus")
    ap.add_argument("--pressure", action="store_true",
                    help="list files within --pressure-pct of their effective limit")
    ap.add_argument("--pressure-pct", type=float, default=95.0,
                    help="what counts as pressure (default 95%% of min(cap, baseline))")
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

    if args.pressure:
        # A cap is a hard wall a worker meets only when it tries to write, so a
        # task that cannot be done without exceeding one is a compaction task
        # wearing a feature task's clothes -- and the supervisor finds that out
        # when the worker reports, not when it dispatches. This makes the wall
        # visible one step earlier.
        #
        # It reports rather than files: DOC-COMPACTION.md §8 warns against
        # compacting a subsystem still in flux, and nothing here can tell. The
        # caller decides.
        near = []
        for rel, size in docs():
            role, cap = role_and_cap(rel)
            if cap is None:
                continue
            limit = min(cap, base[rel]) if rel in base else cap
            pct = 100.0 * size / limit
            if pct >= args.pressure_pct:
                near.append((pct, rel, role, size, limit))
        near.sort(reverse=True)
        if not near:
            print(f"no file is within {100 - args.pressure_pct:g}% of its limit.")
            return 0
        print(f"{len(near)} file(s) at or above {args.pressure_pct:g}% of "
              f"min(cap, baseline):\n")
        for pct, rel, role, size, limit in near:
            print(f"  {pct:5.1f}%  {rel}  ({role}) {size}/{limit} B, "
                  f"{limit - size} B left")
        print("\nA task that must write one of these cannot be done without a\n"
              "compaction pass first (DOC-COMPACTION.md §9). Say so in the task\n"
              "file before dispatching it, and record §7's human question in the\n"
              "log -- 'can spec.md alone answer what someone needs to work on this\n"
              "component today' is not a thing a script can answer.")
        return 1

    if args.update or args.adopt:
        raised, adopted_refused = [], []
        for rel, _, size in shrunk:
            base[rel] = size
        for rel in capped:
            base.pop(rel, None)
        # A baseline entry for a file that no longer exists is dead weight that
        # makes the ratchet report "N still over cap, holding 0 KB". Deleting or
        # renaming an over-cap file is the whole point of a migration, so prune.
        present = {rel for rel, _ in docs()}
        gone = sorted(set(base) - present)
        for rel in gone:
            base.pop(rel)
        for rel, size in docs():
            role, cap = role_and_cap(rel)
            if not cap or size <= cap:
                continue
            if rel not in base:
                # Newly over cap. --update records progress and must never
                # absorb a regression, so pinning takes an explicit --adopt.
                if args.adopt:
                    base[rel] = size
                else:
                    adopted_refused.append((rel, size, cap))
            elif base[rel] < size <= base[rel] + RENAME_ALLOWANCE:
                raised.append((rel, base[rel], size))
                base[rel] = size
        print(f"baseline updated: {len(base)} file(s) still over cap")
        for rel, was, now in shrunk:
            print(f"  ratcheted {rel}: {was/KB:.0f}K -> {now/KB:.0f}K")
        for rel in capped:
            print(f"  AT CAP, baseline dropped: {rel}")
        for rel in gone:
            print(f"  GONE, baseline pruned: {rel}")
        for rel, was, now in raised:
            print(f"  RAISED (within the {RENAME_ALLOWANCE} B rename allowance) "
                  f"{rel}: {was} -> {now} B")
        BASELINE.write_text(json.dumps(dict(sorted(base.items())), indent=2) + "\n")
        if adopted_refused:
            print(f"\n{len(adopted_refused)} file(s) newly over cap, NOT pinned "
                  f"(--update records progress, never a regression):")
            for rel, size, cap in adopted_refused:
                print(f"  {rel}  {size/KB:.1f}K > {cap/KB:.0f}K cap")
            print("Shrink them, or pass --adopt if this is a deliberate bootstrap.")
            return 1
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
        # Last line must read as a failure on its own. A neutral footer here was
        # misread as a pass three times in one session when only the tail was
        # checked -- and the commits went out over-cap.
        print(f"FAIL: {len(fails)} file(s) over their limit.")
        return 1

    print(f"All {sum(1 for _ in docs())} docs within their limit. "
          f"Corpus {total/KB:.0f} KB; {len(base)} still over cap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
