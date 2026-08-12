# design.md: changelog archive

Entries beyond the 8 most recent, moved here from [design.md](design.md)
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.

- 2026-07-17 — Initial draft, written to document the existing embarch-core implementation.
- 2026-07-20 — Moved from `embarch-core-design.md` (repo root) to `embarch-core/design.md` as part of the embarch-doc per-sub-project restructure; no content changes.
- 2026-07-21 — Milestone-1 hardware validation (§3.1–3.4): confirmed the native-Windows build (requires the VS Build Tools C++ workload, not just `rustup`'s bare toolchain), confirmed the real probe-rs chip target is `nRF54L15` (not the `nRF54L15_M33` placeholder), validated `/status`/`/serial-log`/`/reset`/`/flash` against the physical board-a board from WSL2, and confirmed WSL2⟷Windows reachability needs no explicit Windows Firewall rule on this machine's networking mode (§7). Also fixed a real bug found during this validation: `api.rs`'s `internal_err` used to discard the full `anyhow` error chain via `Display`, returning/logging only the outermost context string — now uses `Debug` and logs server-side too (§4). §3.5 (`EMBARCH_TOKEN` surviving an installed Windows service) remains open — diagnosed, not yet fixed (§10).
