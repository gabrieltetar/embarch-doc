# embarch-ui decisions: The Topology tab and signal routing

**Status:** active, 2026-09-02.

The one declaration a human makes about wiring. The trace half of decision 10 is in [trace-view.md](trace-view.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Routing half: the Topology tab gains a DUT signal's route

**Routing belongs next to the diagram it changes.** Each declared signal gets a row — name, origin role, and a route selector: `direct`, which then asks for a serial port from **Core's own enumeration**, or `via dev-bench`, which asks for pins. The diagram redraws from the same data, so a `direct` signal is **drawn going around the dev-bench node** rather than through it: the picture matches the wiring, including when the wiring is deliberately unusual. Writes go to Core over HTTP like every other hardware-adjacent call (decision 5), because Core owns that storage.

*Rejected: the Enroll tab* — it answers "which physical board is which", a question about identity, where routing answers "what is wired to what", a question about the bench, and the Topology tab is already where the second one is *shown*. *Rejected outright: the Study Designer* — a study names a signal, never a carrier, so putting routing there would **bind bench wiring into saved studies and re-author every one of them the day a cable moves.**

**There is deliberately no `embarch-topology` CLI mirror, so this tab is the only human surface there is.** Two consequences. A signal that is declared but wrong **shows up here or nowhere**, since a mismatch is not written to the alert log this tab renders. And `DELETE /signals/{name}` had to exist: "only human surface" plus an idempotent declare meant **the one place that can state a wire could not retract one.**

**`GET /signals` had to exist too**, because this tab must list declared signals before it can offer to change one and nothing had ever called the list function over HTTP; so did `GET /serial-ports`, because "a pick from Core's own enumeration" had no enumeration to pick from — the dev-bench port route answers a different question and VID-gates to do it, **which would hide exactly the bridge a direct route names.** The shared Core client had no wrapper for any of them, so building this tab touched `embarch-api`'s workspace as well.

**The diagram's geometry is the requirement, not decoration.** Every declared signal gets a lane *below* the three nodes: a direct signal's line runs the full width, past and underneath the bench box, and comes back up into "this machine"; a bench-mediated one stops at the bench. An earlier version drew the bench-mediated edge at the nodes' own y and **put the line straight through both boxes it was meant to connect** — caught in the first real render rather than by reasoning about it.

**An empty signal list and an unanswerable one are different states, and this bench proves it.** The live Core predated `GET /signals` and answers `404`; folding that into an empty list would have made the very first thing this tab shows — "no signal declared" — **a false statement about the wiring.** The snapshot carries a separate error field per read, set only when Core itself answered, so the message never duplicates the unreachable banner.

**The one defect was in the markup, and it made the migration path unreachable.** Re-declaring the same name *is* the migration path, and that is what the "Move route" button starts. Every one of those buttons rendered its signal-name attribute **empty** — a stray quote closed it before the name reached it — so the handler looked up a signal named `""`, found none, and opened the dialog on a blank *read-only* name field. **The only human surface for retracting or moving a wire had no working way in, and no Rust test could see it.** Found by rendering the row in headless Firefox and reading the attribute back.
