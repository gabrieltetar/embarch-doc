# 011 — An Edit or Write diff in the timeline is one line until opened

**State:** claimed by agent/chat/011-the-inline-diff-is-one-line-until-opened, 2026-11-09 20:34
**Source:** Linear issue EMB-58, filed by the owner
**Issue:** EMB-58
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

In the timeline, an Edit or Write diff is collapsed to one line — the file name and `+N −M` — and a click expands it in place; a second click collapses it. A permission card keeps its diff open, because the owner decides on it there.

Today `DiffView` renders the diff open, up to 40 lines (24 in a permission card), in a `.diff` box with `max-height: 280px` and its own scroll, so a few edits fill the screen.

## Why now

The owner asked for it.

## Where to look

- `webview/chat/tools.tsx` `DiffView` — the inline diff and its line limit
- `webview/chat/cards.tsx` — the permission card's diff, which stays open
- `webview/shared/style.css` — `.diff`
- `test/webview.e2e.mjs` — the Edit/Write tests

## Dispatch notes

- `tasks/chat/010` makes the chat wrap instead of scrolling sideways, `.diff` included. Whichever lands second rebases; do not do 010's work here.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] An Edit or Write in the timeline shows one line with the file and `+N −M`, and expands in place on click.
- [ ] A permission card for an Edit or Write still shows its diff open.
- [ ] An e2e test covers both.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-chat` docs updated, `changelog.d/` fragment dropped.
