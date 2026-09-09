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
in flux (DOC-COMPACTION-PASS.md, "Failure modes"), which is when compaction writes a clean
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
import datetime
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

# THE RATCHET MOVES IN STEPS, not to the exact byte. A baseline pinned to a
# file's exact size means "no correct edit may ever be made here without an
# equal deletion in the same commit" -- a hard stop wearing a gradient's
# clothes. Measured 2026-09-07: `ops.md` at 29,701/29,701 and `protocol.md` at
# 32,466/32,466, both at ZERO headroom, which is how one new rule cost four
# squeeze passes.
#
# So a shrink records the next step boundary ABOVE the new size, and the
# baseline is still `min(old, that)` -- monotonically decreasing, never a raise.
# A file that shrinks from 32,466 to 29,701 lands on 30,720 and has earned
# 1,019 B of real room; it can never grow back toward 32 K. A file already
# pinned tight from an older exact-pin update stays tight until someone shrinks
# it, and then it gets a boundary. Shrinking always buys room at a boundary,
# and never buys room you did not earn.
RATCHET_STEP = 1 * KB

# A file may exceed its limit by up to this much WITHOUT failing the gate, if
# and only if the overrun is recorded as a debt carrying a due date that has
# not passed (see `DUE`). One amendment's grace, on a clock, once.
#
# This is the ledger, and it exists because refusing a correct edit at the wall
# is the expensive failure. Measured across 2026-09-06/07: three units spent
# their reserve shaving Status-column rows to clear fourteen bytes; one
# supervisor filed a decision in the WRONG FILE because the right one had 96
# bytes left -- "a cap that misfiles is worse than a cap that refuses"; and a
# task parked on `In flux: yes` sat at 22 bytes of headroom with the argument
# that unparked it written inside it.
#
# The grace is bounded twice over so it cannot become a renewable licence: by
# this many bytes, and by the due date. Past either, the gate fails.
OVERRUN_ALLOWANCE = 2 * KB

# How long a debt has. A leg is four units and ~40 minutes; a busy day is 15 to
# 47 units. Seven days is long enough that nothing thrashes and short enough
# that a park cannot outlive it -- which is the point, since `blocked` was an
# absorbing state: 13 of 28 reserve debts were filed only against a blocked
# task, invisible to every leg.
DUE_DAYS = 7

# A file at or above this fraction of its effective limit is *in reserve*: it
# may still be written, and the gate still passes, but the debt must be filed.
# 90% of a 12 KB decision group is ~1.2 KB and of a 5 KB open.md is ~512 B --
# roughly one cycle of runway, deliberately not more. It buys the crossing being
# recorded and judged, not a steady state; the corpus still grows.
RESERVE_PCT = 90.0

# ...but a percentage of a small cap is not runway. 90% of a 5 KB `open.md` is
# 512 B and of a 12 KB decision group 1.2 KB, and the corpus reached states no
# percentage would have called dangerous: `suite/features.md` with **36 bytes**
# left, `embarch-api/decisions/core-link.md` with **22**. A worker dispatched at
# either cannot write the sentence its task exists to add, and three legs in a
# row spent a unit shaving bytes to clear fourteen.
#
# So reserve is `max(RESERVE_FLOOR, (100 - RESERVE_PCT)% of the limit)` from the
# top. The floor is one decision amendment's worth of prose, measured against
# what this suite's amendments actually cost: the 2026-09-06 fold records single
# additions of 350 B, ~940 B and 1,548 B. 1.2 KB covers the middle of that and
# is honest about not covering the top.
#
# **It files debts EARLIER, not later, and that is the point.** A file warned
# 1.2 KB out can still be split; a file warned 22 bytes out can only be
# squeezed, and squeezing is how live reasoning gets deleted to make room for
# new reasoning. DOC-COMPACTION.md §2 carries the rule that follows from it.
RESERVE_FLOOR = 1200

