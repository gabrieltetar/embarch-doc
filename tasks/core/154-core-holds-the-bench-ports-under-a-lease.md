# 154 — Core holds the bench's serial ports for a lease's or a study's life

**State:** claimed by agent/core/154-core-holds-the-bench-ports-under-a-lease, 2026-11-25 02:30
**Source:** EMB-326 — Core lets go of every serial port between calls, even under a lease
**Issue:** EMB-326
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

Every serial use in Core opens a port, uses it and closes it:
`src/exchange.rs`, `src/serial.rs`, `src/instrument.rs`,
`src/dev_bench_link.rs`, `src/host_study.rs`, `src/study.rs`, `src/api.rs`,
`src/bootload.rs`, and two the issue does not name, `src/analog_source.rs` and
`src/outpost_preflight.rs` (grep `serialport::new`). `serialport` 4.9 opens a
POSIX port exclusive by default (TIOCEXCL and an flock), and a Windows COM port
is exclusive by the OS (unmeasured), so a second opener is kept off only during
a call. The HIL design (`embarch-doc/notes/hil/12-prevention.md`, "The root of
trust"): while a run or a lease holds the bench, the service keeps exclusive OS
handles on its probes and ports, so a second Core opening them gets an error,
and the signed record says Core held them. When this is done:

- A port holder in `AppState`. When a lease is taken, or a study starts with no
  lease, Core opens every declared signal and instrument port it finds and
  keeps it.
- A Core call on a held port borrows the handle, one borrower at a time, under
  `hw_lock` as today. Release, expiry and the study's end close them.
- A port absent at take is logged and held from its first use.
- Bootload ports are left out, since they re-enumerate during a bootload; the
  decision says so. Say what happens to the dev-bench link and the analog
  source port, which the issue does not decide.
- The signed record's `observed` lists the ports held during the run.

Where: the files above; `src/lease.rs` (`LeaseSlot`), `src/api.rs`
(`AppState`, `acquire_hw_lock`). `core/153` landed today and changed
`AppState`, `/status` and the signed record's `observed` (it added `mode`);
build on it.

## Why now

EMB-326, unit A.7 of the HIL attested phase
(`embarch-doc/notes/hil/14-implementation-plan.md`). The attested Core beside a
development Core: the shared HTTP port keeps two Cores from serving at once,
but a Core started on another port would still reach the bench between two of
the service's calls.

**A new numbered decision is yours to write**, recording the holder; amend 93
(`decisions/lease.md`) and 4, 14, 15 (`decisions/platform.md`) only with dated
one-line pointers. `decisions/lease.md` (93) has 35 B left under its
per-decision limit: put the new decision in its own topic file or beside
`platform.md`'s, not inside 93. Do not grow decision 110 (`decisions/signing.md`,
already over its limit); describe `observed`'s new field in
`interfaces/signing.md`.

No file is in reserve on the size ledger at dispatch.

## Done when

- [ ] On a Linux pty pair: with a lease taken, a second open of the held port
      fails, and Core's own exchange on it still works through the held handle.
- [ ] After the release, a second open succeeds.
- [ ] A study's signed record lists the ports held during it.
- [ ] Every existing serial test passes.
- [ ] A hardware-verification debt is left in this file for Windows COM ports
      on the bench; a new decision records the holder.
- [ ] Gate green; the native Windows build stays a debt for the owner;
      `changelog.d/` fragment dropped; `status.d/` fragment for anything
      suite-level it made false.
