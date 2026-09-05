# 011 — Check 10 parses a `claude mcp get` format that does not exist

**State:** open
**Source:** the owner's live `embarch doctor` run, 2026-09-05, plus running `claude mcp get` by hand — closing `open.md`'s "nothing here has ever seen its output"
**Scope:** umbrella
**Hardware:** none

## What

`open.md` recorded that check 10's parse target was **assumed rather than
observed**. It has now been observed, against Claude Code **2.1.261**, and the
assumption is wrong three separate ways.

**1. There is no `Command:` line.** The whole output for a healthy local stdio
server is:

```
embarch-api:
  Scope: Local config (private to you in this project)
  Status: ✔ Connected

To remove this server, run: claude mcp remove embarch-api -s local
```

`parse_registered_command` requires `Command:` and returns `None` without it, so
it can only ever produce `UnreadableEntry` → `Warn`. **The 10 s JSON-RPC
handshake decision 23 is built around is unreachable**, and so is its budget.
There is no `--json` on `mcp get` or on `mcp list`. The command and args are in
`~/.claude.json` under `projects.<cwd>.mcpServers.<name>` — `command` and `args`,
already structured:

```json
{ "embarch-api": { "command": "…/embarch-api", "args": ["--config", "…/embarch.toml"] } }
```

**2. The name is wrong for a real machine.** `MCP_SERVER_NAME` is `embarch`;
the registration that actually works here is `embarch-api`. `doctor` in that
repo reports `[10] FAIL … not registered` **beside a server the same session is
using**, and its fix line tells you to add a second registration under the other
name.

**3. `claude` is never on `PATH`.** It lives inside the VS Code extension, at
`~/.vscode-server/extensions/anthropic.claude-code-*/resources/native-binary/claude`.
From a terminal, check 10 reaches only its `no-cli` arm. That arm's `Warn` is
correct posture and the *reason* is not what anyone would guess.

Fix candidates, and this is the real question: read `~/.claude.json` directly and
keep the spawn; or drop the spawn and trust `Status: ✔ Connected`, which is the
CLI's own health check and is the thing decision 23 built a spawn to reproduce.
**Either changes what decision 23 claims**, so it needs a decision entry, not a
patch. Whichever wins, `Environment:` is still ignored and the server would be
spawned in doctor's environment rather than the registered one.

## Why now

Check 10 exists because *registered* is not the same as *working* — it replaced a
check that returned Pass on a zero exit. As shipped it cannot reach either of its
real verdicts on the machine it was written for, and its `Warn` reads as "cannot
tell" rather than "this check is inoperative".

## Done when

- [ ] Check 10 reaches a real verdict on the owner's machine, from a terminal,
      against the registration that is actually there.
- [ ] It does not report `not registered` for a connected server, whatever name
      that server carries.
- [ ] A decision entry records which route won and what it now claims; decision
      23 is amended or retired per `DOC-CONVENTIONS.md`, never silently reworded.
- [ ] `open.md`'s `claude mcp get` bullet loses whatever this answers, and keeps
      the `Environment:` half if it survives.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
