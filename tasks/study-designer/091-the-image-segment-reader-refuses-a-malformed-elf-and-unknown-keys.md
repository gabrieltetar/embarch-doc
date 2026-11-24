# 091 — The image-segment reader refuses a malformed ELF and unknown keys

**State:** open
**Source:** the post-merge review of `study-designer/090` (2026-11-24): unchecked offset arithmetic in `src/hil_image.rs`, and HIL JSON types without `deny_unknown_fields`
**Issue:** EMB-397
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/hil_image.rs` (feature `hil-image`) reads ELF header fields as `u64` and
adds them unchecked: `off + filesz` when it slices a segment,
`phoff + i * phentsize` for each program header, and `off + len` in the `rd`
field reader. A malformed or hostile ELF whose fields sum past `u64::MAX`
panics in a debug build instead of returning an error. Separately, `Segment`,
`BenchImage` and `BenchFirmwareList` derive `Deserialize` without
`deny_unknown_fields`, where `interfaces/hil-shapes.md` asks every HIL JSON file
to refuse unknown keys and `host_study.rs` already does.

When this is done every offset sum and product in the ELF path is checked
(`checked_add`, `checked_mul`), an overflow is an `ImageError` (the existing
`ImageError::Elf("truncated")` or a named variant, the worker's call), and the
three types refuse an unknown key.

## Why now

Core will call `image_segments` on files a caller hands it once its flash
record uses the identity (`core/150`, in flight beside this one). Nothing turns
the feature on yet, so the fix is cheap now. EMB-397.

**Burndown leg: no new numbered decision.** The contract is
`interfaces/hil-image.md`. If the change seems to need a new decision, stop and
say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-study-designer` file is in
reserve. Decisions near their per-decision limit are ones this task does not
touch (streams#39, versioning#12, seals#17, protocols#58, authoring#73,
declares#40, protocol-exec#60, ble#44).

**Shared crate:** the supervisor reads this diff before merging and builds
every consumer's feature set. Do not change `image_segments`'s signature or the
three types' fields: `core/150` builds against them concurrently.

## Done when

- [ ] An ELF whose segment offset plus size overflows `u64`, and one whose
      program-header table position overflows it, each give an `ImageError`,
      in tests that run in a debug build.
- [ ] `Segment`, `BenchImage` and `BenchFirmwareList` each refuse an unknown
      key, with a test each.
- [ ] `interfaces/hil-image.md` says both.
- [ ] Gate green under every feature set the crate's consumers build it with
      (`../../embarch-fleet/gate.md`), `hil-image` and `--all-features`
      included.
- [ ] `changelog.d/` fragment dropped.
