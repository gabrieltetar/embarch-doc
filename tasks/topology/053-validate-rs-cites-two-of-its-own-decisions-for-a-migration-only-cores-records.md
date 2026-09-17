# 053 — `validate.rs`'s header cites two of this crate's own decisions for a migration only `embarch-core` records

**State:** done — leg 131 unit 1, 2026-09-17, `agent/topology/053-validate-rs-migration-citation`
**Source:** `topology/052`'s reviewer, leg 130, 2026-09-16, filed as
`inbox/topology-validate-rs-1-2-citation.md` and drained here. The `052` worker flagged the line and
**correctly left it alone** — its task was scoped to wrapped citations and this one is single-line —
so this is a real finding rather than a scope failure. The supervisor re-verified every claim below
against the three decision bodies and the source line before filing.
**Scope:** topology
**Hardware:** none — one doc comment. Nothing is built for a board, no probe, no live Core.
**Owner:** no

**Doc-size reserve for `topology`: nothing.** No `embarch-topology/*` doc is inside the last 10% of
its cap (`scripts/check-doc-size.py --pressure`, 2026-09-16). If your work pushes one into reserve,
file `tasks/topology/<NNN>-compact-topology.md` in the same commit.

## What

`src/hardware/validate.rs:1-3` opens:

> Live board-identity validation — formerly `embarch-core`'s own
> `board_gate.rs` (decisions 2, 8). One implementation,
> multiple call sites: …

The citation is bare, so both numbers read as **this crate's own**. One of them is right and one is
not:

- **Decision 8** (`embarch-topology/decisions/consumer-boundary.md`, *"One implementation, multiple
  call sites — not two independent layers"*) supports the sentence that **follows** the
  parenthetical, near-verbatim. Keep it.
- **Decision 2** (`embarch-topology/decisions/crate.md`, *"A shared crate `embarch-core`,
  `embarch-api` and `embarch-umbrella` all link and call in-process"*) describes the crate's current
  architecture and **says nothing about `board_gate.rs`, and nothing about anything having moved out
  of `embarch-core`.** Nothing in this crate's own decisions records that history.

The decision that does record it is **`embarch-core` decision 22**
(`embarch-doc/embarch-core/decisions/probes.md`), whose own text says *"**Moved wholesale into
`embarch-topology`**, because the stale-serial incident that motivated that crate *is* this
mechanism's own override path going stale."* That is `board_gate.rs`'s migration, named and
attributed, and as a cross-repo citation it needs the `` `embarch-core` `` label.

## Why this one is worth a unit

**`topology/052` fixed the structurally identical defect one file over** — `hardware/enrollment.rs:3`
cited a bare `(decisions 2, 3, 7)` for *"formerly `embarch-core`'s own `known_boards.rs` /
`known_boards.toml`"* and now cites `` (`embarch-core` decision 22) ``. Two sibling files, the same
"formerly Core's own X" sentence, the same wrong attribution, and **only one of them was in a
sweep's scope**, because one wrapped across a line and the other did not. That asymmetry is the whole
reason `tasks/doc/071` exists, seen from the other side.

## Done when

- [x] The header's citation is split so the "formerly `embarch-core`'s own `board_gate.rs`" clause
      cites `` (`embarch-core` decision 22) `` and the "One implementation, multiple call sites"
      clause keeps decision 8. How it reads as prose is your call — match `enrollment.rs:3`'s shape
      if that reads well.
- [x] Say in your report whether **any other** bare `(decisions …)` in this crate attributes a
      migration to a decision that does not describe one. Do not sweep the crate; just say what you
      noticed while you were in the file.

      Checked every "formerly `embarch-core`'s own X" doc comment in `src/`: `enrollment.rs` (fixed
      by `topology/052`), `validate.rs` (this unit), `port.rs`, and `hardware_id.rs`.

      **`port.rs:1-3`** cites `(decisions 2, 4)` for "formerly `embarch-core`'s own `dev_bench.rs`" —
      **not a defect**. Decision 4 (`consumer-boundary.md`) names "the dev-bench port heuristic"
      moving into this crate specifically, and no `embarch-core` decision documents that migration by
      name, so decision 4 is the right and only provenance record available.

      **`hardware_id.rs:1-6`** cites `(decisions 2, 4)` for "formerly `embarch-core`'s own
      `hardware_id.rs`, moved here unchanged" — **same defect as this unit's own finding.** Decision 4
      is a forward-looking scope decision that doesn't name this file or narrate why; the real
      provenance record is `embarch-core` decision 22, whose own text ("a machine-local table keyed
      by probe serial, holding the chip's own factory-burned ID read live over the debug port …
      Moved wholesale into `embarch-topology`") describes `hardware_id.rs`'s exact mechanism, almost
      verbatim against its own docstring. Left unfixed per this task's own scope and filed as an inbox
      drop rather than swept: `/home/gabriel/Github/embarch/embarch-doc/inbox/topology-hardware-id-rs-migration-citation.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10): `cargo build --all-targets`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` in `embarch-topology`; `check-docs.py` in
      `embarch-doc`.
- [x] `changelog.d/` fragment.

## Not yours

Do not amend `embarch-core` decision 22, `embarch-topology` decision 2 or decision 8 — all three are
correct as written; only the comment's attribution is wrong. Do not turn this into a crate-wide
single-line citation sweep: that surface was swept by `topology/040` and `046` and re-swept by `050`,
and re-doing it is not what this task is for.
