# 022 — Decision 103's as-built prose names a deleted function and chip

**State:** claimed by agent/chat/022-decision-103-names-a-deleted-function-and-chip, 2026-11-10 02:10
**Source:** Linear issue EMB-125, filed by the reviewer of `chat/018`
**Issue:** EMB-125
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-chat/decisions/sessions.md` decision 103 (an agent hands its chat to a fresh session) says in its **As built** sentence that the fresh session starts as `freshChat` does ("`freshChat`'s start"), and its **Rejected** list says a new tab is what "36's chip does". `chat/018` (EMB-66, the owner's call) deleted `freshChat` from the code and removed 36's chip. 103's decision stands; only these two pointers are stale.

Reword both so neither names `freshChat` or 36's chip as a live thing: describe how the fresh session actually starts in the code today (read `src/` for what `handoffChat` calls), and say of the rejected new tab what is still true without leaning on the removed chip.

## Why now

The reviewer of `chat/018` found it; 103's prose now points at code that does not exist.

## Where to look

- `embarch-doc/embarch-chat/decisions/sessions.md` decision 103
- `embarch-doc/embarch-chat/decisions/assistant.md` decisions 36 and 97, as amended by `787c9cfb`
- `embarch-chat` `src/`: `handoffChat` and what it calls to start the fresh session (read only, from the main checkout at `/home/gabriel/Github/embarch/embarch-chat`)

## Dispatch notes

- Doc only: no `embarch-chat` code worktree. Nothing under `src/`, `webview/` or `test/` names `freshChat` or 36's chip any more (checked at dispatch).
- Burndown is on: no new numbered decision. Edit 103's prose in place; its decision is unchanged.
- No file in `embarch-doc/embarch-chat/` you will edit is in doc-size reserve. `decisions/promptu.md` (decision 96) has 204 B left; you should not need it.
- `promptu/005` amends Promptu's decision 39 for the same issue in parallel; do not edit `embarch-promptu/`.

## Done when

- [ ] Decision 103 no longer names `freshChat` or "36's chip" as live things, and its decision text is unchanged.
- [ ] Gate green (`python3 scripts/check-docs.py`, `check-ownership.py --scope chat`); `changelog.d/` fragment dropped.
