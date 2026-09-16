# 050 — Citation sweep: `src/` remainder after `protocol.rs`

**State:** open
**Source:** `tasks/study-designer/049`, which swept `src/protocol.rs` (the
largest of the 20 files `049` found remaining after `048`) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (leg 116, 2026-09-16, re-checked fresh
by `049`): two files, both already filed against, unchanged.**
`embarch-study-designer/spec.md` 9,350/10,240 B (890 B left) and
`embarch-study-designer/open.md` 4,659/5,120 B (461 B left) — filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This unit
is a source-comment sweep and should not need to write either file; **if it
turns out you must**, spend the bytes and say so in your report, and if you
leave either file deeper in reserve than you found it, file
`tasks/study-designer/051-compact-study-designer.md` in the same commit per
`tasks/README.md`. Do not compact `spec.md` or `open.md` as part of this
unit — both have a live park and an owner.

## What

Six of the four originally-named plus the two largest-remaining files are now
swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
41  src/lib.rs            — swept in 047 (recount; 044 estimated 34)
38  src/study_builder.rs  — swept in 048
32  src/protocol.rs       — swept in 049
```

**19 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — this is
a *line* count, not a citation-instance count; a line with two citations
counts once, and `049` found the two do not track each other exactly):

```
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

Take one file — `src/streams.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**None of the six swept files' full-file line count predicted its cost, and
grep-line-count does not predict citation-instance count either.**
`protocol.rs` (32 grep-matching lines, a 221-line file) actually carried ~38
individual citation instances once multi-number lines (`decisions 10, 12,
20`; `decision 47, embarch-core decision 35`) and one citation repeated
across a line wrap were counted separately, and fit in one leg with room to
spare because most of the eleven decision files it touched were short and
the one real defect resolved by a direct textual match rather than git
history. Do not assume a small grep count is cheap, and check whether a
sibling repo or this crate's own other decision files already answer the
question before reaching for `git log`.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`049`, confirmed useful all six times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all six
sweeps in this one, has been prose a decision made false or a citation
pointing at the wrong (but real) decision, not a bare typo. Count the two
categories separately and report both, honestly, even if one or both is zero —
"checked N, found none" is a legitimate result.

**A cross-repo citation that resolves to a real, on-topic decision is not
automatically suspect just because it feels surprising.** `049` initially
flagged `embarch-dev-bench decision 39` on `dev_bench_log_level` as a likely
same-repo-mislabelled-as-foreign case (the shape `048` found once already,
this crate's own `decision 26` mislabelled `embarch-api decision 26`) —
because this crate's *own* `decision 39` is the unrelated streams/tap
retirement. It was not that shape: `embarch-dev-bench` genuinely has its own,
different `decision 39` ("A study says how loud the bench should be, filtered
at runtime rather than compiled in", `decisions/logging.md`), and it is
exactly on topic. Read the far-repo decision's own text before concluding a
cross-repo cite is wrong — a coincidence in numbering is not evidence.

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one bare cross-repo
citation missing its label, `045` found a second, structurally identical one.
`046`, `047` and `049` found none. `048` found the *opposite* shape: a
same-repo decision (`decision 26`, this crate's own) mislabelled *as*
`embarch-api decision 26`, a real but unrelated decision in that repo. Check
every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right, and (per `049`, above) is not proof it is wrong either.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s, `048`'s and `049`'s findings all resolved
without it — `049`'s one date claim (`decision 39's 2026-08-25 amendment`) was
confirmed instead by `git log -S'streams_crc'` against `decisions.md`/
`decisions/streams.md`, which is a related but distinct check from crediting a
paragraph to the wrong decision number. `048`'s three defects all resolved by
reading the cited decision's own current text directly. When no paired table
or direct textual match exists, run `git log --follow -p -- embarch-study-designer/decisions/<file>.md`
and read how the cited paragraph's wording evolved.

**A wrong number is not always a nearby-digit typo, and not every
over-attribution is a "wrong number," and not every wrong attribution is
cross-repo.** `045` found three wrong numbers, `046` found three more of an
"established vs. credited" shape, `047` found two more of the same shape but
in the opposite direction, `048` found three (one reachable via a sibling
repo's prior finding, one a same-repo decision mislabelled as foreign, one
topically-adjacent-but-wrong), and `049` found one same-repo defect with no
cross-repo component at all: a structural rule ("each seal immediately
follows the one contiguous span it covers") attributed to `decision 39's
amendment set` when both `decisions/seals.md`'s own decision 17 entry and
`decisions/protocols.md`'s decision 58 amendment paragraph state the identical
rule and credit it to decision 17 — decision 39 (the streams/tap model) has no
seal-ordering content at all. Check every citation against what the decision's
own text *establishes*, not just whether the general topic area is adjacent,
and don't assume the nearest plausible decision *number* is the error when the
error is which *rule* the sentence is describing.

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
  citation instances, read against `decisions/wire.md` (2, 10, 24, 25),
  `decisions/versioning.md` (12, 30, 47, 72), `decisions/seals.md` (17, 18,
  26), `decisions/study.md` (14, 16, 51), `decisions/streams.md` (11, 20, 39),
  `decisions/gatt.md` (36, 41), `decisions/declares.md` (40, 74),
  `decisions/payload-meaning.md` (52), `decisions/protocols.md` (58, 59),
  `decisions/protocol-exec.md` (60, 62), `decisions/crate.md` (2), plus
  `embarch-dev-bench` decisions 7, 18 and 39 and `embarch-core` decision 35
  (all four cross-repo cites already correctly labelled and, on inspection,
  correctly on-topic — see the method note above). **1 wrong number (a
  seal-ordering structural rule credited to `decision 39's amendment set`
  when it is decision 17's — decision 39 has no seal-ordering content), 0
  false sentences, 0 unlabelled cross-repo citations — fixed.**

## Done when

- [ ] One named file (`src/streams.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text is read before it is called wrong.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047`, `048` and `049` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file (`049`: unchanged from `048`'s
91.3%/91.0%, both parked and blocked). Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
