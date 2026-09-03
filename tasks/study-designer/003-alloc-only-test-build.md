# 003 — `cargo test --features alloc` does not compile

**State:** done on agent/study-designer/003-alloc-only-test-build, 2026-09-02 — pushed, not merged.
**Source:** found by the study-designer/002 worker, 2026-09-02, while running the feature matrix; reproduced on `main` at `2a136be`, so it predates that task and is not caused by it.
**Scope:** study-designer
**Hardware:** none

## What

```
$ cargo test --features alloc
error[E0599]: no method named `to_string` found for reference `&'static str`
   --> src/outpost.rs:757:32
error[E0599]: no method named `to_string` found for reference `&'static str`
   --> src/outpost.rs:772:32
error: could not compile `embarch-study-designer` (lib test) due to 2 previous errors
```

`a_layout_2_stream_is_refused_rather_than_misread` is gated
`#[cfg(feature = "alloc")]` and calls `"abc123".to_string()`. Under `alloc`
without `std` the crate is `#![no_std]`, so `ToString` is not in the prelude —
`alloc::string::ToString` has to be imported, or the call replaced with
`String::from`.

Library code is fine: `cargo build --features alloc` passes. Only the `lib test`
target is broken, so nothing shipped is affected.

## Why now

`alloc` alone is exactly the configuration Cargo.toml already records as the
only one that can see this class of gap — every real consumer also pulls in
`serde/std`, so feature unification hides it. The last time that bit, the
crate's `Deserialize` for `Backing` did not exist at all. A feature the crate
supports and cannot run its own tests under is a hole in the same place.

Small: two lines plus whichever import is chosen.

## Done when

- [x] `cargo test --features alloc` compiles and passes.
- [x] The rest of the matrix stays green: default, `--features std`, `--all-features`.
- [x] `cargo clippy --all-targets --features alloc -- -D warnings` clean.
- [x] `changelog.d/study-designer-<slug>.fixed.md` dropped.

## What shipped

Both `to_string()` calls in `a_layout_2_stream_is_refused_rather_than_misread`
(`src/outpost.rs`) became `String::from(...)`, with a local
`use alloc::string::String;` inside the test function. **Chose `String::from`
over importing `alloc::string::ToString`** to match the rest of this file: the
`render` module (same file, ~line 620) already carries a comment explaining
why it uses `format!`/`String::from` rather than `.to_string()` under `alloc`
without `std` — this test now follows the same rule instead of introducing the
second style the comment was written to avoid.

Full matrix, run explicitly rather than trusting feature unification:

| Build | Result |
|---|---|
| `cargo test` (default) | 108 passed, 0 failed — no stack overflow. study-designer/002's harness fix holds. |
| `cargo test --features alloc` | 109 passed, 0 failed (the previously-uncompilable test now runs) |
| `cargo test --features std` | passes |
| `cargo test --all-features` | passes |
| `cargo clippy --all-targets --features alloc -- -D warnings` | clean |
| `cargo build`, `cargo clippy --all-targets -- -D warnings` (default) | clean |

No hardware verification debt: host-side only, `lib test` target, no wire or
library-code change (`cargo build --features alloc` was already fine, per the
task's own note).

**On "nothing stops this from breaking again":** true, and worth a check —
recorded as one paragraph in
[open.md](../../embarch-study-designer/open.md) §"Not exercised by any routine
check" rather than as new CI machinery here, since any such check would live
outside this crate's own row (a schedule or workflow, not a source file this
task owns).
