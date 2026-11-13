# 109 — `service install` keeps the UI's config when the shell does not set `EMBARCH_UI_CONFIG`

**State:** done on agent/ui/109-service-install-keeps-the-ui-config, 2026-11-12
**Source:** EMB-140, found deploying the UI as a user service (EMB-63) on a bench machine
**Issue:** EMB-140
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Since decision 101 (`decisions/launcher.md`) the launcher no longer passes
`embarchUi.configPath`, so the service unit is the only thing that sets
`EMBARCH_UI_CONFIG`. `embarch-ui service install` copies it into the unit only
when the installing shell has it set (`src/service.rs`, the `CARRIED` list and
`install()`). A shell opened normally, or a Claude session's shell, does not set
it, so the unit gets no config line, `config::load()` (`src/config.rs`) falls
back to `Config::default()`, and the UI loses its tabs and the per-repo settings
in that file. The install prints the same success line either way.

Wanted, one of two, and the choice is a decision with its reason:

- `load()` reads a default path when the variable is unset (the XDG config
  directory, and its Windows equivalent if the UI runs there), so an install
  from any shell finds the file; or
- `service install` refuses, or warns naming the variable, when the unit would
  carry no config.

If you pick the default path, say what happens when neither the variable nor
the file exists (today's zero-config default must keep working), and whether
`service install` should write the path it resolved into the unit.

Also correct the comments that still name the VS Code extension or
`embarchUi.configPath` as the variable's source: `src/firmware_build.rs` (the
paragraph that says "The VS Code extension sets `EMBARCH_UI_CONFIG`"), `load()`'s
doc comment, and the sample config's header comment.

**What you may change.** Only `embarch-ui` and `embarch-doc/embarch-ui/`.
**Never install, restart or reinstall the running UI service.** The owner
deploys; leave a deploy debt in this file.

**Doc reserve.** No `embarch-ui` file is in reserve. Decisions within their
own limit: `launcher` (28) 22 B, `tab-folders` (100) 113 B, `trace-view` (10)
0 B. Decision 101 is in `decisions/launcher.md`; a new decision goes in the file
of its subject, never the one with room, and if `launcher.md` cannot hold it,
split before you write.

## Why now

Reinstalling is the documented dev restart path once the binary path moves, and
every reinstall from a session shell drops the config with no warning.

## Done when

- [x] `service install` from a shell without `EMBARCH_UI_CONFIG` produces a UI
      that still loads its config, or the command says it will not.
- [x] A test covers the unset case.
- [x] The comments that name the extension or `embarchUi.configPath` as the
      variable's source are corrected.
- [x] Gate green (`../../embarch-fleet/gate.md`), and a deploy debt written here.

## Done

Chose the default path ([decision 102](../../embarch-ui/decisions/ui-config.md), new file `decisions/ui-config.md`, since `launcher.md` had 22 B): `load()` reads `embarch-ui/config.toml` under `$XDG_CONFIG_HOME` / `~/.config` (`%APPDATA%` on Windows) when the variable is unset and the file exists; neither means today's zero-config default. The unit is not given the path, but `service install` now prints which config it will read, or that there is none. Corrected the comment in `firmware_build.rs` and `load()`'s doc; no sample config file exists in the repo, so none to fix.

## Deploy debt

Owner: `cargo build` in the main `embarch-ui` checkout after landing, then `systemctl --user restart embarch-ui` (or re-run `service install`). Put the config at `~/.config/embarch-ui/config.toml` (or keep `EMBARCH_UI_CONFIG` exported when installing) and confirm the tabs load. The Windows `%APPDATA%` path is written, not run.
