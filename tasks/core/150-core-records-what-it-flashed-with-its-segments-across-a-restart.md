# 150 — Core records what it flashed, with its segments, across a restart

**State:** claimed by agent/core/150-core-records-what-it-flashed-with-its-segments-across-a-restart, 2026-11-24 09:53
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, Test phase), checked against `notes/hil/08-existing-pieces.md`: `last_images` is in memory, holds no segments, and a restart forgets it
**Issue:** EMB-361
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`last_images` (`src/lease.rs`, `FlashedImage`, `ImageLog`) holds, per chip, the
path, the SHA-256 of the file as given, the time and the lease holder, in
memory only, and no load segment, so nothing can be compared with a readback.
The call log's flash entry names the board and the token's scope (decision
122), not the segments.

When this is done, at each successful flash and bootload Core computes the
shared crate's `image_segments` (study-designer feature `hil-image`, landed in
`study-designer/090`) from the bytes it flashed, and appends
`{chip, probe_serial, role, identity, segments, scope, at_utc_ms, call_log_seq}`
to `flashed-images.jsonl` beside the run log. The latest entry per board is
what Core flashed there. At start the file is read back, so a restart keeps
it; an entry from before a start stays, and a later readback says whether the
chip still holds it (decision 12 already says a bench may have been driven by
another Core). `GET /status`'s `last_images` reads from it, **unchanged in
shape**. Field names may differ from the list above if the code already has a
name for the same fact; say so in the interface doc.

## Why now

The readback and the smoke check before a bench's first test wait on this, and
so does the `unreleased` image's "scope of the token that flashed it"
(`notes/hil/03-test.md`, "A run", item 3). EMB-361.

**Burndown leg: no new numbered decision.** Amend decision 93 in place. If the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):**
- **Decision 93 (`decisions/lease.md`) has 87 B before its per-decision
  limit.** Amend it with one short sentence pointing at the new interface text,
  or tighten 93's own wording to make room; `check-docs.py` is the judge.
- **`embarch-core/spec.md` is in reserve** (9,160 of 10,240 B), filed as
  `tasks/core/147-compact-core.md`, `blocked`, `In flux: yes`. Put the file's
  shape in `interfaces/` (a new file, or `hardware.md`), not in `spec.md`. If
  `spec.md` must change at all, do 147's compaction in this unit: move
  reference detail into `spec/` verbatim, honouring 147's `Must not delete:`
  line, and close 147 `done` (leave its `In flux:` as written).
- Other decisions near their limit, which this task should not need: signing#110,
  host-study#95, run-log#111, instruments#104.

**Shared crate dependency:** turn on `embarch-study-designer`'s `hil-image`
feature in Core's manifest. `study-designer/091` is fixing that module's
overflow checks concurrently without changing its signature; build against
`main`'s version. Say in this file whether `Cargo.lock` moved and why.

## Done when

- [ ] A fixture hex flashed through a fake backend gives an entry with its
      segments, identity and scope.
- [ ] A new `AppState` over the same folder reads the entry back.
- [ ] `GET /status` answers as before (an existing or new test pins its shape).
- [ ] The file's shape is documented in `embarch-doc/embarch-core/interfaces/`,
      and decision 93 amended.
- [ ] Gate green (`../../embarch-fleet/gate.md`); the native Windows build is
      the supervisor's hardware debt, so note anything Windows-specific.
- [ ] `changelog.d/` fragment dropped, `features.d/` row if a feature row is
      owed, `status.d/` fragment for anything suite-level made false.
