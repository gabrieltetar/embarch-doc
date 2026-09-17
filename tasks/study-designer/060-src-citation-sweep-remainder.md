# 060 — Citation sweep: `src/` remainder after `outpost.rs`

**State:** open
**Source:** `tasks/study-designer/059`, which swept `src/outpost.rs` (8
grep-matching lines, 8 distinct citation instances) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `059`,
2026-09-16, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Seventeen files are now swept (the four originally-named plus thirteen more):

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
14  src/crc.rs            — swept in 055
12  src/eap_parse.rs      — swept in 056 (recount; 056's own header table
                            estimated 13)
11  src/gatt.rs           — swept in 057
 9  src/registry.rs       — swept in 058
 8  src/outpost.rs        — swept in 059
```

**7 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs`
— a *line* count, not a citation-instance count):

```
 7  src/decoder.rs
 7  src/sample.rs
 6  src/merged_actions.rs
 5  src/gatt_names.rs
 5  src/eap_interp.rs
 3  src/vendor.rs
 2  src/records.rs
 0  src/ids.rs — no citations; needs no sweep, listed so the count above is exhaustive
```

Take one file — `src/decoder.rs` or `src/sample.rs` next (tied at 7 lines;
either is a reasonable start), unless a reason is given to reorder — read
every cited decision's body against the sentence around the citation, and fix
what is wrong. Count wrong *numbers* and false *sentences* separately, per
the method below. When you run out of budget, file the next
`tasks/study-designer/<next>` naming exactly which files remain, the same way
this one does.

**`059`'s find, carried forward: a citation can be correctly labelled
cross-repo and still name the wrong decision, where the *general subject* is
close enough to sound right.** `src/outpost.rs` line 9 cited "embarch-core
decision 30" for "Core holds no column knowledge" — decision 30
(`embarch-core/decisions/streams.md`) is real, on-topic (it is about stream
tap capture) and correctly labelled cross-repo, but it never discusses column
knowledge anywhere in its text; it is about a second serial port, manifest
binding by build ID, and being the trace's clock. Decision 38, three
paragraphs later in the same file, is the one that actually says "Core
renders a `Struct`-encoded tap and holds no more column knowledge than
before" and "Core still knows no field name, width, or byte order." Fixed by
repointing to 38. **This is a fourth distinct shape of wrong citation**,
alongside `056`'s (right decision, drifted true-at-the-time claim), `055`'s
(right decision, wrong module/status claim) and `058`'s (real decision, never
said the thing at all, same repo) — here the two decisions are neighbours in
the same file, on the same broad topic (what Core stores/knows about a
stream), and only one of them makes the specific claim being cited. Worth
checking for on every file: when a cross-repo citation's *topic* is right but
the *specific claim* isn't verbatim or close to verbatim in that decision's
own text, check the neighbouring decisions in the same source file before
concluding the citation is correct.

**`058`'s find, still carried forward: a citation number can be to a real,
existing decision and still be flatly wrong — not stale, not superseded,
just never having said what the comment claims it said.** See
`tasks/study-designer/059`'s copy of this paragraph (the `registry.rs`
`StreamCapture`/decision 35→39 account) for the full history.

**`056`'s find, still carried forward: a wrong number that was real,
on-topic, cross-repo, and correctly labelled — and still wrong, because a
nearer same-repo decision said the identical thing two lines above.** See
`tasks/study-designer/057`'s predecessor text for the full account
(`embarch-core` decision 30's "settlement 2" vs. same-repo decision 59, in
`eap_parse.rs`). **`057`, `058` and `059` all found zero candidates for this
shape** — `gatt.rs`, `registry.rs` and `outpost.rs` all had either no
cross-repo citations or none with a same-repo duplicate, so three files
running in the true-zero column for this specific check.

**`055`'s find (carried forward, still the standing reminder): a false
sentence can misattribute *where* a cited feature runs, not just *which*
decision covers it.** See `tasks/study-designer/056`'s copy of this
paragraph for the full `crc32_ieee` account.

