# 002 — The crate's own test suite cannot run at default stack size

**State:** open
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

- [ ] `cargo test` passes from a clean checkout with no env var set.
- [ ] The fix is a stated decision, not a workaround: `.cargo/config.toml`
      setting the harness stack, boxing the offending value in the test, or
      shrinking the type. Record which and why in `decisions.md` — decision 49
      is the precedent to reference.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`.
- [ ] `changelog.d/study-designer-<slug>.fixed.md` dropped.
