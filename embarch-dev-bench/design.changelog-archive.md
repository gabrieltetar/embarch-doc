# design.md: changelog archive

Entries beyond the 8 most recent, moved here from [design.md](design.md)
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.

- 2026-07-20 — Placeholder created alongside the embarch-doc per-sub-project restructure.
- 2026-07-29 — Initial scoping pass, resolved via Q&A rather than a written proposal-first draft: repo created empty at [gabrieltetar/embarch-dev-bench](https://github.com/gabrieltetar/embarch-dev-bench). Locked in: Zephyr as the common cross-vendor RTOS (not a custom multi-SDK HAL); a single repo with multiple west workspaces (one per vendor family) sharing one application source tree, resolving the "a west manifest pins one Zephyr revision" constraint against vendor forks like NCS; NCS (not vanilla Zephyr) for the first, Nordic-family workspace, with application code restricted to portable Zephyr APIs regardless; nRF54L15DK as the first board (over nRF54H20DK, to avoid its `sysbuild` complexity for a role that doesn't need multiple cores); Nordic's SoftDevice Controller for that workspace's BLE controller; USB CDC ACM as the Core link, one interface; dev-bench's own log output modeled as a new `DevBenchMessage::LogLine` variant rather than a second interface or raw shared-wire text; the Rust FFI staticlib pulled in as a west module with its cross-compilation invoked automatically via a CMake custom command; no CI and no second vendor/board committed to yet. GPIO/analog stimulus and power-sampling hardware explicitly scoped out of v1.
