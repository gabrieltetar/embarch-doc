# 006 — Check 5 still reports the Linux permission failure as the warn decision 18 calls misleading

**State:** open
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 18 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** verify-only — dispatchable; the drop wrote "none to build; one Linux machine with a probe to verify for real", which is `verify-only`, and it must leave a hardware-verification debt (supervisor, on the drain)

**Compacts:** embarch-umbrella/spec.md
**In flux:** yes — by this task, which is the point: `tasks/umbrella/009-compact-docs.md` is `blocked` on exactly
that, and a blocked compaction task parks the pass, not the reserve (`DOC-COMPACTION.md`
§2). You are the unit that rewrites a row of `spec.md`'s doctor table, so **compact both as part of this
commit**, honour `tasks/umbrella/009-compact-docs.md`'s `Must not delete:` list, and close only their item there.
**Headroom: `spec.md` 151 B of 10,240**, and it cannot be split — 10 KB is a role cap on a
single file (`DOC-COMPACTION.md` §2–3), so shortening is the only move. `open.md` was on
this line too and **is paid**: the owner's live-`doctor` pass took it 5,051 → 4,388 B while
adding what the run measured, which is this rule's first real use. `Must not delete:`, from
009: the doctor table's per-row **designed-and-unbuilt** distinction, which lives nowhere
else. Refresh 009's counts if you change the table's shape — a `Must not delete:` clause
that protects a table *by a count* is worse than useless once the count is stale.

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
