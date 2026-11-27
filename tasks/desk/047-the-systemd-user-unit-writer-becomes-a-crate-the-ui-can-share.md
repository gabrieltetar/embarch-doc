# 047 — the systemd user-unit writer becomes a crate the ui can share

**State:** claimed by agent/desk/047-the-systemd-user-unit-writer-becomes-a-crate-the-ui-can-share, 2026-11-27 02:57
**Source:** EMB-302 — the systemd user-unit writer exists twice, in `embarch-desk` and `embarch-ui`
**Issue:** EMB-302
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`src/service.rs` here and `embarch-ui/src/service.rs` each carry their own
`quoted()`, `unit_text()`, `systemctl --user` wrapper and install, uninstall
and status, and both encode the same WSL `PATH` rule (a `PATH` holding
`Program Files`, `%` doubled, `$` doubled in `ExecStart` only) with the same
adversarial test string. A fix to one is silently missing from the other.

When this is done, the part both need lives once, in a small library crate
inside this repo (for example `crates/embarch-user-unit/`, in the mold of
`embarch-api/crates/embarch-core-client`), and the desk installs through it.
The crate renders a unit's text from an executable, a `PATH` value, a set of
`Environment=` pairs and a description, quotes every word by the WSL rule,
knows where a user unit lives under `$XDG_CONFIG_HOME` (empty read as unset)
or `~/.config/systemd/user`, and wraps `systemctl --user` with an error that
carries its stderr. **It takes no dependency beyond `std` and `anyhow`**, so
the ui gains nothing heavier than this by depending on it, and it does not
make the desk depend on any sibling repo. The desk's instance support (names,
ports, folders, the flags that need `--instance`) stays in `src/service.rs`
and feeds the crate; the crate knows nothing about instances. The adversarial
quoting test moves into the crate; the desk's instance tests stay where they
are.

The ui moves onto the crate in `tasks/ui/131`, which waits on this. Make the
crate's API fit what `embarch-ui/src/service.rs` does today (read it; do not
edit it): its carried variables (`CARRIED`), its config note and its
`USAGE` stay the ui's own.

**Not yours:** every other repo, `embarch-ui` included. You never touch
hardware.

## Where to look

- `src/service.rs` (`quoted`, `unit_text`, `systemctl`, `unit_path`,
  `install`, `uninstall`, `status`, the tests near the end)
- `embarch-ui/src/service.rs` (read only)
- `embarch-doc/embarch-ui/decisions/launcher.md` (read only: the ui's
  install is recorded there as the desk's own install cut down, with no
  reason given for not sharing)
- `embarch-doc/embarch-desk/decisions/` (where the desk's service install is
  decided today)

## Where the doc goes

A new desk decision records where the writer lives, why a crate in this repo
(and not a dependency on the whole desk, nor a sibling repo), what it takes and
what stays desk-only. `embarch-desk/decisions/access-point.md`'s decision 56
is already 15 B over its per-decision limit; do not grow it. Update `spec.md`
and `interfaces.md` where they describe the service install.

## Done when

- [ ] The unit-text rendering, the quoting and the `systemctl --user` wrapper
      exist once, in a crate in this repo with no dependency beyond `std` and
      `anyhow`, and `embarch-desk service install`, `uninstall` and `status`
      run through it with the same unit text they write today, instance or
      not (a test pins one unit's text before and after).
- [ ] The adversarial quoting test lives in the crate.
- [ ] A new desk decision records the home and what stays desk-only.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings` for the desk and for the new crate); `changelog.d/`
      fragment.
