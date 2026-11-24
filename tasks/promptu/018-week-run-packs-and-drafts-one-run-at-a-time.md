# 018 — `promptu week run` packs and drafts the week, one run at a time, and `week timer` prints its units

**State:** done — week run (lock, exit 4, run record), week timer (prints units), README, three stale lines fixed; timer unobserved under real systemd
**Source:** decisions 14 and 45 (`decisions/learning.md`); `embarch-promptu` `docs/contract.md`'s run record and exit codes; `week pack` (`promptu/013`) and `week draft` (`promptu/017`)
**Issue:** EMB-277
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

The timer, the chat's "run now" (EMB-85) and a terminal user need one command
that runs the weekly pass end to end. `week pack` and `week draft` exist as
separate steps. When this is done:

- **`promptu week run`** packs, then drafts. A lock keeps the timer and a
  click from running two at once: a second `week run` while one runs exits
  with the contract's "already running" code and changes nothing, and a run
  killed part-way leaves no lock that blocks the next one. It writes a run
  record (start, end, result, cost) that `week status` reads, a failed run
  included.
- **`promptu week timer`** prints a systemd user service and timer built from
  the schedule config key (decision 45; default Wednesday 08:00,
  `Persistent=true` per decision 14), with the binary's own path in
  `ExecStart`. It installs nothing: turning the timer on is the user's step.
  Decision 45 says `week timer` "writes" the units; the issue asks that it
  print them. Amend 45 in place to say what you built.
- **The repo's `README.md`**: how to turn the timer on, and how to run the
  pass from any other scheduler (decision 29, users without EmbArch).

Where to start: `src/main.rs` `Cmd`, the `week status` reader, and
`docs/contract.md` for the run record and exit codes. If the contract does
not yet name an "already running" code or the run record's fields, add them
there.

## Why now

`week draft` landed as `promptu/017`. EMB-284 (the chat card's run-now and
open-sheet click) waits on this.

**Burndown leg: no new numbered decision.** Amend decisions 14 and 45 in place
where they change. Where the contract leaves a choice open, record it as a fork
in `docs/forks.md` on a default, as `promptu/011`, `013` and `017` did. If the
work needs a new decision, stop and say so in this file and in your report.

**Dispatch note (supervisor, 2026-11-24): three stale lines from
`promptu/019`, fix them in this unit.** Its reviewer found wording that the
amended decision 43 and fork W17 no longer match: `docs/contract.md` (near
line 704, §14.2) still says "one commit per line" where `week apply` makes one
commit per pattern; the comment above `sheet_md` in `src/draft.rs` and fork
W5's option text in `docs/forks.md` still call `sheet.md` a read-only view,
where `week mark` and `week apply` now read it back. Make each say what is
built.

## Done when

- [x] A second `week run` while one runs exits with the contract's "already running" code and changes nothing.
- [x] A run killed part-way leaves no lock that blocks the next run.
- [x] `week status` shows the run's record after it ends, a failed run included.
- [x] A test checks the timer's `OnCalendar`, `Persistent=true` and `ExecStart` lines.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `cargo test --all-targets` and `cargo clippy --all-targets -- -D warnings`.
- [x] `spec.md`/`decisions.md`/`interfaces.md` updated where they change, `changelog.d/` fragment dropped.

## Built

`src/weekrun.rs` (`week run`, `week timer`), `RunMeta` in `src/draft.rs`, `tests/weekrun.rs` (9 tests). Contract §14 gained exit 4, `week/run.lock`, the run record's `kind`/`cost_usd`/`interrupted`, and the printed-timer text. Forks W19 (the lock) and W20 (`week timer --enabled` records `timer.json`) are new, on defaults; W5 and W12 reworded. The three dispatch-note lines are fixed (contract §14.2 "one commit per pattern", `sheet_md`'s comment, W5's option text). Decisions 14 and 45 amended in place.

**Debt (hardware-verification style, no board):** the printed units were never enabled under a real systemd user manager; `Persistent=true` catch-up and `ExecStart` quoting are unobserved.
**Owed:** a feature-inventory row (no `features.d/promptu-*` fragment possible, EMB-292).
