# embarch-core decisions: Platform, process, and auth

**Status:** active, 2026-09-02.

How Core runs at all: language and framework choices, how it installs and elevates as an OS service, what authenticates a request, what it binds to, and what serialises hardware access.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Platform and process

### 1, 2, 7, 17 — Rust, probe-rs as a library, Axum, `spawn_blocking`, and CI everywhere
probe-rs is called as a library, not shelled out to: no subprocess or output-scraping, and typed errors. Axum for one toolchain across the stack and because its `State`/middleware model fits `AppState`. Both probe-rs and `serialport` are synchronous, so every hardware call goes through `spawn_blocking` — a slow flash must never stall the runtime. CI runs `build`/`clippy -D warnings`/`test` per push on every repo that lacked it, plus a `native_sim` build for dev-bench, which would have caught a real Zephyr API breakage before it was found by hand.

### 3 — `service-manager` for install; self-elevation here rather than in every caller
One code path registers `run` as a systemd unit, launchd job, or Windows Service. **Registration is not the whole job:** systemd and launchd accept "the process stayed alive", but Windows kills a start that has not called `StartServiceCtrlDispatcherW` and reported `SERVICE_RUNNING` within 30 s, however healthy the process — so `run` attempts the real SCM handshake first on Windows and falls back to foreground only when SCM did not launch it. All four subcommands **self-elevate**, because a human running `embarch-core install` and `embarch-umbrella` shelling out to it hit the same wall; fixing it here fixes both callers. Re-launching the *same already-running binary* adds no new trust step. Hence also `update <new-exe>`: stop, rename aside (Windows will not overwrite a running image), copy, start, roll back on failure.

*Rejected:* printing the command for a human to re-run elevated — a transcription-error opportunity, and it left updating an installed Core with no supported path at all.

---


## Auth, binding, configuration

### 5, 6 — Bearer-token auth, and a `127.0.0.1` default widened explicitly by `embarch-umbrella setup`
Core may be reachable over a real network, so an unauthenticated surface is unacceptable even at single-engineer scale; a plain exact-string compare, deliberately not OAuth or anything session-based. The bind default was originally `0.0.0.0`, since reachability is the point. Reversed: `0.0.0.0` plus no TLS plus a static token plus `/flash` reading an arbitrary local path, in a process that may run as `LocalSystem`, is a posture nobody had assessed **as a whole** — each piece was documented, never composed. Two gaps surfaced on implementation: the default had never changed in code, and `service::windows::run_service` **hardcoded `"0.0.0.0"`**, discarding whatever `--bind` a service was registered with, so every Windows deployment had been wide open regardless of any flag.

### 42 — The bearer-token sweep derives its route list from `build_router`'s own source
Decision 5's invariant is "every route, no exceptions", and it was checked by one hand-written `*_requires_the_bearer_token` test per route. Two lists that must agree, with nothing asserting they do: by 2026-09-06 the router registered 26 paths and 12 had a test — the 14 without included **every** `/study*` route, the newest and largest surface added since the tests were written. Nothing was actually unauthenticated; the *evidence* for the invariant had quietly become half of it.

So the list is no longer written twice. `registered_route_paths()` scans `include_str!("api.rs")` for `.route("` literals, and `every_registered_route_has_an_auth_case` asserts set equality in both directions against a table of `(method, path, concrete URI)` — a registered path with no row fails, and a row for a path no longer registered fails too. Two table-driven sweeps then drive every row through the real router with no `Authorization` header and with a wrong token, expecting `401`. The old individual tests are folded into the table rather than left beside it, since two lists is the shape that drifted in the first place.

Reading the source text rather than the `Router` is not a shortcut: axum exposes no route iterator, so a built `Router` cannot be asked what it serves. The scan asserts it found a plausible number of registrations, so a broken scan fails loudly instead of vacuously passing. **A lexical scan is not a Rust parse, and the residual is one-sided:** a route registered in a form the scan does not match — split across lines by rustfmt, or a router assembled in another file — is invisible to *both* directions of the set-equality check and passes silently, while the `> 20` guard catches only a wholly broken scan. A *reformatted existing* route still fails loudly, through the stale-row direction; **only a newly added one is at risk.** All 26 registrations are one contiguous block in `api.rs` today, with no `nest`/`merge`/`fallback` anywhere in the crate, which is what keeps this cheap. Nothing here touches hardware — `auth_middleware` is a `.layer` on the whole router and rejects before axum routes the request, so no handler runs. `embarch-api` reached the same conclusion for its own machine-readable surface (its decision 54); this is the `embarch-core` half, and neither repo depends on the other for it.

### 11 — An optional `core.toml`, narrowed to `bind`/`port`, still design-only
Every knob is env-var-only, and passing environment to an installed service is the bug class decision 3 already paid for. **Never written.** Narrowed when `embarch-topology` abandoned the four `dev_bench_*` knobs outright: a config value left stale wins over reality exactly as capably as an env var left stale, and enrollment is the fix either way.

---


## Locking

### 4, 14, 15 — One `hw_lock`, `study_lock` for the bench, and a `503` that was never built
`hw_lock` is held for the whole handler body, so a `/flash` blocks a concurrent `/reset` from *starting* rather than serialising at the probe-rs call level. The dev-bench link is a different physical connection and is arbitrated by `study_lock`; port enumeration opens nothing and takes neither. No new lock was needed — the existing ones already covered it.

**Decision 14 — `503` naming the holder — is designed and not implemented, and this entry asserted the opposite until 2026-09-06.** The proof is the type, not a grep: `hw_lock` is `Arc<Mutex<()>>`, and a `Mutex<()>` has nowhere to put a holder, so a refusal naming one was never built and no refactor can hide that it wasn't. Consistently, all eight acquisitions are `state.hw_lock.lock().await`, which cannot refuse; `try_lock`, `503` and `SERVICE_UNAVAILABLE` appear nowhere in `src/` in either the git checkout or the rsync tree the Windows service is built from; the router has exactly one `.layer` (`auth_middleware`) and no tower load-shed, concurrency-limit or timeout layer, which are the only stock sources of a `503` nobody wrote. **So contention queues, silently and without a deadline** — precisely the behaviour this entry named as the problem it had fixed: "the second caller used to block silently on the mutex, indistinguishable from Core being unresponsive". It still does.

Exercised against the live Windows-service Core at `http://172.22.128.1:4884` [measured 2026-09-06, `core/007`, both boards enrolled and validated]: three concurrent `GET /serial-log` on one port, `duration_ms=3000` each, **all three returned `200` with a body — no refusal of any kind**, and none failed port-busy either. Wall time was 17.96 s against 8.38 s for a single identical call; that is consistent with serialisation but does **not** on its own exclude the client having issued them sequentially, since ~5.4 s of the single call is fixed overhead. The queueing claim rests on `.lock().await`, which must wait; the wall clock corroborates and does not carry it. Settling the ordering costs nothing and needs no hardware — the three handler entry/exit stamps in `core.log`. **Nothing observed names a holder, because there is no refusal for a holder to be named in.** Whether to build the `503` or retire decision 14: `tasks/core/013`.

---
