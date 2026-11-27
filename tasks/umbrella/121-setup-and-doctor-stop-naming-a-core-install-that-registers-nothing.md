# 121 — `setup` and `doctor` stop naming a Core install that registers nothing

**State:** claimed by agent/umbrella/121-setup-and-doctor-stop-naming-a-core-install-that-registers-nothing, 2026-11-27 00:43
**Source:** EMB-339 — the finding comment of 2026-11-27 (Core decision 157, `core/183`)
**Issue:** EMB-339
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Since Core decision 157, `embarch-core install --bind <addr>` without
`--service` registers nothing: it prints that nothing was registered and exits
0. `install --service --bind <addr>` registers `run --service` under Core's own
account, and only for a binary that `<data dir>/installed-release.json` lists
by SHA-256 in `binary_sha256` (`embarch-doc/embarch-core/interfaces/installed-release.md`).
Core decision 106's last sentence now says only `install --service --bind`
rewrites a registration.

Umbrella still says the old thing:

- `src/setup.rs` — the Local arm (around line 303) runs `install --bind` and
  prints "Installed and started." on exit 0, so `embarch setup` on a Local
  topology reports a service that does not exist. The dry-run, remote and
  Windows arms print the same command (around lines 278 to 312).
- `src/doctor.rs` — check 17's fix lines (`umbrella/095`, decision 22) and the
  Core-placement lines (around 460 and 465, and 3211 to 3327) name
  `embarch-core install --bind`.

When this is done: no umbrella output names `install --bind` as the step that
registers or rewrites Core's service, and `setup` never reports a registration
it did not make. Where a registration is the fix, name the route that makes
one: `embarch install-core <release>` for a first install (decision 61, and its
elevated half once `umbrella/119` and `umbrella/120` land), and the installed
binary's `install --service --bind <addr>` to change the address of an existing
registration. Where a route is not built yet on a platform, say so rather than
print a command that does nothing. Record the choice in a decision.

**Not yours:** `embarch-core` and every other repo; `install-core`'s own
behaviour (`umbrella/119`, `umbrella/120`). You never touch hardware.

## Where to look

- `src/setup.rs`, `src/doctor.rs` (check 17, `REINSTALL_NOTE`), their tests
  (`doctor.rs` around 4636 asserts the old text)
- `embarch-doc/embarch-umbrella/decisions/install.md`, `decisions/bind.md`
  (22), `decisions/install-core.md` (61); `embarch-doc/embarch-core/decisions/platform.md`
  (106, 157, read only)

## Where the doc goes

A new umbrella decision, or an amendment of 22 if it fits under the
per-decision cap; an index row for a new one (take the next free number by
scanning the headings, as `DOC-CONVENTIONS.md` says, and cite only that number
in code comments). **Do not grow:** `agent-runtime#67`, `agent-container#62`,
`deploy#32`, `prune-policy#26`. `open.md`'s check 17 debt names `install
--bind 0.0.0.0`: correct it in place, net-neutral or smaller if `open.md` is
still in reserve.

## Done when

- [ ] `setup`'s Local arm no longer prints "Installed and started." for a call
      that registered nothing, tested.
- [ ] No fix line in `doctor` names `install --bind` without `--service` as a
      registration step; the tests assert the new text.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
