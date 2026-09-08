# 025 — Settle whether `flash_backend`'s nRF54L match stays its own classifier

**State:** done
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

- [x] `embarch-core/decisions/` carries a numbered decision that states which
      way this went and the evidence behind it — including, if the answer is
      "keep them separate", what is and is not known about nRF54H's RRAM.
      Decision 49 (`decisions/flashing.md`): kept as two independent
      matchers — a shared one needs `embarch-topology` to export a currently
      private `classify_chip`, which is topology's call — and states plainly
      that nobody here owns an nRF54H part and nothing establishes its
      RRAM/erase-write story either way.
- [x] `flash_backend.rs`'s match arm and its tests agree with that decision,
      including case handling, and a name that matches nothing still reaches the
      named refusal rather than a silent default. `requires_vendor_tool` now
      matches `nrf54h` (case-insensitive, any suffix) the same way it already
      matched an unrecognized `nrf54l` name, so it reaches the named refusal in
      `discover` instead of silently permitting probe-rs. New tests:
      `an_nrf54h_name_is_refused_too_case_and_suffix_insensitive`,
      `the_nrf54h_refusal_reason_makes_no_rram_claim`.
- [x] Any cross-repo half is an `inbox/` drop, not an edit.
      `inbox/suite-share-nordic-chip-family-classifier-between-core-and-topology.md`
      (not committed — inbox is gitignored by design).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo clippy --all-targets -- -D warnings` and
      `scripts/check-ownership.py --scope core`. `cargo build`/`cargo test`
      (169 passed)/`cargo clippy --all-targets -- -D warnings` all clean in
      the code worktree; `check-docs.py` all 10 checks green in the doc
      worktree; `check-ownership.py --scope core` (doc worktree) and
      `--scope core --code-repo` (code worktree) both OK;
      `check-client-names.py --repo <code worktree>` clean.
- [x] `spec.md`/`decisions.md`/`open.md` updated as they need it,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level this made false. `decisions.md` index and
      `decisions/flashing.md` updated; `spec.md`'s existing
      `flash_backend.rs` row (decision 36) still holds, no edit needed;
      `open.md` deliberately left untouched — it is already in reserve
      (642 B left, filed against blocked `022`) and nothing here left an
      open question that wasn't already fully resolved by decision 49 itself,
      so touching it would only have spent reserve for no new unresolved
      fact. No suite-level doc's claims changed, so no `status.d/` fragment.

## Blocked

Not blocked — done. One residual gap, tracked, not fixed here: the header
comment atop `flash_backend.rs` still says "design.md §3 decision 48", a
stale pre-restructure reference (no decision 48 exists in `decisions.md`
today, and grep finds it nowhere else). Pre-existing, unrelated to this
task's scope, and untouched.
