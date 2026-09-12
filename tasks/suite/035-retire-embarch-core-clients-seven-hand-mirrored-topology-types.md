# 035 — retire `embarch-core-client`'s seven hand-mirrored `embarch-topology` types, now that the types are reachable

**State:** open — announced, awaiting its silence-as-consent window.

**Announcement window (leg 101, 2026-09-12):** posted to `#embarch-fleet` at `ts 1789232916.230899`,
opened **11:08 local**. Closes **11:38**. No `--action`, per `ops.md` §4 — silence is consent. If
this leg ends before 11:38, **the next leg completes this window rather than restarting it**: poll
`scripts/fleet-read.py --thread 1789232916.230899`, and if nothing objected and 30 minutes have
passed, run it. A reply saying go runs it immediately; a cancel drops this task back to plain `open`
with the reply quoted here.

**Leg 101 note on where to run it:** in its own `embarch-api` worktree, never the main checkout.
Leg 100's entry flagged that a `suite` task editing a linked crate in the main checkout put a
half-applied edit into three concurrent workers' builds. `embarch-api` is a sibling-symlink target
for `embarch-ui` worktrees, so this task has exactly that hazard.

**Source:** the second half of `tasks/suite/020`, split out by leg 100 on 2026-09-12 after its first
half landed. `020`'s own scoping section (written by leg 099) is the long-form version of everything
below; read it in the git history of `tasks/suite/020-topologys-hardware-feature-gate-forces-seven-mirrored-types.md`.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-topology` decision 31 (landed 2026-09-12) added a `wire` feature: `serde` only, no
`probe-rs`, no `serialport`, no C toolchain, and `hardware` implies it. `EnrolledBoard`, `Alert`,
`DetectedPort`, `SignalLink`, `Route` and `SignalDirection` are now reachable by a crate that must
never link probe-rs — which is exactly what `embarch-api/crates/embarch-core-client` is.

That crate still hand-mirrors all seven at `client.rs:273, 293, 320, 333, 346, 365, 501`, with
comments at `:269` and `:1589` explaining that the real types are unreachable. **They are reachable
now.** This unit is the switch-over.

## Why it is its own unit, and why it is the risky half

- The mirrors are not plain duplicates. They are `*Response` types with their own contracts, and
  some have drifted — `EnrolledBoardResponse` has already dropped `link_port_interface`, which is
  what `tasks/api/032` exists to paper over.
- `client.rs:1875-2126` is a block of **deliberate mirror-pinning tests** (`api/032`'s work) whose
  whole purpose is to catch the drift this change removes structurally. Retiring the mirrors means
  retiring those tests, and that should be a stated decision, not a side effect of a refactor.
- `embarch-core-client` is a **shipped crate**. Replacing a locally-defined public type with a
  re-exported one from another crate changes its public API for anyone depending on it.
- `client.rs` is 2,357 lines.

## Done when

- [ ] `embarch-core-client` depends on `embarch-topology` with `default-features = false,
      features = ["wire"]` and uses its types for enrolled boards, alerts, signal links, routes and
      detected ports.
- [ ] `cargo tree -e normal` shows no `probe-rs` and no `serialport` in `embarch-api`,
      `embarch-ui` or `embarch-umbrella`. **Check all three**, not just the crate being edited.
- [ ] No hand-maintained mirror of an `embarch_topology::hardware` type remains, or the one that
      does says in a comment why it is not the same shape.
- [ ] The retirement of `client.rs:1875-2126`'s mirror-pinning tests is recorded as a numbered
      `embarch-api` decision naming what used to guard this and what guards it now (the compiler).
- [ ] `tasks/api/032` is re-read and either closed or narrowed to the `link_port_interface` field
      itself — `020` said this unit makes most of it unnecessary.
- [ ] `embarch-topology` decision 4's and decision 8's 2026-09-12 qualifications are updated: both
      currently say in so many words that they are *still not true as written* until this lands.
- [ ] Gate green; `changelog.d/` fragments for both repos.

## Read before dispatching

This is a `suite` task because it spans `embarch-api` and `embarch-doc` and changes a shipped public
API — `ops.md` §4's announcement window applies. The `embarch-topology` side is already done and
needs no further change.
