# 065 — The `wire`-only build compiles again, and `enroll_reporting` is reachable from `hardware`

**State:** open
**Source:** three inbox drops from the 2026-10-26 leg's workers, merged into one task by the
supervisor: `topology-software-feature-build-breaks.md` (ui/090 worker),
`topology-upserted-reexport-breaks-default-build.md` (umbrella/091 worker) and
`topology-reexport-enroll-reporting.md` (core/110 worker, blocked on it). All three trace to
`topology/063` (`6732ad6`, decision 42).
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

Two defects in what `topology/063` landed, both in `src/hardware/mod.rs`.

1. **A consumer without `hardware` does not compile.** `mod.rs:33` re-exports
   `enrollment::Upserted` unconditionally, but the struct (`src/hardware/enrollment.rs` ~:297) is
   behind `#[cfg(feature = "hardware")]`. `embarch-api`'s `embarch-core-client`
   (`default-features = false, features = ["software", "wire"]`), `embarch-ui` and
   `embarch-umbrella` all fail with `error[E0432]: unresolved import enrollment::Upserted`, measured
   by three workers on 2026-10-26. `93a83d9` (HEAD~1) builds. `topology/063`'s gate ran default
   features and `--all-features`; neither combination is the one these consumers use, so nothing
   caught it. Gate the re-export (or the struct) consistently, and make the `wire`-only build part of
   this crate's own gate so it cannot recur: a test, a CI line, or at minimum a sentence in the
   crate's docs that names `cargo build --no-default-features --features software,wire` as a gate
   item.
2. **`enroll_reporting` is unreachable.** `validate::enroll_reporting` is `pub` inside the private
   `mod validate`, and the public wrapper `hardware::enroll` (~:177) still calls `validate::enroll`
   and discards the report. Decision 42 and `topology/063`'s log entry both describe
   `enroll_reporting` as additive public API, so the code is what is wrong. Add
   `hardware::enroll_reporting` next to `hardware::enroll`, same signature as
   `validate::enroll_reporting`, returning `(EnrolledBoard, Upserted)`, behind `hardware`.

## Why now

Every `embarch-api`, `embarch-ui` and `embarch-umbrella` build against topology `main` is red, so
no consumer unit can pass the merge gate cleanly, and `tasks/core/110` is blocked on item 2.

## Done when

- [ ] `cargo build` and `cargo clippy --all-targets -- -D warnings` are green in `embarch-topology`
      for default features, `--all-features`, and `--no-default-features --features software,wire`.
- [ ] `embarch_topology::hardware::enroll_reporting` exists, is documented, and is behind
      `hardware`.
- [ ] The `wire`-only build is named as a gate item where the next topology worker will read it.
- [ ] Decision 42 still matches the code (amend only if it does not); `changelog.d/` fragment.
