# 007 — An issue read says when comments were cut, and the rest can be read

**State:** open
**Source:** Linear issue EMB-13, filed by a session
**Issue:** EMB-13
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

When an issue has more comments than `linear_get_issue` returned, the answer says so — the total, and that some were not returned — and the agent can read the others through the desk, on both account types (an API-key account over GraphQL and an account through Linear's MCP server).

Today both read paths fetch at most 25 comments and return them oldest first, with no total and no truncated flag: `gql_detail` asks `comments(first: 25)`, and `linear_mcp.rs` has `COMMENTS = 25`. Check which 25 each path actually returns before you write the fix: a `first: 25` page and a `limit` ordered by `createdAt` may keep different ends of a long thread, and the tool description and `plugin/skills/desk/SKILL.md` both say "latest comments". Make the answer and the wording agree with what is kept.

## Why now

A decision recorded in a comment the cap cut is missed with nothing to say it was. Decision 59 already sets the rule for paged reads — say when the cap cut — and the issue read does not follow it yet.

## Where to look

- `src/linear.rs` `gql_detail` (`comments(first: 25)`) and `detail_from` — the GraphQL answer
- `src/linear_mcp.rs` `issue_detail`, `detail_from` and `COMMENTS` — the same cap through the MCP account
- `src/mcp.rs` `linear_get_issue` — the tool and its description
- `plugin/skills/desk/SKILL.md` — "latest comments"
- `embarch-doc/embarch-desk/decisions/agents.md` decision 59 — paged reads say when the cap cut

## Done when

- [ ] An issue with more than 25 comments returns a total and says some were not returned, on both account types.
- [ ] A caller can read the older comments through the desk (a parameter on `linear_get_issue`, or a second tool; your call, recorded in `decisions/` if it is a new choice).
- [ ] Tests cover the cut and the uncut answer.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `embarch-desk` `interfaces.md` updated for the changed answer, `changelog.d/` fragment dropped.
