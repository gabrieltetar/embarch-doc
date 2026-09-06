# embarch: roadmap

**Status:** active, 2026-09-02.

What shipped, what is in flight, what is deferred. **Every milestone uses a real suite release plus the real `reference-dut-fw` client repo as its target, not a placeholder project or a synthetic fixture.** Per-milestone reasoning lives in the owning `decisions.md`; findings live in [the reversals page](../embarch-decision-reversals.md).

## Shipped foundation

The original numbered milestones — Flash, Token, Study Designer scoping and implementation, Dev Bench scoping, Onboarding — are done and shipped as real `v0.1.0` releases across all three code-bearing repos. **Recorded as a foundation rather than as active milestones, and deliberately not renumbered into the sequence below.**

## Milestones

Numbered fresh from 1. *(An execution doc for one of these was filed as `milestone-N.md` with N continuing past the foundation's own 1–6 so it could not collide; every one of those docs is now folded into its sub-project's four files and deleted.)*

### 1 — Flash and build on real hardware · **done**

*API, Core.* Validate the full build→flash chain against the real client repo with the API in WSL2 and Core on Windows: **the suite's actual daily-use topology.** The foundation's Flash milestone proved the chain against a generic board and Onboarding validated config discovery, **but neither ever drove a physical flash through it.** Closed with the board resolved by live discovery rather than pre-selected.

### 2 — Dev-bench self-test · **done**

*Core, dev-bench, API.* Establish the self-test as a standing precondition every study runs before touching a DUT: the bench exercises its own peripherals and the whole transport — link, handshake, real dispatch of a multi-step study with results round-tripping — **end to end on physical hardware for the first time.** Power sampling explicitly out of scope.

**Retargeted from the DK to the ESP32-C5 mid-milestone** ([reversals](../embarch-decision-reversals.md) row 13): the DK's replacement never arrived, and the C5 — originally only an interim substitute — had already validated the entire mechanism. Closed with **one item unmet**: the watchdog's lapse-produces-failure behaviour stayed unit-tested only, because **two live attempts both lost the same timing race against a step that resolves in well under a second.**

### 3 — Study Designer: feature-branch iteration · **done**

*Study Designer, Core, API, dev-bench.* Use the full chain to iterate a real feature branch: build and flash it, have the bench BLE-connect to the running DUT, exchange GATT data, and forward it over the link into Core. **One successful end-to-end run is the definition of done** — not a repeated edit-rebuild-reflash loop.

The design pass made the GATT interaction **generic rather than tied to one known characteristic**, which is what wildcard discovery and monitor-everything exist for. Closed by the first physical BLE connection between two independent boards this suite has ever made. **One real gap left open rather than blocking: a ~50% flake rate connecting to and discovering the DUT's table, not root-caused.**

### 4 — Power-sampling study · **deferred, not cancelled**

*Dev-bench, Study Designer.* Acquire and wire in the power front end and exercise the sampling path end to end for the first time — the one dev-bench area milestones 2 and 3 explicitly defer.

**Deferred on the repo owner's direct call.** No front end gets ordered; the hardware pick stands as the pick if this resumes rather than being withdrawn, and the milestone keeps its number and scope **so the sequencing history stays readable.**

**The deferral settles four open questions in one stroke, which is most of why it was worth asking rather than letting the milestone drift**: the physical bench design and its DUT connector, the sample-grain question, the power CSV columns, and the signal-check variant set with its naive transform. **All four are now deferrals with one shared trigger instead of four questions waiting on an answer nobody could give.**

### 5 — Study Designer UI · **done except real-hardware validation**

*Study Designer.* Opened by a gap milestone 3's own closing session hit directly: **a real monitor-everything run came back empty, because nothing in that study ever wrote anything to make the DUT stream** — and there was no way for whoever authored it to know what to write. That is DUT-specific knowledge no generic discovery can produce, **and an attempt to answer it by reading the DUT's own source and asserting a conclusion was flagged as destructive to the dev process.**

So: an interactive table-based study builder whose action list merges built-in actions, live discovery, and static extraction, plus a user-authored registry — **name and clickable enumerated values only, never a semantic description this suite invents.** Built and smoke-tested against the real repo; **closing the loop for real needs someone who actually knows that DUT's protocol, deliberately not invented by this milestone.**

### 6 — Stimulate and capture · **the pipeline is built and exercised; the end-to-end run is not done**

*Study Designer, dev-bench, Core, API, UI.* Opened by a concrete goal — *"send an NUS shell message to the DUT mid-study, stimulate it over BLE, and get exhaustive logs of everything that happened on the GATTs, from a study I can save and re-run, authored in the UI"* — and by the gap that goal immediately exposed: **it was not expressible.** Steps run strictly in sequence and monitor-everything unsubscribes when its own step ends, **so a stimulus write and a capture could never overlap; every ordering produced an empty capture and a pass.**

Built: a capture window that outlives its step, a streamed uncapped GATT transcript, a free-text payload path alongside the registry, a saved-study library under the firmware repo that doubles as a CLI input, and the Study Designer tab's frontend — **which, it turned out, had never actually been built, only its backend.** A second pass added a vendor GATT catalog, authorable step timing, and connect-by-name, **because "connect to whichever DUT shows up first" reached a different peripheral on consecutive runs of the same study.**

**Running it is what found the real bugs, none of which any test suite would have caught.** The bench's inbound link was *polled*, so every frame larger than the UART's 128-byte FIFO was silently truncated — **and this milestone's own four-step study is the first one this suite ever authored large enough to cross that line, which is why the feature could never have worked.** 16-bit UUIDs were reported two bytes out of place. And connect-with-no-target reached arbitrary nearby peripherals, then **reported "service not found on DUT" about devices that were never under test.** The bench's tests now decode the *real* bytes Core sends, not only what its own encoder produces — the blind spot that let the first one survive.

