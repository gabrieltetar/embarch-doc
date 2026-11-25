# 045 — The desk's reference index holds the Linear documents of its projects

**State:** open
**Source:** EMB-407 — the desk's reference index holds no Linear documents
**Issue:** EMB-407
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

The reference index (decision 56) is `RefIndex {desk_id, synced_ms, issues,
prs, projects}` in `src/refs.rs`; `desk/044` added `projects`, read on both
connector paths (`linear::scope_projects` in `linear.rs`, the Linear MCP
server's `list_projects` in `linear_mcp.rs`). No query reads a Linear document
anywhere. When this is done, `GET /refs` also carries the documents of the
projects the index holds: titles and links, never their text.

- `RefDocument {id, title, url, project_id, project_name, updated_ms}` and
  `RefIndex.documents`, with `#[serde(default)]` so a `refs.json` written
  before it loads.
- **Which documents, as the issue states:** those of the projects the index
  holds, the newest 500 by update (`DOCUMENTS_CAP`); trashed ones left out. A
  document outside any indexed project (a team's or an initiative's, if Linear
  has them) is left out, and decision 56 says so.
- **Titles and links only.** A document's content is never requested. A title
  is anyone's to write, so it is data, as an issue title is.
- **Both connector paths**: GraphQL (`documents` filtered on the indexed
  projects' ids, ordered by update; check the filter against Linear's schema
  as far as the repo's own schema copy or tests allow, and say what was not
  checked), and the Linear MCP server's `list_documents` per project. Read
  that tool's arguments from the server's tool list as `linear_mcp.rs` already
  does for its other tools; if they cannot be read here, write what was
  assumed in decision 56, as `desk/044` did for `list_projects`.
- `Fetched` gains `documents`; `Store::apply` treats them as it treats
  projects: a failed fetch keeps the rows for an unchanged scope, a changed
  scope drops them, and a changed list (an edited title included) moves
  `synced_ms` and `/view`'s `refs_ms`.
- **The shape is fixed in `embarch-promptu`'s `docs/contract.md` §15.3**
  (read it from `origin/main` of that repo); follow it where it is more exact
  than this list.

## Why now

EMB-407: the chat linker's Linear projects and documents kind
(`embarch-promptu` build step 5) mirrors `GET /refs`. Its blocker, the
projects in the index (EMB-406, `desk/044`), landed on 2026-11-25.

**Burndown leg: no new numbered decision.** Amend decision 56
(`embarch-doc/embarch-desk/decisions/access-point.md`) in place with a dated
`(EMB-407)` clause, the earlier text standing, as `desk/044` did, and update
`interfaces/chat-routes.md` (`GET /refs`). If the work needs a decision neither
the issue nor the contract states, stop and say so in this file.

No file is in reserve on the size ledger at dispatch.

## Done when

- [ ] On the GraphQL path and on the MCP path, a fixture project's documents
      appear in `GET /refs` with title, URL and project, newest first.
- [ ] A trashed document is absent; the cap keeps the newest 500.
- [ ] A failed document fetch keeps the rows for the same scope; an edited
      title moves `synced_ms`.
- [ ] A `refs.json` with no `documents` loads, and `GET /refs` then answers
      `documents: []`.
- [ ] Decision 56 and `interfaces/chat-routes.md` say it, including what is
      left out.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
