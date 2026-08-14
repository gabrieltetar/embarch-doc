# embarch: features

**Status:** draft, 2026-07-17. Hand-maintained. Todo rows should stay in sync with the source design docs' own "open questions" sections rather than duplicating their detail — link back, don't restate.

| Feature | Sub-project | Status | Notes |
|---|---|---|---|
| `GET /status` — list connected debug probes | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `POST /flash` — flash a chip from a local firmware path | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `POST /reset` — reset a chip | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `GET /serial-log` — bounded-duration serial capture | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `GET /dev-bench/port` — dev-bench serial-port auto-detection (SEGGER VID + product/serial/interface match), plus the `detect-dev-bench` CLI subcommand | embarch-core | Shipped, no real dev-bench yet | `embarch-core/design.md` §4, §5, §10; implements `embarch-dev-bench/design.md` §3 decision 12 |
| `POST /resolve-chip` — Zephyr SoC name → probe-rs chip target string, validated against probe-rs's own target registry | embarch-core | Shipped | `embarch-core/design.md` §3 decision 8, §4; `embarch-api/design.md` §3 decision 12 |
| Bearer-token auth on all endpoints | embarch-core | Shipped | `embarch-core/design.md` §6 |
| `hw_lock` — serializes all hardware access | embarch-core | Shipped | `embarch-core/design.md` §3.4 |
| Cross-platform service install/control (`install`/`uninstall`/`start`/`stop`) | embarch-core | Shipped — all four need elevation on every OS, not just Windows | `embarch-core/design.md` §3.3 |
| `list_projects` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `status` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `build` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `flash` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `build_and_flash` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `reset` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `serial_log` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `list_targets` MCP tool + `list-targets` CLI subcommand — live target discovery for a `discovery = "zephyr-west"` project, or a `[[projects.targets]]` menu for a `static` one | embarch-api | Shipped | `embarch-api/design.md` §3 decision 12, §5, §5a |
| `discovery = "zephyr-west"` — live, per-call `board`/`variant`/`revision`/`app` resolution (file-backing-validated against real overlay/defconfig files) on `build`/`flash`/`build_and_flash`/`reset`, instead of a static hand-maintained `[[projects]]` entry | embarch-api | Shipped — verified against a synthetic fixture + a real Core; not yet revalidated against the real healthband repo itself | `embarch-api/design.md` §3 decision 12; `embarch-umbrella/milestone-6.md` §3.9 |
| CLI subcommand interface (`build`/`flash`/`build-and-flash`/`reset`/`serial-log`/`list-projects` — kebab-case, unlike the snake_case MCP tools above) | embarch-api | Shipped | `embarch-api/design.md` §3.10, §5a |
| Artifact freshness check (mtime before/after build) | embarch-api | Shipped | `embarch-api/design.md` §6; WSL2 wall-clock jitter fix applied 2026-07-22 (§12), not yet hardware-revalidated |
| Per-project build concurrency lock | embarch-api | Shipped | `embarch-api/design.md` §6 |
| PATH/toolchain preflight validation | embarch-api | Todo — now expected to land as `embarch-umbrella`'s `doctor` check, not in the build path | `embarch-api/design.md` §12, §11a; `embarch-umbrella/design.md` §5 |
| Config hot-reload | embarch-api | Todo | `embarch-api/design.md` §12 |
| `artifact_path_for_core` UNC-path pass-through (WSL2-same-PC artifact transfer) | embarch-api | Shipped, validated against real hardware | `embarch-api/design.md` §4, §9; not yet populated for `project-a-board` specifically — see §12 |
| Artifact-transfer over a real network (Core on a genuinely separate machine, e.g. a future Pi) | embarch-api / embarch-core | Todo | `embarch-api/design.md` §9, §12; `embarch-core/design.md` §7, §10 |
| Multi-probe selection (beyond "first probe found") | embarch-core | Todo | `embarch-core/design.md` §5, §10 |
| ESP-IDF UART-bootloader flashing via `esptool` fallback | embarch-core | Todo | `embarch-core/design.md` §10 |
| Per-caller identity (beyond one shared token) | embarch-core | Todo | `embarch-core/design.md` §6, §10 |
| Auto-generated, machine-wide token file (replaces `dev-token-change-me` fallback) | embarch-core | Shipped, Windows hardware-unvalidated | `embarch-token.md` §2, §3.1, §5; `embarch-core/milestone-2.md` §3.5 |
| `sc.exe` service `EMBARCH_TOKEN` passthrough fix | embarch-core | Shipped, Windows hardware-unvalidated | `embarch-token.md` §6; `embarch-core/milestone-2.md` §3.4/§3.5 |
| Token-file discovery + WSL2⟷Windows path translation | embarch-api | Shipped — WSL2⟷Windows translation exercised for real; end-to-end re-check against a live Core-generated file not yet done | `embarch-token.md` §3.1; `embarch-api/milestone-2.md` §3.5 |
| Stimulus/sensing hardware-in-the-loop rig | embarch-dev-bench | Proposed | See `embarch-roadmap.md` Next |
| Shared `app/` firmware: COBS/postcard serial protocol, `Hello`/`HelloAck`, `LogLine`, stubbed study FFI | embarch-dev-bench | Shipped, `native_sim` only | `embarch-dev-bench/design.md` §2, §3 decisions 7/16/20 |
| BLE bridge: advertise, connect (central/peripheral), GATT read/write/notify/indicate/subscribe/stream-capture | embarch-dev-bench | Shipped, compiles for nRF54L15DK — never run on a board | `embarch-dev-bench/design.md` §3 decision 16, §4 |
| Shared `no_std` study data-types library (BLE interaction + power profiling) | embarch-study-designer | Shipped — not yet a Cargo dependency of `embarch-core`/`embarch-api` | `embarch-study-designer/design.md` §3, §4; `embarch-study-designer/milestone-3.md` |
| `embarch-core` ↔ `embarch-dev-bench` serial bridge (new endpoints) | embarch-core | Proposed, design-only | `embarch-study-designer/design.md` §5 |
| Study-running MCP tool + CLI subcommand | embarch-api | Proposed, design-only | `embarch-study-designer/design.md` §6 |
| `embarch setup` — one-time per-machine setup with topology auto-detection | embarch-umbrella | Shipped — smoke-tested on WSL2 for all three classes; the Windows-side install command has never been run | `embarch-umbrella/design.md` §3 decisions 3/6/7, §8 |
| `embarch init` — scaffold a firmware repo's `embarch/` config + local MCP registration, touching nothing tracked | embarch-umbrella | Shipped — verified against a repo shaped like the real one; run for real against the healthband repo | `embarch-umbrella/design.md` §3 decisions 10/12/13, §7 |
| `embarch init`/`doctor` support for `discovery = "zephyr-west"` — scaffolds the minimal schema instead of guessing one board; `doctor` checks 7-9 branch on `discovery` | embarch-umbrella | Shipped — verified against a synthetic fixture + a real Core; not yet revalidated against the real healthband repo itself | `embarch-umbrella/design.md` §3 decision 17; `embarch-umbrella/milestone-6.md` §3.9 |
| Topology auto-detection (ordered loopback → WSL2 gateway → explicit host, `401` counts as finding Core) | embarch-umbrella | Shipped — verified on WSL2 and against a mock, never against a real Core | `embarch-umbrella/design.md` §3 decisions 6/15; `embarch-umbrella/milestone-6.md` §3.2 |
| `embarch status` — where Core is, `--json` | embarch-umbrella | Partial — reports reachability, address, and topology class; no probe list and no token check yet | `embarch-umbrella/design.md` §3 decision 11 |
| `embarch doctor` — verify the whole chain, `--json` | embarch-umbrella | Shipped — all twelve checks plus `--json`; smoke-tested against a live Core and the real healthband repo's config | `embarch-umbrella/design.md` §5; `embarch-umbrella/milestone-6.md` §3.4 |
| `embarch up` / `down` — fallback Core start/stop, including across the WSL2⟷Windows boundary | embarch-umbrella | Shipped — never started a real Core; the WSL2→Windows path prints the command rather than elevating | `embarch-umbrella/design.md` §3 decisions 4/7 |
| Suite release archive (all three binaries, four targets) | embarch-umbrella | Shipped — real `v0.1.0` releases across all three repos, plus a real assembled `suite-v0.1.0` archive that `doctor` check 1 has validated a manifest against | `embarch-umbrella/design.md` §3 decision 14; `embarch-umbrella/milestone-6.md` §3.7 |
| `base_url = "auto"` — Core address resolved per-process at first use, retiring the stale WSL2 gateway IP | embarch-api | Shipped — verified against a mock and with Core down; never against a real Core | `embarch-api/design.md` §3.11, §4, §7 |
| `start` / `stop` CLI subcommands | embarch-core | Shipped — smoke-tested on Linux, not on Windows/macOS | `embarch-core/design.md` §2, §3.3; `embarch-umbrella/milestone-6.md` §3.6 |
| EmbArch UI — see whether Core is up and drive operations by hand, no agent involved | *(unnamed)* | Proposed | `embarch-umbrella/design.md` §10; see `embarch-roadmap.md` Later |
| Curated firmware-specific skills/prompt library | embarch-promptu | Proposed | See `embarch-roadmap.md` Next |
| Agent-facing codebase structural analysis (successor to the old GUI's static analysis) | *(unnamed)* | Proposed | See `embarch-roadmap.md` Later |

## Changelog

*Older entries archived to [embarch-features.changelog-archive.md](embarch-features.changelog-archive.md).*

- 2026-08-14 — Added four new Shipped rows for Zephyr/west live target discovery, implemented across all three repos same day: `embarch-core`'s `POST /resolve-chip`, `embarch-api`'s `list_targets` tool/subcommand and `discovery = "zephyr-west"` itself, and `embarch-umbrella`'s matching `init`/`doctor` support. Also updated the `embarch init` row's caveat — it's now been run for real against the healthband repo, not just a repo shaped like it.
- 2026-08-11 — Corrected status drift: the `embarch doctor` and suite-release-archive rows were still marked `Proposed, design-only` even though `embarch-umbrella/milestone-6.md` §3.4 (doctor, done 2026-08-10) and §3.7 (release CI, done 2026-08-11, all three repos released clean) had both closed — violated `DOC-PROTOCOL.md` §5's "sub-project doc and suite-level docs should never disagree about status" rule. Flipped both to Shipped with links to the specific milestone section rather than restating its detail here.
- 2026-08-05 — `embarch init` flipped to Shipped. `doctor` is now the only unimplemented command.
- 2026-08-05 — `embarch setup` and `embarch up`/`down` flipped to Shipped, with status wording kept specific about what has *not* been exercised: no real Core has been started by either, and the Windows-side install/start commands are printed but have never been run.
- 2026-08-05 — `embarch-core`'s `start`/`stop` flipped to Shipped, and the service-install row now records that elevation is required on every OS (a systemd system unit wants root/polkit, not just Windows wanting Administrator).
- 2026-08-05 — `base_url = "auto"` flipped to Shipped (`embarch-umbrella/milestone-6.md` §3.5). Corrected the CLI-subcommand row, which had listed snake_case names the CLI has never actually had — `clap`'s derive renames to kebab-case, so it's `list-projects`, not `list_projects` (`embarch-api/design.md` §5a).
- 2026-08-05 — Split the `doctor`/`status` row now that they've diverged in status: topology auto-detection is Shipped (verified on WSL2 and against a mock, never against a real Core), `status` is Partial (reachability/address/class, no probe list or token check yet), `doctor` stays design-only.
- 2026-08-05 — Added eight design-only rows for Milestone 6 (Onboarding): five for the new `embarch-umbrella` sub-project (`setup`, `init`, `doctor`/`status`, `up`/`down`, the suite release archive), one each for `embarch-api`'s `base_url = "auto"` and `embarch-core`'s `start`/`stop`, and one Proposed row for the future EmbArch UI. Note what did *not* move: `embarch-api`'s PATH/toolchain-preflight row stays `Todo` but its Notes now point at umbrella's `doctor` as the intended home rather than at a build-path check.
- 2026-08-04 — Added three rows for work that shipped on the Core↔dev-bench hop: `embarch-core`'s dev-bench port auto-detection (`GET /dev-bench/port` + `detect-dev-bench`), and two `embarch-dev-bench` firmware rows (the shared serial/protocol application, and the BLE bridge now covering the full `Action`/`GattOperation` surface). Status wording is deliberately specific about *how far* each is verified — `native_sim` only, or uncompiled — since neither has met real hardware — the BLE-bridge row was updated the same day once `workspaces/nordic` was fetched and built, moving it from "uncompiled" to "compiles for nRF54L15DK, never run on a board." See each design doc's own open questions. Also corrected pre-existing status drift on the `embarch-study-designer` row, still marked `Proposed, design-only` even though `embarch.md` §3 and that crate's own changelog have recorded it as implemented and tested since 2026-07-29 (`DOC-PROTOCOL.md` §5's never-disagree rule).

