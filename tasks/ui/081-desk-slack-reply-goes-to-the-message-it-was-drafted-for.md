# 081 — A Slack reply from the Desk goes to the message it was drafted for, not whatever now sits at that index

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-ui finding 2), verified by Opus against embarch-ui@aa5ffdaa
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The Desk tab's Slack bar identifies a message by its position in `view.slack.items`. The Draft and Send handlers look the item up by that position when clicked (`assets/desk.js:1071`, `:1083`). A pushed view replaces `view` unconditionally (`:1305`), but the re-render is held back while focus is anywhere inside the Slack bar (`editing()`, `:1298-1301`). So the buttons and the reply box on screen keep the old positions while `view` already holds the new list. The desk orders that list unread first, then newest first (embarch-desk `src/slack.rs:172`), and the UI pushes a fresh view every 10 s (`src/desk.rs:117`). One new mention, or one message changing to read, shifts every position. The usual case: someone clicks Draft reply, edits the draft for a few seconds, and clicks Send. Send then posts with another message's `account` and `channel` and the drafted message's `thread_ts`, as the user. Draft can also draft against a different message than the card shown. Suggested direction: make the identity travel with the card, not with its position. One option is to take a copy of the message's account/channel/ts when Draft is clicked and reuse it for Send. Holding the re-render back while someone types is deliberate (the comment at `:1290-1295`) and stays.

## Why now

This is the one finding in the review that sends something the user did not mean to send: a message posted under their own Slack identity, into a conversation they were not looking at. The trigger is ordinary use: a draft takes a `claude -p` call, and new mentions arrive while it runs.

## Done when

- [ ] A browser check (`tests/browser/drive_desk.py`, or a sibling script) captures the page's own `/api/desk/slack/*` requests, so nothing reaches a real desk or Slack. It renders two Slack items, clicks Draft reply on the second, pushes a view that adds a new unread item at the top, then clicks Send. The captured reply request must carry the second message's account, channel and thread.
- [ ] The same holds when an item is removed from the list or changes to read between Draft and Send.
- [ ] A reply box whose message has left the list says so, and sends nothing.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
