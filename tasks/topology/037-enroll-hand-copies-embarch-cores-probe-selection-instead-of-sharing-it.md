# 037 — `validate::enroll`'s probe selection is a copy of `embarch-core::resolve_probe`, not a share

**State:** open
**Source:** `inbox/topology-enroll-duplicates-core-probe-selection.md`, dropped by `tasks/core/053`'s
worker while rewording `embarch-core/src/hardware.rs`'s `resolve_probe` doc comment. Filed by the
leg of 2026-09-13 17:0x.
**Scope:** topology
**Hardware:** none — a code-structure observation and a documentation call; nothing is executed.
**Owner:** no

## What

`embarch-core`'s `resolve_probe` (`src/hardware.rs`) is `pub(crate)` — unreachable from outside
that crate. Before `embarch-core` decision 22 moved the board-identity gate wholesale into
`embarch_topology`, that did not matter: `board_gate.rs` lived inside `embarch-core`, so
`resolve_probe` really was the one implementation behind both the enforce path (flash/reset) and
the enroll path.

After the move, `embarch_topology::hardware::validate::enroll` (`src/hardware/validate.rs`, near
line 327) carries its own inline probe-selection block — `Lister::new()`, `list_all()`,
find-by-serial, else bail if `len() != 1` — structurally the same rule, hand-written a second time
in a different crate. `pub(crate)` cannot cross that boundary, so the move silently turned one
shared implementation into two independently maintained ones. `core/053` verified this against
`embarch-topology/src/hardware/validate.rs` itself; its worker could not act on it, because a
`core` worker may not write `embarch-topology`.

**Verify both sites still read that way before acting** — the drop is a day old at most, but the
claim is the whole task.

## Why now

This is the exact drift shape `embarch-core` decision 9 already paid for: an implementation
described as the one source of truth quietly stops being that, and nothing fails until the copies
disagree (there, "single-probe-only" survived months until a real second probe exposed it). The
`core` side's comment has now been reworded to stop claiming a share it does not have, which
removes the only written trace that the duplication exists at all.

## Done when

- [ ] Decide, and say why in the commit: document the duplication, or de-duplicate it. Documenting
      it means a numbered decision in `embarch-topology`'s decisions, cross-referencing
      `embarch-core` decision 9's drift class. De-duplicating means a `pub` helper or shared home —
      **but note `embarch-topology` is a dependency of `embarch-core`, not the other way round**,
      so "re-export `embarch-core`'s helper" is not available; check the direction before choosing.
- [ ] If documented rather than de-duplicated, the note names **both** call sites
      (`embarch-core::resolve_probe`, `embarch_topology::hardware::validate::enroll`) so a search
      for either finds the other.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/topology-*` fragment; `open.md` updated if the decision leaves a question open.
