# Proposal: picking up an issue, and Claude sessions on the Desk

**Status:** proposal, 2026-10-22.

Spans `embarch-desk`, `embarch-ui` and the `embarch-desk` Claude Code plugin, which is why it sits at this repo's root ([DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3). Shaped with the owner in four rounds of questions on 2026-10-22.

**Built and folded** (`embarch-desk` decisions 43–45, 2026-10-22): picking an issue up from the Desk and the live sessions on its card. **What follows, finishing an issue, is still proposed.**

## Finishing an issue (owner's choice, 2026-10-22)

1. **The session drafts the PR**, and it waits on the Desk like any draft (`embarch-desk` decision 30) until the owner sends it: a `github_pr` draft kind (title, body, head branch); Send opens the PR through the GitHub API.
2. **The issue moves to In Review when its PR opens** — a status move.
3. **The worktree is removed when the PR merges**, asking first if it holds uncommitted work.

## Order of work

1. The PR draft kind, its tool for agents, its place in the Drafts area. About half a day with 2 and 3.
2. In Review on open; the worktree's removal on merge.
3. **Fold** into the desk's and the UI's docs; delete this file.

## Open questions

- **A desk with several repos** (a firmware repo and its manifest repo): which one a PR opens against when a session touched both.
