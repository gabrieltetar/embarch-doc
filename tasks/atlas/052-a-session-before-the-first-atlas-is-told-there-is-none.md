# 052 — A session before the first atlas is told there is no atlas yet

**State:** claimed by agent/atlas/052-a-session-before-the-first-atlas-is-told-there-is-none, 2026-11-10 01:41
**Source:** Linear issue EMB-22, filed by a session
**Issue:** EMB-22
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`embarch-atlas init` writes the import line `@embarch/atlas/MAP.md` into `<fw>/CLAUDE.local.md`, but `MAP.md` is only written by `join`, once an atlas's commit equals HEAD. Between `init` and the first `join` the import resolves to nothing, and a session in that repo gets no hint that an atlas is missing or what to run. An agent then answers hardware questions from memory instead of asking.

Make the file the import names exist from `init` on, saying no atlas is built yet and naming the next step, and have the first `join` replace it with the real map, byte-stable as before.

## Why now

The window between `init` and a first atlas is exactly when a session most needs to know the map is absent: it is the planning phase, before any distillation.

## Where to look

- `src/embarch_atlas/project.py` `wire_session_map` — writes the import into `CLAUDE.local.md`; writes no map
- `src/embarch_atlas/project.py` `mark_map` — adds the `> **Stale:**` line, returns without writing when `MAP.md` does not exist
- `src/embarch_atlas/mapgen.py` — the only writer of `MAP.md` (the `<atlas_dir>/MAP.md` copy)
- `src/embarch_atlas/stale.py` — what reads the map's state
- `DESIGN.md` "How a session sees the atlas" — states the map loads every session

## Dispatch notes

- The direction the issue names: `init` writes a short placeholder `MAP.md` that says no atlas is built and names the next skill (`/atlas-translate-docs`, then `/atlas-build`, as the skills are named today; check them), which `join` overwrites. `mark_map` and `stale.py` must treat the placeholder as "no atlas", never as a stale atlas. If you find a cheaper route that meets the same Done when, take it and say why in the task file.
- A placeholder must not be mistaken for a map anywhere: a lookup's `src:` line, `status`, and anything that reads `MAP.md`'s first line. Grep for every reader.
- Burndown is on: no new numbered decision. Amend `DESIGN.md` "How a session sees the atlas" in place.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] After `embarch-atlas init` and before any `join`, the file `CLAUDE.local.md` imports exists and tells the session no atlas is built yet and which skill to run.
- [ ] The first `join` replaces it with the real map, byte-stable as before, and `mark_map` / `stale.py` read the placeholder as no atlas.
- [ ] A test covers `init`, then the map's content, then a `join` replacing it; `DESIGN.md` says so.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
