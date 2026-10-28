# 046 — A bench board can own a signal and be read and validated by its probe, not only flashed

**State:** claimed by agent/suite/046-bench-board-owns-signals, 2026-10-28 15:08 — announced 14:33:53 (`ts` `1793219633.062879`); the window closed 15:03:53 with no reply in the thread or the channel (polled 15:06:46), so the supervisor runs it as its leg's last unit.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the bench Nucleo was enrolled as a role-less bench board on 2026-10-09 (topology decision 41), but its console signal could only be declared from role `dev-bench`, which holds an nRF54L15 DK; two refusals on 2026-10-19 named that role, not the Nucleo, and when the bench firmware hung (2026-10-09) its program counter was read with the probe-rs CLI, since `mem_read` takes only a role
**Scope:** suite
**Hardware:** verify-only
**Owner:** no

## What

Decision 41 lets any number of bench boards enroll, keyed by probe, and flash and reset reach them by probe serial. Three other paths still take only a role. A signal's `origin_role` (`embarch-topology/src/hardware/signal.rs:58-63`) is what Core resolves to a board when it must reset the board a signal leaves (`embarch-core/src/study.rs:1233-1273`). `POST /live/mem-read` (`embarch-core/src/live.rs:37-47`, `api.rs:1377`) and `POST /validate` (`api.rs:1571`) resolve a role. So a bench board's console has to borrow a role it does not hold, its refusals name that role's board, and a reset resolved through the signal would reach the role's board, here the DK, not the Nucleo. Let a signal name a board (a bench board's name or probe serial) as its origin instead of a role, and resolve resets and refusal text through it (`enrolled_as`, `validate.rs:432`, already names bench boards). Let mem-read and validate take a probe serial as well as a role, behind the same identity gate. The api's `declare_signal`, `mem_read` and `validate` take the new forms.

## Why now

Decision 41 made the bench board flashable, and the first live session on it then needed its console, a halted read and a validate, and got none of the three by its own name.

## Done when

- [ ] topology: a `SignalLink` can name a board as its origin; existing rows with `origin_role` load unchanged.
- [ ] core: a reset resolved from a signal reaches the board it names, and refusals for a bench board's signal name that board.
- [ ] core: mem-read and validate accept a probe serial, with the same identity gate as by role.
- [ ] api: `declare_signal`, `mem_read` and `validate` (tools and subcommands) accept the board and probe-serial forms.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) in each repo touched.
- [ ] `spec.md`/`decisions.md`/`open.md` updated in each repo touched, `changelog.d/` fragment dropped.
