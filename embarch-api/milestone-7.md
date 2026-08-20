# embarch-api: milestone 7 — Flash & Build (real hardware)

**Status:** draft, 2026-08-17. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 1 ("Flash & Build (real hardware)" — filed on disk as `milestone-7` per that doc's filename note, continuing the counter past the shipped foundation's 1–6). Companion to [embarch-core/milestone-7.md](../embarch-core/milestone-7.md) — that doc covers Core's half. See [design.md](design.md) for the durable architecture record this plan folds decisions back into once shipped, and [embarch-umbrella/milestone-6.md](../embarch-umbrella/milestone-6.md)'s 2026-08-12–14 entries for the config/discovery-only groundwork this milestone builds on (real reference-dut repo has four boards — `roadrunner`, `dut_dev`, `ref_nrf54dk`, `dut_demo` — and `roadrunner`'s real product variants only have hardware-revision overlays at `evt1`; that finding is why `discovery = "zephyr-west"` / live `list_targets` exists at all, decision 12).

## 1. Goal, restated for embarch-api

Milestone 1 (Flash) proved the WSL2⟷Windows build→flash chain end-to-end, but only against a placeholder project (`project-a-board`). Milestone 6 (Onboarding) proved `init`/`list_targets`/`doctor` against reference-dut's real, messier config — but never drove a physical flash through it. This milestone closes that gap: run the real chain — `init` → `list_targets` (live discovery, not a hardcoded target) → `build_and_flash`, **config-only, no `--firmware-path` override** — against the real `reference-dut-fw` repo, onto physical hardware, both via direct CLI and via Claude Code over MCP.

Two things this milestone proves for the first time, for *any* project, not just reference-dut:
- **Config-only `build_and_flash`** (no manual `--firmware-path` override) actually works against real hardware. Milestone 1 only proved the CLI `flash --firmware-path <UNC path>` override path; config-only `flash`/`build_and_flash` were marked resolved-in-code but explicitly flagged unvalidated against hardware (`design.md` §12).
- **The MCP path** triggering a real physical flash. Every prior hardware validation in this suite (Milestone 1, and Milestone 6's discovery-chain work) went through the CLI only, invoked directly by a human at a terminal — never through an MCP client.

## 2. Scope for this milestone

- **Repo:** the real `reference-dut-fw` checkout, not `project-a-board` and not Milestone 6's synthetic fixture.
- **Target selection: not hardcoded here.** Per `discovery = "zephyr-west"` (decision 12), embarch-api never stores a static board/variant/revision for this project — §3.3 below runs `list_targets` live and picks from whatever it actually reports as file-backed, the same way a real user would. This plan deliberately does not pre-name a board/variant/revision; doing so would just be re-introducing the static-config assumption decision 12 exists to avoid, and the 2026-08-13 finding already showed that assumption breaks against this exact repo.
- **`embarch init`'s multi-`build_info.yml` ambiguity** (flagged in Milestone 6 — reference-dut has at least two, `roadrunner` production vs. `dut_dev` ad hoc dev): resolve manually for this run if `init` picks the wrong one; the general disambiguation mechanism stays a separate open question (§5), not something this milestone needs to solve generically.
- **Both flashing paths in scope:** (a) direct CLI (`embarch-api build_and_flash ...`), and (b) Claude Code driving the same operation over MCP. Both need config-only `build_and_flash` to succeed against physical hardware.
- ~~Standing instruction — never flash autonomously.~~ **Removed 2026-08-17**, then generalized the same day: full build/test/flash/develop autonomy on the user's own machine, any project. **The one real precondition left is physical, not procedural — the reference-dut board and probe need to actually be connected before §3.5 onward can do anything;** once that's true, §3.1–3.10 run straight through with no per-step go-ahead needed.
- Out of scope: `embarch-dev-bench` (Milestone 2, separate board, separate transport), power sampling (Milestone 4), the west-runner wrapper (Milestone 1 §3.6 territory, not reopened here), config hot-reload, PATH/toolchain preflight validation.

## 3. Steps

### 3.1 Confirm the real reference-dut workspace's toolchain is invocable from embarch-api's build subprocess

Milestone 1 §3.1 solved this for `project-a-fw`'s own venv (`west` not on bare PATH, resolved via absolute venv path or a `bash -lc` shell-activation escape hatch). Reference DUT's workspace may or may not follow the same pattern — confirm rather than assume:

- Locate the reference-dut workspace's own venv/toolchain activation (its own `scripts/env`-equivalent, if one exists, the way `project-a-fw` had `docs/board-a_v2_bringup.md`'s `source scripts/env`).
- Confirm a plain `west build` actually works from a real terminal in this workspace first, before wiring embarch-api's `build_command` to it.
- Use whichever of the two escape hatches (`design.md` §4) the real workspace needs; if it needs more than venv activation covers, replicate via the `env` config table rather than assuming equivalence.

### 3.2 Point embarch-api's config at the real reference-dut project

Add (or correct) a project entry in `config.toml` for the real reference-dut repo:

- `discovery = "zephyr-west"` (decision 12) — no static `board`/`variant`/`revision`/`app` fields; those get live-scanned per call.
- `source_path` / `build_cwd` pointed at the real checkout's actual west-workspace root — confirm this the same way Milestone 1 §3.3 discovered `project-a-board`'s `build_cwd`/`artifact_path` assumption was wrong (a real `west build`'s actual output location, not an assumed one).
- `chip`/`base_url`/`token_env` following Milestone 1 §3.2's pattern — `base_url` likely already set from Milestone 6's real `init` runs against Windows-hosted Core; confirm it's still current (WSL2's host-gateway IP is dynamic across restarts, `embarch-core/milestone-1.md` §3.4).
- `artifact_path_for_core` — this is the UNC-translated path Core will actually open; needs the same real-build-output confirmation as `build_cwd` above, not an assumed value.

### 3.3 Run `embarch init` against the real repo; confirm or correct the target it picks

Per Milestone 6's 2026-08-12/13 finding, `init` derives its guess from whichever `build_info.yml` it finds first — for reference-dut that could be `roadrunner` (production) or `dut_dev` (ad hoc dev board), and picking the wrong one silently configures the wrong project. Run it for real, inspect what it produced, and correct by hand if it didn't land on the intended target. This is a live check, not a formality — Milestone 6 records this going wrong on the first real attempt.

### 3.4 Run `list_targets` live against the real repo; confirm the reported (board, variant, revision, app) tuples

This is the live-discovery step that replaces hardcoding a target in this plan (§2). Run `list_targets` for real against the actual `boards/`/`app/` tree and record what it reports:

- Expect it to surface roughly the shape Milestone 6's 2026-08-13 investigation found by hand — `roadrunner`'s `os_5led`/`os_3led`/`max_5led`/`max_3led` variants, file-backed only at revision `evt1`; `roadrunner`'s bare `cpuapp` (no variant) as a separate, non-product entry — but that investigation was manual and not through this exact code path, so **treat whatever `list_targets` actually reports as the source of truth for this run, not the prior finding.** If it disagrees with the 2026-08-13 finding, that disagreement is itself a result worth recording (§5/§6), not a bug to paper over.
- Pick one reported, unambiguous (board, variant, revision, app) tuple from the live output for §3.5 onward. Prefer a real product variant (`os_*`/`max_*`) over the bare test build if both are reported as file-backed, since the product variant is what an engineer would actually flash day to day.

### 3.5 Resolve chip for the selected target

Call (or let `build`/`flash` internally call) Core's `/resolve-chip` for the selected target's SoC, confirming it resolves to the correct probe-rs chip string (`nRF54L15`, per the SoC family already confirmed in Milestone 1 §3.2 — but confirm this holds for whichever exact board/cpucluster combination `list_targets` reported, not just assumed by family resemblance).

### 3.6 `build` — config-only, real repo

Run `embarch-api build <project> <selected target>` with no path overrides. Confirm the artifact lands where `build_cwd`/`artifact_path` (§3.2) expect — this is exactly the kind of assumption Milestone 1 §3.3 found wrong for `project-a-board`; confirm rather than assume it holds here too.

### 3.7 `flash` — config-only, no `--firmware-path` override, real hardware

The first time this exact path (config-derived `firmware_path`/`artifact_path_for_core`, no manual override) has been proven against physical hardware for any project.

### 3.8 `build_and_flash` — config-only, end-to-end, real hardware

This milestone's centerpiece DoD item: one call, no overrides, real build feeding a real flash against physical reference-dut hardware.

### 3.9 Repeat `build_and_flash` via MCP

Same operation as §3.8, but invoked by Claude Code over MCP instead of directly via CLI — the first MCP-triggered physical flash for any project in this suite.

### 3.10 `reset` / `serial_log` against the real board

Round out the operation surface against real reference-dut hardware — confirm `reset` succeeds and `serial_log` returns real console output (board-specific UART/CDC port, likely different from `project-a-board`'s `COM5`).

## 4. Definition of done

- ~~`embarch init` against the real reference-dut repo lands on (or is manually corrected to) an intended real target — `roadrunner` production, not `dut_dev` (§3.3).~~ **Superseded, not literally met**: `embarch/embarch.toml` already existed pre-configured for `discovery = "zephyr-west"` from Milestone 6 (2026-08-14) — `init` wasn't re-run this session. The user picked `dut_dev@7`/`reference-dut`/`ble-shell` from live `list_targets` output for the actual physical board on the bench, not `roadrunner` — this DoD line's board assumption didn't hold, and live selection (the whole point of decision 12) is what actually happened.
- ✅ `list_targets` reports live, file-backed (board, variant, revision, app) tuples from the real repo (§3.4) — 20 real tuples across `roadrunner`/`dut_dev`/`dut_demo`/`ref_nrf54dk`. **Disagreement with Milestone 6's manual finding, recorded not reconciled**: live output reports `roadrunner`'s real product variants as `os`/`max_5led`/`max_3led` at `evt1`, not `os_5led`/`os_3led`/`max_5led`/`max_3led` as that manual investigation expected.
- ✅ Chip resolves correctly for the selected real target (§3.5) — **but only after a real gap was found and fixed**: the installed Core binary predated `/resolve-chip` entirely (stale since ~Aug 4, missing everything from decision 8 onward). Fixed by syncing current source to the Windows checkout, rebuilding, and deploying — which is also what prompted `embarch-core/design.md` §3 decision 3 (self-elevation) and its `update` subcommand, built and validated live the same session.
- ✅ Config-only `build`, `flash`, and `build_and_flash` (no `--firmware-path` override) all succeed against physical reference-dut hardware (§3.6–3.8) — including against the **installed service**, not just a foreground workaround. Along the way, found a new gap (`embarch-api/design.md` §9, `embarch-decision-reversals.md` row 10): the installed service runs as `LocalSystem` in Session 0, which cannot reach `artifact_path_for_core`'s `\\wsl.localhost` UNC path at all (`os error 67`) — confirmed by direct A/B test, identical call, only Core's run-mode changed. **Fixed the same day**: `flash` now uploads the artifact's bytes (`multipart/form-data`) instead of a path for a `WslHost`/`Remote` Core; `artifact_path_for_core` retired entirely. Re-confirmed live against the installed service after the fix.
- ✅ `build_and_flash` succeeds via MCP as well as CLI (§3.9) — **closed 2026-08-18, fresh session**: `embarch-api` confirmed visible as an MCP server (`~/.claude.json`), `build_and_flash` called for real against `dut_dev@7`/`reference-dut`/`ble-shell` — clean build (fresh artifact, no stale-build refusal), `flashed: true` against the real J-Link (`000852006107`), `chip: "nRF54L15"`. First MCP-triggered physical flash for any project in this suite.
- ✅ `reset`/`serial_log` against the real board (§3.10) — `reset` succeeded repeatedly, including immediately before a `serial_log` call. `serial_log` still returned "no lines captured" on this session's fresh attempt too (8s window, immediately after `reset`) — **root-caused, closed as not-applicable rather than left open**: `embarch-core`'s serial link was never actually meant to reach a DUT's own console UART at all, only `embarch-dev-bench`'s (`embarch-core/design.md` §5, `embarch-decision-reversals.md` row 11) — a premise this very doc's own §3.10 wording ("confirm `serial_log` returns real console output") had wrongly assumed. Incidental, secondary evidence for this specific board: `app/reference-dut/snippets/ble-shell/ble-shell.overlay` explicitly disables `&uart20` and moves console/shell to BLE NUS (`ble-shell.conf`: `CONFIG_UART_CONSOLE=n`, `CONFIG_CONSOLE=n`, `CONFIG_UART_BT=y`) — so even setting design intent aside, this exact build has no physical UART output to capture. The board's *default* (no-`ble-shell`) config does keep `CONFIG_UART_CONSOLE=y` on physical `uart20` per `dut_dev`'s board defconfig, for context.
- ✅ No `usbipd attach`/`usbipd bind` anywhere in the path (same invariant as Milestone 1).
- ✅ `design.md` §12/§9 updated to reflect real-hardware findings — §9's UNC/Session-0 correction, §12's MCP/config-only-flash item closed, and decision 26 corrected for the `serial_log`/DUT-UART finding above.

## 5. Open questions / risks carried into execution

- **`embarch init`'s multi-`build_info.yml` disambiguation** (Milestone 6) has no general mechanism — moot for this run (config pre-existed from Milestone 6), but the underlying gap stays open for future repos with the same shape.
- ~~**Whether reference-dut's real workspace toolchain matches `project-a-board`'s venv pattern**~~ — confirmed yes: the existing `west_binary` venv-path config worked without changes, real `build`s succeeded.
- ~~**Whether `list_targets`'s live output matches Milestone 6's manual 2026-08-13 finding**~~ — resolved 2026-08-18: it doesn't, exactly (see §4) — recorded, not reconciled.
- ~~**`build_cwd`/`artifact_path`/`artifact_path_for_core` for the real reference-dut workspace**~~ — resolved: build/flash/build_and_flash all succeeded, artifacts landed where `zephyr-west` discovery computed them.
- ~~**The installed-service artifact-transfer gap**~~ (§4, `embarch-api/design.md` §9) — resolved the same day it was found: `flash` uploads bytes instead of a path for `WslHost`/`Remote`, confirmed against the real installed service, no foreground workaround needed.
- ~~**`serial_log` returning empty**~~ — resolved 2026-08-18: not a capture-timing bug or a silent-shell quirk to distinguish — `serial_log` against a DUT's own console UART was never an intended `embarch-core` capability at all, only `embarch-dev-bench`'s link is (§4, `embarch-decision-reversals.md` row 11). `reference-dut-fw`'s `ble-shell` snippet also independently has no physical UART output, but that's secondary color, not the root cause.
- ~~**§3.9 (MCP) still unexercised**~~ — resolved 2026-08-18: fresh Claude Code session, `build_and_flash` confirmed visible and called for real against `dut_dev@7`/`reference-dut`/`ble-shell` (§4).

## 6. Changelog

- 2026-08-18 — **Milestone closed out, fresh session**: §3.9 (MCP-triggered `build_and_flash`) succeeded for real against `dut_dev@7`/`reference-dut`/`ble-shell` — first MCP-triggered physical flash for any project in this suite. §3.10's `serial_log` empty-capture item root-caused and closed: `embarch-core`'s serial link was never actually meant to reach a DUT's own console UART, only `embarch-dev-bench`'s — a design-intent correction (`embarch-decision-reversals.md` row 11, `embarch-core/design.md` §5, this doc's own decision 26 corrected), not a bug fix. Incidental, secondary finding: this project's `ble-shell` snippet also independently disables the DUT's physical UART in favor of BLE NUS. All DoD lines in §4 now closed.
- 2026-08-18 — Executed against real hardware for the first time: §3.4–3.8 all ran for real (target `dut_dev@7`/`reference-dut`/`ble-shell`, user-selected from live `list_targets`, not `roadrunner` as originally assumed). Found and fixed a stale-Core-binary gap (missing `/resolve-chip`), then found and fixed the installed-service artifact-transfer gap (Session 0 can't reach `\\wsl.localhost` — fixed by uploading bytes instead of a path, `embarch-api/design.md` §9) the same day. Re-confirmed `build`/`flash`/`build_and_flash`/`reset` against the real, installed service after the fix. §3.9 (MCP) and §3.10's `serial_log` half remain open — see §4/§5 for the honest state of each DoD line.
- 2026-08-17 — Removed the "ask before running this step" gates on §3.7–3.9 and §2/§5's standing-instruction notes: the user removed the never-flash-autonomously rule globally (any project, build and flash both). §3.6–3.9 now run the same way §3.1–3.5 always could.
- 2026-08-17 — §2 updated: the rule generalized further into "full autonomy except a physical action." Named the one real precondition this milestone still has — the board/probe physically connected — as distinct from any remaining procedural gate, since there no longer is one.
- 2026-08-17 — Initial draft, scoping embarch-api's half of Milestone 1 (Flash & Build, real hardware). Deliberately does not pre-select a board/variant/revision — §3.4 runs `list_targets` live against the real repo and picks from its actual output, per `discovery = "zephyr-west"` (decision 12) and the user's explicit correction that hardcoding a target here would just reintroduce the assumption decision 12 exists to avoid.
