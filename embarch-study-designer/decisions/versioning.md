# embarch-study-designer decisions: Schema versioning, handshake, and clocks

**Status:** active, 2026-09-02.

Two hand-bumped constants, what each guards, and where time comes from.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 12 — Two hand-bumped schema constants, checked at both connection points

Core and the API track this crate at head but **deploy independently — nothing stops one running a build ahead of the other, and a drifted type would fail however serde happens to fail rather than with a clear error.** Bumped only when a wire-relevant type changes, independent of the crate's own semver.

- **The wire constant** — checked at the handshake, bumped only by a change to something dev-bench itself parses or emits. **This is the number whose movement costs a firmware reflash and a decision 36 re-pinning pass.**
- **The host constant** — checked at the status endpoint, bumped by any change to a type crossing the API↔Core hop. **A strict superset: every wire change plus host-only ones.**

**Both are mismatch *detectors*, not compatibility *negotiators*** — no fallback to an older format, matching the suite's minimal-viable posture rather than **building version-negotiation machinery nothing needs.**

**Why one constant became two.** The trigger list included the validation module. **That was half right, and the wrong half mattered:** validations never reached dev-bench at all, so no change there could drift a firmware decoder — **but a study *including* validations did cross the API→Core hop, whose only drift check was that same constant.** Dropping validation from the list **would have created a real undetected failure between two processes this suite genuinely deploys separately**, so the constant split instead. The old name was **removed outright rather than kept as an alias, so every call site had to choose which hop it meant — an alias would have let the ambiguity survive.**

**Neither constant was renumbered, and that was a decision.** Both continue the single constant's sequence. **Renumbering would make every version string already logged, pinned in a C test, or written into a doc ambiguous about which scheme counted it** — the same harm as [reversals](../../embarch-decision-reversals.md) row 18's stale bump number, with a wider blast radius.

**A compile-time assertion holds the invariant** that the host constant never trails the wire one. **Compile-time rather than a test, because the build carrying the bug is not necessarily one anybody ran the suite against.**

Three things implementation settled:

- **The API↔Core half had never been built.** This decision described the status endpoint carrying a version for a month; the endpoint returned status and probes and nothing else. **So "update the field and the comparison" was *adding* both.** The comparison lives in the shared client's submit path, not at each caller: **the CLI and the MCP tool both submit through that one method, and a drift detector only one of them runs is not a detector.**
- **A Core that serves no version is a mismatch, not a pass.** The field is optional purely so such a response still parses and the drift can be named. **The operational consequence was real and not hidden:** the then-live Core served no such field, **so the API refused to submit until it was redeployed. That is the detector working — but it makes Core-first the deployment order for such a pass.**
- **The FFI exposes the wire constant only**; dev-bench is not a party to the host hop. Separately the by-hand C mirror the simulator uses **was found stale at four bumps behind, because nothing compares it against the crate by construction.** Corrected, and **the gap in what a simulator run can prove is unchanged by fixing the number.**

**The handshake also does two other jobs.** It is a **hard reset**: receiving one unconditionally tells the bench to abort any in-progress study and clear its execution state before replying, **which is what lets Core recover a usable connection after its own crash with no separate abort message and no waiting out step timeouts.** And it **carries host wall-clock time**, because **the bench has no other clock source at all** — this is its only way to learn it, seeding its offset on every connection. Best-effort resync, not disciplined: acceptable drift between resyncs is open.

**The seeding half was designed and never built** — a sentence claiming it made the timestamp real UTC is struck here, 2026-09-10. Decision 72.

### 30 — Core records its own arrival time on every incoming message

A sample's timestamp comes from the bench's free-running clock, corrected only at a handshake — **so for a long study with no reconnect that clock free-runs with no way to correct for it after the fact.** Resolved **without adding a second resync trigger**: Core stamps its own receipt of every timing-relevant message and records it alongside as an additive column, **changing the wire shape not at all.**

**This does not correct drift in real time; it gives post-hoc analysis the raw material to detect and account for it**, which a resync-on-handshake-only design otherwise cannot surface.

### 72 — `Sample::rx_utc_ms` carries bench uptime, and the name's promise is corrected rather than kept

**Three contracts asserted a clock resync that no firmware performs**, and they said it in stronger words the closer they got to a reader: this crate's `interfaces/decoders.md` ("seeded and resynced from the host on every handshake"), decision 12's paragraph above ("that is what makes a sample's timestamp a real UTC one rather than uptime-relative"), and `src/protocol.rs`'s own doc comment on `Hello.host_utc_ms` ("which is what makes `Sample::rx_utc_ms` meaningful"). The firmware decodes `host_utc_ms`, stores it, and reads it from nothing but a round-trip test; `ble_bridge_real.c` stamps `k_uptime_get()` and no offset arithmetic exists anywhere in the build. `embarch-dev-bench/open.md` has said so plainly the whole time — **the only place in the suite that contradicted the three was another repo's list of unresolved questions**, which is precisely where nobody reading a CSV column would look.

**So the field is documented as what it is: milliseconds since the bench booted.** Corrected at all three sites, and `tasks/suite/016`'s first acceptance condition takes its own second arm — *"or the exception is named at the point a consumer reads it"* — because every consumer of this column now meets the exception where the column is described.

**The rename is not made here, deliberately.** `rx_utc_ms` names a column in Core's study CSV header, the transcript, `embarch-study-designer`'s `Sample`, and dev-bench's wire struct, and the same name in an **outpost** trace file carries Core's real epoch clock. Renaming it is a coordinated change across four repos and every already-written capture file, and doing it in the same pass as establishing what the field means would leave nobody able to say which half broke a reader. `tasks/suite/027` carried the rename with that argument attached, and **settled it the other way on 2026-09-12: the name is kept in both homes and every home now says which clock it is** ([suite decision 3](../../suite/decisions.md)). The rename stays available and is the owner's, with the board in front of him.

**What would make decision 12's removed sentence true again:** dev-bench applying the offset it already receives — one subtraction at the stamp site — after which `rx_utc_ms` becomes what its name says and `embarch-dev-bench/open.md`'s standing bullet closes with it. Until then, **`core_rx_utc_ms` is the column to plot against anything else in this suite**, and `rx_utc_ms` answers intervals within one capture and nothing wider.

*Rejected:* fixing the firmware in this pass. It is a real change to a real board's timestamps, it invalidates the comparability of every capture taken before it against every capture taken after, and it needs the bench — which this leg does not touch.

### 47 — The handshake carries dev-bench's own hardware ID

The wire half of Core's same-chip gate, and the answer to a topology gap **that doc had correctly described as needing a firmware protocol change it could not make unilaterally.** One field on the frame that already carries the schema and firmware versions, **both of which Core already checks at exactly this moment — so the comparison lands in an existing gate rather than adding one.** The bench reads its own chip ID and reports it; **Core compares against the identity it just verified over JTAG and refuses the link on a mismatch.**

**An empty ID is a real value, not an absent field**, and both sides test it: a board whose build has no hardware-info driver reports empty, **which still writes its length prefix and leaves the frame walkable.** **Core's comparison is where "no ID" acquires meaning — the encoder's job is only to carry it faithfully.**

Decision 36's pinning applied in full, **and the interesting part is that the handshake frame had never been pinned at all** — like the step result, **it predates that rule.** Both sides now hold the same 30 bytes. **They agreed on the first run.**
