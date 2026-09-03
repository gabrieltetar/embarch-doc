# 002 — The crate's own test suite cannot run at default stack size

**State:** done on agent/study-designer/002-test-harness-stack-overflow, 2026-09-02 — pushed, not merged.
**Source:** surfaced by task 001's worker, 2026-09-03, and independently reproduced on `main` at `2a136be`.
**Scope:** study-designer
**Hardware:** none

## What

`cargo test` aborts on `main`, untouched:

```
thread 'tests::dev_bench_message_discriminants_are_pinned' has overflowed its stack
fatal runtime error: stack overflow, aborting   (SIGABRT)
```

`RUST_MIN_STACK=33554432 cargo test` passes **107/107**. So this is libtest's
default 2 MiB per-test-thread stack against this crate's large inline result
types — the same class of failure [decisions/limits.md](../../embarch-study-designer/decisions/limits.md)
decision 49 records `embarch-core` solving with a 64 MiB thread stack. Nothing
does the equivalent for the test harness.

## Why now

**It makes the merge gate structurally unenforceable for this crate.** §10 says a
red gate means a branch does not land; with `cargo test` red on `main`, every
future study-designer branch either lands on a red gate by exception — which is
what happened for task 001 — or nothing lands at all. Neither is acceptable as a
standing state.

## Done when

- [x] `cargo test` passes from a clean checkout with no env var set.
- [x] The fix is a stated decision, not a workaround: `.cargo/config.toml`
      setting the harness stack, boxing the offending value in the test, or
      shrinking the type. Record which and why in `decisions.md` — decision 49
      is the precedent to reference.
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`.
- [x] `changelog.d/study-designer-<slug>.fixed.md` dropped.

## What shipped

`.cargo/config.toml` in the crate sets `RUST_MIN_STACK=67108864`, plus a ceiling
test on the `no_std` `DevBenchMessage` so unbounded growth fails as a named
assertion rather than a SIGABRT. Recorded as decision 63 in
[decisions/limits.md](../../embarch-study-designer/decisions/limits.md).

**The type is oversized and stays that way, deliberately.** `cargo test` builds
*default* features — the allocator-free shape dev-bench links — where
`DevBenchMessage` is 75,288 bytes against 2,128 under `alloc`. Shrinking it
reverses decision 15 for the one build with no allocator, and
`the_no_std_build_keeps_its_fixed_capacity_arrays` already forbids it. Decision
63 says so in full rather than letting the config file imply the problem is
solved.

No hardware verification debt: this is host-side only.
