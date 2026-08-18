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

- `embarch init` against the real reference-dut repo lands on (or is manually corrected to) an intended real target — `roadrunner` production, not `dut_dev` (§3.3).
- `list_targets` reports live, file-backed (board, variant, revision, app) tuples from the real repo (§3.4) — and any disagreement with Milestone 6's manual 2026-08-13 finding is recorded, not silently reconciled.
- Chip resolves correctly for the selected real target (§3.5).
- Config-only `build`, `flash`, and `build_and_flash` (no `--firmware-path` override) all succeed against physical reference-dut hardware (§3.6–3.8) — the first time this exact path is proven on real hardware for any project.
- `build_and_flash` succeeds via MCP as well as CLI (§3.9) — the first MCP-triggered physical flash for any project.
- `reset`/`serial_log` succeed against the real board (§3.10).
- No `usbipd attach`/`usbipd bind` anywhere in the path (same invariant as Milestone 1).
- `design.md` §12 updated to reflect config-only `build_and_flash` and the MCP path both now proven against real hardware, no longer open items.

## 5. Open questions / risks carried into execution

- **`embarch init`'s multi-`build_info.yml` disambiguation** (Milestone 6) has no general mechanism — this run resolves it by hand if needed, but the underlying gap (which file is "the real one" when a repo has several) stays open for future repos with the same shape.
- **Whether reference-dut's real workspace toolchain matches `project-a-board`'s venv pattern** is unconfirmed until §3.1 actually runs.
- **Whether `list_targets`'s live output matches Milestone 6's manual 2026-08-13 finding** is unconfirmed until §3.4 actually runs against the real tree through this exact code path (that finding was investigated by hand, not through `list_targets` itself).
- **`build_cwd`/`artifact_path`/`artifact_path_for_core` for the real reference-dut workspace** are unconfirmed — Milestone 1 found `project-a-board`'s assumed value wrong only by attempting a real build; the same could happen here (§3.2/§3.6).

## 6. Changelog

- 2026-08-17 — Removed the "ask before running this step" gates on §3.7–3.9 and §2/§5's standing-instruction notes: the user removed the never-flash-autonomously rule globally (any project, build and flash both). §3.6–3.9 now run the same way §3.1–3.5 always could.
- 2026-08-17 — §2 updated: the rule generalized further into "full autonomy except a physical action." Named the one real precondition this milestone still has — the board/probe physically connected — as distinct from any remaining procedural gate, since there no longer is one.
- 2026-08-17 — Initial draft, scoping embarch-api's half of Milestone 1 (Flash & Build, real hardware). Deliberately does not pre-select a board/variant/revision — §3.4 runs `list_targets` live against the real repo and picks from its actual output, per `discovery = "zephyr-west"` (decision 12) and the user's explicit correction that hardcoding a target here would just reintroduce the assumption decision 12 exists to avoid.
