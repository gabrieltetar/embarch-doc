# embarch-outpost decisions: Capture and routing

**Status:** active, 2026-09-02.

Study-scoped, post-hoc, and a signal whose carrier is a bench fact.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 10 — Capture is study-scoped and rendered post-hoc. There is no live feed

Core opens the tap when a study starts and closes it when the study ends; **the timeline is drawn from the recorded stream afterwards.**

**This reverses the framing this work opened with** — *"debug MCU load in realtime"* — deliberately, and it is worth recording rather than letting the doc quietly disagree with its own motivation. **A live feed costs a decode-and-push path in Core, an SSE channel, and a renderer that can draw a partial timeline, all before the first byte has ever been captured** — and **the actual debugging question is answered just as well by a complete recording as by a partial live one.** Always-on capture is a plausible later addition; **pretending it was a v1 requirement would have shaped the port-ownership design around a case nobody asked to use yet.**

**Half-reversed 2026-09-18** ([reversals row 112](../../embarch-decision-reversals.md); [`embarch-core` decision 72](../../embarch-core/decisions.md), [`embarch-ui` decision 37](../../embarch-ui/decisions.md)). All three costs above were built, as priced — and **none of the reasoning above is wrong.** What changed is that a second consumer arrived: `embarch-ui`'s Time chart reads a trace *against the study's other streams*, which is not "debug MCU load in realtime" but placing a GATT notification inside the step it arrived in. For that question a complete recording is not equivalent, because the chart exists while the run does.

**What is reversed is only the feed. The post-hoc render stays authoritative and still runs**, and the live path is a stated preview of it: the render has a whole-capture header pre-pass, the stale-prefix drop over everything and the verified arrival join, **none of which a live path can have.** So a frame decoded before the capture's header carries an empty `us` and an empty `name` and says so (`header_seen: false`), and the render fills both in. **Capture is still study-scoped** — nothing here makes the tap always-on, which is the half of this decision that has not moved.

### 11 — "Dev-bench bypass" is not an outpost feature — it is a routing property of a topology entity

[embarch-topology](../../embarch-topology/decisions/links.md) decision 18 owns it: a named signal originating at the DUT with a declared route, either direct to the Core machine or via declared bench pins. **The outpost UART is the first instance; a DUT console UART, an SWO pin and eventually a stimulus line are the obvious next ones.**

**Today's route is direct, for a stated hardware reason and not a design preference.** The intended topology is DUT → bench → Core, **because the bench already owns a validated link and is what will eventually correlate a trace against its own BLE view.** It does not have the pins or the pass-through firmware, **so modelling this as a first-class declared route rather than "the temporary way it happens to be wired" is what makes the eventual move a declaration change instead of a redesign** — and what lets a topology diagram draw an honest picture of a signal that skips a node.

**On a via-bench route the bench passes bytes through and interprets nothing** — receives on the declared pin, stamps arrival, forwards. **Not decode-and-summarise: putting record semantics in bench firmware would make it carry knowledge of a specific DUT's build, and would mean reflashing the bench whenever that DUT's manifest changes.**

### 12 — A study names the signal; topology resolves the carrier

The tap says `outpost`, **not a port name and not a bench pin.** This is what makes decision 11 pay: **the identical saved study runs unchanged before and after the bench gains pass-through hardware, on a machine whose bridge enumerates differently, or against a Core running elsewhere.** Naming the concrete source **is more explicit on the wire and re-authors every saved study the day the bench is rewired.**

### 13 — The outpost's capture is a `StreamTap`

Which means the stream pipeline's inbound half is accepted, and [embarch-study-designer](../../embarch-study-designer/decisions/gatt.md) decision 36's dedicated-variant route is reversed **one day after it shipped.**

**The collision was flagged before this was decided, and the decision was made anyway, knowingly.** Decision 36 chose a dedicated message variant over generalising the channel enum, **reasoning correctly that a sample's single float has no room for raw bytes, a direction, or a UUID pair. That reasoning was an argument against the shape that enum had, not against a generic pipeline** — and the tap model was designed around exactly that objection. **The cost is real and is not being minimised:** a schema bump, a second wire-contract pinning pass in both C and Rust, and edits to firmware that was code-complete and deployed. **The offsetting fact is what made it affordable: nothing about decision 36's wire shape was load-bearing on a real bench yet. This was the last moment it was cheap.**
