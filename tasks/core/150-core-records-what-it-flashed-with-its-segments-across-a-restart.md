# 150 — Core records what it flashed, with its segments, across a restart

**State:** done — flashed-images.jsonl written per flash and bootload with segments, scope and call-log seq, read back at start; decision 93 amended
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

- [x] A fixture hex flashed through a fake backend gives an entry with its
      segments, identity and scope.
- [x] A new `AppState` over the same folder reads the entry back.
- [x] `GET /status` answers as before (an existing or new test pins its shape).
- [x] The file's shape is documented in `embarch-doc/embarch-core/interfaces/`,
      and decision 93 amended.
- [x] Gate green (`../../embarch-fleet/gate.md`); the native Windows build is
      the supervisor's hardware debt, so note anything Windows-specific.
- [x] `changelog.d/` fragment dropped, `features.d/` row if a feature row is
      owed, `status.d/` fragment for anything suite-level made false.

## Notes (worker)

- **Cargo.lock moved by one line**: `embarch-study-designer` gains `sha2 0.11.0` (the `hil-image` feature's dependency, already in the tree through Core). Built against `main`'s `hil_image.rs`.
- **Fields**: the entry uses `FlashedImage`'s existing names (`flashed_at`, `lease_holder`, `path`, `sha256`) beside the task's; `flashed_at` and `at_utc_ms` are one instant. New: `role`, `identity`, `segments`, `scope`, `at_utc_ms`, `call_log_seq`. Said in `interfaces/hardware.md`.
- **call_log_seq**: the call-log entry is written after the handler, so the handler only marks the chip on the call's `BoardNote` and `call_log_middleware` appends the line with the entry's `seq` (and the scope). A handler run without that middleware writes nothing.
- **"Fake backend"**: Core has no fake flash backend (`hardware::flash` opens a real probe), so the tests drive `ImageLog` and `image_detail` on a fixture hex, and a stand-in `/flash` handler through `call_log_middleware`. The `/flash` and `/bootload` handler bodies themselves are not run by a test.
- **Bootload records no segments** (`identity`/`segments` `null`): the slot address of a signed image is not known to Core. A readback has nothing to compare for a bootloaded board until something supplies it.
- **Windows-specific**: none; `std::fs` append only. Native Windows build is the supervisor's debt as usual.
- **Hardware-verification debt**: one real `/flash` and `/bootload` on a bench, then check `flashed-images.jsonl` in the data folder has the line, `role`, `call_log_seq` matching the call-log entry, and survives a Core restart.
- `spec.md` untouched, so 147's compaction was not triggered.
