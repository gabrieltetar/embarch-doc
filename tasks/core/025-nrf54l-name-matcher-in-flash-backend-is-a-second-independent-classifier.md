# 025 — Settle whether `flash_backend`'s nRF54L match stays its own classifier

**State:** open
**Source:** `inbox/core-unify-nrf54l-name-classifier-with-topology.md`, filed by
`topology/007`'s worker — fixing topology's own chip classifier surfaced that
`embarch-core/src/flash_backend.rs` makes a related decision about the same
silicon family from a separately-maintained match arm
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/src/flash_backend.rs`'s `requires_vendor_tool` decides whether a
chip needs the vendor RRAM tool rather than probe-rs's flat-NVM erase/write,
using `chip.to_ascii_lowercase().starts_with("nrf54l")`.
`embarch-topology/src/hardware/hardware_id.rs` now has `classify_chip`
(topology decision 25, landed 2026-09-07) deciding which `FICR` register pair
holds a part's device ID, from a rule that covers `nrf54l` **and explicitly
refuses `nrf54h` as unevidenced**.

The two answer different questions about the same family and were never derived
from one place. **Decide, in `embarch-core`, and write the decision down**:

- keep two independent matchers, and record *why* `nrf54h` is out of scope for
  the vendor-tool question — is its RRAM story different, or is its absence an
  accident nobody has examined? **If the honest answer is "nobody knows", say
  that**: an unevidenced claim about a part nobody here owns is exactly what
  topology/007 had to retract, and the same standard applies here; or
- adopt a shared answer, which needs a dependency `embarch-core` does not have
  today.

**If you conclude a shared classifier is the right shape, that is a finding, not
a change to make.** It spans two repos, so it is `suite`-scoped work
(`../../embarch-fleet/protocol.md` §8) and you would be reaching outside your
ownership row. Write it into `inbox/` with the seam you would cut, and land the
`embarch-core`-only half of the decision here.

**`embarch-topology/src/hardware/hardware_id.rs` is a read.** It is the evidence
for what the family rule looks like elsewhere in the suite; it is not yours to
write.

## Why now

`topology/007` fixed the hardware-id side of this exact shape of bug — a chip
name one character or one case off an exact-match list silently taking the wrong
branch — and its reviewer then caught a second unevidenced guess inside the fix.
`flash_backend.rs`'s own test `an_unknown_nrf54l_part_is_still_refused` shows
its author already reasoned about this case, so the question is whether the two
rules are deliberately different or accidentally so, and nothing on disk says.
Getting it wrong in this file means flashing a Nordic RRAM part with probe-rs,
which the suite has a standing rule against.

## Doc-size reserve for `core`

- `embarch-core/open.md` — 4478/5120 B, **642 B left**, filed against
  `tasks/core/022-compact-core.md`, which is **blocked**. If your work spends
  that reserve or leaves it spent, `DOC-COMPACTION.md` §2's ride-along applies:
  compact `open.md` as part of this unit, carrying `022`'s `Must not delete:`
  list and closing only that file's item. A verbatim mission split is the
  cheaper move where a seam exists.
- Nothing else in `core` is in reserve.

## Done when

- [ ] `embarch-core/decisions/` carries a numbered decision that states which
      way this went and the evidence behind it — including, if the answer is
      "keep them separate", what is and is not known about nRF54H's RRAM.
- [ ] `flash_backend.rs`'s match arm and its tests agree with that decision,
      including case handling, and a name that matches nothing still reaches the
      named refusal rather than a silent default.
- [ ] Any cross-repo half is an `inbox/` drop, not an edit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo clippy --all-targets -- -D warnings` and
      `scripts/check-ownership.py --scope core`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated as they need it,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level this made false.
