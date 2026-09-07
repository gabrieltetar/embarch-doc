# 011 — The only check holding the outpost's three wire implementations in agreement cannot run in the configuration its own README claims, and no CI runs it anywhere

**State:** open
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

- [ ] A bare checkout with no `WEST` set still runs the cross-decoder and the other toolchain-free
      leg.
- [ ] `README.md:143`'s claim about which legs need a toolchain is true.
- [ ] A run in which the cross-decoder skipped for missing fixtures says so in its final summary,
      not only mid-stream.
- [ ] Gate green; `changelog.d/outpost-*` fragment.
