# 012 — `embarch-ui/spec.md` says the UI reaches Core over `GET /logs/stream`; it does not

**State:** claimed by agent/ui/012-spec-names-the-real-log-path, 2026-09-06 21:00
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

## Reserve (supervisor, leg 026 — measured at dispatch)

`embarch-ui/spec.md` is **7,653 / 10,240 B (74.7%)**, comfortably out of reserve — the file you are
fixing has room. Two `embarch-ui` decisions files are in reserve and **neither is where this work
goes**: `decisions/study-designer.md` 11,164 / 12,288 (90.9%, filed as `tasks/ui/011`, `open`) and
`decisions/trace-view.md` 11,080 / 12,288 (90.2%, filed as `tasks/ui/009`, `blocked`).
`decisions/debug-tab.md` is 4,828 and is the obvious home if this warrants a numbered decision at
all — **and it probably does not**: correcting a spec line to match shipped code records no choice.
Say which you did and why. If your work pushes any file into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

## Scope note from the supervisor — one task, but read the whole block

This is a small edit and the temptation is to change exactly one line. **Do read the entire
architecture block in `embarch-ui/spec.md` before you edit it.** One wrong dependency arrow in a
block that nothing checks is evidence about that block, not just about that line: `check-links.py`
sees a link that resolves, `check-staleness.py` only fires on a row that *disagrees* with a
sub-project doc, and nothing at all compares a stated HTTP dependency against the code that would
make the call. If another arrow in that block is also unsupported, fix it in the same unit and say
so; if they all hold, say that too — a checked "the rest is right" is worth more than silence. This
stays inside `embarch-ui/spec.md`, so it is one task in one sub-project.

**Do not widen into `embarch-core`.** `/logs/stream` still exists and `embarch-core` decision 44
deliberately keeps it; this task is about what the UI's spec *claims*, not about retiring anything.

## Why now

`embarch-core` decision 44 (landed by core/006) turns on `/logs/stream` having
no consumer today. That reasoning and this spec line contradict each other, and
whichever is read first wins.

## Done when

- [ ] `embarch-ui/spec.md`'s architecture block describes how the Debug tab
      actually reaches Core (poll of `/logs/recent`), or the code changes to
      match the spec and the spec says which.
- [ ] Gate green.
