# embarch-api: open questions

**Status:** active, 2026-09-02.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong, not fixed

- **`snippets` is accepted, silently discarded, and reported as success** for a project with an explicit build command ([decisions](decisions/studies.md) 44c). A build with two snippets returned success, having produced an image whose config said the option was unset. The help text saying snippets are Zephyr-discovery-only is documentation, not a gate. **Reject them, or splice them in.**
- **A `[[projects]]` `board` is a hardware fact, and this config has been deriving it from build artifacts.** The reference-dut entry carried one for three weeks, commented as authoritative *because the repo's own `build_info.yml` recorded it* — a derivation from whatever someone last built, not from the board on the desk, which was a different revision entirely. **Cost: a day of bring-up spent measuring a UART faithfully transmitting into the wrong pin**, across two well-evidenced and wrong diagnoses. It violates [spec.md](spec.md) §2's no-inference-as-fact invariant, on the most load-bearing DUT fact in this file. **Two fixes, neither built:** `init` refusing to *write* an inferred board unconfirmed — cheap, and enough here — and `validate`/`status` comparing it against what the hardware reports, the real one.
- **`schema_version` and `error_kind` are documented and were never built.** [decisions](decisions/surface.md) 16/24 and [tools.md](interfaces/tools.md) describe them as fields of every `--json` object; neither string appears in this crate's source, so a caller told to branch on `error_kind` instead of an exit code has nothing to branch on. **Build them, or retire it.**
- **The build-log cap keeps the tail only**, while `spec.md` claimed "head and tail" from the initial commit until 2026-09-03 — an intent nobody built. A Zephyr build's *first* error is usually the actionable one and a 64 KB tail can scroll it away. **Split it, or accept tail-only.**

## Unfinished couplings

- **The alert and enrolled-board response types are unpinned mirrors.** No crate compiles both sides, so nothing typechecks the coupling; the signal-route mirrors are pinned from each side against one JSON literal. These two have the same coupling and no pin.
- **Decision 27's friendlier capacity error was never built.** Oversized submissions *are* rejected before the HTTP call, but by `serde`'s raw error, not the "which field, what limit" message the decision described.
- **The smoke harness ([decisions](decisions/studies.md) 30) is named and unwritten.** The six mocked criteria beside it live in `tests/` ([decisions](decisions/shape.md) 46), with two gaps: the end-to-end half is `#[cfg(unix)]`, and a new endpoint escapes the bearer sweep unless its route list grows too.
- **The study event stream has never met a real embarch-core.** `study-status --follow`/`study_watch` ([decisions](decisions/core-link.md) 48, 49) run only against a mock whose frames are a *copy* of the wire format; `lagged` is provoked by writing the frame, not by outrunning Core's real buffer. Debt: `tasks/api/001-sse-client.md`.
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads, from its own lifted copy of the retired UNC helpers. A different repo's correction.

## Structural limits

- **Nothing can read a firmware version off a DUT.** A declared version describes the tree that was built, so "flashed this run" is the strongest claim available — weaker than a measurement.
- **The inbound trust boundary is "whoever can spawn the process"**, MCP and CLI alike. Fine while an interactive client spawns it; revisit the moment one does not.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39): a remote Core cannot see a local path, and the manifest rides the same route into the same wall.

## Settled-deferred

Re-read suite-wide; none acquired a new argument:

- **PATH/toolchain preflight validation** — kept out of the build path deliberately: a build failure surfaces naturally, and preflighting every build costs the common case to improve one uncommon message. Expected as an `embarch doctor` check.
- **Config fragments / `include`**, so `[core]` is not duplicated per repo. Tolerable for v1: `[core]` is three lines with `base_url = "auto"`.
- **Config hot-reload** — config loads once; picking up an edit means reconnecting.
- **`serial_log` stays one-shot rather than streaming.** Core's endpoint is itself a bounded capture, so streaming needs Core to grow a streaming mode first — **not this crate's to decide unilaterally**. Unchanged by `study_watch`, which consumes a stream Core already has.
- **Adding projects stays manual TOML editing** — no mutation tool, consistent with the no-database philosophy and with how little the project list churns. **Partially superseded**: a Zephyr-discovery project needs no config edit to add a board, variant, revision or app. The reasoning holds for static projects and whole new ones.