# Where a filed debt lives. `tasks/doc/` for a doc the fleet may write,
# `inbox/` for one reserved to the owner -- DOC-PROTOCOL.md and DOC-COMPACTION.md
# are the case that forced this: no agent can compact them, so a wall there can
# only ever be taken down in the owner's own session, and nothing said so.
DEBT_DIRS = ("tasks", "inbox")
# Matching `done` alone is sufficient ONLY because `check-task-state.py` (added
# 2026-09-09) fails the gate on any state token outside the four in
# tasks/README.md. Until then it was not: five tasks on `main` said `closed`,
# which is not a state and never was, and each one satisfied the size ledger
# exactly as well as an open task would have -- so a paid-looking debt could go
# unowned with every check green. Do not "fix" that by adding synonyms here;
# the vocabulary is the fix, and a second spelling would put the hole back.
DONE_STATE = re.compile(r"^\*\*State:\*\*\s*done\b", re.M)
BLOCKED_STATE = re.compile(r"^\*\*State:\*\*\s*blocked\b", re.M)
# A debt is DECLARED, never inferred from a path appearing somewhere in an item.
# Matching on a mention made five of today's twelve read as filed by tasks that
# merely cite the doc they are about to edit -- which is every task.
COMPACTS = re.compile(r"^\*\*Compacts:\*\*[ \t]*(.+)$", re.M)
# The due date that turns a recorded debt into a ledger entry. Absent means
# "no clock", which is the parked state this exists to end -- so an over-cap
# file whose debt carries no due date fails the same as an unrecorded one.
# Set ONCE, from the day the debt is opened. Moving it forward is visible in
# the diff of a reserved path and is an owner act; nothing here can tell, and
# `DOC-BUDGET.md` says so rather than pretending otherwise.
DUE = re.compile(r"^\*\*Size debt due:\*\*[ \t]*(\d{4}-\d{2}-\d{2})", re.M)

# Per-decision cap. A file-level cap cannot tell "many decisions" from "one
# sprawling decision", and the difference decides the remedy: a file of many
# splits, a file of one does not. Measured over all 307 decisions in the
# corpus on 2026-09-07 -- median 1,395 B, p75 2,435, p90 3,904, max 10,605 --
# so 4 KB sits at about p90 and puts 26 decisions over, every one of them a
# genuine sprawl rather than a well-argued entry.
#
# The worked example is `embarch-umbrella/decisions/bind.md`: 92.8% full, and
# its decision 22 alone is 10,605 of those 11,409 bytes. The file-level view
# says "split it"; the file has ONE decision in it, so a split cannot help.
# Only the per-decision view gives the right instruction.
#
# Ratcheted like the file caps, and seeded with the 26 at their current sizes,
# so introducing it reddens nothing on day one and each may only shrink.
DECISION_CAP = 4 * KB
# And the decision ratchet steps too, for the reason the file ratchet does --
# learned the same hour, from real work. Seeding pinned decisions at their exact
# size refused a **one-byte** growth in `embarch-dev-bench/decisions/ble.md`'s
# decision 34/37 (5,155 > 5,154) while landing a unit whose own gate was
# otherwise green. That is precisely the "refusing a correct edit at the wall"
# failure the ledger above exists to stop, reintroduced by a second mechanism
# with no allowance. 256 B is proportionate to a decision the way 1 KB is to a
# file: the median decision is 1,395 B, so a 1 KB step would be a 70% licence.
DECISION_STEP = 256
DECISION_BASELINE = REPO / "scripts" / "decision-size-baseline.json"
DECISION_HEAD = re.compile(r"(?m)^(### .*)$")

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
    # features.md is ASSEMBLED from features.d/, and gets NO BYTE CAP. The cap
    # was 20 KB and called "a backstop, not the constraint" -- but it became the
    # constraint: the file sat at 20,444 of 20,480 B, so **every new
    # `features.d/` fragment breached it**, and three separate units spent their
    # reserve shaving Status-column rows to clear a few bytes. A cap that the
    # file's own assembler breaches on every legitimate addition is not a
    # discipline anyone can exercise; it is a wall in front of the generator.
    #
    # The budget that bites is the per-row one `build_features.py` enforces
    # (600 B), which is the real constraint and the one an author can act on:
    # the file's total size is a function of how many capabilities the suite
    # has, which is not a discipline at all. `None` means no cap, no reserve
    # and no ratchet -- every caller already skips a `None`.
    ("suite-assembled", None, re.compile(r"^suite/features\.md$")),
    ("suite",       10 * KB, re.compile(r"^suite/[a-z-]+\.md$")),
    # Any DOC-*.md: the protocol layer. It splits the way anything else does
    # (DOC-COMPACTION-PASS.md came out of DOC-COMPACTION.md §6-§9), so this
    # matches the family rather than naming its members. **Cite a moved section
    # by NAME, not by number** -- this file knew about that split here and
    # nowhere else, so three other comments went on pointing at §8 and §9 for
    # two days after they stopped existing (tasks/doc/011).
    ("protocol",    12 * KB, re.compile(r"^DOC-[A-Z][A-Z-]*\.md$")),
    # A pass doc: the method for a sweep over the whole suite, run by hand and
    # reserved to the owner. Must come AFTER `protocol` -- DOC-COMPACTION-PASS.md
    # matches both and keeps the role it already had.
    #
    # 15 KB rather than `protocol`'s 12 because of what the role must carry, not
    # because of what the first one weighed: SUITE-REVIEW-PASS.md defines seven
    # hunting dimensions, and DOC-COMPACTION-PASS.md's own rule says a failure
    # signature and a rejected alternative are hot and non-negotiable -- so the
    # bytes that would be cut to reach 12 KB are exactly the ones that make the
    # rules actionable. Same size as `interfaces`, for the same reason: every
    # item must be present and the budget is spent on items.
    ("pass",        15 * KB, re.compile(r"^[A-Z][A-Z-]*-PASS\.md$")),
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
    #
    # `embarch[-.]`, not `embarch-`: the suite's own index, `embarch.md`, has no
    # hyphen, so for as long as this pattern required one that file had NO role
    # and NO cap -- 15 KB of index and status table, absent from `--report`
    # entirely, while every sibling beside it was capped at 25 KB. It was
    # classified for *ownership* (check-ownership.py --supervisor asserts every
    # tracked top-level *.md is reserved or fleet-writable, and it passed), which
    # is why nothing ever noticed: two lists over the same files, agreeing on
    # membership and not on coverage. tasks/doc/014.
    ("legacy",      25 * KB, re.compile(r"^(embarch-[a-z-]+/|embarch[-.]|DOC-|README)")),
]
EXEMPT = re.compile(r"(^\.|/\.|^history/archive/|changelog\.d/|features\.d/"
                    r"|^CLAUDE\.md$|^LICENSE$)")


