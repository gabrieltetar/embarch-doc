# 018 — The host decoder has no test for either kind of backwards DUT clock, and only one of the two is a defect

**State:** open
**Source:** `embarch-outpost/open.md` — "**The DUT's clock can go backwards for two unrelated
reasons**, and only one is a defect. … a real capture showed one such step of **13 µs**, and a host
**must tolerate it** … A step longer than the whole capture means the counter *restarted*, and the
test is the other clock rather than a threshold." Mechanism: `decisions/clocks.md` decision 17.
**Scope:** outpost
**Hardware:** **none** — this is `tests/decoder_unit.py`, which needs only `python3` and is already
covered by CI (`suite/decisions.md` 2).
**Owner:** no

## What

Decision 17 states a precise rule with two arms, and **nothing mechanical checks either**:

- A **small** backwards step is an inherent artifact — a hook reads the counter and *then* reserves
  its ring slot, so an interrupt preempting that window is stamped before the thread it preempted.
  A host **must tolerate it** and still report it; refusing the clock over it would refuse every
  real capture.
- A **large** one means the counter restarted. The test is **the other clock, not a threshold**:
  a backwards step longer than the whole capture took is two independent clocks contradicting each
  other. When it fires, the host **refuses the DUT clock, falls back to the host's, and says so**.

Add fixtures to `decoder_unit.py` for both, asserting the tolerated case stays on the DUT clock and
is still reported, and the restart case falls back **and says which clock it used**.

## Why now

This is the cheapest untested rule left in the repo — pure host Python, no west, no `ZEPHYR_BASE`,
no siblings, and it lands inside a CI workflow that already runs `decoder_unit.py` on every push.
The 13 µs measurement that motivates the first arm is already recorded, so the fixture has a real
number to be built around rather than an invented one.

## Done when

- [ ] `decoder_unit.py` covers both arms, each with a fixture whose numbers come from the recorded
      measurement or are stated as synthetic.
- [ ] The fallback case asserts the decoder **names the clock it used** — decision 17's "says so"
      is the part a silent fallback would lose.
- [ ] Mutation-checked: removing the tolerance turns the first red, removing the cross-clock test
      turns the second red.
- [ ] `tests/run-all.sh`'s host legs still pass, and **if a new host-only leg was added it is
      listed in `.github/workflows/host-tests.yml` in the same commit** — that workflow lists its
      legs itself and picks nothing up automatically (`suite/decisions.md` 2).
- [ ] Gate green; `changelog.d/` fragment.
