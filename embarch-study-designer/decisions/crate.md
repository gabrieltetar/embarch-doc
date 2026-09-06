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

### 64 — The feature matrix is six cells run by this crate's own CI, and the two narrow ones are `cargo build`, not `cargo test`

Nothing built or tested a single feature cell of the most depended-on crate in the suite until 2026-09-05. That is what let decision 46's `alloc` cell ship broken: `alloc` did not imply `serde/alloc`, so `Backing<T, N>: Deserialize` did not exist, and **every real consumer also pulls something that turns on `serde/std`, so feature unification always supplied the missing half.** Only this crate's own single-feature build could ever see it, and no consumer's CI can — by construction, because a consumer is what hides it.

`.github/workflows/test.yml` now runs, on push and pull_request, one named step per cell a real consumer actually uses — deliberately not a `2^7` powerset, which would be job count mistaken for coverage:

| Cell | Why it is its own cell |
|---|---|
| default (no features) | dev-bench firmware's `no_std`, allocator-free shape (decisions 5, 15, 46). The one that must never break. |
| `alloc` alone | The cell that was broken and unseen. Its own step with its own name, permanently. |
| `std` | Implies `alloc`; what `embarch-core`/`embarch-api`/`embarch-ui` get. |
| `gatt-extract`, `study-ui`, `eap-parse` | Each is `std`-only, off by default, and pulls its own dependencies (`regex`/`serde_json`/`ignore`, `toml`), so each rots independently. Run separately so one feature's compile error is not reported as another's. |
| `ffi` | Below. |

**The load-bearing half is that `default` and `alloc` are checked with `cargo build`, not `cargo test`.** This crate's only dev-dependency is `serde_json`, which pulls `serde` with `std`; edition 2021 means resolver v2, and resolver v2 unifies dev-dependency features into the library whenever it builds a target needing dev-deps — which `cargo test` always does. Measured with `cargo tree -f "{p} {f}"`: for the `default` cell `serde_core` is `result` with `-e normal` and `result,std` with `-e normal,dev`; for `std` both columns read `alloc,result,std`. So on the two narrow cells `cargo test` compiles a *different library than any consumer links*.

**Verified rather than reasoned**: reintroducing the bug on a scratch copy, `cargo build --no-default-features --features alloc` fails with 16 errors while `cargo test --no-default-features --features alloc` passes 9/9. A matrix copied verbatim from `embarch-topology`'s all-`cargo test` shape would have been a step that cannot fail for the reason it was added — worse than an absent one, because it reads as coverage. The `std` and tool cells keep `cargo test` alone, since a `build` twin there is measurably the same build.

**`ffi` is a `build` with a stated ceiling, and the workflow says so in its own comment.** A host `cargo build --features ffi` does type-check `src/ffi.rs`'s `extern "C"` surface (decisions 7, 23) against the rest of the crate in dev-bench's real `no_std`, no-alloc configuration, which is a real regression class. It does **not** prove what dev-bench needs: that the crate links as a `--crate-type staticlib` on a cross target with a panic handler and `panic = "abort"`. That build root does not exist yet, and adding a cross-compile step before the toolchain does would be the same fake-coverage mistake in a different place.

Clippy `-D warnings` runs on `--all-features` (the widest set, and the only configuration asserting the tool features do not collide) and again on `default` and `alloc`, because a `no_std` build's lints are not a subset of a `std` build's. `--locked` throughout is honest here: `Cargo.lock` is committed, this crate being the FFI build root (decision 23).

**Every step was run locally before the workflow was pushed, and all fourteen were green** — no cell was red on arrival.

Not in scope, and still absent: a `release.yml` with the `verify-version` job `embarch-umbrella`'s decisions 27/29 put in four repos. That is a separate absence with a separate decision behind it.

---
