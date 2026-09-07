# 015 — The unknown-outcome band borrows the hatch that means "the firmware lost records"

**State:** open
**Scope:** ui
**Hardware:** none
**Source:** `embarch-reviewer` on `tasks/ui/014`, leg 034, 2026-09-07. Filed by the supervisor
rather than fixed in the fold, on purpose — see *Why this was not fixed at the fold* below.

## What

`ui/014` (code `624cdb0`, doc `4ec4e92`) closed a real bug: a step outcome arriving in either of two
wire shapes used to be decoded by two half-decoders, each silent on the other's input, so a step
that **failed** could render as a step that did not. That fix is sound and is not in question here.

To satisfy the task's requirement that an unrecognised shape never render as a pass or a neutral,
the trace band for an unknown outcome was given a danger-red stroke **filled with the `tr-gap`
hatch pattern**. That is the contradiction.

**`tr-gap` already means something specific, and it is a fact about the DUT rather than about the
client.** `embarch-ui` **decision 10** (`decisions/trace-view.md` — left standing, untouched by
`ui/014`) and `assets/app.js`'s own unchanged comment establish a deliberate **two-hatch
vocabulary**:

- **`tr-cross`** — a span whose *continuity* the data cannot vouch for.
- **`tr-gap`** — specifically an interval **the firmware said it lost records in**, tied to
  `records_lost` / `unbounded_start`. It is a report from the DUT's ring buffer.

An `Outcome` value the client failed to parse has nothing to do with dropped hardware records. So
the same red diagonal hatch now means both *"hardware dropped data here"* and *"the UI could not
parse a string"*, distinguishable only by hovering — **which is the exact ambiguity decision 10 was
written to prevent.**

## Why this matters more than a colour choice

The trace view's whole job is telling an engineer which parts of a capture they may trust. A hatch
that means "the DUT lost data" is a claim about the hardware; borrowing it for a client-side parse
failure makes the view **report a hardware fault that did not happen**. That is worse than the
neutral-dash bug `ui/014` fixed, in the one direction that matters: the old bug under-reported a
problem, this one misattributes one.

## What to do

Give the unrecognised-outcome band its own fill, **or** use `tr-cross`, whose meaning ("cannot
vouch for this span") is the honest one for a value the client could not read. Whichever you pick:

- Say in the decision record which of the two you chose **and why the other was wrong** — this is a
  question about a visual vocabulary, so the argument is the deliverable, not the CSS.
- **Amend decision 23** (`embarch-ui/decisions/trace-chart.md`, filed by `ui/014`) rather than
  filing a new decision, unless you are actually extending the vocabulary to a third hatch — in
  which case decision 10 is the one that needs the amendment, and say so.
- The step-table half of `ui/014`'s fix — a red `badge-danger "?"` — was checked by the reviewer and
  is **fine**. Do not change it; only the trace band is wrong.

**Do not revert `ui/014`.** Both SHAs are clean single-purpose commits and a revert is technically
available, but it would restore the silent-unknown-shape bug the unit existed to fix. This is a
forward fix.

## A related question worth answering while you are in here, but only if it is cheap

`ui/014`'s decision 23 landed in `decisions/trace-chart.md` rather than `decisions/study-designer.md`,
and one of the reasons given was that `study-designer.md` is at **98.2%** of its cap. **A file being
full is not an argument about where a decision belongs** — that pattern (the reserve making the
placement call, with the argument arriving afterward to agree with it) has recurred across several
legs and is named repeatedly in the supervisor log. The worker's *other* reason is real and
free-standing: the change spans both the step table and the trace chart. The reviewer judged that
sufficient and did not file it. If you touch decision 23 anyway, it is worth one sentence saying
which file is the right home on the merits, so the next reader is not left to wonder whether the
cap decided it.

## Doc-size reserve for this scope

`embarch-ui/decisions/study-designer.md` is at **98.2%** (12,064/12,288 B, **224 B left**), filed
against `tasks/ui/011-compact-ui-study-designer-decisions.md`. `decisions/trace-chart.md` had
headroom as of `ui/014`. Check `check-doc-size.py --pressure` yourself before writing, and if your
work pushes a file into reserve or leaves one there that nothing has filed, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

## Done when

- [ ] An unrecognised outcome in the trace band no longer renders as `tr-gap`.
- [ ] `tr-gap` still means only "the firmware reported lost records", and decision 10's two-hatch
      vocabulary is intact — or is deliberately extended, with that argued.
- [ ] The step table's `badge-danger "?"` is unchanged and still visible.
- [ ] Gate green; `changelog.d/ui-*` fragment.
