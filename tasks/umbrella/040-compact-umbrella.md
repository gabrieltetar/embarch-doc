# 040 — `decisions/reporting.md` is in reserve

**State:** blocked — its own `## In flux: yes` below says decision 46 is still moving, and a
compaction pass may not restate reasoning that is about to change. **Unparked by:** decision 46
settling, which means `tasks/umbrella/039`'s `bad-response` state surviving one further unit
without another amendment to 46. Corrected from `open` by the supervisor at `039`'s fold, leg 034:
the worker filed it `open` while declaring `In flux: yes`, and those two cannot both be right —
`queue-status.py` would have offered it for dispatch.
**Source:** scripts/check-doc-size.py, hit landing `tasks/umbrella/039`
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/decisions/reporting.md
**Size debt due:** 2026-09-28

## What

`decisions/reporting.md` is **11,589 / 12,288 B (94.3%), 699 B left** — pushed there by `039`'s
amendment to decision 46 (a sixth `ProbeReport` state, `bad-response`, split out of
`request-failed`). It was not in reserve before this change; `039` is what tipped it. Run
`scripts/check-duplication.py embarch-umbrella` first — decision 46's entry and decision 37 both
discuss which states/codes exist and why, and that pairing is exactly the kind of restatement
`009` found once already in this same sub-project (against `decisions/doctor.md`).

## Why now

`DOC-COMPACTION.md`'s reserve is a debt notice, not a wall — the debt is real once a file is in
the last 10% of its cap, whether or not the unit that tipped it over is itself blocked.

## In flux: yes

Decision 46 is the entry that just moved (five states to six) and is named directly in this same
commit's `inbox`-sourced task. `open.md`/the task queue may still hold work that reads decision 46
(a consumer-facing `--json` shape question was flagged as possibly needing its own decision against
decision 11, and 039 judged it did not — a later worker could disagree). **Unparks when the
umbrella task queue holds no open task naming decision 46, `probe_report`, or the `status --json`
`probes` shape**, whichever that turns out to be.

## Must not delete

- Decision 46's full state list and each state's one-clause reason for existing (six now: `ok`,
  `unreachable`, `no-token`, `unauthorized`, `request-failed`, `bad-response`) — this is the
  contract `--json` consumers match on.
- The distinction decision 46 exists to name: a real zero and "wasn't allowed to look" never share
  a value — and, as of `039`, that a *transport* failure and a *successful request with an
  unreadable body* never share a value either.
- Decision 37's own content (codes vs. states) — a compaction here should stop restating it, not
  delete it from wherever it actually lives.

## Done when

- [x] `decisions/reporting.md` out of reserve (below 90% of its cap), by deletion or a split, not
      by trimming wording alone (`009`'s finding: a few bytes of wording is not a real shave).
      **Closed incidentally by `tasks/umbrella/031`**, not by this task: `031` needed to amend
      decision 43 and had no room, so it split decision 43 out verbatim into
      `decisions/message-rendering.md` (`DOC-COMPACTION.md` §2's split-first rule — a verbatim
      split restates nothing) and amended it there. `reporting.md` is now 9,064 / 12,288 B
      (73.8%), out of reserve. **Decision 46 was not touched** — its prose is byte-for-byte what
      it was before `031` — so this task's own driver (decision 46 still in flux) is unaffected
      and the task stays `blocked` on the condition below. Only this one item is ticked; the rest
      are still this task's job whenever it unparks.
- [ ] All six states and their reasons survive, per state, not by count.
- [ ] No question disappears from `collect-open-questions.py` unless it can be named as answered.
- [ ] `DOC-COMPACTION-PASS.md`'s question answered in the commit message: can `reporting.md` alone
      answer what someone needs to work on `status`'s probe reporting today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/umbrella-*` fragment
      dropped.
