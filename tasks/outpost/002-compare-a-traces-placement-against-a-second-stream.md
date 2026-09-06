# Compare a trace's placement against a second stream in the same study

**State:** open
**Source:** `embarch-outpost/open.md` — "Nothing has compared a trace's placement against a second stream in the same study… that is the check the dual-clock flag exists to enable, **and it has not been run.**"
**Scope:** outpost
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench`. **This needs a study that runs**, with two streams captured in the
same run — see the companion `api` bench task. Validate both roles first; if either is
unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- **DUT: `nff_dev` rev 6** (AS7058 PPG AFE). Owner-stated 2026-09-06.
- **`ble speed fast` over NUS before any BDS step**; **`meas_sched stop` before `hrm_start`**;
  **`CONFIG_LOG` off** for BDS runs. Each of these is load-bearing — see the `api` task.
- Outpost link ceiling is **460800 baud**; keep the DUT's current speed and
  `EMBARCH_SIGNAL_BAUD` in step by hand.
- **The outpost snippet compiles `CONFIG_LOG` out**, so NUS `log …` returns "command not
  found". Expected, not a fault.
- **`.eap`: never tap a protocol source.** The dev-bench's 4-slot queue drops capture data
  silently; bulk characteristics go on a monitor window instead.
- **Reading the trace CSV**: drop the stale pre-reset prefix, calibrate the ~1 MHz clock
  against `rx_utc_ms`, and **check frame loss before trusting any lane conclusion.**
- **Lane identity is not established for rev6.** The `spim_21` + `gpiote_20` PPG mapping is a
  rev7 fact. If a conclusion here depends on which peripheral a lane is, stop and say so.
- **Flash what is already built**; do not `west build` the client workspace.

## What

One study captures an outpost trace **and** a second stream, and the two are compared: does
the trace's placement line up with the other stream's timing, at the ~4.0 ms median placement
resolution `open.md` records for the reference capture? That comparison is what the dual-clock
flag exists to enable and it has never been made.

`open.md` is explicit that "every outpost wire constant is still an unmeasured default with
the instrumentation's own overhead deliberately uncharacterised, so a working view is not
validation of the numbers underneath it." **Do not let a plausible-looking overlay become a
claim that the constants are right.** Report the observed alignment and its spread, and say
what remains uncharacterised.

## Why now

The bench is attached and the fleet may use it (`../../embarch-fleet/protocol.md` §7,
2026-09-06). This is the one check that turns the dual-clock design from reasoned to observed.

## Done when

- [ ] A study captures a trace and a second stream in the same run, or the task records
      exactly why it could not and stays `open`.
- [ ] The placement comparison is made and its spread recorded with provenance.
- [ ] Frame loss is checked and reported **before** any timing conclusion is drawn.
- [ ] `open.md` distinguishes what this run measured from what is still an unmeasured default.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
