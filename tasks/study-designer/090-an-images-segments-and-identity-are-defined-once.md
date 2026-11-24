# 090 — An image's segments and identity are defined once

**State:** open
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, Test phase): a readback compares a chip's load segments with the artifact Core flashed (`notes/hil/03-test.md`, "A run", item 3), and no shared definition of either exists
**Issue:** EMB-357
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

Core keeps the SHA-256 of the file it was given (`last_images`), which a
readback cannot compare with: a chip holds load segments, not a hex or ELF
file. The HIL design compares the load segments' SHA-256 with the artifact Core
flashed, and every bench board's image with the bench firmware the installed
release ships. Neither the segment list nor the released list's shape exists.

When this is done the shared crate holds them, in the plan's recommended shape
(kept by the owner, `14-implementation-plan.md` line 64), **host-only, behind a
feature like `reducers`**, so nothing reaches the firmware side:

- `image_segments(bytes, format, base) -> Vec<Segment>`, `format` one of hex,
  ELF or bin (bin with a base address): the maximal contiguous address ranges
  the image writes, each `{address, length, sha256}`, sorted by address. For an
  ELF, the bytes of its loadable segments at their physical addresses, so a hex
  and an ELF of one build give the same list.
- **The image's identity**: the SHA-256 of the canonical JSON of that list.
- **The bench-firmware list's shape**, `bench-firmware.json`:
  `{schema, release, images: [{app, board, version, commit, identity, segments}]}`.
- **A small example binary** printing a file's segments and identity as JSON
  (`cargo run --example image_segments -- <file>`), for the list's script.

A new dependency for ELF or hex parsing is allowed behind that feature only;
say in this file which and why, or parse by hand if the subset needed is small.

Docs, in `embarch-doc/embarch-study-designer/`: a new
`interfaces/hil-image.md` giving the segment rule, the identity and the list's
shape; `interfaces/hil-characterisation.md`'s `firmware.image_sha256` points at
the identity; `spec.md` names the feature and the function.

## Why now

Core's record of what it flashed and its readback, the script writing the
bench-firmware list, and a bench board's characterisation each wait on this one
definition, so Core, the script and `verify` agree. EMB-357.

**Burndown leg: no new numbered decision.** The contract lives in the
interface doc. If the change seems to need a new decision, stop and say so in
this file.

**Doc-size reserve (dispatch note):** no `embarch-study-designer` file is in
reserve. Decisions near their per-decision limit are all ones this task does
not touch (streams#39, versioning#12, seals#17, protocols#58, authoring#73,
declares#40, protocol-exec#60, ble#44).

**Shared crate:** the supervisor reads this diff before merging, and builds
every consumer's feature set.

## Done when

- [ ] A fixture hex and the ELF it was made from give the same segments and
      identity.
- [ ] A bin with a base address gives one segment at that address.
- [ ] A hex with a gap gives two segments.
- [ ] Gate green under every feature set the crate's consumers build it with
      (`../../embarch-fleet/gate.md`).
- [ ] `interfaces/hil-image.md` gives the segment rule, the identity and the
      list's shape; `hil-characterisation.md` points at it; `changelog.d/`
      fragment dropped.
