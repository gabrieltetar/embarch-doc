# embarch-api: milestone 1 — Flash

**Status:** done, 2026-08-11. Milestone 1 (Flash) is part of the shipped foundation ([embarch-roadmap.md](../embarch-roadmap.md) §1), released as `v0.1.0`.. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 1. Companion to [embarch-core/milestone-1.md](../embarch-core/milestone-1.md) — that doc covers Core's half of the same milestone, including bringing Core up on Windows and making it reachable from WSL2, which this plan depends on. See [design.md](design.md) for the durable architecture record this plan folds decisions back into once they actually ship. For §3.3 and §3.4 specifically, [milestone-1-implementation-guide.md](milestone-1-implementation-guide.md) turns those two steps into ready-to-run agent prompts against the real source tree.

## 1. Goal, restated for embarch-api

Milestone 1's actual point is letting an engineer go from "firmware source in WSL2" to "flashed onto the board" without ever forwarding the debug probe's USB device into WSL2. embarch-api's part: run `west build` in WSL2 as it does today, get the resulting artifact to the now-Windows-hosted Core (see [embarch-core/milestone-1.md](../embarch-core/milestone-1.md)), and expose the whole thing as MCP tools for Claude Code, as CLI subcommands ([design.md](design.md) §3.10/§5a) for a human with no agent in front of them — the primary human-facing path — and, optionally per §3.6, a `west flash` wrapper around those same subcommands for engineers who'd rather keep typing `west flash` directly.

## 2. Scope for this milestone

- **Board:** `project-a-board` only, matching [embarch-core/milestone-1.md](../embarch-core/milestone-1.md) §2. `project-b-mkr` follows the same steps later.
- **Artifact transfer:** solved via UNC-path pass-through (§3.3 below), not a Core API change, not a shared network mount. This is WSL2-specific — the known gap in `design.md` §9/§12 for a true separate-machine deployment (e.g. Core on a LAN Pi) is not closed by this, only the WSL2⟷Windows-same-PC case this milestone actually needs.
- **Three flashing paths, all in scope:** (a) Claude Code calling embarch-api's existing `build`/`flash`/`build_and_flash` MCP tools, (b) a human calling those same operations directly via embarch-api's new CLI subcommands ([design.md](design.md) §3.10/§5a, §3.4 below), and (c) — optional, kept only for typing-convenience, §3.6 — a human typing `west flash` at a WSL2 terminal via a thin west-runner wrapper around path (b). Going beyond MCP-only was a deliberate scope call for this milestone, so at minimum (a) and (b) need to work.
- Out of scope: config hot-reload, PATH/toolchain preflight validation, any change to Core's `/flash` request contract.

## 3. Steps

### 3.1 Get `west` actually invocable by embarch-api's build subprocess

`west` is not on the bare PATH in this WSL2 environment today (a plain `which west` finds nothing). The real toolchain lives in a project-specific venv — `project-a-fw`'s workspace has one at `/home/dev/Github/project-a-files/workspace/.venv` (confirmed to contain a `west` executable). Since `build_command` runs via `tokio::process::Command` with **no shell interposed** (`design.md` §4), a plain `build_command = ["west", "build", ...]` will fail with a bare "command not found" unless embarch-api's own process can resolve `west`. Two ways to close this, using the config schema's existing escape hatches:

- Point `build_command` at the venv's `west` by absolute path: `["/home/dev/Github/project-a-files/workspace/.venv/bin/west", "build", "-b", "board-a@1/nrf54l15/cpuapp"]`.
- Or use the documented shell escape hatch: `build_command = ["bash", "-lc", "source /home/dev/Github/project-a-files/workspace/.venv/bin/activate && west build -b board-a@1/nrf54l15/cpuapp"]` — needed if `west build` depends on more venv-relative environment state than just `west`'s own path (Zephyr toolchain variables, etc.).
- Try the absolute-path form first; fall back to the shell form if it's not sufficient. Either way, check `scripts/env` (referenced in this project's own `docs/board-a_v2_bringup.md`: `source scripts/env` before `west build`) for anything beyond what venv activation covers — if it sets more, replicate that via embarch-api's `env` config table (additive over its inherited environment, `design.md` §4), not by assuming venv activation alone is equivalent.

