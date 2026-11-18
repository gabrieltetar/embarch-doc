# 033 — A desk tool returns a pull request's review threads

**State:** open
**Source:** EMB-176, an audit finding: a session answering a code review pulls the review comments with `gh api` and writes a throwaway script to group them into threads
**Issue:** EMB-176
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`embarch-desk` reads pull requests today (`src/github.rs`, `pr_query`,
`pr_state`), only to match a PR to a work item and report its state. Add an MCP
tool, for example `github_pr_threads`, that returns a PR's review discussion:

- Input: a repo and a PR number, or the session's work item (its PR).
- Every inline review thread as its root comment and the replies under it, each
  with author, time, file path and line.
- The review bodies with their state (approved, changes requested, commented),
  oldest first.
- A mark on each thread where the PR author has not replied after the latest
  reviewer comment.
- Complete results past 100 comments: handle pagination.

Use whatever route the desk already uses to reach GitHub. Keep the output
compact enough that a long review does not need paging through raw JSON. A flag
for "only threads that changed since the author's last reply" is welcome and
optional.

**Public repo.** Tests use synthetic review JSON, never a real PR's comments.

**No new numbered decision** (burndown). If the tool needs a design call the
desk's decisions do not cover, file it with `scripts/fleet-linear.py file
--from decision` and say so in the task file.

**What you may change.** Only `embarch-desk` and `embarch-doc/embarch-desk/`.

**Doc reserve: carry `tasks/desk/032` with this unit.**
`embarch-desk/interfaces.md` is 14,128 of 15,360 B (1,232 B left, out of
reserve at 13,823 B or less), and `tasks/desk/032` is blocked on `In flux: yes`
with "the next unit that writes `embarch-desk/interfaces.md` carries the
compaction with it". This unit adds a tool row there, so it is that unit:
bring `interfaces.md` out of reserve in the same branch. A verbatim split into
`embarch-desk/interfaces/` restates nothing and is the cheaper move where one
fits (`DOC-COMPACTION.md` §2). Keep `tasks/desk/032`'s **Must not delete**
list: the route table rows and the caller's-desk paragraph (decision 77) as
stated, and the MCP tool list. If `interfaces.md` ends out of reserve, close
`tasks/desk/032` `done` in your branch and leave its `In flux:` line as written.

## Why now

The owner moved EMB-176 to Fleet Ready.

## Done when

- [ ] One desk tool call returns a PR's inline threads grouped root-then-replies, with author, time, path and line on each comment.
- [ ] The same call returns the review bodies with their state.
- [ ] Threads where the PR author has not replied after the latest reviewer comment are marked.
- [ ] A PR with more than 100 review comments comes back complete; a test covers pagination.
- [ ] `spec.md` and `interfaces.md` name the tool, and `interfaces.md` is out of reserve.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
