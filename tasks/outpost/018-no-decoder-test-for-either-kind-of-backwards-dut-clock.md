# 018 — The host decoder has no test for either kind of backwards DUT clock, and only one of the two is a defect

**State:** done — first arm tested here; the second arm is not this repo's (see Outcome)
**Reserve (dispatch note, 2026-10-29):** `embarch-outpost/spec.md` is 9,126/10,240 B (1,114 B left, out of reserve at <= 9,039 B), filed only against `tasks/outpost/028`, `blocked` on `In flux: yes`: if you write to it, cut what you add (carry `outpost/028`'s `Must not delete:` list). Per-decision caps: `decisions/clocks.md` decision 17 has **26 B** left and `testing` decision 26 has 55 B, so an amendment to either must cut what it adds or file a debt. This task is also a candidate in `tasks/suite/055`'s triage; dispatching it settles that.
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

## Outcome (2026-10-29)

**The premise was half wrong.** `scripts/decode_outpost.py` has no clock-fallback: it unwraps the 32-bit counter and never refuses it. The restart arm ("backwards step longer than the whole capture, tested against the host's clock; refuse, fall back, say so") lives in `embarch-ui/src/trace.rs` and `embarch-core/src/outpost_load.rs`, which need the host's `rx_utc_ms`. `decoder_unit.py` cannot test it and was not given a stand-in.

- **Arm 1 shipped:** `TestWrapVersusGap.test_a_13_us_inversion_between_ordinary_records_is_tolerated_and_reported` — the recorded 13 us step (13 cycles at the 1 MHz the fixtures use), on ordinary records so only the step size can keep it from being read as a wrap; asserts the row is kept and reported. **Mutation-checked:** replacing the `> (1 << 31)` wrap threshold with `True` turns it red (and the two gap tests).
- **Arm 2 is covered where it lives:** `embarch-ui/src/trace.rs` tests `a_benign_microsecond_backstep_is_not_a_reset`, `a_stale_pre_reset_prefix_does_not_anchor_the_projection`, `a_stale_leading_prefix_is_dropped_and_the_dut_clock_survives_it`, `a_small_backwards_step_on_the_dut_clock_is_tolerated_and_costs_no_record`. **Not checked by this worker:** whether any of them asserts that the fallback *names* the clock it used; if not, that is a `ui` task, not an `outpost` one.
- No new host-only leg, so `host-tests.yml` is unchanged. No spec/decision edit (reserve respected).

## Done when

- [x] `decoder_unit.py` covers arm 1 (recorded 13 us number); arm 2 is not decoder behaviour (see Outcome).
- [ ] Fallback names the clock: **not applicable to this repo**, see Outcome.
- [x] Mutation-checked for arm 1.
- [x] `tests/run-all.sh` host legs: `decoder_unit.py` 36 tests green; no new leg.
- [x] Gate green (see report); `changelog.d/` fragment.
