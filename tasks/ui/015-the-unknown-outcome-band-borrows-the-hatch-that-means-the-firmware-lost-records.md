# 015 — The unknown-outcome band borrows the hatch that means "the firmware lost records"

**State:** done — leg 035, 2026-09-07, branch `agent/ui/015-unknown-outcome-hatch` / `agent/ui/015-unknown-outcome-hatch-doc`.
**Scope:** ui
**Hardware:** none
**Source:** `embarch-reviewer` on `tasks/ui/014`, leg 034, 2026-09-07. Filed by the supervisor
rather than fixed in the fold, on purpose — see *Why this was not fixed at the fold* below.

**Doc-size reserve in `embarch-ui` (leg 035, measured at dispatch).** One file is in reserve:
`embarch-ui/decisions/study-designer.md` at **12,064 / 12,288 B — 224 B left (98.2%)**, debt already
filed as `tasks/ui/011` (`open`, not blocked). Two more are just under the line and are the ones your
work is most likely to touch: `decisions/trace-chart.md` at **11,035 / 12,288 B (89.8%, 1,253 B
left)** and `decisions/trace-view.md` at **10,989 / 12,288 B (89.4%, 1,299 B left)** — decision 10,
the hatch vocabulary this task is about, lives in the latter and decision 23 in the former. Neither is
in reserve yet, so you have room, but a long new decision in either will push it in. **If your work
spends the reserve — pushes a file into it, or leaves one there that nothing has filed — file
`tasks/ui/<NNN>-compact-ui.md` in the same commit** (`tasks/README.md` has the shape; the path is
`tasks/ui/`, never `tasks/doc/`). Prefer amending decision 10's existing text over adding a fourth
hatch decision if the amendment says the same thing in fewer bytes.

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

**Answered:** touched decision 23 (amended it), so answering this. `trace-chart.md` is the right
home on the merits, independent of either file's cap: decision 23 is about a **rendering** decision
— which of two wire shapes a decoder reads, and how the *drawing* marks an unrecognised one — made
entirely in `app.js`'s chart/step-row code, not about the study-designer's own result-schema
concerns that `study-designer.md` otherwise holds. The change touching both the step table and the
trace chart (the worker's free-standing reason) is what makes it belong to neither alone, but the
decision's subject — a rendering idiom — sits with the other rendering decisions in `trace-chart.md`
and `trace-view.md`, not with schema/data-shape material in `study-designer.md`.

## Doc-size reserve for this scope

`embarch-ui/decisions/study-designer.md` is at **98.2%** (12,064/12,288 B, **224 B left**), filed
against `tasks/ui/011-compact-ui-study-designer-decisions.md`. `decisions/trace-chart.md` had
headroom as of `ui/014`. Check `check-doc-size.py --pressure` yourself before writing, and if your
work pushes a file into reserve or leaves one there that nothing has filed, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

## Done when

- [x] An unrecognised outcome in the trace band no longer renders as `tr-gap`. `assets/app.js`'s
      step-row fill now uses `tr-cross` for `decoded.kind === "unknown"`; the stroke stays
      `traceOutcomeColor`'s danger-red so the band still reads as wrong, not calm. Chose reuse of
      `tr-cross` over a third hatch: its existing meaning, "this view cannot vouch for this span",
      is honestly what an unparsed value is, and both `trace-chart.md`'s decision 23 and this file
      are near their byte cap, so a new decision would have cost more than a one-line swap said.
      Verified by reading the diff and the surrounding code; **not observed rendering** — there is
      no `node` on this machine and `src/trace.rs`'s browser harness is `#[ignore]`d, so nothing
      about the pixels was actually seen, only reasoned about.
- [x] `tr-gap` still means only "the firmware reported lost records", and decision 10's two-hatch
      vocabulary is intact. Not extended: reused the existing `tr-cross` token rather than adding a
      third, per the task's own preference and the reserve pressure on both `trace-view.md` (1,299 B
      left before this task, decision 10's home) and `trace-chart.md` (was 1,253 B left, decision
      23's home).
- [x] The step table's `badge-danger "?"` is unchanged and still visible — untouched in this diff;
      confirmed by reading `outcomeBadge` (unchanged) and the amended lines around it.
- [x] Gate green; `changelog.d/ui-trace-band-unknown-outcome-hatch.fixed.md` filed. `cargo build`,
      `cargo test` (101 passed, 2 pre-existing ignores), `cargo clippy --all-targets -- -D warnings`
      all clean in the code worktree; `scripts/check-docs.py` reports "all 10 checks green" in the
      doc worktree, including `check-doc-size.py` after filing `tasks/ui/016-compact-ui.md` for
      `trace-chart.md`'s reserve crossing (95.2%, 590 B left, caused by amending decision 23).
      `check-client-names.py --repo` clean; `check-ownership.py --scope ui` (doc, 3 paths) and
      `--code-repo` (code, whole tree) both green.
