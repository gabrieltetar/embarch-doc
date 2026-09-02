# embarch-study-designer decisions: Crate shape and boundaries

**Status:** active, 2026-09-02.

What this crate is, what it links, and how it reaches three consumers in two languages.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — Separable crate, not embedded in `embarch-api`

`embarch-core`, `embarch-api`, and dev-bench firmware each compile it in independently — a Cargo dependency for the first two, a cross-compiled FFI staticlib for the third (decision 7). Chosen explicitly over embedding study logic inside `embarch-api`: dev-bench firmware is a different binary in a different language and needs the identical types, which is impossible if they live only in `embarch-api`'s crate.

### 2 — Data types plus the narrow set of tools needed to use them identically everywhere — not a protocol or transport

The crate defines `serde`-derived types (§4) *and* the small number of type-adjacent helpers every consumer needs one implementation of, so `embarch-core`/`embarch-api`/dev-bench never reimplement the same logic and drift: CRC sealing (`steps_crc`, decision 17) and `Sample`'s canonical row-rendering (§4.7, since §5.2's CSV rework). It deliberately hardcodes no wire format and no transport — different hops need different formats (decision 3), and baking one in forces a lossy re-encode at whichever hop doesn't match.

The line: anything every consumer must agree on byte-for-byte or column-for-column belongs in the crate; anything hop-specific (the socket, the HTTP client) stays out.

### 5 — `#![no_std]`, not std-everywhere

Dev-bench firmware may be bare-metal and its runtime was undecided when this was locked (§7). A `no_std` crate keeps every option open (bare-metal Rust, an RTOS, a hosted environment via a `std` shim); a `std`-only crate forecloses the bare-metal case outright. `embarch-core`/`embarch-api` run hosted and simply use the `no_std`-compatible types.

### 7 — Dev-bench firmware is C, bridged via an FFI staticlib — not native Rust, not a Zephyr+Rust module

Resolved over native embedded Rust and `zephyr-lang-rust` because the nRF54 family splits sharply by variant: nRF54L15 (single Cortex-M33) has a workable Rust path via existing `zephyr-lang-rust` samples on comparable Nordic parts, but nRF54H20's mandatory multi-core `sysbuild` build isn't a proven fit for that project's west-module/CMake integration. Either way Zephyr's BLE host stays a C API reached through generated bindings, so the BLE-heavy parts wouldn't be idiomatic Rust regardless. Going C sidesteps the split.

This crate cross-compiles as a `#![no_std]` staticlib for the target ABI, exposing `extern "C"` functions to build/serialize/deserialize `Study`/`Step`; `cbindgen` generates the C header from the Rust source so it cannot drift by hand. The `postcard` encode/decode logic (decision 3) stays inside the compiled Rust — C calls into it rather than re-implementing the wire format, which is what stops this becoming the three-independent-definitions problem decision 1 exists to avoid.

### 8 — A sibling-repo path dependency, not a published crate and not a git reference

`embarch-core` and `embarch-api` consume it as `embarch-study-designer = { path = "../embarch-study-designer" }`. Not a registry package: that means version-bump-and-republish overhead while the type model (§4) still changes across all three consumers, all of whom track head. Originally specified as a *git* dependency and implemented as a plain path instead once Milestone 2 needed it wired for real — edits are picked up by the next `cargo build` in either consumer with no commit/push/re-vendor step, and a path is exactly what [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §2's sibling layout already assumes. A git dependency stays available if a consumer's checkout is ever not a true sibling (a CI runner, a machine without all four repos cloned side by side); no real workflow needs it yet.

The repo is [gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), standalone rather than a workspace member of an existing repo — three independently-versioned consumers (two Cargo dependents, one FFI/C consumer) is the case a shared standalone crate is for.

### 23 — The FFI boundary is panic-safe by construction: `panic = "abort"` plus explicit status codes, not `catch_unwind`

A Rust panic unwinding across `extern "C"` into C firmware is undefined behavior, and decision 7 left it unaddressed. Resolved with `panic = "abort"` in `[profile.release]` — the natural fit for a `no_std` bare-metal target with no unwinding runtime (decision 5) — rather than wrapping every exported body in `std::panic::catch_unwind`, which needs `std` and is unavailable here. Every exported function returns an integer status (`0` = success, negative = a documented reason: buffer-too-small, capacity-exceeded, malformed input) plus out-parameters, so no Rust `Result` or panic ever reaches the C caller. Same philosophy as decision 18 applies at the HTTP boundary: name the specific failure, never let a raw internal error surface.

---
