# 036 — The Promptu card test waits for the state it asserts on

**State:** done — card test waits for the state event carrying the patterns; 4/20 failed before, 0/20 after
**Source:** `chat/035`'s gate (2026-11-24 log entry): the worker saw the test fail on unchanged `main` 2 of 3 runs; the supervisor's gate run passed it
**Issue:** EMB-294
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

The test in `test/promptu.test.mjs` whose name starts "the card: on by
default" fails about two runs in three on `embarch-chat`'s own `main`, with no
change applied. It looks like a race over which load emits the first `state`
event: the test takes the first one and asserts on it, while more than one
load can emit first. When this is done:

- The test passes on every run. Either it waits for the `state` event it
  asserts on (the first one matching, with a bounded timeout) rather than the
  first one emitted, or the service in `src/promptu/` emits its first events in
  a fixed order. Pick the fix that matches what the card promises: if the
  order is part of the service's contract, fix the service; if it is not,
  fix the test.
- Reproduce the failure first and say in the task file how often it failed
  before the fix.
- Check the other tests in `test/promptu.test.mjs` for the same "first event"
  pattern and fix any that share it.

## Why now

A gate that is red one run in two either blocks an unrelated unit or teaches
whoever lands it to rerun until green, which hides a real failure. EMB-294,
filed by `chat/035`'s worker.

**Burndown leg: no new numbered decision.** This should need none; if it
does, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-chat` file is in reserve;
decision 96 (`decisions/promptu.md`) has 204 B left under its per-decision
limit, so do not grow it.

## Result

Cause: the card test took the first `state` event, but patterns and week
status load side by side and each emits one, so the week load could fire first
and the test read empty patterns. Event order is not part of the service's
contract, so the test was fixed: it waits (5 s bound) for the `state` event
after which `patterns` is non-empty. Before: 4 failures in 20 runs. After: 0 in
20. The other tests in the file wait for two `state` events (both loads) and do
not share the pattern. Service and spec unchanged.

## Done when

- [x] The test passes in 20 consecutive `npm test -- test/promptu.test.mjs`
      runs (or the narrowest invocation that runs it), and the count is in
      this file.
- [x] The test waits for the state it asserts on, or the service orders its
      first events deterministically.
- [x] Full `npm test` green with the desk binary from `scripts/desk-gate-bin.py`
      in `embarch-fleet` (`gate.md`'s npm bullet), plus `npm run build`,
      `npm run typecheck` and `npm run test:webview`.
- [x] `changelog.d/` fragment dropped; no `spec.md` change expected unless
      the service's event order becomes a stated promise.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
