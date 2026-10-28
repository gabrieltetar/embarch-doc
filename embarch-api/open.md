# embarch-api: open questions

**Status:** active, 2026-09-09.

Truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong / unfinished

- **A `[[projects]]` `board` is a hardware fact nothing checks against hardware.** From `build_info.yml`, it names the last build, not the desk's board; violates [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` no longer writes one (`embarch-umbrella` decision 41); older configs do.
- **Windows never runs the smoke-harness tier.** `tests/smoke_harness.rs` ([decisions](decisions/smoke-harness.md) 30, `tasks/api/075`) is `#[cfg(unix)]` (POSIX-shell `build_command`). Windows reaches only the mocked criteria ([decisions](decisions/tests.md) 46).
- **`bootload` has never met a real bootloader** ([decisions](decisions/bootload.md) 80, 81). Mock-tested; the first DUT has no MCUboot yet, so no real `domains.yaml` or upload seen.
- **`bench_exchange` has never met two real consoles** ([decisions](decisions/bench-exchange.md) 89). Mock-tested; cross-console order unmeasured: Core's receive times when sent (`api/147`), else poll-bounded.
- **`study_watch` has met a real embarch-core; the rest has not.** Leg 021: pushed frames and `polled` fallback seen ([decisions](decisions/study-events.md) 48, 49). Unexercised: `study-status --follow`, drop path, `lagged`, reconnect. Debt: `tasks/api/059-sse-client-remaining-observations.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred. **Never derive a kind from the HTTP status.**
- **`artifact_path_for_core` is still tolerated at load.** `embarch-umbrella` stopped scaffolding it 2026-09-13. **Closes with one grep of the real configs** — none carrying it means refuse it by name like `[[projects.targets]]`/`soc_chip_overrides`; not checkable inside the suite: [decisions](decisions/config-retirement.md) 64
- **The test ledger has never met a bench** ([decisions](decisions/ledger.md) 98). Owed: a study run lands a row; `ledger_pending` matches attached roles.
- **The bench lease client has never met a real Core** ([decisions](decisions/lease.md) 90). Mock-tested. An MCP-taken token reaches no CLI or atlas subprocess until exported there; the 900 s default TTL is assumed.
- **`stack` has met only throwaway repos** ([decisions](decisions/stack.md) 96): no real PR stack or forge; hunks spanning two commits go to the newest.
- **`patches` has met only a 3-patch fixture** ([decisions](decisions/patches.md) 92). No real `west patch` manifest, plain-diff entries or merge-heavy history; base passed by hand.

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version names the tree built.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/study-reads.md) 39): a remote Core can't see local paths.
- **`list-targets`' `build_dir_name` names only the default combination** ([decisions/target-json.md](decisions/target-json.md) 77) — a non-default snippet/`extra_args` build gets no name; only its `target.json` (decision 69) attributes it. `embarch-umbrella` decision 26's `--prune` must fold `target.json` in beyond the default build.

## Settled-deferred

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting taxes the common case for an uncommon message. Expected as a `doctor` check.
- **`serial_log` stays one-shot** — Core's endpoint is bounded; streaming needs Core to grow one, **not this crate's call**.
- **The decision corpus runs narrow across `api`** — several `decisions/*.md` sit near the reserve line; never file an entry in whichever file has room instead of its topic's. `tasks/api/*-compact-api.md` tracks which.
