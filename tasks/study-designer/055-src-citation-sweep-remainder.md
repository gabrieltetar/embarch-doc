# 055 — Citation sweep: `src/` remainder after `ffi.rs`

**State:** done
2026-09-16. `src/crc.rs` swept: 14 grep-matching lines, 14
distinct citation instances (no plural-citation lines), 0 wrong numbers, 1
false sentence fixed, 0 unlabelled cross-repo citations (the file cites only
this crate's own decisions). Follow-up filed as `056`, naming `eap_parse.rs`
next.
**Source:** `tasks/study-designer/054`, which fixed two unlabelled cross-repo
citations and one false sentence in `src/ffi.rs` (the largest of the 13 files
`053` left remaining), and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `054`,
2026-09-16, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Twelve of the four originally-named plus the eight largest-remaining files
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
15  src/ffi.rs            — swept in 054
```

**12 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — a *line*
count, not a citation-instance count, re-measured fresh for this dispatch):

```
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

Take one file — `src/crc.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**Grep-line-count does not predict citation-instance count, and does not
predict cost, and does not predict yield.** `054` took one file (`ffi.rs`, 15
grep-matching lines, 16 distinct citation instances — line 1's `decisions 7,
23` expands to two instances on one line) and found **zero wrong numbers** but
**one false sentence**: the `essd_study_decode_and_verify` doc comment cited
`embarch-topology decision 18's amendment` as sharing this crate's "no caller
anywhere" posture — but that decision's own 2026-09-11 amendment (`tasks/suite/014`)
had already retracted exactly that mutual citation as circular and said
plainly that this crate's surface "gets no such defence." The comment was true
when written and became false the day the far-repo decision was amended out
from under it, and nothing in this repo would ever have caught that — the
sentence resolved to a real, on-topic decision the whole time.
`054` also found **two unlabelled cross-repo citations**, both bare `decision
21` (lines that would have been same-repo by convention) referring to
`embarch-dev-bench decision 21` — correctly labelled on its first mention in
the same file, then repeated bare twice more, the same "third shape" `050`
found in `streams.rs`. This crate's *own* decision 21 (`decisions/streams.md`)
is `GattOperation::StreamCapture`, an unrelated superseded streaming
mechanism — reading it, not just noticing a repo prefix was missing, is what
confirmed the bare citations meant the far-repo one and not this crate's own.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`054`, confirmed useful all twelve times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and eleven of
the twelve sweeps in this one, has been prose a decision made false or a
citation pointing at the wrong (but real) decision, or a plain wrong count
elsewhere in the same sentence, not a bare typo in the citation number itself.
`052` is the only true zero so far. `054`'s false sentence adds a new shape to
the pile: a cited decision that was correct when the comment was written and
was made false later by an *amendment to the far-repo decision itself*, not by
anything in this crate — worth remembering because nothing in `check-decision-refs.py`
or this crate's own history would surface it; only reading the cited decision's
current text does. **Check every number in the cited sentence, not just the
decision number.** Count the two categories separately and report both,
honestly, even if one or both is zero — "checked N, found none" is a
legitimate result.

**A cross-repo citation that resolves to a real, on-topic decision is not
automatically suspect just because it feels surprising.** Read the far-repo
decision's own text before concluding a cross-repo cite is wrong — a
coincidence in numbering is not evidence either way (`049`'s
`embarch-dev-bench decision 39` case, confirmed correct). **Reading it is also
what catches the opposite failure** — `054`'s false sentence looked
unremarkable (a real, named, on-topic-sounding far-repo decision) until the
far-repo file was actually opened and its amendment block read.

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
`054` found that same third shape again, in a different file and a different
far repo — two more bare repeats of an already-labelled `embarch-dev-bench
decision 21`. Check every bare *and* every labelled `decision N` against *this
crate's own* decisions.md/decisions/*.md first regardless — a repo prefix is
not proof the label is right, and is not proof it is wrong either.

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
one — looks off**, though `047`'s through `054`'s findings all resolved
without needing the decisions-file history beyond reading the cited entry's
current (possibly amended) text; `053`'s one find *did* need `git log -S` on
the source file, to confirm the wrong count was original to the file's first
commit rather than a later drift. When no paired table or direct textual
match exists, run `git log --follow -p -- embarch-study-designer/decisions/
<file>.md` (or, for a count claim about the crate's own code, `git log -p -S"<the actual definition>" -- src/<file>.rs`)
and read how the cited paragraph, or the type it describes, evolved. **`054`'s
lesson applies to a cross-repo cite too:** if it resolves and reads on-topic,
still check whether the far-repo decision carries a later amendment block
that changes what it says — a resolved number is not evidence the *current*
text of that decision still supports the sentence citing it.

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
- `src/ffi.rs` — done in `054`. 15 grep-matching lines, 16 distinct citation
  instances (line 1's `decisions 7, 23` expanding to 2). 0 wrong numbers, 1
  false sentence, 2 unlabelled cross-repo citations — all fixed. The false
  sentence: `essd_study_decode_and_verify`'s doc cited `embarch-topology
  decision 18`'s amendment as sharing this crate's "no caller anywhere"
  justification for `streams_crc` staying unchecked at the FFI boundary — that
  amendment (2026-09-11, `tasks/suite/014`) had retracted exactly that mutual
  citation as circular and said this crate's surface "gets no such defence."
  Rewritten to cite decision 7's own 2026-09-11 correction (which already
  records the two decode functions as having no caller in any repo) and
  `tasks/suite/032` (the still-open call on retiring the surface) instead. The
  two unlabelled cites: both bare `decision 21`, which is `embarch-dev-bench
  decision 21` (`main.c` dispatches a real `Study`) correctly labelled on its
  first mention in the same file, then repeated bare twice more — this
  crate's own decision 21 (`decisions/streams.md`) is the unrelated,
  superseded `GattOperation::StreamCapture`.

## Running tally across the chain (`044`–`054`, twelve files reporting
per-file counts plus `045`'s discrepancy note on grep-vs-instance)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported; no distinct-instance recount published), `study.rs` 52
(ditto), `gatt_extract.rs` 36 (ditto), `lib.rs` 41 (ditto),
`study_builder.rs` 36, `protocol.rs` ~38, `streams.rs` 31, `limits.rs` 32,
`result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16. **Total: 406.**
Wrong numbers found: 0+3+3+2+3+1+0+1+1+0+1+0 = **15**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1 = **4**. Recompute this fresh in your report using the
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
of what a specific commit pair measured). `054` re-ran the full suite fresh
(`cargo test`) and got the same 125/125 (116 + 9), so the comment does not yet
need a third dated line. The comment now carries **two** dated measurements
side by side. If this keeps drifting, a future sweep should decide whether
the comment should track "as of last sweep" indefinitely or drop the
running-count framing entirely in favor of just decision 63's citation — not
this task's call to make unprompted, noted here so it is not lost.

## Done when

- [x] One named file (`src/crc.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately, and
      every plain number in a cited sentence checked, not only the decision
      number. Result: 14 checked, 0 wrong numbers, 1 false sentence
      (`crc32_ieee`'s doc wrongly claimed the in-frame `crc32` grammar
      primitive is "applied host-side at render time (`crate::eap_parse`)";
      decision 71 and `open.md` both record it as parsed-and-pinned with no
      render consumer — rewritten to cite decision 71 for the gap and
      `crate::records`'s `RecordCheck` (decision 70) as the function's real
      caller).
- [x] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted. Result: `crc.rs` has no
      cross-repo citations at all — every one of its 14 resolves to this
      crate's own `decisions/*.md`.
- [x] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep). Filed as
      `tasks/study-designer/056-src-citation-sweep-remainder.md`, naming
      `src/eap_parse.rs` next (11 files plus `ids.rs` remain).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build
      --all-targets`, `cargo test --all-targets` (125 passed: 116 lib + 9
      `firmware_test_vectors`), `cargo clippy --all-targets -- -D warnings`
      all clean in the code worktree; `python3 scripts/check-docs.py` clean
      in the doc worktree (see report).
- [x] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.
      `changelog.d/study-designer-crc-rs-sweep.fixed.md`: "study-designer/055:
      citation sweep of crc.rs, 14 checked, 0 wrong numbers, 1 false
      sentence; file 056".

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047` through `054` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file. Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