## Method (carried over from `044`-`059`, confirmed useful all seventeen
times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero. **A zero is a real, reportable result, not a null
one** — two of seventeen files so far (`bounded.rs`, `gatt.rs`) checked out
completely clean; `outpost.rs` had exactly one problem, a wrong-number
cross-repo citation with no false sentence of the other kind (8 citations, 1
wrong number, 0 false sentences).

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. Check every bare *and* every labelled `decision N`
against *this crate's own* decisions.md/decisions/*.md first regardless, and
**for every cross-repo citation found, also ask whether a same-repo decision
already says the same thing** (`056`'s shape) — a file can have none of
these to check, as `gatt.rs`, `registry.rs` and `outpost.rs` all did. **Also
ask, per `059`'s find, whether a *different* decision in the same cited
file/repo is the one that actually backs the specific claim** — a decision
being on-topic and correctly labelled is not the same as it being the right
number.

**Run the continuation-grep too, every file, not just the target.**
`grep -rlIE '[Dd]ecisions[[:space:]]*$'` over the whole repo catches a
citation wrapped across a comment continuation, which a line-based
`grep -cE` census misses entirely (found first by `embarch-core/068`). As of
`059` it still hits the same **four files**: `Cargo.toml`, `src/lib.rs`
(twice), `src/eap.rs`, and `src/schema_version.rs` — all four
already-swept or out of this chain's file list, and all four checked
correct again. Re-run this full-repo grep fresh each time rather than
trusting a prior unit's file list as closed; report whatever it finds, even
if it lands outside the file being swept and even if it repeats a hit a
prior unit already named.

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
  cross-repo citations — both fixed.
- `src/result.rs` — done in `051`. 24 grep-matching lines, 25 distinct
  citation instances. 1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed.
- `src/bounded.rs` — done in `052`. 22 grep-matching lines, 25 distinct
  citation instances. 0 wrong numbers, 0 false sentences, 0 unlabelled
  cross-repo citations.
- `src/eap.rs` — done in `053`. 21 grep-matching lines, 21 distinct citation
  instances (one range citation, `decisions 58-62`, expanding to 5). 1 wrong
  number, 0 false sentences, 0 unlabelled cross-repo citations — fixed.
- `src/ffi.rs` — done in `054`. 15 grep-matching lines, 16 distinct citation
  instances. 0 wrong numbers, 1 false sentence, 2 unlabelled cross-repo
  citations — all fixed.
- `src/crc.rs` — done in `055`. 14 grep-matching lines, 14 distinct citation
  instances. 0 wrong numbers, 1 false sentence, 0 unlabelled cross-repo
  citations — fixed (`crc32_ieee`'s doc misattributed both which module
  applies the in-frame `crc32` primitive and whether it runs at all;
  repointed to decision 71 and `crate::records`' `RecordCheck`, decision 70).
- `src/eap_parse.rs` — done in `056`. 12 grep-matching lines, 13 distinct
  citation instances. 1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed (a cross-repo citation to `embarch-core`
  decision 30's "settlement 2", real but no longer a citable unit anywhere,
  repointed to same-repo decision 59, which states the identical reasoning).
- `src/gatt.rs` — done in `057`. 11 grep-matching lines, **13** distinct
  citation instances (`057` reported 14; corrected at its fold). 0 wrong
  numbers, 0 false sentences, 0 unlabelled cross-repo citations — the second
  true zero in the chain; no cross-repo citations of any kind in this file.
- `src/registry.rs` — done in `058`. 9 grep-matching lines, 9 distinct
  citation instances (every matching line carries exactly one number). 0
  wrong numbers, 1 false sentence, 0 unlabelled cross-repo citations —
  fixed (`RegisteredOperation`'s doc comment attributed the exclusion of
  `GattOperation::StreamCapture` to "decision 35's own 'doesn't need it
  here' call"; decision 35 says nothing of the kind anywhere in its history,
  in this file or any other decision file — repointed to decision 39, which
  actually says `StreamCapture` was folded into the tap model as
  `StreamSource::GattNotify`).
- `src/outpost.rs` — done in `059`. 8 grep-matching lines, 8 distinct
  citation instances (every matching line carries exactly one number). 1
  wrong number, 0 false sentences, 0 unlabelled cross-repo citations —
  fixed (the module doc's "Why this lives here and not in `embarch-core`"
  paragraph attributed "Core holds no column knowledge" to "embarch-core
  decision 30"; decision 30 is real, on-topic and correctly labelled but
  never discusses column knowledge — repointed to decision 38, three
  paragraphs later in the same `embarch-core/decisions/streams.md`, which
  states the identical claim almost verbatim).

## Running tally across the chain (`044`–`059`, seventeen files reporting
per-file counts)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14, `eap_parse.rs` 13, `gatt.rs` 13, `registry.rs` 9, `outpost.rs` 8.
**Total: 463.** Wrong numbers found:
0+3+3+2+3+1+0+1+1+0+1+0+0+1+0+0+1 = **17**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1+1+0+0+1+0 = **6**. Recompute this fresh in your
report using the actual per-file numbers above plus whatever this unit adds.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` through `059`
all re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [ ] One named file (`src/decoder.rs` or `src/sample.rs`, unless a reason is
      given to reorder) fully swept, wrong numbers and false sentences
      counted separately, and every plain number and implementation-status
      claim in a cited sentence checked, not only the decision number.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted. Remember `056`'s find:
      correctly labelled and still wrong is possible; `058`'s find: a
      citation can be to a real decision that never said the thing at all;
      and `059`'s find: an on-topic, correctly-labelled cross-repo citation
      can still be the wrong neighbouring decision in the same source file —
      read the whole cited decision, not just its header, and check nearby
      decisions in the same file before trusting a plausible-sounding topic
      match.
- [ ] The whole-repo continuation-grep
      (`grep -rlIE '[Dd]ecisions[[:space:]]*$'`) run fresh (do not assume
      `059`'s four-file list is exhaustive) and any hit reported, even one
      landing outside the file being swept.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`,
`026`) blocked, `In flux: yes`. `047` through `059` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
