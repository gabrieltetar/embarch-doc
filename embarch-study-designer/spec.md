# embarch-study-designer: spec

**Status:** active, 2026-09-02.

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Types: [interfaces/types.md](interfaces/types.md) · [interfaces/decoders.md](interfaces/decoders.md) · [interfaces/eap.md](interfaces/eap.md). What a study carries and which seal covers it: [spec/carriage.md](spec/carriage.md).

## 1. What it is

A shared `#![no_std]` Rust library defining what a **study** of a DUT is, and the narrow set of helpers every consumer needs one implementation of. A study is a scripted sequence of stimulus and interaction steps plus measurement, for three overlapping purposes: fuzz testing, power profiling, and automated integration testing.

**Not a service** — a data-types-and-tools library. It defines *what* gets sent, not the plumbing that sends it. It ships two authoring-time binaries behind feature flags (a GATT-config extractor, and previously a UI server since retired to `embarch-ui`), and neither is a service.

```
                    embarch-study-designer (#![no_std]; linked by two, read by dev-bench's build)
                                       |
      embarch-api  ------HTTP+JSON---->  embarch-core  ---serial, COBS+postcard--->  embarch-dev-bench
      (MCP + CLI)                        (bridges the two)                          (C, hand-written codec)
                                                                                             |
                                                                                        DUT (BLE)
```

Three consumers in two languages: two Cargo dependents, and dev-bench, which links no Rust: its C codec is hand-written and pinned by the cross-side byte tests, and its build reads the schema version, limits and wire enum values from this crate's source (decision 7). **Anything every consumer must agree on byte-for-byte or column-for-column belongs here**; anything hop-specific stays out.

## 2. Invariants

- **Allocator-free end to end.** Every sequence and string field is fixed-capacity, so the crate links into bare-metal C firmware with no global allocator anywhere in the chain. A `std`/`alloc` feature swaps the host-side container where the inline array was genuinely costly.
- **This crate never interprets a payload.** What a byte *means* is engineer-declared knowledge, carried as a declared encoding or layout and resolved host-side. No component ever sniffs content to decide.
- **No inference presented as fact.** No semantic description of what a GATT action does, and no encoding of a number into bytes on an engineer's behalf — that requires assuming a width and endianness nobody here is positioned to know.
- **A capacity limit refuses; it never truncates.** Every bound is disclosed, and exceeding one is a named error **naming the bound actually exceeded** — not a neighbouring bound reused because its error already existed.
- **Loss is reported.** A stream that dropped records says so on close; a row that cannot fit is dropped and logged rather than truncated into a plausible-wrong value.
- **Numbers are exact or absent.** Integers render as integers; a trailing partial element is dropped rather than zero-padded; addition saturates rather than wrapping. **A plausible wrong number is the failure this crate keeps refusing to produce.**
- **The wire enum is append-only.** Variants are never reordered or removed, which is what makes postcard's discriminant give forward compatibility for free. The one discriminant reuse was safe only because no firmware carrying the old shapes had ever been flashed.
- **Symmetric human and agent access.** Every capability reaches both an MCP tool and a CLI subcommand, converging on the same modules.

## 3. Feature and target split

| Feature | Brings | Who uses it |
|---|---|---|
| *(default, `no_std`)* | the wire types, CRC sealing, canonical row rendering, tap validation | everyone (no firmware links it today) |
| `std` / `alloc` | heap-backed `steps` and result containers; the host-run study types (`HostStudy`, decision 80; `Repeat` and `LineCount`, decision 86; a prompt's `bench_config`, decision 88; JSON only). `std` also pulls `regex` to compile a count pattern | the two host crates |
| `gatt-extract` | the repo-walking GATT extractor (needs `regex`, `ignore`) | an authoring-time binary |
| `eap-parse` | the `.eap` parser and a host-side **reference** interpreter | authoring, and pinning the semantics C must match |
| `study-ui` | table-authoring types, the study builder, and the custom-action registry | `embarch-ui` |

**Every cell above is built on every push** by `.github/workflows/test.yml` — the two narrow cells with `cargo build`, not `cargo test`, which resolver v2 contaminates with the dev-dependency's `serde/std` ([decisions/ci.md](decisions/ci.md) decision 64).

**The custom-action registry** (`ActionRegistry`/`StructRegistry`, `std`-only, behind `study-ui`) reads and writes `<firmware_repo_root>/embarch/study-actions.toml` — engineer-authored names and literal byte choices for a DUT's custom GATT actions, never linked into dev-bench or the plain Cargo-dependency use of `embarch-core`/`embarch-api`. Format, `validate`'s refusals, and why: [decisions/registry.md](decisions/registry.md).

**No `extern "C"` surface:** the FFI staticlib and its `ffi` feature were retired on 2026-11-10 (decisions 7, 23), since its only live call was the schema version.

## 4. Result storage

Core writes `study_results/<study_id>/`, and this crate owns every **row shape** in it while Core owns the paths and the storage. Layout and the endpoint surface: [embarch-core/interfaces.md](../embarch-core/interfaces.md) — *Result layout on disk*, and the `/study/{id}/…` routes above it.

- `events.json` — the `StudyResult`: per-step outcomes with both time edges, provenance, and one entry per declared tap. Written incrementally, one step result at a time, because the type is ~9 KB even after the size passes and Core never materialises a whole one.
- `streams/<tap>.*` — raw bytes **always written before any decode is attempted**, plus a rendered file where the declared encoding has one. Row shapes are this crate's: a sample row, a transcript row (with the payload rendered **twice** — exact hex and printable-ASCII, so a shell transcript is readable without decoding by hand while nothing is lost for a binary protocol), and a struct row.

## 5. Consumers

**`embarch-core`** bridges HTTP to serial: it validates a submission, checks all three seals, runs the handshake, relays `StudyStart`, receives step results, opens a signal tap's own port where the route bypasses dev-bench, and writes the results. One study in flight at a time; no cancel endpoint; the in-memory job registry does not survive a restart, so a poll afterwards is indistinguishable from an id that never existed — by design.

**`embarch-api`** is the authoring and submission surface: it fills the seals, validates capacities before the HTTP call, sequences an optional reflash, and exposes every capability as both an MCP tool and a CLI subcommand.

**`embarch-dev-bench`** executes, in its own C: it verifies `steps_crc` before step 0, decodes one step at a time from the retained span, opens declared taps from their scope, forwards arrival-stamped bytes **interpreting nothing**, and runs a `.eap` state machine against the live DUT.

## 6. Constants

Every capacity bound lives in one `limits` module. Values and provenance: [interfaces/limits.md](interfaces/limits.md); why they are fixed-capacity: [decisions/limits.md](decisions/limits.md). The two schema constants and what each guards: [decisions/versioning.md](decisions/versioning.md). Whole-`Study`/`DevBenchMessage` sizes on the host vs. `no_std` shapes, and why the test harness needs a raised `RUST_MIN_STACK`: [decisions/limits.md](decisions/limits.md) decision 63.
