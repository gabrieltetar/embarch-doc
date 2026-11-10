# 025 — A chat host test fails on `main` whenever the desk binary is set

**State:** done
**Source:** EMB-134, filed while gating `chat/023` on its merge result, 2026-11-10
**Issue:** EMB-134
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

With `EMBARCH_DESK_BIN` set, `npm test` in `embarch-chat` gives 338 pass, 3
skipped, 1 fail. The failing test is `test/host.test.mjs`'s "the page asks for
ghost text and cards; the host streams Haiku's answers back", at its "the cards
call ran" check. Without the binary the test skips, and the merge gate reads a
skip as not red, so nothing has caught it. The `chat/023` worker stashed its
branch and saw the same failure on `main`; the binary it ran was a desk debug
build from 2026-11-03, a week behind `embarch-desk` `main`.

Two hypotheses, and the check that tells them apart:

- **The binary was stale** and lacks a route or field the test now expects.
- **The test regressed** when a later chat change moved the cards call.

**Next check.** Build `embarch-desk` `main` fresh **without writing to its
checkout**: `cargo build --manifest-path
/home/gabriel/Github/embarch/embarch-desk/Cargo.toml --target-dir
/home/gabriel/Github/embarch/.worktrees/embarch-chat/desk-target` (the target
directory sits beside your worktree, outside every repo). Point
`EMBARCH_DESK_BIN` at the binary it produces and run only
`test/host.test.mjs`, then the whole suite. A pass means the old binary was
stale; a fail is a real regression.

**What you may change.** Only `embarch-chat` and `embarch-doc/embarch-chat/`.
If the cause is in the chat (the test, or the code it exercises), fix it here
with the test that proves it. If the cause is in the desk, **do not touch the
desk**: file it with `scripts/fleet-linear.py file --from worker --project
embarch-desk` and name the issue in this file. Either way, write the cause in
this file's closing section in one or two sentences; the supervisor carries it
to the issue.

**Doc reserve.** `embarch-chat/spec.md` is at 9,373 of 10,240 B, in reserve,
and its compaction task (`tasks/chat/024-compact-chat.md`) is `blocked` on
`In flux: yes`. An investigation should not need `spec.md`. If yours does, keep
the edit inside the file's current size by a verbatim move, and leave 024's
`Must not delete:` items readable. `decisions/promptu.md` (decision 96) has 204 B
left: a new decision on this goes in the file of its subject, never the one with
room.

## Why now

The host suite is the only test that runs the chat against a real desk, and
it has been red whenever it runs. A red that only shows when an optional
variable is set is one nobody sees until it hides a second failure.

## Done when

- [x] The cause is named in this file, and the host suite passes against a
      desk built from `main`, or an issue is filed for what fails and named here.
- [x] If the cause was in the chat, the fix ships with the test that shows it.
- [x] Gate green (`../../embarch-fleet/gate.md`), with `EMBARCH_DESK_BIN` set
      to the fresh build for the `npm test` run.

## Closing

**Cause: the test regressed, not the binary.** Against a desk built fresh from `main` (1997108) the failure is the same. Decision 97 made the cards call conditional on the desk's references; in `test/host.test.mjs` this window gets none, so no cards call is made, yet the test still asserted `calls().some(task === "cards")`. The old binary was not at fault. Fixed by asserting the opposite (no cards call without references), matching `assistant.test.mjs`'s 97 test. With the fresh desk: `host.test.mjs` 61/61, `npm test` 339 pass, 0 fail, 3 skipped.

**Debt:** `npm run test:webview` could not run: port 4989 was already in use (EADDRINUSE; another process held it, and I did not kill it). It fails identically with my change stashed, so it is environmental. Needs one run on a free port.