# A sub-project whose decisions have been reduced to their hot half
# (DOC-COMPACTION-PASS.md, "The second pass") is held at a tighter cap than one
# that has not, so a
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

    **But it yields whether the item is BLOCKED, because `blocked` plus
    "in reserve" is a state nothing revisits.** `queue-status.py` does not
    count a blocked task as dispatchable, so no leg reads one; the unpark
    condition is prose inside the file that only a person re-reading it can
    evaluate. Measured 2026-09-07: seven compaction tasks parked that way, one
    (`api/026`) already carrying the argument that unparks it -- a verbatim
    split restates nothing, so `In flux: yes` cannot forbid it -- and one
    (`study-designer/006`) whose file this script had been reporting as PAID
    for days. A debt that is filed, at a wall, and invisible is worse than an
    unfiled one, which at least fails the gate.
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
                blocked = bool(BLOCKED_STATE.search(text))
                m = DUE.search(text)
                due = None
                if m:
                    try:
                        due = datetime.date.fromisoformat(m.group(1))
                    except ValueError:
                        due = None
                yield str(p.relative_to(REPO)), {q for q in paths if q}, blocked, due


def decisions():
    """Every numbered decision entry in the corpus, as (key, rel, heading, bytes).

    A decision is a `### N -- title` block and everything under it up to the
    next one, which is the shape all 80 decisions files use. The key is
    `<file>#<numbers>` rather than the whole heading, because a title gets
    edited and a number does not -- and the combined form (`### 37, 38 -- ...`)
    keeps both numbers, so it stays stable too.
    """
    files = sorted(REPO.glob("embarch-*/decisions/*.md")) + \
        sorted(REPO.glob("embarch-*/decisions.md"))
    for f in files:
        rel = str(f.relative_to(REPO))
        parts = DECISION_HEAD.split(f.read_text(encoding="utf-8", errors="replace"))
        for i in range(1, len(parts), 2):
            head = parts[i]
            size = len((head + parts[i + 1]).encode())
            nums = head[4:].split("\u2014")[0].split("--")[0].strip().rstrip(":").strip()
            yield f"{rel}#{nums}", rel, head[4:].strip(), size


