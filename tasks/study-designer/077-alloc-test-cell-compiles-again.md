# 077 — The `alloc` test cell compiles again

**State:** open
**Source:** found by the `study-designer/075` worker on 2026-10-26 and confirmed by the supervisor on `main` at `3ec19b9`, before 075 landed: `cargo test --no-default-features --features alloc` fails with four `cannot find macro vec in this scope` errors in `src/host_study.rs`'s tests. That file arrived with `study-designer/070` (`ba3ad46`).
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`.github/workflows/test.yml` runs `cargo test --locked --no-default-features --features alloc` (line 101), so CI on `main` is red on that cell today. Under `alloc` without `std` the prelude has no `vec!`; the tests need `alloc::vec!` (or the crate's existing `alloc` import pattern), or the test module needs the same `cfg` gate its neighbours use. Fix the tests, not the CI cell.

## Done when

- [ ] `cargo test --no-default-features --features alloc` passes, and every other cell in `test.yml` still does.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment.
