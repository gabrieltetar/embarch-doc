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

- [x] Every source-comment `design.md` citation in `embarch-ui` is repointed at the correct
  `decisions.md` / `decisions/<topic>.md` path, in the settled form — except the two listed below,
  which match no standing decision.
- [x] Any comment whose claim matches no standing decision is listed here rather than repointed at a
  guess.
- [x] `cargo test` and `clippy --all-targets -- -D warnings` stay clean (comments only, so this was
  free).

## Two citations that match no standing decision (left unrepointed)

Both claim "Core being unreachable is an expected, renderable state" as `decision 5`'s own
"confirmed" reasoning. `embarch-ui decision 5` (`decisions/wiring.md`) is real but is about
routing every hardware-adjacent call over HTTP+Bearer to Core — it says nothing about Core's
unreachability being expected or "confirmed." No other `embarch-ui` decision states this either
(checked `topology-tab.md`, `trace-view.md`, `shape.md`, `shell.md` bodies, not just headings).
Left as `design.md`-citing prose rather than repointed at a guess, per this task's own instruction:

- `src/logs.rs:58` — `// here too (design.md §3 decision 5's own "confirmed" reasoning)`
- `src/snapshot.rs:73-75` — `/// renderable state (§ design.md decision 5's own "confirmed"
  reasoning: Core down is not a crash)`

## Also found, out of scope for this task (repointed or noted separately)

Several `design.md`-adjacent citations turned out to be pointing at the *wrong* decision number
once the cited decision's body was actually read (per this task's own warning, taking `core/008`
as precedent) — all now fixed in this unit:

- `src/main.rs`: `embarch-topology decision 14` → `embarch-core decision 25` (the retired
  `GET /enroll` page and its `hw_lock`-bypass fix — topology's decision 14 is the human-enrollment
  scope call, unrelated); `embarch-outpost decisions 9, 16` → `embarch-outpost decision 18` (named/
  timed as two independent booleans lives in `decisions/clocks.md` 18, not manifest/hardware).
- `src/study_designer.rs`: `embarch-ui decision 15` → `decision 14` (project-open state, twice);
  `embarch-study-designer decision 34` → `decision 35` (the registry itself, not the authoring UI);
  `... decision 39` (app.js, vendor services) → `decision 41`; `... decision 41` (app.js,
  `target_name`) → `decision 43`; and one bare `(design.md §3 decision 14)` in a section banner
  that was actually about the auto-declared transcript tap → `decision 15`.

Also two references to a `milestone-1.md` file that no longer exists in `embarch-ui`
(`assets/style.css` §4.3/§4.4, `assets/app.js` §4.5/§4.7) — left untouched since this task's scope
is `design.md` citations specifically, and there's no obvious decisions.md mapping for a
milestone-tracking doc. Dropped separately to `embarch-doc/inbox/` for whoever owns that judgment
call.

## Explicitly not this task

Whether `check-decision-refs.py` should scan source comments as well as `*.md`. That is a
doc-tooling question about a reserved script, so it is the owner's — file it as an `inbox/` drop if
this unit strengthens the case for it, and do not edit `scripts/`.
