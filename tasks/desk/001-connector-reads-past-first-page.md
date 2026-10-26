# 001 — Harvest entry reads and the assigned-issues list read past their first page

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-desk findings 5 and 8), verified by Opus against embarch-desk@880d9707
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

Two connector reads stop at their first page and say nothing:

- **`harvest::entries_between`** asks for `per_page=100` and never follows `next_page`, unlike `harvest::targets` in the same file. It backs the `harvest_entries` agent tool (any `from`/`to`), the polish's 45 days of recent entries, and each day's `logged_hours`. Over a long range, an agent's `total_hours` comes back short with no sign of it.
- **`linear::my_issues`** asks for `assignedIssues(first: 50)` with no cursor. It backs `GET /pickup` and the `linear_my_issues` tool. A user with more than 50 open assigned issues in scope never sees the older ones as startable work. This is most likely with no desk open, or with a desk that follows a whole team (decision 34).

When done, both reads return every result up to a stated cap, and say so when the cap cuts a result. The worker chooses the cap and how a truncated result is reported. A cap matters most for the agent tool, which an agent may call with a whole year's range.

## Why now

- `src/harvest.rs:109-131`: one `GET /time_entries` per account, no loop. Compare `:66-104`, which pages on `next_page`. The agent route is at `src/server.rs:1461-1480`.
- `src/linear.rs:208-226`: `first: 50` in both arms, no `pageInfo`.
- Neither limit is listed among the constants in spec.md §4, which does list the reference index's caps (1,000 issues, 300 PRs per repo).

## Done when

- [ ] `entries_between` against a stubbed Harvest returning three pages returns every entry from all three, and stops at the cap with a truncation flag the agent route passes on.
- [ ] `my_issues` against a stubbed Linear returning two pages returns both, up to its cap.
- [ ] Both caps are in spec.md §4's constants table.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
