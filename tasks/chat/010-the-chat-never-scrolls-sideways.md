# 010 — The chat never shows a horizontal scroll bar

**State:** open
**Source:** Linear issue EMB-57, filed by the owner
**Issue:** EMB-57
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

No element of the chat page scrolls sideways. Long text wraps (`white-space: pre-wrap`, `overflow-wrap: anywhere` for long tokens), flex-row children shrink and truncate with an ellipsis, and table cells wrap.

Today several elements scroll horizontally:

- `.timeline` sets `overflow-y: auto` and no `overflow-x`, which CSS computes as `auto`, so one row wider than the column gives the whole timeline a horizontal bar. The rows that can overflow are flex rows with `white-space: nowrap` children that cannot shrink: `.tool .name`, `.tool .st`, `.subject-key` (`flex: none`) and `.tool.run > .line .count`.
- Code blocks: `.codeblock pre { overflow-x: auto }` with `code { white-space: pre }`.
- Tables: `.tablewrap { overflow-x: auto }`.
- Edit and Write diffs: `.diff { overflow: auto }` with `.diff div { white-space: pre }`.
- The compaction summary (`details.compacted .compact-summary`) and what went with a message (`.ctx-row pre`), both `overflow: auto`.

## Why now

The owner asked for it. No decision covers horizontal scrolling; decision 91 is about the vertical bar's place, so this likely wants a short new decision recording the rule.

## Where to look

- `webview/shared/style.css` — every selector listed above
- `test/webview.e2e.mjs` — nothing checks horizontal overflow today; the only `scrollWidth` check is on `.status-line`

## Dispatch notes

- `tasks/chat/011` collapses the inline diff to one line. The two touch `.diff` from different sides; whichever lands second rebases. Do not do 011's work here.
- No `embarch-chat` doc is in reserve at the split.

## Done when

- [ ] With a 400-character unbroken line in a code block, a diff, a table cell, a tool name and a message, no element in the chat page has `scrollWidth > clientWidth`.
- [ ] An e2e test asserts it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-chat` docs updated, `changelog.d/` fragment dropped.
