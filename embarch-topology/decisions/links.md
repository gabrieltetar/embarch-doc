# embarch-topology decisions: Links and DUT signals

**Status:** active, 2026-09-02.

Declared facts about wires: a link's own port, and a signal that leaves a board.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 17 — The dev-bench link's own USB serial is a second declared fact, distinct from its JTAG probe's

**Found live, running the first real study against both real boards enrolled together for the first time.** Port resolution reported dev-bench's detection as **ambiguous between its real link (a Silabs bridge) and the DUT's own probe's VCOM** — both pass the vendor-ID and product-string filter, and **the only disambiguation signal available, the enrolled dev-bench probe's *JTAG* serial, can never match either**, because the bench's link had moved to a dedicated UART bridge chip that is **a different physical USB device from its JTAG probe.** The JTAG-serial fallback **assumed those two were the same device — which held until a second same-vendor device was enrolled onto the same bench at the same time, never previously exercised.**

So an enrolled board gains the link port's *own* USB serial: **a directly declared fact, because no identity readback is possible over a plain UART**, so this cannot be inferred the way JTAG identity is. Resolution **prefers it, hard**, over the JTAG-serial fallback whenever set; unset, behaviour is unchanged, **so today's common case where the link and the probe really are the same device keeps working.**

**Exposed two ways, matching decision 8** — a CLI subcommand writing the crate's storage directly, and a Core endpoint going through the already-elevated service process. **The endpoint had to exist because a plain-user CLI run on the live Windows deployment hit exactly the NTFS permission wall that motivated Core, not a second process, owning system-file writes.** A unit test reproduces the exact real ambiguity, and it was verified against the real live deployment end to end.

**Only the *fallback* has hardware evidence.** The one live two-probe resolution narrowed its candidates on `probe_serial` with `serial_is_fallback` set, because that bench declares no `link_port_serial` of its own [measured 2026-09-06] — so the **declared** path is exercised by unit test only, and this decision exists precisely to keep a reader from reading the fallback's success as its.

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

**Declared through Core, and only through Core, via new signal endpoints — deliberately no CLI mirror, unlike decision 17.** Decision 17's own CLI writes the store directly, and on the real deployment a plain-user run hits the NTFS permission wall that motivated the endpoint in the first place; a second writer that does not work where the suite actually runs is a surface to keep in step for no one. A *read* route exists alongside the write because the human surface must list declared signals. Cost stated rather than hidden: a bench with no Core running has no terminal path to declare a signal, inconsistent with decision 17's CLI, and stays that way rather than being retired on speculation.

**`validate_signal` has no caller, deliberately** — resolving at the point of use *is* the validation and returns the identical mismatch, so calling both would check twice and report once. The same posture the suite takes toward `embarch-study-designer`'s advertise-scoped decode surface: validated infrastructure with no caller, left as it is rather than extended on speculation.

**A second consumer needed a function this crate did not have.** A human declaring a direct route picks its port from Core's own enumeration, which did not exist: the existing functions answer "which port is dev-bench's link" and vendor-gate to do it. The new listing is deliberately not the old selection with the gate off — a direct bridge is a wire's carrier and can carry any vendor, so gating the list would hide exactly the port the route exists to name. Its provenance is a fourth answer, `"enumerated"`, rather than one of the three that name a *rule* — an unfiltered listing applied no rule. Ports with no USB identity are omitted: a direct route is declared *by* its serial, so a port reporting none could never be declared as one.

### 24 — `detected_by` gets a fourth answer for a declared serial with the VID gate off, and one over-crediting case is accepted rather than chased

**Found the same way decision 20 was: an invisible answer that looked confident.** A direct signal route (decision 18) resolves through `Filter::for_declared_serial`, which turns the VID gate off — a DUT signal may land on any USB-UART bridge, so gating on vendor could only exclude the right answer. But `detected_by` was still set by the same VID lookup every other path uses, which falls back to a generic `"vid-match"` for an unrecognized vendor — a label naming a rule that, with the gate off, never ran at all.

**The fix: a fourth, distinct constant, `DECLARED_SERIAL`, set unconditionally whenever `Filter::no_vid_gate` is on** — not derived from the candidate's actual VID, because under this regime the VID played no discriminating role regardless of what it happens to be. Decision 18's own precedent, read the way decision 20 already reads honesty: `ENUMERATED` exists because an unfiltered listing applied no rule; `DECLARED_SERIAL` exists because a *different* rule ran and the VID-named ones did not.

**A related over-crediting case is accepted rather than chased.** With the VID gate genuinely on, `Filter::resolve` can credit `segger-vid-match` for a bench with several same-vendor candidates where the VID rule matched all of them and eliminated none, while the declared link serial and interface (decisions 17, 20) did the actual narrowing. This is not the bug just fixed — the gate did run, and did exclude every other vendor, a real if coarse fact — so crediting it under-sells how much was pinned down without asserting something false.

**Kept as one field.** `detected_by` names which of three *regimes* resolved a port — a VID rule ran and gated, a declared serial ran and did not, or nothing ran at all — not which individual comparison eliminated the last other candidate. Naming the latter would mean every narrowing step in `select` (serial, product string, interface) reporting what it actually changed, tracked per candidate rather than per regime — a materially larger shape than a `&'static str`, for a case that is honest today, just imprecise. Pinned by a unit test (`a_vid_rule_that_narrowed_nothing_is_still_credited_when_the_gate_ran`).
