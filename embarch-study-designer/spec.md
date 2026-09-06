# embarch-study-designer: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Types: [interfaces/types.md](interfaces/types.md) · [interfaces/decoders.md](interfaces/decoders.md) · [interfaces/eap.md](interfaces/eap.md).

## 1. What it is

A shared `#![no_std]` Rust library defining what a **study** of a DUT is, and the narrow set of helpers every consumer needs one implementation of. A study is a scripted sequence of stimulus and interaction steps plus measurement, for three overlapping purposes: fuzz testing, power profiling, and automated integration testing.

**Not a service** — a data-types-and-tools library. It defines *what* gets sent, not the plumbing that sends it. It ships two authoring-time binaries behind feature flags (a GATT-config extractor, and previously a UI server since retired to `embarch-ui`), and neither is a service.

```
                    embarch-study-designer (#![no_std], compiled in by all three)
                                       |
      embarch-api  ------HTTP+JSON---->  embarch-core  ---serial, COBS+postcard--->  embarch-dev-bench
      (MCP + CLI)                        (bridges the two)                          (C, via FFI staticlib)
                                                                                             |
                                                                                        DUT (BLE)
```

Three consumers in two languages: two Cargo dependents, and dev-bench through a cross-compiled FFI staticlib with a generated C header. **Anything every consumer must agree on byte-for-byte or column-for-column belongs here**; anything hop-specific stays out.

## 2. Invariants

- **Allocator-free end to end.** Every sequence and string field is fixed-capacity, so the crate links into bare-metal C firmware with no global allocator anywhere in the chain. A `std`/`alloc` feature swaps the host-side container where the inline array was genuinely costly.
- **This crate never interprets a payload.** What a byte *means* is engineer-declared knowledge, carried as a declared encoding or layout and resolved host-side. No component ever sniffs content to decide.
- **No inference presented as fact.** No semantic description of what a GATT action does, and no encoding of a number into bytes on an engineer's behalf — that requires assuming a width and endianness nobody here is positioned to know.
- **A capacity limit refuses; it never truncates.** Every bound is disclosed, and exceeding one is a named error.
- **Loss is reported.** A stream that dropped records says so on close; a row that cannot fit is dropped and logged rather than truncated into a plausible-wrong value.
- **Numbers are exact or absent.** Integers render as integers; a trailing partial element is dropped rather than zero-padded; addition saturates rather than wrapping. **A plausible wrong number is the failure this crate keeps refusing to produce.**
- **The wire enum is append-only.** Variants are never reordered or removed, which is what makes postcard's discriminant give forward compatibility for free. The one discriminant reuse was safe only because no firmware carrying the old shapes had ever been flashed.
- **Symmetric human and agent access.** Every capability reaches both an MCP tool and a CLI subcommand, converging on the same modules.

## 3. Feature and target split

| Feature | Brings | Who uses it |
|---|---|---|
| *(default, `no_std`)* | the wire types, CRC sealing, canonical row rendering, tap validation | dev-bench firmware, and everyone |
| `ffi` | the `extern "C"` surface plus a generated C header | dev-bench's staticlib |
| `std` / `alloc` | heap-backed `steps` and result containers | the two host crates |
| `gatt-extract` | the repo-walking GATT extractor (needs `regex`, `ignore`) | an authoring-time binary |
| `eap-parse` | the `.eap` parser and a host-side **reference** interpreter | authoring, and pinning the semantics C must match |
| `study-ui` | table-authoring types and the study builder | `embarch-ui` |

**Every cell above is built on every push** by `.github/workflows/test.yml` — the two narrow cells with `cargo build`, not `cargo test`, which resolver v2 contaminates with the dev-dependency's `serde/std` ([decisions/crate.md](decisions/crate.md) decision 64).

**The FFI boundary is panic-safe by construction:** `panic = "abort"` plus an explicit status code on every exported function, rather than `catch_unwind`, which needs `std`. Board→target-triple selection lives in dev-bench's CMake, and the soft-float variant is mandatory on Cortex-M33 here — a hard-float staticlib fails to link the moment any path touches an `f32`, which includes a field inside `Sample` and not just the exposed signatures.

