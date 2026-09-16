# 049 — Citation sweep: `src/` remainder after `study_builder.rs`

**State:** claimed — `agent/study-designer/049-src-citation-sweep-remainder`, leg 116, 2026-09-16
**Source:** `tasks/study-designer/048`, which swept `src/study_builder.rs` (the
largest of the 21 files `048` found remaining after `047`) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (leg 116, 2026-09-16): two files, both already filed
against.** `embarch-study-designer/spec.md` 9,350/10,240 B (890 B left) and
`embarch-study-designer/open.md` 4,659/5,120 B (461 B left) — filed as `tasks/study-designer/032`
and `026` respectively, both **blocked**. This unit is a source-comment sweep and should not need to
write either file; **if it turns out you must**, spend the bytes and say so in your report, and if
you leave either file deeper in reserve than you found it, file
`tasks/study-designer/050-compact-study-designer.md` in the same commit per `tasks/README.md`. Do
not compact `spec.md` or `open.md` as part of this unit — both have a live park and an owner.

## What

Five of the four originally-named plus the largest-remaining files are now
swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
41  src/lib.rs            — swept in 047 (recount; 044 estimated 34)
38  src/study_builder.rs  — swept in 048
```

**20 files remain, ~263 `[Dd]ecision`-matching lines by the same grep
methodology** (`grep -cE '[Dd]ecision' src/<file>.rs`), largest first:

```
32  src/protocol.rs
29  src/streams.rs
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

Take one file — `src/protocol.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**None of the five swept files' full-file line count predicted its cost.**
`gatt_extract.rs` (36 lines) took a whole leg's budget; `lib.rs` (41 lines, a
1159-line file) fit in one leg with room to spare; `study_builder.rs` (38
lines, a 1776-line file across module docs, an enum, a builder function and a
large test module) fit in one leg too, but only because two of its three
defects were caught by cross-checking against a *sibling* repo's own citation
sweep of the very same field (`embarch-ui`'s `047`, `delay_before_ms` ->
decision 42) rather than needing independent derivation. Do not assume a small
number is cheap, and do not assume a large file is expensive — check the
sibling repos' sweeps of the same field/decision pair when one exists; they
sometimes hand you the answer directly.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`048`, confirmed useful all five times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all five
sweeps in this one, has been prose a decision made false or a citation
pointing at the wrong (but real) decision, not a bare typo. Count the two
categories separately and report both, honestly, even if one or both is zero —
"checked N, found none" is a legitimate result.

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one bare cross-repo
citation missing its label, `045` found a second, structurally identical one.
`046` and `047` found none. `048` found the *opposite* shape for the first
time: a same-repo decision (`decision 26`, this crate's own — `steps_crc`
filled in by whoever submits) mislabelled *as* `embarch-api decision 26`, a
real but unrelated decision in that repo (`serial_log`'s `serial_port` field).
Check every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s and `048`'s findings resolved without it.
`048`'s three defects all resolved by reading the cited decision's own current
text directly: `decision 40` for `delay_before_ms` should have been `decision
42` (confirmed independently by `embarch-ui/047`'s identical finding on the
same field); `embarch-api decision 26` should have been bare `decision 26`
(embarch-api's real decision 26 is unrelated); and a vendor-row "no schema
bump" claim credited to `decision 39` (the streams/tap pipeline, which *is* a
schema bump) belongs to `decision 41` (the vendor-identity table, whose own
text says "No schema bump" almost verbatim). When no paired table or direct
textual match exists, run `git log --follow -p -- embarch-study-designer/decisions/<file>.md`
and read how the cited paragraph's wording evolved.

**A wrong number is not always a nearby-digit typo, and not every
over-attribution is a "wrong number."** `045` found three wrong numbers, `046`
found three more of an "established vs. credited" shape, `047` found two more
of the same shape but in the opposite direction, and `048` found three: one a
plain wrong number reachable by checking a *sibling repo's* prior finding on
the same field, one a same-repo decision mislabelled as a foreign one, and one
a topically-adjacent-but-wrong decision (both concern "no wire/schema
change", one is true of it and one is not). Check every citation against what
the decision's own text *establishes*, not just whether the general topic area
is adjacent, and check whether a sibling repo has already swept the identical
shared field.

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
  instances; two split across a line wrap) read against `decisions/authoring.md`
  (34, 37, 73's own text), `decisions/registry.md` (35), `decisions/gatt.md`
  (36, 41, 53), `decisions/ble.md` (43, 44, 50), `decisions/declares.md` (40),
  `decisions/seals.md` (26), `decisions/streams.md` (39), `decisions/study.md`
  (42), `decisions/limits.md` (46), plus `embarch-ui` decisions 11 and 17
  (both already correctly labelled). **3 wrong numbers (a `TableRow.delay_before_ms`
  doc comment credited `decision 40` — firmware-version declarations — for
  what `decision 42` actually establishes, the "when" half of a step, while
  the file's own later section headers and test docs already correctly cited
  42 for the same field; a `steps_crc`/`streams_crc` overwrite-on-submit
  comment was labelled `embarch-api decision 26` when it is this crate's own
  `decision 26` — embarch-api's real decision 26 is `serial_log`'s
  `serial_port` field, unrelated — so the fix removed the repo prefix rather
  than changing the number; a vendor-row test doc's "no firmware change and no
  schema bump" claim was credited to `decision 39`, the streams/tap pipeline —
  which *introduced* a schema bump — rather than `decision 41`, the
  vendor-identity table, whose own text says "No schema bump" of exactly this
  case and names the exact test the comment sits on), 0 false sentences, 0
  unlabelled cross-repo citations (both cross-repo cites were already
  correctly labelled) — all three fixed.**

## Done when

- [ ] One named file (`src/protocol.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047` and `048` both
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file (`048`: still 91.3%/91.0%, both parked
and blocked, unchanged). Check fresh again rather than trusting this number —
a comment sweep should not need either file regardless. If this sweep turns up
a question worth recording, file it as `tasks/study-designer/<next>` rather
than adding to `open.md`.
