# 078 — Compact ui's spec.md

**State:** done — 2026-10-26 — spec.md 9,516 -> see Result.
**Size debt due:** 2026-10-13 (two weeks; the file is 5 B inside reserve).
**In flux:** no — as of 2026-10-26. The "In flux" section below is kept as the history of why it was parked; its one instruction (re-check the "role is a fixed slot" paragraph, never re-drop "served by the binary") still binds and is repeated under `Must not delete`.
**Source:** tasks/ui/077 restored "served by the binary" in `embarch-ui/spec.md`'s
dev-bench-picker invariant, which pushed the file to 9045/10240 B (88.3%),
inside `check-doc-size.py`'s reserve.
**Scope:** ui
**Hardware:** none
**Owner:** no

**Compacts:** embarch-ui/spec.md

## Dispatch note, 2026-10-26 — read this first

**Today's numbers:** `embarch-ui/spec.md` is **9,516 / 10,240 B** (92.9%, 724 B left); the reserve
line is 9,216 B, so getting under it is the target and under the cap is not enough. The 9,045 B in
`## What` below is the September figure.

**Method.** Read `DOC-COMPACTION.md` §2 (split first) and `DOC-COMPACTION-PASS.md` before cutting.
A verbatim move of a self-contained section into an existing ui topic file restates nothing and is
the cheaper move if one fits — **but check the destination's headroom first**: `embarch-ui/open.md`
is itself in reserve (4,366 / 5,120 B, parked under `ui/088`) and must not receive bytes, and
`embarch-ui/interfaces.md` is 13.4 K of 15 K. Otherwise compact settled prose only, quoting every
hunk in the commit message. Answer `DOC-COMPACTION-PASS.md`'s human question (can `spec.md` alone
tell someone what they need to work on `embarch-ui` today?) in your Result, in your own words.

**Doc-only.** You have an `embarch-doc` worktree only; no code change is expected. Gate:
`python3 scripts/check-docs.py`, `check-ownership.py --scope ui`. If you stop above the reserve line
because everything left is live, leave this task `open` with the remaining reserve stated and a
dated reason — an honest outcome, not a failure. Otherwise mark it `done`.

## What

`embarch-ui/spec.md` is in the size reserve (9045/10240 B, 1195 B left). Run a
compaction pass per `DOC-COMPACTION-PASS.md`, quoting every hunk in the commit
message per its quoting rule.

## In flux

Was yes on 2026-09-29: ui/077 (that leg) had just edited the "role is a fixed slot" paragraph
(dev-bench-picker invariant) to restore a dropped load-bearing phrase.
Whoever runs this compaction should re-check that paragraph is still current
before touching it, and must not re-drop "served by the binary" or the
"served from the binary like every other vocabulary" tie to
`embarch-ui/decisions/topology-roles.md` — that was the exact loss this task's
predecessor (ui/075 → the ui/077 restore) fixed.

## Must not delete

- The "served by the binary" phrase in the dev-bench-picker sentence
  (the "role is a fixed slot" paragraph).
- Any other named claim currently quoted in `embarch-ui/spec.md`'s invariants
  list — this pass is a squeeze, not a second drop.

## Done when

- [x] `embarch-ui/spec.md` back under the reserve threshold in
      `scripts/check-doc-size.py`.
- [x] Every hunk quoted in the commit message per `DOC-COMPACTION-PASS.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Result, 2026-10-26

`embarch-ui/spec.md` 9,516 -> 8,986 B (reserve line 9,040 B; PAID). Method: a split, not a squeeze. The `## Verification technique` section moved verbatim to the new `embarch-ui/spec/verification.md` (873 B), leaving a two-line pointer; nothing deleted, so nothing to quote beyond that. The "role is a fixed slot" paragraph and "served by the binary" were not touched. Gate green.

Human question (can spec.md alone say what to work on today?): yes for shape, invariants and what is live; the only thing now one hop away is how the UI is verified (harness file names), which is a pointer, not a rule.
