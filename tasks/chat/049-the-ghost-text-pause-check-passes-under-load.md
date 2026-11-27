# 049 — The ghost-text pause check passes under load

**State:** claimed by agent/chat/049-the-ghost-text-pause-check-passes-under-load, 2026-11-26 18:14
**Source:** EMB-578 — the ghost-text pause check fails under CPU load
**Issue:** EMB-578
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`test:webview`'s check "Haiku's ghost text after a 300 ms pause, streamed; Tab
takes it; the next keystroke cancels a stale call" asserts that no ghost request
was posted before the pause, after a `sleep` on the runner's side. Under CPU load
the runner's sleep and the page's timer drift apart, so the request is already
posted when the assertion reads it, and the check fails with "not before the
pause". It was seen 3 times in about 60 loaded runs while `chat/048` worked on the
💡 cards checks.

`chat/048` fixed the same shape for the cards checks (chat decision 120,
`decisions/assistant.md`): `waitAssist` polls the page's own posts against a
deadline on the page's clock. When this is done:

- **The "not before the pause" assertion measures the pause on the page's
  clock**, not with a runner-side `sleep`: what it asserts is that the page posted
  no ghost request until 300 ms of the page's own time had passed since the last
  keystroke.
- **It still catches a real early post.** Show it: with the page's pause
  shortened (a test-only change you revert), a loaded run fails the check.
- **Product code changes only if you find the page itself posting early.** If you
  do, say so with the evidence, as `chat/047` did for the timeline follow.

Report the loaded-run counts before and after, the load you used, and anything
you could not explain. `chat/048` left one: a burst of failures on a page-clock
deadline that a slow driver reply does not explain. If you see it again, write it
down.

## Where to look

- `test/webview.e2e.mjs`: the check above, its
  `assert.equal(await lastAssist("ghost"), undefined, "not before the pause")`,
  and `waitAssist`
- `embarch-doc/embarch-chat/decisions/assistant.md` (120, the page-clock wait)

## Where the doc goes

A new chat decision beside 120 in `decisions/assistant.md`, or amend 120 in place
if the new check is the same mechanism applied to one more assertion. Say which
you chose and why.

## Done when

- [ ] The check passes under load, with before and after counts in the decision.
- [ ] A loaded run with an early post still fails it.
- [ ] Gate green: `npm ci`, `build`, `typecheck`, `npm test`, `test:webview`.
