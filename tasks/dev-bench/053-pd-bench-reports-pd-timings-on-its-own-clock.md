# 053 — pd-bench reports PD timings on its own clock

**State:** done — pd times and PD event stamps built, native_sim tested; hardware debt recorded
**Source:** EMB-388 — the PD partner cannot report a PD timing on its own clock
**Issue:** EMB-388
**Scope:** dev-bench
**Hardware:** verify-only
**Owner:** no

## What

A PD timing requirement is measured on the bench board's own clock, because a
host stamp through a USB serial bridge is not a sub-millisecond clock
(`embarch-doc/notes/hil/03-test.md`, "The verdict"); a Test parses its number
out of a reply at step time. `pd status` prints counts and the contract, and no
time (`pd-bench/README.md`, "Shell"). When this is done:

- **Each PD event the stack reports to the app** — attach, Source_Capabilities
  received, Request sent, Accept, PS_RDY, Hard Reset sent or received,
  keep-alive stopped — is stamped with the bench's uptime in microseconds as it
  is seen.
- **`pd times`** prints the last few events with their stamps, then the
  intervals a test needs — attach to Source_Capabilities, Request to PS_RDY,
  keep-alive stopped to Hard Reset received — one line per interval,
  `<name> <us>`, then `pd: ok`. A missing event gives no line for its interval.
- **The interval arithmetic lives in `pd_logic.c`**, tested on native_sim.

The owner may strike the new command in favour of extra `pd status` lines; say
in the decision which you chose and why.

**Not measured**: where in the stack's callbacks each event is seen, so what an
interval includes. Leave that as the hardware-verification debt below.

## Where to look

- `pd-bench/src/main.c`, `pd-bench/src/pd_logic.c`, `pd-bench/tests/logic`
- `pd-bench/README.md` — the shell contract
- `embarch-doc/embarch-dev-bench/decisions/pd-bench.md` (68, `pd idle` and
  `pd hello`)

## Where the doc goes

A new dev-bench decision in `decisions/pd-bench.md`; the README documents
`pd times`. **`embarch-dev-bench/spec.md` is in reserve** (1,102 B left; its
compaction `tasks/dev-bench/052` is blocked, In flux: yes): do not write it.

## Hardware verification

Leave a debt for the bench's clock characterisation: on each shield, what each
interval includes (which callback stamps it) and how it compares with a probe on
CC.

## Done when

- [x] The native_sim suite tests the intervals over a scripted event list, a
      missing event giving no line for its interval.
- [x] Both shields build.
- [x] The README documents `pd times` and what each interval starts and ends
      on.
- [x] The hardware-verification debt is recorded here.

## Result

Decision 69. `pd times` is a new command (not extra `pd status` lines; the owner may strike it). Stamps come from `k_uptime_ticks()`; the interval arithmetic is `PdLogicInterval` in `pd_logic.c`, tested on native_sim (23 cases pass), both shields build under twister.

## Hardware-verification debt

On each shield (SNK1M1 and DRP1M1), against a probe on CC:

- Run attach, `pd max`, `pd keepalive off` against a PPS source, then `pd times`; compare `attach_to_src_caps`, `request_to_ps_rdy` and `keepalive_stopped_to_hard_reset` with the same intervals on the CC probe.
- Record which callback stamps each event and what each interval therefore includes: `policy_get_rdo` runs before the Request is on the wire; `MSG_ACCEPT_RECEIVED` and `TRANSITION_PS` run in the Policy Engine thread after the message; the keep-alive event is one 8 s period after the last Request.
- Record the kernel tick's resolution on the G0B1 (`CONFIG_SYS_CLOCK_TICKS_PER_SEC`); if it is coarser than the 100 us a PD timing needs, switch to `k_cycle_get_32`.
- Check a Hard Reset the bench sends is never stamped as received (the `hard_reset_sent` flag), on both roles.
