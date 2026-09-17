# 061 — Citation sweep: `src/` remainder after `decoder.rs`

**State:** open
**Source:** `tasks/study-designer/060`, which swept `src/decoder.rs` (7
grep-matching lines, 9 distinct citation instances, the third true zero in
the chain) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `060`,
2026-09-17, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Eighteen files are now swept (the four originally-named plus fourteen more):

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
```

**6 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs`
— a *line* count, not a citation-instance count, and per `060`'s finding
below, not a complete count of every citation either):

```
 7  src/sample.rs
 6  src/merged_actions.rs
 5  src/gatt_names.rs
 5  src/eap_interp.rs
 3  src/vendor.rs
 2  src/records.rs
 0  src/ids.rs — no citations; needs no sweep, listed so the count above is exhaustive
```

Take `src/sample.rs` next (the sole remaining file tied for largest — `060`
took `decoder.rs`, its tie-mate) unless a reason is given to reorder — read
every cited decision's body against the sentence around the citation, and fix
what is wrong. Count wrong *numbers* and false *sentences* separately, per
the method below. When you run out of budget, file the next
`tasks/study-designer/<next>` naming exactly which files remain, the same way
this one does.

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
`057`, `058`, `059` and `060` all found zero candidates for this shape (no
cross-repo citation with a same-repo duplicate in any of the four) — four
files running in the true-zero column for this specific check.

**`055`'s find (carried forward, still the standing reminder):** a false
sentence can misattribute *where* a cited feature runs, not just *which*
decision covers it. See `tasks/study-designer/056`'s copy of this paragraph
for the full `crc32_ieee` account.

## New in `060`: the continuation-grep is plural-only and has a real blind spot

The method section below has always run
`grep -rlIE '[Dd]ecisions[[:space:]]*$'` to catch a citation number wrapped
onto the next comment line — but that pattern only matches a line ending in
the **plural** "decisions". A line ending in the **singular** "decision" is
just as valid a wrap and is invisible to it, and also invisible to the
per-file `grep -cE '[Dd]ecisions? [0-9]+'` census, since that pattern
requires the number on the *same* line as the word. `060` found this by
reading `decoder.rs` directly: its module doc opens `— decision` at the end
of line 1 and `52 (interfaces/decoders.md).` at the start of line 2, a real
citation to decision 52 that no grep in this chain, ever, had caught.

**Run the corrected, singular-inclusive pattern instead, from now on:**

```
grep -rlIE '[Dd]ecisions?[[:space:]]*$'
```

Re-run at `060` time, this surfaced **16 hits across the repo** (verified by
reading the line after each — all real number-on-next-line wraps, not false
positives):

- `src/decoder.rs:1` — decision 52. **Checked by `060`, correct.**
- `src/merged_actions.rs:72` — decision 39. **Not yet swept** — this file is
  on the remaining-files list above; whoever takes it must check this
  citation as part of that file's normal sweep, same as any other line.
- `src/protocol.rs:93` — decision 10 (swept `049`).
- `src/study.rs:3` and `:88` — decision 39, twice (swept `045`).
- `src/study_builder.rs:190`, `:1438`, `:1510` — decisions 37, 46, 41 (swept
  `048`).
- `src/schema_version.rs:113`, `:133`, `:203` — decisions 40, 40, and
  31/32/52/53/54 together (swept `044`).
- `src/lib.rs:38`, `:45`, `:758` — decisions 58-62 (twice) and 47 (swept
  `047`).
