# Goals notes: scope, and the answers behind it

**Status:** draft, 2026-11-16.

The answers behind [00-goals.md](00-goals.md)'s "Built for", "Non-goals" and "Who may use it", with the owner's reasons where the owner gave one. Every answer here is the owner's, 2026-11-16, unless it sits under Open.

## Who EmbArch is for

**A firmware engineer who lets an LLM agent work on their real bench.** Not a team, not a consultancy, and not the owner first. Teams and clients are reached through what that engineer publishes.

## What is the product, and what is the owner's own tooling

**The product goals cover hardware-in-the-loop and what feeds it.** The product is `embarch-core`, `embarch-api`, `embarch-study-designer`, `embarch-dev-bench`, `embarch-outpost`, `embarch-topology`, `embarch-smp`, `embarch-ui`, `embarch-umbrella` and `embarch-atlas` ([embarch.md](../../embarch.md) §3).

**`embarch-desk`, `embarch-chat`, `embarch-promptu` and the agent fleet are the owner's own tooling.** They are MIT-licensed, used to build EmbArch, outside the product goals, and promised to no one. How the suite is built, by an agent fleet among other ways, is not part of the goals (owner: not mentioned).

## A community project

**EmbArch is a community project.** The owner's comparison: FreeRTOS, a community project that ended up shipped in millions of systems. **The comparison is about the path, from a community project to wide use, and nothing more** (the owner, when a follow-up read more into it).

- **What should spread is the bench tooling**: engineers installing EmbArch on their own benches.
- **Commercial use is welcome and not pursued.** MIT lets anyone use EmbArch for their own products and clients, as companies do with FreeRTOS; the project does not chase clients or build for one.
- **The licence already allows it**: every repo is MIT except `embarch-smp`, which is Apache-2.0 (each repo's `LICENSE`, read 2026-11-16).

## Firmware, hosts and agents

- **Zephyr first.** Builds go through west and the in-DUT trace (`embarch-outpost`) is a Zephyr module; other firmware can use flashing, serial and studies, but Zephyr-only features are not promised for it.
- **Windows with WSL2, and Linux.** The daily setup is Core as a Windows service with `embarch-api` in WSL2; macOS shipped reasoned-only and has never been tested ([roadmap](../../suite/roadmap.md), "Later").
- **Any MCP agent, Claude Code first.** The MCP server and the CLI are the contract; Claude Code is the agent tested and documented ([agent-guide.md](../../suite/agent-guide.md)).
- **"LLM", not "AI".** The owner's reason: "the word LLM suits better for a technical crowd than AI that is a way broader concept and overused word". Every file here says LLM agent; the sweep of the suite's existing docs is EMB-194, in Backlog.

## The trinity

**One engineer, one Core, one machine.** The owner's reason: "it would be valuable to show the project is not shooting for the stars (for a one man show) to state the current design relies on a trinity of 1 engineer 1 Core 1 machine, and it could only outgrow this if the suite gets to a real impressive milestone and it's time to scale the solution". When that is, is the owner's call ([02-phases.md](02-phases.md)).

The trinity replaces the "single-engineer scope" principle of [embarch.md](../../embarch.md) §5 as the way the goals state the boundary.

## Non-goals

- **Not a certification.** Pre-compliance evidence only.
- **No hosted service.**

Offered and not picked: "no runtime safety envelope" and "no bench farm". **On safety, the owner disagreed with the framing**: what a study or test does is checked when it is written, and while it runs, only the run can alter the bench, so the check is enforced at run time indirectly. [00-goals.md](00-goals.md) goal 2 carries that wording.

## The goals offered and cut

Offered as goals and cut by the owner:

- **A short first hour** and **nothing tied to the owner's machine or setup**: cut as goals now, kept as goals of the scaling phase ([02-phases.md](02-phases.md)).
- **Honest status** (every feature states how far it is verified), **the docs as the source of truth**, **one hardware implementation**, **Rust as one toolchain**: cut as goals. They stay principles in [embarch.md](../../embarch.md) §5, which this does not change.

## The HIL goals

**The HIL notes' goals are for review; these goals are for the world.** They state the same idea and can be reviewed against each other; neither cites the other (owner).

## Open

- **`embarch-chat` has no remote**, by the owner's choice ([embarch.md](../../embarch.md) §3), so "MIT-licensed" for the owner's tooling describes the licence file, not a published repo. Whether the goals say so.
- **The two token scopes** of the HIL evidence design (an agent scope and a person scope) are read here as living inside the trinity: one engineer, two kinds of caller. An inference, not asked.
- **Whether the trinity and §5's "single-engineer scope"** are reconciled when this folds: §5 rewritten to the trinity, or both kept.
