# 038 — embarch-umbrella's spec.md is in reserve again

**State:** blocked — **state corrected by leg 057, 2026-09-09.** This task's own `## In flux: yes`
section below names its unparking condition ("the umbrella task queue holds no open task naming a
`doctor`-chain or `status` row change") and that condition is **not met**:
`tasks/umbrella/033-settle-check-17s-two-fail-arms-against-a-real-narrow-bound-core.md` is open and
is exactly a check-17 doctor-chain row change. A compaction task whose `In flux:` says yes must not
be dispatched (`.claude/leg.md`), so the state line was wrong rather than the flux. **Unparks when
`033` lands** — or when whatever open umbrella task names a `doctor`/`status` row change is gone.
**Source:** scripts/check-doc-size.py, hit landing `tasks/umbrella/028`
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/spec.md, embarch-umbrella/open.md
**Size debt due:** 2026-09-12

## Clock brought forward by leg 066, 2026-09-10 — from 2026-09-30, and here is why

`umbrella/036` landed today and **spent the reserve rather than paying it**, on both of this
task's files:

| file | before `036` | after `036` | left |
|---|---|---|---|
| `spec.md` | 10,104 B (98.7%) | **10,144 B (99.1%)** | **96 B** |
| `open.md` | 4,870 B (95.1%) | **4,996 B (97.6%)** | **124 B** |

Nothing was done wrong. My dispatch note offered `036`'s worker two paths — make the `spec.md`
edit net-zero-or-negative, or compact `spec.md` as part of the unit carrying this task's
`Must not delete:` list — and it took the first, honestly, within the 136 B it was told it had.
Its closing note describes this as "no new debt was created and none was paid down", which is
true of *this ledger's* bookkeeping and misleading about the file: **96 bytes is not headroom, it
is a wall one row-edit away.**

**So the date moves, because the date is the only thing that makes a park non-absorbing.** The
`In flux: yes` argument below is unchanged and still correct — `tasks/umbrella/033` is open and is
exactly a check-17 `doctor`-chain row change — so this task is **still `blocked` and still must
not be dispatched as a compaction unit while that holds.** What the earlier date buys is that a
leg's first-unit ledger check surfaces it in two days rather than twenty, at which point whoever
looks has three options and should pick deliberately:

1. **Land `tasks/umbrella/033`**, which unparks this task properly and is the intended path.
2. **Split `spec.md`** — `DOC-COMPACTION.md` §2's mission split, which a verbatim move makes safe
   even under `In flux: yes`, exactly as `outpost/008` did to `decisions/tracing.md` this same
   leg. The eighteen-row `doctor` chain table is the obvious candidate to move out, and it is also
   the volatile part this task's flux argument is about — moving it verbatim into its own file
   would leave `spec.md` stable *and* give the volatile table room to change.
3. **Accept that the next `umbrella` unit touching `spec.md` must compact it in-flight**, which is
   what `DOC-COMPACTION.md` §2 already says for a file whose compaction task is parked.

**Option 2 is the one nobody has considered for this file** and it is the reason I am recording
this rather than only moving a date: this task's flux argument has parked `spec.md` since
2026-09-09 on the grounds that its `doctor` table may be rewritten, while the split that would
make that rewrite cheap is available and unblocked by the same argument.

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

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.
