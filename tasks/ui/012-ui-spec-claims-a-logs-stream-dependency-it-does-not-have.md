# 012 — `embarch-ui/spec.md` says the UI reaches Core over `GET /logs/stream`; it does not

**State:** open
**Source:** core/006 worker, 2026-09-06 — found while surveying `/logs/stream`'s consumers
**Scope:** ui
**Hardware:** none
**Owner:** no

**Filed by the supervisor, leg 025**, from an `inbox/` drop the `core/006` worker wrote into
**its own doc worktree** rather than the main checkout. That worktree is deleted at cleanup, so
the drop existed for about twenty minutes and nowhere else. `Hardware:` re-checked: `none` —
this is a doc correction against sources already read.

## What

`embarch-ui/spec.md:32` lists, under "HTTP + Bearer --> embarch-core", the line
`GET /logs/stream (SSE live tail) · GET /logs/recent (backfill)`.

Only the second half is true. `embarch-ui/src/logs.rs`'s `poll_loop` calls
`core.logs_recent(POLL_TAIL)` on a 2 s interval and republishes the diff over a
`watch` channel; `sse_lines` then relays that as the UI's *own* `lines` SSE
event to the browser. `embarch-core-client` (`client.rs:1163`) has `logs_recent`
and no `/logs/stream` method at all — a grep of the whole suite finds no caller
of Core's `/logs/stream` anywhere outside `embarch-core` itself.

So the UI's live tail is a server-side poll of `/logs/recent`, not an SSE
subscription to Core, and the spec line reads as though Core's SSE stream is a
dependency the UI holds. A later reader deciding whether `/logs/stream` may
change (or go) will conclude it has a consumer when it has none.

Not fixed here: this is `embarch-ui`'s doc and a `core` worker may not edit it.
`embarch-core`'s own decision 44 records the same finding from Core's side.

## Why now

`embarch-core` decision 44 (landed by core/006) turns on `/logs/stream` having
no consumer today. That reasoning and this spec line contradict each other, and
whichever is read first wins.

## Done when

- [ ] `embarch-ui/spec.md`'s architecture block describes how the Debug tab
      actually reaches Core (poll of `/logs/recent`), or the code changes to
      match the spec and the spec says which.
- [ ] Gate green.
