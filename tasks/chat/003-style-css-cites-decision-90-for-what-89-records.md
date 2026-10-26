# 003 — A stylesheet comment cites a decision number chat has never issued, for the rows 89 records

**State:** done — agent/chat/002-agent-card-shows-the-hand-back, 2026-10-26
**Source:** `chat/001`'s reviewer, 2026-10-25 (below its bar, filed by the supervisor so it is not lost when the log folds).
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`webview/shared/style.css:571` (embarch-chat `82b82e0`) opens the block for the CLI-sent rows with
`/* What the CLI sent Claude (90): … */`. The decision `chat/001` wrote is **89**
(`embarch-chat/decisions/timeline.md`); chat has issued no number above it. When done, the comment cites 89,
and a grep of `src/`, `webview/` and `test/` for the same unissued number finds nothing else
pointing at a decision that does not exist.

## Why now

A citation to a number nobody has issued is silent until that number is issued for something else,
and then it points at the wrong decision with nothing failing. It is one line, so fold it into the
next `chat` unit that touches the webview (`tasks/chat/002` is the likely one) rather than
dispatching it alone.

## Done when

- [x] The comment cites 89; no other reference to a nonexistent chat decision remains.
- [x] Gate green (`../../../embarch-fleet/gate.md`, the npm bullet).
