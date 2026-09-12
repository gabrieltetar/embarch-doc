# 033 — Source comments across `embarch-ui` cite a pre-split `design.md` that does not exist

**State:** claimed by agent/ui/033-design-md-comments, 2026-09-12
**Source:** `inbox/ui-design-md-comment-citations.md`, dropped by `ui/032`'s siblings check,
2026-09-12. Out of scope there — `ui/032` fixed only shipped/rendered strings in `assets/`, not
source comments — so it was reported rather than widened into that unit.
**Scope:** ui
**Hardware:** none — comments in `assets/*.js`, `assets/*.css` and `src/*.rs`, plus the docs they
point at. Re-checked at intake: no board, no running UI, no live Core.
**Owner:** no

## What

`embarch-ui` split its decisions into `decisions.md` + `decisions/*.md` topic files, but dozens of
`//`, `/* */` and `<!-- -->` comments across the repo still cite the old `design.md` path — some
naming `embarch-ui/design.md`, others `embarch-outpost/design.md` or
`embarch-study-designer/design.md`, both of which have also split. Not user-facing, so lower
priority than `ui/032`'s dialog fix, but they mislead whoever edits that file next.

This is the same defect class `core/008`, `umbrella/043` and `api/052` already cleaned up in their
own repos' source comments, and the settled citation form comes from those units: bare
`decision N` for a same-repo citation, `` `<repo>` decision N `` cross-repo.

Non-exhaustive grep hits (2026-09-12): `assets/app.js` (dozens), `assets/style.css` (several),
`src/main.rs`, `src/study_designer.rs`, `src/trace.rs`, `src/logs.rs`, `src/snapshot.rs`,
`src/config.rs`.

## Why now

`check-decision-refs.py` walks only `*.md` under the repo root — confirmed while working `ui/032` —
so none of these citations has ever been checked by anything. They are exactly as invisible to the
gate as the shipped HTML string `ui/032` fixed was, and there are far more of them.

**Verify each target before repointing it.** `core/008` is the precedent and the warning: a
heading-only check rejected a citation that the decision's *body* made correct. Read the body of
every decision you cite, and if a comment's claim matches no decision at all, say so in the task
rather than inventing a plausible number.

## Done when

- Every source-comment `design.md` citation in `embarch-ui` is repointed at the correct
  `decisions.md` / `decisions/<topic>.md` path, in the settled form.
- Any comment whose claim matches no standing decision is listed here rather than repointed at a
  guess.
- `cargo test` and `clippy --all-targets -- -D warnings` stay clean (comments only, so this should
  be free).

## Explicitly not this task

Whether `check-decision-refs.py` should scan source comments as well as `*.md`. That is a
doc-tooling question about a reserved script, so it is the owner's — file it as an `inbox/` drop if
this unit strengthens the case for it, and do not edit `scripts/`.
