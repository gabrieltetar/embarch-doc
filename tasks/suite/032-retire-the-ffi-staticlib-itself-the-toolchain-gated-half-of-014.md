# 032 — Retire the FFI staticlib itself: the toolchain-gated half of `suite/014`

**State:** open
**Source:** split out of `tasks/suite/014` by leg 093, 2026-09-11, which took the doc-and-citation
half and **could not safely take this one unattended**. See "Why this is split" below — the reason
is a build coupling, not a scoping preference.
**Scope:** suite
**Hardware:** **toolchain.** `embarch-dev-bench`'s Zephyr tree is gitignored, so no worktree in this
fleet can build the board workspaces this change alters. The change cannot be verified where it is
made, which is exactly the condition this field exists for.
**Owner:** no

## Why this is split, and why the halves are not independently landable

`suite/014` reads as two halves — "correct decision 7's false claims" and "retire the staticlib" —
and the task file suggested splitting on that seam. **That seam is not safe in the obvious
direction.** `embarch-dev-bench/app/CMakeLists.txt:162-202` cross-compiles
`cargo rustc --release --target <triple> --features ffi --lib --crate-type staticlib` on **every
non-POSIX build**. So:

- Retiring `embarch-study-designer`'s `ffi` feature and `src/ffi.rs` **first** breaks every
  dev-bench board build immediately — and **nothing in this fleet can observe that**, because the
  board workspaces cannot be built here. It would land green and be discovered on the bench.
- The CMake half must therefore go **first or together**: lift the existing `schema_version.rs`
  read at `CMakeLists.txt:120-146` out of its `if(CONFIG_ARCH_POSIX)` guard so every board gets
  the constant the cheap way, drop the staticlib target, then retire the Rust side.

Leg 093 took only the half with **no build coupling at all** — the decision text, the three stale
"does not exist yet" claims, and the mutual-precedent citation. Nothing in that half changes a byte
that any build consumes.

## What is left to do here

1. **Lift the `schema_version.rs` configure-time read out of the `CONFIG_ARCH_POSIX` guard**
   (`embarch-dev-bench/app/CMakeLists.txt:120-146`). It already has `CMAKE_CONFIGURE_DEPENDS`, so it
   is staleness-proof; it currently serves `native_sim` only, while real boards pay a Rust
   cross-toolchain for the same `u32`.
2. **Drop the staticlib machinery**: the `add_custom_target`, `target_link_libraries`, the two-arm
   board-to-triple map, and the `ESSD_LIB` path derivation. `CMakeLists.txt:184`'s `FATAL_ERROR` is
   why a third vendor family cannot be ported without adding a target-triple arm.
3. **Retire the two no-caller decode functions** — `essd_study_decode_and_verify` and
   `essd_study_decode_full` — with `study_ffi_real.c`, `study_ffi.h`'s three mirrored struct copies
   and four hand-mirrored `STUDY_FFI_MAX_*` constants, `study_ffi_stub.c`'s now-dead sibling arms,
   and the real-vs-stub CMake split. Verified 2026-09-11: the only FFI call reaching C is
   `study_ffi_schema_version()` at `main.c:1091` and `:1555`.
4. **Retire `embarch-study-designer`'s `ffi` feature** (`Cargo.toml:79`, enabled by no manifest in
   the suite), `src/ffi.rs` (19,773 B, with its `#[panic_handler]`, `EssdStatus` and three
   `#[repr(C)]` types), and the `ffi` cell in the CI matrix (decision 64's six feature cells).
5. **Whatever `study_ffi.h` still declares must be *derived*, not typed** — the `schema_version.rs`
   reader is the precedent in the same file.
6. **`embarch-study-designer/open.md`'s "nothing proves the FFI staticlib actually cross-links"**
   bullet is discharged by this, not by the doc half. Leg 093 deliberately left it standing.

## What leg 093 already did, so it is not redone

- Decision 7 (`embarch-study-designer/decisions/crate.md`) no longer claims `cbindgen` generates the
  header, and no longer claims C does not re-implement the wire format.
- The three "does not exist yet" claims (`open.md`, `README.md`, `Cargo.toml`) are corrected —
  `embarch-dev-bench` decision 20 records decision 8 as closed, and `src/ffi.rs:37` has the panic
  handler.
- The mutual-precedent loop is cut at the `embarch-topology` end: `validate_signal`'s keep-reason no
  longer rests on this surface.

**Note the direction this leaves things.** The decision record is now *correct about a surface that
still exists*. That is a strictly better state than before, but it is not the end state — decision 7
still describes an FFI bridge, because there still is one.

## Done when

- [ ] `essd_study_decode_and_verify` and `essd_study_decode_full` are gone from every repo.
- [ ] No board build invokes `cargo rustc --crate-type staticlib`; `study_ffi_schema_version` is
      served from the configure-time constant read on **every** workspace, not just `native_sim`.
- [ ] A real dev-bench board workspace builds and flashes, and `main.c:1091`'s schema check still
      reports the same number it did before.
- [ ] `embarch-study-designer` `cargo build`/`test`/`clippy --all-targets -- -D warnings` green with
      the `ffi` feature and `src/ffi.rs` removed, and the CI matrix updated to match.
- [ ] Decision 7 is rewritten to describe the boundary that actually exists once this lands.
- [ ] Gate green; `changelog.d/` fragments for both repos.
