# 184 — The live log's contract states the file's time zone, `sent`'s form and a writer's added fields

**State:** claimed by agent/api/184-live-log-states-zone-sent-form-and-added-fields, 2026-11-23 23:54
**Source:** worker and reviewer of `atlas/103` (2026-11-23): the atlas became the live log's second writer and had to guess four things `interfaces/live-log.md` does not say
**Issue:** EMB-290
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-api/interfaces/live-log.md` fixes the `embarch-live/1`
line shape. The atlas now writes decoded lines into the same file, and had to
assume these four things. When this is done, the doc states each one as
embarch-api's writer (`src/live_log.rs`, and `src/cli.rs` `finish`) already
behaves:

- **The time zone** of the file name's date and `HHMMSS`. embarch-api slices
  them out of the lease's `started_at` text as written, and uses UTC `now` for
  a `no-lease` file.
- **`sent`'s form, per writer.** The doc says "the subcommand as the CLI parsed
  it, a string". embarch-api writes the Rust debug form of the subcommand; the
  atlas writes a command line (`reg-read X --role y`). Say what each writer
  puts there, or what a reader may rely on.
- **A writer's added fields.** The atlas adds `outcome` (`answered`,
  `did-not-run`, `refused`, `no-reply`, `may-have-run`). The doc says an added
  field is no schema bump, but names no field a second writer may add or how a
  reader tells writers apart. Name `outcome`, or state the rule and where a
  writer's own fields are recorded.
- **`core_calls` on a failure.** embarch-api's `--json` output carries it on a
  failed call that reached a gated route. Say so.

Change no code unless the doc and the code disagree; if they do, say which you
changed and why in your report. The atlas's own fields and behaviour are the
atlas's: read them in `embarch-atlas`'s `src/embarch_atlas/livelog.py`, and do
not edit that repo.

## Why now

A reader of a Live session's log sees lines from both writers, and the atlas's
next live-log units (`atlas/104`, then `atlas/105`) build on the same contract.

**Burndown leg: no new numbered decision.** If a decision needs amending, amend
it in place. If the work needs a new decision, stop and say so in this file and
in your report.

**Doc size:** `embarch-api/open.md` is in reserve, 916 B left, with its debt
parked as `tasks/api/181` (blocked). Decision 90 (`decisions/lease.md`) is
already over its size line: do not grow it.

**Dispatch note (supervisor, 2026-11-24): compact `embarch-api/open.md` in
this unit.** `api/181`'s unpark condition has been met: the atlas's live-log
writers landed (`atlas/103` to `atlas/106`), and this unit is the one that
states the live log's contract, so its `open.md` item can be rewritten once,
here. Bring `open.md` out of reserve (at or below 3,919 B) by moving the
longest items into `open/` verbatim, leaving links, and carry `api/181`'s
`Must not delete:` list: the dated verification debts and their decision
citations stay. Do not edit `tasks/api/181`; I close it at the fold.

## Done when

- [ ] `interfaces/live-log.md` states the file name's zone, `sent`'s form, and `core_calls` on a failed call.
- [ ] It names the atlas's `outcome` field, or the rule for a writer's added fields.
- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-api/open.md`; moved text is byte-identical in its new file.
- [ ] Gate green (`../../embarch-fleet/gate.md`), with `EMBARCH_DOC_DIR` at your doc worktree if a test reads the docs.
- [ ] `changelog.d/` fragment dropped.
