# 041 — Forty `§N` references in this sub-project's docs point into a `design.md` that stopped existing on 2026-09-02

**State:** claimed — leg 110, 2026-09-13.
**Doc-size reserve (supervisor, leg 110):** two files of yours are in reserve and both are already
filed against a **blocked** compaction task, so plan around them rather than discovering them:
`embarch-study-designer/spec.md` 9,350/10,240 B (**890 B left**, `tasks/study-designer/032`) and
`embarch-study-designer/open.md` 4,659/5,120 B (**461 B left**, `tasks/study-designer/026`). This
unit should be byte-negative or neutral in both — dropping a dead `§N` shortens a line — so do **not**
compact either as part of this unit. If your work nonetheless pushes any file into reserve or leaves
one there unfiled, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit
(`scripts/check-task-numbers.py --next study-designer` for the number; never `ls | tail`).
**Source:** the `embarch-reviewer` on `ui/044`, 2026-09-13, as a flagged-not-found aside: it noticed
`interfaces/limits.md:24` still cites `§4.8` for `StreamTap.name`/`StreamRef.name`, the same dead
section number `ui/044` had just dropped from `embarch-ui`'s side of the identical citation. The
supervisor (leg 109) then counted the class rather than filing the one line.
**Scope:** study-designer
**Hardware:** none — prose citations only, no logic change.
**Owner:** no

## What

`grep -rno '§[0-9]' embarch-study-designer/` in `embarch-doc` returns **40 hits across 11 files**:

| file | hits |
|---|---|
| `interfaces/limits.md` | 20 |
| `decisions/crate.md` | 6 |
| `decisions/wire.md` | 4 |
| `decisions/study.md` | 3 |
| `decisions.md`, `decisions/ci.md`, `decisions/declares.md`, `decisions/protocols.md`, `decisions/streams.md`, `interfaces/result-types.md`, `interfaces/types.md` | 1 each |

Most are `§4.x` — `§4.1`, `§4.3`, `§4.3a`, `§4.5`, `§4.7`, `§4.8` — and they are the numbering of the
**monolithic `design.md` this sub-project was split out of on 2026-09-02**. That file is gone.
`interfaces/types.md`, `interfaces/result-types.md`, `interfaces/limits.md` and
`interfaces/gatt-types.md` carry **no numbered headings at all**, so every `§4.x` naming interface
content resolves to nothing.

**The trap, and it is why this needs judgement per site rather than a `sed`.** `spec.md` *does* have
numbered sections, and its `§4` is *"What a study carries"* — genuinely adjacent to what most of
these citations are about. So a reader following `§4.8` lands on a section that looks like the right
neighbourhood and has no eighth subsection, and cannot tell whether the reference is stale, wrong, or
to something deleted. A citation that fails cleanly is cheaper than one that half-succeeds.

Worked example, from the reviewer, both halves confirmed by the supervisor:

```
| `MAX_STREAM_NAME_LEN` | 32 | `StreamTap.name`, `StreamRef.name` (§4.8) | [assumed] |
```
`interfaces/limits.md:24`. `StreamTap` is in `interfaces/types.md`; `StreamRef` moved to
`interfaces/result-types.md` under `study-designer/038` yesterday. **One citation, two files, and a
section number belonging to neither.**

And `decisions/streams.md:31` is the fully-spelled form of the same defect:
`Shapes: [../interfaces/types.md](../interfaces/types.md) §4.8` — the link resolves, the section
does not exist, and half the shapes it promises are now in `result-types.md`.

## Done when

