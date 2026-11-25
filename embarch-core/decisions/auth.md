# embarch-core decisions: Auth, binding, and configuration

**Status:** active, 2026-09-02.

What authenticates a request, and what it binds to and is configured by: the token, the bind
address, and `core.toml`, plus the `%ProgramData%` ACL. Keeping the documented HTTP surface in
agreement with the router is [decisions/route-sweep.md](route-sweep.md), split out verbatim
2026-09-28 (`tasks/core/046`) — three mechanisms reading `build_router`'s source, none of them
about authentication itself. Language/runtime, process installation, and locking are
[decisions/platform.md](platform.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).


## Auth, binding, configuration

### 5, 6 — Bearer-token auth, and a `127.0.0.1` default widened explicitly by `embarch-umbrella setup`
Core may be reachable over a real network, so an unauthenticated surface is unacceptable even at single-engineer scale; a plain exact-string compare, deliberately not OAuth or anything session-based. The bind default was originally `0.0.0.0`, since reachability is the point. Reversed: `0.0.0.0` plus no TLS plus a static token plus `/flash` reading an arbitrary local path, in a process that may run as `LocalSystem`, is a posture nobody had assessed **as a whole** — each piece was documented, never composed. Two gaps surfaced on implementation: the default had never changed in code, and `service::windows::run_service` **hardcoded `"0.0.0.0"`**, discarding whatever `--bind` a service was registered with, so every Windows deployment had been wide open regardless of any flag.

### 53 — `%ProgramData%\embarch` stays at its default ACL; only the token file is locked down
`token_store.rs`'s `icacls` call ([embarch-token.md](../../embarch-token.md)) names the token file path only, never the directory. **This is deliberate, not an unhardened corner**: `embarch-topology` decision 23 puts its own `enrollment.toml` one level down in that same directory, and relies on the directory's untouched default ACL to let both the Core service account and an unprivileged interactive CLI create and read files there. Locking the directory down to the creating account, `SYSTEM` and Administrators — the same treatment the token file gets — would close exactly the access `embarch-topology` needs from the unprivileged side, and nothing in Core's own build would catch that: `token_store.rs` has no test touching the parent directory's ACL, only the file's.

**A future author tightening this must not do it by narrowing the directory.** The token file already carries the real secret and already gets owner-restricted permissions; the directory holds no secret of its own; only a sibling file inside it does. If the directory's permissiveness is ever judged to be a problem, the fix belongs to whatever new file is added under it needing protection — a lockdown of its own, the way the token file has one — not to the directory as a whole, since `embarch-topology` and anything else sharing `%ProgramData%\embarch` has no way to ask Core for an exception once the directory itself is locked.

**Amended 2026-11-25 (`tasks/core/153`):** with `run --service`, the signing key, both logs and the identity store move into `<data dir>/store/`, the one thing the elevated install protects: [decision 129](#129--core-keeps-a-service-store-or-a-development-store-and-says-which). This decision's reasoning is unchanged for what stays in the directory: the token files and `study_results/`.

**What this decision does not claim**: it does not assert what the default ACL concretely grants on any given Windows machine — `embarch-token.md` already flags that as unmeasured — only that Core deliberately never restricts it, and why.

### 109 — Two tokens, an agent's and a person's, and the scope each request carries
HIL has to say who did each act, and Core had one full-authority secret. At first start Core writes **two** tokens and authenticates a request with either. **The agent's stays exactly what it was**: `EMBARCH_TOKEN`, else `<data dir>/token`, so `embarch-core-client`'s discovery and every caller in `embarch-api`, `embarch-ui` and `embarch-atlas` work unchanged. **The person's is `EMBARCH_PERSON_TOKEN`, else `<data dir>/person-token`** beside it: 64 hex characters, written on first use, `0600` (Linux) or the same `icacls` lockdown (decision 53, unvalidated on Windows for this second file), reused on restart. Two equal values are refused at start, since a scope that cannot be told apart is no scope.

`auth_middleware` resolves the match into `token_store::Scope` (`Agent` or `Person`) and puts it in the request's extensions; a handler takes `scope: Scope` as an extractor, and a request that reached one is always authenticated, so a missing extension is a `500` naming the unwired router. It is also a `debug` line in `core.log`. **Nothing is refused by scope in this unit**: Core is unattested, so the identity routes stay on the agent's token, labelled the agent's, and both tokens reach every route. The lease (decision 93) is **not** scoped: its holder is the `holder` string a caller names, and it neither reads nor records the scope. M1.5 to M1.8 stamp scope into records and refuse by it; they are why it is carried now.

**Measured:** the unit tests: each token records its own scope, neither is refused, a call with neither is `401`, and the file pair is generated once and reused. **Assumed:** the Windows ACL on `person-token`.

### 129 — Core keeps a service store or a development store, and says which
One data directory held the token pair, `signing-key`, both logs, `study_results/` and the identity store, whatever ran Core, so a development Core on a scratch port shared the attested Core's key and tokens. The HIL design (`embarch-doc/notes/hil/12-prevention.md`, "The root of trust") wants the attested Core's key in a store only its own account opens, and a development Core with a store of its own. `run` takes two flags, chosen once at start (`token_store::init_store`, before any path is read) and mutually exclusive:

- **`--service`**: the store is `<data dir>/store/`. **Core never creates it**; a missing store is a start failure naming the elevated install (which this unit does not change). It holds `signing-key`, `public-key` (the raw public key as 64 hex, written beside the key whenever it is missing, so an older key gets one), `run-log.jsonl`, `call-log.jsonl`, `flashed-images.jsonl` and `topology/` (`embarch-topology`'s `hardware::paths::set_data_dir`). The token pair and `study_results/` stay in `<data dir>`.
- **`--store <dir>`**: the same, plus the token pair and `study_results/`, all in `<dir>`, created if missing. Two such Cores have two keys. `EMBARCH_TOKEN` and `EMBARCH_PERSON_TOKEN` still override the files, as before.
- **Neither**: today's layout exactly, so a source-installed service runs unchanged until the first signed install. It reports `development`.

`GET /status` gains `mode` (`service` only with `--service`), `keyid` and `study_in_flight` (the id held in `study_lock`, null when idle or during the dev-bench hello). `POST /auth/challenge` answers with `mode` beside the signature, **outside the signed frame**: it is Core's own word, not something the frame vouches for. The signed record's `observed` gains `mode`. `public-key` hashes (SHA-256) to `keyid`.

**Left alone on purpose:** `logs/` stays in `<data dir>`, because tracing starts before the flags are parsed and a log needs no protection from the account that reads it. `RunLog` now carries its results root apart from its store, since the two no longer share a parent with `--service`.

**Measured:** unit tests on the path of each layout, the missing-store refusal, `public-key` against `keyid`, two stores' differing keys, and `/status` and the challenge fields. **Assumed:** that the elevated install will create `store/` with an ACL only the service account and administrators open; and the Windows-only parts, whose whole-crate `cargo check --target x86_64-pc-windows-msvc` cannot run here (see the task's debt).

### 11 — An optional `core.toml`, narrowed to `bind`/`port`, still design-only
Every knob is env-var-only, and passing environment to an installed service is the bug class decision 3 already paid for. **Never written.** Narrowed when `embarch-topology` abandoned the four `dev_bench_*` knobs outright: a config value left stale wins over reality exactly as capably as an env var left stale, and enrollment is the fix either way.

---
