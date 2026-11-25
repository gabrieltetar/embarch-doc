# 039 — The 💡 linker offers local branches and worktrees

**State:** claimed by agent/chat/039-the-linker-offers-branches-and-worktrees, 2026-11-25 02:47
**Source:** EMB-410 — the 💡 linker cannot offer a branch or a worktree
**Issue:** EMB-410
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft that says "rebase it on the fan branch" or "do it in the other
worktree" gets no reference line today: the linker knows the desk's PRs, which
name a branch, but never a branch or a worktree itself. When this is done, the
linker has a **branch and worktree source** on decision 112's source interface
(`src/assistant/refsBase.ts`, `src/assistant/references.ts`; `refsDesk.ts` is
the model to follow), read from git in the chat's folder's main clone:

- **Branches:** `git for-each-ref --sort=-committerdate --count=300` over
  `refs/heads` and `refs/remotes/origin`; a remote branch with a local twin
  appears once. An entry's words come from the name split on `/`, `-` and `_`.
- **Worktrees:** `git worktree list --porcelain`, each with its path and branch.
- **The chat's own branch and worktree are left out**, as decision 88 leaves out
  the chat's own item.
- **Gated:** offered by words only when the draft carries a cue word (branch,
  worktree, checkout, clone, rebase, merge), whole word in any case; a branch
  the draft names exactly is offered with no cue word.
- **Written:** `branch <name>`, plus ` (PR owner/repo#N)` when the desk's index
  holds a PR on that branch (`IndexPr.branch`, `src/desk/client.ts`);
  `worktree <absolute path> (branch <name>)`.
- **Refresh:** before a cards call, only when the last read is over 60 s old. A
  git failure leaves the kind empty and logs once.

`src/deskService.ts` already runs `git worktree list --porcelain` and `git
rev-parse --git-common-dir` for its transcript scan (`git`, `mainRepo`,
`worktrees`): share those helpers rather than copying them. The chat's folder
and branch come from `src/views/chatHost.ts`.

## Why now

EMB-410, one linker kind of `embarch-promptu` build step 5. Decision 112
(`chat/038`, landed 2026-11-25) made each later kind one more source and a row
in the decision, not a change to the matcher; this is the first such kind.
`embarch-promptu` decision 16 gives the linker branches and worktrees; the
contract is `embarch-promptu/docs/contract.md` §15 (read it from
`origin/main` if the main checkout lags). The source's details (the 300 cap,
the cue words, the 60 s refresh) are the plan's recommendations, which the
owner may strike: say so where the decision records them.

## Where the doc goes

Decision 112 lives in `embarch-doc/embarch-chat/decisions/references.md`
(moved out of `assistant.md` by `chat/038`; the issue's pointer to
`assistant.md` predates that). Record the branch and worktree kind as a dated
amendment there, or as a new decision in the same file, per decision 112's "one
more source and a row here". `decisions/promptu.md` (decision 96, 204 B under
its limit) is not to be touched. `spec/constants.md` takes the source's
constants.

## Done when

- [ ] In a scratch repo made in the test with branches `main`,
      `fix/abc-9-fan-curve` and `feature/logger`, the draft "rebase it on the
      fan branch" offers `branch fix/abc-9-fan-curve`.
- [ ] The chat's own branch and worktree are never offered.
- [ ] A second worktree is offered as `worktree <path> (branch <name>)`.
- [ ] A branch the desk's index has a PR on is written with that PR.
- [ ] A draft with no cue word and no exact branch name gets no branch line.
- [ ] Git runs at most once a minute while drafts change, and the decision says
      so.
- [ ] Gate green (`../../embarch-fleet/gate.md`): `npm ci`, `build`,
      `typecheck`, `npm test`, `test:webview`.
- [ ] `spec`/`decisions`/`open.md` updated, `changelog.d/` fragment dropped,
      `status.d/` fragment for anything suite-level it made false.
