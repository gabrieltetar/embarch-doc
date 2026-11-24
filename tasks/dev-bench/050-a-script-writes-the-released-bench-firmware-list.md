# 050 — A script writes the released bench-firmware list

**State:** claimed by agent/dev-bench/050-a-script-writes-the-released-bench-firmware-list, 2026-11-24 10:29
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, Test phase: "the released bench-firmware hash list"), with `notes/hil/03-test.md`, "A run", item 3
**Issue:** EMB-389
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

A bench board's image reads as released only when its identity is in the list
the release ships (`notes/hil/03-test.md`, "A run", item 3: a Core in the
engineer's own account takes the hash list from a checkout its configuration
names). Nothing writes that list yet, and `embarch-dev-bench` has no release
workflow (`embarch-release-signing-proposal.md`, "Bench firmware").

The list's shape already exists: `bench-firmware.json`, `BenchFirmwareList` and
`BenchImage` in `embarch-study-designer` (feature `hil-image`), documented in
`embarch-study-designer/interfaces/hil-image.md`, which names "the script
writing the bench-firmware list" as a consumer. `examples/image_segments.rs`
there prints an image's segments and identity.

When this is done `scripts/bench-firmware-list.py <release> <image>...`, beside
`patch-sums.py`, writes `release/bench-firmware.json` in that shape: for each
image its app, board and shield, version and commit, and its identity and
segments, taken from the shared crate's example binary (run it through `cargo`
in the sibling `embarch-study-designer`; do not reimplement the segment
reduction in Python). Entries are sorted. The list is committed with the release
it names, and the person flashes exactly those images. How the script learns
an image's app, board, version and commit is yours to choose and document.
`release/characterisation/<board>.json` beside it is the next step's (the
characterisation, `hil-characterisation.md`); leave a placeholder only if it
costs nothing.

## Why now

Core's readback and the characterisation both read this list. EMB-389.

**Burndown leg: no new numbered decision.** The design is the HIL plan's, kept by
the owner; document it in `spec.md` and the repo README and amend an existing
decision in place if one governs scripts. If the change seems to need a new
decision, stop and say so in this file.

**Doc-size reserve (dispatch note): `embarch-dev-bench/spec.md` is in reserve**
(9,275 of 10,240 B, 965 B left; out of reserve at 9,039 B or less). Its
compaction, `tasks/dev-bench/049-compact-dev-bench.md`, is parked `blocked` on
`In flux: yes`, and its `Unparks when:` says the next unit that writes `spec.md`
carries the compaction. **If you write `spec.md`, compact it out of reserve in
this unit**: move reference detail into `spec/` verbatim with a link, or shorten
the longest paragraphs without dropping a fact or a decision pointer. Carry
049's **Must not delete:** the wire and threading paragraphs, the workspace
layout tree, and the pd-bench and `patch-sums.py` paragraphs as stated. Do not
edit `tasks/dev-bench/049-compact-dev-bench.md`; I close it at the fold if
`check-doc-size.py --pressure` no longer lists `spec.md`. Decisions near their
limit (logging#38 and #39, ble#34/37, protocols#41, conventions#47, capture#29)
are ones this task does not touch.

## Done when

- [ ] The script's output for the shared crate's fixture image
      (`tests/fixtures/hil-image/` in `embarch-study-designer`) carries the
      identity and segments the crate's own test expects for it.
- [ ] Two images give two entries, sorted.
- [ ] The README says where the list lives and when it is written.
- [ ] A test for the script runs in the repo's existing Python test style
      (`scripts/test_patch_sums.py`).
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped.
