# embarch-features.md: changelog archive

Entries beyond the 8 most recent, moved here from [embarch-features.md](embarch-features.md)
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.

- 2026-07-27 — Added three Proposed/design-only rows for Milestone 3 (Study Designer): the shared `embarch-study-designer` data-types library, `embarch-core`'s new dev-bench serial bridge, and `embarch-api`'s future study-running MCP tool/CLI subcommand. All point at `embarch-study-designer/design.md` rather than restating detail, per this file's own header note.
- 2026-07-22 — Corrected status drift: three Milestone-2 (Token) rows were still marked `Todo` even though `embarch-token.md` and both design docs' changelogs recorded milestone-2 as code-complete (Windows-unvalidated) since 2026-07-21 — violated `DOC-PROTOCOL.md` §5's "sub-project doc and suite-level docs should never disagree about status" rule. Flipped to `Shipped, Windows hardware-unvalidated` (or the WSL2-specific equivalent) to match. Also annotated the artifact-freshness-check row with the WSL2 wall-clock-jitter fix applied the same day (`embarch-api/design.md` §12).
- 2026-07-17 — Initial draft.
- 2026-07-20 — Updated doc references for the `embarch-core/design.md` / `embarch-api/design.md` subfolder restructure.
- 2026-07-20 — Added the CLI subcommand interface row (Todo), per `embarch-api/design.md` §3.10/§5a.
- 2026-07-20 — Pointed the CLI subcommand interface row at `embarch-api/milestone-1-implementation-guide.md`, the new file with the actual implementation prompts; row stays Todo until that guide's prompts actually ship (see the guide's Prompt 5, which flips this to Shipped).
- 2026-07-20 — CLI subcommand interface shipped (`milestone-1-implementation-guide.md` Prompts 1–4); flipped row to Shipped, pointing back at `design.md` §3.10/§5a per DOC-PROTOCOL.md §5 (link to the design doc, don't restate).
- 2026-07-21 — Split the artifact-transfer row: `artifact_path_for_core`'s WSL2-same-PC UNC-path mechanism is now validated against real hardware (a real `west`-built artifact flashed onto the physical nRF54L15 board through it), so it gets its own Shipped row distinct from the still-Todo general cross-machine case, which this validation does not cover.
- 2026-07-21 — Added three Todo rows for Milestone 2 (Token): embarch-core's auto-generated machine-wide token file (replacing `dev-token-change-me`), the folded-in `sc.exe` service-environment fix, and embarch-api's token-file discovery/WSL2⟷Windows path translation. See `embarch-token.md` for the target design and `embarch-core/milestone-2.md`/`embarch-api/milestone-2.md` for execution plans.
