# 181 — Core switches every declared output off at start and at a graceful stop

**State:** claimed by agent/core/181-core-switches-every-declared-output-off-at-start-and-graceful-stop, 2026-11-26 22:55
**Source:** EMB-325 — Core leaves bench outputs as they were across a stop and a start
**Issue:** EMB-325
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`embarch-topology` already lets an instrument declare `safe_off: Vec<String>`
and a signal `safe_off: Option<String>` (each line checked by
`check_safe_off_line`), but nothing in `embarch-core/src` sends one. A host
study's teardown runs its own steps on every exit; Core itself has no safe-off.
A Windows SCM stop drains `serve` and flushes the call log's fold, while
foreground `run` (the whole story on Linux) is
`serve(bind, port, std::future::pending())`, so nothing runs on SIGTERM or
Ctrl-C. Core binds its port after it reads the tokens and logs.

The design this implements (`embarch-doc/notes/hil/12-prevention.md`, "The root
of trust"): "a service stop runs Core's safe-off, every Core start switches off
every output the bench declares before it serves a route and logs that it did";
"on every service start, Core logs the time it was stopped".

When this is done, per the issue's direction (the owner moved it to Fleet Ready
with that direction; follow it, and record any deviation in the decision):

- **Start order:** bind the port first; a bind failure says another Core may
  hold it, names the address, and sends nothing to the bench. Then the
  safe-off. Then serve.
- **The safe-off:** for each declared instrument with `safe_off`, open its port
  and send each line with its own terminators and pacing, keeping the reply;
  for each signal with `safe_off`, send its line to the bench board. A
  declaration with none, or a port absent, is logged as such and does not stop
  the start. The command is built from the declaration only.
- **Graceful stop:** SCM Stop, SIGTERM and Ctrl-C (tokio's signal handling) end
  `serve`. A study in flight is cancelled and its teardown runs, then the
  safe-off, the fold flush and the stop entry.
- **The call log** gains `start` and `stop` entries. A start names the last
  clean stop's time (from the last `stop` entry) or "not a clean stop", the
  mode, and each safe-off result; the first start in an empty log says "log
  started anew". `last_images` lives in memory, so every board's last flasher
  is already unknown after a start; the start entry says so.
- A kill, a crash or a power loss runs no safe-off; the next start does. The
  doc says so.

**Not yours:** `embarch-topology` (its `safe_off` fields are read, not
changed), `embarch-api`, and every other repo. You never touch hardware: every
test uses fake ports and a fake bench board, as the existing instrument and
exchange tests do. Two tasks blocked on this one (EMB-328, the call log's
fail-closed rule, then EMB-329) build on the `start`/`stop` entries, so keep
their shape in `interfaces/call-log.md` exact.

## Where to look

- `src/main.rs` (`serve`, `run`, the start sequence), `src/service.rs` (the SCM
  stop, around line 449)
- `src/instrument.rs`, `src/exchange.rs` (the senders to reuse),
  `src/call_log.rs` (entry types), `src/lease.rs` (`ImageLog`)
- `embarch-topology/src/hardware/instrument.rs` and `signal.rs` (`safe_off`)
- `embarch-doc/embarch-core/interfaces/call-log.md`,
  `decisions/call-log.md` (122); `embarch-doc/notes/hil/12-prevention.md`,
  `notes/hil/14-implementation-plan.md` (A.2, A.9)

## Where the doc goes

A new core decision for the safe-off and the start/stop entries (156 is the next
free number at the time of writing; take the next free one when you write it,
found by scanning the headings as `DOC-CONVENTIONS.md` says, and cite only that number in code comments), in
`decisions/call-log.md` (4.2 KB of 12 KB) or a new topic file, with an index
row. `interfaces/call-log.md` gives the two entry shapes. **Over or near the
per-decision cap, do not grow:** `signing#110`, `analog-capture#127`,
`host-study#95`, `definitions#133`, `lease#93`, `stopping-a-study#128`.
**`open.md` is 3,917 B, 2 B under its reserve line, and `spec.md` 9,011 B, 28 B
under it.** Leave both alone if you can (spec §3 "Deployment" may need one
sentence on start order and stop); if your edit puts either into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit (`tasks/README.md` has the
shape; number from `scripts/check-task-numbers.py --next core`).

## Done when

- [ ] With fake ports, a start sends every declared `safe_off` line before the
      first route answers, and a declaration without one is logged as "no
      safe-off declared".
- [ ] A start whose port is taken fails, naming the address, and sends nothing.
- [ ] A test-driven shutdown signal runs the safe-off after the last request
      and before the `stop` entry.
- [ ] After a test kill, the next `start` entry reads "not a clean stop"; the
      call log's chain still recomputes.
- [ ] A hardware-verification debt is written into this file for a real
      instrument and bench board.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`), and the Windows-gated code type-checks for
      `x86_64-pc-windows-msvc` if you touch it (`cargo check --target
      x86_64-pc-windows-msvc` where the target is installed; say if it is not).
- [ ] `interfaces/call-log.md` gives the two entry shapes; a new decision
      records the safe-off; `changelog.d/` fragment.
