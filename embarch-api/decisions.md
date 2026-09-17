# embarch-api: decisions

**Status:** active, 2026-09-06.

Why it is the way it is, split by mission. Current truth: [spec.md](spec.md). Unresolved: [open.md](open.md). Config: [interfaces/config.md](interfaces/config.md), [interfaces/dev-bench-config.md](interfaces/dev-bench-config.md). Tools: [interfaces/tools.md](interfaces/tools.md), [interfaces/studies.md](interfaces/studies.md).

**Numbers are permanent identifiers**, unique to this sub-project, never renumbered or reused ([DOC-CONVENTIONS.md](../DOC-CONVENTIONS.md)). `scripts/check-decision-refs.py` resolves every one.

| Load this for | Decisions | Size |
|---|---|---|
| [Scope and boundaries](decisions/shape.md) — what this is, what it is not, the one-way relationships, and the `dev_bench_hello` CLI twin | 1, 2, 3, 4, 6, 7, 8, 9, 10, 25, 61 | 6.0 KB |
| [Retired config keys and target selection](decisions/config-retirement.md) — the one target a `static` project has, and the general rule for a config key this crate stops reading | 53, 64 | 6.3 KB |
| [How far the tests reach](decisions/tests.md) — the one-module `lib` target, where the bearer sweep's exhaustiveness comes from, and how the gate came to reach the shared client's own tests | 46, 54, 56 | 9.7 KB |
| [The named smoke-harness tier](decisions/smoke-harness.md) — the live-run methodology's name and script, and its real bound under concurrent load | 30, 74 | 3.8 KB |
| [The tool and CLI surface — JSON shape and versioning](decisions/surface.md) — JSON shape, watching a study live, what this binary says about itself | 16, 24, 50 | 4.9 KB |
| [How a failure is reported and attributed](decisions/failure-reporting.md) — how a tool description cites its own decision, the parity rule extended to the signal/dev-bench-link writers, `validate`'s call sites branching on `kind`, the third `"unknown"` value for a `kind`-less Core, and the `not_attached` lead's wording | 57, 67, 71, 73, 76 | 11.3 KB |
| [Per-tool wrapping](decisions/tool-wrapping.md) — why a given tool exists (or deliberately doesn't), its params, what its description promises | 23, 29, 41, 47, 52 | 6.0 KB |
| [Hardware selection and identity](decisions/hardware-selection.md) — enrollment, mismatch alerts, the dev-bench identity cross-check, and why no tool here ever picks a physical board or port on a caller's behalf | 34, 35, 59, 60, 70 | 9.0 KB |
| [Running a build](decisions/build.md) — the generic per-project command, and the unix-only process-tree kill | 5, 75 | 2.9 KB |
| [What a build log keeps](decisions/log-capture.md) — what a truncated log keeps, and how the drain reads a child stream | 18, 65 | 3.9 KB |
| [`target.json` provenance](decisions/target-json.md) — the readable build-dir prefix, the descriptor file, the crate-owned hash, and `build_dir_name` on every `list-targets` row | 19, 69, 77 | 8.6 KB |
| [The flash offset a `bin` needs](decisions/flash-address.md) — `base_address` as config, not a per-call parameter | 42 | 1.7 KB |
| [Target discovery and selection](decisions/zephyr.md) — the Zephyr exception, what a call may name, and what a `static` project refuses rather than ignores | 12, 20, 21, 51 | 9.1 KB |
| [What board.yml/app scanning trusts](decisions/zephyr-scan.md) — the retired SoC-override hatch, the uncached scan's cost bound, and the `app/`/`apps/` scan | 13, 22, 63 | 5.7 KB |
| [Reaching Core](decisions/core-link.md) — address resolution and artifact transfer | 11, 14, 15, 17, 26 | 3.9 KB |
| [The shared client crate](decisions/client-crate.md) — extraction, the one auth-and-send funnel, the stack, older-Core parsing, one WSL2 predicate, the crate's home | 36, 37, 38, 55, 58, 62, 66 | 10.6 KB |
| [The study event stream](decisions/study-events.md) — `lagged` and a dropped stream as facts, fallback to polling, the mirrored `StudyEvent` | 48, 49 | 3.7 KB |
| [The per-machine logfile](decisions/logging.md) — why this crate keeps its own rolling logfile, and why it is per-user | 43 | 1.6 KB |
| [What a study reads back](decisions/study-reads.md) — seals, schemas, the manifest, and the stream tools that replaced three fixed-channel aliases | 27, 28, 31, 33, 39 | 6.2 KB |
| [What a study flashes first](decisions/study-reflash.md) — reflash sequencing and three gaps in `run_study`'s own contract | 40, 44 | 5.7 KB |
| [The dev-bench pipeline](decisions/dev-bench.md) — outside `[[projects]]`, no longer constants, and the one route whose timeout is stated rather than inherited | 32, 45, 68 | 4.9 KB |

**Decisions 31 and 33 are one decision under two numbers.** The commit that added decision 32 inserted it in the middle and **renumbered the entry below it from 31 to 33**, so every prose reference to `decision 31` written before that commit silently began pointing at a different entry. One entry owns both numbers, in [study-reads.md](decisions/study-reads.md) — which is why numbers are permanent here now (DOC-COMPACTION.md §5).
