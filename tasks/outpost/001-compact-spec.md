# 001 — embarch-outpost/spec.md is in reserve

**State:** open
**Source:** scripts/check-doc-size.py --pressure
**Scope:** outpost
**Hardware:** none
**Compacts:** embarch-outpost/spec.md
**In flux:** no
**Must not delete:** §4's measured cost table with its provenance — the instrument's own overhead is the number every conclusion drawn from a trace rests on; the statement that **both clocks are on the wire and neither substitutes for the other**, which is what layout 3 changed and what §1–§2 went on contradicting for days after it landed.

## What

`spec.md` is at ~90% of 10 KB, the shallowest entry in the reserve, so this is
the least urgent of the seven and the one with the most room to be done well.

**This sub-project has already had the §9 pass** — it is the only entry in
`check-doc-size.py`'s `TIGHTENED` map, and its decision groups are held at 8 KB
because of it. §9 says do not run that pass twice: a sub-project at its hot
floor has no cold half left and further cuts take rules. So the answer here is
**not** another hot/cold sweep of `decisions/`. It is either a genuine
duplication (run `scripts/check-duplication.py embarch-outpost`, which reports
31 overlaps — by far the most in the suite, including a 36-word run between
`decisions/tracing.md` and `open.md`) or a reference table that belongs in
`interfaces/`, where `wire.md` and `integration.md` already are.

## Why now

Deepest in the reserve of the three specs, and the 31 overlaps say the bytes
are there without touching a rule.

## Done when

- [ ] `spec.md` out of reserve, and the duplication count down.
- [ ] No decision text is cut. If you conclude bytes can only come from rules,
      say so here and stop — that is a real answer and §9 predicts it.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/outpost-*` fragment dropped.
