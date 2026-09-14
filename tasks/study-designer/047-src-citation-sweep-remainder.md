# 047 — Citation sweep: `src/` remainder after `gatt_extract.rs`

**State:** claimed by agent/study-designer/047-src-citation-sweep-remainder, 2026-09-13 22:36
**Source:** `tasks/study-designer/046`, which swept `src/gatt_extract.rs` (the
third of four files `044` named) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

## What

`044` counted 435 `decision[s] N`-matching lines across `src/`. Three of the
four files it named are now swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
34  src/lib.rs            — not yet swept
```

…and ~239 more lines across the rest of `src/` (every other file), also not
yet swept.

Take one file — `src/lib.rs` next, per `044`'s own ordering — read every cited
decision's body against the sentence around the citation, and fix what is
wrong. Count wrong *numbers* and false *sentences* separately, per the method
below. When you run out of budget, file the next `tasks/study-designer/<next>`
naming exactly which files remain, the same way this one does.

**`lib.rs` is a large file** (1159 lines; a rough same-methodology recount
gave 41 lines matching `[Dd]ecision`, close enough to `044`'s 34 that either
count is a fine starting estimate — recount precisely before trusting either).
It is comparable in size to `gatt_extract.rs`, which took this task's full
budget on its own; do not assume it is cheap, and file the remainder honestly
if it is not fully swept.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-ui`, `embarch-umbrella` all depend on it), so its
comments are read from four other repos' default citation index, which makes a
bare `decision N` genuinely ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`/`045`/`046`, confirmed useful all three times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all three
sweeps in this one, has been prose a decision made false or a citation
pointing at the wrong (but real) decision, not a bare typo. Count the two
categories separately and report both, honestly, even if one or both is zero —
"checked N, found none" is a legitimate result.

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one bare cross-repo
citation, `045` found a second, structurally identical one. `046` found none —
the file's one cross-repo citation (`embarch-ui decision 17`) was already
correctly labelled. Check every bare `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless.

**Git history of the decisions file is worth checking when a citation's
credit looks off.** `046`'s two false-sentence findings both resolved cleanly
by running `git log --follow -p -- embarch-study-designer/decisions/<file>.md`
and reading how the cited paragraph's wording evolved — one showed a decision
explicitly walking back its own earlier claim ("weaker than this decision
claimed"), the other showed a fact attributed to a *later* decision number had
actually been folded into the *earlier* one "the same session." Don't stop at
"does the decision doc currently say this" — check whether it once said
something the source comment still assumes.

**A wrong number is not always a nearby-digit typo, and not every
over-attribution is a "wrong number."** `045` found three wrong numbers (a
real decision cited in the wrong repo; a structural rule attributed to the
decision that *used* it rather than the one that *established* it; a paired
decision over-cited from a different table row). `046` found three more of the
same "established vs. credited" shape — a design fact belonging entirely to
decision 56 was additionally credited to decision 57 in three separate
comments, when decision 57's own text has zero connection to it — plus two
*false sentences* where the cited number was right but the specific claim
built on it was stale (an undercount of how many failure modes a decision
adds; a "byte-for-byte" comparability claim the cited decision's own text had
already walked back).

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations. Zero wrong numbers,
  zero false sentences, one unlabelled cross-repo citation (fixed).
- `src/study.rs` — done in `045`. 52 citations read against
  `decisions/seals.md`, `study.md`, `declares.md`, `removed.md`, `ble.md`,
  `gatt.md`, `streams.md`, `protocols.md`, `protocol-exec.md`,
  `payload-meaning.md`, `authoring.md`, plus `embarch-dev-bench` decisions
  18/38/39, `embarch-api` decisions 26(wrong→27/28)/36, `embarch-topology`
  decision 3, and `embarch-decision-reversals.md` row 37. **3 wrong numbers, 0
  false sentences, 1 unlabelled cross-repo citation — all fixed.**
- `src/gatt_extract.rs` — done in `046`. 36 citations read against
  `decisions/gatt-extract.md` (33, 56, 57), `decisions/gatt.md` (31, 32),
  `decisions/seals.md` (18), `decisions/crate.md` (23), and `embarch-ui`
  decision 17 (already correctly labelled). **3 wrong numbers (a design fact
  belonging solely to decision 56 was additionally credited to decision 57, in
  three separate comments — the doc file's own git history shows the fact was
  folded into 56 "the same session", with no connection to 57 at all), 2 false
  sentences (an undercount of decision 57's three failure modes stated as
  "two"; a "byte-for-byte comparability" claim decision 33's own text already
  disclaims as "weaker than this decision claimed" — compare as sets instead),
  0 unlabelled cross-repo citations — all fixed.**

## Done when

- [ ] One named file (`src/lib.rs`, unless a reason is given to reorder) fully
      swept, wrong numbers and false sentences counted separately.
- [ ] Cross-repo citations in it carry their repo name.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note. Check
`scripts/check-doc-size.py` fresh rather than trusting this number — a comment
sweep should not need either file regardless. If this sweep turns up a
question worth recording, file it as `tasks/study-designer/<next>` rather than
adding to `open.md`.

## Ride-along, added by leg 111's supervisor at `046`'s fold

**One word of `046`'s own fix points the wrong way, and it is a free fix for
whoever opens `src/gatt_extract.rs` next.** `046` corrected the module doc's
undercount to *"Two of the three failure modes decision 57 adds outright — the
third, an empty walk, is [`ExtractError::NoSourceFilesFound`] **above**"*. The
arithmetic is right and `046`'s reviewer confirmed it against decision 57's
three named failure modes — but that variant's own doc comment sits **below**
the module doc in file order, not above. Change the direction word; nothing
else. It carries no decision claim, which is why `046`'s reviewer raised it as
a nit rather than a finding, and why it is a ride-along here rather than a task
of its own.
