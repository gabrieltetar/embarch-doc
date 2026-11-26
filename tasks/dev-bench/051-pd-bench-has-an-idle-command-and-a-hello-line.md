# 051 — pd-bench has an idle command and a hello line

**State:** done — pd idle and pd hello shipped host-side (decision 68); both shields build, logic suite green; hardware debt left
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

- [x] Both shields build from the main checkout's `workspaces/pd-bench` with
      the worktree's sources.
- [x] The native_sim logic suite tests the idle settings list.
- [x] The README's shell table lists both commands.
- [x] A hardware-verification debt is left for the characterisation session.
- [x] Gate green.

## Hardware-verification debt

For the PD bench's characterisation session, on a NUCLEO-G0B1RE with each shield (decision 68):

- **Each setting restored after a test that changed it, on both shields**: set `pd keepalive off`, `pd dr reject`, `pd pr reject`, `pd answer wait`, `pd srccaps 5000:1500` (DRP1M1), `pd pps ...`; run `pd idle`; read `pd status` and `pd srccaps` back and see every one at its default.
- **A contract dropped**: with a sink holding a (PPS) contract, `pd idle` sends a Hard Reset and the bench renegotiates at the `pd max` choice; with the DRP1M1 sourcing to an attached sink, `pd idle` ends with VBUS off, under 0.6 V within tSafe0V, and the port attaching again from scratch (the ErrorRecovery request).
- **`pd hello`** prints the version, the commit of the sources as built (`-dirty` when they were) and the right shield on each build.
- **Not host-checked**: the Hard Reset and ErrorRecovery choices are read from the stack, not run.

## Build record

Built from the main checkout's `workspaces/pd-bench` (west init, `west update --narrow`, `west patch apply`; ignored there) with this worktree's `pd-bench/` as `-s`: SNK1M1 129496 B flash, DRP1M1 149760 B, both clean; the native_sim logic suite passes with four new idle tests.
