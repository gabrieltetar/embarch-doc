# 044 — Repoint a `StreamRef` citation from `study-designer/interfaces/types.md` to `result-types.md`

**State:** done
**Source:** `tasks/study-designer/038`'s suite-wide citation sweep, 2026-09-13 — found in
`embarch-ui`, a repo outside that task's ownership, so it was dropped to `inbox/` rather than fixed
in place, and drained into this file by the supervisor (leg 108) in `study-designer/038`'s fold.
**Scope:** ui
**Hardware:** none — a doc-comment text edit, no logic change.
**Owner:** no

## What

`embarch-study-designer/interfaces/types.md`'s `Results` section — holding `Provenance`,
`StudyResult`, `StepResult` and the `StreamRef` row — moved verbatim into a new
`embarch-study-designer/interfaces/result-types.md` in `tasks/study-designer/038` (2026-09-13).
`embarch-ui/src/study_designer.rs:780` cites the old path for content that moved:

```
/// `limits::MAX_STREAM_NAME_LEN` — how long a `StreamTap`/`StreamRef`
/// name may be (`embarch-study-designer/interfaces/types.md` §4.8), also the file
/// name a stream becomes under a study's `streams/` directory. Served
```

`StreamRef` is `Results` content and moved, so repoint this citation to
`embarch-study-designer/interfaces/result-types.md`.

**The `§4.8` in that same citation is a second, older defect and it is not what this task is
about.** `interfaces/types.md` carries no numbered headings and has not since the 2026-09-02 split,
so `§4.8` resolved to nothing before this move and would have resolved to nothing without it. Fix it
or leave it at this task's discretion — but if you fix it, say so, because that is a different
defect with a different cause and conflating the two is how a citation sweep's result stops meaning
anything.

**Checked and confirmed unaffected, so do not touch it:** `embarch-ui/src/study_designer.rs:1524`,
which cites `embarch-study-designer/interfaces/types.md §4.3` for `Uuid`'s raw-array `Serialize`
form. That content is in the `Action`/GATT section, which did not move.

## Why now

`tasks/doc/044` records the class: **a verbatim split is the one move `check-decision-refs.py` and
`check-links.py` cannot see.** The path still resolves — it just no longer holds the cited content,
so the gate stays green while a reader following this citation from `embarch-ui` lands on `types.md`
and does not find `StreamRef` there. Nothing mechanical will ever surface this; it has to be swept by
hand at the moment of the split, which is what `study-designer/038` did.

## Done when

- [x] `embarch-ui/src/study_designer.rs:780`'s citation repointed to
      `embarch-study-designer/interfaces/result-types.md`.
- [x] `cargo build`, `cargo test`, and `cargo clippy --all-targets -- -D warnings` green in
      `embarch-ui`. It is a comment-only change, so this is confirmation rather than risk — but
      confirm it, because a comment edit inside a doc-comment block is exactly the kind of thing that
      breaks a build without reading oddly.
- [x] `changelog.d/` fragment dropped **only if something reader-visible changed**. A citation
      repoint inside a source doc comment is usually not; say which way you judged it.

      Judged: not reader-visible. This is an internal source doc-comment citation repoint with no
      externally observable behavior or documented-surface change; no fragment dropped.

## What shipped

`embarch-ui/src/study_designer.rs:780`'s citation now reads
`` `embarch-study-designer/interfaces/result-types.md` `` (was
`` `embarch-study-designer/interfaces/types.md` §4.8 ``).

**`§4.8` fixed, not left:** dropped rather than carried forward or replaced with a new section
number, per the dispatch note's guidance. It was dead before this move (`interfaces/types.md` has had
no numbered headings since the 2026-09-02 split) and stays dead after it — `result-types.md` is a
split file with no numbered headings either, so writing a fresh `§N` there would have been a new
fabricated citation rather than a repaired one. This is a second, distinct defect from the path move
and is called out separately per the task's own instruction not to conflate the two.

`embarch-ui/src/study_designer.rs:1524`'s `types.md §4.3` citation (`Uuid`'s raw-array `Serialize`
form) was left untouched, as instructed — that content is in the `Action`/GATT section, which did not
move.

Gate: `cargo build`, `cargo test` (101 passed, 4 ignored, plus 2 in `element_ids.rs`), and
`cargo clippy --all-targets -- -D warnings` all green in `embarch-ui`. `check-docs.py` (11/11),
`check-client-names.py`, and `check-ownership.py --scope ui` (both repos) all green.

## Dispatch note (supervisor, leg 109)

**Nothing in `embarch-ui`'s docs is in reserve** — `check-doc-size.py --pressure` lists no `ui` file
in the last 10% of its cap, so you have headroom. The standing rule still applies: if your work
pushes a `ui` doc into reserve, file `tasks/ui/<NNN>-compact-ui.md` in the same commit
(`tasks/README.md` has the shape).

**On the `§4.8` half:** your discretion, as written above. If you fix it, the right form is to drop
the section reference rather than invent a new one — `result-types.md` is a split file with no
numbered headings either, so any `§N` you write there would be a fresh fabricated citation. Say
which way you went in the task file.

## Not in scope

- `tasks/study-designer/039`, which covers the equivalent stale citations inside
  `embarch-study-designer`'s **own** source (`README.md:23`, `src/result.rs:1,23,35,89`,
  `src/limits.rs:50`). Different repo, different owner, already filed.
- Any change to `embarch-study-designer`, `embarch-doc`'s shared docs, or the split itself.
