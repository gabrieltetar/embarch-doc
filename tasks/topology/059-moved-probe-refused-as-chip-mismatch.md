# 059 — A probe moved to a board of another chip is refused as a chip mismatch, by name, before any attach

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — on 2026-09-30 a flash of an STM32G0B1VE image through a J-Link still enrolled as `dut` on another project's nRF54L15 board was refused as "failed to read its hardware ID (failed to read FICR.INFO.DEVICEID[0] at 0xffc304)"; sessions flashed with J-Link Commander for six days (73 calls, 19 image loads, 759 s) and wrote a note telling later sessions to bypass EmbArch, until the probe was re-enrolled with one `enroll_probe` call on 2026-10-06
**Scope:** topology
**Hardware:** verify-only
**Owner:** no

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
