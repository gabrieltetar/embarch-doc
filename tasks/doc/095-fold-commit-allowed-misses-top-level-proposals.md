# 095 — `fold-commit.py` refuses `bootload-proposal.md`, a top-level doc the supervisor may write

**State:** open
**Source:** `suite/054`'s fold, leg started 2026-10-29 15:24 (log entry `2026-10-29 15:47 — suite/054`): `check-ownership.py --supervisor` passed `bootload-proposal.md` (classified fleet-writable in `fleet.toml`), then `fold-commit.py` refused it with "1 path(s) outside what a unit's fold may stage". Its `ALLOWED` prefixes (`embarch-fleet/scripts/fold-commit.py`, about line 71) accept `embarch-` and `embarch.md` but no top-level doc with another name, so the three `embarch-*-proposal.md` files folded and `bootload-proposal.md` had to go in a separate commit (`b21b0fef`). Filed from an inbox drop at the leg started 2026-10-29 15:49.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `embarch-fleet/scripts/`, which is reserved.

## What

The set of paths a fold may stage and the set `check-ownership.py --supervisor` lets the supervisor write disagree for top-level docs that do not start with `embarch-`. Either derive `ALLOWED` for top-level docs from `fleet.toml`'s fleet-writable list (one source, the way `check-task-state.py` asks `queue-status.py` rather than keeping a second pattern), or add the missing names. Today the only such file is `bootload-proposal.md`; a future split or proposal with a non-`embarch-` name hits the same refusal.

## Why now

A suite task that edits one of these has to split its fold into two commits, which is exactly the "unit landed in more than one commit" shape the single fold commit exists to prevent, and the leg's log entry then names two SHAs for one unit.

## Done when

- [ ] A fold that stages `bootload-proposal.md` (or any top-level doc `check-ownership.py --supervisor` accepts) is not refused for its path.
- [ ] The two lists cannot drift apart again, or a check says when they do.
