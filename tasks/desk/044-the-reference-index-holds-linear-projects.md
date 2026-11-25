# 044 — The desk's reference index holds the Linear projects in its scope

**State:** claimed by agent/desk/044-the-reference-index-holds-linear-projects, 2026-11-25 01:19
**Source:** EMB-406 — the desk's reference index holds no Linear projects
**Issue:** EMB-406
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The reference index (decision 56) is `RefIndex {desk_id, synced_ms, issues,
prs}` in `src/refs.rs`, fetched from `linear::scope_issues` and
`github::repo_prs`. The desk reads Linear projects only for its desk form
(`linear::projects`: `id`, `name`, `state`, `teams`, no URL). When this is
done, `GET /refs` carries the projects in the desk's scope, each with its
Linear URL.

- `RefProject {id, name, state, url, team_keys}` and `RefIndex.projects`, with
  `#[serde(default)]` so a `refs.json` written before it loads.
- **Scope, as the issue states:** a desk bound to a project indexes that
  project; one bound to a team indexes the team's projects, the newest 200 by
  update (`PROJECTS_CAP`). Archived projects count, as Done issues do; trashed
  ones do not.
- **Both connector paths**: GraphQL in `linear.rs` beside `scope_issues`, and
  the Linear MCP server's `list_projects` scoped to the team in
  `linear_mcp.rs`, as `scope_page` scopes issues. The project's `url` is
  Linear's own.
- `Fetched` gains `projects: Option<Vec<RefProject>>`; `Store::apply` keeps
  the old rows when the fetch failed and the scope is unchanged, as it does
  for issues, and counts a changed project list as a change, so `synced_ms`
  and `/view`'s `refs_ms` move.
- **The shape is fixed in `embarch-promptu`'s `docs/contract.md` §15.3**; read
  it and follow it where it is more exact than this list.

## Why now

EMB-406: the chat linker's Linear projects and documents kind
(`embarch-promptu` build step 5) mirrors `GET /refs`, and the documents unit
(EMB-407) reads the projects this one indexes. Promptu's contract §15 fixed the
shape on 2026-11-25 (`promptu/024`), which was this issue's blocker.

**Burndown leg: no new numbered decision.** Amend decision 56
(`embarch-doc/embarch-desk/decisions/access-point.md`) in place to say the
index carries projects, and update `interfaces/chat-routes.md` (`GET /refs`).
If the work needs a decision neither the issue nor the contract states, stop
and say so in this file.

## Done when

- [ ] A team-bound desk's index lists the team's projects with their URLs; a
      project-bound desk's lists that one project.
- [ ] A failed project fetch keeps the rows it held for the same scope; a
      changed scope drops them.
- [ ] A renamed project moves `synced_ms`; an unchanged list does not.
- [ ] A `refs.json` with no `projects` loads, and `GET /refs` then answers
      `projects: []`.
- [ ] Decision 56 and `interfaces/chat-routes.md` say it.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
