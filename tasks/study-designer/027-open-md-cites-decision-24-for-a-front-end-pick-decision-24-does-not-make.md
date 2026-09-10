# 027 — `open.md` cites decision 24 for a power-profiling front-end pick, and decision 24 is about the `StudyStart` wire message

**State:** open
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
