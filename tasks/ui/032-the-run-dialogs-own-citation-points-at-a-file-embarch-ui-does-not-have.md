# 032 — The run dialog cites `embarch-ui/design.md`, and `embarch-ui` has no `design.md`

**State:** claimed by agent/ui/032-run-dialog-citation, 2026-09-12 01:32
**Source:** `ui/031`'s reviewer, 2026-09-12, which verified the dialog string for that unit and
found the citation inside it wrong. Out of scope there — that unit changed no code and the reviewer
reads diffs for decision contradictions — so it was reported rather than fixed.
**Scope:** ui
**Hardware:** none — a string in `assets/index.html` and the docs it points at.
**Owner:** no

## What

`embarch-ui/assets/index.html`'s run-check dialog (around line 350) reads:

> "Reflashing is deliberately not offered here — see `embarch-ui/design.md` §3 decision 11. Build
> and flash through `embarch-api run-study --reflash`, which owns the project config and the build
> machinery."

**There is no `embarch-ui/design.md`.** Decision 11 lives in
`embarch-ui/decisions/study-designer.md`, reached through `embarch-ui/decisions.md`. The `design.md`
path is a survival from before this sub-project's decisions were split into topic files — the same
class `core/008`, `umbrella/043` and `api/052` have each cleaned up in source comments.

Two things separate this one from those:

1. **It ships.** Every other instance of this defect has been a comment or a doc line, read by
   whoever is editing that file. This one is rendered to a user, in a dialog, at the exact moment
   they wondered why they cannot reflash — so the citation is the whole value of the sentence and
   it sends them nowhere.
2. **The settled citation form applies** (`api/052`, adopted by `umbrella/043` and `core/008`): bare
   `decision M` same-repo, `` `<repo>` decision M `` cross-repo. A user-facing string is not a source
   comment, so the right form here needs a judgement call — a reader in a browser cannot follow
   "decision 11" without a path, but the path must be one that exists.

## Why now

`ui/031` just landed a doc bullet whose entire content is "this dialog string was checked". Leaving
a wrong path inside the string that was checked is the worst possible resting state: the doc now
asserts verification, and the thing verified has a dead reference in it.

Check for siblings while you are in there — `index.html` is likely not the only shipped string
citing a pre-split path.

## Done when

- [x] The dialog cites a path that resolves. Decided: user-facing strings cite `embarch-ui/decisions.md`
      (the index), not the topic file — same reasoning as `DOC-CONVENTIONS.md`'s link-the-index rule
      (a topic file can move an entry between missions without renumbering; the index is what a
      splitter maintains, so it survives). Fixed `assets/index.html:350` (`embarch-ui/design.md` §3
      decision 11 -> `embarch-ui/decisions.md`, decision 11).
- [x] Any sibling strings in `assets/` citing a pre-split path are fixed in the same unit. Found one
      more rendered (non-comment) instance: `assets/index.html:517`'s trace-tab note cited
      `embarch-outpost/design.md` §3 decision 10 — also a repo with no `design.md` (it too has
      already split into `decisions.md` + `decisions/*.md`). Fixed to `embarch-outpost/decisions.md`,
      decision 10. Everything else matching `design.md` in `assets/` and `src/` is inside a `//` or
      `/* */` comment or an HTML `<!-- -->` comment — never rendered — so left alone as out of this
      unit's "ships to a user" scope; those are the same class `core/008`/`umbrella/043`/`api/052`
      already clean up in source comments, and there are many (dozens across `app.js`,
      `study_designer.rs`, `main.rs`, `snapshot.rs`, `trace.rs`, `logs.rs`, `config.rs`,
      `style.css`) — worth a dedicated task, not folded into this one silently.
- [x] `check-decision-refs.py` is green (1690 references resolve). **It could not have caught this**:
      `md_files()` (the script's own file walker) globs only `*.md` under the repo root and explicitly
      skips `scripts/`/`.claude`/etc — it never opens `assets/index.html`, `*.rs`, `*.js`, or `*.css`
      at all. A wrong citation baked into a non-Markdown string is invisible to it by construction,
      not by a gap in its regexes. That is a real gap: worth a separate task if shipped strings are
      meant to be checked mechanically (e.g. extracting quoted/rendered text from `assets/*.html`
      before running the same resolver against it).
