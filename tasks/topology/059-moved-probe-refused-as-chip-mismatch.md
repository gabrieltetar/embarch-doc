# 059 — A probe moved to a board of another chip is refused as a chip mismatch, by name, before any attach

**State:** claimed by agent/topology/059-moved-probe-refused-as-chip-mismatch, 2026-10-26 03:42
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — on 2026-09-30 a flash of an STM32G0B1VE image through a J-Link still enrolled as `dut` on another project's nRF54L15 board was refused as "failed to read its hardware ID (failed to read FICR.INFO.DEVICEID[0] at 0xffc304)"; sessions flashed with J-Link Commander for six days (73 calls, 19 image loads, 759 s) and wrote a note telling later sessions to bypass EmbArch, until the probe was re-enrolled with one `enroll_probe` call on 2026-10-06
**Scope:** topology
**Hardware:** verify-only
**Owner:** no

## Dispatch note, 2026-10-26 — read this first

**Topology half only.** You own `embarch-topology` and `embarch-doc/embarch-topology/`, nothing else. The "every Core path (flash, reset, bootload)" box is Core's: Core calls `embarch_topology::hardware::validate_serial` today (`embarch-core/src/hardware.rs:180`, `:391`; `live.rs:93`, `:141`) and has no requested-chip argument to pass. Build the comparison and its refusal text in topology as **additive public API** (a new function or type; do not change the signature or meaning of `validate_serial`/`validate_serial_timed`, which `embarch-core` compiles against on `main`), test it against a fixture enrollment, and **drop the Core wiring as an inbox file** at `/home/gabriel/Github/embarch/embarch-doc/inbox/core-<slug>.md`, absolute path, full task format, naming your new API and the four call sites. Tick that box as "filed for Core" rather than leaving it unexplained.

**Doc reserve, and the compaction you owe.** `embarch-topology/decisions/enrollment.md` is 12,045 / 12,288 B (**243 B left**) and `embarch-topology/spec.md` 9,550 / 10,240 B (690 B left), both filed against `tasks/topology/060`, which is **blocked on `In flux: yes` naming this task** and due 2026-11-01. You are the actor making that flux, so if you write into either file, **compact that file as part of this unit**: a verbatim split first (`DOC-COMPACTION.md` §2; a split restates nothing), carrying 060's `Must not delete:` list (every measured STM32 identity fact in `spec.md`). Then delete that file from 060's `Compacts:` line, say so in 060's body, and re-answer 060's `In flux:` for what remains. If you write neither file, say so in your Result and leave 060 alone. `decisions/link-declares.md` (1,133 B left, `tasks/topology/064`) is also in reserve; leave it unless you must.

## What

`validate_serial_timed` finds the enrolled row by probe serial and checks the live board against that row's chip (`embarch-topology/src/hardware/validate.rs:442-451`). Core calls it before every flash (`embarch-core/src/hardware.rs:177-179`) and never compares the chip the caller asked for (the project's `chip`) with the enrolled one. When a probe has moved to a board of a different family, the gate attaches with the old chip's target description and reports a failed identity read, which looks like a broken board or bad wiring. Compare first. When the requested chip and the enrolled chip differ, refuse before the probe is opened, naming the probe, the enrolled board (name, chip, role or bench board) and the requested chip, and say that the fix is to re-enroll this probe, naming what that re-enrolment displaces. The identity gate stays exactly as strict; this only changes which refusal comes first and what it says.

## Why now

The refusal pointed at the wrong cause, so sessions worked around EmbArch for a week, and the workaround note outlived the cause. The fix was one `enroll_probe` call that nothing suggested.

## Done when

- [ ] A flash or reset whose requested chip differs from the probe's enrolled chip is refused before any attach, with text naming both chips, the enrolled board and the re-enroll call; unit test against a fixture enrollment.
- [ ] Equal chip names behave as today, and the identity gate's mismatch and failed-read refusals are unchanged.
- [ ] Every Core path that passes a requested chip into the gate (flash, reset, bootload) gets the same check.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
