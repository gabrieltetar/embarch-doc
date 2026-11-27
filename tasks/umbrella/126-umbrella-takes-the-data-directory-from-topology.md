# 126 — `embarch` takes the machine data directory and the WSL helpers from `embarch-topology`

**State:** claimed by agent/umbrella/126-umbrella-takes-the-data-directory-from-topology, 2026-11-27 02:57
**Source:** EMB-307 — the machine data directory is resolved five ways, with three unset behaviours
**Issue:** EMB-307
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/setup.rs` `data_dir_for` hardcodes `/mnt/c/ProgramData/embarch` for a
`wsl-host` topology, so `doctor` check 16 reads "nothing yet" when the Windows
host's `ProgramData` is relocated (`decisions/reporting.md` records the
caveat), and `src/locate.rs` carries its own copy of the WSL2 shell-out of a
Windows environment variable and the Windows-to-WSL path translation.
`tasks/topology/074` puts one public `machine_data_dir(TopologyClass)` and both
WSL helpers in `embarch-topology`. When this is done:

- `data_dir_for` returns what topology's resolver returns for each class (read
  `topology/074`'s decision for the names and the unset policy), keeping the
  `windows` argument's meaning for a `Local` class if the resolver does not
  already cover it, and `Remote` still has no path.
- `locate.rs` calls topology's two helpers and its own copies are deleted.
- `doctor` check 16 on a relocated `ProgramData` reads the real directory; the
  caveat in `decisions/reporting.md` is rewritten to say what is true now (a
  resolver error is reported in check 16's detail, not as "nothing yet").

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/setup.rs` (`data_dir_for` and its callers), `src/locate.rs`
  (`windows_env_var_via_shellout`, `translate_windows_path_to_wsl` and their
  callers), `src/doctor.rs` (check 16)
- `embarch-doc/embarch-topology/decisions/storage.md` (`topology/074`'s
  decision), `embarch-doc/embarch-umbrella/decisions/reporting.md` (the
  `%ProgramData%` caveat)

## Where the doc goes

**Since this was filed, `open.md` went into reserve** (4,553 of 5,120 B,
567 B left), parked under `tasks/umbrella/127` (`In flux: yes`): do not grow
it; if this unit must edit it, compact it in the same commit and keep 127's
`Must not delete:` list. `decisions/agent-runtime.md` (67),
`install-core-platforms.md` (72) and `agent-container.md` (62) are over their
per-decision limit; do not touch them. Amend `decisions/reporting.md`'s caveat in
place; `embarch-token.md` is suite-level and not yours, so if its relocated-
`ProgramData` gap is now closed for `doctor`, drop a `status.d/` fragment.

## Done when

- [ ] `data_dir_for` and `locate.rs` call topology; umbrella's copies are gone.
- [ ] A test drives check 16's path through a stubbed resolver for a relocated
      `ProgramData` (or the resolver's seam, if `topology/074` gives one).
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); decision updated; `changelog.d/` fragment.
