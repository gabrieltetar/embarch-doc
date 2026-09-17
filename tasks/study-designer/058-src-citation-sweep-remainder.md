# 058 — Citation sweep: `src/` remainder after `gatt.rs`

**State:** open
**Source:** `tasks/study-designer/057`, which swept `src/gatt.rs` (11
grep-matching lines, 14 distinct citation instances) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `057`,
2026-09-16, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Fifteen files are now swept (the four originally-named plus eleven more):

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
```

**9 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs`
— a *line* count, not a citation-instance count):

```
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

Take one file — `src/registry.rs` next, largest remaining, unless a reason
is given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget,
file the next `tasks/study-designer/<next>` naming exactly which files
remain, the same way this one does.

**`056`'s find, carried forward (the reason this chain checks same-repo
proximity, not just cross-repo labelling): a wrong number that was real,
on-topic, cross-repo, and correctly labelled — and still wrong, because a
nearer same-repo decision said the identical thing two lines above.** See
`tasks/study-designer/057`'s predecessor text for the full account
(`embarch-core` decision 30's "settlement 2" vs. same-repo decision 59, in
`eap_parse.rs`). **`057` found zero candidates for this shape** — `gatt.rs`
had no cross-repo citations at all — which is itself worth recording: the
shape is real but not universal, and a file can be clean of it.

**`055`'s find (carried forward, still the standing reminder): a false
sentence can misattribute *where* a cited feature runs, not just *which*
decision covers it.** See `tasks/study-designer/056`'s copy of this
paragraph for the full `crc32_ieee` account.

## Method (carried over from `044`-`057`, confirmed useful all fifteen
times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero. **A zero is a real, reportable result, not a null
one** — two of fifteen files so far (`bounded.rs`, `gatt.rs`) checked out
completely clean.

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. Check every bare *and* every labelled `decision N`
against *this crate's own* decisions.md/decisions/*.md first regardless, and
**for every cross-repo citation found, also ask whether a same-repo decision
already says the same thing** (`056`'s shape) — a file can have none of
these to check, as `gatt.rs` did.

**Run the continuation-grep too, every file, not just the target.**
`grep -rlIE '[Dd]ecisions[[:space:]]*$'` over the whole repo catches a
citation wrapped across a comment continuation, which a line-based
`grep -cE` census misses entirely (found first by `embarch-core/068`). As of
`057` it hits **four files**: `Cargo.toml`, `src/lib.rs` (twice), `src/eap.rs`,
and `src/schema_version.rs` — all four already-swept or out of this chain's
file list, and all four checked correct. **`057` also found that
`schema_version.rs`'s hit had not been named in `056`'s report despite the
file being unchanged since `044`** — so re-run this full-repo grep fresh each
time rather than trusting a prior unit's file list as closed; report
whatever it finds, even if it lands outside the file being swept and even if
it repeats a hit a prior unit already named.

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
- `src/gatt.rs` — done in `057`. 11 grep-matching lines, 14 distinct citation
  instances. 0 wrong numbers, 0 false sentences, 0 unlabelled cross-repo
  citations — the second true zero in the chain; no cross-repo citations of
  any kind in this file.

## Running tally across the chain (`044`–`057`, fifteen files reporting
per-file counts)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14, `eap_parse.rs` 13, `gatt.rs` 14. **Total: 447.** Wrong numbers
found: 0+3+3+2+3+1+0+1+1+0+1+0+0+1+0 = **16**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1+1+0+0 = **5**. Recompute this fresh in your report
using the actual per-file numbers above plus whatever this unit adds.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` through `057`
all re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [ ] One named file (`src/registry.rs`, unless a reason is given to
      reorder) fully swept, wrong numbers and false sentences counted
      separately, and every plain number and implementation-status claim in
      a cited sentence checked, not only the decision number.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted. Remember `056`'s find: correctly
      labelled and still wrong is possible; and check whether a same-repo
      decision already says the same thing.
- [ ] The whole-repo continuation-grep
      (`grep -rlIE '[Dd]ecisions[[:space:]]*$'`) run fresh (do not assume
      `057`'s four-file list is exhaustive) and any hit reported, even one
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
`026`) blocked, `In flux: yes`. `047` through `057` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
