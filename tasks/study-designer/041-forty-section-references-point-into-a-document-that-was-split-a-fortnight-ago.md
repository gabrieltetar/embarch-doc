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

- [ ] Every one of the 40 is classified, and the classification is stated in the task file: **(a)
      resolves correctly today** (a `spec.md` §N that really is that section — leave it), **(b) dead**
      (names a section of no live document), or **(c) ambiguous** (could be read as a live `spec.md`
      section but was written about the old `design.md`).
- [ ] (b) and (c) are repaired. **Prefer naming the file over inventing a section number**: these
      interface files have no numbered headings, so any `§N` written into one is a fabrication, and
      `ui/044` set the precedent by dropping the number rather than replacing it. Where the content
      genuinely lives in a numbered `spec.md` section, cite that section.
- [ ] Where a citation names content that moved in the 2026-09-13 split, the **file** is corrected
      too — `limits.md:24` needs both halves.
- [ ] `check-docs.py` green. Note that it was **already green** with all 40 of these standing:
      `check-links.py` checks link targets, not section anchors, so nothing here is a regression it
      can catch, and a green run proves nothing about this task. Say so when you report.
- [ ] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.

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
