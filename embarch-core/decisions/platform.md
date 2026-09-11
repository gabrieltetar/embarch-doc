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

### 4, 14, 15 — One `hw_lock`, `study_lock` for the bench, and a `503` naming the holder on contention
`hw_lock` is held for the whole handler body, so a `/flash` blocks a concurrent `/reset` from *starting* rather than serialising at the probe-rs call level. The dev-bench link is a different physical connection and is arbitrated by `study_lock`; port enumeration opens nothing and takes neither. No new lock was needed — the existing ones already covered it.

**Decision 14 — `503` naming the holder — is now built (`tasks/core/013`), after a period (until 2026-09-06) where this entry asserted it was implemented and it was not.** `hw_lock` stayed `Arc<Mutex<()>>`; a second, plain `std::sync::Mutex<Option<String>>` field (`AppState::hw_holder`) tracks which route currently holds it, set and cleared only by one helper, `acquire_hw_lock`, that every handler now goes through instead of calling `.lock().await` directly. That helper waits up to 500 ms (`HW_LOCK_WAIT_MS`) for the lock via `tokio::time::timeout` over an owned guard; past that it returns `503` with a plain-text body naming the current holder, e.g. `hw_lock held by POST /flash; POST /reset refused after waiting 500ms`, and logs the refusal (`tracing::warn!`) as distinct from a successful, uncontended acquisition (`tracing::info!`) — so `core.log` can tell a wait from a refusal after the fact, which is `tasks/core/013`'s own "Done when" requirement. 500 ms was chosen, not measured, against the bench numbers below (single calls in the low seconds, dominated by fixed overhead) — a value big enough that the common case of a short flash/reset never trips it, small enough that a caller sees the refusal well before its own timeout; a reversal candidate if bench numbers ever show a legitimate hardware op needing longer.

Exercised against the live Windows-service Core at `http://172.22.128.1:4884` [measured 2026-09-06, `core/007`, both boards enrolled and validated], **before this build**: three concurrent `GET /serial-log` on one port, `duration_ms=3000` each, all three returned `200` with a body — no refusal of any kind, consistent with the queueing this decision now replaces. That measurement is history, not current behaviour; `tasks/core/013`'s own test (`api::tests::a_second_caller_is_refused_503_naming_the_holder_under_real_contention`) is host-side, not hardware, and holds `hw_lock` across the 500 ms window itself rather than depending on a live board.

---
