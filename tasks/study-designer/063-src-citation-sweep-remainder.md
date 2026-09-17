# 063 — Citation sweep: `src/` remainder after `merged_actions.rs` (closes `src/`)

**State:** done — 2026-09-17, `agent/study-designer/063-src-citation-sweep-remainder`
**Source:** `tasks/study-designer/062`, which swept `src/merged_actions.rs` (6
grep-matching lines, 8 distinct citation instances, plus its own
located singular-wrap at `:72`) and left the last four files.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

**Doc-size reserve for `study-designer` (re-checked fresh by `062`,
2026-09-17, via `scripts/check-doc-size.py --pressure`): unchanged.**
`embarch-study-designer/spec.md` (9,350/10,240 B, 890 B left) and `open.md`
(4,659/5,120 B, 461 B left) remain in the last 10% of their caps, filed as
`tasks/study-designer/032` and `026` respectively, both **blocked**. This
unit is a source-comment sweep and should not need to write either file; if
it turns out you must, spend the bytes and say so in your report.

## What

Twenty files are now swept (the four originally-named plus sixteen more):

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
 6  src/merged_actions.rs — swept in 062
```

**4 files remain, largest first, by the same grep methodology**
(`grep -cE '[Dd]ecisions? [0-9]+' src/<file>.rs` — a *line* count, not a
citation-instance count, and per `060`'s finding, not a complete count of
every citation either):

```
 5  src/gatt_names.rs
 5  src/eap_interp.rs
 3  src/vendor.rs
 2  src/records.rs
 0  src/ids.rs — no citations; needs no sweep, already confirmed exhaustive
