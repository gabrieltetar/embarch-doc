# embarch-ui decisions: The Topology tab and signal routing

**Status:** active, 2026-09-02.

The one declaration a human makes about wiring. The trace half of decision 10 is in [trace-view.md](trace-view.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Routing half: the Topology tab gains a DUT signal's route

**Routing belongs next to the diagram it changes.** Each declared signal gets a row — name, origin role, and a route selector: `direct`, which then asks for a serial port from **Core's own enumeration**, or `via dev-bench`, which asks for pins. The diagram redraws from the same data, so a `direct` signal is **drawn going around the dev-bench node** rather than through it: the picture matches the wiring, including when the wiring is deliberately unusual. Writes go to Core over HTTP like every other hardware-adjacent call (decision 5), because Core owns that storage.

*Rejected: the Enroll tab* — it answers "which physical board is which", a question about identity, where routing answers "what is wired to what", a question about the bench, and the Topology tab is already where the second one is *shown*. **That split held the two tabs apart from the shell's first sketch until 2026-09-19, and decision 43 ends it in the other direction**: both questions are answered against the same picture, so the identity one moved *here* rather than routing moving there. *Rejected outright: the Study Designer* — a study names a signal, never a carrier, so putting routing there would **bind bench wiring into saved studies and re-author every one of them the day a cable moves.**

**There is deliberately no `embarch-topology` CLI mirror.** **This tab was the only human surface
there was until 2026-09-10**, when [`embarch-api` decision 67](../../embarch-api/decisions.md)
wrapped `POST/GET/DELETE /signals` and `POST /dev-bench/link` as a CLI subcommand and an MCP tool
each. **The rejection this generalised from was narrower than the generalisation**:
[`embarch-topology` decision 18](../../embarch-topology/decisions/links.md) refused a
signal-declaring CLI *inside the topology crate*, on grounds specific to that binary — a direct
enrollment-file write, into a real deployment's permission wall — and it never named
`embarch-api`, which reaches the same Core route over HTTP exactly as this tab does. Decision 18
still stands for `embarch-topology`'s own CLI. A signal that is declared but wrong **shows up here or nowhere**, since a mismatch is not written to the alert log this tab renders. And `DELETE /signals/{name}` had to exist: "only human surface" plus an idempotent declare meant **the one place that can state a wire could not retract one.**

**`GET /signals` had to exist too**, because this tab must list declared signals before it can offer to change one and nothing had ever called the list function over HTTP; so did `GET /serial-ports`, because "a pick from Core's own enumeration" had no enumeration to pick from — the dev-bench port route answers a different question and VID-gates to do it, **which would hide exactly the bridge a direct route names.**

**The diagram's geometry is the requirement, not decoration.** Every declared signal gets a lane *below* the three nodes: a direct signal's line runs the full width, past and underneath the bench box, and comes back up into "this machine"; a bench-mediated one stops at the bench. An earlier version drew the bench-mediated edge at the nodes' own y and **put the line straight through both boxes it was meant to connect.**

**An empty signal list and an unanswerable one are different states, and this bench proves it.** The live Core predated `GET /signals` and answers `404`; folding that into an empty list would have made the very first thing this tab shows — "no signal declared" — **a false statement about the wiring.** The snapshot carries a separate error field per read, set only when Core itself answered, so the message never duplicates the unreachable banner.

**The one defect was in the markup, and it made the migration path unreachable.** Re-declaring the same name *is* the migration path, and that is what the "Move route" button starts. Every one of those buttons rendered its signal-name attribute **empty** — a stray quote closed it before the name reached it — so the handler looked up a signal named `""`, found none, and opened the dialog on a blank *read-only* name field. **The only human surface for retracting or moving a wire had no working way in, and no Rust test could see it.**

### 43 — The Enroll tab folds in: the box that says a role is empty is the box a probe is dropped on

**A tab whose whole content was a picture of two roles, next to a tab that already draws those two roles.** The Enroll tab was a probe pool, two rectangles labelled `dev-bench` and `dut`, and a table of enrolled boards; the Topology tab was a diagram whose two role boxes already said `not enrolled` when they were, plus a `Boards` table with the same three columns. **The second picture existed only because the first one was not a drop target** — which is a property of the markup, not of the question being asked.

So the drop target is the diagram. Each role box is one `<g>`, rect and both labels together, carrying its role in a `data-enroll-role` attribute, and a probe dragged (or clicked, then clicked) onto it opens the same chip dialog the retired tab used and posts to the same `/api/enroll`. **Nothing about the route changed** — Core still owns the mutation, over HTTP+Bearer, per decision 5.

**Three properties are load-bearing, and each is a defect the obvious implementation has:**

- **The listeners live on the `<svg>`, never on a node.** `renderTopologyDiagram` rewrites the whole picture on every snapshot, so a listener bound to a role box is gone within five seconds of being bound. Delegation also makes a box droppable before the first poll has drawn it.
- **The hover highlight is restored after a re-render, not waited for.** A snapshot landing mid-drag rebuilds the node under a stationary cursor, and `dragover` may not fire again while the pointer sits still inside a box it has already entered — so the box would go dark under a cursor that had not moved.
- **`preventDefault` is called on a node and nowhere else.** Without it the browser treats the drop as forbidden and no `drop` event ever fires; called unconditionally on the `<svg>`, the empty space between the boxes looks droppable and then swallows the drop.

**One table, and it leads with the roles rather than with the entries.** The merged `Boards` table carries both columns the fold had to reconcile — Topology's live `Status` badge and the Enroll tab's `Enrolled` instant, still labelled for enrolment time and never for a freshness check. It is built from the two canonical roles **plus every enrolled board outside that pair**: a role-driven table is the only thing that can render "dut: not enrolled" at all, and an entry-driven one was the only thing that could show a board enrolled as something else. Dropping either half loses a row a human needs.

**Re-enrolling an occupied role is the migration path, not an error** — the same shape as re-declaring a signal to move its route (decision 10) — so an occupied box opens the ordinary dialog rather than refusing the drop. The chip field arrives pre-filled from the enrolment being replaced, and the dialog names what it displaces, so a mis-drop is visible before the button rather than after the row is gone. *Rejected: refusing the drop and asking for an unenroll first* — safest, and this UI has no unenroll control to send anyone to.

**`#enroll` still lands on Topology.** A retired fragment resolves to its new home rather than to `null`; falling through would have put a typed, bookmarked or agent-relayed link on whichever tab that browser last had open. **The `?role=` pre-fill went the other way and was deleted**: it was inherited from Core's retired `/enroll` page, its target was a drop zone that no longer exists, and a grep of all eight repos found the only mention of it was the code reading it — **nothing in the suite had ever emitted one.**

**Driven in a real browser before it was believed**: `tests/browser/drive_topology.py`, eighteen checks against a stub Core serving an occupied role, an empty one and a board enrolled as `sniffer` — including a click on a box's *text label* (a `<rect>`-only target leaves the labels a dead zone sitting on top of it) and the highlight surviving a poll. The retired tab's own rebuild-skip carried over unchanged with the probe pool, which is what keeps a 5 s re-poll from dropping a selection mid-drag.

### 50 — The Topology tab stops explaining itself; a path is the one note that stays

Under almost every title on this tab sat a paragraph of prose: what a board *type* is, that a probe and a board are separate things, that a wire between two headers is invisible to software, that loading a bench touches no hardware. Each was true and each was written while the decision behind it was being made — which is the tell. **A design note addressed to the person who just built the surface is not documentation for the person using it**, and eight of them stacked down one tab turn a bench description into a reading task; the reader wanting the reasoning is served better by these files than by a `<p>` they cannot skip.

So the tab keeps: **a path** — `embarch/topologies/`, `embarch/boards.toml`, and the catalog's own served file line, which say where a fact lives and cannot be inferred from the screen — and **a state**, such as a repo whose targets could not be scanned or a board type the scan does not have. What goes is every paragraph that explains a model the surface already enacts. The combination picker's note keeps its two refusals and loses its two counts: "3 combinations in this repo's scan", printed beside a list of three, is the list read aloud.
