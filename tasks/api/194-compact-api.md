# 194 — compact `embarch-api/open.md`

**State:** done — open.md 4,292 to 3,779 B by verbatim split: live-log debt to open/bench-verification.md, Windows smoke-harness gap to open/unmeasured-details.md
**Scope:** api
**Hardware:** none
**Owner:** no
**Compacts:** embarch-api/open.md
**Size debt due:** 2026-12-09
**In flux:** no
**Must not delete:** every hardware or owner debt line with the command it names to run, including the `person_writer` Windows-branch line from `api/193` (it is struck only once `cargo test person_writer` has run on Windows).

## What

`open.md` is in reserve (4,292 of 5,120 B) after `api/193` added the `person_writer` Windows debt. Compact it under `DOC-COMPACTION.md`. Answered by the unit that just worked in it: `open.md` is not moving as a whole; the person mirror's caller (C.17) will touch only the one `person_writer` line.

## Done when

- [x] `open.md` is out of reserve and every `Must not delete:` line survives.
