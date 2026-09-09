# embarch-core decisions: Platform, process, and locking

**Status:** active, 2026-09-02.

How Core runs at all: language and framework choices, how it installs and elevates as an OS
service, and what serialises hardware access. Auth, binding, configuration, and keeping the
documented HTTP surface in agreement with the router are [decisions/auth.md](auth.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Platform and process

### 1, 2, 7, 17 — Rust, probe-rs as a library, Axum, `spawn_blocking`, and CI everywhere
probe-rs is called as a library, not shelled out to: no subprocess or output-scraping, and typed errors. Axum for one toolchain across the stack and because its `State`/middleware model fits `AppState`. Both probe-rs and `serialport` are synchronous, so every hardware call goes through `spawn_blocking` — a slow flash must never stall the runtime. The intent was that CI run `build`/`clippy -D warnings`/`test` per push on every repo that lacked it, plus a `native_sim` build for dev-bench, which would have caught a real Zephyr API breakage before it was found by hand.

**Corrected 2026-09-08 — "CI everywhere" was never built, and this repo is one of the repos it was not built in.** Measured across all nine repos: `embarch-core` has `release.yml` and **no test workflow at all**, so nothing runs `build`/`clippy`/`test` on a push here. The only per-push Rust test workflows in the suite are `embarch-study-designer`'s and `embarch-topology`'s; `embarch-doc` has `docs-ci.yml`. The `native_sim` job is `embarch-dev-bench`'s own decision 9 and is also unbuilt — that repo has never had a `.github` directory. **The heading keeps "CI everywhere" because the decision *numbers* are permanent ([DOC-CONVENTIONS.md](../../DOC-CONVENTIONS.md)) and this title is how they are cited elsewhere — nothing has ever decided whether a title may be amended, so this is a choice rather than a rule, and it is recorded as one. What the heading names is what was decided; the clause above is not what exists.** What actually checks a change in this repo is [embarch.md](../../embarch.md) §5's table: the fleet's own merge gate ([the protocol](../../../embarch-fleet/protocol.md) §10), run per branch by a supervisor, and nothing else.

### 3 — `service-manager` for install; self-elevation here rather than in every caller
One code path registers `run` as a systemd unit, launchd job, or Windows Service. **Registration is not the whole job:** systemd and launchd accept "the process stayed alive", but Windows kills a start that has not called `StartServiceCtrlDispatcherW` and reported `SERVICE_RUNNING` within 30 s, however healthy the process — so `run` attempts the real SCM handshake first on Windows and falls back to foreground only when SCM did not launch it. All four subcommands **self-elevate**, because a human running `embarch-core install` and `embarch-umbrella` shelling out to it hit the same wall; fixing it here fixes both callers. Re-launching the *same already-running binary* adds no new trust step. Hence also `update <new-exe>`: stop, rename aside (Windows will not overwrite a running image), copy, start, roll back on failure.

*Rejected:* printing the command for a human to re-run elevated — a transcription-error opportunity, and it left updating an installed Core with no supported path at all.

---


## Locking

### 4, 14, 15 — One `hw_lock`, `study_lock` for the bench, and a `503` that was never built
`hw_lock` is held for the whole handler body, so a `/flash` blocks a concurrent `/reset` from *starting* rather than serialising at the probe-rs call level. The dev-bench link is a different physical connection and is arbitrated by `study_lock`; port enumeration opens nothing and takes neither. No new lock was needed — the existing ones already covered it.

**Decision 14 — `503` naming the holder — is designed and not implemented, and this entry asserted the opposite until 2026-09-06.** The proof is the type, not a grep: `hw_lock` is `Arc<Mutex<()>>`, and a `Mutex<()>` has nowhere to put a holder, so a refusal naming one was never built and no refactor can hide that it wasn't. Consistently, all eight acquisitions are `state.hw_lock.lock().await`, which cannot refuse; `try_lock`, `503` and `SERVICE_UNAVAILABLE` appear nowhere in `src/` in either the git checkout or the rsync tree the Windows service is built from; the router has exactly one `.layer` (`auth_middleware`) and no tower load-shed, concurrency-limit or timeout layer, which are the only stock sources of a `503` nobody wrote. **So contention queues, silently and without a deadline** — precisely the behaviour this entry named as the problem it had fixed: "the second caller used to block silently on the mutex, indistinguishable from Core being unresponsive". It still does.

Exercised against the live Windows-service Core at `http://172.22.128.1:4884` [measured 2026-09-06, `core/007`, both boards enrolled and validated]: three concurrent `GET /serial-log` on one port, `duration_ms=3000` each, **all three returned `200` with a body — no refusal of any kind**, and none failed port-busy either. Wall time was 17.96 s against 8.38 s for a single identical call; that is consistent with serialisation but does **not** on its own exclude the client having issued them sequentially, since ~5.4 s of the single call is fixed overhead. The queueing claim rests on `.lock().await`, which must wait; the wall clock corroborates and does not carry it. Settling the ordering costs nothing and needs no hardware — the three handler entry/exit stamps in `core.log`. **Nothing observed names a holder, because there is no refusal for a holder to be named in.** Whether to build the `503` or retire decision 14: `tasks/core/013`.

---
