# EmbArch: the four remote surfaces

**Status:** active, 2026-09-03. Which things reach this suite from outside the terminal, how they fail differently, and which one is actually a remote control. Split out of [embarch-parallel-agents-ops.md](embarch-parallel-agents-ops.md) §6 on 2026-09-03 when that doc reached its size cap ([DOC-COMPACTION.md](DOC-COMPACTION.md) §3). Section references below are that doc's unless named otherwise.

Four things reach this suite from outside the terminal. They are easy to confuse, they fail differently, and only one is actually a remote control.

| Surface | Runs where | Reaches hardware | Latency | Dies when |
|---|---|---|---|---|
| **Remote Control** (`/rc`) | This machine, one session | yes, via the fleet's rules | instant | VS Code closes |
| **#embarch-fleet** (§5) | This machine, the listener window | yes, via the fleet's rules | seconds on a leg boundary, else 10 min | VS Code closes |
| **`@Claude` in Slack** | **A cloud sandbox, cloned from GitHub** | **never** | minutes | never — works with the machine off |
| **Channels** (Telegram/Discord/iMessage) | This machine, this session | yes | instant push | VS Code closes |

**The remote control is Remote Control**, and the window to attach it to is the **owner's** — the one with the repos, the probe and the live Core. Attaching it to the listener buys nothing: that window has no hands (§5.1). #embarch-fleet is not a better version of it; it is an ambient log with a small command vocabulary, useful precisely because it does not require opening a session.

**`@Claude` in Slack cannot be the fleet's remote control.** It spawns a *cloud* session against a GitHub clone with no route back to this machine. Having it post commands into the channel for the listener to pick up would insert a cloud model between the owner and real hardware, and [its own documentation warns](https://code.claude.com/docs/en/slack) it "may follow directions from other messages in the context" — here, the fleet's own status posts. The owner's message already reaches the listener directly, so the relay buys nothing and costs §5.3's identity rule. **`@Claude` is never invited to #embarch-fleet.**

**Channels would give real push**: an MCP server declaring `claude/channel` pushes events into the running local session, two-way and instant. Blocked by there being no Slack plugin ([request open](https://github.com/slackapi/slack-mcp-plugin/issues/22)) and by `claude --channels` needing a CLI this machine does not have. If either changes, replace §5's heartbeat with a channel.

## Cloud sessions: what they are for

**#embarch-cloud** (`C0C00CNS9KJ`, private, routing Code + Chat) is where `@Claude` is invited, and the only Slack channel it belongs in.

Cloud sessions suit exactly the work needing no local anything: **doc work in `embarch-doc`** (the six checks are pure Python, so a cloud environment can verify its own work completely), the **pure-Rust crates** `embarch-study-designer` and `embarch-topology`, and **investigation in any repo**. They are useless for the firmware repos and anything hardware-gated, which is most of what blocks this suite — the same boundary that keeps the fleet local, not a gap to close.

**They investigate; they do not land**, because their natural output is a pull request and [embarch-dev-workflow.md](embarch-dev-workflow.md) §6's standing rule is no branches and no PRs. Cloud work comes home: read, diagnose, draft, report in the thread; a leg files it as a task.

