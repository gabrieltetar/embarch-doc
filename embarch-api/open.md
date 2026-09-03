# embarch-api: open questions

**Status:** active, 2026-09-02.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong, not fixed

- **`snippets` is accepted, silently discarded, and reported as success** for a project with an explicit build command ([decisions](decisions/studies.md) 44c). A build with two snippets returned success having produced an image whose config said the option was not set. The help text says snippets are Zephyr-discovery-only, and that is documentation rather than a gate. The right fix is a decision: **reject the flags, or teach that path to splice them in.**
- **A `[[projects]]` `board` is a hardware fact, and this config has been deriving it from build artifacts.** The reference-dut entry carried a board value for three weeks with an inline comment presenting it as authoritative *because the repo's own `build_info.yml` recorded it* — which is a derivation from an artifact left by whatever someone last typed, not a statement about the board on the desk, which was a different revision entirely. **Cost: a day of bring-up spent measuring a UART faithfully transmitting into the wrong pin**, across two well-evidenced and wrong diagnoses.

  It violates [spec.md](spec.md) §2's own invariant — no inference presented as fact — and `board` is the most load-bearing DUT fact in this file. **Two things would have caught it and neither exists:** `init` could refuse to *write* an inferred board without operator confirmation, and `validate`/`status` could compare the configured board against what the attached hardware reports. The second is the real fix and the harder one; the first is cheap and would have been enough here.
- **The build-log cap keeps the tail only**, while `spec.md` claimed "head and tail" from the initial commit until 2026-09-03 — an intent nobody built. A Zephyr build's *first* error is usually the actionable one, and a 64 KB tail can scroll it away. **Build the split, or accept tail-only.**

## Unfinished couplings

- **The alert and enrolled-board response types are unpinned mirrors.** The signal-route mirrors are pinned from each side against the same JSON literal, because no crate in the suite compiles both sides and so nothing can typecheck the coupling. These two have the same coupling and no pin.
- **Decision 27's friendlier capacity error was never built.** Oversized submissions *are* rejected before the HTTP call, but by `serde`'s own raw error rather than the "which field, what limit" message the decision described calling a dedicated helper for.
- **The smoke harness ([decisions](decisions/studies.md) 30) is named and unwritten.** The six mocked criteria beside it now live in `tests/` ([decisions](decisions/shape.md) 46), with two gaps: the end-to-end half is `#[cfg(unix)]`, and a new endpoint escapes the bearer sweep unless its route list grows.
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads at all, from its own lifted copy of the retired UNC helpers. A different repo's correction to make.

## Structural limits

- **Nothing can read a firmware version off a DUT.** A declared version describes the tree that was built, so "flashed this run" is the strongest claim available and it is still weaker than a measurement.
- **The inbound trust boundary is "whoever can spawn the process"**, for MCP and CLI alike. Fine while this is spawned by an interactive client; it needs revisiting the moment it is not.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39). A remote Core cannot see a local path, and the manifest rides the same route into the same wall.

## Settled-deferred

Re-read suite-wide; none acquired a new argument:

- **PATH/toolchain preflight validation** — kept out of the build path deliberately, since a build failure surfaces naturally and preflighting every build adds latency to the common case to improve one uncommon message. Expected to land as an `embarch doctor` check instead, which is what a diagnostic run on demand is for.
- **Config fragments / `include`**, so `[core]` is not duplicated per repo. Tolerable for v1 because `[core]` is three lines with `base_url = "auto"`.
- **Config hot-reload** — config loads once; picking up edits means reconnecting the client.
- **`serial_log` stays one-shot rather than streaming.** Core's endpoint is itself a bounded capture and MCP calls are synchronous request/response, so real streaming would need Core to grow a streaming mode first — **not this crate's to decide unilaterally**, since Core has no idea it exists. An agent can approximate it with repeated windows.
- **Adding projects stays manual TOML editing** — no mutation tool. Consistent with the no-database philosophy; not enough churn in the project list to justify a second way to mutate it. **Partially superseded**: a Zephyr-discovery project no longer needs a config edit to add a board, variant, revision or app at all, since those are discovered live. The reasoning holds for static projects and for adding a whole new project.