- `src/eap.rs:1` — decisions 58-62 (swept `053`).
- `Cargo.toml:19`, `:91` — embarch-dev-bench decision 8, and decisions 34/35
  (outside the `src/` file list; `Cargo.toml` is already in the standing
  continuation-grep's tracked set, just under the plural pattern only).

**None of the seven already-closed files' singular-wrap citations have been
re-checked for correctness against their decision text** — `044` through
`049` and `053` all ran the plural-only grep, found nothing new, and closed.
That is not evidence these seven specific citations are wrong; it is only
evidence they were never actually looked at by any unit in this chain,
because the tool that was supposed to surface them could not see them. This
is real, scoped audit work: seven citations (decision 10, decision 39 x2,
decisions 37/46/41, decisions 40/40/31-32-52-53-54, decisions 58-62 x2 and
47) in six already-closed files, none previously read against their decision
bodies. **Whoever takes this task should spend part of the budget on these
seven before or alongside `sample.rs`**, since they are cheap to check (the
line is already located) and each is a citation this whole chain's own
"exhaustive" claim was silently wrong about until now.

## Method (carried over from `044`-`060`, confirmed useful all eighteen times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero. **A zero is a real, reportable result, not a null
one** — three of eighteen files so far (`bounded.rs`, `gatt.rs`, `decoder.rs`)
checked out completely clean; `outpost.rs` had exactly one problem, a
wrong-number cross-repo citation with no false sentence of the other kind (8
citations, 1 wrong number, 0 false sentences).

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. Check every bare *and* every labelled `decision N`
against *this crate's own* decisions.md/decisions/*.md first regardless, and
**for every cross-repo citation found, also ask whether a same-repo decision
already says the same thing** (`056`'s shape) — a file can have none of
these to check, as `gatt.rs`, `registry.rs`, `outpost.rs` and `decoder.rs` all
did. **Also ask, per `059`'s find, whether a *different* decision in the same
cited file/repo is the one that actually backs the specific claim** — a
decision being on-topic and correctly labelled is not the same as it being
the right number.

**Run the continuation-grep too, every file, not just the target — using the
corrected, singular-inclusive pattern from now on** (see above):
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`. As of `060` it hits the four
already-known files plus `Cargo.toml`'s second location and every file listed
above. Re-run this full-repo grep fresh each time rather than trusting a
prior unit's file list as closed; report whatever it finds, even if it lands
outside the file being swept and even if it repeats a hit a prior unit
already named.

## Files already swept (do not re-do)

See `tasks/study-designer/060`'s copy of this section for the full
seventeen-file history through `outpost.rs`. Adding:

- `src/decoder.rs` — done in `060`. 7 grep-matching lines, **9** distinct
  citation instances (line 154's `decisions 59/60` is two, plus one the
  line-based census cannot see at all — the module doc's opening citation to
  decision 52, split across a line wrap). 0 wrong numbers, 0 false sentences,
  0 unlabelled cross-repo citations — the third true zero in the chain, and
  the file that found the continuation-grep's blind spot.

## Running tally across the chain (`044`–`060`, eighteen files reporting per-file counts)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14, `eap_parse.rs` 13, `gatt.rs` 13, `registry.rs` 9, `outpost.rs` 8,
`decoder.rs` 9. **Total: 472.** Wrong numbers found:
0+3+3+2+3+1+0+1+1+0+1+0+0+1+0+0+1+0 = **17**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1+1+0+0+1+0+0 = **6**. Recompute this fresh in your
report using the actual per-file numbers above plus whatever this unit adds.
This total does not yet include any of the seven singular-wrap citations
found in already-closed files above — those were located, not counted or
verified, by `060`.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` through `060`
all re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [ ] `src/sample.rs` fully swept, wrong numbers and false sentences counted
      separately, and every plain number and implementation-status claim in
      a cited sentence checked, not only the decision number.
- [ ] The seven singular-wrap citations found in already-closed files
      (`merged_actions.rs:72` is the exception — not yet swept, check it as
      part of that file's own turn instead) read against their decision
      bodies and reported correct or fixed, same as any other citation.
- [ ] Cross-repo citations carry their repo name — and every citation, bare
      or labelled, is checked against this crate's own decisions first, and
      a cross-repo decision's own text (including any amendment) is read
      before it is called wrong, or trusted. Remember `056`'s find, `058`'s
      find, and `059`'s find (see above).
- [ ] The whole-repo continuation-grep, **using the corrected,
      singular-inclusive pattern** `grep -rlIE '[Dd]ecisions?[[:space:]]*$'`,
      run fresh (do not assume this task's list is exhaustive) and any hit
      reported, even one landing outside the file being swept.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`,
`026`) blocked, `In flux: yes`. `047` through `060` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
