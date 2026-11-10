# 019 — A desk tool lists a team's issues in a named state

**State:** claimed by agent/desk/019-a-desk-tool-lists-a-teams-issues-by-state, 2026-11-10 02:54
**Source:** Linear issue EMB-11
**Issue:** EMB-11
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The desk has `linear_my_issues` and `linear_search`, but nothing that lists a team's issues in a given state, for example every issue in a team's "Fleet Ready". `linear_my_issues` lists only the user's assigned open issues; `linear_search` matches title words or one key. Decision 29 makes the desk the one access point to Linear, so an agent that needs a queue listing has no route that keeps to it.

Add the tool, **with this direction (decided at the split):**

- A new desk MCP tool lists the issues of a named team, optionally narrowed to one project, in a named workflow state. The worker names the tool and its parameters; the state is matched by name as the team defines it.
- It works in **every connected workspace**, both the API-key backend (`src/linear.rs`) and the Linear-MCP backend for a workspace that gives no key (`src/linear_mcp.rs`, decision 68). If one backend cannot filter by state, filter after fetching and say so in the decision.
- It pages up to a cap and says when the cap cut the list, as decision 59 does for assigned issues.
- **The skill's policy, decided here:** agents do not fall back to Claude's own Linear connector for anything the desk lacks. Where the desk has no tool for a read, the session says so and the gap is filed against the desk. That is decision 29 applied, not a new rule; `plugin/skills/desk/SKILL.md` says it in one place.

## Why now

A fleet leg, an audit or a session reading a queue is otherwise tempted to use the connector, which decision 29 rules out.

## Where to look

- `src/linear.rs` `open_issues` — already lists every open issue of the open desk's scope (decision 71); it takes no state or team argument
- `src/linear_mcp.rs` — the MCP-backed workspace's calls, beside its `search`
- `src/server.rs` `linear_open`, `linear_search` — the routes the tools go through
- `src/mcp.rs` `linear_search`, `linear_teams` — where the tool goes
- `plugin/skills/desk/SKILL.md`
- `embarch-doc/embarch-desk/decisions/access-point.md` (29, 59) and `decisions/agents.md` (68); `interfaces.md` for any new route

## Dispatch notes

- Normal mode: a new numbered decision is expected (the tool, its cap and the no-fallback line). Number it per `DOC-CONVENTIONS.md`; another desk worker may have taken the next number on `main` by the time you land, so check `main` before you commit.
- Tests use the existing fakes for both backends; nothing calls a real Linear workspace.
- No `embarch-desk` doc in `embarch-doc` is in doc-size reserve at the split.

## Done when

- [ ] A desk MCP tool lists a named team's issues in a named state, in any connected workspace, and reports when its cap cut the list.
- [ ] Both backends have a test, the cap's cut included.
- [ ] `plugin/skills/desk/SKILL.md` says agents do not fall back to the connector for what the desk lacks.
- [ ] A new `embarch-desk` decision records the tool, and `interfaces.md` lists any new route.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
