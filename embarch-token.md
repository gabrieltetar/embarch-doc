# EMBARCH_TOKEN: design

**Status:** draft, 2026-07-21. Consolidates token-handling content previously scattered across `embarch-core/design.md` and `embarch-api/design.md` into one canonical doc. Append changes to the Changelog (§9) rather than silently editing history above it.

**This revision documents the design (§2, §3.1) that replaces the insecure `dev-token-change-me` fallback with an auto-generated, machine-wide token file.** Both halves — `embarch-core`'s generation/persistence and `embarch-api`'s discovery — are now code-complete (`embarch-core/milestone-2.md` / `embarch-api/milestone-2.md` §6). **Windows validation is still outstanding**: the Windows-specific pieces (the token file's ACL restriction, and the `sc.exe` service-registry environment fix) were written and reviewed on a Linux machine with no way to exercise them for real — see §3.1/§6 below and `embarch-core/milestone-2.md` §3.5.

## 1. Purpose and scope

`EMBARCH_TOKEN` is the single shared secret that authenticates every caller of `embarch-core`'s HTTP API. This doc is the source of truth for its full lifecycle — generation, storage, transport, security model, rotation, and known gaps — across every component that touches it (`embarch-core`, `embarch-api`). Component-specific docs link here rather than restate this content, per `DOC-PROTOCOL.md` §5.

Out of scope: `embarch-dev-bench`, `embarch-promptu`, `embarch-atlas` are planned/paused with no repo yet and no defined relationship to Core's auth — not considered here until that relationship exists.

## 2. What it is

- A single opaque string, shared across every caller. Not a JWT, not signed, not structured — Core's `auth_middleware` (`api.rs`) does a plain exact-string comparison against every request's `Authorization: Bearer <token>` header.
- **Two ways a value gets chosen, in strict precedence order:**
  1. **Explicit override**, unchanged from today: `EMBARCH_TOKEN` env var on Core, `token`/`token_env` in embarch-api's `[core]` config. If set, it's used as-is — no file is read or written.
  2. **Auto-generated and persisted**, when nothing explicit is set: Core generates a random value on first startup with no `EMBARCH_TOKEN` set, and persists it to a machine-wide file (§3.1) so the same value survives a restart. embarch-api, when neither `token` nor `token_env` is configured, reads that same file. This replaces the old `dev-token-change-me` hardcoded fallback entirely (§5) — no insecure default literal remains in the codebase.
- No expiry, no issued-at, no claims — it's valid until the token file is deleted and Core regenerates one (§7), or an explicit override changes it.

## 3. Where it lives

| Component | How it holds the token | Reference |
|---|---|---|
| `embarch-core` (HTTP server) | Reads `EMBARCH_TOKEN` once at startup (`main.rs`'s `run()`) if set. Otherwise reads the token file (§3.1) if present, or generates one and writes it there if not. No hardcoded fallback literal remains (§5). | `embarch-core/design.md` §6 |
| `embarch-core` CLI (`run` foreground process) | Same resolution as the HTTP server — local CLI operation isn't a separate credential. | `embarch-core/design.md` §2 |
| `embarch-api` | Config's `[core]` table: inline `token` or `token_env` (`token_env` wins if both are set). If neither resolves, falls back to reading the same token file (§3.1) Core uses. If that also isn't found, embarch-api fails to start with a clear error (§8). | `embarch-api/design.md` §4 |

Beyond process memory, embarch-api's own config file (for the inline `token` case) and the token file (§3.1) are the only two places the token is ever written to disk. If stored inline in config, that file should be `chmod 600` and excluded from version control — identical treatment to any other local secret.

### 3.1 The auto-generated token file

**Code-complete on both sides; Windows-specific pieces not yet hardware-validated.** embarch-api's discovery side (same-OS file read, plus WSL2⟷Windows path translation) shipped 2026-07-21 — code-complete, `cargo build`/`cargo clippy -- -D warnings` clean, unit-tested, and the WSL2 translation manually re-verified on a real WSL2 machine (see `embarch-api/milestone-2.md` §6). embarch-core's half — generating and persisting the token file (`token_store.rs`) — also shipped 2026-07-21: `cargo build`/`cargo clippy --all-targets -- -D warnings` clean, and the generate/reuse/explicit-override behavior was verified on a Linux machine (against a temp-path unit test rather than the real `/var/lib/embarch/token`, since that path isn't writable unprivileged there). The Windows ACL restriction and the Windows registry-environment fix (§6) were written and reviewed on that same Linux machine with no way to actually exercise them — still need confirming on real Windows hardware (`embarch-core/milestone-2.md` §3.5).

A canonical, machine-wide path per OS, independent of which user account runs Core or embarch-api — this is what lets an installed Windows service (typically running as a different account than the interactive user) still find the same file, sidestepping §6's service-environment gap for the common case:

- Windows: `%ProgramData%\embarch\token` (typically `C:\ProgramData\embarch\token`).
- Linux/macOS: `/var/lib/embarch/token`.

Core creates the directory and file — with owner-restricted permissions (`chmod 600` on Linux/macOS; on Windows, shelling out to `icacls` to grant only the creating account, `SYSTEM`, and `Administrators`, rather than relying on `ProgramData`'s default inheritance, which is more permissive than a user-profile directory — chosen over the `windows-acl` crate, which is a thin and infrequently-updated wrapper worth avoiding for a security-relevant, currently-Windows-unvalidated operation) — the first time it starts with no explicit `EMBARCH_TOKEN` set, and reuses the existing file on every subsequent startup rather than regenerating. The same value survives a restart, matching today's env-var behavior of not changing unless someone changes it.

**WSL2⟷Windows discovery**, since that's this suite's primary deployment split (§4): embarch-api running under WSL2, talking to a Windows-hosted Core, resolves the real `%ProgramData%` value via a one-time shell-out to the Windows side — rather than hardcoding `C:\ProgramData`, which could be wrong on a machine that customized it — and maps the result through WSL2's `/mnt/<drive>` convention to read the same file.

**Scope limit.** This only bridges same-machine deployments — including the WSL2⟷Windows split, since both sides are really one physical machine — not a genuinely separate host. Core running on a real LAN/Pi deployment (§4; `embarch-core/design.md` §7) has no local file for embarch-api to discover at all; that case still requires explicit `token`/`token_env` config. No filesystem convention can bridge two actual machines (§8).

## 4. Transport

Every request from `embarch-api` to `embarch-core` carries `Authorization: Bearer <token>` (`core_client.rs`'s `.bearer_auth(&token)`), checked via exact-string comparison in Core's `auth_middleware`. There is currently no TLS anywhere in this path — Core's HTTP server is plain HTTP (`embarch-core/design.md` §7's WSL2⟷Windows and future LAN/Pi deployment models). This means the token crosses the network in cleartext on every call; anyone who can observe that traffic (a shared LAN segment, a compromised host on the same network) can read and replay it. Recorded as an open question (§8) — it wasn't an explicit design decision anywhere else.

## 5. Security model

- **Single shared secret, no per-caller identity.** The same token authenticates the embarch-core CLI's local `run` process and any remote embarch-api caller — Core can tell "authorized" from "not," never "which caller." Adequate for the suite's single-engineer scope (`embarch.md` §5); revisit if Core ever needs to distinguish who is calling (§8).
- **No more hardcoded insecure default (§3.1).** Previously, an unset `EMBARCH_TOKEN` fell back to the literal string `dev-token-change-me` with a `tracing::warn!` — a real known-insecure value baked into the binary. That literal is now gone entirely: an unset `EMBARCH_TOKEN` instead generates and persists a real random token to the machine-wide file, and Core logs loudly either way (`tracing::info!` on both generating a new token and reusing an existing one, so which happened is never silent). embarch-api's behavior when nothing resolves also changed: instead of failing to start outright, it checks the same token file before giving up (§8).
- **No TLS** (§4) — the token's confidentiality in transit relies entirely on the trustworthiness of the local network segment it crosses (localhost, WSL2⟷Windows loopback, or eventually a LAN to a Pi).
- **Threat model, explicitly:** this protects against an unauthenticated stranger on the same network hitting Core's endpoints directly. It does **not** protect against anyone with access to the machine(s) running Core or embarch-api (env vars, config files, and process memory are all readable at that level of access), nor against network-level eavesdropping (§4). Appropriate tradeoff for a single-engineer local tool, not an oversight — but worth stating plainly rather than leaving implicit.

## 6. Known gaps

- **`sc.exe`-installed Windows service environment fix is code-complete but Windows-unvalidated.** `service.rs`'s `install()` previously passed `environment: None` unconditionally to `ServiceInstallCtx`, so an installed Windows service ignored whatever `EMBARCH_TOKEN` was set to at install time. Root cause fully diagnosed in `embarch-core/milestone-1-implementation-guide.md`; the fix shipped as part of `embarch-core/milestone-2.md` (folded in alongside the token-file work since both touch `service.rs`): `install()` now passes `environment` through only when an explicit `EMBARCH_TOKEN` was set (fixing Linux/macOS for free via `systemd.rs`/`launchd.rs`'s existing handling), and writes the Windows `Environment` registry value via the `winreg` crate. That registry-write path hasn't been exercised on real Windows hardware yet (`embarch-core/milestone-2.md` §3.5). Since §3.1's auto-generated file has also shipped, this gap only matters for someone who specifically wants an explicit (not auto-generated) token on an installed service — the common case is unaffected, since the machine-wide file doesn't depend on which account the service runs as.
- **WSL2⟷Windows path translation (§3.1) assumes `%ProgramData%` resolves to something WSL2 can reach via `/mnt/<drive>`.** Mitigated by resolving the real value via a shell-out rather than hardcoding `C:\ProgramData`, but an unusual Windows install (e.g. `ProgramData` relocated to a non-`C:` drive not mounted in WSL2) isn't yet an exercised edge case. embarch-api's side of this translation shipped and was exercised against the real `%ProgramData%`/`wslpath` shell-outs on the standard (`C:` drive) case (`embarch-api/milestone-2.md` §6) — the non-standard-drive case above remains untested either way.
- **Native Linux/macOS path (`/var/lib/embarch/token`) ships as code but isn't hardware/service-validated yet.** `embarch-core/milestone-2.md` scopes real validation to the Windows+WSL2 topology actually in use today (matching how `embarch-core/milestone-1.md` scoped board validation), deferring native-Linux/macOS validation as a fast-follow.

## 7. Rotation

No hot-reload on either side — both `embarch-core` and `embarch-api` read the token once at startup, so rotation always requires restarting both. Given the suite's single-engineer, mostly-local scope, this cost is accepted rather than designed around (no dual-token grace window, no config-reload mechanism — see §8).

**To rotate an explicit override** (`EMBARCH_TOKEN` set on Core, or `token`/`token_env` set on embarch-api):

1. Choose a new token value (§2 — no prescribed method, just avoid reusing the old value).
2. Update wherever `embarch-core` reads `EMBARCH_TOKEN` from — the shell environment for a foreground `run`, or the service's environment for an installed service (subject to §6's Windows gap).
3. Restart `embarch-core` so the new value takes effect.
4. Update every `embarch-api` instance's `[core]` config to match before its next call to Core.
5. Restart (or reconnect, for an MCP-spawned instance) `embarch-api`.

**To rotate an auto-generated token** (§3.1): delete the machine-wide token file, restart Core — it regenerates a new one on next startup since the file is now absent — then restart/reconnect every embarch-api instance so it re-reads the new file. Simpler than the explicit case, since there's no value to pick or copy between two places, but the restart requirement and the no-grace-window caveat below still apply identically.

Because there's no grace window, any call made after Core's restart but before every embarch-api instance re-reads the new value will 401 until they agree — acceptable downtime for a single engineer rotating their own token, but worth knowing before doing this mid-session.

This doc doesn't prescribe *when* to rotate (no expiry, no scheduled cadence) — that judgment call is left to the engineer (e.g. suspected exposure, a machine change).

## 8. Open questions / future work

- **Per-caller identity.** One shared token can't distinguish which caller made a request. Revisit if Core ever needs to tell "which caller," not just "authorized or not" (`embarch-core/design.md` §6, §10).
- **No TLS in transit** (§4/§5) — the token crosses the network in cleartext. Not yet assessed against the anticipated LAN/Pi deployment (`embarch-core/design.md` §7); may need revisiting before Core is reachable over a real, less-trusted LAN rather than a WSL2⟷Windows loopback.
- **No rotation grace window / hot-reload.** Both components must restart to pick up a new token, with no dual-token overlap period (§7). Not designed around further since it's an accepted, low-frequency cost — revisit only if rotation ever needs to happen without a stop-the-world restart.
- **No rotation trigger/cadence policy.** §7 covers mechanics only; there's no guidance on when to rotate. Left to engineer judgment for now.
- **Cross-machine (LAN/Pi) token distribution remains unsolved.** §3.1's file-based mechanism only bridges same-machine deployments; a genuinely separate host still needs explicit `token`/`token_env` config, with no auto-discovery. Revisit once a real LAN/Pi deployment (`embarch-core/design.md` §7) actually needs this.
- **Native Linux/macOS path is unvalidated against real hardware/service.** `embarch-core/milestone-2.md` deliberately scoped hardware validation to Windows+WSL2 (today's actual topology); `/var/lib/embarch/token` ships as code without the same real-world confirmation the Windows path gets.

## 9. Changelog

- 2026-07-21 — Initial draft, consolidating token-handling content previously scattered across `embarch-core/design.md` (§6, §10) and `embarch-api/design.md` (§8, §12) into one canonical doc; those docs now point here instead of restating this content.
- 2026-07-21 — Documented the file-based auto-generation design (§2, §3.1): explicit `EMBARCH_TOKEN`/`token`/`token_env` still wins if set; otherwise Core generates and persists a token to a canonical machine-wide path (`%ProgramData%\embarch\token` / `/var/lib/embarch/token`), which embarch-api reads as a fallback discovery step, replacing the `dev-token-change-me` literal entirely (§5). Covers the WSL2⟷Windows split via path translation (§3.1); explicitly does not cover a genuinely separate host (§8). Rotation (§7) and known gaps (§6) updated to match. Implementation tracked in `embarch-core/milestone-2.md` and `embarch-api/milestone-2.md`.
- 2026-07-21 — Noted (§3.1, §6) that embarch-api's half of the target design — token-file discovery, same-OS and WSL2⟷Windows-translated — shipped code-complete (`embarch-api/milestone-2.md` §6). Overall status stays "not yet implemented," since embarch-core's half (generating and persisting the file) hasn't shipped — there's no real file for embarch-api's discovery code to find outside manual/unit testing yet.
- 2026-07-21 — embarch-core's half shipped code-complete (`embarch-core/milestone-2.md` §3.1–3.4): `token_store.rs` (generation, machine-wide file, `chmod 600`/`icacls` permissions) and the `sc.exe` service-environment fix (`winreg`-based registry write). Both halves of the design are now code-complete, so the top-of-doc framing moved from "target design, not yet implemented" to "implemented, Windows-unvalidated" (intro, §3.1, §5, §6). The `dev-token-change-me` literal is confirmed gone from `embarch-core` (§5). What's still open: the Windows-specific pieces (ACL restriction, registry-environment write) were written and reviewed on a Linux machine with no way to exercise them for real — real Windows hardware validation (`embarch-core/milestone-2.md` §3.5) is the remaining gap before this design is fully confirmed end-to-end.
