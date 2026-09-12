# 037 — `embarch-ui` source comments cite a `milestone-1.md` that does not exist

**State:** done — leg 096, 2026-09-12, `agent/ui/037-milestone-1-comments`

**Resolution:** re-grepped `embarch-ui` for `milestone-[0-9]` and found nine hits (the two known
plus seven not previously listed): `Cargo.toml:20`, `assets/style.css:7-8,10,413,469,539`,
`assets/index.html:644`, `assets/app.js:428,610,831`. Repointed at a standing decision body where
one exists and says the same thing:

- `Cargo.toml:20` — decision 5 was already cited alongside the milestone reference; dropped the
  dead `milestone-1.md §4.1` clause, kept `decision 5`.
- `assets/style.css:7-8` — decision 8 was already cited alongside `§4.3`; dropped the milestone
  clause, kept `decision 8`. The `§4.4 onward` sentence about per-tab classes arriving as each tab
  ships states no decision's content (it's a build-order note); dropped the citation, kept the
  prose.
- `assets/style.css:469` and `assets/app.js:610` (Debug tab) — decision 7 (`decisions/debug-tab.md`)
  is exactly "the Debug tab is a new suite-wide capability"; cited it in place of the milestone
  reference.
- `assets/style.css:413`/`assets/app.js:428` (Enroll tab drag-and-drop) and `assets/style.css:539`/
  `assets/app.js:831` (Study Designer tab CSS/JS section banners) and `assets/index.html:644`
  ("stop server", not wired yet) — no standing decision states what any of these three comments
  claimed (checked `decisions.md`'s index and every topic file it points at: `shell.md`,
  `debug-tab.md`, `study-designer.md`, `wiring.md`, and `decisions.md` itself have no entry for an
  Enroll-tab decision or a "not wired yet" footer button). Per the method note, did not invent a
  number — dropped the `milestone-1.md` citation and left a plain in-place label instead.

No comment was left citing `milestone-1.md`; a second full re-grep after editing confirms zero
hits for `milestone-[0-9]` anywhere in the `embarch-ui` tree.

**Also found, out of scope, dropped to inbox:** `Cargo.toml:6,14,19` still cite a `design.md` that
also does not exist (`ui/033`'s target file) — `ui/033` was scoped to `design.md` and appears to
have missed `Cargo.toml`'s own comments. Not touched here since this task's scope is `milestone-1.md`
specifically; see `inbox/ui-cargo-toml-design-md-citations.md`.
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
