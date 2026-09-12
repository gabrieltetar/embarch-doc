# 029 — `interfaces/limits.md` claims "every bound the crate declares" and omits two live ones

**State:** open
**Source:** refill sweep, leg 087, 2026-09-11. `embarch-study-designer/interfaces/limits.md` against
`src/limits.rs` and `src/records.rs`.
**Scope:** study-designer
**Hardware:** none.
**Owner:** no

## What

`interfaces/limits.md` opens by claiming it lists *"Every bound the crate declares, each marked
`[measured <date>]` or `[assumed]`"*. Two are missing from both the table and the
retired-constants paragraph:

- `MAX_RECORD_MAGIC_LEN = 8` (`src/limits.rs`), which bounds `RecordFraming.magic`
  (`src/records.rs`, a `Vec<u8, MAX_RECORD_MAGIC_LEN>`)
- `MAX_BAD_RECORDS_REPORTED = 32` (`src/limits.rs`), which bounds `RecordReport.bad_offsets`
  (`src/records.rs`, a `Vec<u32, MAX_BAD_RECORDS_REPORTED>`), with a cap test beside it

Both are live capacity bounds in use, not retired constants. Add a row each to the first table.
**The sizing rationale is already written verbatim in their own doc comments in `src/limits.rs`** —
use it rather than composing a new one, and carry the `[measured <date>]` / `[assumed]` marker
honestly: if a constant's comment does not establish a measurement, it is `[assumed]`, and **do not
promote one to measured because the number looks deliberate.**

**Then check the claim is true after your edit rather than true about the two you were told about.**
Walk `src/limits.rs`'s public constants against the table and report any further omission in the
task file; a doc that says "every" is worth one exhaustive pass.

## Why now

`limits.md` exists so a caller can size a buffer without reading the crate. A file whose opening
sentence is "every" and whose table is not is worse than one that never claimed completeness,
because the absence reads as "no such bound exists".

## Done when

- [ ] Both constants appear in the first table with their bound target and an honest
      `[measured <date>]` / `[assumed]` marker.
- [ ] A full pass over `src/limits.rs`'s public constants is done and any further gap is either
      filled or named in this task file.
- [ ] No constant's value changes.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
