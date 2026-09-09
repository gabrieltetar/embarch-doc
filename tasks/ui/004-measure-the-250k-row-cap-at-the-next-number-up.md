# Measure the 250,000-row view cap at the next number up, so raising it stops being an extrapolation

**State:** claimed by agent/ui/004-measure-the-row-cap, 2026-09-09 00:18
**Source:** `embarch-ui/open.md` — "it should be made against a measurement at the new number rather than by extrapolating this one"
**Scope:** ui
**Hardware:** none
**Owner:** no

## Supervisor's dispatch note, leg 058 (2026-09-09, burndown)

**Doc-size reserve in `embarch-ui`** — one file is inside the last 10% of its cap, and a second is
53 bytes clear of the line and will re-file itself on the next byte:

- `embarch-ui/spec.md` — 9,461/10,240 B, **779 B left**; filed against `tasks/ui/018-compact-ui-spec.md`
  (state `open`, not blocked), so you owe no new compaction task for it.
- `embarch-ui/decisions/study-designer.md` — 11,007 B against an 11,059 B reserve line: **53 B of
  clearance**, deliberately left there by leg 057 after that file was caught losing an invariant to
  a squeeze. **Do not write to it and do not shave it.** If your measurement genuinely belongs
  there, stop and say so in your report.

`embarch-ui/open.md` is not in reserve, which matters because rewriting its cap bullet is one of
this unit's Done-when items. **That is where the measured numbers go.**

**This leg runs in burndown mode: do not author a new numbered decision.** The Done-when's "the cap
is either changed or explicitly kept, with the number cited" is satisfied by recording the
measurement and the resulting cap in `open.md` and in the `changelog.d/` fragment, marked
`[measured 2026-09-09, <build>]` per `DOC-CONVENTIONS.md`. **Keeping the cap where it is, with the
measurement as the stated reason, is a complete and legitimate outcome** — the task says so
explicitly. If you conclude the outcome needs its own numbered decision in
`decisions/trace-transfer.md`, stop and say so in your report rather than writing one.

If your work pushes a file into reserve or leaves one there unfiled, file
`tasks/ui/<next free NNN>-compact-ui.md` in the same commit (`tasks/README.md` has the shape, and
the path is `tasks/ui/`, never `tasks/doc/`).

## What

`embarch-ui/open.md` says the 250,000-row cap "is now the only term left, and the reason it was set
is gone". The cap is `src/trace.rs:120`. The instrument already exists at `src/trace.rs:3748`
(`summarise_a_capture_from_disk`, `EMBARCH_VIEW_CSV`) but needs a real file on disk.

Add a synthesiser plus an `#[ignore]`d measurement test that builds captures of the committed
fixture's shape at 250k / 500k / 1M rows and prints decode time, resident view size and `/bins`
payload size at a reference grid width. Put the numbers in `open.md` (or a decision), then either
raise the cap with the measurement beside it or leave it where it is **with the measurement as the
reason**. Both outcomes close this; an unstated one does not.

## Why now

`open.md` states the decision is blocked only on a measurement at the new number, and
`decisions/trace-transfer.md` 18 already removed the transfer half of the original justification.
Nothing else about it is open.

## Done when

- [ ] A synthesiser and an `#[ignore]`d measurement test exist and run from a documented one-line
      invocation, needing no file on disk.
- [ ] Decode time and both payload sizes are recorded at three row counts, marked
      `[measured <date>, <build>]` per `../../DOC-CONVENTIONS.md`.
- [ ] The cap is either changed or explicitly kept, with the number cited.
- [ ] `open.md`'s bullet is rewritten to what is now unknown.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
