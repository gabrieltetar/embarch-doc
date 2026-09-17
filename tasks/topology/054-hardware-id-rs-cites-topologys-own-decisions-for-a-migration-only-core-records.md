# 054 — `hardware_id.rs`'s header cites topology's own decisions 2, 4 for a migration only `embarch-core` decision 22 records

**State:** done — leg 132 unit 2, 2026-09-17, `agent/topology/054-hardware-id-citation`
**Source:** `topology/053` (leg 131, 2026-09-17), noticed while fixing the sibling
defect in `validate.rs:1-3`. Not fixed there because that task's scope was
exactly one line (`board_gate.rs`'s citation) and explicitly said not to sweep
the crate.
**Scope:** topology
**Hardware:** none — one doc comment. Nothing is built for a board, no probe,
no live Core.
**Owner:** no

## What

`src/hardware/hardware_id.rs:1-6` opens:

> Vendor-specific, per-chip-family readback of a target's factory-burned
> unique ID — the live signal [`super::validate`]'s board-identity check
> cross-checks against [`super::enrollment`], since it survives a probe
> getting physically moved to a different board in a way a bare USB serial
> number can't. Formerly `embarch-core`'s own `hardware_id.rs`, moved here
> unchanged (decisions 2, 4).

Same shape of defect as `topology/053` (`validate.rs`) and `topology/052`
(`enrollment.rs`): the citation is bare, so both numbers read as this crate's
own, and neither actually narrates this file's migration.

- **Decision 2** (`embarch-topology/decisions/crate.md`) describes the crate's
  current shared-library architecture generally. It says nothing about
  `hardware_id.rs` or anything having moved out of `embarch-core`.
- **Decision 4** (`embarch-topology/decisions/consumer-boundary.md`, "Both
  software and hardware topology, in one pass, not hardware-first") lists what
  moved into this crate's scope by name: "the board-identity gate, its
  storage, the dev-bench port heuristic, and the software-class detection."
  That is a forward-looking scope decision, not a provenance record — it does
  not say "formerly `hardware_id.rs`" or give a reason, and it does not name
  the chip-ID-readback mechanism specifically.

The decision that does record this file's specific history is **`embarch-core`
decision 22** (`embarch-doc/embarch-core/decisions/probes.md`), which
describes the exact mechanism verbatim: *"a machine-local table keyed by
probe serial, holding the chip's own factory-burned ID **read live over the
debug port**"* — `hardware_id.rs`'s own docstring is almost the same sentence
— and then *"**Moved wholesale into `embarch-topology`**, because the
stale-serial incident that motivated that crate *is* this mechanism's own
override path going stale."* That is the same decision 22 that `topology/053`
used to fix `validate.rs`'s identical defect (`board_gate.rs` is part of the
same "probe/board identity gate" bundle decision 22 describes as moving
wholesale).

`port.rs`'s neighbouring "formerly `embarch-core`'s own `dev_bench.rs`"
citation (also `decisions 2, 4`) was checked too and is **not** a defect:
decision 4 names "the dev-bench port heuristic" specifically, and no
`embarch-core` decision documents that migration by name — so decision 4 is
the correct, and only, provenance record available for that one.

## Why now

Same crate, same sentence shape, same wrong-attribution pattern the two
already-fixed siblings (`enrollment.rs` via `topology/052`, `validate.rs` via
`topology/053`) share. Leaving it findable-but-unfixed is exactly the
asymmetry `topology/053`'s own "Why this one is worth a unit" section
describes from the other side.

## Done when

- [x] The header's citation is split so the "formerly `embarch-core`'s own
      `hardware_id.rs`" clause cites `` (`embarch-core` decision 22) ``,
      matching `enrollment.rs:3`'s and `validate.rs:1-3`'s shape.
- [x] Gate green (`../../../embarch-fleet/protocol.md` §10): `cargo build
      --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-topology`; `check-docs.py` in `embarch-doc`.
- [x] `changelog.d/` fragment.

## Not yours (for whoever picks this up)

Do not amend `embarch-core` decision 22 or `embarch-topology` decision 2 or
decision 4 — all three are correct as written; only the comment's attribution
is wrong. Do not turn this into a crate-wide single-line citation sweep: that
surface was swept by `topology/040` and `046` and re-swept by `050`.
