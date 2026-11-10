# 010 — A Start work worktree links the main clone's untracked local files

**State:** claimed by agent/desk/010-a-start-work-worktree-links-the-clones-local-files, 2026-11-09 20:23
**Source:** Linear issue EMB-18, filed by a session
**Issue:** EMB-18
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A worktree made by Start work has `embarch/`, `CLAUDE.local.md` and `.mcp.json` as links to the main clone's, whenever the main clone has them, and git ignores the links. The links exist before the chat opens, so the session loads the atlas and the MCP servers.

Today `prepare` makes the worktree and `set_auto_mode` writes only `.claude/settings.local.json` into it; the three files sit untracked in the main clone and do not exist in the worktree. Checked on `main` at the split (`0c44f9d`): `worktree.rs` touches none of the three.

## Why now

A session in a Start work worktree has no hardware map and no MCP config, and nothing says so.

## Where to look

- `src/worktree.rs` `prepare`, `prepare_at`, `set_auto_mode` — what is set up in the worktree
- `src/worktree.rs` `edit_permissions` — already appends to the repo's shared `info/exclude`
- `src/server.rs` `start_work` — calls `prepare`, then `set_auto_mode`
- `embarch-doc/embarch-desk/decisions/` — decision 43, Start work

## Dispatch notes

- No `embarch-desk` doc is in reserve at dispatch (2026-11-09 20:23): `desk/011` just moved decisions 29–32, 56, 59 out of `decisions/agents.md` into `decisions/access-point.md`. Decision 43 is in `decisions/sessions.md` (6,137 B).
- This leg runs in burndown: amending decision 43 in place is fine; a new numbered decision is not. If the change needs one, stop and say so here.

## Done when

- [ ] A new worktree has `embarch/`, `CLAUDE.local.md` and `.mcp.json` linked from the main clone when the main clone has them, and nothing when it does not.
- [ ] `info/exclude` lists `embarch` without a trailing slash, since a symlink is not a directory to git.
- [ ] The links are made before `start_work` returns.
- [ ] Tests in `src/worktree.rs` cover a clone with and without the files.
- [ ] Decision 43 amended or `spec.md` updated to say what a worktree is given; gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
