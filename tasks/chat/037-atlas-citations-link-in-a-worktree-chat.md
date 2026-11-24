# 037 — Atlas citations link in a chat opened in a worktree

**State:** open
**Source:** EMB-409 — a chat opened in a linked worktree finds no atlas, so its citations stay plain text
**Issue:** EMB-409
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`atlasRoot(cwd)` in `embarch-chat/src/atlas.ts` walks up from the chat's
folder for `embarch/atlas/docs` or `embarch/atlas/boards`, and `atlasInfo`
returns null when it finds none. The atlas folder is git-excluded and lives in
the main clone, so a chat opened in a worktree beside it (the shape the desk's
Start work creates) finds nothing, and `embarch-chat` decision 16's citation
links never appear there.

When this is done, `atlasInfo` makes the same fallback the atlas's own tools
make (`embarch-atlas/src/embarch_atlas/common.py`, `atlas_dir`): the chat's own
`<toplevel>/embarch/atlas` when it exists, else the main clone's, the main clone
found from the git common dir. `src/deskService.ts`'s `mainRepo` already finds
it with `git rev-parse --git-common-dir`; `atlasInfo` is synchronous and cached
for 60 s, so it may stay synchronous by reading the worktree's `.git` file
(`gitdir:`) and that folder's `commondir`. Decision 16
(`embarch-doc/embarch-chat/decisions/readouts.md`) says where the atlas is
looked for.

## Why now

EMB-409: Start work chats, where most firmware work happens, are exactly the
ones that open in a worktree.

**Burndown leg: no new numbered decision.** Amend decision 16 in place.

## Done when

- [ ] In a fixture worktree beside a main clone with an atlas, `atlasInfo`
      returns the main clone's atlas root, doc ids and boards (a test in
      `test/atlas.test.mjs`: a scratch main clone, `git worktree add` beside it).
- [ ] A worktree's own `embarch/atlas`, when it has one, wins over the main
      clone's.
- [ ] A folder in no git repo, and a main clone with no atlas, give null as
      today.
- [ ] Decision 16 says where the atlas is looked for.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the npm bullet), `changelog.d/`
      fragment dropped.
