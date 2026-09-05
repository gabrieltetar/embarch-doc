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

The cap is a wall, and a wall is discovered by the worker whose edit it
refuses -- which converts unrelated work into a compaction task mid-flight. So
above the cap there is a RESERVE: the last RESERVE_PCT..100% of a file's limit.
A file in reserve is still writable, and the gate still passes, but it must be
named by an open item in ``tasks/`` or ``inbox/``. **The debt is filed by
whoever spends the reserve**, in the same commit, because that actor is the only
one who knows the thing no script can decide -- whether the subsystem is still
in flux (DOC-COMPACTION.md §8), which is when compaction writes a clean
statement of something about to be wrong. A parked item naming what unparks it
is a legitimate resting state; an unfiled file in reserve is not.

Usage:
  scripts/check-doc-size.py              check (CI): caps, the ratchet, and the reserve
  scripts/check-doc-size.py --update     re-baseline anything now smaller
  scripts/check-doc-size.py --report     show the whole corpus against caps
  scripts/check-doc-size.py --pressure   what is in reserve, filed and unfiled
Exit status: 0 if nothing exceeds min(cap, baseline) and every file in reserve
is filed against, 1 otherwise.
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

# A file at or above this fraction of its effective limit is *in reserve*: it
# may still be written, and the gate still passes, but the debt must be filed.
# 90% of a 12 KB decision group is ~1.2 KB and of a 5 KB open.md is ~512 B --
# roughly one cycle of runway, deliberately not more. It buys the crossing being
# recorded and judged, not a steady state; the corpus still grows.
RESERVE_PCT = 90.0

# Where a filed debt lives. `tasks/doc/` for a doc the fleet may write,
# `inbox/` for one reserved to the owner -- DOC-PROTOCOL.md and DOC-COMPACTION.md
# are the case that forced this: no agent can compact them, so a wall there can
# only ever be taken down in the owner's own session, and nothing said so.
DEBT_DIRS = ("tasks", "inbox")
DONE_STATE = re.compile(r"^\*\*State:\*\*\s*done\b", re.M)
# A debt is DECLARED, never inferred from a path appearing somewhere in an item.
# Matching on a mention made five of today's twelve read as filed by tasks that
# merely cite the doc they are about to edit -- which is every task.
COMPACTS = re.compile(r"^\*\*Compacts:\*\*[ \t]*(.+)$", re.M)

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
    ("suite-inventory", 15 * KB, re.compile(r"^suite/roadmap\.md$")),
    # features.md is assembled from features.d/, so the budget that bites is the
    # per-row one build_features.py enforces (600 B) -- the file's size is a
    # function of how many capabilities the suite has, which is not anyone's
    # discipline to exercise. This cap is a backstop, not the constraint.
    ("suite-assembled", 20 * KB, re.compile(r"^suite/features\.md$")),
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
EXEMPT = re.compile(r"(^\.|/\.|^history/archive/|changelog\.d/|features\.d/"
                    r"|^CLAUDE\.md$|^LICENSE$)")


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


def open_debt_items():
    """Every queue item not marked done, as (repo-relative path, text).

    A `done` item is about to be deleted by the fold, so it cannot carry a
    debt forward. Everything else counts, `blocked` and parked included --
    a parked compaction task is the mechanism working, not a gap in it.
    """
    for d in DEBT_DIRS:
        root = REPO / d
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*.md")):
            if p.name == "README.md":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            if DONE_STATE.search(text):
                continue
            paths = set()
            for m in COMPACTS.finditer(text):
                paths.update(t.strip().strip("`,") for t in m.group(1).split(","))
            if paths:
                yield str(p.relative_to(REPO)), {q for q in paths if q}


def reserve_state(base, reserve_pct):
    """(in_reserve, filed_but_clear) -- both as (rel, size, limit, [items]).

    A file over its limit is a hard failure elsewhere and is not reported here
    twice. `filed_but_clear` is a debt named by an item that a later pass has
    already paid: worth closing, never worth failing on.
    """
    items = list(open_debt_items())
    in_reserve, filed_clear = [], []
    for rel, size in docs():
        role, cap = role_and_cap(rel)
        if cap is None:
            continue
        limit = min(cap, base[rel]) if rel in base else cap
        if size > limit:
            continue
        filed = [i for i, paths in items if rel in paths]
        if 100.0 * size / limit >= reserve_pct:
            in_reserve.append((rel, size, limit, filed))
        elif filed:
            filed_clear.append((rel, size, limit, filed))
    return in_reserve, filed_clear


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
                    help="list what is in reserve, filed and unfiled")
    ap.add_argument("--reserve-pct", type=float, default=RESERVE_PCT,
                    help="what counts as reserve (default %(default)g%% of min(cap, baseline))")
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
        # This reports rather than files, and that is the whole point:
        # DOC-COMPACTION.md §8 warns against compacting a subsystem still in
        # flux and nothing here can tell, so the actor who spends the reserve
        # writes the item and answers that question in it.
        in_reserve, filed_clear = reserve_state(base, args.reserve_pct)
        if not in_reserve and not filed_clear:
            print(f"nothing is in reserve (the last "
                  f"{100 - args.reserve_pct:g}% of any file's limit).")
            return 0
        unfiled = [r for r in in_reserve if not r[3]]
        for rel, size, limit, filed in sorted(
                in_reserve, key=lambda r: -r[1] / r[2]):
            mark = "UNFILED" if not filed else "filed   "
            print(f"  {mark} {100.0 * size / limit:5.1f}%  {rel}  "
                  f"{size}/{limit} B, {limit - size} B left")
            for i in filed:
                print(f"           -> {i}")
        for rel, size, limit, filed in filed_clear:
            print(f"  PAID     {100.0 * size / limit:5.1f}%  {rel} is out of "
                  f"reserve; close its item")
            for i in filed:
                print(f"           -> {i}")
        if unfiled:
            print(f"\n{len(unfiled)} file(s) in reserve with nothing filed. "
                  f"One item may name several\nfiles of one sub-project; a "
                  f"compaction pass is a sub-project act.")
            return 1
        print(f"\n{len(in_reserve)} file(s) in reserve, every one filed against.")
        return 0

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

    in_reserve, _ = reserve_state(base, args.reserve_pct)
    unfiled = [r for r in in_reserve if not r[3]]
    if unfiled:
        print(f"{len(unfiled)} file(s) in reserve with no debt filed:\n")
        for rel, size, limit, _ in sorted(unfiled, key=lambda r: -r[1] / r[2]):
            print(f"  {100.0 * size / limit:5.1f}%  {rel}  {size}/{limit} B, "
                  f"{limit - size} B left")
        print("\nThe reserve is writable and this is not a wall -- it is the debt\n"
              "going unrecorded. File one task per sub-project as\n"
              "tasks/doc/<NNN>-compact-<scope>.md, listing these paths on a\n"
              "**Compacts:** line, in the same commit that spent the reserve. The\n"
              "task carries the judgements no script can make: **In flux:**\n"
              "(DOC-COMPACTION.md \u00a78), \u00a77's question, and what the pass\n"
              "may not delete. tasks/README.md has the shape.")
        print(f"FAIL: {len(unfiled)} file(s) in reserve with no debt filed.")
        return 1

    print(f"All {sum(1 for _ in docs())} docs within their limit; "
          f"{len(in_reserve)} in reserve, all filed. "
          f"Corpus {total/KB:.0f} KB; {len(base)} still over cap.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