```

Take `src/gatt_names.rs` or `src/eap_interp.rs` next (tied at 5 lines) unless
a reason is given to reorder — read every cited decision's body against the
sentence around the citation, and fix what is wrong. Count wrong *numbers*
and false *sentences* separately, per the method below. **This closes out
`src/` if all four are swept in one unit** (13 grep-matching lines total,
likely more distinct instances once multi-citation lines are counted) — say
so plainly in the report, and note what (if anything) in the repo still
needs a citation check outside `src/` (`Cargo.toml`'s two hits have been
re-confirmed correct by every unit from `061` on and need no further
standing check unless the continuation-grep surfaces something new).

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
`057` through `062` all found zero candidates for this exact shape (no
cross-repo citation with a same-repo duplicate saying the identical thing);
`062` did find a same-repo near-duplicate of a different kind (see below),
worth watching for again.

**`062`'s find: a wrong number can be a same-repo mislabel of the sole other
kind — two sentences making the identical claim in the same file, citing two
different, both-real decision numbers, only one of which actually backs the
claim.** `src/merged_actions.rs:72` said "the busywork decision 39 removes"
for the claim that vendor-published UUIDs never need engineer registration;
decision 39 (`streams.md`) is "One generic inbound stream pipeline", wholly
unrelated. The identical claim, worded almost the same way, sits ~100 lines
later in the same file (`:170`) correctly citing **decision 41** (`gatt.md`,
"A built-in table of vendor-defined GATT service identities" — whose own
body states "transcribing a 128-bit UUID ... is pure error surface" nearly
verbatim). Unlike `056`'s shape (a cross-repo citation shadowed by a
same-repo one), both citations here were same-repo; the tell was the two
near-identical sentences citing different numbers, not a repo-label
mismatch. Watch for two sentences saying the same thing with different
numbers, regardless of which is cross-repo — check both, don't assume the
later one (or the more prominent one) is the one that's right.

**`055`'s find (carried forward, still the standing reminder):** a false
sentence can misattribute *where* a cited feature runs, not just *which*
decision covers it. See `tasks/study-designer/056`'s copy of this paragraph
for the full `crc32_ieee` account.

## Method (carried over from `044`-`062`, confirmed useful all twenty times)

**Read the cited decision's body, then read the sentence around the
citation, in that order.** A number that resolves is not evidence the claim
holds. **Check every number and every implementation-status claim in the
cited sentence, not just the decision number.** Count the two categories —
wrong numbers, false sentences — separately and report both, honestly, even
if one or both is zero. **A zero is a real, reportable result, not a null
one** — three of twenty files so far (`bounded.rs`, `gatt.rs`, `decoder.rs`)
checked out completely clean; `outpost.rs` had exactly one problem, a
wrong-number cross-repo citation with no false sentence of the other kind (8
citations, 1 wrong number, 0 false sentences); `sample.rs` had exactly one
problem, a false sentence with no wrong number (7 citations, 0 wrong
numbers, 1 false sentence); `merged_actions.rs` had exactly one problem, a
wrong number with no false sentence of the other kind (8 citations, 1 wrong
number, 0 false sentences — the same-repo near-duplicate shape above).

**Check cross-repo labelling as the first pass, specifically in this repo.**
A bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N`. Check every bare *and* every labelled `decision N`
against *this crate's own* decisions.md/decisions/*.md first regardless, and
**for every cross-repo citation found, also ask whether a same-repo decision
already says the same thing** (`056`'s shape) — a file can have none of
these to check, as `gatt.rs`, `registry.rs`, `outpost.rs`, `decoder.rs` and
`sample.rs` all did; `merged_actions.rs` had one cross-repo citation
(`embarch-ui` decision 17), correctly labelled and correct on the merits —
its section heading looked unrelated ("selective-monitor target list
becomes a dialog"), but reading the *whole* cited section (not just its
first paragraph) surfaced the exact matching claim two paragraphs down.
**Read a cited section to its end before judging it off-topic.** **Also ask,
per `059`'s find, whether a *different* decision in the same cited file/repo
is the one that actually backs the specific claim** — a decision being
on-topic and correctly labelled is not the same as it being the right
number.

**Run the continuation-grep too, every file, not just the target — using the
corrected, singular-inclusive pattern**:
`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`. As of `062` it hits the same nine
files (`Cargo.toml` plus `src/study_builder.rs`, `src/study.rs`,
`src/protocol.rs`, `src/decoder.rs`, `src/eap.rs`, `src/merged_actions.rs`,
`src/lib.rs`, `src/schema_version.rs`) — all now fully checked, so a fresh
run for this unit is expected to turn up nothing new unless this unit's four
files themselves gain a hit. Re-run this full-repo grep fresh each time
rather than trusting a prior unit's file list as closed; report whatever it
finds, even if it lands outside the file being swept and even if it repeats
a hit a prior unit already named. **Caution from `062`: a file can appear in
this grep's hit list and still have its wrap already checked and counted by
an earlier unit** (`decoder.rs:1` did — checked in `060`, resurfaced in
`062`'s fresh grep, not a new find) — read "Files already swept" below
before assuming a hit is new.

## Files already swept (do not re-do)

See `tasks/study-designer/062`'s copy of this section for the full
nineteen-file history through `sample.rs`. Adding:

- `src/merged_actions.rs` — done in `062`. 6 grep-matching lines, **8**
  distinct citation instances (line 1's `decisions 34/35` is two) plus the
  located singular-wrap at `:72` checked as part of this file's own sweep.
  **1 wrong number** (`:72`, decision 39 → 41, fixed), **0 false sentences**.
  1 cross-repo citation (`embarch-ui` decision 17, line 48), correctly
  labelled and correct on the merits.

## Running tally across the chain (`044`–`062`, twenty files reporting
per-file counts, plus thirteen singular-wrap re-checks)

Distinct citation instances checked so far: `schema_version.rs` ~53 (grep
count only reported), `study.rs` 52 (ditto), `gatt_extract.rs` 36 (ditto),
`lib.rs` 41 (ditto), `study_builder.rs` 36, `protocol.rs` ~38, `streams.rs`
31, `limits.rs` 32, `result.rs` 25, `bounded.rs` 25, `eap.rs` 21, `ffi.rs` 16,
`crc.rs` 14, `eap_parse.rs` 13, `gatt.rs` 13, `registry.rs` 9, `outpost.rs` 8,
`decoder.rs` 9, `sample.rs` 7, `merged_actions.rs` 8, plus 13 singular-wrap
re-checks. **Total: 500.** Wrong numbers found:
0+3+3+2+3+1+0+1+1+0+1+0+0+1+0+0+1+0+0+0+1 = **18**. False sentences found:
0+0+2+0+0+0+0+1+0+0+0+1+1+0+0+1+0+0+1+0+0 = **7**. Recompute this fresh in
your report using the actual per-file numbers above plus whatever this unit
adds.

## Also worth doing: the `.cargo/config.toml` count is now dated, not fixed

`053` found the test count had drifted from decision 63's dated
[2026-09-02] 108/108 to a fresh [2026-09-16] measurement of **125/125**
(116 lib + 9 `firmware_test_vectors` integration tests). `054` through `062`
all re-ran the full suite fresh (`cargo test --all-targets`) and got the
same 125/125 (116 + 9), so the comment does not yet need a third dated line.
If this keeps drifting, a future sweep should decide whether the comment
should track "as of last sweep" indefinitely or drop the running-count
framing entirely in favor of just decision 63's citation — not this task's
call to make unprompted, noted here so it is not lost.

## Done when

- [x] `src/gatt_names.rs`, `src/eap_interp.rs`, `src/vendor.rs`,
      `src/records.rs` all fully swept, wrong numbers and false sentences
      counted separately per file, every plain number and
      implementation-status claim in a cited sentence checked, not only the
      decision number.
- [x] Cross-repo citations carry their repo name — and every citation, bare
      or labelled, is checked against this crate's own decisions first, and
      a cross-repo decision's own text (including any amendment) is read to
      its end before it is called wrong, or trusted. Remember `056`'s find,
      `058`'s find, `059`'s find, and `062`'s same-repo near-duplicate shape
      (see above).
- [x] The whole-repo continuation-grep, singular-inclusive pattern
      `grep -rlIE '[Dd]ecisions?[[:space:]]*$'`, run fresh (do not assume
      this task's list is exhaustive) and any hit reported, even one landing
      outside the file being swept — and cross-checked against "Files
      already swept" before treating any hit as new.
- [x] Say plainly whether this closes out `src/` (all four files done, `src/`
      exhausted) or, if not, file the next `tasks/study-designer/<next>`
      naming exactly which files remain.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/study-designer-*` fragment, reporting distinct citation
      instances checked, wrong numbers found, and false sentences found as
      three explicit numbers.

## Result

**`src/` is now fully swept** — all twenty files (`044` through `063`) plus
`Cargo.toml` checked. No file in `src/` remains.

**Per-file counts, this unit:**

- `src/gatt_names.rs` — 5 grep-matching lines, **5** distinct citation
  instances (lines 1, 83, 126, 146, 269, each one citation). **3 wrong
  numbers** (lines 83, 126, 269 all cited "decision 57" for claims that are
  actually decision 56's — fixed to 56), **0 false sentences** once the
  number is corrected (the surrounding claims themselves — the two-map
  split, vendor-wins precedence, the group-header naming — all check out
  against decision 56's body).
- `src/eap_interp.rs` — 5 grep-matching lines, **6** distinct citation
  instances (line 10's "decisions 31/32" is two). **0 wrong numbers, 0
  false sentences.** Decision 60 (`protocol-exec.md`, `RunProtocol`)
  confirmed for all three citations including the "no `Event` for a write's
  own ATT response" claim; decisions 31/32 (`gatt.md`, `GattDiscover`/
  `GattMonitorAll`) confirmed by title; decision 62 (`protocol-exec.md`, "A
  protocol run reports the state it stopped in") confirmed for the
  session-variables-not-reported claim.
- `src/vendor.rs` — 3 grep-matching lines, **3** distinct citation
  instances. **1 wrong number** (line 192, "decision 57" → 56, same shape
  as `gatt_names.rs` above — the "service a UUID names" / vendor-wins-one-
  level-up claim is decision 56's content), **0 false sentences**. Decision
  41 (`gatt.md`, vendor-defined GATT service identities) confirmed for the
  module's own header citation; decision 56 (line 59, `short_name` as a
  separate field) confirmed.
- `src/records.rs` — 2 grep-matching lines, **2** distinct citation
  instances. **0 wrong numbers, 0 false sentences.** Decision 70
  (`payload-meaning.md`) confirmed word-for-word against the module doc
  comment's 10 h-drain account (976 bytes, four 244-byte notifications, 3 of
  598 records, 9538149 vs 9537173 bytes). Decision 39 (`streams.md`)
  confirmed for the "byte meaning is the knowledge decision 39 took away
  from dev-bench" claim, cross-checked against decisions 55/60's own
  restatements of the same fact.

**This unit's totals: 16 distinct citation instances checked, 4 wrong
numbers found, 0 false sentences found.**

**New find, carried into `064`:** unlike every prior wrong number in this
chain (each its own one-off mistake, or `062`'s two-different-decisions
shape), this was **the same wrong number, "decision 57" for "decision 56",
repeated four times across two files**, for what reads as the same
underlying claim each time (service naming reuses the characteristic-naming
mechanism). Worth checking whether the pattern recurs in the four files this
unit found unswept outside `src/` (see below) — `filed as
tasks/study-designer/064`.

**Not closed: four files outside `src/` this chain has never checked.**
`tools/extract_gatt_config.rs` (7 grep-matching lines), `tests/
firmware_test_vectors.rs` (8), `tests/eap_worked_protocols.rs` (3), `.cargo/
config.toml` (6) all carry citations and were outside this task's and every
prior unit's scope (`Cargo.toml` itself was re-checked through `061`–`063`,
but nothing under `tools/` or `tests/`, and `.cargo/config.toml` is a
different file from `Cargo.toml`). Filed as
`tasks/study-designer/064-citation-sweep-outside-src.md`.

**Running tally across the chain (`044`–`063`), recomputed:** distinct
citation instances checked: 500 (through `062`) + 16 (this unit) = **516**.
Wrong numbers found: 18 (through `062`) + 4 (this unit) = **22**. False
sentences found: 7 (through `062`) + 0 (this unit) = **7**.

**Continuation-grep (`grep -rlIE '[Dd]ecisions?[[:space:]]*$'`), run fresh:**
same nine files as `062`/`063` — `Cargo.toml`, `src/protocol.rs`,
`src/decoder.rs`, `src/lib.rs`, `src/schema_version.rs`,
`src/study_builder.rs`, `src/eap.rs`, `src/merged_actions.rs`,
`src/study.rs`. All nine already fully checked in prior units (per "Files
already swept"); no hit lands in this unit's four files. Nothing new.

**Reserve:** re-checked fresh via `scripts/check-doc-size.py --pressure`.
`spec.md` (9,350/10,240 B) and `open.md` (4,659/5,120 B) unchanged, both
still parked with their existing blocked compaction tasks (`032`, `026`).
This unit touched neither file.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`,
`026`) blocked, `In flux: yes`. `047` through `062` all re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
