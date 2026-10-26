# 100 — Capture a signal in the background while other hardware calls run

**State:** done (host-side half; hardware-verification debt below), agent/core/100-capture-a-signal-in-the-background, 2026-10-26
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 69 hand-written PowerShell `System.IO.Ports.SerialPort` scripts in 18 sessions (1,510 s of tool time) read consoles around Core; after `signal_exchange` landed on 2026-10-06, 21 of them (1,237 s) still ran on the DUT and bench consoles, each one a listener on one console while `signal_exchange` drove the other, or a boot log held across a reset; a 20 s `serial_log` was refused at the 10 s cap
**Scope:** core
**Hardware:** verify-only — reclassified from `bench` on filing by the 2026-10-25 leg: the capture endpoint is host-side code a worker can build and test against a mock port; the two-console bench check is its hardware-verification debt, collected by a supervisor.
**Owner:** no

## Dispatch note, 2026-10-26 05:14 leg

**Scope this unit to the host-side half.** Routes, the port owner, the caps decision and tests against a mock or in-process fake port. Every bench line in Done-when (two consoles, flash and reset during a capture, a real CDC ACM re-enumeration) is a hardware-verification debt you write into this file, not something to attempt. If the shared port owner with study taps turns out to be a large refactor of its own, land the capture with the seam named and leave the sharing as an `open.md` item or an `inbox/` drop, rather than half-doing both.

**Doc reserve in your scope:** `embarch-core/spec.md` 9,148 / 10,240 B (1,092 B left) and `embarch-core/open.md` 4,262 / 5,120 B (858 B left), both filed under `tasks/core/112`, which is blocked with `In flux: yes` about decision 89. Keep what you add to either small; if you need room, shorten text that is not on 112's `Must not delete:` list and that this change makes obsolete, and say what in your Result. `decisions/signal-exchange.md` is 9,635 / 12,288 B (about 1.4 KB before its reserve line). A capture decision of any size is better as a new topic file (for example `decisions/signal-capture.md`, listed in `decisions.md`) than pushing `signal-exchange.md` into reserve. If your work does leave a file in reserve with nothing filed against it, file `tasks/core/<NNN>-compact-core.md` in the same commit.

**No wire-schema bump.** New routes are fine. If the design needs `host_type_schema_version` or `schema_version` to move, stop and report it; that is a §4 announcement, not a worker's call.

**The client half** (MCP tools and CLI) is another scope: write it as a complete task file into `/home/gabriel/Github/embarch/embarch-doc/inbox/` by that absolute path, after checking whether `tasks/api/131` already covers it.

**Isolation, not optional.** Never start the Core binary on its default port or data dir, never reach the live Core (the Windows service at the WSL2 gateway, `:4884`), never open a real serial port or a debug probe, never call the `mcp__embarch-api__*` or desk tools, never touch the desk on :4891, and never read or write the owner's data dirs. Tests own their own ports, temp dirs and fake ports. The last two legs each had a worker reach something live; do not be the third.

## What

