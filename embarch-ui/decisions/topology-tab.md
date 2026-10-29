# embarch-ui decisions: The Topology tab and signal routing

**Status:** active, 2026-09-02.

The one declaration a human makes about wiring. The trace half of decision 10 is in [trace-view.md](trace-view.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Routing half: the Topology tab gains a DUT signal's route

**Routing belongs next to the diagram it changes.** Each declared signal gets a row — name, origin role, and a route selector: `direct`, which asks for a serial port from **Core's own enumeration**, or `via dev-bench`, which asks for pins. The diagram redraws from the same data, so a `direct` signal is **drawn going around the dev-bench node** rather than through it: the picture matches the wiring, including when the wiring is deliberately unusual. Writes go to Core over HTTP like every other hardware-adjacent call (decision 5), because Core owns that storage.

**Amended 2026-10-26 (`suite/052`):** a port sharing its USB serial with another is listed with its interface, and picking it declares that interface ([`embarch-topology` decision 46](../../embarch-topology/decisions/links.md)); a port alone under its serial is declared without one, as before. The validate pass and the carrier cell fail a direct route several ports share with none declared, since Core refuses it. Driven in `drive_topology.py`.

*Rejected: the Enroll tab* — it answers "which physical board is which", a question about identity, where routing answers "what is wired to what", a question about the bench, and this tab already *shows* the second. **That split held the two tabs apart until 2026-09-19, and decision 43 ends it**: the identity question moved *here*, not routing there. *Rejected outright: the Study Designer* — a study names a signal, never a carrier, so putting routing there would **bind bench wiring into saved studies and re-author every one of them the day a cable moves.**

**There is deliberately no `embarch-topology` CLI mirror** — [`embarch-topology` decision 18](../../embarch-topology/decisions/links.md) refused one in the topology crate, on grounds specific to that binary: a direct enrollment-file write, into a real deployment's permission wall. It never named `embarch-api`, which reaches the same Core routes over HTTP as this tab does, and [`embarch-api` decision 67](../../embarch-api/decisions.md) (2026-09-10) wrapped `POST/GET/DELETE /signals` and `POST /dev-bench/link` as a CLI subcommand and an MCP tool each. **Until then this tab was the only human surface**, and with an idempotent declare **the one place that can state a wire could not retract one** — so `DELETE /signals/{name}` had to exist. A signal declared but wrong **shows up here or nowhere**: a mismatch is not written to the alert log this tab renders.

**`GET /signals` had to exist too** — nothing had called the list function over HTTP, and the tab must list before it can change — and so did `GET /serial-ports`: the dev-bench port route answers a different question and VID-gates to do it, **which would hide exactly the bridge a direct route names.**

**The diagram's geometry is the requirement.** Every declared signal gets a lane *below* the three nodes: a direct line runs the full width, under the bench box, and back up into "this machine"; a bench-mediated one stops at the bench. Drawn at the nodes' own y, a bench-mediated edge **ran straight through both boxes it connected.**

**An empty signal list and an unanswerable one are different states** ([reversals](../../embarch-decision-reversals.md) row 46: the live Core answered `404`, and an empty list would have been **a false statement about the wiring**). The snapshot carries an error field per read, set only when Core itself answered, so it never duplicates the unreachable banner.

**Re-declaring the same name is the migration path**, started by **Move route**. A stray quote once rendered every such button's signal-name attribute **empty**, opening the dialog on a blank read-only name: **the only surface for moving a wire had no way in, and no Rust test could see it.**

### 43 — The Enroll tab folds in: the box that says a role is empty is the box a probe is dropped on

**A tab whose whole content was a picture of two roles, next to a tab that already draws those two roles.** The Enroll tab was a probe pool, two rectangles labelled `dev-bench` and `dut`, and a table of enrolled boards; the Topology tab's two role boxes already said `not enrolled`, beside a `Boards` table with the same three columns. **The second picture existed only because the first was not a drop target** — a property of the markup, not of the question.

So the drop target is the diagram. Each role box is one `<g>`, rect and both labels together (a `<rect>` alone leaves the labels a dead zone on top of it), carrying its role in `data-enroll-role`; a probe dragged (or clicked, then clicked) onto it opens the retired tab's chip dialog and posts to the same `/api/enroll`. **Nothing about the route changed** — Core still owns the mutation, over HTTP+Bearer, per decision 5.

**Three properties are load-bearing, and each is a defect the obvious implementation has:**

- **The listeners live on the `<svg>`, never on a node.** `renderTopologyDiagram` rewrites the whole picture on every snapshot, so a listener bound to a role box is gone within five seconds. Delegation also makes a box droppable before the first poll has drawn it.
- **The hover highlight is restored after a re-render, not waited for.** A snapshot mid-drag rebuilds the node under a stationary cursor, and `dragover` may not fire again while the pointer sits still inside a box it already entered — so the box would go dark under a cursor that had not moved.
- **`preventDefault` is called on a node and nowhere else.** Without it the browser treats the drop as forbidden and no `drop` event fires; called unconditionally on the `<svg>`, the space between the boxes looks droppable and swallows the drop.

**One table, led by the roles rather than the entries.** The merged `Boards` table keeps Topology's live `Status` badge and the Enroll tab's `Enrolled` instant, still labelled for enrolment time, never a freshness check. Its rows are the two canonical roles **plus every enrolled board outside that pair**: only a role-driven table can render "dut: not enrolled", and only an entry-driven one could show a board enrolled as something else. Dropping either half loses a row a human needs.

**Re-enrolling an occupied role is the migration path, not an error** — the same shape as re-declaring a signal to move its route (decision 10) — so an occupied box opens the ordinary dialog, chip pre-filled from the enrolment being replaced and naming what it displaces, so a mis-drop shows before the button rather than after the row is gone. *Rejected: refusing the drop and asking for an unenroll first* — safest, and this UI has no unenroll control to send anyone to.

**`#enroll` still lands on Topology** — a retired fragment resolves to its new home, not to `null`; falling through would put a typed, bookmarked or agent-relayed link on whichever tab that browser last had open. **The `?role=` pre-fill was deleted**: inherited from Core's retired `/enroll` page, its target no longer exists, and a grep of all eight repos found only the code reading it — **nothing in the suite had ever emitted one.**

**Driven in a real browser before it was believed**: `tests/browser/drive_topology.py`, eighteen checks against a stub Core serving an occupied role, an empty one and a board enrolled as `sniffer`, including a click on a box's text label and the highlight surviving a poll. The retired tab's rebuild-skip carried over unchanged with the probe pool, which is what keeps a 5 s re-poll from dropping a selection mid-drag.

### 67 — A signal's origin is a role or a bench board, shown by name and re-saved unchanged

`embarch-topology` decision 48 lets a signal leave a role-less bench board (`origin_board` = its probe serial, `origin_role` empty). The signals table shows that origin as the enrolled board's name, the serial when no enrolled board matches. The dialog's origin picker lists the enrolled role-less bench boards (option value `board:<serial>`) after the roles and sends `origin_board` with an **empty** `origin_role` — one origin, never both; `origin_role` stays on the wire because the shared `SignalLink` has no serde default for it. A board-origin signal opens on its board (an extra "board not enrolled" option if it no longer is one), so a re-save keeps it; before this a re-save would have re-declared it from `dut`. The UI server needed no change: it passes the typed `SignalLink` straight to Core.
