# 013 — A `linear_search` word query names the project or team it searched

**State:** claimed by agent/desk/013-a-word-search-names-the-team-it-searched, 2026-11-09 20:58
**Source:** Linear issue EMB-12, filed by a session
**Issue:** EMB-12
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A `linear_search` answer to a word query says which Linear project or team it searched, for a desk bound to a whole team as well as one bound to a project, so an empty result reads as "nothing in this scope", not "nothing exists". A key query is unchanged: it still reads the issue from any connected workspace. The tool description says both.

Today a word query is filtered on the open desk's project or team (decision 34), and the answer's `scope` is `scope.project_name`, which is empty for a team-bound desk, so the caller cannot see that a filter applied.

## Why now

A title search for another team's issue silently finds nothing, and the caller reads that as an answer.

## Where to look

- `src/server.rs` `linear_search` — builds `scope` from `open_linear` and returns `scope.project_name`
- `src/linear.rs` `search` — key queries go through `read_issue`, word queries through `in_scope` and `scope_filter`
- `src/mcp.rs` `linear_search` — the tool description ("Find Linear issues by words in their title, or by key.")
- `embarch-desk/decisions/desks.md` decision 34 — scoping filters search on the project when one is named, else on the team

## Dispatch notes

- **Report the scope; do not widen the search.** Searching every connected team is the issue's other option, but decision 34 says scoping filters search, and changing that is a new decision, which this leg (burndown) does not author. If the worker finds the reported scope cannot be made honest without widening it, it files an issue (`fleet-linear.py file --from decision`) and stops there.
- No `embarch-desk` doc is in reserve at the split.

## Done when

- [ ] A word query's answer names the team or project it searched, including on a team-bound desk; a test covers the team-bound case.
- [ ] A key query still resolves an issue of any connected team.
- [ ] The tool description says a word query searches the desk's scope and the answer names it.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `embarch-desk` docs updated if they describe the answer's fields; `changelog.d/` fragment dropped.
