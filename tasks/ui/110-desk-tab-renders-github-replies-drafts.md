# 110 — The Desk tab renders and edits GitHub review-reply drafts

**State:** claimed by agent/ui/110-desk-tab-renders-github-replies-drafts, 2026-11-18 03:18
**Source:** Fleet Ready issue: the Desk tab shows a GitHub review-replies draft as a blank Linear comment, so its replies cannot be read, edited or sent from the tab.
**Issue:** EMB-205
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-desk` now stores pending drafts of kind `github_replies` (`desk/035`, EMB-173), carrying `repo`, `pr` and `gh_replies` — a list of (`comment_id`, `body`, optional `url`) — in the drafts its `/view` route returns. The Desk tab's draft cards (`assets/desk.js`, the `d.kind` branches and the patch built from the `.desk-draft-reply` fields) know only `linear_comment`, `linear_issue` and `linear_edit`, so this kind renders with no issue key and an empty body.

Give `github_replies` a card of its own: a header reading "Replies on owner/name#N", one editable textarea per reply labelled by its comment id, and an edit that PATCHes `/drafts/{id}` with `gh_replies` (the full list as edited; an emptied body drops that thread). Send stays the existing `/drafts/{id}/send`, which answers `urls`; show the posted URLs on the card. A partly sent draft (some replies already carry a `url`) shows which threads were posted and leaves only the rest editable.

## Why now

The owner moved the issue to Fleet Ready. Until it lands, an agent's reply draft can only be sent from the desk's data and routes, not from the screen the owner reviews drafts on.

## Dispatch notes

- **Burndown: no new numbered decision.** This is a new card on an existing surface; document it in `spec.md` without authoring a decision. Several of `embarch-ui`'s decision topic files are within 256 B of their cap (`check-doc-size.py --pressure`), which is one more reason not to write one.
- Read `embarch-doc/embarch-desk/interfaces.md` for the draft's exact fields and the Send answer; do not edit it, it is `desk`'s. If the routes lack something the card needs, stop and say so here rather than working around it.
- Test against recorded `/view` payloads or a stub server. **Never send a draft to a real repository.**
- No file of this sub-project is in reserve.

## Notes

Browser check (`drive_desk.py`) stubs PATCH and Send in the page; the scratch desk binary had to be rebuilt from `embarch-desk` main (the checked-in debug binary predated EMB-173). A fully sent draft leaves `/view`, so the tab keeps a dismissable "Posted" card for the URLs. Debt: not run against a real PR (by rule).

## Done when

- [x] A `github_replies` draft renders on the Desk tab with its repo, PR and one editable body per thread.
- [x] Editing a body and pressing Send posts the edited text, and the posted URLs are shown on the card.
- [x] Tests or a recorded-payload check cover the render and the PATCH body; gate green (`../../embarch-fleet/gate.md`); `spec.md` updated, `changelog.d/` fragment dropped, `features.d/ui-<NNN>-*` row if it is a user-visible feature.
