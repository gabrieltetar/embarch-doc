# embarch-outpost decisions: The manifest

**Status:** active, 2026-09-02.

The build artifact that makes IDs on the wire acceptable, and refuses to decode wrong.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 9 — The manifest is a build artifact, matched against the running firmware, and a mismatch refuses to decode rather than decoding wrong

The DUT build emits it — marker IDs to names, thread addresses to names, the layout version — and **Core stores it with the study and will not render a trace whose header does not match. It records the raw stream and reports the mismatch.**

**This is the whole reason IDs on the wire are acceptable, and the failure mode that has to be loud: a stale manifest against a rebuilt firmware would silently relabel every marker, producing a trace that is entirely readable and entirely wrong** — the worst available outcome, and **exactly the class of staleness `embarch-topology` was created to eliminate.** The manifest travels to Core **the same way the firmware artifact already does.**

**Selection and verification are two questions, answered by two mechanisms.** *"Which manifest should I decode this against?"* and *"is this actually the right one?"* are not the same question, **and trying to make one exact mechanism answer both is what drove an earlier design into patching a CRC into the linked image.**

- **Selection: the study's own flash binds it.** The manifest belongs to the build the study just put on the DUT — **same operation, so there is no interval in which the binding can rot.** **This is not the write-ahead-staleness pattern [embarch-topology](../../embarch-topology/decisions/crate.md) decision 3 exists to eliminate, and the distinction is exactly where that principle's edge lies:** what decision 3 forbids is a *persisted* record of resolved state consulted at some later, unrelated moment. **A binding whose lifetime is the study that created it has no later moment to be wrong in.**
- **Verification: a compile-time build ID in the header frame** — the DUT repo's description, the module's own pinned revision, and a hash of the marker registration list. **All knowable at compile time, so this is a generated header rather than an image-patching post-link step.**

**Each mechanism covers precisely the other's blind spot, which is why both and not either.** Flash-binding is **exact through a dirty-tree rebuild — the common case during active debugging, and the one a dirty build ID cannot distinguish.** The build ID **catches a DUT flashed out-of-band between the study's flash and its capture — a bare `west flash` or an IDE button, entirely normal, and the case flash-binding is blind to.**

**What is genuinely given up, stated rather than glossed:** a DUT flashed out-of-band from a *dirty* tree carrying the same dirty string **still decodes against the wrong manifest.** That is the one residual hole, it is narrow, **and it is the price of not patching the image. If it ever bites, the post-link stamp is the known fix.**

**Reflash is optional, which matters here:** a trace captured on a run that did *not* reflash **falls back entirely to the build ID, and the result's provenance says so.** This does **not** retire umbrella's own staleness check — **a per-study gate only fires when a study runs, while that check answers "is this bench current" before anything is attempted at all.**

**A manifest CRC in the header could never have existed** ([reversals](../../embarch-decision-reversals.md) row 37): the manifest is generated **from the linked image**, its thread and ISR tables being ELF reads, **so no CRC of it exists at compile time for the firmware to carry.** A tap variant that declared one was worse still, since **a CRC chosen when a study was *authored* is precisely the persisted-and-later-consulted record this decision spends three paragraphs distinguishing itself from.** The manifest keeps a CRC **of its own** — a content fingerprint for telling two manifests apart, **computed and read entirely host-side, never compared against anything the firmware says.**

**A mismatch costs the *names*, never the capture.** Core writes the raw bytes first and renders unnamed with the reason recorded, **because a timeline of numeric thread pointers is a real answer and is honestly distinguishable from a named one.**

**The same header makes a DUT staleness check possible**, mirroring the one that already exists for bench firmware: the running firmware reports its outpost version, **and that can be compared against the module revision currently checked out.** Not built; **named because the mechanism is now free.**
