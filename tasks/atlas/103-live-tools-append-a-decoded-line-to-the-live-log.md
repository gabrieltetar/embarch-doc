# 103 — The atlas's live tools append a decoded line to the live log

**State:** done — live tools append a decoded embarch-live/1 line, with every Core call-log entry, to the live log
**Source:** `notes/hil/05-live.md`, "The live log": "One file and one line shape, written by both embarch-api (raw calls) and embarch-atlas (decoded calls)"
**Issue:** EMB-266
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The atlas's decoded reads go through the `embarch-api` CLI, which since
`api/180` appends one raw line per hardware call to the firmware repo's
`embarch/live/` log. The decoded answer, the one the engineer reads, leaves no
trace: `live.py` writes nothing there. When this is done:

- After each live call (`reg_read`, `reg_read_clear`, `reg_read_bank`,
  `live_stacks`, `core_state`, `shell`, `shell_run`, and the CLI's `live`
  verbs), the atlas appends one decoded line in `embarch-api`'s shape
  (`embarch-doc/embarch-api/interfaces/live-log.md`, schema `embarch-live/1`),
  with its own `writer`, holding the decoded answer and every Core call-log
  entry the call made, taken from the CLI's `--json` output in `call_api`.
- It writes the same file `embarch-api` chose for that session, one write per
  line in append mode, so the decoded line follows the raw lines it decodes.
  Read `live-log.md` for how the file is named and found, and match it rather
  than re-deriving it.
- A call that did not run writes a line saying so, using the five shell
  answers `live.py` already tells apart.
- The lease token never reaches a line (`_scrub`).

Where: `src/embarch_atlas/live.py` (`call_api`, `lease`, `_scrub`, `reg_read`,
`shell`, `live_stacks`), `src/embarch_atlas/corestate.py`,
`src/embarch_atlas/mcp_server.py`; `DESIGN.md` "Live" and
`embarch-doc/embarch-atlas/design.md`.

`embarch-api`'s file is not yours: if `live-log.md` lacks something the atlas
needs (a field, a naming rule), write it into `embarch-atlas`'s docs as an
assumption and say so in your report, and the supervisor files it.

## Why now

The engineer reading a Live session back needs the decoded answers beside the
raw calls, and the atlas's write-back of a measured fact (EMB-267) names a
live-log line beside Core's entry. `embarch-api`'s writer landed as `api/180`.

**Burndown leg: no new numbered decision.** Amend in place where a decision
needs it. If the work needs a new decision, stop and say so in this file and in
your report.

## Done when

- [x] With a fake `embarch-api` returning Core entries, a `reg_read` appends
      one decoded line naming them.
- [x] A `shell` call that reads an external part's register over several
      exchanges names every entry.
- [x] A call refused before the write appends a line saying it did not run.
- [x] No line carries the lease token (a test).
- [x] `DESIGN.md` "Live" and `embarch-doc/embarch-atlas/design.md` say what the
      atlas writes and where.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [x] `changelog.d/` fragment dropped.
