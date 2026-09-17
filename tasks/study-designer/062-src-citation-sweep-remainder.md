# 062 — Citation sweep: `src/` remainder after `sample.rs`

**State:** claimed by agent/study-designer/062-src-citation-sweep-remainder, 2026-09-17 01:03
**Source:** `tasks/study-designer/061`, which swept `src/sample.rs` (7
grep-matching lines, 7 distinct citation instances) plus the thirteen
singular-wrap citations located but not yet checked in six already-closed
files, and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `061`,
2026-09-17, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Nineteen files are now swept (the four originally-named plus fifteen more):

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
 7  src/decoder.rs        — swept in 060
 7  src/sample.rs         — swept in 061
```

**5 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs`
— a *line* count, not a citation-instance count, and per `060`'s finding, not
a complete count of every citation either):

```
 6  src/merged_actions.rs
 5  src/gatt_names.rs
 5  src/eap_interp.rs
 3  src/vendor.rs
 2  src/records.rs
 0  src/ids.rs — no citations; needs no sweep, listed so the count above is exhaustive
```

Take `src/merged_actions.rs` next (the sole remaining file tied for largest)
unless a reason is given to reorder — read every cited decision's body
against the sentence around the citation, and fix what is wrong. Count wrong
*numbers* and false *sentences* separately, per the method below. **This
file carries one already-located singular-wrap citation** —
`merged_actions.rs:72`, decision 39 — check it as part of this file's normal
sweep, same as any other line; it was deliberately left unchecked by `060`
and `061` so it would be checked once, by whoever swept the file itself,
rather than twice or by a unit with no other business in the file. When you
run out of budget, file the next `tasks/study-designer/<next>` naming
exactly which files remain, the same way this one does.

**`059`'s find, carried forward: a citation can be correctly labelled
cross-repo and still name the wrong decision, where the *general subject* is
close enough to sound right.** See `tasks/study-designer/060`'s copy of this
paragraph for the full `outpost.rs` decision-30-vs-38 account.

**`058`'s find, still carried forward: a citation number can be to a real,
existing decision and still be flatly wrong** — not stale, not superseded,
just never having said what the comment claims it said. See
`tasks/study-designer/059`'s copy of this paragraph (the `registry.rs`
`StreamCapture`/decision 35→39 account) for the full history.

**`056`'s find, still carried forward:** a wrong number that was real,
on-topic, cross-repo, and correctly labelled — and still wrong, because a
nearer same-repo decision said the identical thing two lines above. See
`tasks/study-designer/057`'s predecessor text for the full account.
`057` through `061` all found zero candidates for this shape (no cross-repo
citation with a same-repo duplicate in any of the five) — five files running
in the true-zero column for this specific check.

**`055`'s find (carried forward, still the standing reminder):** a false
sentence can misattribute *where* a cited feature runs, not just *which*
decision covers it. See `tasks/study-designer/056`'s copy of this paragraph
for the full `crc32_ieee` account.

**`060`'s find, closed by `061`: the continuation-grep was plural-only and
missed a singular "decision" wrap.** Fixed permanently — run
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'` (singular-inclusive) from now on,
not the old plural-only pattern. `061` re-ran it and got the same 17 hits as
`060`'s corrected count, checked the thirteen that sat in already-closed
files (`protocol.rs:93`, `study.rs:3`/`:88`, `study_builder.rs:190`/`:1438`/
`:1510`, `schema_version.rs:113`/`:133`/`:203`, `lib.rs:38`/`:45`/`:758`,
`eap.rs:1`) against their decision bodies, and found all thirteen correct —
0 wrong numbers, 0 false sentences. That leaves exactly one located-but-
unchecked singular-wrap citation outstanding: `merged_actions.rs:72`, this
file's own line, to be checked as part of its normal sweep above. `Cargo.toml`'s
two hits (`:19`, `:91`) remain outside the `src/` file list and were
re-confirmed correct by `061` as they have been every prior unit.

