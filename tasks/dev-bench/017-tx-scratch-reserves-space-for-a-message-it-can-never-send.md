# 017 — `tx_scratch` reserves ~15.7 KB for a `dbm_study_start` the bench can never transmit

**State:** open
**Source:** `embarch-dev-bench/open.md:38` — "the single largest remaining lever on ESP32-C5 SRAM";
decision 38 explains why the buffer is sized by its largest member today. Surfaced by leg 076's
refill sweep.
**Scope:** dev-bench
**Hardware:** required — **and it is a toolchain, not a board.** No board is needed, but the
evidence this task turns on (a `native_sim` test run and the ESP32-C5 build's size report) cannot be
produced from the fleet's environment at all: there is no `west` and no `ZEPHYR_BASE`, which is the
same standing debt that gates every other `embarch-dev-bench` task in the queue. Dispatch it from a
session that has the Zephyr toolchain. Filed `open` rather than `blocked` because nothing needs
unblocking — only the environment has to be right.
**Owner:** no

## What

`tx_scratch` is a union sized by its largest member, and that member is `dbm_study_start`, which is
a message the bench **receives** and never sends. Give the TX path its own message type that
excludes the RX-only variants, so the buffer is sized by what can actually go out of it.

**Record the number.** The point of this change is an SRAM figure, so the task is not done until the
ESP32-C5 build's size report before and after is written down in the `changelog.d` fragment. A
refactor that is *supposed* to save 15.7 KB and is never measured is not evidence of anything.

**Supersede decision 38 rather than contradicting it.** That decision states the current sizing rule
and its reason; if this change makes it false, it gets superseded explicitly.

## Why now

It is the largest single SRAM lever this firmware has left, and the cost is paid continuously
whether or not anything needs the space — which is the kind of debt that stops being payable once
something else grows into the room it was hiding.

## Done when

- [ ] A TX-only message type excludes `StudyStart` (and any other RX-only variant) from the union
      `tx_scratch` is sized by.
- [ ] The ESP32-C5 build's SRAM figure is captured before and after and **both numbers are in the
      `changelog.d` fragment**, not just the delta.
- [ ] Existing bench tests pass on `native_sim`.
- [ ] Decision 38 is superseded, saying what the sizing rule is now.
- [ ] Re-confirming a real study still runs on the bench board is a **separate** debt — record it in
      the log entry rather than claiming it done. The evidence this task requires is the
      `native_sim` run and the size report, both of which need the Zephyr toolchain named above.
- [ ] `embarch-dev-bench/open.md` is at 4,782/5,120 B and `spec.md` at 9,460/10,240 B — **both in
      reserve**, with `tasks/dev-bench/012-compact-dev-bench.md` parked against them. Do not file a
      second compaction task for either.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.
