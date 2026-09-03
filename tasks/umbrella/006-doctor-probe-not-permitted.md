# 006 — Check 5 still reports the Linux permission failure as the warn decision 18 calls misleading

**State:** open
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 18 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** verify-only — dispatchable; the drop wrote "none to build; one Linux machine with a probe to verify for real", which is `verify-only`, and it must leave a hardware-verification debt (supervisor, on the drain)

## What

`embarch-umbrella` decision 18 says that on Linux, after zero probes are
reported, `doctor` checks the USB device tree for a known debug-probe vendor ID
the enumeration missed, and reports a hit as **Fail — attached but not
permitted**, with the udev-rules fix line. **None of that exists.**
`check_probes` in `src/doctor.rs` reads the probe count off `/status`, warns on
zero, and has no `Fail` branch at all.

Build the Linux-only branch. macOS and Windows keep the current behaviour —
decision 18 says so explicitly.

## Why now

This is named as the most common Linux first-run failure, and the current output
tells that user their probe is legitimately unplugged. The host-side half (the
device-tree read and the vendor-ID list) is testable without a probe; confirming
the Fail actually fires on a real permission-denied probe is hardware-verification
debt for whoever has a Linux box with one attached.

## Done when

- [ ] On Linux, zero enumerated probes plus a known vendor ID in the USB device
      tree reads Fail with the udev fix line; a genuine miss stays the warn.
- [ ] macOS/Windows behaviour unchanged, and a test pins that.
- [ ] `spec.md`'s check 5 row, its "which checks can fail" sentence, and decision
      18's implementation note updated.
- [ ] Hardware-verification debt written into the task if the Fail branch could
      not be exercised against a real probe.
- [ ] Gate green; `changelog.d/` fragment dropped.
