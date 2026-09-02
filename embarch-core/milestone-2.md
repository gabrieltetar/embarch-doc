# embarch-core: milestone 2 — Token

**Status:** done, 2026-08-11. Milestone 2 (Token) is part of the shipped foundation ([embarch-roadmap.md](../embarch-roadmap.md) §1), released as `v0.1.0`.. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 2. Companion to [embarch-api/milestone-2.md](../embarch-api/milestone-2.md) — that doc covers embarch-api's half of the same milestone (token-file discovery, WSL2⟷Windows path translation). See [design.md](design.md) for the durable architecture record this plan folds decisions back into once it ships, and [embarch-token.md](../embarch-token.md) for the target design this milestone implements (§2, §3.1, §5, §6, §7 there).

## 1. Goal, restated for Core

Milestone 2 exists to close two related gaps in `EMBARCH_TOKEN` handling, both already tracked as known issues before this milestone existed: the insecure `dev-token-change-me` hardcoded fallback (`embarch-token.md` §5), and the diagnosed-but-unapplied Windows-service environment-variable gap (`embarch-token.md` §6, `milestone-1-implementation-guide.md` Prompt 1). embarch-core's part: generate and persist a random token to a canonical machine-wide file when no explicit `EMBARCH_TOKEN` is set, removing the insecure literal default entirely, and — in the same pass, since both touch `service.rs` — apply the already-diagnosed fix so an installed Windows service actually receives an *explicit* `EMBARCH_TOKEN` when one is set at install time.

## 2. Scope for this milestone

- **Platform validation:** Windows (native) + WSL2, matching milestone 1's actual validated topology (Core on Windows, embarch-api in WSL2). The Linux/macOS code path (`/var/lib/embarch/token`) ships in this milestone but is not validated against real hardware or a real systemd/launchd service — that's an explicit fast-follow (see §5).
- **Board:** none specifically — this milestone is auth infrastructure, not board-specific. The end-to-end hardware re-check in §4 reuses `project-a-board` (milestone 1's board) purely as a known-working existing path to re-validate against, not because the token mechanism is board-specific.
- **Folded in from an existing tracked gap:** the `sc.exe` service `ServiceInstallCtx.environment` fix `milestone-1-implementation-guide.md` Prompt 1 already fully diagnosed but never applied (§3.4 below).
- Out of scope: per-caller identity, TLS in transit, rotation grace windows/hot-reload — all still open per `embarch-token.md` §8, none blocking this milestone.

## 3. Steps

### 3.1 Remove the insecure fallback; add token generation

Remove the `dev-token-change-me` literal and its `tracing::warn!` from `main.rs`'s `run()` (`embarch-token.md` §5). Add a token-generation function (e.g. via the `rand` crate — 32 random bytes, hex-encoded) used only when `EMBARCH_TOKEN` is unset and no token file exists yet (§3.2).

### 3.2 Canonical machine-wide token-file path resolution

Add a small module (e.g. `token_store.rs`) that resolves the canonical path per OS (`embarch-token.md` §3.1):

- Windows: `%ProgramData%\embarch\token`
- Linux/macOS: `/var/lib/embarch/token`

On startup, when `EMBARCH_TOKEN` is unset: if the file exists, read and trim it and use that value (`tracing::info!` that an existing token was reused, with the path). If it doesn't exist, generate a new token (§3.1), create the directory if needed, write the file, and log that a new token was generated and where — this is the one moment logging matters most, since there's no `EMBARCH_TOKEN` env var left as a breadcrumb.

### 3.3 Restrictive file/directory permissions at creation time

`%ProgramData%`/`/var/lib` are more permissive by default than a user-profile directory — the file itself must be locked down at creation, not left to the parent directory's inherited permissions (`embarch-token.md` §3.1):

- Linux/macOS: `chmod 600` the file immediately after writing it (`std::os::unix::fs::PermissionsExt`).
- Windows: set an explicit ACL restricting the file to the account that created it plus `Administrators`/`SYSTEM`, rather than trusting `ProgramData`'s default inheritance. Spike the exact mechanism first (a crate like `windows-acl`, or shelling out to `icacls`) — this is the least-precedented part of this milestone and the one most likely to need adjustment once tried for real, on the actual Windows machine.

### 3.4 Apply the diagnosed `sc.exe` service environment fix

Apply the fix `milestone-1-implementation-guide.md`'s Prompt 1 already specifies in full: read `EMBARCH_TOKEN` in `service.rs`'s `install()` before calling `mgr.install(...)`; pass it through `ServiceInstallCtx.environment` (fixes Linux/macOS via `systemd.rs`/`launchd.rs`, which already honor that field); add a Windows-only `winreg`-based write to `HKLM\SYSTEM\CurrentControlSet\Services\com.embarch.core\Environment` (`sc.rs` never reads `ctx.environment` on Windows). This step is only needed for the explicit-token case — once §3.1–§3.3 ship, an installed service with no explicit `EMBARCH_TOKEN` just uses the machine-wide file like any other Core invocation, since that file doesn't depend on which account the service runs as.

### 3.5 Re-validate the flash path end-to-end under the new token mechanism

On the Windows machine, with the board-a attached: uninstall/stop any currently-installed Core service, clear `EMBARCH_TOKEN` from the environment, start `embarch-core.exe run` fresh, and confirm it generates a new token file at `%ProgramData%\embarch\token` with the expected restricted permissions. From WSL2, with embarch-api's config pointed at Core and neither `token` nor `token_env` set, confirm embarch-api's discovery ([embarch-api/milestone-2.md](../embarch-api/milestone-2.md) §3) finds that file and successfully calls `/status` and `/flash` against the real board — the same validation milestone 1 did for the old token model, now proving the new one doesn't regress it. Restart Core a second time and confirm the *same* token is reused (not regenerated) and embarch-api still authenticates without any config change.

## 4. Definition of done

- `dev-token-change-me` no longer exists anywhere in the codebase (§3.1).
- An unset `EMBARCH_TOKEN` generates and persists a token to the canonical machine-wide path on both Windows and Linux/macOS, with restrictive permissions set at creation time (§3.2–§3.3).
- A second startup with no `EMBARCH_TOKEN` reuses the existing file rather than regenerating (§3.2).
- The `sc.exe` service environment fix from `milestone-1-implementation-guide.md` Prompt 1 is applied and confirmed on Windows (§3.4).
- `/status`, `/flash`, `/reset`, `/serial-log` all still succeed against the real board-a board from WSL2, authenticated via the new auto-generated-file mechanism instead of a manually-set `EMBARCH_TOKEN` (§3.5).

## 5. Open questions / risks carried into execution

- Windows ACL-setting is the least-precedented step in this milestone (§3.3) — the exact crate/mechanism isn't chosen yet; may need a spike before the real implementation prompt.
- Native Linux/macOS path (`/var/lib/embarch/token`) ships as code but isn't validated against a real systemd/launchd service or real hardware this milestone — deferred per the platform-scope decision (`embarch-token.md` §6/§8).
- Whether `/var/lib/embarch` is writable by an unprivileged (non-root) user running Core in the foreground on Linux is unconfirmed — if it isn't, Core would need a graceful fallback (e.g. a user-scoped XDG path with a logged warning) not yet designed. Not blocking this milestone since Linux validation is deferred, but worth flagging before Linux is actually exercised for real.
- Depends on `embarch-api/milestone-2.md`'s WSL2⟷Windows path-translation step landing before §3.5 can be validated end-to-end.
