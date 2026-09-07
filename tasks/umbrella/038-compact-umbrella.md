# 038 — embarch-umbrella's spec.md is in reserve again

**State:** open
**Source:** scripts/check-doc-size.py, hit landing `tasks/umbrella/028`
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/spec.md

## What

`spec.md` is **9,257 / 10,240 B (90.4%), 983 B left** — pushed there by `028`'s one-clause
addition to the `status` command-surface row (decision 46: authenticated probe count, five
reported states). `009` paid this same file down to 87.9%/89.4% twice before (2026-09-05,
2026-09-06); it has drifted back up on ordinary row growth since, one small true addition at a
time, with no compaction pass run on it since `009`'s. Run `scripts/check-duplication.py
embarch-umbrella` first — `009`'s note that `decisions/doctor.md` was re-arguing build status
`spec.md`'s table already owns may have grown a sibling since.

## Why now

`DOC-COMPACTION.md`'s reserve is a debt notice, not a wall — the debt is real once a file is in
the last 10% of its cap, whether or not the unit that tipped it over is itself blocked.

## In flux: yes

`open.md` still lists check 17's two Fail branches as never having met a real narrow-bound Core,
check 13 comparing across a rewritten history, and the `saved.host`/check 2 stickiness gap — any
of which can rewrite a row of `spec.md`'s eighteen-row `doctor` table or its command-surface table
out from under a compaction pass written today. **Unparks when the umbrella task queue holds no
open task naming a `doctor`-chain or `status` row change**, whichever that turns out to be —
narrower than `009`'s old "queue down to one task" condition, since this file's volatile part is
specifically those two tables, not the whole sub-project.

## Must not delete

- The `doctor` chain table's designed-vs-built distinction, row by row (per-row, not by count —
  `009`'s own lesson: a count goes stale the moment one row's status changes).
- The `status` row's five-state list this task (`028`) just wrote in, and its "never a probe
  count of `0`" clause — the whole reason decision 46 exists.
- Anything `009`'s own `Must not delete:` still names that has not since been answered
  (`decisions/bind.md`'s two Fail-branch arguments, `saved.host`'s stickiness and why it was left
  unfixed) — check `open.md` before assuming any of those closed.

## Done when

- [ ] `spec.md` out of reserve (below 90% of its cap), by deletion or a split, not by trimming
      wording alone (`009`'s finding: 37 B of wording is not a real shave).
- [ ] The unbuilt/built distinction survives, per row.
- [ ] No question disappears from `collect-open-questions.py` unless it can be named as answered.
- [ ] `DOC-COMPACTION-PASS.md`'s question answered in the commit message: can `spec.md` alone
      answer what someone needs to work on this component today?
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/umbrella-*` fragment
      dropped.
