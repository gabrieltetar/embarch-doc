# 024 — `decisions/topology-tab.md` decision 10 is over the per-decision cap and nothing has filed it

**State:** done — leg 077, 2026-09-10, `agent/ui/024-decision-10-over-cap`
**Source:** `scripts/check-doc-size.py --decisions`, run during leg 076's refill sweep —
`OVER 4430 B embarch-ui/decisions/topology-tab.md#10` against the 4,096 B per-decision cap. Not on
the size ledger, because the ledger clocks files and this is a decision.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Decision 10 in [embarch-ui/decisions/topology-tab.md](../../embarch-ui/decisions/topology-tab.md)
is 4,430 B against a 4,096 B cap — 334 B over, the mildest instance of this shape in the suite.
Bring it under.

**Prefer a verbatim split** ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). At 334 B over, a
compaction of this one decision is also plausibly the honest answer; whichever you pick, say in the
body which and why. **A written "no safe cut" is an acceptable outcome** — but at 8% over it is a
weaker claim than it was for the files leg 075 refused to shave, so make the argument explicitly
rather than by assertion.

## Why now

`embarch-ui` is the sub-project with the fewest open tasks in the queue — every file under
`tasks/ui/` is `done` or `blocked` — so a worker dispatched to `ui` has nothing else to take, and
"at most one task per sub-project" is per *slot*: an empty scope costs the fleet a whole worker's
concurrency, not just a task.

## Done when

- [x] `python3 scripts/check-doc-size.py --decisions` no longer reports
      `embarch-ui/decisions/topology-tab.md#10` as OVER — or the task is closed with a written
      argument for why no safe cut exists, naming what a cut would have destroyed.
- [x] Every citation of ui decision 10 still resolves: `scripts/check-decision-refs.py` green. If a
      split moves it, the half with out-of-scope citers keeps the original filename.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.

## Resolution

**Compacted, not split.** At 334 B over (8%), the entry did not read as two
arguments — the routing decision, its history with `embarch-api` decision 67 /
`embarch-topology` decision 18, the diagram-geometry fix, and the markup-defect
fix are all consequences of the same "this tab is the only human surface"
claim, not independent claims that would earn their own numbers. A file split
had nothing to move to either: this file holds one decision (10), so a
file-level split (moving half of one entry into a second file) would only have
relocated the cap problem, not solved it.

Applied the hot/cold test from `DOC-COMPACTION-PASS.md`: cut four spans that
were investigation narrative or pure provenance, no invariant/constraint/
rejection/failure-signature attached —

- `"Two consequences, both of which were written when this tab was the sole surface and are stated here as they were reasoned then."` — meta-commentary about when the sentences after it were written.
- `"The shared Core client had no wrapper for any of them, so building this tab touched embarch-api's workspace as well."` — build-log provenance, not a constraint a future reader needs.
- `"— caught in the first real render rather than by reasoning about it."` — investigation narrative attached to the geometry-bug sentence, which keeps the bug and the fix.
- `"Found by rendering the row in headless Firefox and reading the attribute back."` — investigation method; the failure signature it followed ("no Rust test could see it") stays.

Result: 4,430 B → 4,034 B, 62 B of headroom under the 4,096 B cap (not pinned
to the exact byte, per `DOC-BUDGET.md`'s own warning about zero-headroom
splits). Every rejected alternative, constraint, and failure signature in the
original entry is still present verbatim; nothing renumbered.

**Other OVER entries found by the same sweep (not fixed, out of scope):**
`embarch-topology/decisions/validation.md#25` (6,224 B), `embarch-outpost/decisions/testing.md#22`
(4,442 B), `embarch-core/decisions/logging.md#44` (4,352 B) — all three genuinely `OVER`
(unpinned), distinct from the 27 `pin`-ratcheted entries the same run lists.
