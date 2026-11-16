# EmbArch goals

**Status:** draft, 2026-11-16.

**What EmbArch sets out to be, written for a reader who has never heard of it.** The future `suite/goals.md`, in draft. The vision, scope, goals and non-goals are the owner's answers of 2026-11-16; the wording of each goal is the interviewer's and the owner may correct it. Each status line is taken from the suite's docs, not checked against the code ([03-status.md](03-status.md)).

## Vision

**Hardware-in-the-loop for the firmware engineer and LLM agents: real benches, real measurements, and evidence anyone can check.**

EmbArch is in its build phase: hardware-in-the-loop and the atlas are being improved, and scaling comes once the toolset is stable ([02-phases.md](02-phases.md)).

## Built for

- **A firmware engineer who lets an LLM agent work on their real bench.** Teams, colleagues and clients benefit through that engineer's reports.
- **Zephyr first.** Other firmware can be flashed, read over serial and studied; the Zephyr-only features (the build, the in-DUT trace) are not promised for it.
- **Windows with WSL2, and Linux.** macOS is best effort until someone tests it.
- **Any agent that speaks MCP, or a person at the CLI.** Claude Code is the agent EmbArch is tested and documented with.
- **The trinity: one engineer, one Core, one machine.** Core is the service that owns the debug probes and serial ports; every hardware call goes through it. The design relies on the trinity, and outgrows it only once the toolset is stable and the owner decides to scale.

## Goals

Grouped by theme, not ranked. Each states where the codebase stands: **met**, **partly met** or **not yet**.

### At the bench

1. **Real hands on the bench.** An LLM agent can build, flash, reset, read, and run studies, tests and live actions on a real bench, through the MCP server or the CLI.
   *Partly met*: building, flashing, serial capture and studies run on real hardware; tests and live access are designed, not built.
2. **The engineer stays in control.** The agent does to the hardware only what the engineer allowed. What a study or test does is checked when it is written, and enforced while it runs, because the run is then the only thing that can touch the bench. An act that is the person's (a confirmation, the go, a verdict) stays the person's.
   *Partly met*: a bench lease exists and the agent guide says which tools should ask first; one token still serves agent and person alike.
3. **One path, agent or human.** Every hardware capability is reachable by an agent and by a person through the same code. Neither has a privileged path.
   *Met*, with one gap: making a saved bench live is in the UI only.

### Evidence

4. **Evidence anyone can check.** No number, verdict or identity in a published report depends on the agent having told the truth, and a reader checks the report offline with an open-source tool.
   *Not yet*: designed in full, with signed records and a `verify` command; nothing published or signed today.
5. **Professional practice.** Verdicts, limits, units, uncertainty and reports are what a test lab expects to see.
   *Not yet*: the verdict model and the report are designed; no run has a verdict today.
6. **Never an inference stated as fact.** What a specific board or firmware does is declared by the engineer or measured on the bench; an inference is labelled as one.
   *Met as a rule*: held across the design; nothing checks it mechanically.

### Understanding

7. **Hardware truth for agents.** The atlas lets an agent answer pin, net, part, register and limit questions from the schematics, datasheets and reference manual, joined to the firmware, with every mismatch reported.
   *Partly met*: built on one real two-board product, not yet published; a rework into seven planes is proposed.
8. **One timeline.** What happens inside the DUT (its trace) and outside it (the radio link, serial, instruments) sits on one timeline, so a result can be explained, not only measured.
   *Partly met*: the in-DUT trace works on real silicon with no records lost; no run has yet placed it against a second stream.

### Yours

9. **Built for your hardware and firmware.** The engineer and the agent describe their own bench, write their own studies and tests, and build an atlas of their own product. A contributor adds a test suite, a reducer or decoder, a bench board or an instrument without touching Core.
   *Partly met*: benches, studies, DUT protocols and instruments are the engineer's own files; test suites and the reducer contract are designed, not built.
10. **Local-first.** Everything runs on the engineer's own machines, with no EmbArch cloud service or account. Only the agent's model API leaves the machine.
    *Met*.

## Non-goals

- **Not a certification.** EmbArch produces pre-compliance evidence. It never certifies a product or stands in for an accredited lab.
- **No hosted service.** No EmbArch cloud, account or server.

## Who may use it

**EmbArch is a community project, MIT-licensed** (one crate, `embarch-smp`, is Apache-2.0). Anyone may use it in commercial work, for their own products and their own clients; the project does not pursue clients or build for any one of them.

## Open

- **Goal 3 against goal 2.** Goal 2 keeps some acts to the person alone, so "reachable by an agent and by a person" no longer holds for every capability. Recommended: goal 3 reads "every capability the agent has, a person has too, through the same code; the agent has no privileged path".
- **The wording of each goal's title and sentence**, goal by goal: the interviewer's, from the owner's picks.
- **macOS "best effort"** in Built for: the owner picked Windows with WSL2 and Linux; the macOS line is the recommendation that came with that pick.
- **Whether "Teams, colleagues and clients benefit through that engineer's reports"** stays in Built for, or reads as pursuing clients.
- **Goal 10's "met"** rests on the architecture sketch; whether a goal can be met without a check that keeps it met.
