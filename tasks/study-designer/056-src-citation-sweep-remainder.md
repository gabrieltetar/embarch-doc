# 056 — Citation sweep: `src/` remainder after `crc.rs`

**State:** open
**Source:** `tasks/study-designer/055`, which swept `src/crc.rs` (14 grep-matching
lines, 14 distinct citation instances) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `055`,
2026-09-16, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Thirteen of the four originally-named plus the nine largest-remaining files
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
14  src/crc.rs            — swept in 055
```

**11 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs`
— a *line* count, not a citation-instance count, and note the standing
correction: the plain `[Dd]ecision ` pattern this chain used through `053`
cannot match a plural like `decisions 27/29`; use the `?` form when
re-measuring):

```
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

Take one file — `src/eap_parse.rs` next, largest remaining, unless a reason
is given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget,
file the next `tasks/study-designer/<next>` naming exactly which files
remain, the same way this one does.

**`055`'s find: a false sentence that misattributed *where* a cited feature
runs, not just *which* decision covers it.** `crc.rs`'s `crc32_ieee` doc
claimed the in-frame `crc32` grammar primitive (decision 59) "is applied
host-side at render time (`crate::eap_parse`)" as the reason the function is
public. Both halves were wrong: `eap_parse::lower_layout` explicitly refuses
to render a `crc32` field (`LowerGap::Primitive("crc32")` / test
`crc32_is_refused_by_name_rather_than_rendered_flat`), matching decision 71
("A host-side primitive still parsed but not rendered refuses loudly, by
name") and `open.md`'s "Parsed and pinned, with no consumer" section by name
— it is not applied anywhere yet. The function's real, current caller is
`crate::records`'s `RecordCheck` (decision 70), verifying a captured record's
own DUT-computed CRC-32 post-capture — a different feature entirely from the
`.eap` grammar's per-frame primitive. The decision *number* cited (59) was
real and on-topic (`crc32_ieee` genuinely is that primitive's algorithm); the
sentence's claim about it being wired up and *where* was false. Confirmed by
reading `decisions/protocols.md` (58, 59, 71) and `open.md`'s render-gap
section, not by the number alone.

**Reminder from `054` and now `055`: reading the cited decision is necessary
but not sufficient — the false half can be a plain implementation-status
claim (rendered vs. not rendered, called vs. not called) sitting right next
to a correctly-resolving citation.** Check what the surrounding sentence
claims is *true right now*, not only whether the decision number names a
real, on-topic decision.

## Method (carried over from `044`-`055`, confirmed useful all thirteen
times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero.

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. `044` and `045` each found one bare cross-repo
citation missing its label; `050` and `054` each found the different third
shape (a cite correctly labelled on its first mention, then repeated bare
later in the same file, past `check-decision-refs.py`'s attribution window).
`046`, `047`, `049`, `051`, `052`, `053` and `055` found no unlabelled
cross-repo citations in their files (some had none of any kind). Check every
bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless.

**A cross-repo citation that resolves to a real, on-topic decision is not
automatically suspect just because it feels surprising**, and conversely **a
same-repo citation that resolves is not automatically safe** — `055`'s find
resolved to a real, on-topic, same-repo decision the whole time; only reading
the decision's actual current text (including any later amendment, per
`054`) and cross-checking the surrounding implementation-status claim against
the actual code caught it.

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
  citations — fixed. The false sentence: `crc32_ieee`'s doc claimed the
  in-frame `crc32` grammar primitive is "applied host-side at render time
  (`crate::eap_parse`)" — it is not; decision 71 and `open.md` both record it
  as parsed-and-pinned with no render consumer, refused by name
  (`RenderUnimplemented`). Rewritten to cite decision 71 for the render gap
  and `crate::records`' `RecordCheck` (decision 70) as the function's actual,
  current caller.

## Running tally across the chain (`044`–`055`, thirteen files reporting
per-file counts)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14. **Total: 420.** Wrong numbers found:
0+3+3+2+3+1+0+1+1+0+1+0+0 = **15**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1+1 = **5**. Recompute this fresh in your report using
the actual per-file numbers above plus whatever this unit adds, since some
early files (`044`-`047`) never published a distinct-instance count separate
from the grep-line count, only the grep count.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` and `055`
both re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [ ] One named file (`src/eap_parse.rs`, unless a reason is given to
      reorder) fully swept, wrong numbers and false sentences counted
      separately, and every plain number and implementation-status claim in
      a cited sentence checked, not only the decision number.
- [ ] Cross-repo citations in it carry their repo name — and every citation,
      bare or labelled, is checked against this crate's own decisions first,
      and a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`,
`026`) blocked, `In flux: yes`. `047` through `055` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
