# 039 — Repoint `embarch-study-designer` source doc comments from `interfaces/types.md` to `interfaces/result-types.md`

**State:** done
**Source:** `tasks/study-designer/038`'s citation sweep, 2026-09-13 — found and deliberately left
unfixed, since that task's own `## Not in scope` excluded any change to this sub-project's source.
**Scope:** study-designer
**Hardware:** none — doc-comment text only, no logic change.
**Owner:** no

## What

`038` moved `Provenance`, `StudyResult`, `StepResult` and `Outcome`'s field documentation out of
`embarch-study-designer/interfaces/types.md` into the new `embarch-study-designer/interfaces/result-types.md`,
verbatim. A handful of this crate's own rustdoc comments cite the old path for exactly that moved
content, by bare filename (`interfaces/types.md`, no link syntax — this is a `#![no_std]` crate, doc
comments, not Markdown links). Confirmed by grep at `038`'s claim commit:

- `README.md:23` — `| \`result\` | \`StudyResult\`, \`StepResult\`, \`Outcome\` (interfaces/types.md) |`
- `src/result.rs:1` — module doc: `//! \`StudyResult\`/\`StepResult\`/\`Outcome\` — interfaces/types.md.`
- `src/result.rs:23` — `Provenance` field doc, "(decision 40, interfaces/types.md)"
- `src/result.rs:35` — `Provenance` type doc, "(decision 40, interfaces/types.md)"
- `src/result.rs:89` — `VersionOverride` type doc, "(decision 40, interfaces/types.md)"
- `src/limits.rs:50` — `MAX_VERSION_OVERRIDES` doc: "`Provenance.overrides` (decision 40, interfaces/types.md)"

Repoint each to `interfaces/result-types.md`. Every other `interfaces/types.md` mention in this
crate's source (`src/study.rs`, `src/ffi.rs`, `src/study_builder.rs`, `src/gatt.rs`, `src/lib.rs`)
is about `Study`/`Step`/`Action`/GATT content that did not move — checked at `038`'s claim commit and
confirmed correct as-is. Recheck against `main` at claim time in case another unit has landed
between, rather than trusting this list blind.

## Why now

`038`'s own "citation problem" section names this as the class of defect a verbatim split creates
and `check-decision-refs.py`/`check-links.py` cannot see (the path still resolves; it just no longer
holds the cited content). `038` chose not to fix it in the same unit because its `## Not in scope`
explicitly excluded any change to this crate's source, to keep that unit doc-only with a
predictably-empty code branch. This task is the deferred half.

## Dispatch note (supervisor, leg 109)

**In reserve for `study-designer`** (last 10% of cap, still writable): `spec.md` 9350/10240 B
(890 B left), `open.md` 4659/5120 B (461 B left). `interfaces/types.md` is now **out** of reserve
(73.2%) after `038`'s split. If your work pushes a file into reserve or leaves one there that
nothing has filed, file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit
(`tasks/README.md` has the shape) — recording the debt, not paying it.

This unit should not come near any of them: it is six doc-comment lines in your own crate's source
plus a `changelog.d/` fragment.

**Scope correction carried forward from `038`.** That task's "not in scope: any change to this
sub-project's source" was the supervisor's wording error — it meant *no logic change*. Doc comments
in your own repo are squarely yours to fix, which is why this task exists at all. Fix all six; do
not file a third task for them.

## Done when

- [x] The six sites above repointed to `interfaces/result-types.md`.
- [x] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green in
      `embarch-study-designer` (doc comments only, but confirm nothing else moved under this task).
- [x] `changelog.d/` fragment dropped.

## Shipped

Repointed all six sites (`README.md:23`, `src/result.rs:1,23,35,89`, `src/limits.rs:50`) from
`interfaces/types.md` to `interfaces/result-types.md`. Re-grepped at claim time: the list from `038`
still matched exactly — no other unit had landed in between. Every remaining `interfaces/types.md`
mention in this crate (`README.md:15,22`, `src/lib.rs:11`, `src/study.rs` ×7, `src/ffi.rs` ×3,
`src/gatt.rs:22`, `src/study_builder.rs:645`) is about `Study`/`Step`/`Action`/`Requirements`/GATT
content that did not move — confirmed by reading each site's surrounding doc comment, not just the
grep hit. `cargo build`, `cargo test` (116 + 9 tests), `cargo clippy --all-targets -- -D warnings`
all green, no other diff. `changelog.d/study-designer-repoint-result-types-comments.fixed.md`
dropped. `check-docs.py`: all 11 checks green, including `check-doc-size.py` — this unit did not
touch `spec.md`/`open.md` (both in reserve per the dispatch note) or push any file into reserve, so
no compaction task filed.