**Still open, and the DUT-side blocker is understood:** the DUT requires an authenticated link before it tolerates discovery (**asked and answered by the engineer, not inferred**), and the bench registered no pairing callbacks at all, **making that unreachable whatever a study asked.** Four decisions came out of it and are now built. The DUT also rotates its address inside one scan window, **so the name filter is the handle that works and an address is not one.**

### 7 — MCU load tracing · **Phases A–E closed; it works on real hardware**

*Outpost, topology, Core, Study Designer, dev-bench, API, UI.* Opened by a goal nothing in this suite could serve: **"a study told me the DUT responded in 40 ms; I need to know whether that was one busy thread, forty context switches, or an ISR storm."** Every existing component observes the DUT from outside it. This milestone builds the one that ships *inside*: a Zephyr module compiled into the DUT's own debug firmware, emitting compact records out a **TX-only** UART into a lock-free ring, decoded host-side against a build-ID-matched manifest.

**Capture is study-scoped and rendered post-hoc — there is no live feed**, reversing this milestone's own opening framing, deliberately.

Three pieces landed alongside it, none optional: the **dev-bench bypass** became a real modelled route rather than a description of how things happen to be wired (the bench has neither the spare pins nor the pass-through firmware); the **stream pipeline's inbound half was accepted**, which is what kept this from becoming the suite's fourth near-identical capture pipeline; and the UI gained route declaration plus a Trace view. A fourth piece joined the same pass, wider than the outpost that prompted it: **a study now declares the firmware versions it is meant to run against**, closing a gap nobody had named — **a result could not say what firmware it ran against, making two runs of one study against two builds indistinguishable afterwards.**

**Where it stands:** the module builds for the simulator and for the real target; the manifest generator resolves 20 of 20 threads and 13 real ISRs out of a real ELF; Core stores what a flash bound and decodes against it, and **a build-ID mismatch costs the *names*, never the capture**; the UI renders a trace named and timed. **Phase E closed 2026-08-27** with **437,789 bytes in 20 s off a real nRF54L15 — 21.9 KB/s, 43,948 records, zero lost** — and a study then captured a trace on its own tap and the Trace view rendered it.

**What it is still honest to say it does not know:** every Kconfig wire constant is an unmeasured default, the instrumentation's own overhead is **deliberately uncharacterised** (the repo owner's call), and **nothing has compared a trace's placement against a second stream in the same study**, which is the check the dual clock exists to enable.

**Three scope changes worth keeping, because each was a reversal rather than a detail.** Record layout 2 removed every DUT timestamp on the grounds that the per-record read sat inside the context switch and inside the ISR wrapper — **the instrument charging its cost to the path it measures**. Layout 3 then restored it, because **the objection was to the lock, not to the clock, and only the lock had to go**; the version went 2 → 3 and not back to 1, since **a version byte exists so a host can say "I decode up to N", and a number reused after an incompatible wire has worn a higher one cannot say that.** And the host **did not follow the wire for a day**, which cost a 46× error on the one number the next session was briefed to reduce ([reversals](../embarch-decision-reversals.md) rows 62, 80, 86).

**Three things this milestone closed with a *named trigger* rather than as owed work** — the manifest halves, the durable signal alert, and a validation surface with no caller. That pattern is the milestone's own contribution to how this repo handles not-yet: **name what has to be true, rather than carrying a question nobody can answer.**

## Next

- **A real `.eap` protocol run on real hardware.** The mechanism shipped, and it closes the *authoring* half of the blocker milestone 5 named: **an engineer can now state a DUT's protocol instead of the tool guessing it.** The bench's real-time interpreter is built and pinned against the reference one by a literal frame carrying the worked protocol; Core gained the third pre-flight seal alongside it. **What is left is the one thing milestone 5 always named: a real engineer authoring a real manifest for a real DUT.** Nothing has executed one against a radio yet, so **expect the first real run to find something in the BLE half** — discovery, three concurrent subscriptions, and the notification queue under a real chunk burst are the parts no host test reaches. Also owed: a Core redeploy and a bench reflash **in the same sitting**, since the wire moved ([dev-workflow](../embarch-dev-workflow.md) §4a).
- **`embarch-promptu`** — the curated library of firmware-specific skills, subagents and prompt patterns. Planned, no repo.

## Later

- **Core on a Raspberry Pi over the LAN.** Detected and verified today, and **cross-machine token distribution stays manual.** A deliberately late milestone.
- **macOS validation.** Shipped reasoned-only, with no machine to test on; validating it means a Mac-only engineer walking the user guide.
- **Power profiling** — milestone 4 above, deferred by explicit decision. **Resuming it is what unblocks four open questions.**
- **`embarch-atlas`** — static analysis and graph visualization of a firmware codebase, for agents and engineers. Paused, no repo.
- **Adopting `rustfmt`** — deferred by explicit decision 2026-09-06, **on sequencing**: the check that would keep it true lives in [the protocol](../../embarch-fleet/protocol.md) §10 and is the owner's, and formatting first decays immediately. Measured cost, and the reversal condition that fires the moment the check exists: [embarch.md](../embarch.md) §5.

## Release

**`v0.1.0`, shipped 2026-08-11.** Real per-repo tags and releases for every component with code, plus a real assembled suite archive that `doctor`'s manifest check has validated against. **Scope in practice: everything through Onboarding's release-engineering step, which turned out to include three milestones together.**

**"Rochambeau" — superseded, kept for history.** The original working name for "the first release, milestones 1 + 2 only". Never cut under that scope, because release engineering itself turned out to be part of Onboarding's work. **Recorded rather than silently deleted, so the name does not get reused by someone who did not know it was already spent on a plan that did not survive contact with what got built.**
