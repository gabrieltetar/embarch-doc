# 039 — Keep every agent revision and owner edit of a pending draft as a version

**State:** open
**Source:** Fleet Ready issue: a pending draft keeps only the agent's last version beside the owner's current body, so the learning diff cannot be taken against an earlier round, and a second owner edit after a revision cannot be told apart from the first. Named as next work in `embarch-desk` decision 88.
**Issue:** EMB-211
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

A pending draft carries a version history. Every agent revision (`POST /drafts/{id}/revise`, `desk_revise_draft`) and every owner edit (`PATCH /drafts/{id}`) adds a version to the draft in the store, recording who made it (agent or owner), when, and the text. The draft's creation is version 1.

`GET /drafts/{id}` returns the versions, and `desk_get_draft` takes two optional version numbers and returns the diff between them. With neither given, both keep answering exactly as today: **`agent_body` and `owner_diff` keep their meaning** (the agent's last version, and that version against the text the owner leaves or sent), so nothing reading them breaks.

## Why now

The owner chose this as the extension on top of decision 88 when he recorded it (EMB-207).

## Dispatch notes

- Code: `src/store.rs` (the draft record), `src/draftedit.rs` (revise and the owner-only diff), `src/server.rs` (`GET`, `PATCH`, `POST .../revise`), `src/mcp.rs` (`desk_get_draft`). A draft stored before this unit has no versions: give it one synthesized from what it holds (the agent version, then the owner's body if it differs) rather than failing, and test that path.
- A `PATCH` that changes nothing adds no version. Say in the decision what the history keeps for a draft that is sent or deleted, and keep it bounded or say why it need not be.
- `github_replies` drafts: version them too if it falls out of the same record; per-reply revision of that kind is `tasks/desk/040`, which builds on this one, so do not build it here.
- Docs: amend decision 88 (`embarch-desk/decisions/agent-writes.md`) to name the history; document the new fields and parameters in `interfaces.md` / `interfaces/mcp-tools.md`.
- **`embarch-desk/spec.md` is in reserve: 9,186 of 10,240 B, 1,054 B left.** Its compaction, `tasks/desk/038`, is `blocked` (`In flux: yes`). Put the field detail in `interfaces/`, not `spec.md`. If this unit needs `spec.md` past its cap, compact it in this unit by a verbatim move into `spec/`, keeping 038's **Must not delete** list, and close 038 `done` (leave its `In flux:` as written). Left in reserve, it is already filed by 038: no new debt.

## Done when

- [ ] Every agent revision and owner edit of a pending draft is kept as a version with its author and time; a no-op `PATCH` adds none.
- [ ] `GET /drafts/{id}` returns the versions, and `desk_get_draft` diffs any two; with no versions named, `agent_body` and `owner_diff` answer as before.
- [ ] A draft stored before this unit reads with a synthesized history, tested.
- [ ] Decision 88 names the history; `interfaces` documents the new fields.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped, `features.d/` row if a new capability shows.
