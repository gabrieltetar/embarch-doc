# embarch: features

**Status:** draft, 2026-07-17. Hand-maintained. Todo rows should stay in sync with the source design docs' own "open questions" sections rather than duplicating their detail — link back, don't restate.

| Feature | Sub-project | Status | Notes |
|---|---|---|---|
| `GET /status` — list connected debug probes | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `POST /flash` — flash a chip from a local firmware path | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `POST /reset` — reset a chip | embarch-core | Shipped | `embarch-core/design.md` §4 |
| `GET /serial-log` — bounded-duration serial capture | embarch-core | Shipped | `embarch-core/design.md` §4 |
| Bearer-token auth on all endpoints | embarch-core | Shipped | `embarch-core/design.md` §6 |
| `hw_lock` — serializes all hardware access | embarch-core | Shipped | `embarch-core/design.md` §3.4 |
| Cross-platform service install (`install`/`uninstall`) | embarch-core | Shipped | `embarch-core/design.md` §3.3 |
| `list_projects` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `status` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `build` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `flash` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `build_and_flash` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `reset` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| `serial_log` MCP tool | embarch-api | Shipped | `embarch-api/design.md` §5 |
| CLI subcommand interface (`build`/`flash`/`build_and_flash`/`reset`/`serial_log`/`list_projects`) | embarch-api | Shipped | `embarch-api/design.md` §3.10, §5a |
| Artifact freshness check (mtime before/after build) | embarch-api | Shipped | `embarch-api/design.md` §6; WSL2 wall-clock jitter fix applied 2026-07-22 (§12), not yet hardware-revalidated |
| Per-project build concurrency lock | embarch-api | Shipped | `embarch-api/design.md` §6 |
| PATH/toolchain preflight validation | embarch-api | Todo | `embarch-api/design.md` §12 |
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
| Shared `no_std` study data-types library (BLE interaction + power profiling) | embarch-study-designer | Proposed, design-only | `embarch-study-designer/design.md` §3, §4; `embarch-study-designer/milestone-3.md` |
| `embarch-core` ↔ `embarch-dev-bench` serial bridge (new endpoints) | embarch-core | Proposed, design-only | `embarch-study-designer/design.md` §5 |
| Study-running MCP tool + CLI subcommand | embarch-api | Proposed, design-only | `embarch-study-designer/design.md` §6 |
| Curated firmware-specific skills/prompt library | embarch-promptu | Proposed | See `embarch-roadmap.md` Next |
| Agent-facing codebase structural analysis (successor to the old GUI's static analysis) | *(unnamed)* | Proposed | See `embarch-roadmap.md` Later |

## Changelog

- 2026-07-27 — Added three Proposed/design-only rows for Milestone 3 (Study Designer): the shared `embarch-study-designer` data-types library, `embarch-core`'s new dev-bench serial bridge, and `embarch-api`'s future study-running MCP tool/CLI subcommand. All point at `embarch-study-designer/design.md` rather than restating detail, per this file's own header note.
- 2026-07-22 — Corrected status drift: three Milestone-2 (Token) rows were still marked `Todo` even though `embarch-token.md` and both design docs' changelogs recorded milestone-2 as code-complete (Windows-unvalidated) since 2026-07-21 — violated `DOC-PROTOCOL.md` §5's "sub-project doc and suite-level docs should never disagree about status" rule. Flipped to `Shipped, Windows hardware-unvalidated` (or the WSL2-specific equivalent) to match. Also annotated the artifact-freshness-check row with the WSL2 wall-clock-jitter fix applied the same day (`embarch-api/design.md` §12).
- 2026-07-17 — Initial draft.
- 2026-07-20 — Updated doc references for the `embarch-core/design.md` / `embarch-api/design.md` subfolder restructure.
- 2026-07-20 — Added the CLI subcommand interface row (Todo), per `embarch-api/design.md` §3.10/§5a.
- 2026-07-20 — Pointed the CLI subcommand interface row at `embarch-api/milestone-1-implementation-guide.md`, the new file with the actual implementation prompts; row stays Todo until that guide's prompts actually ship (see the guide's Prompt 5, which flips this to Shipped).
- 2026-07-20 — CLI subcommand interface shipped (`milestone-1-implementation-guide.md` Prompts 1–4); flipped row to Shipped, pointing back at `design.md` §3.10/§5a per DOC-PROTOCOL.md §5 (link to the design doc, don't restate).
- 2026-07-21 — Split the artifact-transfer row: `artifact_path_for_core`'s WSL2-same-PC UNC-path mechanism is now validated against real hardware (a real `west`-built artifact flashed onto the physical nRF54L15 board through it), so it gets its own Shipped row distinct from the still-Todo general cross-machine case, which this validation does not cover.
- 2026-07-21 — Added three Todo rows for Milestone 2 (Token): embarch-core's auto-generated machine-wide token file (replacing `dev-token-change-me`), the folded-in `sc.exe` service-environment fix, and embarch-api's token-file discovery/WSL2⟷Windows path translation. See `embarch-token.md` for the target design and `embarch-core/milestone-2.md`/`embarch-api/milestone-2.md` for execution plans.