### 3.2 Resolve the config TODOs and point at Core — done (2026-07-21)

In embarch-api's config (copied from `config.example.toml` to a real path, per its own header comment):

- Fill in the real `chip` value for `project-a-board` once [embarch-core/milestone-1.md](../embarch-core/milestone-1.md) §3.2 confirms it (currently a placeholder, `"nRF54L15_M33"`).
- Set `[core].base_url` to whatever address [embarch-core/milestone-1.md](../embarch-core/milestone-1.md) §3.4 lands on (dynamic Windows-host IP, or a mirrored-networking `localhost`).
- Set `token_env = "EMBARCH_TOKEN"` (or inline `token`, `chmod 600`'d) to the same value Core was started with.

**Done**: `chip = "nRF54L15"` (§3.2's placeholder was wrong — confirmed via `probe-rs chip list`, no `_M33` variant exists). `base_url = "http://172.29.64.1:4884"` (the dynamic WSL2 host-gateway IP — see [embarch-core/milestone-1.md](../embarch-core/milestone-1.md) §3.4 for the fragility caveat). `token_env = "EMBARCH_TOKEN"` was already set; confirmed working with the token Core was actually launched with.

### 3.3 Add the UNC-path translation for `firmware_path` — code shipped; config value for `project-a-board` still wrong

Core reads `firmware_path` from **its own** local disk (`design.md` §7; `embarch-core/design.md` §4). Core now runs on Windows, but `source_path`/`build_cwd`/`artifact_path` in embarch-api's config are WSL2-side paths — used for running the build itself, and for `build.rs`'s local freshness check. There's currently no field carrying "the same file, as a path Core can open." Add one:

- A new optional per-project config field, e.g. `artifact_path_for_core`, holding the Windows-visible UNC form of the same file. For this machine (WSL distro `Ubuntu-24.04`), `project-a-board`'s artifact resolves to:
  `\\wsl.localhost\Ubuntu-24.04\home\dev\Github\project-a-files\workspace\project-a-fw\app\project-a\build\zephyr\zephyr.hex`
  (`\\wsl$\Ubuntu-24.04\...` is an older but still-supported equivalent, in case any tooling assumes that form instead.)
- When set, the `flash`/`build_and_flash` tools send this value as `firmware_path` in Core's `/flash` call, while `build.rs`'s existence/mtime freshness check keeps using the regular (WSL2-local) `artifact_path` — the two paths point at the same bytes, just as seen from each side.
- When unset, fall back to today's behavior (send the same path Core would also see identically) — keeps this backward-compatible for a same-machine, non-WSL2 deployment.
- Once this ships, fold the decision back into `design.md` §9/§12: this closes the artifact-transfer gap specifically for the WSL2-same-PC case, not the general one (per DOC-PROTOCOL.md §4).

**Status as of 2026-07-21**: the `artifact_path_for_core` field and its use in `cli.rs`'s `flash`/`build_and_flash` were already implemented (per §6's changelog). But the specific UNC path proposed above for `project-a-board` — `...\app\project-a\build\zephyr\zephyr.hex` — **is wrong**: a real `west build` for this project actually wrote its output to `...\project-a-fw\build\zephyr\zephyr.hex` (the west-workspace root, no `app\project-a` segment), discovered while validating §3.5 against real hardware. This means `config.toml`'s `build_cwd = "app/project-a"` / `artifact_path = "build/zephyr/zephyr.hex"` pair — which `resolved_artifact_path()` (`design.md` §6) also uses for the WSL2-local freshness check — resolves to a path that doesn't exist for this project as it's actually being built. The field itself is still unset in the real `config.toml`; hardware validation so far used the CLI's `--firmware-path` override with the correct (workspace-root) UNC path instead of the config field. **Not yet resolved**: whether `build_cwd`/`artifact_path` are simply wrong for this project, or whether the engineer's usual `west build` invocation differs from what `build_command` runs (e.g. always invoked from the workspace root regardless of `build_cwd`) — needs the actual `west build` workflow confirmed before either the config or `resolved_artifact_path()`'s assumption gets changed. See `design.md` §12 for the durable open-question record.

### 3.4 Implement embarch-api's CLI subcommand surface

New work this milestone needs, not just a validation step: build the CLI subcommand interface `design.md` §3.10/§5a describes but that doesn't exist in the source tree yet. This is a prerequisite for both §3.5 (validating the CLI path) and §3.6 (the west-runner wrapper depends on `embarch-api flash`/`build_and_flash` actually existing).

- All six subcommands (`list_projects`, `status`, `build`, `flash`, `build_and_flash`, `reset`, `serial_log`) — the full surface from `design.md` §5a, not just the flash-path subset, so this doesn't need a second implementation pass later.
- New `cli.rs`, thin glue over the same `config.rs`/`build.rs`/`core_client.rs` modules `tools.rs` already calls (`design.md` §10).
- `main.rs` dispatch: no subcommand → MCP stdio server (today's exact behavior, unchanged); a subcommand present → `cli.rs::run` (`design.md` §3.4, §3.10).
- `--json` flag and the exit-code convention (`design.md` §5a): success → `0`; any operation failure → `1` with a stderr message (or the error folded into the `--json` object); `clap`'s own exit code (`2`) for malformed invocations, unchanged.

### 3.5 Validate the MCP and CLI paths end-to-end — partially done (2026-07-21): CLI `flash` proven against real hardware; the rest still open

Point Claude Code (or another MCP client) at the built `embarch-api` binary with `--config <real path>`, **and** separately run the same six operations as direct CLI subcommands (§3.4) against the same config. Against `project-a-board`, both ways:

- `list_projects` — sanity check config loaded correctly.
- `status` — confirms embarch-api reaches Core at all (also embarch-api's own startup check for MCP mode, `design.md` §7 — CLI mode has no eager check, per the same section).
- `build` — a real `west build`, using whichever §3.1 approach was chosen.
- `flash` (against the artifact `build` just produced), then `build_and_flash` as the combined path.
- `reset`, `serial_log`.
- For the CLI path specifically: confirm both the human-readable default output and `--json` output, and confirm exit codes (`0` on success, `1` on a deliberately-forced failure such as an unknown project name).

**What actually ran, against the real board**: `embarch-api --config config.toml flash project-a-board --firmware-path <UNC path>` (CLI, human-readable output, no `--json`) — succeeded, with probe-rs's own log confirming real page-by-page flash programming, not a no-op. This is the first real proof `embarch-api`'s CLI path works end-to-end against hardware through a Windows-hosted Core. This exercise is also what surfaced §3.3's build_cwd/artifact_path bug and `embarch-core`'s `internal_err` error-swallowing bug (`embarch-core/design.md` §4) — the first `flash` attempt (config-only `firmware_path`, no override, and before the `internal_err` fix) failed with an opaque, undiagnosable `500 flashing failed`.

**Not yet done**: `list_projects`, `status`, `build`, `build_and_flash`, `reset`, `serial_log` haven't been exercised via the CLI against this config; nothing has been validated via MCP (no MCP client was involved in this session's validation — it was direct CLI use only, initiated by a human at a terminal, consistent with `design.md` §3.10's "no agent in front of them" path). `--json` output and forced-failure exit codes are also unconfirmed. `build`/`build_and_flash` specifically cannot be expected to work yet given §3.3's open `build_cwd`/`artifact_path` bug.

### 3.6 Make `west flash` work via embarch-api's new CLI, not a from-scratch Core-calling runner

This milestone's scope includes a human typing `west flash` directly at a WSL2 terminal and having it transparently flash via Core — not just Claude-Code-driven MCP calls or the direct CLI (§3.4/§3.5). With the CLI subcommand surface now available, this runner no longer needs to call Core's HTTP API directly — it shells out to `embarch-api flash`/`build_and_flash` (§3.4) instead:

- **What this removes**: the runner no longer needs its own HTTP client, its own bearer-token config, or its own copy of the UNC-path translation logic (§3.3) — it delegates all of that to `embarch-api flash`, which already has (or will have, once §3.3 ships) `artifact_path_for_core` wired through. The runner's Python code becomes: shell out to `embarch-api --config <path> --json flash project-a-board`, parse the JSON result (or just check the exit code — `design.md` §5a), and translate a failure into whatever west's runner API expects for a failed flash.
- **What this does not remove**: the spike into west's custom-runner registration mechanism is unaffected — that part of the plan is about *how west discovers a runner*, not *what the runner does once invoked*, so it's still real, unremoved work (§5's largest unknown risk still applies).
  - **Spike first, don't assume the mechanism.** West's out-of-tree custom-runner registration has shifted across Zephyr versions; confirm the exact extension point (a `ZephyrBinaryRunner` subclass, and how it gets discovered — most likely referenced from the board's `board.cmake` via `board_runner_args`/`set(BOARD_FLASH_RUNNER ...)`, or a west-level plugin registration) against the actual Zephyr version pinned in this workspace's `west.yml`, rather than trusting a remembered API shape that may have moved on.
  - Register it as an additional runner for `board-a` in `board.cmake`, alongside the existing `jlink`/`pyocd`/`nrfutil` entries (additive — it doesn't remove those as a fallback), and confirm `west flash` picks it up by default or via `west flash -r <new-runner-name>`.
  - This is new Python code living in the firmware repo (`project-a-fw`), not in `embarch-api` or `embarch-core` — but it is now a thin wrapper delegating to `embarch-api flash`, not a duplicate implementation of Core's HTTP client.

**Open question — is the west-runner wrapper still worth keeping at all, now that `embarch-api flash project-a-board` is directly callable?** Flagging this explicitly rather than assuming either answer:
- *For keeping it*: real workflow-continuity value (existing muscle memory, board-name tab-completion via west's own machinery), and it now costs little since it's a thin wrapper rather than a duplicate Core client.
- *For dropping it*: `embarch-api flash project-a-board` is barely longer to type than `west flash`, needs no `board.cmake` spike/registration work at all, and sidesteps west-version-specific runner-API churn entirely — the single largest unknown this plan already carries (§5).
- **Recommendation for this milestone**: keep the spike timeboxed (already planned). If the runner-registration mechanism resolves cleanly, keep the thin wrapper. If it's fragile or version-specific, ship `embarch-api flash`/`build_and_flash` directly as the human-facing path for this milestone's definition of done, and treat the west-runner wrapper as a fast-follow rather than a blocker.

## 4. Definition of done

- `west build` for `project-a-board` runs successfully from embarch-api's `build` tool (§3.1–3.2).
- embarch-api's CLI subcommand surface exists and works against the real board — `list_projects`/`status`/`build`/`flash`/`build_and_flash`/`reset`/`serial_log`, both default and `--json` output (§3.4–3.5).
- `build_and_flash` flashes the real board through Windows-hosted Core, called both from Claude Code over MCP and directly via `embarch-api build_and_flash project-a-board` (§3.5).
- A human with no Claude Code in front of them can flash the real board through Core with no `usbipd attach` anywhere in the path, either via `embarch-api flash project-a-board` directly, or — if kept per §3.6's open question — via `west flash`.
- `design.md` §9/§12 updated to reflect the artifact-transfer decision actually shipped (§3.3).

## 5. Open questions / risks carried into execution

- West's custom-runner registration mechanism is unconfirmed against this workspace's pinned Zephyr version until §3.6's spike happens — the single largest unknown in this plan.
- Whether `scripts/env` does more than `.venv` activation covers is unconfirmed until §3.1 is actually tried.
- ~~`artifact_path_for_core` (§3.3) is a new field name proposed here, not yet reflected in `config.rs`'s schema or `design.md` §4's field reference~~ — **implemented** (`design.md` §4), but **not yet populated with a working value for `project-a-board`**: the UNC path this doc originally proposed for it assumed the wrong build-output location. See §3.3's 2026-07-21 update and `design.md` §12 for the durable record. Needs the engineer's actual `west build` invocation pattern confirmed before fixing `build_cwd`/`artifact_path`/`artifact_path_for_core` together.
- Whether the west-runner wrapper (§3.6) is worth keeping at all, now that `embarch-api flash`/`build_and_flash` is directly callable — see §3.6's explicit open question and recommendation.
- **Artifact-freshness check is racy under WSL2 clock jitter** — see `design.md` §12. Reproduced during CLI smoke-testing; could cause `build_and_flash` to spuriously refuse a genuinely fresh build during §3.5's hardware validation if rebuilds happen faster than the observed jitter window. Worth resolving, or at least re-confirming it doesn't reproduce with the real `west build` timing, before relying on `build_and_flash` end-to-end.
