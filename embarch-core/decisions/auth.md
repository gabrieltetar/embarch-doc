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

**What this decision does not claim**: it does not assert what the default ACL concretely grants on any given Windows machine — `embarch-token.md` already flags that as unmeasured — only that Core deliberately never restricts it, and why.

### 11 — An optional `core.toml`, narrowed to `bind`/`port`, still design-only
Every knob is env-var-only, and passing environment to an installed service is the bug class decision 3 already paid for. **Never written.** Narrowed when `embarch-topology` abandoned the four `dev_bench_*` knobs outright: a config value left stale wins over reality exactly as capably as an env var left stale, and enrollment is the fix either way.

---
