# 062 — `decisions/target-json.md` decision 19 is over the per-decision cap and nothing has filed it

**State:** done — leg 076, worker on `agent/api/062-compact-target-json`
**Source:** `scripts/check-doc-size.py --decisions`, run during leg 076's refill sweep —
`OVER 5510 B embarch-api/decisions/target-json.md#19` against the 4,096 B per-decision cap. It is
**not** on the size ledger (`--due` lists only `core-link.md` and `zephyr.md` for this scope), so
nothing was going to pay it on a clock.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Decision 19 in [embarch-api/decisions/target-json.md](../../embarch-api/decisions/target-json.md)
is 5,510 B against a 4,096 B per-decision cap — 34% over. The file as a whole is not in reserve,
which is why the ledger never saw it: the *file* budget and the *decision* budget are separate
checks and only the first has a clock. Bring decision 19 under the cap.

**Prefer a split over a squeeze**, per [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 — a verbatim
split restates nothing and so cannot lose a fact, which is the whole reason it is preferred. If
decision 19 is really one sprawling decision rather than several wearing one number, compact it
instead and say in the body that you judged it so.

**A written "no safe cut" is an acceptable outcome.** Two of leg 075's three compaction units
concluded the cap was wrong rather than the file, and said so; that is a finding, not a failure.
What is not acceptable is manufacturing bytes by deleting a fact that only lives here.

## Why now

An over-cap decision is invisible to the one mechanism that would otherwise schedule it: the size
ledger clocks *files*, and this is a *decision*. So it will sit at 34% over indefinitely, and it
grows every time somebody amends it — which is exactly the shape that produced
`embarch-api/decisions/zephyr.md` at 14,269/12,288 B.

## Done when

- [x] `python3 scripts/check-doc-size.py --decisions` no longer reports
      `embarch-api/decisions/target-json.md#19` as OVER — or the task is closed with a written
      argument for why no safe cut exists, naming what a cut would have destroyed.
- [x] Every existing citation of api decision 19 still resolves: `scripts/check-decision-refs.py`
      green. **If a split moves the decision to a new file, the half with out-of-scope citers keeps
      the original filename** — see `topology/026`, leg 075, where splitting the other way would
      have left four sub-projects' citations red with no legal fix available.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.

## Resolution

Decision 19 was one number wearing two distinct decisions: the crate-owned FNV-1a hash for
`extra_args` (with its migration/orphaning argument), and the `target.json` descriptor file itself
(what it is, when it's written, what its absence means). Neither half restates the other — the
hash entry only needs to say "and there's a `target.json` too" in passing, the file entry only
needs "the hash covers `extra_args`" in passing — so this is a **verbatim split**, not a squeeze:
each paragraph moved intact into whichever of the two new headings it already belonged to, nothing
reworded to save bytes. New number: **69** (next free in the sub-project), both entries staying in
`target-json.md` since the *file* was never in reserve — only the one decision was over its own
cap. `embarch-api/decisions.md`'s index row and `embarch-api/interfaces/config.md`'s one citation
of "decision 19" for absence-semantics were repointed to 69, since that's the half that actually
carries that claim now.

**Citations:** `check-decision-refs.py` was green before and after; every existing reference to api
decision 19 was inside `embarch-api/` itself (`decisions.md`, `interfaces/config.md`,
`decisions/build.md`, `decisions/zephyr.md`) — no other sub-project cites it, so the "out-of-scope
citer keeps the filename" rule from `topology/026` doesn't bind here: both halves stay in the one
file under their own numbers, and the two in-repo prose citations were moved to whichever number
now states the fact they're citing.

**Compaction question (embarch-doc §DOC-COMPACTION-PASS.md):** yes, `embarch-api/spec.md` alone
answers what someone needs to work on `target.json`/build-dir naming today — the resolved-selection
descriptor, the length-prefixed hash, absence-means-unattributable are all already stated as
current truth in `spec.md` and `interfaces/config.md`. `decisions/target-json.md` was purely
rationale (why FNV-1a, why written after not before, why no migration) and none of that rationale
is needed to *use* the mechanism, only to *change* it safely — which is exactly what a decisions
file is for. No fact was destroyed; this was a pure re-filing under two numbers instead of one.
