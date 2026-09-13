# 053 — A task title naming another repo's root readme trips the scope-claim check, because the match is a bare substring

**State:** open
**Source:** `inbox/doc-check-task-state-title-substring-false-positive.md`, filed by `core/052`'s
worker; the same wall was hit independently by leg 110's supervisor, which worked around it by
rewording its own task title (`5dcfc88`) rather than touching the script. Filed as a task by leg 111
on 2026-09-13.
**Scope:** doc
**Hardware:** none — a checker script.
**Owner:** required — every path it writes is under `scripts/`, which
[protocol.md](../../../embarch-fleet/protocol.md) §3 reserves to the owner. No agent may run this,
including a supervisor; it is filed here so it is visible rather than remembered.

## What

`scripts/check-task-state.py`'s `check_scope_claims` builds its candidate list from
`tracked_paths()` — every tracked `.md`/`.py`/`.toml` in **this** repo — and then tests `if q in
title`, a plain substring with no path or word boundary. This repo tracks its own root readme, so
that candidate matches inside a title naming *another repo's* readme, and the check reports that the
task's scope may not write a file the task never mentioned.

That fires for any title naming a path whose last segment collides with a reserved `embarch-doc`
path, in any repo, against whichever scope owns that repo — and a readme-correction task's title is
exactly the title that needs to name its own repo's readme, for a reader to know what it is about.

## Why now

It is a false-positive **RED** on `scripts/check-docs.py` for a well-formed, correctly-scoped task,
which is the class of loud-but-wrong signal `tasks/doc/028`–`030` were written to eliminate for the
state fields — now present in the rule those same efforts added. It has already cost two actors this
day: the worker that filed the drop and the supervisor that reworded a title around it. Left
standing, every future occurrence is re-derived from scratch, and the cheap workaround is to write a
vaguer title, which is the wrong direction.

Recorded against it: leg 110's judgement that **a red `check-docs.py` on `main` may be a task file
that leg just wrote**, and that `check-task-state.py` is the sub-check that says so.

## Done when

- [ ] The candidate match requires a path or word boundary — a candidate must not match when
      immediately preceded by `/`, so a sibling repo's path no longer matches this repo's root file.
- [ ] A regression case: a title naming another scope's readme passes for the scope that owns that
      repo, and a title naming this repo's own root readme still fails for a non-`doc` scope.
- [ ] `core/052`'s original title, or an equivalent fixture, passes.
- [ ] `python3 scripts/check-docs.py` green.
- [ ] `changelog.d/` fragment.