## 4. What a study carries

| Field | Crosses to dev-bench? | Sealed by |
|---|---|---|
| `steps` | yes | `steps_crc` |
| `streams` (declared taps) | yes | `streams_crc` |
| `protocols` (`.eap` manifests) | yes — dev-bench *executes* them | `protocols_crc` |
| `requires` (firmware versions) | **no** | — |
| `gatt` (the declared table) | **no** | — |
| `decoders` (payload layouts) | **no** — only an index rides on a tap | — |
| `dev_bench_log_level` | yes | **deliberately neither** |

**Three sibling seals, not one widened one**, each carried immediately after the one contiguous span it covers, so a hand-written C decoder digests one run of bytes per seal and a mismatch names **which third** arrived wrong.

**What is outside every seal is a rule, not an oversight:** how the host later *renders* a captured byte, and how loud the bench is while capturing it, change neither what dev-bench executes nor what it captures. **Re-rendering a capture with a corrected layout, or re-running at a louder log level, must leave it the same study** — otherwise debugging a failure would require altering the artifact under investigation.

## 5. Result storage

Core writes `study_results/<study_id>/`, and this crate owns every **row shape** in it while Core owns the paths and the storage. Layout and the endpoint surface: [embarch-core/interfaces.md](../embarch-core/interfaces.md) — *Result layout on disk*, and the `/study/{id}/…` routes above it.

- `events.json` — the `StudyResult`: per-step outcomes with both time edges, provenance, and one entry per declared tap. Written incrementally, one step result at a time, because the type is ~9 KB even after the size passes and Core never materialises a whole one.
- `streams/<tap>.*` — raw bytes **always written before any decode is attempted**, plus a rendered file where the declared encoding has one. Row shapes are this crate's: a sample row, a transcript row (with the payload rendered **twice** — exact hex and printable-ASCII, so a shell transcript is readable without decoding by hand while nothing is lost for a binary protocol), and a struct row.

## 6. Consumers

**`embarch-core`** bridges HTTP to serial: it validates a submission, checks all three seals, runs the handshake, relays `StudyStart`, receives step results, opens a signal tap's own port where the route bypasses dev-bench, and writes the results. One study in flight at a time; no cancel endpoint; the in-memory job registry does not survive a restart, so a poll afterwards is indistinguishable from an id that never existed — by design.

**`embarch-api`** is the authoring and submission surface: it fills the seals, validates capacities before the HTTP call, sequences an optional reflash, and exposes every capability as both an MCP tool and a CLI subcommand.

**`embarch-dev-bench`** links the staticlib and executes: it verifies `steps_crc` before step 0, decodes one step at a time from the retained span, opens declared taps from their scope, forwards arrival-stamped bytes **interpreting nothing**, and runs a `.eap` state machine against the live DUT.

## 7. Constants

Every capacity bound lives in one `limits` module. Values and provenance: [interfaces/limits.md](interfaces/limits.md); why they are fixed-capacity: [decisions/limits.md](decisions/limits.md). The two schema constants and what each guards: [decisions/versioning.md](decisions/versioning.md).

On the host — the `alloc`/`std` shape both Cargo dependents build — `Study` is **1,080 bytes**, down from 77,368 before three size passes: a heap container for `steps`, a generalised bounded newtype for the result types, and the outright removal of post-hoc validation, which was 97% of what remained after the first.

**The default `no_std` shape is still large, and that is the point**: with no allocator every one of those containers is an inline array, so the same `Study` is 83,512 bytes and a `DevBenchMessage` is 75,288 ([measured 2026-09-02]). `cargo test` builds default features, so the test harness runs against *that* shape and needs more than libtest's 2 MiB per-thread stack — `.cargo/config.toml` in the crate sets `RUST_MIN_STACK` to the 64 MiB Core already uses ([decisions/limits.md](decisions/limits.md) decision 63).
