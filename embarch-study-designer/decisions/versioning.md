# embarch-study-designer decisions: Schema versioning, handshake, and clocks

**Status:** active, 2026-09-02.

Two hand-bumped constants, what each guards, and where time comes from.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 12 — Two hand-bumped schema constants, checked at both connection points

`embarch-core` and `embarch-api` track this crate at head (decision 8) but deploy independently — nothing stops one running a build ahead of the other, and a drifted `Study`/`StudyResult` shape would fail however `serde` happens to fail rather than with a clear error. Bumped only when a wire-relevant type changes, independent of `Cargo.toml`'s own semver.

- **`DEV_BENCH_WIRE_SCHEMA_VERSION`** — checked at `Hello`/`HelloAck`, bumped only by a change to something dev-bench itself parses or emits. This is the number whose movement costs a firmware reflash and a decision 36 both-languages re-pinning pass.
- **`HOST_TYPE_SCHEMA_VERSION`** — checked at `GET /status`, bumped by any change to a type crossing the `embarch-api`↔`embarch-core` hop. A strict superset: every dev-bench wire change plus host-side-only ones.

**Both are mismatch *detectors*, not compatibility *negotiators*** — no fallback to an older wire format, matching the suite's minimal-viable posture (no config hot-reload, single shared token) rather than building version-negotiation machinery nothing needs. A `SchemaVersionMismatch` is downcastable like `StudyConflictError`.

**Why one constant became two, 2026-08-25.** `schema_version.rs` listed `crate::validation` among the modules that bump the single constant. That was half right, and the wrong half mattered: `validations` never reached dev-bench at all (decisions 17, 19), so no change to it could drift a dev-bench decoder — but `Study` *including* `validations` did cross the api→Core hop as JSON, whose only drift check was that same constant. Dropping validation from the trigger list would have created a real undetected failure between two processes this suite genuinely deploys separately ([embarch-dev-workflow.md](../../embarch-dev-workflow.md)); so the constant split instead. `STUDY_DESIGNER_SCHEMA_VERSION` was removed outright rather than kept as an alias, so every call site had to choose which hop it meant — an alias would have let the ambiguity survive.

**Neither constant was renumbered, and that was a decision.** Both continue the single constant's sequence from v8; `schema_version.rs`'s rewritten history says which side each past bump would have belonged to rather than recounting them. Renumbering would make every version string already logged, pinned in a C test, or written into a doc ambiguous about which scheme counted it — the same harm as [embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 18's stale bump number, with a wider blast radius.

**A compile-time assertion holds the invariant:** `HOST_TYPE_SCHEMA_VERSION >= DEV_BENCH_WIRE_SCHEMA_VERSION`. The host constant's triggers are a strict superset so it can never trail, and a wire bump that forgot to move the host one would otherwise leave the api↔Core hop talking across a difference it exists to refuse. Compile-time rather than a test, because the build carrying the bug is not necessarily one anybody ran the suite against.

Three things implementation settled:

- **The api↔Core half had never been built.** This decision described `/status` carrying a version since 2026-07-28; `embarch-core/decisions.md` §4 recorded (2026-08-23) that `status_handler` returned `{status, probes}` and nothing else. So "update the field and the comparison" was *adding* both. `embarch-api`'s comparison lives in `embarch-core-client`'s `post_study`, not at each caller: the CLI and the MCP tool both submit through that one method, and a drift detector only one of them runs is not a detector.
- **A Core that serves no version is a mismatch, not a pass.** `StatusResponse.study_designer_schema_version` is `Option<u32>` purely so such a response still parses and the drift can be named; `None` is refused. The operational consequence was real and not hidden: the then-live Core served no such field, so `embarch-api` refused to submit until it was redeployed. That is the detector working — but it makes Core-first the deployment order for such a pass.
- **The FFI's `essd_schema_version` returns the wire constant**, and there is deliberately no FFI surface for the host one; dev-bench is not a party to that hop. Separately, `study_ffi_stub.c` — the by-hand mirror `native_sim` uses in place of the real staticlib — was found **stale at v4, four bumps behind**, because nothing compares it against the crate by construction. Corrected; the gap in what `native_sim` can prove is unchanged by fixing the number and is recorded in `embarch-dev-bench/decisions.md`.

**`Hello` also does two other jobs.** It is a **hard reset**: receiving one unconditionally tells dev-bench to abort any in-progress `Study` and clear its execution state before replying, which is what lets Core recover a usable connection after its own crash (decision 16) with no separate abort message and no waiting out dev-bench's step timeouts. And it **carries `host_utc_ms: u64`**: dev-bench has no other clock source, so this is its only way to learn wall-clock time at all, seeding/resyncing its UTC offset on every connection and reconnection. That is what makes `Sample.rx_utc_ms` (§4.7) a real UTC timestamp rather than dev-bench-uptime-relative. Best-effort periodic resync, not NTP-style discipline — acceptable drift between resyncs is an open item (§7).

### 30 — Core records its own arrival time on every incoming message

`Sample.rx_utc_ms` is stamped by dev-bench's free-running clock, corrected only when a `Hello` arrives (decision 12) — for a long study with no reconnect, that clock free-runs with no way to correct for it after the fact. Resolved without adding a second resync trigger (decision 12 deliberately ties resync to connection establishment, not a periodic timer): Core timestamps its own receipt of every timing-relevant `DevBenchMessage` using its own wall clock and records it alongside as an additive `core_rx_utc_ms` column, changing `Sample`'s wire shape not at all. This doesn't correct drift in real time; it gives post-hoc analysis the raw material to detect and account for it, which a resync-on-`Hello`-only design otherwise cannot surface.

### 47 — `HelloAck` carries dev-bench's own `hardware_id`

Wire v9 → v10, host v11 → v12. *(Written as host 10 → 11; decision 48 landed first and took 11, so this re-derived to 12 — [embarch-decision-reversals.md](../../embarch-decision-reversals.md) row 18's protocol working as intended, as decisions 44/45's reserved bump also had to.)*

The wire half of [embarch-core/decisions.md](../../embarch-core/decisions.md) decision 35 and the answer to [embarch-topology/decisions.md](../../embarch-topology/decisions.md) §5's UART-and-JTAG-are-different-USB-devices gap, which that doc had correctly described as needing a firmware protocol change it could not make unilaterally. One field on the handshake frame that already carries `schema_version` and `firmware_version`, both of which Core already checks at exactly this moment — so the comparison lands in an existing gate rather than adding one. Dev-bench reads its own chip ID and reports it; Core compares against the identity `hardware::validate_role` just verified over JTAG and refuses the link on a mismatch.

Both constants move per decision 12's rule: the wire one because a message dev-bench encodes changed shape, the host one because its triggers are a superset and the compile-time assertion refuses to let it trail.

**An empty `hardware_id` is a real value, not an absent field**, and both sides test it: a board whose Zephyr build has no `hwinfo` driver reports `""`, which still writes its length prefix and leaves the frame walkable. Core's comparison is where "no ID" acquires meaning — the encoder's job is only to carry it faithfully.

Decision 36's both-languages pinning applied in full, and the interesting part is that **`HelloAck` had never been pinned at all** — like `StepResult`, it predates that rule. `WIRE_HELLO_ACK` here and `test_hello_ack_encodes_to_the_pinned_wire_bytes` in dev-bench's ztest suite now hold the same 30 bytes from both sides. They agreed on the first run.

---

