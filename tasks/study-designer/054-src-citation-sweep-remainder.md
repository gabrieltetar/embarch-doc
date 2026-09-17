# 054 — Citation sweep: `src/` remainder after `eap.rs`

**State:** claimed by agent/study-designer/054-src-citation-sweep-remainder, 2026-09-16 19:25
**Source:** `tasks/study-designer/053`, which fixed `.cargo/config.toml`'s
stale test-count comment and swept `src/eap.rs` (the largest of the 14 files
`052` left remaining), and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `053`,
2026-09-16, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Eleven of the four originally-named plus the seven largest-remaining files
are now swept:

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
22  src/bounded.rs        — swept in 052
21  src/eap.rs            — swept in 053
```

**13 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — a *line*
count, not a citation-instance count, re-measured fresh for this dispatch):

```
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

Take one file — `src/ffi.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**Grep-line-count does not predict citation-instance count, and does not
predict cost, and does not predict yield.** `053` took one file (`eap.rs`, 21
grep-matching lines, 21 distinct citation instances — a range citation
(`decisions 58-62`) expanding to 5 instances offsetting four lines that used
the bare word "decision" with no number) and found **one wrong number**: the
module doc's `//! The expression set is three operand forms...` — `Operand`
has always had four variants (`Literal`, `Field`, `Session`, `SpanLen`,
all added in the same commit that created the file) — wrong the day it
landed, never a drift. Zero false sentences: every one of the ten unique
decision numbers cited (3, 18, 35, 39, 52, 58, 59, 60, 61, 62), all
same-crate, checked against `decisions/wire.md`, `decisions/seals.md`,
`decisions/registry.md`, `decisions/streams.md`, `decisions/payload-meaning.md`
and `decisions/protocols.md`/`decisions/protocol-exec.md`, held up including
the embedded numeric claims (`ScalarType`'s 18 variants, confirmed against
`src/decoder.rs` and `interfaces/decoders.md`).

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`053`, confirmed useful all eleven times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and ten of
the eleven sweeps in this one, has been prose a decision made false or a
citation pointing at the wrong (but real) decision, or a plain wrong count
elsewhere in the same sentence, not a bare typo in the citation number itself.
`052` is the only true zero so far; `053` found a wrong number that had
nothing to do with which decision was cited — the citation itself resolved
correctly, but a number in the sentence it was attached to was wrong. **Check
every number in the cited sentence, not just the decision number.** Count the
two categories separately and report both, honestly, even if one or both is
zero — "checked N, found none" is a legitimate result.

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
`046`, `047`, `049`, `051`, `052` and `053` found none (`052`'s and `053`'s
files had no cross-repo citations of any kind, labelled or not — every
instance in both was same-crate). `048` found the *opposite* shape: a
same-repo decision mislabelled *as* foreign. `050` found a **third** shape: a
cross-repo decision correctly labelled on its first two mentions but repeated
bare four lines later, past `check-decision-refs.py`'s attribution window.
Check every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right, and is not proof it is wrong either.

**A wrong number is not always a nearby-digit typo, and is not always the
decision number itself.** `051`'s two finds were both a real, existing, but
topically wrong decision — not a transposed digit — found only by reading the
cited decision's actual text against the claim, never by the number alone
looking suspicious. `053`'s one find was the opposite shape again: the cited
decision (60) was exactly right, but an unrelated count in the same sentence
(`Operand`'s variant count) was wrong and always had been — found only by
counting the actual enum variants in the same file, not by reading the
decision at all. Reading the crate's own `interfaces/*.md` and its own type
definitions mattered as much as reading `decisions/*.md`.

**Git history of the decisions file (and, per `053`, of the source file
itself) is worth checking when a citation's credit — or a plain count near
one — looks off**, though `047`'s through `053`'s findings all resolved
without needing the decisions-file history; `053`'s one find *did* need
`git log -S` on the source file, to confirm the wrong count was original to
the file's first commit rather than a later drift. When no paired table or
direct textual match exists, run `git log --follow -p -- embarch-study-designer/decisions/
<file>.md` (or, for a count claim about the crate's own code, `git log -p -S"<the actual definition>" -- src/<file>.rs`)
and read how the cited paragraph, or the type it describes, evolved.

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
  citation instances. 1 wrong number, 1 false sentence, 0 unlabelled
  cross-repo citations — both fixed (`MAX_SOURCES_PER_PROTOCOL`'s
  `decision 57` cite and its "three (`ctrl`/`status`/`data`)" claim; corrected
  to two, `ctrl`/`status`, per `interfaces/eap.md`).
- `src/result.rs` — done in `051`. 24 grep-matching lines, 25 distinct
  citation instances. 1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed (`security_level`'s `decision 50` cite,
  should be `decision 44`).
- `src/bounded.rs` — done in `052`. 22 grep-matching lines, 25 distinct
  citation instances. 0 wrong numbers, 0 false sentences, 0 unlabelled
  cross-repo citations — every citation (decisions 15, 46, 49, 54, 63)
  checked against `decisions/limits.md` and `decisions/removed.md` and found
  accurate, including all embedded numeric claims.
- `src/eap.rs` — done in `053`. 21 grep-matching lines, 21 distinct citation
  instances (one range citation, `decisions 58-62`, expanding to 5). 1 wrong
  number, 0 false sentences, 0 unlabelled cross-repo citations — fixed (the
  module doc's "three operand forms" should be "four": `Operand` has always
  had `Literal`/`Field`/`Session`/`SpanLen`, wrong since the file's first
  commit).

## Running tally across the chain (`044`–`053`, ten files reporting per-file
counts plus `045`'s discrepancy note on grep-vs-instance)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported; no distinct-instance recount published), `study.rs` 52
(ditto), `gatt_extract.rs` 36 (ditto), `lib.rs` 41 (ditto),
`study_builder.rs` 36, `protocol.rs` ~38, `streams.rs` 31, `limits.rs` 32,
`result.rs` 25, `bounded.rs` 25, `eap.rs` 21. **Total: 390.** Wrong numbers
found: 0+3+3+2+3+1+0+1+1+0+1 = **15**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0 = **3**. Recompute this fresh in your report using the
actual per-file numbers above plus whatever this unit adds, since some early
files (`044`-`047`) never published a distinct-instance count separate from
the grep-line count, only the grep count.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests; `eap_worked_protocols.rs`
and the doctest binary both currently declare zero tests) — real growth in
the fourteen days between, not a re-measurement error, and *not* evidence
decision 63 was ever wrong (it is dated, and stands as the historical record
of what a specific commit pair measured). The comment now carries **two**
dated measurements side by side. If this keeps drifting, a future sweep
should decide whether the comment should track "as of last sweep" indefinitely
or drop the running-count framing entirely in favor of just decision 63's
citation — not this task's call to make unprompted, noted here so it is not
lost.

## Done when

- [ ] One named file (`src/ffi.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately, and
      every plain number in a cited sentence checked, not only the decision
      number.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text is read before it is called wrong.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047` through `053` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file. Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