A USB PD test needs both consoles at once: the bench Nucleo is driven one command at a time while the DUT's log records what its policy engine did, for 10 to 60 s. Core cannot do this today. `GET /serial-log` and `POST /signals/{name}/exchange` both run inside the one `hw_lock` (`embarch-core/src/api.rs:846`, `:1328`), so a log capture on the DUT console makes every exchange on the bench console fail after 500 ms, and a capture ends at `serial::MAX_DURATION_MS`, 10 s (`embarch-core/src/serial.rs:16`). Add a background capture on a declared signal. `POST /signals/{name}/capture {max_s, max_bytes}` opens the port and returns an id, `GET` returns what arrived after a given offset, and `DELETE` stops it. The capture holds only its own port, never `hw_lock`, so flash, reset and exchanges on other signals run while it records. This keeps decision 79's reason for refusing a held-open session (no lock held across an agent's thinking time) because the lock is never taken. An exchange on the captured signal itself writes through the capture's open handle, returns its reply as today, and its bytes also land in the capture. A capture on a UART bridge survives a reset of its board, which is the "arm, then reset" ordering a boot-log capture needs; a capture on a USB CDC ACM port reopens when the port re-enumerates and marks the gap. This is the interactive counterpart of `core-console-capture-during-host-study`, which taps consoles inside a host study: the field sessions ran no study in six weeks, so both are needed, and the two should share one port owner so a study tap and an ad hoc capture never open the same COM port twice.

## Why now

The listeners were base64-encoded PowerShell, to survive WSL quoting, with escape-code stripping and `sleep`-staged background writers; one 60 s policy-engine trace (2026-10-10, three runs, 683 s) had no route through Core at all.

## Done when

- [x] Capture start, read-from-offset and stop exist on a declared signal; a second capture on the same signal is a `409` naming the first. (`capture.rs`, `api.rs`; unit-tested against scripted ports.)
- [ ] On the bench, with a capture running on one console, exchanges on the other console and a flash and reset of either board all succeed. **Hardware-verification debt.**
- [x] An exchange on the captured signal returns its reply, and the capture contains the same bytes. (Host side, scripted port; test `an_exchange_goes_through_the_capture_and_its_bytes_land_in_it`. Real-console check in the debt.)
- [ ] A capture across a reset holds the boot lines on a UART bridge; across a CDC ACM re-enumeration it reopens and records a gap marker. Host side done against a scripted port (`a_lost_port_is_marked_and_reopened`); **real UART bridge and CDC ACM are hardware-verification debt.**
- [x] Duration and byte caps are named in a decision (92), and a capture is not bounded by the client's 15 s request timeout (`POST` returns at once; only each `GET` is short).
- [x] The client half is filed as an `api` task: `/home/gabriel/Github/embarch/embarch-doc/inbox/api-signal-capture-tools.md` (`tasks/api/131` is the higher-level `bench_exchange` built on this and does not cover the raw tools).
- [x] Gate green (see Result).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `features.d/core-260-signal-capture.md` written.

## Result

Shipped `embarch-core/src/capture.rs` plus three routes and `AppState.captures`; `exchange::exchange_with` is `pub(crate)` and the response tail is `exchange::response`, shared. Decision 92 in `decisions/signal-capture.md`. No wire-schema change.

**Not done, by the dispatch note:** one port owner shared with a study's signal tap. The seam is `AppState.tap_ports`: a capture claims its port there (so `/bootload` and a new capture refuse it) and refuses a port a tap holds, but a study that starts later on a captured signal is only refused by the OS. Recorded in `open.md` and decision 92, left to the console-capture-during-host-study task (`core/101`).

**Docs shortened:** nothing; `spec.md` is 9,398 / 10,240 B and `open.md` 4,872 / 5,120 B (both already filed under `core/112`, which stays blocked).

## Hardware-verification debt

Bench: both consoles of the USB PD board, a Core on a scratch data dir and port.

1. Declare the DUT and bench consoles as signals. `POST /signals/dut/capture {"max_s":60}`; while it runs, `POST /signals/bench/exchange` several times, `POST /flash` and `POST /reset` on either board. All succeed; `GET /signals/dut/capture?after=0` shows the DUT log.
2. `POST /signals/bench/exchange` on the captured signal: reply returned and the same bytes in `GET`.
3. UART bridge: arm a capture, `POST /reset`; the boot lines are in the capture with no gap.
4. USB CDC ACM: arm a capture, reset or reflash the DUT; `state` goes `reopening`, then `running`, `gaps` has one entry, the text holds `[embarch: port lost]` and `[embarch: port reopened]`. Check the reopen finds the device under a changed COM name.
5. A 120 s `max_s` capture read with `GET` polls over several minutes is not cut by a client timeout; `DELETE` returns the final text.
6. Windows: a second open of the captured port (study tap) fails cleanly.
