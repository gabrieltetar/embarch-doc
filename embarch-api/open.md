# embarch-api: open questions

**Status:** active, 2026-09-09.

Truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong / unfinished

- **A `[[projects]]` `board` is a hardware fact nothing compares against the hardware.** Derived from `build_info.yml`, it names the last build, not the board on the desk — a mismatched revision costs a day of bring-up, violating [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` stopped writing one unconfirmed (`embarch-umbrella` decision 41); older configs assert one, comparing to hardware is unbuilt.
- **Windows never runs the smoke-harness tier.** `tests/smoke_harness.rs` ([decisions](decisions/tests.md) 30, `tasks/api/075`) is `#[cfg(unix)]` — its fixture's `build_command` is a POSIX shell one-liner, the same limit decision 46's four end-to-end tests already have. A Windows `cargo test` run reaches the mocked criteria in `tests/` ([decisions](decisions/tests.md) 46) only.
- **`study_watch` has met a real embarch-core; the rest has not.** Bench, leg 021: pushed live frames and `transport: polled` fallback both seen ([decisions](decisions/study-events.md) 48, 49). `study-status --follow`, drop path, `lagged`, reconnect: unexercised. Debt: `tasks/api/059-sse-client-remaining-observations.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred. **Never derive a kind from the HTTP status.**
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads — a different repo's fix. Why no by-name load refusal, unlike `[[projects.targets]]`/`soc_chip_overrides`: [decisions](decisions/shape.md) 64
- **`embarch init` never writes `serial_port` at all** — `embarch-umbrella` decision 17's minimal discovery schema does not include it, so every config reaches [`list_serial_ports`/`serial_log`](decisions/hardware-selection.md) 70 without one configured. **Not this crate's to fix.**

## Owed decisions

None currently — the one open here (`list_serial_ports`, task `041`) is now [decisions/hardware-selection.md](decisions/hardware-selection.md) 70 (`tasks/api/063`).

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version names the tree built, not a measurement.
- **Inbound trust is "whoever can spawn the process"** ([spec.md](spec.md) §6) — fine while spawned interactively.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/study-reads.md) 39): a remote Core can't see local paths.

## Settled-deferred

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting costs the common case for an uncommon message. Expected as a `doctor` check.
- **Config fragments/`include`** (`[core]` is 3 lines) **and hot-reload** (loads once; an edit needs a reconnect).
- **`serial_log` stays one-shot** — Core's endpoint is bounded; streaming needs Core to grow one, **not this crate's call**.
- **Adding projects stays manual TOML editing** — no mutation tool, the list barely churns; `zephyr-west` needs none for board, variant, revision, app.
- **The decision corpus runs narrow across `api`** — several `decisions/*.md` sit a paragraph from the reserve line, invisible to `check-doc-size.py` until crossed; the wrong answer to the next entry is whichever file has room, not the one whose topic it is (leg 015, 96 B left). `tasks/api/*-compact-api.md` tracks which crossed.