- [x] Every one of the 40 is classified, and the classification is stated in the task file: **(a)
      resolves correctly today** (a `spec.md` §N that really is that section — leave it), **(b) dead**
      (names a section of no live document), or **(c) ambiguous** (could be read as a live `spec.md`
      section but was written about the old `design.md`).

  **Classification (leg 110, 2026-09-13), 40/40 accounted for:**

  **(a) resolves correctly today — 6.** All resolve into a document other than the dead `design.md`,
  none needed touching: `decisions.md:7` §3 (narrates the historical `design.md`→`decisions.md` move,
  same idiom `embarch-core/decisions.md:7` and `embarch-dev-bench/decisions.md:7` already use —
  content, not a live pointer, per `DOC-CONVENTIONS.md`'s "a dated entry that narrates a move");
  `decisions/ci.md:45` §10 (`../../../embarch-fleet/protocol.md` §10, the gate); `decisions/crate.md:38`
  §2 (`DOC-PROTOCOL.md` §2, repo layout); `decisions/declares.md:37` §4a
  (`embarch-dev-workflow.md` §4a); `interfaces/result-types.md:3` §3 (`DOC-COMPACTION.md` §3, four
  files per sub-project); `interfaces/types.md:33` §3a (`suite/studies-guide.md` §3a — a real, still-live
  suite-level section, unrelated to any `design.md`).

  **(c) ambiguous — 5.** Every one is a *bare* `§N` (no decimal) naming this crate's own doc implicitly,
  landing on one of spec.md's real top-level numbers (1, 4, 7) with the wrong content behind it — the
  exact trap this task describes: `decisions/crate.md:15` §4 (serde-derived types — spec §4 is "What a
  study carries", a narrower table, not the whole type model); `decisions/crate.md:21` §7 (dev-bench
  runtime undecided — spec §7 is "Constants"); `decisions/crate.md:38` §4 (the type model, same
  mismatch as the first); `decisions/wire.md:37` §1 (a 10–100 kHz power-profiling rate — spec §1 is
  "What it is", which names power profiling as a purpose but states no rate);
  `interfaces/limits.md:64` §7 (a retired constant's "stack-safety risk" — again spec §7 is
  "Constants", not risks).

  **(b) dead — 29.** Every remaining hit: either a bare or decimal `§N` naming a document (this crate's
  own, or another repo's) whose split predates or postdates this one, with **no** live section at that
  number, and none confusable with a real `spec.md` number the way the five (c)s are. Full list:
  `decisions/crate.md:15` (§4.7, §5.2); `decisions/protocols.md:23` (§4.9); `decisions/streams.md:31`
  (§4.8); `decisions/study.md:45` (§5.1), `:57` (§4.1, §3.6); `decisions/wire.md:11` (§4), `:15` (§5),
  `:27` (§4); `interfaces/limits.md:18` (§4.7), `:19,20,21` (§3 ×3, all cross-repo), `:22` (§4.5),
  `:23,24,25,26,27` (§4.8 ×5), `:28,29` (§4.3a ×2), `:34,35,36,37` (§4.8a ×4), `:38` (§4.3b), `:41`
  (§3 and §4.9) — nineteen of the twenty `limits.md` hits, the twentieth (line 64's §7) being (c).

- [x] (b) and (c) are repaired. **Prefer naming the file over inventing a section number**: these
      interface files have no numbered headings, so any `§N` written into one is a fabrication, and
      `ui/044` set the precedent by dropping the number rather than replacing it. Where the content
      genuinely lives in a numbered `spec.md` section, cite that section.

  None of the 40 turned out to belong in a numbered `spec.md` section — spec.md's own 1–7 have no
  subsections, so every decimal hit failed cleanly and every bare hit was the (c) trap. Repair applied
  per rule, matching `embarch-dev-bench` decision 47's precedent (own repo, discovered mid-task, not
  re-derived from scratch): resolve to the owning decision where one exists (bare number, own-repo;
  `<repo> decision N`, cross-repo — `embarch-dev-bench decision 7/18/27`, `embarch-core decision 35`);
  name the live document directly where the content moved to one and no decision owns it
  (`interfaces/{types,decoders,taps,gatt-types,eap,result-types}.md`, `embarch-core/interfaces.md`,
  `embarch-core/interfaces/{hardware,studies}.md`, `embarch-api` decision 1); or drop the section
  pointer outright where neither applies (`decisions/wire.md:37`'s power-profiling rate,
  `interfaces/limits.md`'s `StreamRecord.bytes`/`StreamChunkBatch.records` rows, `crate.md:21`'s
  runtime aside, `limits.md:64`'s stack-safety aside). One citation (`decisions/wire.md:27`) narrates
  a past design review's quote from `embarch-core`'s own then-monolithic `design.md` — kept as
  history per the same narrates-a-move exception, with the wrong current filename (`decisions.md`)
  corrected to the accurate historical one (`design.md`) plus where that content lives now
  (`embarch-core/interfaces.md`).

  **One correction to this task's own worked example.** `interfaces/limits.md:24`'s `StreamTap` is
  **not** in `interfaces/types.md` as this task file first said — it's fully defined in
  `interfaces/taps.md` (confirmed via `git log`: `taps.md` has held it since the 2026-09-02 split,
  never lived in `types.md`). `types.md` only carries `Study.streams: Vec<StreamTap>` as a field
  reference. Fixed to `taps.md` for `StreamTap.name`, `result-types.md` for `StreamRef.name` (that
  half was accurate).

  **Not fixed, and not filed, on purpose:** four unrelated `spec.md §N` citations found in this
  repo's own `src/*.rs` while checking whether the code repo needed changes (`src/sample.rs:82`,
  `src/gatt_extract.rs:10`, `src/streams.rs:428`, `src/study.rs:717`) all resolve correctly against
  spec.md's real 1/3/7 sections — checked, not touched, nothing to file.

- [x] Where a citation names content that moved in the 2026-09-13 split, the **file** is corrected
      too — `limits.md:24` needs both halves.

  Done — see above. Same pattern applied wherever a citation's content had moved to a specific
  interface file rather than staying at a decision (`interfaces/limits.md`'s `MAX_STREAM_NAME_LEN`,
  `MAX_CSV_ROW_LEN`, `MAX_DISCOVERED_SERVICES`/`MAX_CHARS_PER_SERVICE`/`MAX_GATT_CSV_ROW_LEN`,
  `MAX_DECODER_NAME_LEN`/`MAX_STRUCT_*`, and `decisions/streams.md:31`'s `Shapes:` link, which pointed
  at `types.md` for content — `StreamTap`/`StreamSource`/`StreamEncoding` — that has only ever lived
  in `taps.md`).

- [x] `check-docs.py` green. Note that it was **already green** with all 40 of these standing:
      `check-links.py` checks link targets, not section anchors, so nothing here is a regression it
      can catch, and a green run proves nothing about this task. Say so when you report.

  Confirmed still green after the fix (11/11 checks). Restating the caveat as instructed: green here
  never meant these 40 were fine, before or after — `check-links.py` never saw a bare `§N` at all.

- [x] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.

  Filed (`study-designer-dead-section-refs.fixed.md`). Judged reader-visible: every one of these 40
  is prose a reader can click through (or fail to) today, in files a reader actually opens
  (`decisions/*.md`, `interfaces/limits.md`) — even though "where a citation points" rather than "what
  the docs say" changed, a reader following one of these 29 dead links before this unit landed
  somewhere and now lands somewhere real (or nowhere, cleanly, rather than in the `spec.md` §4 trap).
  That is a reader-facing fix, not internal bookkeeping.

## Why now

`tasks/doc/044` records the class — a verbatim split is the one move `check-decision-refs.py` and
`check-links.py` cannot see. This is its oldest instance in the suite: the 2026-09-02 split predates
the class being named at all, so these forty were never swept, and every sweep since has been aimed
at *path* citations rather than *section* ones. The suite has now paid for the same defect four times
in a fortnight (`core/050`, `dev-bench/030`, `study-designer/039`, `ui/044`), each time one repo at a
time.

## Not in scope

- **`embarch-ui/src/study_designer.rs:1524`**, which cites `types.md §4.3` for `Uuid`'s raw-array
  `Serialize` form — same defect class, different repo, filed separately as `tasks/ui/045`.
- Any change to what the docs *say*. This is about where they point. If you find a citation whose
  content is also wrong, file it rather than fixing it — conflating a dead section number with a
  false claim is how a sweep's result stops meaning anything.
- Renumbering or adding numbered headings to the interface files. That is a `DOC-CONVENTIONS.md`
  question and is not settled by this task.
