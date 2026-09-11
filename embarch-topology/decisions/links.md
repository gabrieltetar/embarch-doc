# embarch-topology decisions: The DUT signal link, its declared route, and what detection reports for it

**Status:** active, 2026-09-02.

Split verbatim 2026-09-10, once the `embarch-api` decision 67 annotation pushed this file into
reserve. Decisions 17 and 24 — a link's own declared port, and the `detected_by` answer that
runs when its vendor-ID gate is off — moved to [links-port.md](links-port.md); decision 18, the
DUT signal entity and its route, stays here because other sub-projects already cite this path by
name for it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 18 — A new entity: the DUT signal link, with a declared *route* that may deliberately bypass dev-bench

Opened by [embarch-outpost](../../embarch-outpost/decisions.md): its debug UART must reach the host from inside the DUT's own firmware, and **this crate had no way to say "the DUT has a UART, and here is where it currently goes."** A signal that skips a node had no representation, so a topology diagram drawn from this data could not show one.

A named signal with an origin role, a direction, and a route, **stored alongside enrolled boards as another declared fact** — a wire between two headers is invisible to software, the same reasoning decision 14 established for enrollment, extended from "which board is which" to "what is wired to what". One file: both are the same kind of thing. A store predating signals still loads.

**The route is the load-bearing field.** A *direct* route goes straight to a serial port on the Core machine, bypassing dev-bench entirely, identified by the bridge's own USB serial and resolved by decision 17's machinery. A *via-dev-bench* route terminates on declared bench pins and is relayed over the bench's existing link.

**The bypass is modelled as a first-class route, not "the temporary way it happens to be wired".** The intended topology is DUT → bench → Core — the bench is the node that could eventually correlate a DUT signal against its own BLE view, but has neither the spare pins nor the pass-through firmware yet. A declared route makes that move a one-field change plus firmware, not a redesign of anything that consumes it — a study names the signal, never the carrier — and lets the diagram draw the honest picture now: an edge from inside the DUT that goes *around* the bench.

**A third serial device on the bench makes decision 17's ambiguity worse before the declared fact fixes it** — the bench already had two candidates passing the filter; a direct route adds a third, the same resolution failure, one candidate louder.

**Scope held deliberately narrow, matching decisions 10 and 11:** an extensible table, but no logic for a signal fanning out to two destinations, between two DUTs, or as a host-to-DUT stimulus line — none are real yet. Declaring is idempotent by name, and that overwrite *is* the migration path: moving the outpost onto bench pins is one call, not a redesign.

**Resolution reuses decision 17's machinery, with one addition: a filter that skips the vendor-ID gate.** The vendor filter stands in for "this is plausibly a bench link at all" when nothing more specific is known; for a direct route the declared serial already identifies exactly one device, so gating on vendor could only exclude the right answer — a DUT signal may land on a bridge this module has never heard of. Defaults off so the bench's own resolution is untouched; a unit test pins that.

**What validation can honestly assert, and what it cannot.** A direct route confirms the declared serial is currently enumerable, returning a downcastable mismatch naming it when not — it cannot confirm the wire from the DUT's TX pin actually lands on that bridge, and code behind that would not change it. A via-bench route validates on the strength of being declared: its carrier is the bench's link, whose liveness is another function's job, and re-checking it through a second, weaker path would assert more than is known.

**One deliberate gap: a signal mismatch is not written to the durable alert log.** An alert's shape is board-specific — chip, recorded ID, live ID — and a wire has none of those; filling three fields with empty strings a UI would render as facts is the exact silent-mislabelling this crate exists to prevent. Revisit when a signal is declarable **and** a route is physically real.

Two facts about what that landing costs, recorded here so they need not be re-derived (verified against the code as it stands 2026-09-07, not carried forward on the strength of an older note): `embarch-ui` needs no change — it renders only an alert's reason, role and timestamp (`embarch-ui/assets/app.js`'s `alertsListHtml`) — while the mirrored alert type in the shared Core client (`AlertResponse` in `embarch-api/crates/embarch-core-client/src/client.rs`) declares those three fields, plus `chip` and `recorded_hardware_id`, non-optional and would have to move in lockstep.

**Declared through Core, and only through Core, via new signal endpoints — deliberately no CLI mirror, unlike decision 17.** Decision 17's own CLI writes the store directly, and on the real deployment a plain-user run hits the NTFS permission wall that motivated the endpoint in the first place; a second writer that does not work where the suite actually runs is a surface to keep in step for no one. A *read* route exists alongside the write because the human surface must list declared signals. Cost stated rather than hidden: a bench with no Core running has no terminal path to declare a signal, inconsistent with decision 17's CLI, and stays that way rather than being retired on speculation.

**Untouched by [`embarch-api` decision 67](../../embarch-api/decisions/surface.md) (2026-09-10), which gave these routes a CLI and an MCP tool.** What is refused here is a *second writer* — a CLI in this crate writing the store directly, which is what meets the NTFS wall. `embarch-api` calls the same Core endpoints the UI does, so there is still one writer, and the cost above stands verbatim: it needs Core running too. Only the *generalisation* was false, in `embarch-ui` decision 10 and `suite/studies-guide.md`; both corrected.

**`validate_signal` has no caller, deliberately** — resolving at the point of use *is* the validation and returns the identical mismatch, so calling both would check twice and report once. The same posture the suite takes toward `embarch-study-designer`'s advertise-scoped decode surface: validated infrastructure with no caller, left as it is rather than extended on speculation.

**A second consumer needed a function this crate did not have.** A human declaring a direct route picks its port from Core's own enumeration, which did not exist: the existing functions answer "which port is dev-bench's link" and vendor-gate to do it. The new listing is deliberately not the old selection with the gate off — a direct bridge is a wire's carrier and can carry any vendor, so gating the list would hide exactly the port the route exists to name. Its provenance is a fourth answer, `"enumerated"`, rather than one of the three that name a *rule* — an unfiltered listing applied no rule. Ports with no USB identity are omitted: a direct route is declared *by* its serial, so a port reporting none could never be declared as one.
