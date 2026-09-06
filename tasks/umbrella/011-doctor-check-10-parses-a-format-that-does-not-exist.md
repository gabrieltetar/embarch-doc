# 011 — Check 10 parses a `claude mcp get` format that does not exist

**State:** done 22:12
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

- [x] Check 10 reaches a real verdict on the owner's machine, from a terminal,
      against the registration that is actually there. **Host-side only — see
      the debt below; it needs no `claude` on `PATH` any more, which is the
      change that makes a real verdict reachable at all.**
- [x] It does not report `not registered` for a connected server, whatever name
      that server carries — the entry is found by the `embarch-api` binary it
      names, not only by the key `embarch`.
- [x] A decision entry records which route won and what it now claims:
      **[decision 40](../../embarch-umbrella/decisions/doctor.md)**, with
      decision 23 amended in place and saying which half of it was replaced.
- [x] `open.md`'s `claude mcp get` bullet is gone; the environment half survives
      as its own bullet, shrunk to the residue `env` did not cover.
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped.

## Added by leg 012 at dispatch (2026-09-05 22:12)

**`decisions/doctor.md` was split by mission an hour ago and decision 23 did not move.**
`umbrella/012` took decisions 11, 37 and 39 out into a new
`embarch-umbrella/decisions/reporting.md` ("what `doctor` and `status` hand back"), leaving
18, 19, 22, 23 and 31 in `doctor.md` ("the check chain, and the states it refuses to
conflate"). **Decision 23 is yours to amend or retire and it is still in `doctor.md`** —
9,454 / 12,288 B, plenty of room. If whatever you build turns out to be about the *shape of
what a consumer reads back* rather than about the check chain, `reporting.md` is where it
belongs; that is a judgement, not a rule.

**Decision 37 is the `--json` `code` field**, now in `reporting.md`, and check 10 is one of
its four users. Whatever verdict you make reachable, keep its `code` — a check that reaches
a real verdict without a stable code is half-built. **Do not "fix" decision 37's stale body
sentence** while you are in there: it says "check 10 is the only user today" and that is
already filed as `tasks/umbrella/015`, which will conflict with you if you both touch it.

**Reserve:** nothing in the suite is in reserve. `embarch-umbrella/spec.md` is 9,203 / 10,240
B and `open.md` is 4,596 / 5,120 B — **89.8%, a hair under the line**, and this task removes
a bullet from `open.md`, so it should pay for itself. If it does not, you owe a ride-along
compaction of that file inside your own commit rather than a new task
(`tasks/umbrella/009` is `blocked` on `In flux: yes`, and a blocked compaction task parks the
pass, not the reserve — `DOC-COMPACTION.md` §2). Measure with
`python3 scripts/check-doc-size.py --pressure` before you report.

**You may not run `claude mcp get`, spawn the MCP server, or touch the live Core.** The task
records what the owner already observed by hand; treat that transcript as the evidence and
do not go looking for more of it yourself. Anything that needs a live run is a
**hardware-verification debt** written into this file — there is already one owed for the
next live `embarch doctor`, and yours rides on it for free. Say exactly what a live run
should print, before it runs; that prediction is what makes the run worth something.

## Closed 2026-09-05 by agent/umbrella/011-check-10-parses-a-format-that-does-not-exist

**Route chosen: read `~/.claude.json`, keep the spawn** ([decision 40](../../embarch-umbrella/decisions/doctor.md)).
The `Status: ✔ Connected` route was not rejected on taste — it **loses on the third
finding**. Reading `Status:` still means running `claude`, and `claude` is not on `PATH`
from a terminal, so that route reaches *no* verdict on the machine the check was written
for. Reading a config file needs no CLI at all. It would also have handed the verdict back
to the CLI's own health check, which is the thing decision 23 built a spawn to reproduce
independently.

**`Environment:` half-survives.** The registered entry's `env` map is now applied on the
spawn, because reading the config structurally gave us the map that `claude mcp get`'s
output never showed. What does **not** survive: the server still starts in `doctor`'s
environment rather than the CLI's, and that is now the whole of the stated gap
([open.md](../../embarch-umbrella/open.md)).

**Codes unchanged, deliberately.** A remote-transport (`http`/`sse`) registration is
readable but unspawnable and shares `unreadable-entry` rather than taking a seventh code:
`init` only ever writes stdio, and both states are the same actionable thing. Decision 37's
list of check 10's codes therefore stays correct and was not touched — `tasks/umbrella/015`
owns that entry.

## Hardware-verification debt — rides on the next live `embarch doctor`

**Nothing here was run against the owner's machine.** No `claude mcp get`, no MCP spawn, no
live Core. The predictions below are what makes the run worth something; write down which
one happened.

Run `embarch doctor` **from a terminal, in a firmware repo that has the registration** —
one of the five directories whose `projects.<cwd>.mcpServers` entry exists. Expected:

    [10] PASS  MCP server registered and answering
               registered as `embarch-api` (local scope), and it answered initialize (embarch-api)

`--json`: `checks[9].code == "handshake-ok"`, `path == null`.

**The honest degraded outcomes, so a reader can tell "the fix missed" from "the fix worked
and the machine changed":**

- Run from a directory with no registration → `[10] FAIL … nothing registered for <cwd>,
  under any name`, code `not-registered`. **This is correct, not a regression** — local
  scope is keyed by absolute cwd and the agent CLI would answer the same there.
- On a machine that never ran the agent CLI → `[10] WARN … no agent-CLI config to read — no
  readable /home/<user>/.claude.json (…)`, code `no-cli`.
- `[10] FAIL … registered as `embarch-api` (local scope), but the handshake failed — …`
  (`handshake-failed`) means the binary named in the config does not start; the detail
  quotes its stderr. **The most likely real cause is the environment residue above**, not a
  bad registration — the fix line already says re-adding it fixes nothing.
- **`unreadable-entry` should now be unreachable here.** If it appears, that is a genuinely
  malformed or remote-transport entry, not the old "the parse was wrong" — that meaning is
  gone.

If the PASS line appears, `open.md`'s "never run live" clause closes and only the
environment residue stays open.
