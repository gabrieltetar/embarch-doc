# 121 — A bench study whose tap names a captured signal is refused only by the OS

**State:** open
**Source:** `embarch-core/open.md` — "A bench study's signal tap is still a second port owner beside a capture (a host study's taps are captures, decision 98). A capture refuses a tap's port; a study started on a captured signal is refused only by the OS." Filed by the 2026-10-28 15:00 leg's refill sweep.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`POST /study` (a bench study) accepts a study whose signal tap names a signal that a decision 92
capture (`decisions/signal-capture.md`) is holding open. Nothing in Core checks this, so the study
takes `hw_lock`, flashes and resets the board, and only then fails when the tap's port open is
refused by the operating system, with an OS error that names neither the capture nor the signal.
The two neighbouring paths already refuse this up front: `POST /host-studies` starts its taps as
captures at submission and answers `409` when one is running (`decisions/host-study.md`), and
`GET /serial-log?signal=` answers `409` on a running capture before it opens anything (decision 101,
`decisions/logging.md`, `serial_log_handler` in `src/api.rs`). When this is done, a bench study
whose taps include a captured signal is refused at submission with a `409` that names the signal
and says a capture holds it, before the board is flashed or reset. Pick the check's place yourself: the registry lookup the
serial-log path uses is the obvious model. If you find the bench path should instead reuse the
capture's handle the way a host study does, say so in a decision and do the refusal anyway; the
reuse is a separate change.

## Why now

`core/120` added the same refusal to `GET /serial-log` this leg, so the bench-study path is now the
only signal consumer that meets a running capture at the OS. The open.md bullet has no trigger
and no owner.

## Done when

- [ ] `POST /study` with a tap on a captured signal answers `409` naming the signal and the capture, before any flash or reset; a unit test drives it through the router with a registered capture.
- [ ] A study whose taps name no captured signal is unaffected (existing tests stay green).
- [ ] The open.md bullet is closed or narrowed to what is still true.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
