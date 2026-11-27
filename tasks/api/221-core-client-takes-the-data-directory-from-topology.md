# 221 — `embarch-core-client` takes the machine data directory from `embarch-topology`

**State:** done — token discovery uses topology machine_data_dir; own resolver and WSL helpers deleted
**Source:** EMB-307 — the machine data directory is resolved five ways, with three unset behaviours
**Issue:** EMB-307
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client/src/token_discovery.rs` resolves the machine data
directory itself: on Windows it falls back **silently** to a literal
`C:\ProgramData` when `ProgramData` is unset, and under WSL2 it shells out to
Windows for the real value and translates the path. `tasks/topology/074` moves
that WSL code into `embarch-topology` as one public
`machine_data_dir(TopologyClass)` with an explicit unset policy (an error, not a
literal). When this is done, token discovery calls topology's resolver
(`Local` on Windows and Unix, `WslHost` under WSL2 — read `topology/074`'s
decision for the exact names), the crate's own copies
(`windows_embarch_dir`, `wsl2_embarch_dir`, the shell-out and translation
helpers) are deleted, and an unset `ProgramData` is reported as an error that
names it, through the same "no token" path a caller already handles.

Check what else in the crate or in `embarch-api` uses those helpers
(`user_dirs.rs`, anything that reads a Windows environment variable) before
deleting them.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `crates/embarch-core-client/src/token_discovery.rs`, `src/lib.rs`, its
  `Cargo.toml` (it already path-depends on `embarch-topology`)
- `embarch-doc/embarch-topology/decisions/storage.md` (`topology/074`'s
  decision), `embarch-doc/embarch-token.md` (the WSL2 discovery and the
  relocated-`ProgramData` gap)

## Where the doc goes

**Reserve, at dispatch:** `decisions/client-crate.md` is 11,828 of 12,288 B,
460 B left, filed under `tasks/api/222`. If the decision that owns token
discovery lives there, keep your amendment net-neutral in that file, or move
the decision verbatim into a new topic file with its index row; do not grow
`client-crate.md`. Otherwise amend the api decision that owns token discovery
in place. `embarch-token.md` is suite-level and not yours: if this
task makes a line there false (the silent fallback, the relocated-`ProgramData`
gap), drop a `status.d/` fragment naming it.

## Done when

- [x] Token discovery calls topology's resolver; the crate's own resolver and
      WSL helpers are gone; an unset `ProgramData` errors by name.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`, and the crate under each feature set its consumers build it
      with, per `gate.md`); decision updated; `changelog.d/` fragment.
