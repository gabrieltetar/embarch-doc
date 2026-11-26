# 047 — The long-chat scroll check settles before it reads

**State:** done — the follow was a post-paint effect; now a layout effect, 20 loaded runs of the scroll check green
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

- [x] The long-chat scroll check passed in all 20 runs of `npm run test:webview` while a loop of `cargo test` in `embarch-topology` ran (about 36000 rounds of it by the end, the machine otherwise idle). The suite as a whole did not: 8 of 20 runs failed a different check ("no cards request in 5000 ms", four 💡 checks), filed as EMB-574. Isolated, the scroll check alone failed 16 of 25 runs under 24 busy loops before the fix and 0 of 25 after.
- [x] It still fails if the timeline stops following the reply: with the layout effect's `el.scrollTop = el.scrollHeight` removed it failed "at the bottom while it streams"; restored.
- [x] Gate green (`npm ci`, `build`, `typecheck`, `npm test` with the desk binary: 428 pass, 3 skipped; `npm run test:webview` per the above).

## What it was

A product race, not the test: the follow in `webview/chat/index.tsx` was a `useEffect`, which Preact runs after the next paint, up to 100 ms late on a loaded machine. A read or scroll event in that gap saw the grown timeline above the bottom. It is now a `useLayoutEffect` (chat decision 118); the test is unchanged, since `send` already settles.
