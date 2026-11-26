# 048 — The 💡 cards checks pass under load

**State:** claimed by agent/chat/048-the-cards-checks-pass-under-load, 2026-11-26 14:29
**Source:** EMB-574 — the 💡 cards checks fail under CPU load with no cards request
**Issue:** EMB-574
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Under CPU load, `npm run test:webview` goes red on checks about the 💡 cards
with `no cards request in 5000 ms`, thrown by `waitAssist` in
`test/webview.e2e.mjs` (about line 1484) while it waits for the page to post a
`cards` request. Four checks have hit it: "the 💡 by keyboard, as
IntelliSense", "Tab while a menu shows", "a 💡 open while the panel narrows
measures its previews again", and "while ↓ has focused a row, the pointer over
another marks it". It was 8 of 20 loaded runs on a branch, and 1 of 3 runs at
`embarch-chat` `701a019` on a near-idle machine, so it is on `main` too.

`chat/047` (EMB-571, chat decision 118) found the same symptom in the
long-chat scroll check was a product race — a `useEffect` that ran after the
next paint — not a slow test. Find which this is before changing anything:

- **Late**: the `cards` post is sent, behind a debounce or a timer that runs
  late in a loaded headless browser. Then the wait, not the product, is wrong.
- **Never sent**: a state the page reaches under load where it does not post
  at all (an effect ordering, a focus or a measure that lands after the event
  that should trigger it). Then the product is wrong, and a longer wait would
  hide it.

Show the evidence that tells them apart (for instance, the page's own log of
the post, or whether the request arrives after the timeout), fix what it
names, and say which it was in the decision.

## Where to look

- `test/webview.e2e.mjs` — `waitAssist`, `lastAssist`, and the four checks
- `webview/chat/` — the code that schedules or debounces the `cards` post
- `embarch-doc/embarch-chat/decisions/timeline.md` decision 118, for how
  `chat/047` measured its race

## Where the doc goes

A new chat decision if the product changes, or an amendment to the decision
that owns the cards request if only the wait does.
`decisions/references-kinds.md` is near its reserve line, and
`check-doc-size.py --pressure` lists `promptu#96` with 204 B left: do not grow
it. If your work pushes a chat file into reserve, file
`tasks/chat/<NNN>-compact-chat.md` in the same commit per `tasks/README.md`.

## Done when

- [ ] The cause is named as late or never sent, with the evidence that decided it.
- [ ] Twenty full `npm run test:webview` runs pass under load (a parallel
      `cargo test` in another suite repo plus about two dozen shell busy loops),
      and a run with the fix removed fails as before.
- [ ] Gate green (`npm test` with the desk binary, per `gate.md`).
