# 051 — pd-bench has an idle command and a hello line

**State:** claimed by agent/dev-bench/051-pd-bench-has-an-idle-command-and-a-hello-line, 2026-11-26 14:02
**Source:** EMB-387 — the PD partner has no idle command and no hello line
**Issue:** EMB-387
**Scope:** dev-bench
**Hardware:** verify-only
**Owner:** no

## What

`pd-bench` has commands that change its behaviour for one test (`pd keepalive
off`, `pd dr reject`, `pd pr reject`, `pd answer wait`, `pd srccaps ...`), none
that puts them all back, and no line that names the app and its build
(`pd-bench/README.md`, "Shell"). The HIL design starts every test from "a DUT
reset plus each bench board's idle command, before every test, so one test's
leftovers (a PPS contract kept alive, a swapped role) are never the next one's
start" (`embarch-doc/notes/hil/03-test.md`, "One test"), and its smoke check
has each companion board answer a hello ("A run", item 3). When this is done:

- **`pd idle`**: keep-alive on, `dr accept`, `pr accept`, `answer accept`, the
  devicetree's Source_Capabilities, any contract dropped, and on the DRP1M1
  VBUS off and discharged as the existing turn-off path does. It ends `pd: ok`
  once all of it holds, else `pd: error <what>`.
- **`pd hello`**: one line with the app name, its version and commit as built,
  and the shield, then `pd: ok`.
- The settings `pd idle` restores move into `pd_logic.c` where they are pure,
  so the native_sim logic suite tests the list.
- `pd detach` is not added here. The decision says the owner may strike that:
  adding it would let a test ask for a `detach` precondition.

## Where to look

- `pd-bench/src/main.c` (the shell), `src/pd_logic.c` and `pd_logic.h`,
  `tests/logic`
- `pd-bench/README.md`, "Shell" and "Tests"
- `embarch-doc/embarch-dev-bench/decisions/pd-bench.md` (48, 49, 58, 59)

## Where the doc goes

A new decision in `decisions/pd-bench.md` if it has room, else a new topic
file; the README's shell table gains both rows. `check-doc-size.py --pressure`
lists logging#38 and #39, ble#34 and #37, protocols#41, conventions#47 and
capture#29 near their limits: do not grow those. No `embarch-dev-bench` file is
in reserve at filing; if your work pushes one in, file
`tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same commit per
`tasks/README.md`.

## Hardware verification

**Not measured**: `pd idle` and `pd hello` on a board. Leave a
hardware-verification debt for the PD bench's characterisation session: each
setting restored after a test that changed it, on both shields, and VBUS off
and discharged on the DRP1M1.

## Done when

- [ ] Both shields build from the main checkout's `workspaces/pd-bench` with
      the worktree's sources.
- [ ] The native_sim logic suite tests the idle settings list.
- [ ] The README's shell table lists both commands.
- [ ] A hardware-verification debt is left for the characterisation session.
- [ ] Gate green.
