# 058 — `embarch-api/decisions/core-link.md` is back in reserve

**State:** done — leg 071
**Source:** `agent/api/054-decision-26-retire-or-retitle` shrank decision 26 by
120 B while paying `tasks/api/026`'s reserve debt on this file, but the file
is still inside the reserve line; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/core-link.md
**Size debt due:** 2026-09-18
**In flux:** no — decision 26 (the last entry `tasks/api/026` was parking) is
now correct and stable; nothing known is about to rewrite this file's
remaining content.
**Must not delete:** every item `tasks/api/026` already named — decision 15's
failure signature, decision 36's rejected-alternative pair, and decision 55's
corrected `default_headers` rejection — still apply; `026` itself is `blocked`
on `spec.md`/`open.md` only, not on this file anymore.

## What

`decisions/core-link.md` is **11,962 / 12,288 B — 326 B left**, inside the
`max(1200 B, 10%)` reserve line (11,059 B). The next `api` unit that writes
this file has little room.

**Prefer a split over a squeeze**, per `DOC-COMPACTION.md` §2: this file still
carries several missions that a prior split (`tasks/api/026`, which pulled the
event stream out to `decisions/study-events.md`) did not touch — address
resolution (11, 14, 17), artifact transfer (15), the shared-client extraction
(37, 38), the per-machine logfile (43), the auth funnel (55), and the
older-Core parse rule (58). The per-machine logfile (43) and the auth funnel
(55) are the largest two entries and share no dependency on the rest; either
is a candidate verbatim move into a new `decisions/<topic>.md`, updating
`decisions.md`'s index.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that leaves it there is the one that must file it — `api/054` is that
commit; it paid `tasks/api/026`'s specific debt on this file (which was about
decision 26, not about the file's overall size) but did not clear the reserve
line itself.

## Done when

- [x] `decisions/core-link.md` is clear of the 11,059 B reserve line, by split
      or by squeeze. Now 9,955 B (was 11,962 B). Decision 43 (the per-machine
      logfile) moved verbatim to the new `decisions/logging.md`.
- [x] Whatever moved, moved verbatim; every `Must not delete:` item above is
      still readable at its new address. Decision 15's failure signature,
      decision 36's rejected-alternative pair, and decision 55's corrected
      `default_headers` rejection all still live in `core-link.md`, unmoved.
- [x] `decisions.md`'s index table names the new file, its decision number
      (43) and both files' sizes (`core-link.md` now 10.5 KB, `logging.md`
      1.6 KB), and `check-decision-refs.py` resolves every number.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `check-docs.py`:
      all 11 checks green.

## Report

`decisions/core-link.md`'s decision 43 (the per-machine logfile: why it's
per-user, the two-layer tracing subscriber, the rejected log-sink-to-Core
alternative) split out verbatim to a new `decisions/logging.md`, matching the
shape of the earlier `study-events.md` split. `spec.md`'s one citation of
decision 43 was repointed to the new file. No other file needed a reserve
task filed against it in this same commit — `check-doc-size.py` reports
"17 in reserve, all filed" with no new unfiled entries.

**Human question (DOC-COMPACTION-PASS.md):** yes — `spec.md` alone still
answers what someone needs to work on this component today. It carries the
mechanism for every decision this task touched (address resolution, artifact
transfer, the auth funnel, the logfile's per-user placement) with a
`[decisions](...)` pointer back to the *why*, and none of that pointer text
changed meaning — only the logfile pointer's target file changed, from
`core-link.md` to `logging.md`, and it was updated in this commit. Nothing in
`spec.md` depended on `core-link.md`'s byte layout, only on the decision
numbers still resolving, which `check-decision-refs.py` confirms.
