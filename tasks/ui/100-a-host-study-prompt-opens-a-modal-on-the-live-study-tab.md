# 100 — A host study's prompt opens a modal on the Live Study tab, answered there

**State:** claimed by agent/ui/100-host-study-prompt-modal, 2026-10-28 21:55 — re-claimed for a resume: the 17:25 worker died with its leg at ~17:35 holding 612 uncommitted lines (5 files), committed by the next leg's recovery as `cc29076` on the code branch (unverified); the worktrees are kept and a fresh worker continues from it.
**Reserve at dispatch (2026-10-28):** nothing in `embarch-ui` is in reserve. `embarch-ui/open.md` is 3,738/5,120 B, under `ui/088`'s 3,920 B floor since `ui/099` retired a bullet, so `check-doc-size.py --pressure` reports it PAID: close `tasks/ui/088` as done in this unit's doc branch (one line saying `ui/099` paid it). The note below predates that; still do not grow `open.md` past the floor.
**Source:** `tasks/suite/048` (operator prompt step), whose Core and `embarch-api` halves landed 2026-10-28 as `embarch-core` decision 105 and `embarch-api` decision 99; the UI half is filed here, as `suite/046` filed `ui/098`. The proposal: [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), owner's choice 4.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A host study can stop at a `Prompt` step until a person answers (`embarch-core` decision 105). Core sends `PromptPending {prompt_id, list, step_index, step_name, text, opened_utc_ms, deadline_utc_ms}` and `PromptResolved {prompt_id, answer, answered_by}` on the study's event stream, shows the waiting prompt as `pending_prompt` on `GET /study/{id}`, and takes `POST /study/{id}/prompt {prompt_id, answer: confirmed|cancelled, answered_by: "ui"}`. `embarch-core-client` decodes all of it (`StudyEvent::PromptPending`/`PromptResolved`, `StudyStatusResponse::pending_prompt`, `CoreClient::answer_prompt`), and `follow_study` reports a prompt already waiting from its opening poll.

Today `src/live_study.rs` only writes those events as feed rows (a stopgap the suite pass added to keep the match exhaustive). When this is done, a waiting prompt opens a **modal on the Live Study tab** on the existing dialog pattern: the prompt's text large enough to read from across the bench, a countdown to `deadline_utc_ms`, **Confirm** and **Cancel**, and a sound or a desktop notification when it opens (the field operator asked for a visual alert, not a chat line). The modal closes on `PromptResolved` whoever answered, and says who if it was another surface. A browser that opens the tab mid-prompt sees it (the session snapshot carries the pending prompt). The answer goes through a ui route to `answer_prompt` with `answered_by: "ui"`; a `409` (the prompt already ended) closes the modal and says why.

## Why now

The field session this came from relayed 25 confirmations through a chat. Core and the API now hold a prompt open; the person at the bench still has no window that shows it.

## Notes for the worker

- How the UI comes to follow a host study started from `embarch-api` (not from this UI) is this task's design call: today a Live Study session exists only for a run started here or opened from the studies list. Record the choice as a ui decision.
- `embarch-ui/open.md` is in reserve (its compaction `ui/088` is blocked on flux): do not grow it.

## Done when

- [ ] The modal: text, countdown, Confirm, Cancel, a sound or notification on open; closes on `PromptResolved`.
- [ ] A mid-prompt reload shows the modal (snapshot carries `pending_prompt`).
- [ ] Answering posts with `answered_by: "ui"`; a `409` is shown, not swallowed.
- [ ] Tested headless against a stub Core (a route test for the answer route at least; a `tests/browser` drive if the modal's rendering can be reached).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions/` updated, `changelog.d/` fragment dropped.
