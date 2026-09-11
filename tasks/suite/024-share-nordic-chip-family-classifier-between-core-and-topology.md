# Give `embarch-core` a way to reuse `embarch-topology`'s Nordic chip-family classifier

**State:** claimed — leg 076, supervisor's own hands. Announced to #embarch-fleet at ts
`1789097484.647639`; the `ops.md` §4 window opened then, ran its 30 minutes, and closed with no
objection.
**Source:** `tasks/core/025-nrf54l-name-matcher-in-flash-backend-is-a-second-independent-classifier.md`
— closing that task's decision (`embarch-core` decision 49) found the seam
this task is filed against.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-core/src/flash_backend.rs`'s `requires_vendor_tool` and
`embarch-topology/src/hardware/hardware_id.rs`'s `classify_chip` both match
Nordic chip names (`nrf54l`/`nrf54h`) by prefix, independently, and already
agree on where the family boundary sits (both stop at nRF54L; both refuse
nRF54H rather than guess). `embarch-core` already depends on the
`embarch-topology` crate (`Cargo.toml`, `hardware` feature) — but
`classify_chip` and the `ChipFamily` enum are a private `fn`/type inside
`hardware_id.rs`, not re-exported from `embarch-topology::hardware`
(`hardware/mod.rs`'s `pub use` list only carries `compare_self_reported` and
`SelfReportedIdentity`). So today, sharing one answer is not just a Cargo.toml
edit — it needs `embarch-topology` to decide what to expose and export it.

The seam to cut, if this is worth doing: `embarch-topology` exposes a public
family judgment — either `classify_chip` and `ChipFamily` themselves, or a
narrower `pub fn is_nrf54l(chip: &str) -> bool` / equivalent — that
`embarch-core`'s `flash_backend.rs` calls instead of maintaining its own
`starts_with` match. That would make one rule instead of two agreeing rules,
at the cost of `flash_backend.rs` depending on a type whose home is the
board-identity/enrollment problem, not the flashing-backend problem — a
coupling `embarch-topology`'s owner should judge, not something to do
unilaterally from `embarch-core`'s side.

**Not required**: the two matchers agree today and each has its own tests
pinning that agreement (`embarch-core` decision 49, topology decision 25).
This is a "worth considering" finding, not a defect.

## Why now

`topology/007` fixed a chip-name-matching bug in `hardware_id.rs` and its
reviewer caught an unevidenced nRF54H guess in the fix; `core/025` found and
fixed the same shape of gap in `flash_backend.rs` (an nRF54H name silently
fell through to "no vendor tool needed" rather than a named refusal). Two
independently-written, independently-tested rules for the same family
boundary, agreeing so far by care rather than by construction, is worth a
suite-scoped owner's judgment on whether it is worth becoming one rule.

## Done when

- [ ] `embarch-topology`'s owner decides whether to export a shared family
      classifier, and if so, what shape.
- [ ] If adopted: `embarch-core`'s `flash_backend.rs` calls it instead of its
      own `starts_with` match, and `embarch-core` decision 49 is updated or
      retired to say so.
- [ ] If declined: a one-line note in `embarch-topology`'s or `embarch-core`'s
      decisions saying so, so this does not get re-discovered as a fresh
      finding next time someone touches either file.
