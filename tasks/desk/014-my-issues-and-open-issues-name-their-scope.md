# 014 — My issues and open issues name the team a team-bound desk filtered on

**State:** claimed by agent/desk/014-my-issues-and-open-issues-name-their-scope, 2026-11-09 21:19
**Source:** Linear issue EMB-111, filed by a worker while landing `desk/013`
**Issue:** EMB-111
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`/linear/mine` and `/linear/open` answer `scope` with the same label `/linear/search` and `/pickup` use since `desk/013`: the bound project's name, else `team <KEY>`.

Today both routes build `scope` from `project_name` alone. On a desk bound to a whole team with no project that is an empty string, although both routes filter on the team (decision 34), so a caller cannot tell a team-filtered list from an unfiltered one.

## Why now

`desk/013` fixed the same field on `/linear/search` and added `LinearBinding::scope_label()` for it; these two routes are the rest of the same gap.

## Where to look

- `src/server.rs` `linear_mine`, `linear_open` — where `scope` is built from `project_name`
- `src/store.rs` `LinearBinding::scope_label` — the label `/linear/search` and `/pickup` use
- `src/mcp.rs` — the `linear_my_issues` tool description, if it says what the answer's scope means
- `embarch-doc/embarch-desk/interfaces.md` — the two routes' rows

## Dispatch notes

- Decision 34 (`embarch-desk/decisions/desks.md`) is unchanged: the routes keep filtering as they do; only the label they answer changes.
- No `embarch-desk` doc is in reserve at the split.

## Done when

- [ ] `/linear/mine` and `/linear/open` answer `scope` as `team <KEY>` on a team-bound desk and as the project name on a project-bound one.
- [ ] A `cargo test` covers the team-bound case for at least one of them.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `interfaces.md` updated; `changelog.d/` fragment dropped.
