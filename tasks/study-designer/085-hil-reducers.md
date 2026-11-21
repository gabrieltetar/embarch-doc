# 085 — The shared crate's built-in HIL reducers, each with a contract, a fixture and a `U` rule

**State:** claimed by agent/study-designer/085-hil-reducers, 2026-11-21 12:10
**Source:** Fleet Ready issue: the shared crate has no built-in reducers, so nothing computes a derived measurement and `verify` has nothing to recompute it with. `notes/hil/14-implementation-plan.md`, unit M1.2 (after M1.1, landed as `tasks/study-designer/084`); `notes/hil/02-study.md`, "Measurements".
**Issue:** EMB-217
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

The built-in reducers in the crate's host-only half: **count, rate, min, max, mean, percentile, the interval between two markers, and the value at a marker.** Each has a stated contract (its inputs, its output unit, how it reports incomplete input), a fixture of its own, and a `U` rule as `notes/hil/02-study.md` states it: an interval combines the two stamps' `U` and the clock's by root sum of squares; a mean takes its inputs' `U` undivided; a count has none; **a statistical reducer (mean, rate, percentile) also returns its type-A term**, the standard uncertainty of its own estimate from the samples' spread, combined with the instrument term by root sum of squares.

**Versioned by behaviour**: each reducer carries an integer behaviour version, bumped only when a result can change, and the crate keeps every behaviour it has shipped, so a reader can ask for the behaviour a record names. The output is the `value`, `unit`, `uncertainty` (with `type_a`), `u_source`, `method` (`{kind: "reducer", name, behaviour, window}`) and `incomplete` of one measurement as `interfaces/hil-shapes.md` fixes them.

## Why now

M1.7 (Core writing `measurements.json` as each study ends) and M1.11 (`verify` recomputing it) both need these, and M1.7 is on milestone 1's critical path.

## Dispatch notes

- **Write against `embarch-study-designer/interfaces/hil-shapes.md` and decisions 90 and 91 (`decisions/hil-shapes.md`)** as `study-designer/084` left them. Where this unit has to change a shape (the `Unit` list, `window`'s keys), amend that doc in the same commit; do not leave a second description of the shape.
- **The crate is `no_std` and has four consumers building it four ways**: `embarch-core` with `std`, `embarch-api` and `embarch-core-client` with `alloc`, `embarch-ui` with `study-ui`/`gatt-extract`/`eap-parse`, and `embarch-dev-bench`'s firmware with no features and no allocator. The reducers go behind a feature (name and whether it needs `std` or only `alloc` are this unit's decision, recorded as one), so every existing consumer builds unchanged. `embarch-api` will need to link them for `verify`, so say in the decision which feature it turns on.
- **Decisions near their size limit** (`check-doc-size.py --pressure`): `versioning` #12 has 67 B left and is pinned, `streams` #39 64 B, `seals` #17 72 B. Behaviour versioning is a new decision in a new or HIL topic file, not an amendment of #12.
- Out of scope: Core calling the reducers (M1.7), the verdict rules (`study-designer/086`, M1.3), the excursion-count reducer of `notes/hil/13-research-phase.md` (not in M1.2's list).

## Done when

- [ ] `cargo test` passes against each reducer's fixture with no Core installed.
- [ ] A reducer over incomplete input (a truncated capture, a record gap) reports it in `incomplete`, and a test shows a behaviour change bumps the version while the old behaviour stays callable.
- [ ] Each statistical reducer's fixture checks its `type_a` term.
- [ ] `spec.md`, `decisions/`, `interfaces/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the shared-crate bullet: once per feature set its consumers build it with; `check-ownership.py --scope study-designer` on both branches).
