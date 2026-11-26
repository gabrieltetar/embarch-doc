# 047 — The long-chat scroll check settles before it reads

**State:** claimed by agent/chat/047-the-long-chat-scroll-check-settles-before-it-reads, 2026-11-26 11:57
**Source:** EMB-571 — a webview check of a long chat's scroll fails under load
**Issue:** EMB-571
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`test/webview.e2e.mjs` has a check that a long chat sticks to the bottom while
a reply streams, stays where the reader left it when scrolled up, and follows
again once back at the bottom. It asserts `atBottom()` right after `send(...)`
with no settle, at the lines "at the bottom while it streams" and "and when it
lands". On 2026-11-25 it failed three runs of three on `main` at two different
assertions (the machine was running cargo builds for two of them), while the
gate that landed the same code an hour and a half earlier passed it. Every chat
unit's gate runs `npm run test:webview`, so a timing-dependent red there either
blocks a good unit or teaches the gate's reader to discount reds; `chat/045`
landed past it.

When this is done:

- **The check reads the scroll position after the timeline has rendered what
  was sent** — the same settle the scrolled-up half already uses, or a wait for
  the frame — not on the next tick.
- **The claim is unchanged**: at the bottom while streaming, kept in place when
  scrolled up, following again once back at the bottom, at the bottom when the
  reply lands. Loosening an assertion until it passes is not the fix.
- If the follow itself turns out to be racy (the timeline really does fall
  behind under load), that is a product bug: fix it in `src/`, and say which it
  was in the commit message.

## Where to look

- `test/webview.e2e.mjs`, the check near line 2805, and its `atBottom`, `send`
  and `settle` helpers
- The webview's scroll-follow code it exercises (search `src/` for the
  stick-to-bottom logic the check names)

## Where the doc goes

No decision is expected for a test-only fix. If the follow logic changes, a
chat decision says what it guarantees. `decisions/references-kinds.md` is near
its reserve line and `promptu#96` has 204 B left; do not grow either.

## Done when

- [ ] The check passes twenty runs in a row of `npm run test:webview` while a
      parallel `cargo test` (any suite repo) loads the machine. Say in the task
      which repo's tests you ran as the load and how many runs passed.
- [ ] It still fails if the timeline stops following the reply (checked once
      by breaking the follow by hand, then restored).
- [ ] Gate green (`npm ci`, `build`, `typecheck`, `npm test` with the desk
      binary, `npm run test:webview`, per `gate.md`).
