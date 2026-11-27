# 049 — The ghost-text pause check passes under load

**State:** done — the pause is measured on the page clock; 40/40 loaded runs pass (old 0/40), a 100 ms pause fails 38/40
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

- [x] The check passes under load, with before and after counts in the decision.
- [x] A loaded run with an early post still fails it.
- [x] Gate green: `npm ci`, `build`, `typecheck`, `npm test`, `test:webview`.

## Outcome

Decision 121 (new, beside 120). Load: 24 busy loops, 8 parallel runs of the ghost check alone, 5 rounds each (40 runs). Old check 0 of 40 pass (all "not before the pause": the runner's 150 ms sleep drifts far past the page's 300 ms timer); new 40 of 40. Early-post proof: `GHOST_MS` = 100, reverted, fails 38 of 40 (101 to 267 ms reported). The page never posted before 300 ms in any run: no product change. Not seen: chat/048's burst of failures on a page-clock deadline; the ghost wait uses the 15 s `waitAssist` and never timed out. Not explained: why 40 of 40 old failures here against 3 in about 60 before; this load was heavier than chat/048's, and the old assertion is only as good as the machine's idle time.
