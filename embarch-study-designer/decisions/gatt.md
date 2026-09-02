# embarch-study-designer decisions: GATT discovery and monitoring

**Status:** active, 2026-09-02.

Walking a DUT table, capture windows that outlive a step, and vendor identities.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 31 — `Action::GattDiscover` — walk a connected DUT's entire GATT table

**A study author pointed at an unfamiliar DUT has no way to ask "what is actually on this device"** before authoring a step against it. This walks every primary service and every characteristic — the stack's ordinary wildcard discovery, a superset of the single-service walk each data exchange already does — reports the table, **and acts on it no further: no subscribe, no capture.** Bound by the step's own timeout, matching every other action.

Properties are carried as **the raw ATT properties byte rather than a crate-invented bitflag enum** — consistent with this crate's UUIDs-are-raw stance.

### 32 — `Action::GattMonitorAll` — discover, subscribe to everything notify-capable, capture for the rest of the step

**Deliberately not built on a prior discovery's result.** *Rejected:* consuming a previous step's output so discovery happens once per connection. **Every other action here is self-contained within its own step**, and threading one step's table into a later step's input **would be new wire-level state-passing this crate has never needed** — for a capability where re-running discovery is cheap.

A captured record's characteristic index indexes the table **flattened in service-then-characteristic order**, stated **because it is the one place dev-bench's encoder and every consumer must agree on that flattening.**

**Overflow behaviour, back when the record list was capped:** the bench stopped capturing and reported what it had — **not a failure or a timeout** — matching the log-and-skip-rather-than-corrupt precedent **rather than silently wrapping or truncating a record's payload.** That cap is gone with decision 54, and the pipeline it was replaced by is uncapped.

**Kept unchanged by both later monitor decisions:** pointing an unfamiliar DUT at "subscribe to everything and see what it does" is **still the first thing anyone does, and still the simpler thing to author.**

### 36 — `GattMonitorStart`/`Stop` — a capture window that outlives its own step, plus a streamed transcript

Opened by a gap found trying to author the first real stimulate-and-capture study: **it was not expressible.** Steps run strictly in sequence and monitor-everything unsubscribes when its own step ends, **so a write that stimulates the DUT and a monitor step that captures the response can never overlap.** Write first and the response arrives after the capture is over; capture first and the write never happens during it. **Every ordering loses, silently, producing an empty capture and a pass.**

Two field-less variants: start runs the same walk then **returns immediately, leaving every subscription armed**, so every following step runs inside a live window; stop unsubscribes and reports. **A stop with no open window is a no-op pass, not a failure**, and a study ending without one has its window closed implicitly, **so an abort mid-study cannot leave subscriptions armed into the next one.**

**The second half, and the reason this is one decision rather than two:** a window spanning steps immediately outgrows a per-step inline record list, which was capped and recorded **inbound notifications only — nothing about what dev-bench itself sent, which is precisely the half a stimulate-and-capture transcript needs to be readable.** So this added a **streamed transcript**, emitted per event and appended incrementally. **Because one entry is streamed per message, only a single entry has to fit in the bench's message buffer — which is what lifts the cap: the transcript is bounded by the study's own duration, nothing else.**

It was deliberately **its own message variant rather than a third stream channel** carried by the sample-shaped chunks: those carried one float plus a unit, **with no room for a byte payload, a direction, or a pair of UUIDs.** **Partially superseded by decision 39 one day later, knowingly, with the collision flagged before the call was made** — the dedicated variant folded into the generic pipeline while the row shape, entry types and streamed/uncapped/both-directions behaviour survive as a declared *encoding*. **The reasoning here was not wrong:** the sample type genuinely had no room for those things, **which is exactly why a third parallel pipeline looked like the only option. It was an argument against the shape the chunks had, not against a generic pipeline as such.**

**The both-languages wire contract, and the rule this decision introduced.** The bench hand-writes its encoding in C, and **nothing in either side's own test suite would notice the two drifting — a reordered field or an integer written the wrong width decodes into plausible-looking garbage, not an error.** So a new record's exact bytes are pinned **twice**: as a literal frame in the firmware suite, and as the identical body here, **asserting decode *and* re-encode. Changing the shape must break both.** **This pairing found a real discrepancy the first time it ran** — and has since done so again, and been applied retroactively to the handshake, **both of which predate the rule because it applied to *new* records only.**

### 41 — A built-in table of vendor-defined GATT service identities

Decision 35's registry is per-repo and engineer-authored **because what a *custom* characteristic's bytes mean is knowledge only that repo's engineers have.** A vendor-defined service is the opposite kind of fact: **Nordic's UART Service has the same UUIDs on every device that implements it, published in the stack's own headers.** Requiring every engineer to transcribe a 128-bit UUID **to write to a service the stack itself defines is pure error surface.** So those identities ship as constants, **picked by id, never by typing a UUID.**

**Identity only. No semantics, ever** — decision 35's rule applied to a table **that would be far more tempting to over-fill.** It records *where* to write and **nothing whatsoever about *what* to write**: no command vocabulary, no line terminator, no "send `help` to list commands". **Whatever sits behind a given DUT's endpoint — a shell, an application protocol, a bootloader, nothing at all — is that DUT's business**, supplied per study as literal bytes.

**An entry is a conditional, not a claim**: *if* a device exposes this service, these are its UUIDs. **Live discovery remains the only thing that answers "does this DUT actually have it?"** — written down rather than assumed **because the first DUT this was pointed at turned out not to expose it at all.**

The vendor's declared properties are included because they decide **whether a chosen operation is even legal**: the builder refuses a write against a notify-only characteristic **rather than letting it fail mid-study as an opaque ATT error.** It remains **the vendor's claim, not a measurement** — a discovered-properties field sits beside it, and **where the two disagree live discovery wins and the disagreement is itself the finding.**

**No schema bump:** a vendor row resolves into an ordinary exchange carrying plain UUIDs before anything is encoded, **so dev-bench never learns the table exists** — pinned by a test asserting a vendor row and the equivalent raw row build the byte-identical action.

### 53 — `GattMonitorSelected` — subscribe to the characteristics the study names

Raised by the repo owner authoring a real study: **monitor-everything was the only monitor available and it is all-or-nothing.** Subscribing to every notify-capable characteristic on a DUT that streams a high-rate waveform **floods the link with traffic nobody asked for and buries the two characteristics the study is about.**

**New variants beside the old rather than a targets field on the existing pair** — the repo owner's call. The stop action is reused unchanged: **a window is a window regardless of how many characteristics it armed, and a second stop would be two names for one thing.**

**These are the first action variants ever to carry a sequence, and that is a real cost, not a footnote.** Every monitor action before them was field-less, so the C decoder walked them by tag alone; **one that kept doing so would read the target-count varint as the next step's name length and decode the rest of the study into nonsense that still parses.** A pinned wire vector holds exactly that shape — two targets, then a field-less stop **whose tag has to land where the encoder put it.**

**An empty target list is refused, not promoted to "everything"**, in the builder and the UI: **"monitor these" with nothing named is the not-thought-about case, and quietly subscribing to the whole table is the flood this action exists to avoid.** Symmetrically, **a named target that is not on the DUT, or that can neither notify nor indicate, fails the step naming it** rather than being skipped — **the log-and-skip rule the unfiltered walk uses is right precisely because nothing there was named, and a study that names a characteristic has said it expects one.**
