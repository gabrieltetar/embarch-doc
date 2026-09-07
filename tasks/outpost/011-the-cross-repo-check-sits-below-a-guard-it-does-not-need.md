# 011 — The only check holding the outpost's three wire implementations in agreement cannot run in the configuration its own README claims, and no CI runs it anywhere

**State:** done by agent/outpost/011-toolchain-free-legs-above-the-west-guard, 2026-09-07
**Source:** suite review pass 2026-09-06, dimension 1 (standalone-ness). Code-confirmed.
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`tests/run-all.sh` is `set -euo pipefail` with `WEST="${WEST:?set WEST to a west executable}"` at
line **18**. The cross-decoder leg is at line **38** — *after* it — under a comment that says
*"Needs neither Zephyr nor west."* So on a bare checkout the script aborts at line 18 and the one
toolchain-free cross-repo check never executes.

`README.md:143` states the opposite: *"only the three Zephyr legs need a toolchain."*

When the leg *is* reached, `tests/cross_decoder.py:56-63` prints `SKIP:` and `return 0` if any of
three fixture paths is missing — and those paths reach into two sibling repos
(`embarch-core/tests/fixtures/…bin` plus `…manifest.json`, and
`embarch-ui/tests/fixtures/outpost-native-sim-stamped.trace.csv`).

And `embarch-outpost` has **no CI at all** — `ls .github/workflows` is empty — so nothing runs it
on push either.

The script's own docstring is precise about why it exists: *"A one-off human act that has to be
remembered is not a check."* It has been demoted to exactly that by an ordering accident plus an
absent workflow. Every failure mode is silent: the abort looks like a missing toolchain, the skip
returns 0, and the absent workflow is invisible.

Candidate direction: the two toolchain-free legs run together **above** the `WEST` guard, and a run
that skipped the cross-decoder says so in its exit summary rather than only in a line of stdout.
Whether `embarch-outpost` gets CI at all is a larger, separate call — see the
`suite-two-decisions-record-a-per-push-ci-that-has-never-existed` drop in this batch.

## Why now

`embarch-outpost/decisions/layout.md` decision 4's rule is *"a wire change is not done … until
every host that decodes it has been re-measured against it"*, and
`embarch-decision-reversals.md` row 86 is the 46× error that rule exists to prevent. This check
has already caught two real drifts (`round()` versus `{:.3}`) — the kind nobody finds by reading
two files in two languages.

## Done when

- [x] A bare checkout with no `WEST` set still runs the cross-decoder and the other toolchain-free
      leg.
- [x] `README.md:143`'s claim about which legs need a toolchain is true.
- [x] A run in which the cross-decoder skipped for missing fixtures says so in its final summary,
      not only mid-stream.
- [x] Gate green; `changelog.d/outpost-*` fragment.

## Closed

Fixed by moving `tests/cross_decoder.py` above the `WEST` guard in
`embarch-outpost/tests/run-all.sh`, alongside `decoder_unit.py`, and giving the
script a final summary block that restates a skipped cross-decoder rather than
leaving it only in the mid-stream `SKIP:` line. `README.md`'s Tests section is
corrected to describe both toolchain-free legs. Recorded as
`embarch-outpost/decisions/module.md` decision 22, which also argues in writing
that a missing sibling-repo fixture should stay a skip rather than become a
failure — decision 4 in `decisions/layout.md` is about a wire change inside
this repo, not about what a solo clone of `embarch-outpost` is entitled to
assume exists beside it.

**Proved both ways**, with `WEST` and `ZEPHYR_BASE` unset:
- Pre-fix (stashed the change and re-ran): aborts at line 18 —
  `tests/run-all.sh: line 18: WEST: set WEST to a west executable` — after the
  decoder-unit leg but *before* the cross-decoder ever runs.
- Post-fix: the decoder-unit leg runs, then
  `=== cross-decoder (this repo's decoder vs embarch-core's, same bytes) ===`
  runs and prints its `SKIP:` lines (no sibling repos in this worktree), and
  *then* the script aborts at the (now later) `WEST` guard line for the three
  Zephyr legs — proving the toolchain-free legs now execute unconditionally.

**CI is out of scope here** (`tasks/suite/021`, suite-scope, not run by this
task) — noted in `open.md` under "Deferred with a named trigger". The three
Zephyr legs (`unit`, `module_off`, `native_sim_stream`) did not run in this
sandbox — no `ZEPHYR_BASE`/west toolchain checkout available here, and this
task's fix does not touch their content or ordering relative to each other,
only what runs ahead of the `WEST` guard.

## Reserve — read before you write a doc (supervisor, leg 030)

One `embarch-outpost` file is in reserve: **`embarch-outpost/decisions/tracing.md`, 7,408 / 8,192 B,
784 bytes left**, filed against `tasks/outpost/008` (`In flux: no`, `open`), so it is writable and
the gate passes. A decision about the *test harness* is not a tracing decision, though —
`decisions/module.md` is the better home and it has room. If your work leaves any file inside its
last 10% that nothing has filed, file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit.

## Two boundaries this task must not cross (supervisor, leg 030)

- **Do not add CI.** Whether `embarch-outpost` gets a workflow at all is `tasks/suite/021`, which is
  suite scope and mine to run under an announcement window. Fix the ordering and the README claim;
  say in `open.md` that the CI half is filed elsewhere.
- **The two sibling-repo fixture paths are read-only to you.** `cross_decoder.py` reaches into
  `embarch-core` and `embarch-ui` fixtures. You own `embarch-outpost` and its docs and nothing else
  (`../../embarch-fleet/protocol.md` §3). If the right fix needs a fixture moved or regenerated in
  another repo, that is an `inbox/` drop, not a change.
