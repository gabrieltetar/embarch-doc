# 157 — Package a finished build as a flashable bundle for a bench engineer

**State:** claimed by agent/api/157-bundle-a-build-for-a-bench-engineer, 2026-11-17 18:09
**Source:** EMB-171, filed by an audit after a firmware packet for a hardware engineer was hand-built with inline Python, because no `zip` binary was installed
**Issue:** EMB-171
**Scope:** api
**Hardware:** none
**Owner:** no

## What

An engineer handing firmware to someone with a debug probe and the vendor's
flashing CLI, but no toolchain and no checkout, repeats the same steps every
time: copy the sysbuild merged hex out of the build directory under a
commit-stamped name, check its segments, write a README of flash commands and
the bench checklist, and zip the folder. `embarch-api` already runs the build
and knows where the artifact is (`build`, `build_and_flash`), and stops at
handing it to Core's `/flash`.

Add `embarch-api bundle <project> [--notes <file>] [--out <dir>]` and a matching
`bundle` MCP tool over one implementation:

- Reuse a fresh artifact or build one, by the same rule `build_and_flash` uses to
  refuse an artifact older than its sources. The issue says that rule exists;
  confirm it in the code before relying on it, and if it does not, add it here
  and say so.
- Write `<name>-<short-sha>/` holding `<name>-<short-sha>.hex` and `README.md`,
  and `<name>-<short-sha>.zip` of that folder, with Rust's own archive and hex
  libraries, never a shell `zip` and never Python.
- Check the hex's segments before writing anything: a merged image must hold a
  segment at the bootloader's address and one at the application slot's, from
  the build's own partition output, not from constants in the code.
- Render the README from a template: the vendor CLI's program (with a full chip
  erase), reset and recover commands with the hex's file name filled in, the
  console settings, then the notes file appended. **Take every command and
  console setting from what the suite already records for that chip family** (a
  flash runner Core or the project's config names). A family the suite records
  nothing for gets a README line saying so, never a command written from memory.

**Public repo.** Tests use a synthetic build directory and a synthetic hex made
in the test. No client project, no real board.

**Burndown leg: no new numbered decision.** Record the verb and the tool in
`spec.md` and `interfaces/`. A real design fork, such as where the README
template lives or which families it covers, goes to `scripts/fleet-linear.py
file --from decision`.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** Nothing of `embarch-api`'s is in reserve, but three decision
entries are near their limit: `ledger` 98 (15 B left), `bench-exchange` 89
(122 B) and `failure-reporting` 67 (192 B). This unit should not need to edit
them.

## Why now

The owner moved EMB-171 to Fleet Ready.

## Done when

- [ ] `embarch-api bundle <project>` writes `<name>-<short-sha>/` with the hex and `README.md`, and `<name>-<short-sha>.zip`, with no `zip` binary on the machine.
- [ ] The README holds the program, reset and recover commands with the hex's file name filled in, taken from what the suite records for the chip family, and says so plainly for a family it records nothing for.
- [ ] A notes file passed to the verb is appended to the README.
- [ ] The verb refuses a build whose artifact is older than its sources.
- [ ] The same operation is reachable as an MCP tool.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