def decision_state():
    """(fails, over_unpinned, rows) for the per-decision cap."""
    base = json.loads(DECISION_BASELINE.read_text()) if DECISION_BASELINE.exists() else {}
    fails, over_unpinned, rows = [], [], []
    for key, rel, head, size in decisions():
        # A pinned decision is over cap and allowed up to its baseline, which
        # only moves down. `min(cap, baseline)` would hold it to a cap it has
        # not reached -- a wall, not a ratchet. Same trap the file-level
        # comment names.
        limit = base[key] if key in base else DECISION_CAP
        rows.append((key, rel, head, size, limit, base.get(key)))
        if size > limit:
            (fails if key in base else over_unpinned).append((key, head, size, limit))
    return fails, over_unpinned, rows, base


def ratchet_to(size: int, cap: int, old: int) -> int:
    """Where a shrunk file's baseline lands. See RATCHET_STEP.

    `min(old, next step above size)` -- monotone by construction, so this can
    never raise a baseline, and a shrink that crosses a boundary earns real
    working room instead of pinning the file at zero headroom.
    """
    step = min(cap, ((size // RATCHET_STEP) + 1) * RATCHET_STEP)
    return min(old, max(step, size))


def ledger_verdict(rel, size, limit, items, today):
    """Why a file over its limit does or does not fail. See OVERRUN_ALLOWANCE.

    Five outcomes, and only one of them passes:
      UNRECORDED -- nothing names it. The debt is invisible; this is the
                    failure the whole filing rule exists for.
      TOO_FAR    -- past the allowance. A grace of one amendment is a grace,
                    not a renewable licence.
      NO_CLOCK   -- recorded, but with no due date, which is exactly the
                    parked state that absorbed 13 of 28 debts.
      OVERDUE    -- the clock ran out.
      IN_DATE    -- recorded, bounded, and inside its window. Passes.
    """
    named = [(i, b, d) for i, paths, b, d in items if rel in paths]
    if not named:
        return "UNRECORDED", None
    if size - limit > OVERRUN_ALLOWANCE:
        return "TOO_FAR", size - limit
    dues = [d for _, _, d in named if d]
    if not dues:
        return "NO_CLOCK", None
    soonest = min(dues)
    return ("OVERDUE" if soonest < today else "IN_DATE"), soonest


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
        filed = [(i, blocked) for i, paths, blocked, _ in items if rel in paths]
        headroom_line = limit - max(RESERVE_FLOOR, limit * (100.0 - reserve_pct) / 100.0)
        if size >= headroom_line:
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
    ap.add_argument("--due", action="store_true",
                    help="print the debt ledger, soonest due first")
    ap.add_argument("--decisions", action="store_true",
                    help="per-decision sizes against DECISION_CAP")
    ap.add_argument("--adopt-decisions", action="store_true", dest="adopt_decisions",
                    help="pin every over-cap decision at its current size (bootstrap)")
    ap.add_argument("--reserve-pct", type=float, default=RESERVE_PCT,
                    help="what counts as reserve (default %(default)g%% of min(cap, baseline))")
    args = ap.parse_args()

    base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
    items = list(open_debt_items())
    today = datetime.date.today()
    fails, tolerated, shrunk, capped, total = [], [], [], [], 0

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
            kind, detail = ledger_verdict(rel, size, limit, items, today)
            if kind == "IN_DATE":
                tolerated.append((rel, role, size, limit, cap, detail))
            else:
                fails.append((rel, role, size, limit, cap, kind, detail))

    if args.due:
        entries = []
        for rel, paths, blocked, due in items:
            for f in sorted(paths):
                fp = REPO / f
                if not fp.exists():
                    continue
                role, cap = role_and_cap(f)
                if cap is None:
                    continue
                sz = fp.stat().st_size
                limit = base[f] if f in base else cap
                # Only live pressure belongs on a ledger. A filed path that is
                # comfortably clear is a PAID item to close (--pressure says
                # so), not a debt with a clock.
                line = limit - max(RESERVE_FLOOR, limit * (100.0 - RESERVE_PCT) / 100.0)
                if sz < line:
                    continue
                entries.append((due, rel, f, sz, limit, blocked))
        if not entries:
            print("the ledger is empty: nothing is filed against a size cap.")
            return 0
        undated = [e for e in entries if e[0] is None]
        dated = sorted((e for e in entries if e[0]), key=lambda e: e[0])
        print(f"{'due':12} {'left':>6}  {'file':52} {'size/limit':>14}  item")
        for due, rel, f, sz, limit, blocked in dated:
            left = (due - today).days
            flag = "OVERDUE" if left < 0 else f"{left}d"
            print(f"{due.isoformat():12} {flag:>6}  {f:52} {sz:6}/{limit:<7} "
                  f"{rel}{'  [BLOCKED]' if blocked else ''}")
        for due, rel, f, sz, limit, blocked in undated:
            print(f"{'(no clock)':12} {'--':>6}  {f:52} {sz:6}/{limit:<7} "
                  f"{rel}{'  [BLOCKED]' if blocked else ''}")
        overdue = [e for e in dated if (e[0] - today).days < 0]
        print(f"\n{len(dated)} dated, {len(undated)} with no clock, {len(overdue)} OVERDUE.")
        if overdue:
            print("\nA leg spends its FIRST unit on the oldest overdue entry "
                  "(DOC-BUDGET.md).\nOldest: " + overdue[0][2] + " -> " + overdue[0][1])
        return 1 if overdue else 0

    if args.decisions or args.adopt_decisions:
        dfails, dover, drows, dbase = decision_state()
        if args.adopt_decisions:
            for key, head, size, limit in dover:
                step = ((size // DECISION_STEP) + 1) * DECISION_STEP
                pinned = min(dbase.get(key, step), max(step, size))
                dbase[key] = pinned
                print(f"  adopt {key}: {size} B pinned at {pinned} B")
            for key in sorted(set(dbase) - {r[0] for r in drows}):
                dbase.pop(key)
                print(f"  GONE, pinned decision pruned: {key}")
            DECISION_BASELINE.write_text(json.dumps(dict(sorted(dbase.items())), indent=2) + "\n")
            print(f"\nwrote {DECISION_BASELINE.relative_to(REPO)}: {len(dbase)} pinned")
            return 0
        print(f"{len(drows)} decisions; cap {DECISION_CAP} B, {len(dbase)} pinned over it\n")
        for key, rel, head, size, limit, pin in sorted(drows, key=lambda r: -r[3])[:20]:
            mark = "OVER" if size > limit else ("pin " if pin else "    ")
            print(f"  {mark} {size:6} B  {key}")
        biggest_share = max(
            ((size, rel, key) for key, rel, head, size, limit, pin in drows), default=None)
        if biggest_share:
            size, rel, key = biggest_share
            whole = (REPO / rel).stat().st_size
            print(f"\nlargest single decision is {100 * size // whole}% of its own file "
                  f"({key}).\nA file-level cap cannot see that, and it decides the remedy: "
                  "a file of\nmany decisions splits, a file of one does not.")
        return 1 if dfails else 0

    if args.pressure:
        # This reports rather than files, and that is the whole point:
        # DOC-COMPACTION-PASS.md's "Failure modes" warns against compacting a
        # subsystem still in flux and nothing here can tell, so whoever spends it
        # writes the item and answers that question in it.
        in_reserve, filed_clear = reserve_state(base, args.reserve_pct)
        if not in_reserve and not filed_clear:
            print(f"nothing is in reserve (the last "
                  f"{100 - args.reserve_pct:g}% of any file's limit).")
            return 0
        unfiled = [r for r in in_reserve if not r[3]]
        for rel, size, limit, filed in sorted(
                in_reserve, key=lambda r: -r[1] / r[2]):
            if not filed:
                mark = "UNFILED"
            elif all(b for _, b in filed):
                mark = "PARKED "
            else:
                mark = "filed  "
            print(f"  {mark} {100.0 * size / limit:5.1f}%  {rel}  "
                  f"{size}/{limit} B, {limit - size} B left")
            for i, b in filed:
                print(f"           -> {i}{'   [BLOCKED]' if b else ''}")
        for rel, size, limit, filed in filed_clear:
            print(f"  PAID     {100.0 * size / limit:5.1f}%  {rel} is out of "
                  f"reserve; close its item")
            for i, b in filed:
                print(f"           -> {i}{'   [BLOCKED]' if b else ''}")
        if unfiled:
            print(f"\n{len(unfiled)} file(s) in reserve with nothing filed. "
                  f"One item may name several\nfiles of one sub-project; a "
                  f"compaction pass is a sub-project act.")
            return 1
        parked = [r for r in in_reserve if r[3] and all(b for _, b in r[3])]
        print(f"\n{len(in_reserve)} file(s) in reserve, every one filed against.")
        if parked:
            verb = "is" if len(parked) == 1 else "are"
            print(f"\n{len(parked)} of them {verb} filed ONLY against a BLOCKED task, which is the\n"
                  "state nothing revisits: `queue-status.py` does not offer a blocked task\n"
                  "to a leg, so its unpark condition is prose only a person will read.\n"
                  "Re-read each park against DOC-COMPACTION.md \u00a72's split-first rule --\n"
                  "**a verbatim split restates nothing, so `In flux: yes` cannot forbid\n"
                  "one** -- and either unpark it as a split or write down which seam it\n"
                  "lacks. A scheduling block on another queued unit is a different thing\n"
                  "and stays.")
        return 0

    if args.update or args.adopt:
        raised, adopted_refused = [], []
        for rel, was, size in shrunk:
            cap = role_and_cap(rel)[1]
            base[rel] = ratchet_to(size, cap, was)
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
        print(f"{len(fails)} file(s) over their limit and not covered by the ledger:\n")
        REASON = {
            "UNRECORDED": "no open item names this file -- the debt is unrecorded",
            "TOO_FAR": f"more than the {OVERRUN_ALLOWANCE} B grace over the limit",
            "NO_CLOCK": "its item carries no **Size debt due:** date",
            "OVERDUE": "its debt is past due",
        }
        for rel, role, size, limit, cap, kind, detail in fails:
            why = "cap" if limit == cap else "ratchet baseline"
            print(f"  {rel}  {size/KB:.1f}K > {limit/KB:.1f}K ({why}; {role} cap is {cap/KB:.0f}K)")
            extra = f" ({detail})" if detail is not None else ""
            print(f"      {kind}: {REASON.get(kind, kind)}{extra}")
        print("\nAn overrun is allowed to LAND, once, on a clock: record it on an open\n"
              "item's **Compacts:** line with a **Size debt due:** date within\n"
              f"{DUE_DAYS} days. Past the date or past {OVERRUN_ALLOWANCE} B it fails here.\n"
              "DOC-BUDGET.md has the reasoning; `--due` prints the ledger.")
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
              "tasks/<scope>/<NNN>-compact-<scope>.md -- the scope of the DOC being\n"
              "compacted, so it is a path you own -- listing these paths on a\n"
              "**Compacts:** line, in the same commit that spent the reserve. The\n"
              "task carries the judgements no script can make: **In flux:**\n"
              "(DOC-COMPACTION-PASS.md), its human question, and what the pass\n"
              "may not delete. tasks/README.md has the shape.")
        print(f"FAIL: {len(unfiled)} file(s) in reserve with no debt filed.")
        return 1

    dfails, dover, drows, dbase = decision_state()
    if dfails:
        print(f"{len(dfails)} pinned decision(s) grew past their baseline:\n")
        for key, head, size, limit in dfails:
            print(f"  {key}  {size} B > {limit} B")
        print("\nA pinned decision may only shrink. Compact the entry, or split it into\n"
              "two numbered decisions if it is really two arguments (DOC-BUDGET.md).")
        print(f"FAIL: {len(dfails)} decision(s) over their baseline.")
        return 1

    print(f"All {sum(1 for _ in docs())} docs within their limit; "
          f"{len(in_reserve)} in reserve, all filed. "
          f"Corpus {total/KB:.0f} KB; {len(base)} still over cap.")
    if tolerated:
        print(f"{len(tolerated)} on the ledger, over the limit but in date:")
        for rel, role, size, limit, cap, due in sorted(tolerated, key=lambda t: t[5]):
            print(f"  due {due.isoformat()}  {rel}  {size - limit} B over")
    if dover:
        print(f"{len(dover)} decision(s) over the {DECISION_CAP} B cap and not yet pinned "
              f"(--adopt-decisions to seed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
