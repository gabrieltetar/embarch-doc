# notes/goals: the goals of EmbArch as a whole

The research behind a future `suite/goals.md`: **what EmbArch sets out to be, stated concisely for a reader outside the project.** Gathered in an interview with the owner on 2026-11-16. **Every answer recorded in these files is the owner's, 2026-11-16, unless it sits under Open.**

**[00-goals.md](00-goals.md) is the statement itself**, kept short; the other files hold the answers and the evidence behind it. **The HIL notes' goals ([hil/00-goals.md](../hil/00-goals.md)) are for review, these are for the world**: the two state the same idea and can be reviewed against each other (owner).

## Files

| File | Subtopic |
|---|---|
| [00-goals.md](00-goals.md) | **The statement**: the vision, what EmbArch is built for, ten goals in four themes with a status each, the non-goals, who may use it |
| [01-scope.md](01-scope.md) | Who it is for, the product against the owner's own tooling, a community project, firmware, hosts and agents, the trinity, the goals offered and cut |
| [02-phases.md](02-phases.md) | Build now, stabilise on the owner's call, scale inside the trinity, then beyond it |
| [03-status.md](03-status.md) | The evidence behind each status line, taken from the docs |

## Vocabulary

Written for a reader new to EmbArch, so each word is the plain one.

- **LLM agent**: a coding agent driven by a large language model; Claude Code is one. **"LLM", never "AI"** (owner, [01](01-scope.md#firmware-hosts-and-agents)).
- **DUT**: the device under test, the board running the engineer's firmware.
- **Bench**: the DUT, plus the boards and instruments wired to it.
- **Core**: `embarch-core`, the service that owns the debug probes and serial ports; every hardware call goes through it.
- **Study, test, live access**: three ways to run hardware-in-the-loop: a measurement answering a question, conformance with a verdict, an instant read or action.
- **The trinity**: one engineer, one Core, one machine; the boundary the design relies on (owner, [01](01-scope.md#the-trinity)).
- **Met, partly met, not yet**: a goal's state against the codebase ([03](03-status.md#the-shape)).
