# embarch-study-designer decisions: Crate shape and boundaries

**Status:** active, 2026-09-02.

What this crate is, what it links, and how it reaches three consumers in two languages.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). CI: [ci.md](ci.md).

### 1 — Separable crate, not embedded in `embarch-api`

`embarch-core` and `embarch-api` compile it in as a Cargo dependency, and dev-bench firmware's build reads its constants and wire enums from its source (decision 7). Chosen explicitly over embedding study logic inside `embarch-api`: dev-bench firmware is a different binary in a different language and needs the identical types, which is impossible if they live only in `embarch-api`'s crate.

### 2 — Data types plus the narrow set of tools needed to use them identically everywhere — not a protocol or transport

The crate defines `serde`-derived types ([interfaces/types.md](../interfaces/types.md)) *and* the small number of type-adjacent helpers every consumer needs one implementation of, so `embarch-core`/`embarch-api`/dev-bench never reimplement the same logic and drift: CRC sealing (`steps_crc`, decision 17) and `Sample`'s canonical row-rendering ([interfaces/decoders.md](../interfaces/decoders.md), since the CSV rework). It deliberately hardcodes no wire format and no transport — different hops need different formats (decision 3), and baking one in forces a lossy re-encode at whichever hop doesn't match.

The line: anything every consumer must agree on byte-for-byte or column-for-column belongs in the crate; anything hop-specific (the socket, the HTTP client) stays out.

### 5 — `#![no_std]`, not std-everywhere

Dev-bench firmware may be bare-metal and its runtime was undecided when this was locked. A `no_std` crate keeps every option open (bare-metal Rust, an RTOS, a hosted environment via a `std` shim); a `std`-only crate forecloses the bare-metal case outright. `embarch-core`/`embarch-api` run hosted and simply use the `no_std`-compatible types.

### 7 — Dev-bench firmware is C, sharing the wire through a hand-written codec and configure-time reads of this crate — not native Rust, not a Zephyr+Rust module

Resolved over native embedded Rust and `zephyr-lang-rust` because the nRF54 family splits sharply by variant: nRF54L15 (single Cortex-M33) has a workable Rust path via existing `zephyr-lang-rust` samples on comparable Nordic parts, but nRF54H20's mandatory multi-core `sysbuild` build isn't a proven fit for that project's west-module/CMake integration. Either way Zephyr's BLE host stays a C API reached through generated bindings, so the BLE-heavy parts wouldn't be idiomatic Rust regardless. Going C sidesteps the split.

**The boundary that exists (2026-11-10, `tasks/suite/032`):** the firmware links no Rust. It re-implements the wire in C — `serial_protocol.c`'s postcard/COBS/CRC-32 codec, `eap.h` and `eap_interp.c` — kept in step by hand and pinned by the cross-side byte tests (`tests/firmware_test_vectors.rs`). Its build reads the wire schema version, every `src/limits.rs` const and every wire enum's declaration indices out of this crate's source at configure time (`embarch-dev-bench` decisions 20, 56), so those cannot drift; field layouts still can. Decision 1's three-definitions problem is accepted here, not avoided.

**Retired: the FFI staticlib.** This entry used to have the crate cross-compile as a `#![no_std]` staticlib exposing `extern "C"` functions, with C calling into it rather than re-implementing the wire. The C codec shipped anyway, `cbindgen` was never built, and by 2026-09-11 the surface's only caller was the schema-version call; `essd_study_decode_and_verify` and `essd_study_decode_full` had none. So the `ffi` feature, `src/ffi.rs` and the boards' `cargo rustc --crate-type staticlib` step are gone, and every board reads the number the way `native_sim` already did. Decision 23 went with it.

### 8 — A sibling-repo path dependency, not a published crate and not a git reference

`embarch-core` and `embarch-api` consume it as `embarch-study-designer = { path = "../embarch-study-designer" }`. Not a registry package: that means version-bump-and-republish overhead while the type model ([interfaces/types.md](../interfaces/types.md)) still changes across all three consumers, all of whom track head. Originally specified as a *git* dependency and implemented as a plain path instead once Milestone 2 needed it wired for real — edits are picked up by the next `cargo build` in either consumer with no commit/push/re-vendor step, and a path is exactly what [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §2's sibling layout already assumes. A git dependency stays available if a consumer's checkout is ever not a true sibling (a CI runner, a machine without all four repos cloned side by side); no real workflow needs it yet.

The repo is [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), standalone rather than a workspace member of an existing repo — three independently-versioned consumers (two Cargo dependents, one C consumer) is the case a shared standalone crate is for.

### 23 — The FFI boundary is panic-safe by construction: `panic = "abort"` plus explicit status codes, not `catch_unwind`

**Retired 2026-11-10 with the FFI surface (decision 7).** `panic = "abort"` stays in `[profile.release]` on decision 5's ground alone, and now reaches only this crate's own release binaries. As decided:

A Rust panic unwinding across `extern "C"` into C firmware is undefined behavior, and decision 7 left it unaddressed. Resolved with `panic = "abort"` in `[profile.release]` — the natural fit for a `no_std` bare-metal target with no unwinding runtime (decision 5) — rather than wrapping every exported body in `std::panic::catch_unwind`, which needs `std` and is unavailable here. Every exported function returns an integer status (`0` = success, negative = a documented reason: buffer-too-small, capacity-exceeded, malformed input) plus out-parameters, so no Rust `Result` or panic ever reaches the C caller. Same philosophy as decision 18 applies at the HTTP boundary: name the specific failure, never let a raw internal error surface.
