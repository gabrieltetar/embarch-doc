# 035 — Post approved replies to GitHub review threads from one draft

**State:** done
**Source:** Fleet Ready issue: posting approved replies to a PR review took a throwaway script that split a draft file and called the GitHub API once per thread.
**Issue:** EMB-173
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A session can propose replies to two or more existing review threads on one GitHub pull request as a single draft — repository, PR number, and a list of (review comment id, reply body) — and the draft waits on the Desk tab beside the Linear drafts until the owner presses Send, exactly as `linear_draft_comment` does. On Send, each body is posted as a reply in its own thread and the tool or the Desk records every posted reply's URL. Before anything is posted, every comment id is checked to be a review comment on that PR, and one that is not stops the whole send.

The shape is the worker's call within `embarch-desk`, for example a `github_draft_review_replies(repo, pr, replies)` MCP tool. Reuse what `github_pr_threads` (EMB-176, `desk/033`) already does to reach GitHub and read a PR's review comments, and what the Linear draft tools already do for the pending-draft store and the Send path, rather than a second mechanism for either.

## Why now

The owner moved the issue to Fleet Ready. Every session that answers a code review writes its own splitter and posting loop, and the desk already holds the owner's Send for Linear.

## Dispatch notes

- **Burndown: no new numbered decision.** Document the tool in `spec.md` or `interfaces.md` without authoring a decision, as `github_pr_threads` was. If the design genuinely needs one — this is the desk's first draft that posts somewhere other than Linear — implement the part that does not, file the decision with `scripts/fleet-linear.py file --from decision` (a `Type: decision` body per `LINEAR-PROTOCOL.md`), and say so in this file.
- Test against a stubbed GitHub client. **Never post to a real repository** from a test or by hand.
- No file of this sub-project is in reserve.

## Outcome

`github_draft_review_replies(repo, number, replies)` MCP tool, over `POST /drafts` kind `github_replies` (same pending-draft store, Send and `direct_writes` path as the Linear drafts). Send checks every comment id against the PR's review comments (`github::thread_roots`) before posting, posts each body under its thread's root, records each URL on the draft and returns `urls`; a mid-batch failure keeps the draft open with posted URLs kept. Tested against a local stub GitHub server (four tests in `server.rs`), never a real repo.

- **No decision authored (burndown).** The desk's first draft that posts outside Linear arguably wants one; not filed, the shape is documented in `interfaces.md`.
- **Debt, other repo:** the Desk tab (`embarch-ui/assets/desk.js`) does not render or edit this draft kind; filed as EMB-205. The first box is met in the desk's data (`/view` drafts) and PATCH/Send routes, not yet on screen.

## Done when

- [x] A session can propose replies to two or more review threads on one PR, and they wait for the owner's Send on the Desk tab.
- [x] On Send, each reply lands in its own thread, and every posted URL is returned or shown.
- [x] A comment id that does not belong to the PR stops the send before anything is posted.
- [x] Tests cover the cases above; gate green (`../../embarch-fleet/gate.md`); `spec.md`/`interfaces.md` updated, `changelog.d/` fragment dropped, `features.d/desk-<NNN>-*` row if it is a user-visible feature.
