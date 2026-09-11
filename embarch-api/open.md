# embarch-api: open questions

**Status:** active, 2026-09-09.

Truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong / unfinished

- **A `[[projects]]` `board` is a hardware fact nothing compares against the hardware.** Derived from `build_info.yml`, it names the last build, not the board on the desk — a mismatched revision costs a day of bring-up, violating [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` stopped writing one unconfirmed (`embarch-umbrella` decision 41); older configs assert one, comparing to hardware is unbuilt.
- **The alert/enrolled-board response types were unpinned mirrors**: `link_port_interface` (`embarch-topology` decision 20) reached Core's wire body and the client mirror silently dropped it. `api`'s half is pinned against a JSON literal now (task `032`); **Core's is not** — filed to `embarch-core`'s inbox.
- **The smoke harness ([decisions](decisions/tests.md) 30) is named, unwritten.** Six mocked criteria live in `tests/` ([decisions](decisions/tests.md) 46); end-to-end is `#[cfg(unix)]`, Windows gets direct tests.
- **`study_watch` has met a real embarch-core; the rest has not.** Bench, leg 021: pushed live frames and `transport: polled` fallback both seen ([decisions](decisions/study-events.md) 48, 49). `study-status --follow`, drop path, `lagged`, reconnect: unexercised. Debt: `tasks/api/059-sse-client-remaining-observations.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred. **Never derive a kind from the HTTP status.**
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads — a different repo's fix. Why no by-name load refusal, unlike `[[projects.targets]]`/`soc_chip_overrides`: [decisions](decisions/shape.md) 64

## Owed decisions

- **`list_serial_ports`/`list-serial-ports` (task `041`) shipped with no numbered decision**, under that leg's burndown rule against new numbers. Owed: the no-param `GET /serial-ports` pair, why `serial_log` has no automatic fallback onto it (several ports can enumerate; only a human or the caller knows the DUT's console), and the correction to `interfaces/tools-build-flash.md`'s stale `GET /dev-bench/port` claim (moved there from `tools.md` 2026-09-10, `tasks/api/053`). File in `decisions/tool-wrapping.md` once out of reserve (`tasks/api/047`), or its successor. **Still open, and not this crate's to fix: `embarch init` never writes `serial_port` at all** — `embarch-umbrella` decision 17's minimal discovery schema does not include it, so every config reaches this surface without one.

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version names the tree built, not a measurement.
- **Inbound trust is "whoever can spawn the process"** ([spec.md](spec.md) §6) — fine while spawned interactively.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39): a remote Core can't see local paths.

## Settled-deferred

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting costs the common case for an uncommon message. Expected as a `doctor` check.
- **Config fragments/`include`** (`[core]` is 3 lines) **and hot-reload** (loads once; an edit needs a reconnect).
- **`serial_log` stays one-shot** — Core's endpoint is bounded; streaming needs Core to grow one, **not this crate's call**.
- **Adding projects stays manual TOML editing** — no mutation tool, the list barely churns; `zephyr-west` needs none for board, variant, revision, app.
- **The decision corpus runs narrow across `api`** — several `decisions/*.md` sit a paragraph from the reserve line, invisible to `check-doc-size.py` until crossed; the wrong answer to the next entry is whichever file has room, not the one whose topic it is (leg 015, 96 B left). `tasks/api/*-compact-api.md` tracks which crossed.
