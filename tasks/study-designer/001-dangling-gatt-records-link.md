# 001 — A rustdoc link points at a constant that no longer exists

**State:** claimed by agent/study-designer/001-dangling-gatt-records-link, 2026-09-02 21:39
**Source:** [embarch-study-designer/open.md](../../embarch-study-designer/open.md) — "`MAX_GATT_ACTIVITY_RECORDS` was never sized against live notification traffic — and it never will be: decision 54 retired the field it bounded."
**Scope:** study-designer
**Hardware:** none

## What

`MAX_GATT_ACTIVITY_RECORDS` is **not defined anywhere in the crate** (verified
2026-09-03 — it is absent from `limits.rs`), yet three sites still name it:

- `src/gatt.rs:138` — an intra-doc link `[crate::limits::MAX_GATT_ACTIVITY_RECORDS]`
  to a symbol that does not exist. This is a **dangling rustdoc link**, not prose.
- `src/gatt.rs:51` and `src/result.rs:180` — comments describing the retired cap
  as though it still applies.

Resolve all three so the code says what is true, and close the stale open
question that has been tracking a constant its own subject removed.

## Why now

Small, entirely host-side, and verifiable: a dangling intra-doc link is a real
defect a doc build can catch, and the open question is the crate's own recorded
example of "resolved-by-removal items not closing themselves."

## Done when

- [x] No reference to `MAX_GATT_ACTIVITY_RECORDS` survives that implies a live cap.
- [x] `cargo doc --no-deps` produces no broken-intra-doc-link warning for it.
- [~] Gate green: `cargo build` and `cargo clippy --all-targets -- -D warnings` are
      clean. **`cargo test` is red, and was red on `main` before this change** —
      see "Pre-existing failure" below.
- [x] The `MAX_GATT_ACTIVITY_RECORDS` bullet in `embarch-study-designer/open.md`
      is closed, not reworded. If decision 54 needs a tombstone line instead
      (DOC-PROTOCOL §7.4), write that.
- [x] `changelog.d/study-designer-<slug>.fixed.md` dropped.

## Pre-existing failure, not caused by this change

`cargo test` aborts in `tests::dev_bench_message_discriminants_are_pinned` with
`has overflowed its stack`. Reproduced on the unmodified base commit (`2a136be`,
on `main`) by stashing this change, so it is **not** this task's doing; this
task edited comments only.

Diagnosed, not guessed: `RUST_MIN_STACK=33554432 cargo test` passes 9/9. It is
the libtest harness's default 2 MiB per-test-thread stack against this crate's
inline result types — the same class of failure `decisions/limits.md` decision
49 records Core solving with a 64 MiB thread stack. **Nothing in the test setup
does the equivalent, so the crate's own test suite cannot run at defaults.**

Left for a task of its own: the fix is a design call (a `.cargo/config.toml`
stack setting, boxing in the test, or shrinking the type further), not a
comment edit, and choosing it inside this task would have hidden it.
