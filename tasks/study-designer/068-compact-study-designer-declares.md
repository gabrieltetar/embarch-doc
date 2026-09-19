# 068 — `embarch-study-designer/decisions/declares.md` is in reserve

**State:** blocked
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by decision 77
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/decisions/declares.md
**Size debt due:** 2026-09-25
**In flux:** yes
**Blocked on:** decision 77 being exercised on a bench — one study run with the build toggle on, which is what would move `MAX_SNIPPETS_PER_BUILD`/`MAX_BUILD_EXTRA_ARGS` if anything does. Unparks the moment that run lands.

## What

The declares group is **12,200 / 12,288 B (99.3%), 88 B left**. Out of reserve
when this closes, or the task says why not.

The entry that crossed the floor is **77** — a study's own build spec and the
outpost mode it requires. It was trimmed five times on the way in.

## Why the seam is a split, not a squeeze

The file's own header says it is about "firmware versions, and how each is
verified", and decision 40 is that. Decision 77 is a different thing wearing the
same field: **what a study builds**, and **what it refuses to run against** —
one is a version string compared after the fact, the other a selection resolved
before the run and a mode read off the wire. The GATT half already left this
file on 2026-09-13 for exactly this reason.

So: `decisions/builds.md`, decision 77 moved verbatim, per
[../../DOC-BUDGET.md](../../DOC-BUDGET.md) §3. Decision 40 stays, and its
"verification asymmetry" paragraph gains a pointer to the file that closes the
DUT half of it.

## In flux

**The `limits.rs` caps 77 adds are sized against one target repo and have never
been hit.** `MAX_SNIPPETS_PER_BUILD` (8) and `MAX_BUILD_EXTRA_ARGS` (8) in
particular are the kind of number a real composition moves; a bench run with the
build toggle on is what would settle them, and the entry will want room to
record it.

## Done when

- [ ] Out of reserve, or the task says why not.
- [ ] **The three rules a reader will try to simplify survive**: no pinned
      `build_id`, no project name in the spec, and two masks rather than one.
      Each is a rejected alternative, not a detail.
- [ ] `decisions.md`'s index row updated, and the "seventeen files" count in it
      re-checked (`tasks/study-designer/066` already says it is wrong).
- [ ] Every inbound reference to 77 still resolves (`check-decision-refs.py`).
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
