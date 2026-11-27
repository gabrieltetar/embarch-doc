# 131 — the ui installs its service through the desk's unit crate

**State:** open — `desk/047` landed the crate this calls (`embarch-desk/crates/embarch-user-unit`, desk decision 94)
**Source:** EMB-302 — the systemd user-unit writer exists twice, in `embarch-desk` and `embarch-ui`
**Issue:** EMB-302
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`src/service.rs` carries its own `quoted()`, `unit_text()`, `unit_path()` and
`systemctl --user` wrapper, a cut-down copy of the desk's. `tasks/desk/047`
moves the desk's into a small crate in the `embarch-desk` repo with no
dependency beyond `std` and `anyhow`.

When this is done, `embarch-ui service install`, `uninstall` and `status`
render and manage `embarch-ui.service` through that crate, by a path
dependency on it, and the ui's own copies of the quoting, the unit text, the
unit path and the `systemctl` wrapper are gone. What is the ui's alone stays
here: `CARRIED`, `config_note`, `USAGE` and the command parsing. A test pins
the unit text the ui writes today against what it writes through the crate.

`decisions/launcher.md` records the ui's install as the desk's own cut down;
make it say where the shared writer lives now (amend the entry in place, or a
new decision if the change is larger than a line).

**Not yours:** every other repo, `embarch-desk` included. You never touch
hardware.

## Where to look

- `src/service.rs`
- `embarch-desk/crates/embarch-user-unit/src/lib.rs` (read only): `Unit`,
  `unit_text`, `unit_path`, `install`, `uninstall`, `status`; `Unit.args` is
  empty for the ui, `Unit.vars` carries `CARRIED` in order
- **Dispatch setup:** the path dependency is
  `../embarch-desk/crates/embarch-user-unit`, so the ui worktree's parent
  needs an `embarch-desk` link to the main checkout, which the dispatch table
  in `.claude/leg.md` does not list yet
- `embarch-doc/embarch-ui/decisions/launcher.md`

## Done when

- [ ] The ui's service command installs, uninstalls and reports status
      through the desk's unit crate, and the ui's own copies are gone.
- [ ] A test pins the unit text, unchanged from today's.
- [ ] `decisions/launcher.md` says where the shared writer lives.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
