# embarch-api decisions: The per-machine logfile

**Status:** active, 2026-09-10.

Why this crate keeps its own rolling logfile instead of asking Core for one,
and why it is per-user rather than machine-wide. Split out of
[core-link.md](core-link.md) on 2026-09-10, verbatim, per `DOC-COMPACTION.md`
§2 — the file was 326 B from its 12,288 B cap (`tasks/api/058`); this entry
and decision 55 were the largest two entries and share no dependency on the
rest.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Reaching Core otherwise: [core-link.md](core-link.md).

### 43 — One rolling per-machine logfile, because there is no process to ask
Core's log endpoints assume a long-running service. This crate is the opposite: spawned per session as an MCP server, or run once as a CLI and gone. **By the time anyone wants to look at a one-shot's output the process has exited.** Every invocation appends to one rolling file, each line tagged with pid and mode so interleaved sessions stay separable. This works for the one-shot case specifically because **the record outlives the process**, which is the property no endpoint-based design can have here.

*Rejected: shipping lines to Core over a log-sink endpoint.* It would reuse mediation Core already has, and it breaks the invariant that Core has no idea this crate exists — load-bearing well beyond logging. *Also rejected: doing nothing*, on the grounds that an MCP client surfaces its server's stderr and a CLI prints to the terminal. Both true, and neither survives the case that matters: wanting to know what an agent's run did twenty minutes ago, in a session that is closed.

**Per-user, not machine-wide.** The machine data dir works for Core, which runs as a service; it does not work here, because this runs as the engineer and `/var/lib` is root-owned. Both alternatives were worse: hard-failing makes logging depend on a one-time `sudo`, and "machine dir if writable, else per-user" is a runtime probe that can land the writer and the reader in **different places**. Nothing is lost, since single-engineer scope means there is no second user to be machine-wide for.

**Both modes had to be given something to log:** a one-shot CLI run emitted nothing at all, since no subcommand calls the tracing macros on its own. Two lines now bracket every run. **The file gets two layers rather than one teed writer** — Core tees a single ANSI-coloured stream to both stderr and its logfile, so every line in its deployed log carries escape sequences a UI renders as garbage. The two-layer form has **no filter of its own**, so the first build wrote `hyper` and `reqwest` trace output into the file; it needs one stated explicitly.
