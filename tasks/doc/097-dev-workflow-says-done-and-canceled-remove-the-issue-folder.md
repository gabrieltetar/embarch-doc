# 097 — embarch-dev-workflow.md §6 says Done and Canceled remove the issue's folder

**State:** open
**Source:** Linear issue EMB-73
**Issue:** EMB-73
**Scope:** doc
**Hardware:** none
**Owner:** required

## What

`embarch-dev-workflow.md` §6, "Landing happens only when the owner asks", says the owner removes an issue's worktrees and its `.dev-worktrees/<key>/` folder by hand once the chat is done. After `tasks/desk/025`, `tasks/desk/026` and `tasks/chat/023` land, that is no longer how it works: moving the issue to Done or Canceled ends its chat, and the desk removes the worktrees, their local branches and the folder once the window is closed (Canceled also deletes the remote branches). §6 should say so, in place of "by hand".

`embarch-dev-workflow.md` is reserved to the owner, so no agent can make this edit.

## Why now

EMB-73's fifth `Done when` box. The other boxes are the three tasks above; the sixth (a Done or Canceled issue's chat opens read-only from the Work tab) is a separate issue outside the fleet's repos.

## Done when

- [ ] After the three tasks above have landed, §6 says Done and Canceled remove the worktrees and the folder, and what blocks it (uncommitted files; for Done, a branch not on `origin/main`).
