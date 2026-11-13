# embarch-api: open questions

**Status:** active, 2026-09-09.

Truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong / unfinished

- **A `[[projects]]` `board` is a hardware fact nothing checks against hardware.** From `build_info.yml`, it names the last build, not the desk's board; violates [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` no longer writes one (`embarch-umbrella` decision 41); older configs do.
- **Windows never runs the smoke-harness tier.** `tests/smoke_harness.rs` ([decisions](decisions/smoke-harness.md) 30, `tasks/api/075`) is `#[cfg(unix)]` (POSIX-shell `build_command`). Windows reaches only the mocked criteria ([decisions](decisions/tests.md) 46).
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred. **Never derive a kind from the HTTP status.**
- **`artifact_path_for_core` is still tolerated at load.** `embarch-umbrella` stopped scaffolding it 2026-09-13. **Closes with one grep of the real configs** — none carrying it means refuse it by name like `[[projects.targets]]`/`soc_chip_overrides`; not checkable inside the suite: [decisions](decisions/config-retirement.md) 64
- **`stack` has met only throwaway repos** ([decisions](decisions/stack.md) 96): no real PR stack or forge; hunks spanning two commits go to the newest.
- **`patches` has met only a 3-patch fixture** ([decisions](decisions/patches.md) 92). No real `west patch` manifest, plain-diff entries or merge-heavy history; base passed by hand.
- **Real-hardware and real-toolchain verification debts** (bootload, `bench_exchange`, `study_watch`, ledger, lease, build verdict, `build --each`) live in [open/bench-verification.md](open/bench-verification.md), moved verbatim.

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version names the tree built.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/study-reads.md) 39): a remote Core can't see local paths.
- **`list-targets`' `build_dir_name` names only the default combination** ([decisions/target-json.md](decisions/target-json.md) 77) — a non-default snippet/`extra_args` build gets no name; only its `target.json` (decision 69) attributes it. `embarch-umbrella` decision 26's `--prune` must fold `target.json` in beyond the default build.

## Settled-deferred

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting taxes the common case for an uncommon message. Expected as a `doctor` check.
- **`serial_log` stays one-shot** — Core's endpoint is bounded; streaming needs Core to grow one, **not this crate's call**.
- **The decision corpus runs narrow across `api`** — several `decisions/*.md` sit near the reserve line; never file an entry in whichever file has room instead of its topic's. `tasks/api/*-compact-api.md` tracks which.
