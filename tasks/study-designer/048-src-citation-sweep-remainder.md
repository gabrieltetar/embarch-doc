# 048 — Citation sweep: `src/` remainder after `lib.rs`

**State:** claimed by agent/study-designer/048-src-citation-sweep-remainder, 2026-09-13 23:12
**Source:** `tasks/study-designer/047`, which swept `src/lib.rs` (the fourth and
last of the four files `044` originally named) and left the rest of `src/`.
**Scope:** study-designer
**Hardware:** none — source comments only; nothing is built for a board.
**Owner:** no

## What

All four files `044` named are now swept:

```
41  src/schema_version.rs — swept in 044
52  src/study.rs          — swept in 045
36  src/gatt_extract.rs   — swept in 046
41  src/lib.rs            — swept in 047 (recount; 044 estimated 34)
```

**21 files remain, ~301 `[Dd]ecision`-matching lines by the same grep
methodology** (`grep -cE '[Dd]ecision' src/<file>.rs`), largest first:

```
38  src/study_builder.rs
32  src/protocol.rs
29  src/streams.rs
28  src/limits.rs
24  src/result.rs
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

Take one file — `src/study_builder.rs` next, largest remaining, unless a
reason is given to reorder — read every cited decision's body against the
sentence around the citation, and fix what is wrong. Count wrong *numbers*
and false *sentences* separately, per the method below. When you run out of
budget, file the next `tasks/study-designer/<next>` naming exactly which
files remain, the same way this one does.

**None of the four swept files' full-file line count predicted its cost.**
`gatt_extract.rs` (36 lines) took a whole leg's budget; `lib.rs` (41 lines, a
1159-line file) fit in this one with room to spare. Line count of citations is
not a time estimate — file size and how tangled the cross-references are
matter more. Do not assume a small number is cheap.

## Why now

**`check-decision-refs.py` resolves decision numbers only inside `*.md`.** A
wrong number or a stale sentence in a source comment fails no gate and never
has — `embarch-study-designer` is a shared crate (`embarch-api`,
`embarch-core`, `embarch-dev-bench`, `embarch-ui`, `embarch-umbrella` all
depend on it or its output types), so its comments are read from several other
repos' default citation index, which makes a bare `decision N` genuinely
ambiguous here in a way it is not in a leaf repo.

## Method (carried over from `044`/`045`/`046`/`047`, confirmed useful all four times)

**Read the cited decision's body, then read the sentence around the citation,
in that order.** A number that resolves is not evidence the claim holds — the
real yield across five-plus days of these sweeps in other repos, and all four
sweeps in this one, has been prose a decision made false or a citation
pointing at the wrong (but real) decision, not a bare typo. Count the two
categories separately and report both, honestly, even if one or both is zero —
"checked N, found none" is a legitimate result.

**Check cross-repo labelling as the first pass, specifically in this repo.** A
bare `decision N` is same-repo by convention; another repo's decision must
read `<repo> decision N` (e.g. `embarch-dev-bench decision 38`) — general form
still open, owner-reserved, `tasks/doc/055`. `044` found one bare cross-repo
citation, `045` found a second, structurally identical one. `046` and `047`
found none — `047`'s file had zero cross-repo decision citations at all
(`decision 17` in its module doc is an illustrative example of the citation
*form*, not a claim about decision 17, and was left alone on that basis).
Check every bare `decision N` against *this crate's own*
decisions.md/decisions/*.md first regardless.

**Git history of the decisions file is worth checking when a citation's
credit looks off**, though `047`'s two findings resolved without it — both
were confirmed directly against a paired schema-bump table already in
`src/schema_version.rs` (`### v12 — decisions 44 and 50`), which named the
right pair in black and white next to the wrong one in `lib.rs`. When no such
table exists, run `git log --follow -p -- embarch-study-designer/decisions/<file>.md`
and read how the cited paragraph's wording evolved — `046` found two false
sentences this way. Don't stop at "does the decision doc currently say this" —
check whether it once said something the source comment still assumes.

