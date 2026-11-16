# Goals notes: where the codebase stands

**Status:** draft, 2026-11-16.

**The evidence behind each status line in [00-goals.md](00-goals.md).** **Taken from the suite's docs on 2026-11-16, not checked against the repos** (the owner's choice); each line cites the doc it came from. [suite/features.md](../../suite/features.md) is the main source, and its **Verified** column is what "on real hardware" means here: `hw` is a real probe or board, `local` a real process with no board, `unit` mocked tests only.

## The shape

**One state per goal**: met, partly met or not yet, **plus one line of evidence** (owner). The three states:

- **Met**: built, and on hardware where the goal touches hardware.
- **Partly met**: some of it built; the rest designed or missing, and said which.
- **Not yet**: designed at most.

## At the bench

| # | Goal | State | Evidence |
|---|---|---|---|
| 1 | Real hands on the bench | Partly met | Flash, reset and serial capture are `hw` ([features](../../suite/features.md), embarch-core); build and flash from the Study Designer were driven on hardware on 2026-09-19 (features, embarch-ui); studies over the dev bench ran on real hardware ([roadmap](../../suite/roadmap.md) milestones 2, 3 and 7). Host studies, SCPI instruments and operator prompts are built but `unit` only, never on a bench (features, embarch-core and embarch-api). Tests and the Live procedure are a [proposal](../../embarch-hil-proposal.md) |
| 2 | The engineer stays in control | Partly met | The bench lease is built host-side only, never against an installed Core or a real second session (features, embarch-core, [decision 93](../../embarch-core/decisions/lease.md)). [agent-guide.md](../../suite/agent-guide.md) §1.1 splits the MCP tools into allow and ask. **One bearer token serves agent and person alike**, and its threat model excludes anyone with access to the machine ([embarch-token.md](../../embarch-token.md)). Refusing every other hardware call while a run is in flight, the two token scopes and the person's acts on a card are a [proposal](../../embarch-hil-evidence-proposal.md) |
| 3 | One path, agent or human | Met, one gap | The MCP server and the CLI are peers over one client crate, `embarch-ui` is Core's second client, and `embarch-topology` is the only code that opens a probe or a serial port ([embarch.md](../../embarch.md) §4). **The gap**: making a saved bench live is in the UI only; a CLI verb for it is in the [HIL proposal](../../embarch-hil-proposal.md) |

## Evidence

| # | Goal | State | Evidence |
|---|---|---|---|
| 4 | Evidence anyone can check | Not yet | Publishing a zip, Core signing its records, the run log and `verify` are designed in the [HIL](../../embarch-hil-proposal.md) and [HIL evidence](../../embarch-hil-evidence-proposal.md) proposals; none is built. **What exists to build on**: a study records the firmware it declares and checks it against the firmware's own header, `hw` (features, embarch-study-designer); Core reports its own binary's hash (features, embarch-core) |
| 5 | Professional practice | Not yet | The six verdicts, limits on measurements, guard bands, uncertainty and the decision rule are designed in [notes/hil/03-test.md](../hil/03-test.md), the report in [06](../hil/06-report-and-publish.md). Today a host study counts lines per tap and **never compares them with an expected value** (features, embarch-core) |
| 6 | Never an inference stated as fact | Met as a rule | A principle of [embarch.md](../../embarch.md) §5. The Study Designer's registry holds names and values only, never a meaning the suite invents ([roadmap](../../suite/roadmap.md) milestone 5); a DUT's protocol is declared by the engineer in an `.eap` file, `hw` (features, embarch-study-designer). **No check enforces it**; it rests on review |

## Understanding

| # | Goal | State | Evidence |
|---|---|---|---|
| 7 | Hardware truth for agents | Partly met | The atlas is built locally on one real two-board product and not yet published (features, "Not yet a sub-project"); `embarch-ui`'s Atlas tab draws it, `local` (features, embarch-ui). The seven-plane rework is a [proposal](../../embarch-atlas-planes-proposal.md) |
| 8 | One timeline | Partly met | The in-DUT trace ran on real silicon: 437,789 bytes in 20 s, zero records lost; Core stamps each frame on arrival so a trace can be placed against every other stream; **no run has compared a trace's placement against a second stream** ([roadmap](../../suite/roadmap.md) milestone 7). Power sampling, one of the outside streams, is deferred (milestone 4) |

## Yours

| # | Goal | State | Evidence |
|---|---|---|---|
| 9 | Built for your hardware and firmware | Partly met | Saved benches (parts, cables, configs) and a repo's own part templates live in the firmware repo, driven in a browser against a stub Core, never a real bench (features, embarch-ui); saved studies live there too (roadmap milestone 6); DUT protocols as `.eap` files, `hw`; SCPI instruments declared, never run against one (features, embarch-api). Test suites, the reducer contract and premade suites are a [proposal](../../embarch-hil-proposal.md) |
| 10 | Local-first | Met | Every component runs on the engineer's own machines, and none calls an EmbArch service ([embarch.md](../../embarch.md) §4). Read from the architecture sketch; nothing checks that it stays true |

## Built for

| Scope | State | Evidence |
|---|---|---|
| Zephyr first | Met | Builds go through west, the board-qualifier grammar, revisions, snippets and sysbuild are set out in [embarch-zephyr.md](../../embarch-zephyr.md), and the in-DUT trace is a Zephyr module |
| Windows with WSL2 | Met | The daily topology, flashed through on real hardware ([roadmap](../../suite/roadmap.md) milestone 1) |
| Linux | Partly met | Core's `start`/`stop` smoke-tested on Linux only (features, embarch-core); no milestone names a Linux-only bench run |
| Any MCP agent, Claude Code first | Partly met | The MCP server and CLI ship (features, embarch-api); only Claude Code is documented ([agent-guide.md](../../suite/agent-guide.md)); no other agent is recorded as tried |

## Open

- **Each line checked against the repos**: the owner chose the docs for now; a line becomes a claim about the code only once checked.
- **Goals 6 and 10 are "met" with nothing that keeps them met.** Whether "met" should need a mechanical check, a CI job or a test, rather than a principle held by review.
- **Who keeps this file current** once it folds into `suite/goals.md`: a status line goes stale the way [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) §4 describes for status words, and nothing here is in `check-staleness.py`.
- **Linux's state**: whether a bench run on native Linux has happened and is not recorded.
