# 183 — `verify` checks a zip's call-log segment against its signed range

**State:** open
**Source:** `notes/hil/06-report-and-publish.md`, check 8: "the chain recomputes over each run's range of entries … a zip from before then carries no call-log segment, and its appendix says 'no call log'"
**Issue:** EMB-254
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/verify.rs` `check_log_segment` checks the run log's segment and then
prints "the call log: no call log (this zip has none)" for every zip. Since
`core/145`, a run's signed record carries `observed.call_log` =
`{prev, head, length, first_seq, last_seq}`, and a published zip can carry
`call-log-segment.jsonl`: a header line
`{"call_log_segment": {prev, head, first_seq, last_seq}}` followed by the
range's `{entry, hash}` lines (`embarch-core` decisions 111 and 116,
`embarch-core/interfaces/signing.md`).

When this is done, check 8 has a second half:

- When the zip holds `call-log-segment.jsonl`, every `hash`, `prev` and `seq`
  recomputes over the segment; it starts at the `prev` and ends at the `head`
  the signed record names, and holds exactly the `first_seq`..`last_seq` range
  it names. Every call-log entry a signed record cites is in it. No record
  cites one yet; write the check for the Test phase's citations, and test it
  with an invented citation.
- A zip with no segment reads "no call log", as now, and is not failed for it.
- The check names what it compared, as the run-log half does.

Read Core's own chain code (`embarch-core/src/` call log and `publish.rs`'s
segment writer) on `origin/main` for the hash rule, and say in your report
which function you matched.

`report-data.json` and the report's appendix are not touched here: they change
in a later cross-repo unit with Core's side, because check 6 fails on a key it
does not expect.

## Why now

A reader checking a zip offline, and the first Live session's published Study,
need the call log checked rather than reported absent. Core's half landed as
`core/145`.

**Burndown leg: no new numbered decision.** Amend the verify decision in
`decisions/verify.md` (or `verify-report.md`, whichever states check 8) in
place. If the work needs a new decision, stop and say so in this
file and in your report.

## Done when

- [ ] A fixture zip with a call-log segment passes check 8 and lists what it
      compared.
- [ ] Copies with an entry dropped, an entry altered, and a segment from
      another run each fail check 8, naming why.
- [ ] A milestone-1 fixture zip with no segment still passes, reading "no call
      log".
- [ ] `interfaces/verify.md` row 8 is amended.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped.