**A wrong number is not always a nearby-digit typo, and not every
over-attribution is a "wrong number."** `045` found three wrong numbers, `046`
found three more of an "established vs. credited" shape, and `047` found two
more of the same shape but in the opposite direction from `046`'s: not a fact
over-credited to a second decision, but the *specific* decision that
established a field (decision 44, `Action::BleSecurity` and the
`StepResult.security_level` field it added) silently swapped for a
*textually-adjacent but wrong* one — decision 50 (`Action::BleUnbond`, the
other half of the same schema-v12 pair, which only ever *mentions* the field
in passing) in one comment, and decision 51 (`dev_bench_log_level`, an
unrelated schema bump entirely) in another. Both read as a plausible slip
between numbers that share a wire-schema table row, not a random typo — check
every citation against what the decision's own text *establishes*, not just
whether the general topic area is adjacent.

## Files already swept (do not re-do)

- `src/schema_version.rs` — done in `044`. ~53 citations. Zero wrong numbers,
  zero false sentences, one unlabelled cross-repo citation (fixed).
- `src/study.rs` — done in `045`. 52 citations read against
  `decisions/seals.md`, `study.md`, `declares.md`, `removed.md`, `ble.md`,
  `gatt.md`, `streams.md`, `protocols.md`, `protocol-exec.md`,
  `payload-meaning.md`, `authoring.md`, plus `embarch-dev-bench` decisions
  18/38/39, `embarch-api` decisions 26(wrong→27/28)/36, `embarch-topology`
  decision 3, and `embarch-decision-reversals.md` row 37. **3 wrong numbers, 0
  false sentences, 1 unlabelled cross-repo citation — all fixed.**
- `src/gatt_extract.rs` — done in `046`. 36 citations read against
  `decisions/gatt-extract.md` (33, 56, 57), `decisions/gatt.md` (31, 32),
  `decisions/seals.md` (18), `decisions/crate.md` (23), and `embarch-ui`
  decision 17 (already correctly labelled). **3 wrong numbers (a design fact
  belonging solely to decision 56 was additionally credited to decision 57, in
  three separate comments — the doc file's own git history shows the fact was
  folded into 56 "the same session", with no connection to 57 at all), 2 false
  sentences (an undercount of decision 57's three failure modes stated as
  "two"; a "byte-for-byte comparability" claim decision 33's own text already
  disclaims as "weaker than this decision claimed" — compare as sets instead),
  0 unlabelled cross-repo citations — all fixed.**
- `src/lib.rs` — done in `047`. 41 citations read against `decisions/crate.md`
  (5, 7, 23), `decisions/limits.md` (15, 46, 49), `decisions/gatt-extract.md`
  (56), `decisions/protocols.md` (58, 59, 61), `decisions/protocol-exec.md`
  (60, 62), `decisions/gatt.md` (31, 32, 36, 41, 53), `decisions/wire.md` (3,
  10), `decisions/versioning.md` (47), `decisions/declares.md` (40),
  `decisions/ble.md` (44), `decisions/removed.md` (54), and
  `decisions/streams.md` (39) — plus `src/schema_version.rs`'s own
  schema-version-to-decision table, used to check two wire-byte test
  comments. **2 wrong numbers (a `StepResult.security_level` wire-byte comment
  credited decision 50 — `Action::BleUnbond` — for a field decision 44
  actually established, now decision 44; a discriminant-pinning comment for
  the same schema-v12 pair read "decisions 50/51" where 51 is
  `dev_bench_log_level`, an unrelated decision, now "decisions 44/50"), 0
  false sentences, 0 unlabelled cross-repo citations (there were none in this
  file at all) — both fixed.**

## Done when

- [ ] One named file (`src/study_builder.rs`, unless a reason is given to
      reorder) fully swept, wrong numbers and false sentences counted
      separately.
- [ ] Cross-repo citations in it carry their repo name.
- [ ] A follow-up task filed naming the files that remain (or, if this closes
      out `src/`, saying so and closing the sweep).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/study-designer-*` fragment.

## Reserve, for planning

`embarch-study-designer/spec.md` and `open.md` were both inside the last 10%
of their caps as of `045`'s dispatch, with both compaction tasks (`032`, `026`)
blocked, `In flux: yes` per `046`'s dispatch note; `047` re-checked
`scripts/check-doc-size.py` fresh and found no new reserve entries for this
scope, touching neither file. Check fresh again rather than trusting this
number — a comment sweep should not need either file regardless. If this
sweep turns up a question worth recording, file it as
`tasks/study-designer/<next>` rather than adding to `open.md`.
