# 021 — Six chat host tests fail against the local desk binary, and the gate skips them

**State:** open
**Source:** Linear issue EMB-118, filed by the worker on `chat/013`
**Issue:** EMB-118
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`EMBARCH_DESK_BIN=<embarch-desk>/target/debug/embarch-desk node --test test/host.test.mjs` on `embarch-chat` `fad3fe8` gave 54 pass, 6 fail. The six: a pending Edit's diff tab (decision 64), a plan as a Markdown tab (77), Always allow from the card (78), a message waiting across a reload (63, 72), a new chat reloaded before the CLI's first message (63), and Start work with Promptu (96). Most fail at about 5 s, which reads as a timeout.

Known: the `chat/013` worker saw five of them fail identically with its change stashed, so they predate it; the only desk binary on the machine then was built 2026-11-03, and `embarch-desk` `main` has moved many times since; the fleet's gate runs `npm test` without `EMBARCH_DESK_BIN`, where these skip.

Name the cause. Fix it if it is in `embarch-chat`; file it as a bug if it is in the desk.

## Why now

A test the gate never runs protects nothing, and five units of chat work have landed on top of these six since anyone saw them pass.

## Where to look

- `test/host.test.mjs` — the six tests
- `test/desk.test.mjs`, `test/resume.test.mjs` — how the desk-gated tests find the binary

## Dispatch notes

- **A desk built from `embarch-desk` `main` (`4b83b5e`) is already at `/home/gabriel/Github/embarch/.worktrees/embarch-chat/desk-target/debug/embarch-desk`** — built by the supervisor with `--target-dir` outside every repo tree. Use it as `EMBARCH_DESK_BIN`. Do not build in, or write to, the `embarch-desk` checkout: it is another sub-project's repo.
- Run the whole of `test/host.test.mjs` with that binary first. All green means the binary was stale: say so in the task file and the changelog fragment, with the pass count, and that is the finding. Some still red means a real break: find out whose.
- A desk-side cause is a `bug` filed with `scripts/fleet-linear.py file --from worker --project embarch-desk`, naming the route or field, and this task closes on that filing. A chat-side cause gets fixed here, with the test that showed it.
- Whether the fleet's chat gate should run these with a desk binary is a gate rule, and `gate.md` is not yours; if you think it should, say so in your report, not in a doc.
- Burndown is on: no new numbered decision.

## Done when

- [ ] The cause is named in this file, then fixed or filed as a bug.
- [ ] `test/host.test.mjs` passes against a desk built from `main`, or each test still failing names the filed bug that owns it.
- [ ] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.
