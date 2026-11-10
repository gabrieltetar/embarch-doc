# 056 — The atlas-use skill knows the no-atlas placeholder

**State:** open
**Source:** Linear issue EMB-123, filed by the reviewer of `atlas/052`
**Issue:** EMB-123
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Since `atlas/052`, `embarch-atlas init` writes `embarch/atlas/MAP.md` as a placeholder (`NO_ATLAS_MAP` in `src/embarch_atlas/project.py`, first line `# No hardware atlas is built yet`) until the first `join` replaces it. The `atlas-use` skill triggers on that file existing, and its step 1 (MAP) knows only the stale-map case, so a session that follows it goes on to step 2 and looks for cards that do not exist.

Give step 1 the no-atlas case: when `MAP.md` is the placeholder, say no atlas is built, name the next steps the placeholder names (`/atlas-translate-docs`, then `/atlas-build`), do not answer the hardware question from memory, and stop rather than reading cards. Make the skill and the placeholder name the same next steps, so the two cannot drift: a test that reads both is the cheap guard.

## Why now

A session between `init` and the first atlas is told by the skill to read cards and by the placeholder that there are none.

## Where to look

- `skills/atlas-use/SKILL.md` step 1 and its `description` line
- `src/embarch_atlas/project.py` `NO_ATLAS_HEAD`, `NO_ATLAS_MAP`
- `DESIGN.md` "How a session sees the atlas" (amended by `atlas/052`)

## Dispatch notes

- Burndown is on: no new numbered decision. The atlas has none; amend `DESIGN.md` in place if it describes the skill's steps.
- The worktree needs `.atlas-local` linked beside it and a `.venv` of its own (both made for you); `test_public_guard` must run, not skip.
- No file in `embarch-doc/embarch-atlas/` is in doc-size reserve.

## Done when

- [ ] The `atlas-use` skill's step 1 says what to do when `MAP.md` is the no-atlas placeholder, and stops there.
- [ ] The skill and the placeholder name the same next steps, with a test.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `changelog.d/` fragment dropped.
