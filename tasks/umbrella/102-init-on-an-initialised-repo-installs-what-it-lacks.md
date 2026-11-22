# 102 — `embarch init` on an initialised repo installs what it lacks and leaves the config alone

**State:** open
**Source:** `tasks/umbrella/101`'s finding (2026-11-21): "A repo already `init`ed gets no skill (`init` exits on an existing config)." `embarch-api/open.md`: "a repo `init`ed earlier needs `init --uninstall` then `init`". `embarch-umbrella` decision 59 (`decisions/integration.md`).
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch init` stops with exit `1` when `embarch/embarch.toml` already exists, before it installs the `embarch-hil` skill, so every repo initialised before decision 59 never gets the skill. The only way to get it today is `init --uninstall` then `init`, which **deletes the config the engineer edited** and scaffolds a fresh one with `CHANGE-ME` in it (decision 41). That workaround costs more than the skill is worth, so nobody will run it.

On a repo whose config already exists, `init` leaves the config untouched and installs whatever else it would have written and is missing: the skill, and each `.git/info/exclude` entry. Whether the MCP registration is checked and repaired on that path too is this unit's decision; say which and why. `--dry-run` names what it would add on that path, and a repo that lacks nothing says so.

## Dispatch notes

- **The exit code on that path is a contract change**: a script that relied on `init` failing on an existing config sees `0` where it saw `1`. Say in the decision what it exits with and why; `embarch-umbrella` decision 12 (nothing committed) still holds.
- **The config is never read to decide what to install** and never rewritten, not even reformatted. A config `init` cannot parse is not this unit's business.
- `embarch-umbrella/spec.md` is 8,808 of 10,240 B, out of reserve; `decisions/integration.md` is 3,837 B. Decisions near their size limit: `prune-policy` #26, `deploy` #32, `mirrors` #20 (each under 40 B).
- Tests in a temporary directory only, never a real firmware repo.
- **The closing note says what `embarch-api/open.md`'s line on the skill should read** (it names the uninstall workaround today); the supervisor amends it at the fold, since that file is `embarch-api`'s.
- Out of scope: `embarch setup`, and upgrading a config's contents.

## Done when

- [ ] `init` on a scratch repo with an existing config installs the skill and the exclude entries, leaves the config byte-identical, and exits as the decision says (a test).
- [ ] `init` on a repo that lacks nothing changes nothing and says so (a test); `--dry-run` on that path writes nothing (a test).
- [ ] `spec.md`, `decisions/` updated; `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope umbrella` on both branches).
