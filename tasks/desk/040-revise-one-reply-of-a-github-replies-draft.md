# 040 — Revise one reply of a GitHub review-replies draft

**State:** claimed by agent/desk/040-revise-one-reply-of-a-github-replies-draft, 2026-11-18 16:34
**Source:** Fleet Ready issue: an agent can revise a Linear draft around the owner's edits, but `POST /drafts/{id}/revise` refuses every `github_replies` draft with a 400. Named as next work in `embarch-desk` decision 88.
**Issue:** EMB-212
**Scope:** desk
**Hardware:** none
**Owner:** no

## What

`POST /drafts/{id}/revise` and `desk_revise_draft` take an optional `comment_id` for a `github_replies` draft and replace that one reply's body. Each reply keeps its own agent version beside the owner's text, as a section does for the Linear kinds under decision 88: a reply the owner has edited is refused with 409 naming the reply (its comment id) and both texts, and nothing changes; every other reply is untouched. A `github_replies` revise with no `comment_id`, or one naming no reply in the draft, is a 400 saying which.

## Why now

The owner chose this as the extension on top of decisions 88 and 89 when he recorded them (EMB-207, EMB-206). It waits for `desk/039` so a reply revision adds a version to the history that unit builds, rather than the two units writing one record twice.

## Dispatch notes

- Code: `src/server.rs` (the `github_replies` branch of revise that returns 400), `src/draftedit.rs` (revise and the owner-only diff), `src/mcp.rs` (`desk_revise_draft`), `src/store.rs` if a reply needs its own agent version field.
- A reply already posted on a partly sent draft (decision 89 keeps those with their URLs) is not revisable: refuse it with a 409 that says it is posted.
- A reply revision adds a version to the history `desk/039` built, like any other revise.
- Docs: decisions 88 and 89 (`embarch-desk/decisions/agent-writes.md`) and `interfaces.md` / `interfaces/mcp-tools.md` say so.
- `embarch-desk/spec.md` is in reserve (1,054 B left at filing; re-check with `scripts/check-doc-size.py --pressure`). Its compaction `tasks/desk/038` is `blocked` on `In flux: yes`; if this unit needs `spec.md` past its cap, compact it here by a verbatim move into `spec/`, keeping 038's **Must not delete** list, and close 038 `done`.

## Done when

- [ ] Revising one reply of a `github_replies` draft by `comment_id` changes that reply and no other.
- [ ] A reply the owner edited is refused with 409, naming the reply and both texts; a posted reply is refused too.
- [ ] Decisions 88 and 89 and `interfaces` say so.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
