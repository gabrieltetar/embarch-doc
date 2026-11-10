# 016 — A chat whose folder was deleted says the folder is missing, not "claude not found"

**State:** done
**Source:** Linear issue EMB-75, filed by a session
**Issue:** EMB-75
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

When a chat's working folder no longer exists, the next message's error names the folder and says it no longer exists, so the owner knows to recreate it or start a new chat. A missing `claude` binary still reports as it does today.

Today, after a chat's process closes (an idle close), the next message respawns `claude --resume` with the chat's folder as `cwd`. When that folder is gone, Node's `spawn` fails with `ENOENT`, and the error handler reports every `ENOENT` as a missing binary:

```
spawn resume mode=auto
spawn failed: claude not found: claude
1 message(s) not taken before the exit: back in the draft
```

Node gives a missing `cwd` the same code as a missing executable: `spawn('ls', {cwd: '/nonexistent'})` emits `ENOENT`, message `spawn ls ENOENT`. So the handler has to tell the two apart itself, for example by checking the `cwd` before or after the failure.

## Why now

Found while tracing a chat that could not be answered after its landing deleted its folder, 2026-11-05. The error sent the reader after a healthy Claude Code install.

## Where to look

- `src/wire/chat.ts` `proc.on("error", …)` — maps every `ENOENT` to `claude not found: <claudePath>`

## Done when

- [x] With the chat's folder deleted, sending a message shows an error naming the missing folder, not `claude not found`.
- [x] A test covers a resume into a folder that no longer exists.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-chat` docs updated where they describe the error, `changelog.d/` fragment dropped.
