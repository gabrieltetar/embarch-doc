# 151 — The spec says what Core persists of what it flashed

**State:** claimed by agent/core/151-the-spec-says-what-core-persists-of-what-it-flashed, 2026-11-24 10:29
**Source:** the reviewer of `core/150` (Core records what it flashed, with its segments, across a restart)
**Issue:** EMB-400
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`core/150` made Core persist what it flashed: `ImageLog` writes
`flashed-images.jsonl` beside the run log and re-reads it at start, so
`GET /status`'s `last_images` survives a restart. Two docs still say otherwise:

- `embarch-core/spec.md`'s invariant "**Core keeps no persisted 'current
  firmware' record.** A manifest binding lives only as long as the study that
  made it. Write-ahead state that can go stale is the pattern this suite
  forbids." Decision 93 used to close by tying itself to that line; the
  `core/150` amendment dropped the sentence and left the spec standing.
- `embarch-core/interfaces/hardware.md`'s `/status` row, whose `last_images`
  clause still says "since it started".

When this is done the spec's invariant says what holds now: Core keeps a
persisted record of what it flashed, and that record is history, not a claim
about what the chip holds now (decision 93 already says "an old entry is what
Core flashed, not what the chip holds"; a readback is what answers that), so it
is not the write-ahead state the line forbids. A manifest binding still
lives only as long as its study. The `/status` row no longer says "since it
started". This is a doc fix, not a revert: the persistence is what EMB-361
asked for.

## Why now

The spec is what an agent loads to work on Core, and it currently contradicts
the code. EMB-400.

**Burndown leg: no new numbered decision.** If decision 93 needs a sentence,
amend it in place; it has **35 B** left under the per-decision cap, so prefer
saying it in the spec and keep 93 within its size.

**Doc-size reserve (dispatch note): `embarch-core/spec.md` is in reserve**
(9,160 of 10,240 B, 1,080 B left; out of reserve at 9,039 B or less). Its
compaction, `tasks/core/147-compact-core.md`, is parked `blocked` on
`In flux: yes`, and its `Unparks when:` says the compaction rides in the next
core unit that writes `spec.md`. **That is this unit: compact `spec.md` out of
reserve as part of it.** Move reference detail into `spec/` verbatim (a new
`spec/<topic>.md` beside `spec/deployment.md`, linked from `spec.md`), which
restates nothing and so is safe while the signing surface moves. Carry 147's
**Must not delete:** the invariants bullets (lease gate, call log, challenge
route) and the decision citations. Do not edit `tasks/core/147-compact-core.md`;
I close it at the fold if `check-doc-size.py --pressure` no longer lists
`spec.md`. Other core decisions near or over their limit (signing#110,
host-study#95, run-log#111, instruments#104) are ones this task does not touch.

## Done when

- [ ] `spec.md` no longer states "no persisted current-firmware record" without
      the `flashed-images.jsonl` record and why it is not write-ahead state.
- [ ] The `/status` row's `last_images` clause in `interfaces/hardware.md` no
      longer says "since it started".
- [ ] `scripts/check-doc-size.py --pressure` does not list
      `embarch-core/spec.md`; moved text byte-identical; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped.
