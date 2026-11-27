# 184 — Core holds its debug probes while a lease or a study holds the bench

**State:** open
**Source:** EMB-327 — Core holds no debug probe between calls, even under a lease
**Issue:** EMB-327
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`src/hardware.rs` opens the probe on every call (`open_probe`, around line
115). A vendor backend (`nrfutil`, J-Link) runs as a separate program that
needs the probe itself (`src/flash_backend.rs`). Core already holds its serial
ports while a lease or a study is live, and every serial use borrows the handle
(`src/port_hold.rs`, decision 130). The design this implements
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust" and "What stays
outside prevention") holds probes as well as ports, and says a probe whose
software admits a second connection is not covered.

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction; follow it, and record any deviation in the decision):

- The holder from decision 130 also opens each enrolled board's probe through
  probe-rs at lease take or study start, keyed by probe serial.
- A Core call on a held probe borrows it.
- A vendor backend's call closes the held probe, runs the tool, then reopens
  it. The window between is logged and documented as not covered.
- The signed record lists the probes held.

**Not yours:** `embarch-topology`, `embarch-api`, and every other repo. You
never touch hardware: use a fake probe factory, as the port-hold tests use fake
ports.

## Where to look

- `src/hardware.rs` (`open_probe`, `resolve_probe`), `src/flash_backend.rs`
- `src/port_hold.rs` (decision 130), `src/lease.rs`
- `embarch-doc/embarch-core/decisions/port-hold.md` (130, 3.6 KB),
  `decisions/probes.md` (6.9 KB), `decisions/flash-backend.md` (9.7 KB of
  12 KB); `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md` (A.7)

## Where the doc goes

A new core decision (159 or later; take the next free number when you write it,
by scanning the headings as `DOC-CONVENTIONS.md` says, and cite only that
number in code comments), most naturally in `decisions/port-hold.md` beside
130, with an index row, saying what is not covered. **Over or near the
per-decision cap, do not grow:** `signing#110`, `analog-capture#127`,
`host-study#95`, `definitions#133`, `lease#93`, `stopping-a-study#128`.
**`open.md` is 3,916 B, 3 B under its reserve line; `spec.md` is in reserve
(9,082 of 10,240 B; out at 9,039 B or less) and filed against `tasks/core/186`,
so do not grow it.** If your edit puts `open.md` into reserve, or leaves
`spec.md` there beyond what 186 names, file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next core`).

## Done when

- [ ] With a fake probe factory: a probe is opened once at lease take, borrowed
      by a mem-read and a flash, and closed at release.
- [ ] A vendor-backend flash closes the held probe before the tool runs and
      reopens it after, and both are logged.
- [ ] A study's record lists the probes held.
- [ ] A hardware-verification debt is written into this file for real probes;
      the decision says what is not covered.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); `changelog.d/` fragment.
