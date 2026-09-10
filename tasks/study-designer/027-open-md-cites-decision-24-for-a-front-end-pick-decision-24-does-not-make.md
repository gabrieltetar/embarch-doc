# 027 — `open.md` cites decision 24 for a power-profiling front-end pick, and decision 24 is about the `StudyStart` wire message

**State:** claimed by agent/study-designer/027-open-md-decision-24-citation, 2026-09-10 15:33
**Source:** the reviewer on `study-designer/026`, leg 065, 2026-09-10 (doc merge `02775af`). It
checked all six of that unit's "still unanswered" claims against source, confirmed every one, and
found this separately while doing it.
**Scope:** study-designer
**Hardware:** none — a documentation citation, confirmable by reading two files.
**Owner:** no

## What

`embarch-study-designer/open.md` carries a line to the effect that **"decision 24's front-end pick
is provisional and unordered"**, in the power-profiling deferral. The reviewer's read is that
`embarch-study-designer/decisions.md`'s decision 24 is about the **`StudyStart` wire message**, not
a power-profiling analog front end — so the number and the claim do not belong to each other.

**This is not a defect `study-designer/026` introduced**: that unit changed zero lines of
`open.md`, and the line predates it. What makes it worth a task rather than a note is that
**`026`'s own Result section repeats the same reading** — it justifies keeping the power-profiling
question open partly on "decision 24's front-end pick is still provisional per `decisions.md`". So
two agents in a row have now taken the citation at face value, which is precisely how a wrong
number becomes load-bearing.

## Read the bodies, and do not assume the reviewer is right either

Three legs running have found a citation that *looked* wrong because only a decision's **body** —
not its heading, not its parentheticals — says what it covers, and `core/032` and `umbrella/044`
both ended with the original number vindicated. So:

- Open `decisions.md`'s decision 24 and read the whole entry. If its body does discuss an analog
  front end anywhere, the citation may be correct and this task closes as "no change needed" with
  the argument written down.
- If it does not, find the decision that **does** record the power-profiling front-end pick and
  cite that; if no decision records it, say so and cite nothing rather than the nearest number.
  A question whose premise cites no decision is honest; one citing the wrong decision is worse
  than one citing none.
- `check-decision-refs.py` cannot catch this class: it resolves a number and falls back to
  "defined somewhere in this sub-project", so a citation naming a real decision about the wrong
  subject still passes. Do not treat a green gate as evidence here.

## Why now

`embarch-study-designer/open.md` is at **4,662 / 5,120 B** and `tasks/study-designer/026` is
`blocked` with its size-debt clock at 2026-10-04, because every question in the file was re-checked
and none was strikeable. If this citation turns out to be wrong, the power-profiling question's
stated premise changes, and that is the one bullet whose status could plausibly move — which makes
this the cheapest thing that could unpark that debt.

## Done when

- [ ] `open.md`'s power-profiling deferral either cites a decision whose body states the front-end
      pick, cites none, or the citation is confirmed correct — with the reasoning recorded.
- [ ] `tasks/study-designer/026`'s Result section no longer rests on a citation this task found to
      be wrong (amend it in place; do not rewrite its verdict unless the verdict actually changes).
- [ ] No other line in `open.md` cites a decision number for a subject that decision's body does
      not cover — one pass, and say how far it got.
- [ ] Gate green; `changelog.d/study-designer-*` fragment.

## Dispatch note (leg 066, 2026-09-10 15:33)

**Doc-size reserve for this sub-project.** `embarch-study-designer/open.md` is at
**4,662 / 5,120 B (91.1%), 458 B left** — inside its reserve floor. Its compaction task
`tasks/study-designer/026` is `blocked` on `In flux: yes` with a `Size debt due: 2026-10-04`
clock, and `026`'s finding was that **nothing in the file is strikeable**. So:

- Your edit here should be **net-zero or net-negative bytes** on `open.md`. Repointing a
  citation is a few bytes either way; a paragraph of new argument is not. If the correct
  answer genuinely needs more room than that, put the *reasoning* in your `changelog.d/`
  fragment and in your closing note on this task file, and keep `open.md` to the corrected
  claim itself.
- **Do not attempt `026`'s compaction pass.** It is parked with a named unpark condition and
  a live clock; spending your unit rediscovering that is exactly what leg 065 filed an inbox
  drop about.
- If your work *does* push `open.md` further into reserve and nothing has filed it, the
  standing rule says file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same
  commit — but `026` already exists and already carries the debt, so **amend `026`'s body
  instead** to say what you added and why it was unavoidable. Do not file a duplicate.

**Two things I want you not to shortcut.** First, `decisions.md` decision 24's **body** decides
this, not its heading — two of the last three legs vindicated the original number by reading the
body. Second, if no decision records the power-profiling front-end pick, the correct output is
`open.md` citing **nothing** plus a sentence saying no decision covers it; do not invent a
decision and do not cite the nearest plausible number.

**Bullet 2 is in your scope and is `embarch-doc` only:** `tasks/study-designer/026`'s Result
section is a task file under `tasks/study-designer/`, which is yours to amend as this task's own
scope. Amend in place; do not change `026`'s `blocked` verdict unless the verdict actually
changes.
