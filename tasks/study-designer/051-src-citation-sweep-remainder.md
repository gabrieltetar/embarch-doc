# 051 — Citation sweep: `src/` remainder after `streams.rs`

**State:** done by agent/study-designer/051-src-sweep-remainder, 2026-09-16
**Source:** `tasks/study-designer/050`, which swept `src/streams.rs` (the
largest of the 19 files `049` found remaining after `048`) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `050`,
2026-09-16): two files, both already filed against, unchanged.**
`embarch-study-designer/spec.md` 9,350/10,240 B (890 B left) and
`embarch-study-designer/open.md` 4,659/5,120 B (461 B left) — filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This unit
is a source-comment sweep and should not need to write either file; **if it
turns out you must**, spend the bytes and say so in your report, and if you
leave either file deeper in reserve than you found it, file
`tasks/study-designer/052-compact-study-designer.md` in the same commit per
`tasks/README.md`. Do not compact `spec.md` or `open.md` as part of this
unit — both have a live park and an owner.

## What

Seven of the four originally-named plus the three largest-remaining files are
now swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
41  src/lib.rs            — swept in 047 (recount; 044 estimated 34)
38  src/study_builder.rs  — swept in 048
32  src/protocol.rs       — swept in 049
29  src/streams.rs        — swept in 050
```

**18 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — a *line*
count, not a citation-instance count):

```
28  src/limits.rs
24  src/result.rs
22  src/bounded.rs
21  src/eap.rs
15  src/ffi.rs
14  src/crc.rs
13  src/eap_parse.rs
11  src/gatt.rs
 9  src/registry.rs
 8  src/outpost.rs
 8  src/decoder.rs
 7  src/sample.rs
 7  src/merged_actions.rs
 5  src/gatt_names.rs
 5  src/eap_interp.rs
 3  src/vendor.rs
 2  src/records.rs
 0  src/ids.rs — no citations; needs no sweep, listed so the count above is exhaustive
```

Take one file — `src/limits.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**Grep-line-count does not predict citation-instance count, and does not
predict cost.** `streams.rs` (29 grep-matching lines, a 788-line file) carried
31 distinct citation instances once multi-number lines (`embarch-outpost
decisions 11, 12`; `decisions 34 and 36` twice) were counted separately, and
resolved in one leg with room to spare: eight distinct decisions files (this
crate's own `streams.md`, `registry.md`, `authoring.md`, `gatt.md`,
`seals.md`, `versioning.md`, `payload-meaning.md`) plus four cross-repo files
(`embarch-topology/decisions/links.md` and `crate.md`,
`embarch-outpost/decisions/capture.md` and `manifest.md`,
`embarch-core/decisions/streams.md`), all short enough to read directly. The
one defect found resolved by direct textual match, no `git log` needed.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`050`, confirmed useful all seven times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all seven
sweeps in this one, has been prose a decision made false or a citation
pointing at the wrong (but real) decision, not a bare typo. Count the two
categories separately and report both, honestly, even if one or both is zero —
"checked N, found none" is a legitimate result.

**A cross-repo citation that resolves to a real, on-topic decision is not
automatically suspect just because it feels surprising.** Read the far-repo
decision's own text before concluding a cross-repo cite is wrong — a
coincidence in numbering is not evidence either way (`049`'s
`embarch-dev-bench decision 39` case, confirmed correct).

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one bare cross-repo
citation missing its label, `045` found a second, structurally identical one.
`046`, `047` and `049` found none. `048` found the *opposite* shape: a
same-repo decision mislabelled *as* foreign. `050` found a **third** shape: a
cross-repo decision correctly labelled on its first two mentions
(`embarch-outpost decision 9` at lines 189 and 203) but repeated bare four
lines later in the next bullet (`decision 9` at line 210, ~55 characters past
the nearest label — past `check-decision-refs.py`'s 44-character attribution
window, though that script cannot see source comments at all) — same real
decision, same correct topic, just the label not carried across the paragraph
break. Fixed by adding the label back rather than by touching the number.
Check every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right, and is not proof it is wrong either.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s, `048`'s, `049`'s and `050`'s findings all
resolved without it. When no paired table or direct textual match exists, run
`git log --follow -p -- embarch-study-designer/decisions/<file>.md` and read
how the cited paragraph's wording evolved.

