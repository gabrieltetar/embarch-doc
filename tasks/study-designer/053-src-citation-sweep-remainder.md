# 053 — Citation sweep: `src/` remainder after `bounded.rs`

**State:** open
**Source:** `tasks/study-designer/052`, which swept `src/bounded.rs` (the
largest of the 16 files `051` left remaining) and left the rest.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `052`,
2026-09-16, via `scripts/check-doc-size.py`): unchanged.**
`embarch-study-designer/spec.md` and `open.md` remain in the last 10% of
their caps, filed as `tasks/study-designer/032` and `026` respectively, both
**blocked**. This unit is a source-comment sweep and should not need to write
either file; if it turns out you must, spend the bytes and say so in your
report.

## What

Ten of the four originally-named plus the six largest-remaining files are now
swept:

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
```

**14 files remain (plus `ids.rs`, which has no citations), largest first, by
the same grep methodology** (`grep -cE '[Dd]ecision' src/<file>.rs` — a *line*
count, not a citation-instance count):

```
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

Take one file — `src/eap.rs` next, largest remaining, unless a reason is
given to reorder — read every cited decision's body against the sentence
around the citation, and fix what is wrong. Count wrong *numbers* and false
*sentences* separately, per the method below. When you run out of budget, file
the next `tasks/study-designer/<next>` naming exactly which files remain, the
same way this one does.

**Grep-line-count does not predict citation-instance count, and does not
predict cost, and does not predict yield.** `052` took one file
(`bounded.rs`, 22 grep-matching lines, 25 distinct citation instances) and
found **zero** defects — a legitimate result, not a sign the pass was
skipped: every citation (decisions 15, 46, 49, 54, 63, all same-crate, none
cross-repo) was read against `decisions/limits.md` and `decisions/removed.md`
in full, including three numeric claims (1,293,608 bytes, 32 × 536-byte
records, the ~3.5x/262,144-byte ceiling derivation, 64 MiB in
`.cargo/config.toml`), all of which check out exactly. This is the first zero
in the chain since `044`/`046` era found only unlabelled-cross-repo defects —
worth noting for the running tally this task's dispatcher asked for (see
`changelog.d/study-designer-052-*` for `052`'s three numbers), since a sweep
that finds nothing is still evidence about the corpus, not a wasted unit.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`-`052`, confirmed useful all ten times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and nine of
the ten sweeps in this one, has been prose a decision made false or a
citation pointing at the wrong (but real) decision, not a bare typo. `052`
is the first true zero. Count the two categories separately and report both,
honestly, even if one or both is zero — "checked N, found none" is a
legitimate result.

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
`046`, `047`, `049`, `051` and `052` found none (`052`'s file had no
cross-repo citations of any kind, labelled or not — every one of its 25
instances was same-crate). `048` found the *opposite* shape: a same-repo
decision mislabelled *as* foreign. `050` found a **third** shape: a
cross-repo decision correctly labelled on its first two mentions but repeated
bare four lines later, past `check-decision-refs.py`'s attribution window.
Check every bare *and* every labelled `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless — a repo prefix is not proof the
label is right, and is not proof it is wrong either.

**A wrong number is not always a nearby-digit typo.** `051`'s two finds were
both a real, existing, but topically wrong decision — not a transposed digit
— found only by reading the cited decision's actual text against the claim,
never by the number alone looking suspicious. Reading the crate's own
`interfaces/*.md` mattered as much as reading `decisions/*.md` in `051`.
`052` had no `interfaces/*.md` claims to check — `bounded.rs` cites only
`decisions/limits.md` and `decisions/removed.md`, and its own `.cargo/config.toml`
comment (not itself a citation, but useful corroboration) independently
restates the same 64 MiB figure decision 63 gives.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s, `048`'s, `049`'s, `050`'s, `051`'s and
`052`'s findings all resolved without it. When no paired table or direct
textual match exists, run `git log --follow -p -- embarch-study-designer/decisions/
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
  citation instances. 1 wrong number, 1 false sentence, 0 unlabelled
  cross-repo citations — both fixed (`MAX_SOURCES_PER_PROTOCOL`'s
  `decision 57` cite and its "three (`ctrl`/`status`/`data`)" claim; corrected
  to two, `ctrl`/`status`, per `interfaces/eap.md`).
- `src/result.rs` — done in `051`. 24 grep-matching lines, 25 distinct
  citation instances. 1 wrong number, 0 false sentences, 0 unlabelled
  cross-repo citations — fixed (`security_level`'s `decision 50` cite,
  should be `decision 44`).
- `src/bounded.rs` — done in `052`. 22 grep-matching lines, **25 distinct
  citation instances. 0 wrong numbers, 0 false sentences, 0 unlabelled
  cross-repo citations** — every citation (decisions 15, 46, 49, 54, 63)
  checked against `decisions/limits.md` and `decisions/removed.md` and found
  accurate, including all embedded numeric claims.

## Running tally across the chain (`044`–`052`, nine files reporting per-file
counts plus `045`'s discrepancy note on grep-vs-instance)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported; no distinct-instance recount published), `study.rs` 52
(ditto), `gatt_extract.rs` 36 (ditto), `lib.rs` 41 (ditto),
`study_builder.rs` 36, `protocol.rs` ~38, `streams.rs` 31, `limits.rs` 32,
`result.rs` 25, `bounded.rs` 25. Wrong numbers found: 0+3+3+2+3+1+0+1+1+0 = 14.
False sentences found: 0+0+2+0+0+0+0+1+0+0 = 3. **This running total is
carried forward from `052`'s dispatch note — recompute it fresh in your
report using the actual per-file numbers above plus whatever this unit adds,
since some early files (`044`-`047`) never published a distinct-instance
count separate from the grep-line count, only the grep count.**

## Done when

- [ ] One named file (`src/eap.rs`, unless a reason is given to reorder)
      fully swept, wrong numbers and false sentences counted separately.
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
blocked, `In flux: yes` per `046`'s dispatch note; `047` through `052` all
re-checked `scripts/check-doc-size.py` fresh and found no new reserve entries
for this scope, touching neither file. Check fresh again rather than trusting
this number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
