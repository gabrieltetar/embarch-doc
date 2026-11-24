# 180 — Each hardware call appends a line to the firmware repo's live log, citing Core's call-log entry

**State:** open
**Source:** notes/hil/05-live.md — "The live log": a readable mirror of Core's call log in the firmware repo, its fields "to fix with the first writer"
**Issue:** EMB-255
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Nothing writes `embarch/live/` in a firmware repo. The design (`notes/hil/05-live.md`):
`embarch/live/<date>-<session>.jsonl` is the call log's readable mirror,
untracked like the rest of `embarch/`: what was read or sent, to which board,
the image hash on it, the time, the answer, and Core's entry. One file and one
line shape, written by both `embarch-api` (raw calls) and `embarch-atlas`
(decoded calls). This unit is the first writer and fixes the fields. When this
is done:

- **One line per MCP tool call or CLI subcommand that reaches a lease-gated
  route**, written after Core answers: the tool; what was read or sent; the
  board (role or probe serial, and chip); the image hash from `GET /status`'s
  `last_images`, or "unknown"; the time; the status; the answer, cut past a
  stated size with its full SHA-256; and Core's entries (`seq` and `hash` from
  the `X-Embarch-Call-Seq` / `X-Embarch-Call-Hash` headers; several for a tool
  that makes several calls, such as `bench_exchange`). `run_study` and
  `run_host_study` are not Live and write no line.
- `--json` output carries Core's entries, so a caller of the CLI can cite them.
- A `call-log` subcommand (and an MCP tool if cheap) reads entries by `seq` or
  range through `GET /call-log`.
- **The file**: `embarch/live/<date>-<session>.jsonl`, the session being the
  lease holder and its start time. The repo is the one whose `embarch/` the
  process runs in, else the project's configured source path; with neither, no
  line, and the answer says so.
- **One `write` per line, in append mode**, so the atlas can append to the same
  file, and a `schema` field the atlas writes too.

Where: `src/tools.rs`, `src/cli.rs`, `src/main.rs` (the hardware tools and
subcommands), `crates/embarch-core-client/src/client.rs` (reading the response
headers; the crate is shared, keep it additive). Core's header and route are
`embarch-core` decision 122; read Core's `src/api.rs` but do not edit it.

## Why now

The engineer reading a Live session back has no trace in the repo, and the
atlas's live tools (EMB-266) and its write-back receipts (EMB-267) wait on this
file's shape.

**Burndown leg: no new numbered decision.** The design is the owner's, in the
note above; fix the line shape in a new `interfaces/live-log.md` and the spec,
and amend an existing decision in place only if one already covers it. If the
work cannot be recorded without a new decision, stop and say so in this file and
your report. `decisions/ledger.md` decision 98 has 15 B left and
`decisions/bench-exchange.md` decision 89 about 120 B: leave both alone.

## Done when

- [ ] Against a fake Core, a `mem_read` and a `reset` each append one line
      naming Core's entry, the board and the image hash.
- [ ] A call Core refuses appends a line with the refusal.
- [ ] `mem-read --json` output carries Core's entry, and `call-log` returns an
      entry by its `seq`.
- [ ] `interfaces/live-log.md` fixes the line shape, the file's name and its
      place.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