## Method (carried over from `044`-`061`, confirmed useful all nineteen times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero. **A zero is a real, reportable result, not a null
one** — three of nineteen files so far (`bounded.rs`, `gatt.rs`, `decoder.rs`)
checked out completely clean; `outpost.rs` had exactly one problem, a
wrong-number cross-repo citation with no false sentence of the other kind (8
citations, 1 wrong number, 0 false sentences); `sample.rs` had exactly one
problem, a false sentence with no wrong number (7 citations, 0 wrong
numbers, 1 false sentence — see `061`'s fold for the `rx_utc_ms`/decision 72
account).

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. Check every bare *and* every labelled `decision N`
against *this crate's own* decisions.md/decisions/*.md first regardless, and
**for every cross-repo citation found, also ask whether a same-repo decision
already says the same thing** (`056`'s shape) — a file can have none of
these to check, as `gatt.rs`, `registry.rs`, `outpost.rs`, `decoder.rs` and
`sample.rs` all did. **Also ask, per `059`'s find, whether a *different*
decision in the same cited file/repo is the one that actually backs the
specific claim** — a decision being on-topic and correctly labelled is not
the same as it being the right number.

**Run the continuation-grep too, every file, not just the target — using the
corrected, singular-inclusive pattern**:
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`. As of `061` it hits the same eight
files plus `Cargo.toml` (17 hits total). Re-run this full-repo grep fresh
each time rather than trusting a prior unit's file list as closed; report
whatever it finds, even if it lands outside the file being swept and even if
it repeats a hit a prior unit already named.

## Files already swept (do not re-do)

See `tasks/study-designer/061`'s copy of this section for the full
eighteen-file history through `decoder.rs`. Adding:

- `src/sample.rs` — done in `061`. 7 grep-matching lines, 7 distinct
  citation instances. 0 wrong numbers, **1 false sentence** — fixed. The
  `rx_utc_ms` field doc asserted dev-bench "seeded and periodically
  resynced" its clock from Core's `Hello.host_utc_ms` (citing decision 12);
  decision 72 established that half is designed and **not implemented in
  firmware** — the same false claim `src/protocol.rs`'s own
  `Hello.host_utc_ms` doc comment carried before decision 72's correction
  pass, and one of the three sites that pass names as corrected. `sample.rs`
  was not among those three sites and had been carrying the same false claim
  ever since, unnoticed by every earlier sweep unit because none of the
  eighteen files it checked was this one. Fixed to match the corrected
  language in `src/protocol.rs` and `interfaces/decoders.md`: cites decision
  72 alongside decision 12, and states plainly that a dev-bench-mediated
  tap's `rx_utc_ms` is bench uptime, not UTC.
- Thirteen singular-wrap citations in six already-closed files
  (`protocol.rs:93`; `study.rs:3`, `:88`; `study_builder.rs:190`, `:1438`,
  `:1510`; `schema_version.rs:113`, `:133`, `:203`; `lib.rs:38`, `:45`,
  `:758`; `eap.rs:1`) — checked for the first time in `061` (the plural-only
  continuation-grep had never surfaced them for any prior unit to check). All
  thirteen correct: 0 wrong numbers, 0 false sentences.

## Running tally across the chain (`044`–`061`, nineteen files reporting
per-file counts, plus thirteen singular-wrap re-checks)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14, `eap_parse.rs` 13, `gatt.rs` 13, `registry.rs` 9, `outpost.rs` 8,
`decoder.rs` 9, `sample.rs` 7, plus 13 singular-wrap re-checks. **Total: 492.**
Wrong numbers found: 0+3+3+2+3+1+0+1+1+0+1+0+0+1+0+0+1+0+0+0 = **17**. False
sentences found: 0+0+2+0+0+0+0+1+0+0+0+1+1+0+0+1+0+0+1+0 = **7**. Recompute
this fresh in your report using the actual per-file numbers above plus
whatever this unit adds.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` through `061`
all re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [ ] `src/merged_actions.rs` fully swept, wrong numbers and false sentences
      counted separately, every plain number and implementation-status claim
      in a cited sentence checked, and the located singular-wrap citation at
      `:72` (decision 39) checked as part of the same pass.
- [ ] Cross-repo citations carry their repo name — and every citation, bare
      or labelled, is checked against this crate's own decisions first, and
      a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted. Remember `056`'s find, `058`'s
      find, and `059`'s find (see above).
- [ ] The whole-repo continuation-grep, singular-inclusive pattern
      `grep -rlIE '[Dd]ecisions?[[:space:]]*$'`, run fresh (do not assume
      this task's list is exhaustive) and any hit reported, even one landing
      outside the file being swept.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`,
`026`) blocked, `In flux: yes`. `047` through `061` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
