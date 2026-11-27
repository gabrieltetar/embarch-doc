# 048 — The 💡 cards checks pass under load

**State:** done — late, never missing: the wait's deadline sat on the runner's clock; waitAssist now polls on the page's clock for 15 s (chat decision 120); 23 of 24 valid loaded runs pass, the one red is EMB-578
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

- [x] The cause is named as late or never sent, with the evidence that decided it.
- [x] Twenty full `npm run test:webview` runs pass under load (a parallel
      `cargo test` in another suite repo plus about two dozen shell busy loops),
      and a run with the fix removed fails as before.
- [x] Gate green (`npm test` with the desk binary, per `gate.md`).

## Notes

- Evidence: before the change, 6 of 12 loaded runs failed on the cards checks, and each failure's page still held the request when asked 15 s later (decision 120). Load was 24 busy loops (no parallel `cargo test`; the other workers' builds stood in) with 4 to 10 parallel runs.
- Fix removed: the same file with a 6 s stall of the runner injected after the draft is typed fails five 💡 checks; with the fix it passes. A natural loaded run with the fix removed failed 0 of 12 in later batches, so the stall is the reproduction, not luck.
- Fix in: 23 of 24 valid loaded runs pass; the one red is the ghost-text pause check, filed as EMB-578. Four more runs crashed with `fetch failed` because port base 6660 lands on a port fetch refuses (6667-6669): not the product.
- One eleven-of-twenty burst of the cards failure at the 5 s page-clock deadline went unexplained (logs lost); the deadline is 15 s because of it.
- `npm test` hung once under the busy loops (no CPU, in a wire test) and passed unloaded: 436 tests, 433 pass, 3 skip. Not looked into.
