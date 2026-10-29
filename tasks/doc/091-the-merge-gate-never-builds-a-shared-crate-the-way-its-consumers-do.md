# 091 — The merge gate never builds a shared crate the way its consumers do

**State:** done — `gate.md` gates a shared crate once per feature set its consumers' manifests name (one grep, no list); replayed `topology/063`, which that set catches; fleet 19b61cd.
**Source:** the 2026-10-26 03:00 leg, `topology/065`. `topology/063` landed green on its own gate
(default features and `--all-features`) and broke every consumer that builds topology with
`default-features = false, features = ["software", "wire"]`: `embarch-api`'s
`embarch-core-client`, `embarch-ui` and `embarch-umbrella` were red on `main` for one leg. Three
workers found it independently, each worked around it differently (a feature flag, a HEAD~1 copy),
and one task (`core/110`) bounced.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is a bullet in `embarch-fleet/gate.md` (and possibly
`.claude/leg.md`), both owner-reserved.

## What

`gate.md` says to read the diff before merging a shared crate (`embarch-study-designer`,
`embarch-topology`, `embarch-core-client`) and to run `cargo build`/`test`/`clippy` "in the touched
repo". For a crate with feature-gated halves, neither default features nor `--all-features` is the
set a consumer compiles, so an item that is `hardware`-only but re-exported unconditionally passes
both and fails every non-`hardware` consumer. `topology/065` wrote the `software,wire` set into
topology's `Cargo.toml` feature comment as a gate item, which a worker reads only if it opens that
file; the supervisor's re-run follows `gate.md`, which does not name it.

Two shapes, the owner's call: name each shared crate's consumer feature sets in `gate.md` (topology:
`--no-default-features --features software,wire`; check study-designer's `alloc`/`std` split the
same way), or make the supervisor's re-run of a shared-crate unit also `cargo build` its consumers
against the merge result, which catches every such case without a list.

## Done when

- [x] `gate.md` says how a shared-crate unit's gate covers the feature sets its consumers use.
