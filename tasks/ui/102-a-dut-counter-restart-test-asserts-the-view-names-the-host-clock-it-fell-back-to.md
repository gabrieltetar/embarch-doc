# 102 — A DUT-counter restart test asserts the view names the host clock it fell back to

**State:** claimed by agent/ui/102-a-dut-counter-restart-test-asserts-the-view-names-the-host-clock-it-fell-back-to, 2026-10-29 15:27
**Source:** `tasks/outpost/018`'s Outcome, 2026-10-29 (its one unticked `Done when` box, re-homed here at its fold). `embarch-outpost` [decision 17](../../embarch-outpost/decisions/clocks.md): a backwards step longer than the whole capture means the DUT counter restarted, and **a host refuses the DUT clock, falls back to `rx_utc_ms`, and says so**. The worker found that arm lives in `embarch-ui/src/trace.rs` (and `embarch-core/src/outpost_load.rs`), not in the outpost decoder.
**Scope:** ui
**Hardware:** none — `trace.rs`'s own unit tests, against synthetic rows.
**Owner:** no

## What

`trace.rs` already tests the restart path's *data* outcome — `a_stale_pre_reset_prefix_does_not_anchor_the_projection`, `a_stale_leading_prefix_is_dropped_and_the_dut_clock_survives_it`, `a_benign_microsecond_backstep_is_not_a_reset`, `a_small_backwards_step_on_the_dut_clock_is_tolerated_and_costs_no_record`. Nobody has checked whether any of them asserts decision 17's third verb, **"says so"**: that when the view gives up the DUT clock it reports which clock it used (the `unit == "ms"` host-clock flag, a diagnostic, or whatever the view exposes). Read the four tests and the fallback path; if none asserts the naming, add one test that does. If the view does not name the clock at all, that is a decision 17 gap: record it in `embarch-ui/open.md` rather than inventing a surface.

## Done when

- [ ] Either an existing test is shown to assert the fallback names the host clock (cite it in the task's close), or a new one does.
- [ ] If the view cannot say which clock it used, an `open.md` line names the gap against decision 17.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment if code changed.
