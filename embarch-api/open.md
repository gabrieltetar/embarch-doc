# embarch-api: open questions

**Status:** active, 2026-09-06.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong, not fixed

- **A `[[projects]]` `board` is a hardware fact, and nothing compares one against the hardware.** Derived from `build_info.yml` it records the last build, not the board on the desk — a different revision, and a day of bring-up lost to it. Violates [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` stopped *writing* one unconfirmed (`embarch-umbrella` decision 41), but refusing to assert is not detecting, and every config scaffolded before then still asserts: **`validate`/`status` comparing it against the hardware is unbuilt.**

## Unfinished couplings

- **The alert and enrolled-board response types were unpinned mirrors, and it fired**: `link_port_interface` (`embarch-topology` decision 20) reached Core's wire body and the client mirror silently dropped it. `api`'s half is now pinned against a JSON literal each, same shape as the signal-route mirrors (task `032`). **Core's half is not** — no test there pins `embarch_topology::hardware::EnrolledBoard`/`Alert` against the same literals; filed to `embarch-core`'s inbox.
- **The smoke harness ([decisions](decisions/tests.md) 30) is named and unwritten.** The six mocked criteria beside it live in `tests/` ([decisions](decisions/tests.md) 46), with one gap left: the end-to-end half is `#[cfg(unix)]`, so Windows runs the direct tests only. **The gate reports no blind spot of its own**: the client's 28 unit tests sat outside it until that crate became a workspace member ([decisions](decisions/tests.md) 56), and it took a hand sweep to notice. That sweep found nothing else behind it.
- **The study event stream has never met a real embarch-core.** `study-status --follow`/`study_watch` ([decisions](decisions/core-link.md) 48, 49) run only against a mock whose frames *copy* the wire format, so nothing tests the coupling. Debt: `tasks/api/001-sse-client.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50), so branching on a cause means matching prose. **The prerequisite is not in this repo**: Core serves plain text on every non-2xx and its `{code, message, cause}` body (`embarch-core` decision 12) is deferred. Ordered: Core emits codes, the shared client carries one typed, this crate passes it on. **Do not derive a kind from the HTTP status** — a coarser vocabulary, later mistaken for decision 12's.
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads, from its lifted copy of the retired UNC helpers. A different repo's fix.

## Structural limits

- **Nothing can read a firmware version off a DUT.** A declared version describes the tree that was built, so "flashed this run" is the strongest claim — weaker than a measurement.
- **The inbound trust boundary is "whoever can spawn the process"** ([spec.md](spec.md) §6). Fine while an interactive client spawns it; revisit the moment one does not.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39): a remote Core cannot see a local path, and the manifest rides that route into the wall.

## Settled-deferred

Re-read suite-wide; none acquired a new argument.

- **PATH/toolchain preflight** — out of the build path: a build failure surfaces naturally, and preflighting every build costs the common case for an uncommon message. Expected as a `doctor` check.
- **Config fragments / `include`**, so `[core]` is not duplicated per repo. Tolerable for v1: `[core]` is three lines.
- **Config hot-reload** — config loads once; picking up an edit means a reconnect.
- **`serial_log` stays one-shot.** Core's endpoint is itself a bounded capture, so streaming needs Core to grow one first — **not this crate's to decide**.
- **Adding projects stays manual TOML editing** — no mutation tool: the no-database philosophy, and the list barely churns. Except a `zephyr-west` project, which needs no edit to add a board, variant, revision or app.
- **The decision corpus has no headroom left.** `core-link.md` crossed on 2026-09-06 taking decision 55; it is 12,266 B against a 12,288 cap, `tasks/api/026-compact-api.md` filed. `surface.md` crossed the 11,059 B reserve line on 2026-09-07 taking decision 57; it is 11,785 B, `tasks/api/043-compact-api.md` filed. `build.md` crossed it 2026-09-08 amending decision 18; it is 11,134 B, `tasks/api/050-compact-api.md` filed. Two more sit a paragraph short and are **invisible to `check-doc-size.py`** until they cross: `zephyr.md` 11,056, `config.md` 11,008. The wrong answer to the next entry is whichever file has room — leg 015 did that with 96 bytes left.
