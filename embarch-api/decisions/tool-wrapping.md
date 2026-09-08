# embarch-api decisions: Per-tool wrapping

**Status:** active, 2026-09-07.

Why a given tool exists (or deliberately doesn't), its params, and what its description promises — one entry per addition, which is why this file is the one that grows on every new tool. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). JSON shape and error handling shared by every tool: [surface.md](surface.md).

### 23 — No `doctor` tool here, deliberately
Adding one means reimplementing `embarch-umbrella`'s diagnostic chain or depending on its binary — both break the one-way relationship that keeps this crate unaware umbrella exists. Resolved by **stating what was left for an agent to discover**: shell out to `embarch doctor --json`, assume no equivalent here. (Reporting one compiled constant is not diagnosing — decision 52.)

### 29 — The study data tools are named ahead of being implemented
The posture every planned-but-unbuilt row here uses: a name matching what the shared crate locks in, chosen before the work, **so the tables never name something that will change.**

### 34 — `enroll_probe`, wrapping Core's enrollment endpoint
The two-layer wrapping every other Core capability gets. **No selection params**: enrollment is not build-target selection but "record which physical probe I mean" — the precedent for anything not project-shaped. **The guided flow is conversational, not a single call**, and enforcement is not client-side: Core's refusal on anything but exactly one attached probe is what makes "plug in only the board you mean" hold. No new config schema — the resulting table is Core-local knowledge.

### 35 — `validate` and `alerts`, and "relay, don't auto-open" confirmed for the agent path
A mismatch comes back naming recorded vs. live hardware ID with the fix-it URL **as plain text** — never fetched or opened, mirroring the CLI and Core's posture toward callers; whatever is in the human's hands decides. These are the suite's only end-to-end exercise of that leaning from the agent side, so it is confirmed rather than reasoned-about.

### 47 — Live study events are a flag on `study-status` and a bounded twin tool, not one shared surface
"What is this study doing" is one question with a name already, so the CLI gets `study-status --follow` rather than a second subcommand: a caller should not have to know *which mechanism* answers, since a follow that loses its stream keeps answering by polling. The flag promises **watch until it is done**, not "use SSE", so the fallback is not a broken promise. `--json` on it is **NDJSON** — one object per line, `summary` last — the only `--json` here that is not one object, because a reader of a live feed has to see a record before the last one has happened.

**MCP cannot take the same flag.** A tool call is request/response, so `study_watch` is bounded on three axes: `wait_secs` (60, capped 600) — call again to keep watching; `max_events` (100, capped 1000); and `include_samples`, **false by default**, counting `SampleBatch`/`GattTranscript` per tap rather than listing them. Without the last, one study with a power tap returns tens of thousands of events into an agent's context, and the bulk data has its own exit (`study_stream_data`).

*Rejected: making `study_status` itself stream.* It has one shape callers depend on; polling stays as it was.

### 41 — `erase` exists, and its *description* is the design point
The surface half of Core's erase delegation. **Every other argument on these tools is a routine knob** — a chip name, a path, a probe serial — and an agent reaching for one more costs nothing. `erase` is the only one that can leave a board unrecoverable by any other tool in the suite, and an LLM picking it because "a clean flash sounds more thorough" is a realistic failure mode. So the description states plainly that it is a **destructive full-chip erase**, that a non-erase flash cannot undo it, and that a normal reflash does not need it. `false` by default, never implicitly `true`.

**This crate does not choose the erase mechanism and must not grow its own.** Which tool performs it, and whether a target supports one, is Core's; a refusal is surfaced verbatim, never retried by another route.

### 52 — The compiled host type schema version is its own subcommand, not a field on `status`
This crate compiles in `embarch-study-designer`'s `HOST_TYPE_SCHEMA_VERSION` and refuses every study submit where Core's served copy differs ([core-link](core-link.md) 17). That number **was readable from nowhere outside the process** — `--version` prints the crate version, `status --json` returns Core's probes — so `embarch-umbrella`'s `doctor` check 11 substituted the `embarch` binary's *own* copy: exact when all three binaries came from one archive, **wrong precisely for a hand-built mixed install, which is how this suite is developed.** `embarch-api versions` prints it; `--json` names it `host_type_schema_version`.

*Rejected: a field on `status --json`*, on the grounds that the object is already stamped and this is one key. **`status` is *Core's* state**: it needs a loadable config **and** a reachable, authenticated Core, and returns `success: false` without both. A compiled constant needs neither. Putting it there answers "what is this binary" only when nothing is broken, handing the check that catches a mismatched install its number on exactly the machines least likely to have one. **A diagnostic's input has to survive a broken machine or it is not worth building**, so `versions` is dispatched in `main` *before* config resolution, and `tests/json_surface.rs` pins that it answers with a config path that does not exist and with none at all. Lesser: a subcommand carries `api_version` too without growing an unrelated object, and cannot be misread as Core's word.

*Rejected: folding it into clap's `--version` string* — human text a caller parses by shape, which is what "machine-readable" was asking not to be.

**The payload key is `host_type_schema_version`, deliberately not `schema_version`.** The object already carries decision 24's stamp under that name, versioning this crate's *JSON shape*. The two counters are unrelated, and one name over both is how a consumer comes to compare the wrong pair.

**CLI-only, no MCP twin.** [spec.md](../spec.md) §1 guarantees CLI ⊇ MCP — a human can do anything an agent can — which a CLI-only diagnostic leaves intact. The consumer is a process shelling out, and an agent submitting a study already learns of a mismatch from the refusal, when it matters.

*Read since 2026-09-04:* `embarch-umbrella` check 11 shells out to it (its 33, 35, 36); that binary's own constant is now warn-only. **Read live 2026-09-07** — check 11 PASS, and `embarch-api --json versions` answered v17 against Core's v17 (`tasks/umbrella/034`).

### 59 — `dev_bench_hello`, and `link_identity` is a stable string on purpose
`GET /dev-bench/hello` (`embarch-core` `study::hello_handler`) is the only route in
the suite that serves the JTAG-read identity, the bench's own self-reported
identity, and how they relate, together — and until now nothing on this crate's
MCP surface reached it (`tasks/api/036`). Wrapped as `dev_bench_hello`: no params,
no project selection, since the route itself takes none.

**Mirrors Core's own serialized `HelloAckInfo` field-for-field, not
`embarch_topology::hardware`'s comparison type** — the two are never checked
against each other (this crate cannot link the `hardware` feature, the same
constraint `SignalLink`'s own mirror lives under), so a struct built from the
wrong side compiles and passes its own tests while failing against a real Core.
`embarch-core-client`'s `HelloAckResponse` gained `self_reported_hardware_id`,
`link_identity` and `probe_hardware_id` alongside the three fields it already
had; no route parsed those three before this, so nothing existing could regress.

**`link_identity` is reported as its own string field, never folded into
`compatible` or any boolean.** Today's real value for every chip is
`"undeclared"` (Core §3 decision 35): the comparison could not be made, which is
not the same fact as "verified" and must not render as one. A caller reading
only `compatible` and ignoring this field has thrown away the one thing this
route exists to report — so the tool description spells out all four possible
values (`match`/`mismatch`/`not-reported`/`undeclared`) and says outright that
the latter two are not a pass.

**`409` and `502` get distinct error text in the tool, not only distinct HTTP
status.** `409` (`DevBenchBusyError`) means a study already has the link and
this call was refused rather than raced — a wait-and-retry, not a fault. `502`
(`DevBenchHandshakeError`) means the handshake itself failed — a real bench
problem. Collapsing both into one generic failure message would send an agent
to the wrong next action either way, so both the client (two downcastable error
types) and the tool description (which states the call opens and closes the
bench link, so a `409` mid-study is not read as a bug) say which is which.
