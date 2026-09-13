# 039 — Repoint `embarch-study-designer` source doc comments from `interfaces/types.md` to `interfaces/result-types.md`

**State:** open
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

## Done when

- [ ] The six sites above repointed to `interfaces/result-types.md`.
- [ ] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green in
      `embarch-study-designer` (doc comments only, but confirm nothing else moved under this task).
- [ ] `changelog.d/` fragment dropped.
