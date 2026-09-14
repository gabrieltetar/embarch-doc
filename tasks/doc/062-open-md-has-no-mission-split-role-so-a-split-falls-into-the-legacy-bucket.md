# 062 — Give `open.md` a mission-split role in `check-doc-size.py`

**State:** open
**Source:** `inbox/` drop written by `tasks/ui/053-compact-ui.md`'s worker mid-task, 2026-09-14;
filed here by leg 115 in `ui/053`'s own fold. The body below is the worker's own text, unedited
except for this line and the title. **Leg 115 re-checked the `Hardware:` claim independently** — a
`scripts/` regex and a `DOC-BUDGET.md` §3 paragraph, nothing built or run: `none` is correct.
Original source line: `tasks/ui/053-compact-ui.md`. That task's own text argued the suite should
"consider a split rather than a third squeeze" for `embarch-ui/open.md`, which had come back
into reserve four units after `ui/050` squeezed it out. I looked for a real seam (three
trace/outpost bullets vs. four unrelated ones) and concluded split was the right shape in
principle, but the suite's tooling has no way to do it cleanly, so I squeezed instead
(113+ B, well within the `Must not delete:` list) and am dropping this instead of inventing
one myself.
**Scope:** doc
**Hardware:** none
**Owner:** required — this is a `scripts/` change, reserved.

## What

`scripts/check-doc-size.py`'s `CAPS` list gives `decisions.md` and `interfaces.md` a mission-split
extension (`decisions/<topic>.md`, `interfaces/<topic>.md`, both 12 KB, both documented in
`DOC-BUDGET.md` §3) but gives `open.md` none. A file matching neither `^embarch-[a-z-]+/open\.md$`
nor any other named role falls through to `legacy` (25 KB, unratcheted, explicitly described in the
script's own comment as "the migration's job is to turn it into one of the roles above") — so a
sub-project that genuinely needs to split its open questions by mission today has no supported way
to do it: the split file would land in a bucket DOC-BUDGET.md's four-file shape (§3) doesn't
recognise, with none of the size discipline the rest of the corpus gets.

Add an `open-group` role (`^embarch-[a-z-]+/open/[a-z-]+\.md$` or similar, cap TBD — probably the
same 5 KB `open.md` gets, since the reasons a single open.md is small apply per-mission too) and
document the convention in `DOC-BUDGET.md` §3 next to the other two.

## Why now

Not urgent — `embarch-ui/open.md` is out of reserve again after `ui/053`'s squeeze, 3,879/5,120 B.
But this is the second time in four units that file has hit its cap on genuinely new content
(`ui/050` squeezed, `ui/051` immediately refilled it, `ui/053` squeezed again), and `DOC-BUDGET.md`'s
own rule is "a split is the default remedy and squeezing is the exception" — the exception is
currently forced on `open.md` by a tooling gap, not by there being no seam. If it happens a third
time, squeezing stops being defensible and there still won't be anywhere for the split to land.

## Done when

- [ ] `check-doc-size.py`'s `CAPS` recognizes a split-by-mission shape for `open.md`, at some cap.
- [ ] `DOC-BUDGET.md` §3 documents the convention, matching how `decisions.md`/`interfaces.md` are
      described.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