**A wrong number is not always a nearby-digit typo, and not every
over-attribution is a "wrong number," and not every wrong attribution is
cross-repo.** Check every citation against what the decision's own text
*establishes*, not just whether the general topic area is adjacent, and don't
assume the nearest plausible decision *number* is the error when the error is
which *rule* the sentence is describing. Two decisions credited jointly for
one failure mode (`050`'s `decisions 34 and 36` — both genuinely opened by a
"silently produces an empty capture" scenario, confirmed by reading both
texts) is not automatically a defect either; read both before assuming one is
extra.

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations. Zero wrong numbers,
  zero false sentences, one unlabelled cross-repo citation (fixed).
- `src/study.rs` — done in `045`. 52 citations. **3 wrong numbers, 0 false
  sentences, 1 unlabelled cross-repo citation — all fixed.**
- `src/gatt_extract.rs` — done in `046`. 36 citations. **3 wrong numbers, 2
  false sentences, 0 unlabelled cross-repo citations — all fixed.**
- `src/lib.rs` — done in `047`. 41 citations. **2 wrong numbers, 0 false
  sentences, 0 unlabelled cross-repo citations — both fixed.**
- `src/study_builder.rs` — done in `048`. 38 citations (36 distinct citation
  instances; two split across a line wrap). **3 wrong numbers, 0 false
  sentences, 0 unlabelled cross-repo citations (both cross-repo cites were
  already correctly labelled) — all three fixed.**
- `src/protocol.rs` — done in `049`. 32 grep-matching lines, ~38 distinct
  citation instances. **1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed.**
- `src/streams.rs` — done in `050`. 29 grep-matching lines, 31 distinct
  citation instances, read against `decisions/streams.md` (11, 20, 21, 27,
  39), `decisions/registry.md` (35), `decisions/authoring.md` (34, 38),
  `decisions/gatt.md` (36), `decisions/seals.md` (18, 26), `decisions/
  versioning.md` (30), `decisions/payload-meaning.md` (52), plus
  `embarch-topology` decisions 3 and 18, `embarch-outpost` decisions 9, 10,
  11 and 12, and `embarch-core` decision 30 (all cross-repo cites on-topic
  and correctly labelled except one). **0 wrong numbers, 0 false sentences,
  1 unlabelled cross-repo citation (a repeated `embarch-outpost decision 9`
  cite four lines past its own label, in the next bullet) — fixed.**

## Done when

- [x] One named file (`src/limits.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately.
      **Took a second, `src/result.rs`, with budget still left, per the
      dispatch note.** `limits.rs`: 28 grep-matching lines, 32 distinct
      citation instances, 1 wrong number + 1 false sentence (both in
      `MAX_SOURCES_PER_PROTOCOL`'s comment — wrong decision cited and the
      "three (`ctrl`/`status`/`data`)" claim itself false per
      `interfaces/eap.md`), 0 unlabelled cross-repo citations. `result.rs`:
      24 grep-matching lines, 25 distinct citation instances, 1 wrong number
      (`security_level`'s `decision 50` should be `decision 44`), 0 false
      sentences, 0 unlabelled cross-repo citations. Totals: 57 citation
      instances checked, 2 wrong numbers, 1 false sentence, 0 unlabelled
      cross-repo citations — all fixed.
- [x] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text is read before it is called wrong.
      Confirmed for both files: `embarch-dev-bench` (7, 18, 27),
      `embarch-core` (35, 31), `embarch-topology` (18), `embarch-outpost` (9),
      `embarch-api` (40) and `embarch-ui` (11, 15) citations were all
      correctly labelled and read on-topic against the far-repo decision's
      own text.
- [x] A follow-up task filed naming the files that remain:
      `tasks/study-designer/052-src-citation-sweep-remainder.md` (16 files,
      `src/bounded.rs` next).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/study-designer-*` fragment.

## Dispatch note (leg 121, 2026-09-16)

**Reserve, re-checked by me at dispatch:** unchanged from what `050` recorded —
`embarch-study-designer/spec.md` **9,350/10,240 B (890 B left)** and `open.md`
**4,659/5,120 B (461 B left)**, filed under `tasks/study-designer/032` and `026`,
both blocked. Nothing else in the scope is in reserve. A source-comment sweep
should need neither file.

**Take `src/limits.rs`** — largest remaining, and the task's own stated next. If
you finish it with real budget left, take `src/result.rs` too and say you took
two; do not start a third.

**The zero-defect question is live and your report feeds it.** The 2026-09-12
handoff flagged that three-plus consecutive clean sweeps may mean refill has
converged on always-clean files rather than that the corpus is clean, and nothing
tracks the hit rate. So report **citation instances checked**, not just
grep-matching lines, and report wrong numbers and false sentences as two separate
counts even when both are zero. That is the only number anyone can later use.

**Do not fix anything outside `src/`** — file it as `tasks/study-designer/<NNN>`
in your own commit instead.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047` through `050` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file. Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
