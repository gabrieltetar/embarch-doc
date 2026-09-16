# embarch-ui decisions: The Debug tab

**Status:** active, 2026-09-02.

A genuinely new suite-wide capability, and where its logs come from.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 7 — The Debug tab is a new suite-wide capability, not a repackaging of something that existed

Neither source UI streamed logs. Core gains a live-tail SSE route **and** a recent-lines route, so the tab **has backlog on first open rather than starting blank** — mirroring the alert pattern Core already had. `embarch-ui` **never reads Core's logfile directly:** Core can run on a different machine, so direct filesystem access would work today on a single-machine bench and **break silently the moment someone runs a split topology.** The UI is handed the data, never the file. Retention is a size-capped rotating logfile rather than a time-based policy — bounded disk, no cleanup pass. `embarch-api`'s own logs are explicitly not addressed here (see decision 13).

> **The retention sentence above describes a mechanism that was never built** (corrected 2026-09-13, `tasks/ui/052`). Core's logfile — the one `/logs/recent` actually serves — is daily-rolling with `max_log_files(7)`, not size-capped (`embarch-core` decision 16). This tab proposed a second, UI-owned size-capped logfile before discovering Core already had a real one, and built neither. Retention here is whatever Core's own daily-rolling policy keeps; the sentence above is left standing as the record of what this decision proposed, not what shipped.

**The SSE half no longer exists** (`tasks/core/021`, 2026-09-10). `GET /logs/stream` was built and never acquired a caller — this tab reaches Core through `/logs/recent` on a poll instead, because decision 13 below shares one poll/diff loop across both log sources and that structurally excludes an SSE source. `embarch-core` retired the route and the hold-past-`\n` rule that governed it (its `decisions/logging.md` 44). The sentence above stands as the account of what was built; only `/logs/recent` remains.

### 13 — `embarch-api`'s logs are read from a rolling per-machine logfile, not from an endpoint

Decision 7's pattern works for Core because **Core is a long-running service with a logfile to mediate.** `embarch-api` is the opposite shape: spawned per session as an MCP server, or once as a CLI, then gone. **There is nothing to poll, and by the time anyone wants to see what a one-shot did, the process that could have answered has exited.** So it appends every invocation in both modes to one rolling file under the machine data dir, pid/mode-tagged so interleaved sessions stay separable, and this tab tails it with the same reader already pointed at Core's file. **The property that decides it: the record outlives the process, which no endpoint design can offer here.**

**This is a real exception to decision 7's "never read a logfile", and it does not reopen that argument.** Decision 7's reasoning is that *Core* can run on a different machine — a topology this suite exists to handle. `embarch-api` cannot: **it is spawned by the MCP client in front of the engineer, on the machine this UI is opened on.** Reading its file locally is correct for the same reason reading Core's was not.

**Switching source is a full console reset, not a merge**: the two files rotate independently, so **interleaving them by arrival order would put lines in an order their own timestamps contradict.** The poll/diff loop is shared; only the fetch differs.

*Rejected: shipping `embarch-api`'s lines to Core* — reuses mediation that exists, but **breaks the invariant that Core has no idea `embarch-api` or any MCP client exist**, which holds up far more than logging. *Rejected: nothing at all* — an MCP client surfaces its server's stderr and a CLI prints to the terminal, but **neither survives wanting to know what an agent did twenty minutes ago in a session that is now closed.**

**Four defects fixed here; two had a comment claiming the code already handled it.**

- **Core's logfile carries ANSI escape sequences** — its writer tees one coloured stream to stderr and file — rendered as literal garbage around every level and target. Stripped at render, **so the *deployed* Core is readable, not just a future one.**
- **Every browser opening this tab saw the stream's most recent batch duplicated on top of its own backlog fetch.** A watch receiver cloned from one whose change was never awaited **inherits the initial version, so the first wait returns immediately** — marking it unchanged at subscribe time is what the code's own comment had always claimed it did.
- **The live tail's diff swallowed every line between two identical ones.** It anchored on the previous window's last line, searching the new window *backward* for its most recent occurrence — **under a comment stating the opposite preference** ("a few duplicate lines in a debug viewer is a smaller problem than missing ones"), **and a test asserting the loss as intended.** The window is a contiguous run of one file, so the anchor is now the longest suffix/prefix overlap, not a line that may appear twice.
- **The "full console reset, not a merge" property above was not actually held.** The backlog fetch was un-awaited and carried no identity, so switching source mid-flight **landed the old source's 200 lines in the new source's console, under the new source's heading** — reproduced against live Core with its recent-lines route delayed — **exactly why this decision avoids a merged stream.** A generation token bumped on every switch now invalidates a stale answer.

**The diff's tolerance for a growing trailing line is conditional, not universal** — Core's tail can end mid-line. `diff_new_lines` (`src/logs.rs:126`) needs exact overlap, so a growing trailing line falls into the no-overlap replay-the-window branch **unless** the window holds a line elsewhere identical to the pre-growth trailing line's content, in which case the overlap search can match spuriously and republish an already-sent line — the same repeat-verbatim property the anchor-bug fix above exists for.
