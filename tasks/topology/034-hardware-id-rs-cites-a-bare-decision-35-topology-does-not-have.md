# 034 — `hardware_id.rs:429` cites a bare `decision 35`; `embarch-topology` has no decision 35

**State:** open
**Source:** leg 099's refill sweep, 2026-09-12. Verified by reading both sides.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/src/hardware/hardware_id.rs:429`:

> `// The whole point of decision 35: the runtime serial link and the JTAG connection are physically separate USB devices`

A **bare** `decision N` means same-repo, per the citation form settled in `api/052`. But
`embarch-doc/embarch-topology/decisions.md`'s group table enumerates every decision this repo has
and **stops at 30** — there is no topology decision 35. The decision that actually says this is
`embarch-core` decision 35 (`embarch-doc/embarch-core/decisions.md` lists it under
`decisions/handshake.md`), and **the same file already cites it correctly** at `hardware_id.rs:161`:
`` (`embarch-core` decision 35) ``. So one line of this file gets the form right and another gets it
wrong, about the same decision.

Two nearby look-alikes were checked and are **correct** — do not touch them:

- `hardware_id.rs:70`, "its decision 49" — `embarch-core` 49 exists, in `decisions/flashing.md`
  (moved to `decisions/flash-backend.md` by `core/035`, 2026-09-12; the bare number is stable across
  the move, only a path citation would have broken).
- `enrollment.rs:37`, `` `embarch-core` decision 21's port migration `` — core 21's body does say
  "Resolved by moving the link to the board's second, dedicated UART port".

## Why now

The mirror image of `tasks/ui/038`, which is the same defect in the other direction. A bare number
that silently resolves to the wrong repo is worse than a broken link: nothing fails, and a reader
who goes looking finds a decision table that stops short and concludes the citation is simply stale
rather than cross-repo.

## Done when

- [ ] `hardware_id.rs:429` reads `` `embarch-core` decision 35 ``.
- [ ] `grep -rnE "decisions? (3[1-9]|[0-9]{2,})" ` over `embarch-topology`'s `src/`, `bin/` and
      `Cargo.toml` shows only repo-qualified hits — any bare number above 30 is the same defect.
- [ ] `cargo test -p embarch-topology` green.
