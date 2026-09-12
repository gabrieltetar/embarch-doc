# 037 — `embarch-ui` source comments cite a `milestone-1.md` that does not exist

**State:** claimed — leg 097, 2026-09-12.

**Doc-size reserve for `ui` (supervisor, leg 097):** no `embarch-ui/` file is in reserve. Nothing to
file. If your work pushes one in, file `tasks/ui/<NNN>-compact-ui.md` in the same commit.
**Source:** `inbox/ui-milestone-1-md-comment-citations.md`, written by `ui/033`'s worker while working
`tasks/ui/033` (2026-09-12), which was itself scoped to `design.md` citations only.
**Scope:** ui
**Hardware:** none
**Owner:** no

## Method note from the supervisor (leg 096)

`ui/033`'s precedent applies and is the reason this is not a cosmetic task: read each cited
**decision body**, not its heading, before repointing anything. That is what turned `ui/033` from a
path sweep into seven corrected decision numbers. Where no standing decision says what a comment
claims, **do not invent a number** — list the comment in this task file and leave it, the way
`ui/033` left `src/logs.rs:58` and `src/snapshot.rs:73-75` (now `tasks/ui/034`). A wrong renumbering
is worse than the stale path it replaces.

## What

A handful of `embarch-ui` source comments cite `embarch-doc/embarch-ui/milestone-1.md` at a
section number (`§4.3`, `§4.4`, `§4.5`, `§4.7`) — a file that does not exist anywhere in
`embarch-doc`. Found alongside the `design.md` citations `ui/033` fixed, but left untouched there
since that task's scope was `design.md` specifically, and there's no obvious 1:1 mapping from a
milestone-tracking doc's section numbers onto today's `decisions.md` / `decisions/*.md` split —
that judgment call belongs to whoever scopes the follow-up task.

Known hits (non-exhaustive, not re-grepped for this drop):

- `assets/style.css:7-8` — `embarch-doc/embarch-ui/milestone-1.md §4.3` and (further down)
  `§4.4 onward`
- `assets/app.js` — `// --- Enroll tab (milestone-1.md §4.5) ---` and
  `// --- Debug tab (milestone-1.md §4.7) ---`

## Why it matters

Same defect class as the `design.md` citations: `check-decision-refs.py` only resolves decision
numbers in `*.md` under the repo root, so a stale file-plus-section citation in a source comment
is invisible to any gate and just misleads the next reader who goes looking for
`milestone-1.md`.

## Suggested next step

Either repoint each citation at whatever doc now covers that ground (if one exists — `spec.md`?
a `decisions/shell.md`-style entry?), or drop the citation to a plain historical note ("built in
the shell's first milestone") if no live doc says the same thing today. Not filed as a `tasks/ui/`
unit here since it needs that scoping decision made first.
