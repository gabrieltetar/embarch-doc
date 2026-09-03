# embarch-api: open questions

**Status:** active, 2026-09-03.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong, not fixed

- **A `static` project's `[[projects.targets]]` menu cannot be picked from.** Nothing reads the rows `list_targets` returns; a build runs the project-level `build_command`. **A `target` param, or drop them.**
- **Decisions 20 and 21 describe config that does not exist** — no `default_target`, no `["none"]` snippet, though `interfaces/config.md` states both as truth. **Build, or retire both.**
- **A `[[projects]]` `board` is a hardware fact, and this config has been deriving it from build artifacts.** The reference-dut entry carried one for three weeks, commented as authoritative *because the repo's own `build_info.yml` recorded it* — whatever was last built, not the board on the desk, a different revision entirely. **Cost: a day of bring-up measuring a UART faithfully transmitting into the wrong pin**, across two well-evidenced wrong diagnoses. It violates [spec.md](spec.md) §2's no-inference-as-fact invariant on the most load-bearing DUT fact here. **Two fixes, neither built:** `init` refusing to *write* an inferred board unconfirmed — cheap, and enough — and `validate`/`status` comparing it against the hardware.
- **The build-log cap keeps the tail only**, while `spec.md` claimed "head and tail" from the first commit until 2026-09-03 — an intent nobody built. A Zephyr build's *first* error is usually the actionable one and a 64 KB tail can scroll it away. **Split, or accept tail-only.**

## Unfinished couplings

- **The alert and enrolled-board response types are unpinned mirrors.** No crate compiles both sides, so nothing typechecks the coupling; the signal-route mirrors are pinned from each side against one JSON literal. These two are not.
- **Decision 27's friendlier capacity error was never built.** Oversized submissions *are* rejected before the HTTP call, but by `serde`'s raw error, not the "which field, what limit" message described.
- **The smoke harness ([decisions](decisions/studies.md) 30) is named and unwritten.** The six mocked criteria beside it live in `tests/` ([decisions](decisions/shape.md) 46), with two gaps: the end-to-end half is `#[cfg(unix)]`, and a new endpoint escapes the bearer sweep unless its route list grows.
- **The study event stream has never met a real embarch-core.** `study-status --follow`/`study_watch` ([decisions](decisions/core-link.md) 48, 49) run only against a mock whose frames *copy* the wire format; `lagged` comes of writing the frame, not outrunning Core's buffer. Debt: `tasks/api/001-sse-client.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50), so branching on a cause means matching prose. **The prerequisite is not in this repo**: Core serves plain text on every non-2xx and its `{code, message, cause}` body (`embarch-core` decision 12) is deferred. Ordered: Core emits codes, the shared client carries one typed, this crate passes it on. A kind from the HTTP status is a coarser vocabulary, later mistaken for decision 12's.
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads, from its lifted copy of the retired UNC helpers. A different repo's fix.
- **Nothing reads `versions` yet** ([decisions](decisions/surface.md) 52): `doctor` check 11 compares `embarch`'s *own* host schema copy, so a mixed install stays invisible. Another repo's fix.

## Structural limits

- **Nothing can read a firmware version off a DUT.** A declared version describes the tree that was built, so "flashed this run" is the strongest claim — weaker than a measurement.
- **The inbound trust boundary is "whoever can spawn the process"** ([spec.md](spec.md) §6). Fine while an interactive client spawns it; revisit the moment one does not.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39): a remote Core cannot see a local path, and the manifest rides that route into the wall.

## Settled-deferred

Re-read suite-wide; none acquired a new argument:

- **PATH/toolchain preflight validation** — deliberately out of the build path: a build failure surfaces naturally, and preflighting every build costs the common case for an uncommon message. Expected as a `doctor` check.
- **Config fragments / `include`**, so `[core]` is not duplicated per repo. Tolerable for v1: `[core]` is three lines.
- **Config hot-reload** — config loads once; picking up an edit means a reconnect.
- **`serial_log` stays one-shot rather than streaming.** Core's endpoint is itself a bounded capture, so streaming needs Core to grow one first — **not this crate's to decide**. Unchanged by `study_watch`, consuming a stream Core has.
- **Adding projects stays manual TOML editing** — no mutation tool: the no-database philosophy, and the list barely churns. **Partially superseded**: a Zephyr-discovery project needs no edit to add a board, variant, revision or app. Holds for static and new.
