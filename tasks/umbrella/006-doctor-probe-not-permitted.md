# 006 — Check 5 still reports the Linux permission failure as the warn decision 18 calls misleading

**State:** done, 2026-09-05, on `agent/umbrella/006-doctor-probe-not-permitted`
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

- [x] On Linux, zero enumerated probes plus a known vendor ID in the USB device
      tree reads Fail with the udev fix line; a genuine miss stays the warn.
- [x] macOS/Windows behaviour unchanged, and a test pins that.
- [x] `spec.md`'s check 5 row, its "which checks can fail" sentence, and decision
      18's implementation note updated.
- [x] Hardware-verification debt written into the task — see below; the Fail
      branch was **not** exercised against a real probe.
- [x] Gate green; `changelog.d/` fragment dropped.
- [x] Ride-along: `spec.md` compacted in this same commit, 10,089 → 9,131 B
      (98.5% → 89.2%), out of reserve, `tasks/umbrella/009`'s counts refreshed
      and only its reserve item closed.

## What shipped

`check_probes` grew a `Fail` branch and, with it, decision 37's `code` field —
`probes-present`, `no-probe-found`, `no-probe-unchecked`, `probe-not-permitted`,
`no-status`, so the two warns that share a status stay distinguishable in
`--json`. The scan is `std::fs` over `/sys/bus/usb/devices/*/idVendor`: no new
dependency, and **sysfs is world-readable while the `/dev/bus/usb` node is what
the udev rule grants**, which is the whole reason it can see a probe the
enumeration could not open.

**One condition decision 18 did not name and this build added:** the scan runs
only when Core enumerates on *this* machine (Linux **and** class `local`).
Check 5 reads its probe count off Core's `/status`, so on `wsl-host` or `remote`
that count is about one computer and this host's USB bus is about another —
scanning anyway would repeat check 14's mistake (decision 31) with a different
peripheral. `wsl-host` and `remote` keep the warn and say which reason applies.
**`0403` (FTDI) is deliberately not on the vendor list**: it is on half the
serial cables on this bench, and a probe ID that means "probe" only sometimes
would fail the check on machines with no probe at all.

Nine tests, including one that holds on all three hosts (`usb_scan_for` returns
`NotLinux` off Linux, whatever the class) — that is the pin on macOS/Windows
being unchanged, since `cfg!` rather than `#[cfg]` keeps every branch compiled
and testable everywhere.

## Hardware-verification debt

**The Fail branch has never met a real permission-denied probe.** Settling it
needs a Linux machine running `embarch-core` natively (class `local` — this
suite's primary `wsl-host` topology skips the scan by design and cannot
exercise it at all), with a debug probe attached and its udev rules removed or
never installed: `embarch doctor` should then report check 5 as **Fail**,
`code` `probe-not-permitted`, naming the probe by its product string and vendor
ID, with the udev fix line — and, with the rules restored and the probe
unplugged, **Warn** `no-probe-found`. Until that runs, the Fail branch is
unit-tested against a synthetic sysfs tree only, and whether the nine vendor IDs
are the right nine is unmeasured. Carried in
[open.md](../../embarch-umbrella/open.md).
