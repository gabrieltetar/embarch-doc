# 003 — `cargo test --features alloc` does not compile

**State:** open
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

- [ ] `cargo test --features alloc` compiles and passes.
- [ ] The rest of the matrix stays green: default, `--features std`, `--all-features`.
- [ ] `cargo clippy --all-targets --features alloc -- -D warnings` clean.
- [ ] `changelog.d/study-designer-<slug>.fixed.md` dropped.
