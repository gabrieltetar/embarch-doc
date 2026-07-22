# embarch-api: milestone 2 — Token

**Status:** draft, 2026-07-21. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 2. Companion to [embarch-core/milestone-2.md](../embarch-core/milestone-2.md) — that doc covers Core's half of the same milestone (generating and persisting the machine-wide token file, plus the unrelated-but-folded-in `sc.exe` service-environment fix), which this plan depends on. See [design.md](design.md) for the durable architecture record this plan folds decisions back into once it ships, and [embarch-token.md](../embarch-token.md) for the target design this milestone implements (§2, §3.1, §5–§8).

## 1. Goal, restated for embarch-api

Milestone 2's point for embarch-api: when neither `[core].token` nor `token_env` is configured, discover the same machine-wide token file Core generates ([embarch-core/milestone-2.md](../embarch-core/milestone-2.md)) instead of failing to start outright. Since this suite's actual deployment is Core-on-Windows / embarch-api-in-WSL2 (`design.md` §9), the real work here is the WSL2⟷Windows path translation — resolving Core's Windows-side canonical path from inside a WSL2 process and reading it through the `/mnt/<drive>` mount, not just a same-OS file read.

## 2. Scope for this milestone

- **Platform validation:** Windows-hosted Core reached from WSL2, matching milestone 1's actual validated topology and `embarch-core/milestone-2.md`'s same platform-scope decision. The native-Linux-to-Linux case (no translation needed, just read `/var/lib/embarch/token` directly) ships as code but isn't validated against a real Core instance this milestone.
- **Board:** none specifically — this milestone is auth infrastructure. §3.5's hardware re-check reuses `project-a-board` purely as a known-working existing path, matching `embarch-core/milestone-2.md` §2.
- Out of scope: any change to `build.rs`, the CLI subcommand surface, or `artifact_path_for_core` — milestone 2 touches only `core_client.rs`/`config.rs`/`main.rs`'s token-resolution path.
- **Genuinely separate-host (LAN/Pi) discovery is explicitly not in scope** (`embarch-token.md` §3.1's scope limit) — this milestone only closes the WSL2⟷Windows-same-PC gap and the native-same-OS case, not a real network deployment.

## 3. Steps

### 3.1 Add token-file discovery as a fallback in config resolution

Today, `config.rs`'s load fails outright if neither `[core].token` nor `token_env` resolves to a value (`design.md` §4). Change this to a three-step resolution, mirroring Core's own precedence (`embarch-token.md` §2):

1. `token` (inline) or `token_env` (env var name) — unchanged, `token_env` wins if both set.
2. If neither resolves, attempt to read the machine-wide token file (§3.2/§3.3 for how the path is found).
3. If that also fails (file not found, unreadable, or path resolution itself fails), config load fails with a clear error naming both things the engineer can do: set `token`/`token_env` explicitly, or start Core so it generates the file — not just today's generic "no token configured" message.

### 3.2 WSL2⟷Windows token-file discovery

The primary case this milestone needs to actually work, matching `embarch-token.md` §3.1's WSL2⟷Windows discovery design:

- Detect that embarch-api is running under WSL2 (e.g. `/proc/version` containing `microsoft`/`WSL`, or `$WSL_DISTRO_NAME` being set — confirm which signal is more reliable once implementing).
- Resolve the real Windows-side `%ProgramData%` value via a one-time shell-out (e.g. `cmd.exe /C echo %ProgramData%` or `powershell.exe -Command "$env:ProgramData"`) rather than hardcoding `C:\ProgramData`, in case a machine customized it.
- Translate the result's drive letter to WSL2's `/mnt/<drive>` mount form (e.g. `C:\ProgramData\embarch\token` → `/mnt/c/ProgramData/embarch/token`) — use `wslpath` if invoking it is simpler/more robust than hand-parsing the drive letter, but confirm it's actually available in this environment before depending on it.
- Cache the resolved path for the process lifetime — no need to re-shell-out per call, only once at startup during config resolution (§3.1).

### 3.3 Native same-OS discovery (no translation needed)

When embarch-api is not running under WSL2 (native Linux/macOS, or — not yet a real topology, but cheap to support the same way — native Windows), just read the canonical path directly (`/var/lib/embarch/token` or `%ProgramData%\embarch\token` per OS, matching `embarch-core/milestone-2.md` §3.2's path resolution exactly — consider sharing this path-resolution logic via a small shared reference between the two docs/repos rather than reimplementing it slightly differently on each side, even though there's no shared crate between embarch-core and embarch-api today).

### 3.4 Clear failure messaging

When discovery fails entirely (§3.1 step 3), the error surfaced at startup (MCP mode's fail-fast check, `design.md` §7) and at CLI dispatch time should name the exact path(s) checked and both remediation options, e.g.: `"No token configured: set [core].token or token_env in config, or start embarch-core (it will generate one at %ProgramData%\embarch\token / /mnt/c/ProgramData/embarch/token) and retry."` — concrete enough that an engineer isn't left guessing which of the two mechanisms broke.

### 3.5 Re-validate the flash path end-to-end under the new token mechanism

Paired with [embarch-core/milestone-2.md](../embarch-core/milestone-2.md) §3.5: with Core running fresh (no `EMBARCH_TOKEN` set, auto-generated file in place) and embarch-api's config updated to have neither `token` nor `token_env` set, confirm `embarch-api status` and `embarch-api flash project-a-board` (CLI, real hardware) succeed via the new discovery path (§3.2). Also confirm the MCP path's startup connectivity check (`design.md` §7) still passes under the same discovery-only config.

## 4. Definition of done

- `config.rs` (or wherever token resolution lives) tries `token`/`token_env`, then the machine-wide file, before failing (§3.1).
- WSL2⟷Windows path translation correctly resolves Core's real `%ProgramData%`-based path and reads it from WSL2 (§3.2).
- Native same-OS discovery reads the canonical path directly with no translation (§3.3) — implemented, not hardware-validated this milestone (§2).
- A config with none of `token`/`token_env`/a discoverable file fails with a message naming both remediation paths (§3.4).
- `embarch-api status` and `embarch-api flash project-a-board` succeed against the real board with no `token`/`token_env` configured, authenticated purely via file discovery (§3.5).

## 5. Open questions / risks carried into execution

- The WSL2-detection signal (`/proc/version` vs. `$WSL_DISTRO_NAME`) isn't chosen yet — confirm which is more reliable once implementing (§3.2).
- Whether `wslpath` is a safe dependency to shell out to, or whether hand-parsing the drive letter is more robust, is unconfirmed until tried (§3.2).
- Depends on `embarch-core/milestone-2.md`'s token-file generation actually existing before this milestone's discovery logic can be validated against a real file — sequencing matters if both are worked in parallel.
- Native same-OS discovery (§3.3) is unvalidated against a real Core instance this milestone, matching the platform-scope decision in `embarch-core/milestone-2.md` §2/§5.

## 6. Changelog

- 2026-07-21 — Initial draft, scoping embarch-api's half of Milestone 2 (Token).
- 2026-07-21 — §3.1–3.4 shipped (code-side): `token_discovery.rs` added and wired into `CoreConfig::resolve_token()`; `cargo build`/`cargo clippy -- -D warnings` clean, unit tests pass, and the WSL2⟷Windows translation (§3.2) was exercised for real on this machine (genuinely under WSL2), not just in isolation. Folded back into `design.md` §4/§7/§8/§10/§13. §3.5 (hardware re-validation against a real Core instance generating the file) and this doc's Definition of Done (§4) remain open until that's run.
