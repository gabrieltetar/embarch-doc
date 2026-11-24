# 145 — A run's signed record names its call-log range, and publish carries the segment

**State:** open
**Source:** notes/hil/12-prevention.md — item 3: "Each signed record carries the call log's head and the run's range of entries, and the zip carries that segment beside the run log's"
**Issue:** EMB-250
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Core keeps a hash-chained call log (decision 122, `tasks/core/140`), but a run's
`record.dsse.json` predicate (`signing.rs`, `seal`) has no call-log field, and
publish writes only the run log's segment (`publish.rs`, `SEGMENT_FILE`). When
this is done:

- At a run's start Core notes the call log's head; at its end, the head again.
  The predicate's `observed` gains the call log's head at the end and the run's
  range (first and last `seq`): the entries made between the two notes.
- Publish writes `call-log-segment.jsonl` into the revision's folder: the
  range's entries, with the entry before the range named by its hash. The
  signed manifest lists it beside `run-log-segment.jsonl`.
- A run with no entry in its range gets an empty segment that still names the
  head, so "no call during the run" is a checkable statement.
- A run recorded before the call log existed keeps its record; its publish
  carries no call-log segment.
- `report-data.json` is **not** touched. `embarch-api`'s `verify` check 6 fails
  a zip whose `report-data.json` holds a key its recompute lacks (`embarch-api`
  decision 124), so the call log's line there lands with `embarch-api`'s side in
  a separate unit.
- A predicate `schema` bump only if the change needs one; say which in the
  amended decision.

`embarch-api`'s publish takes every file the signed manifest names, so it needs
no change; check that against its `src/publish.rs` (read only).

## Why now

The owner's HIL plan (`notes/hil/14-implementation-plan.md`) puts this after the
call log, which has landed. `verify`'s call-log half (EMB-254) and a published
report's call-log line (EMB-265) both wait on it.

**Burndown leg: no new numbered decision.** Record the change by amending the
publish decisions (116 to 120, `decisions/publish.md`) and `decisions/run-log.md`
decision 111 in place. Decision 111 has about 200 B left. **Leave decision 110
(`decisions/signing.md`) alone**: it is already about 2.5 KB over its per-decision
limit, so its predicate field list goes in `interfaces/signing.md`, with at most
a one-line pointer from 110 if one is unavoidable. If the change cannot be
recorded without a new decision, stop and say so in this file and your report.

## Done when

- [ ] A fixture run's `record.dsse.json` names the call log's head and the run's
      range, and still verifies with a standard DSSE check.
- [ ] Publishing it writes `call-log-segment.jsonl`, the signed manifest lists
      it, and its entries recompute to the recorded head.
- [ ] A run with no call in its range publishes an empty segment that names the
      head.
- [ ] A zip published with the segment still passes today's `embarch-api
      verify` (say how you checked; a fixture or reasoning from its checks).
- [ ] `interfaces/signing.md` and `interfaces/publish.md` name the new fields
      and file.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
