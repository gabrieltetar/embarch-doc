# 041 — A StudyStart over one of the bench's capacity limits is dropped without a word

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-dev-bench findings 7 and 11), verified by Opus against embarch-dev-bench@52822069
**Scope:** dev-bench
**Hardware:** toolchain — host-side C plus `native_sim` ztests, no board, built in the **main checkout** (this repo's Zephyr trees are gitignored, so a worktree cannot build it).
**Owner:** no

## What

Every capacity check in the `StudyStart` decoder returns `-1`. That covers:

- the counts: steps over 16 (`serial_protocol.c:1419-1420`), taps (`:1772-1773`), protocols (`:1837-1838`), monitor targets (`:1634`);
- the `.eap` count caps inside `pc_read_protocol_def` (`:382`-`:722`);
- the 3 KB protocol span (`:1859-1860`).

`receive_message` treats every `-1` the same way, whether the frame was malformed or legal but too big: it resyncs on the next delimiter and says nothing (`main.c:914-920`). Only the frame-length overflow branch logs. Core sees a bench that went quiet after a `StudyStart`, which it cannot tell apart from a dead link.

**Proposed direction:** let decode tell "too big for this bench" apart from "malformed". Give `receive_message` a LogLine that names the limit, the value it saw and the cap. Keep a malformed frame as a resync, counted if that is useful, so line noise does not turn into a stream of log lines. The worker designs the shape: a reason code, a reason string, or a decode-result struct.

**Ride-along, comment only, same "the link looks dead" class (finding 11).** `app/boards/nrf54l15dk_nrf54l15_cpuapp.overlay:10`, `:19` and `:47` say the console `uart20` is on VCOM0 and that `uart30` is VCOM1. Decision 43 (`decisions/boards.md`) records the measured opposite: `uart20` is VCOM1, interface 2. `README.md:69-72` and spec §1 agree with decision 43. Correct the overlay's comment. The devicetree itself is right, and nothing else changes.

## Why now

The decoder breaks three written rules:

- spec §3: "A capacity limit refuses, never truncates. An oversized `StudyStart`… is rejected by name";
- decision 41: "Refused by name at decode";
- decision 27: "An oversized study is rejected by name".

Decision 35's own amendment admits it: "17–64-step studies the host accepts are silently unrunnable here". Open task `tasks/dev-bench/004` proposes one more "refused by name at decode" check for out-of-range state indices, and under today's decoder that refusal would be silent too. The overlay comment states the wrong-port fact that decision 43 records costing a bring-up.

## Done when

- [ ] A `StudyStart` that exceeds any one of the bench's decode-time caps produces a LogLine on the link naming that cap, the value received and the limit. Steps, taps, protocols, monitor targets, each `.eap` count and the protocol span are each covered.
- [ ] A malformed frame (bad COBS, a truncated body) still resyncs and does not produce a per-frame log line.
- [ ] `native_sim` ztests cover at least the step cap, one `.eap` cap and the span cap, each asserting the refusal's name, beside the existing refusal tests.
- [ ] The nRF54L15DK overlay's comments name VCOM1 for `uart20` and do not contradict decision 43.
- [ ] Both bench images build: `nrf54l15dk/nrf54l15/cpuapp` from `workspaces/nordic` and `esp32c5_devkitc/esp32c5/hpcore` from `workspaces/espressif`. The `app/tests/serial_protocol` suite passes. To run it: `W=/home/gabriel/Github/embarch/.west-venv/bin/west`, `cd /home/gabriel/Github/embarch/embarch-dev-bench/workspaces/native_sim`, `$W build -b native_sim -d <scratch> /home/gabriel/Github/embarch/embarch-dev-bench/app/tests/serial_protocol`, then `<scratch>/zephyr/zephyr.exe`. Its exit status is the result.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false. Decision 35's amendment in `decisions/link-limits.md` stops saying "silently". `spec.md` is already inside its reserve.
