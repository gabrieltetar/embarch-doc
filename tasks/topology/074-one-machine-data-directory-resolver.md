# 074 — One resolver for the machine data directory

**State:** done — machine_data_dir, windows_env_var, windows_path_to_wsl public in embarch-topology; decision 52
**Source:** EMB-307 — the machine data directory is resolved five ways, with three unset behaviours
**Issue:** EMB-307
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

The machine-wide data directory (`%ProgramData%\embarch` on Windows,
`/var/lib/embarch` elsewhere, `embarch-token.md`) is resolved in five places
with three behaviours when `ProgramData` is unset or relocated:

- `embarch-topology/src/hardware/paths.rs` (`machine_data_dir`, private) and
  `embarch-core/src/token_store.rs` (which it says it copies) return an error
  naming the variable;
- `embarch-api/crates/embarch-core-client/src/token_discovery.rs` falls back
  silently to a literal `C:\ProgramData`, and under WSL2 shells out to Windows
  (`cmd.exe`, then `powershell.exe`) for the real value, then translates it
  (`wslpath`, then a hand parse);
- `embarch-umbrella/src/setup.rs` `data_dir_for` hardcodes
  `/mnt/c/ProgramData/embarch` for a WSL2 host, so `doctor` check 16 reads
  "nothing yet" on a relocated `ProgramData`; `src/locate.rs` carries its own
  copy of the WSL shell-out and the path translation.

This task is the first of four: it puts **one public resolver in this crate**,
which Core, `embarch-core-client` and `embarch-umbrella` already link; the
other three tasks (`tasks/core/192`, `tasks/api/221`, `tasks/umbrella/126`)
replace their copies with calls to it once this lands. When this is done:

- `embarch_topology` exposes `machine_data_dir(class: TopologyClass)` (the
  enum in `src/software.rs`) returning the directory as **this process** reaches
  it: `Local` is this machine's own (`%ProgramData%\embarch` or
  `/var/lib/embarch`); `WslHost` is the Windows host's, from inside WSL2,
  through the shell-out and the translation; `Remote` has no local path.
  Choose the return type so `Remote` is not an error.
- **The unset policy is explicit and one:** `ProgramData` unset on Windows, or
  a WSL2 shell-out that yields nothing usable, is an error naming what was
  tried, never a silent literal. That is what Core and this crate do today;
  `core-client`'s silent `C:\ProgramData` fallback is the behaviour that goes,
  and the decision says so. If you find a caller that genuinely needs a
  fallback, say which in the decision rather than keep a quiet one.
- The WSL2 shell-out of a Windows environment variable and the
  Windows-to-WSL path translation are public helpers here too, so
  `embarch-umbrella/src/locate.rs` can delete its copies (it reads other
  variables than `ProgramData` through the same shell-out).
- The shell-out result is cached once per process, as `core-client` does
  today.
- The existing `data_dir()` / `set_data_dir` behaviour of this crate is
  unchanged and now calls the new resolver for its default.

Port the WSL helpers and their tests from `core-client` rather than writing
new ones: that copy is the one with the `powershell.exe` fallback and the
`wslpath`-then-hand-parse order, which have been exercised.

**Not yours:** every other repo — the four consumers move in their own tasks.
You never touch hardware.

## Where to look

- `src/hardware/paths.rs`, `src/software.rs` (`TopologyClass`), `src/lib.rs`
- `embarch-api/crates/embarch-core-client/src/token_discovery.rs`
  (`windows_embarch_dir`, `wsl2_embarch_dir`, `windows_program_data_via_shellout`,
  `run_shellout`, `translate_windows_path_to_wsl`, `hand_parse_windows_path`)
  — read only
- `embarch-umbrella/src/setup.rs` `data_dir_for`, `src/locate.rs`
  (`windows_env_var_via_shellout`, `translate_windows_path_to_wsl`) — read only
- `embarch-doc/embarch-token.md` (the path, and the relocated-`ProgramData` gap
  in its last section), `embarch-doc/embarch-topology/decisions/storage.md`

## Where the doc goes

A new topology decision in `decisions/storage.md` (6,103 B, room). **Decision
23 in that file is already 492 B over the per-decision cap**: do not grow it;
point to the new decision from it only if the pointer is net-neutral.
`embarch-token.md` is suite-level and not yours: if this task makes a line
there false, drop a `status.d/` fragment naming it.

## Done when

- [x] `machine_data_dir(class)` and the two WSL helpers are public, with the
      unset policy explicit and tested (an unset `ProgramData` on the
      Windows arm, a shell-out that yields nothing, `Remote`).
- [x] The crate's own `data_dir()` default calls it; its tests still pass.
- [x] The decision records the unset policy and names the four callers that
      move to it.
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`, and the crate under each feature set its consumers build
      it with, per `gate.md`); `changelog.d/` fragment.
