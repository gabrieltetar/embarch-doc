# 092 — The image-segment reader checks a segment's end address

**State:** claimed by agent/study-designer/092-the-image-segment-reader-checks-a-segments-end-address, 2026-11-24 10:29
**Source:** reading `study-designer/091`'s shared-crate diff before merging it
**Issue:** EMB-399
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/hil_image.rs` (feature `hil-image`) checks every offset sum in the ELF path
since `study-designer/091`. One sum is left, and it is an **address**, not an
offset: `merge` computes each merged segment's end as `*a + d.len() as u64`,
unchecked. An ELF whose `PT_LOAD` physical address sits within a segment's
length of `u64::MAX`, followed by any second segment, or a bin given such a
base, overflows there and panics in a debug build. Core will run this reader
over files a person hands it.

When this is done the end is `checked_add`ed, and an overflow is an
`ImageError`, as the offset sums already are (reuse an existing variant if one
fits, as 091 did; `image_segments`'s signature and the public types stay as
they are, so `embarch-core` builds against it untouched). Check any other
address arithmetic in the same file while you are there.

## Why now

A panic on a malformed file in a shared crate becomes a panic in Core. EMB-399.

**Burndown leg: no new numbered decision.** If something needs recording, amend
in place.

**Doc-size reserve (dispatch note):** no `embarch-study-designer` file is in
reserve, and the decisions near their limit (streams#39, versioning#12,
seals#17, protocols#58, authoring#73, declares#40, protocol-exec#60, ble#44)
are ones this task does not touch.

## Done when

- [ ] An ELF with a load address near `u64::MAX` and a second segment gives an
      `ImageError` in a debug-build test.
- [ ] A bin with such a base and enough bytes gives an `ImageError`.
- [ ] `interfaces/hil-image.md` says addresses are checked as well as offsets.
- [ ] Gate green (`../../embarch-fleet/gate.md`), under `hil-image` and
      `--all-features` at least.
- [ ] `changelog.d/` fragment dropped.
