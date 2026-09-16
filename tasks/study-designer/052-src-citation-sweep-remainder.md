# 052 — Citation sweep: `src/` remainder after `limits.rs` and `result.rs`

**State:** claimed — leg 122, `agent/study-designer/052-src-citation-sweep-remainder`, 2026-09-16.
**Source:** `tasks/study-designer/051`, which swept `src/limits.rs` and
`src/result.rs` (the two largest of the 18 files `050` found remaining after
`049`) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `051`,
2026-09-16, via `scripts/check-doc-size.py`): unchanged.**
`embarch-study-designer/spec.md` and `open.md` remain in the last 10% of
their caps, filed as `tasks/study-designer/032` and `026` respectively, both
**blocked**. This unit is a source-comment sweep and should not need to write
either file; if it turns out you must, spend the bytes and say so in your
report.

## What

Nine of the four originally-named plus the five largest-remaining files are
now swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
41  src/lib.rs            — swept in 047 (recount; 044 estimated 34)
38  src/study_builder.rs  — swept in 048
32  src/protocol.rs       — swept in 049
29  src/streams.rs        — swept in 050
28  src/limits.rs         — swept in 051
24  src/result.rs         — swept in 051
```

**16 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — a *line*
count, not a citation-instance count):

```
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

Take one file — `src/bounded.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**Grep-line-count does not predict citation-instance count, and does not
predict cost.** `051` took two files (`limits.rs`, 28 grep-matching lines, 32
distinct citation instances; `result.rs`, 24 grep-matching lines, 25 distinct
citation instances — 57 total) in one leg with room to spare, and found two
defects, one per file: `limits.rs`'s `MAX_SOURCES_PER_PROTOCOL` comment cited
`decision 57` (an unrelated GATT-extraction-scope decision) for a claim that
was itself false — "the real BDS download's three (`ctrl`/`status`/`data`)"
— when the crate's own `interfaces/eap.md` says the real manifest
**deliberately does not** name the bulk data characteristic as a source, so
it is two (`ctrl`/`status`), not three; and `result.rs`'s `security_level`
field doc cited `decision 50` (`Action::BleUnbond`, an unrelated action) when
the field it documents — "populated for every step, not only for a security
step" — is decision 44's own implementation note verbatim
(`decisions/ble.md`). Both fixed by correcting the number/reference rather
than the surrounding prose, which was otherwise accurate. Neither file had an
unlabelled cross-repo citation; both files' several cross-repo cites
(`embarch-dev-bench`, `embarch-core`, `embarch-topology`, `embarch-outpost`,
`embarch-api`, `embarch-ui`) were all correctly labelled and on-topic.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`051`, confirmed useful all nine times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all nine
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
`046`, `047`, `049` and `051` found none. `048` found the *opposite* shape: a
same-repo decision mislabelled *as* foreign. `050` found a **third** shape: a
cross-repo decision correctly labelled on its first two mentions but repeated
bare four lines later, past `check-decision-refs.py`'s attribution window.
Check every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right, and is not proof it is wrong either.

**A wrong number is not always a nearby-digit typo.** `051`'s two finds were
both a real, existing, but topically wrong decision — not a transposed digit
— found only by reading the cited decision's actual text against the claim,
never by the number alone looking suspicious. **Reading the crate's own
`interfaces/*.md` mattered as much as reading `decisions/*.md` this time**:
`limits.rs`'s defect was only visible by comparing the comment against
`interfaces/eap.md`'s own worked-protocol finding, which directly
contradicted it — a case where the decision cited was simply the wrong one
to check against at all, and the correct source is a "current truth"
interface doc rather than a decision file.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s, `048`'s, `049`'s, `050`'s and `051`'s
findings all resolved without it. When no paired table or direct textual
match exists, run `git log --follow -p -- embarch-study-designer/decisions/
<file>.md` and read how the cited paragraph's wording evolved.

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations. Zero wrong numbers,
  zero false sentences, one unlabelled cross-repo citation (fixed).
- `src/study.rs` — done in `045`. 52 citations. 3 wrong numbers, 0 false
  sentences, 1 unlabelled cross-repo citation — all fixed.
- `src/gatt_extract.rs` — done in `046`. 36 citations. 3 wrong numbers, 2
  false sentences, 0 unlabelled cross-repo citations — all fixed.
- `src/lib.rs` — done in `047`. 41 citations. 2 wrong numbers, 0 false
  sentences, 0 unlabelled cross-repo citations — both fixed.
- `src/study_builder.rs` — done in `048`. 38 citations (36 distinct citation
  instances). 3 wrong numbers, 0 false sentences, 0 unlabelled cross-repo
  citations — all three fixed.
- `src/protocol.rs` — done in `049`. 32 grep-matching lines, ~38 distinct
  citation instances. 1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed.
- `src/streams.rs` — done in `050`. 29 grep-matching lines, 31 distinct
  citation instances. 0 wrong numbers, 0 false sentences, 1 unlabelled
  cross-repo citation — fixed.
- `src/limits.rs` — done in `051`. 28 grep-matching lines, 32 distinct
  citation instances. **1 wrong number, 1 false sentence, 0 unlabelled
  cross-repo citations — both fixed** (`MAX_SOURCES_PER_PROTOCOL`'s
  `decision 57` cite and its "three (`ctrl`/`status`/`data`)" claim; corrected
  to two, `ctrl`/`status`, per `interfaces/eap.md`).
- `src/result.rs` — done in `051`. 24 grep-matching lines, 25 distinct
  citation instances. **1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed** (`security_level`'s `decision 50` cite,
  should be `decision 44`).

## Done when

- [ ] One named file (`src/bounded.rs`, unless a reason is given to reorder)
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
blocked, `In flux: yes` per `046`'s dispatch note; `047` through `051` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file. Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
