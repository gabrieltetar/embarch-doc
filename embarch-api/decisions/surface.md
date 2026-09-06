# embarch-api decisions: The tool and CLI surface

**Status:** active, 2026-09-03.

What the two front-ends expose, how failures are shaped, and the arguments whose *description* is the design. Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 16 — `error_kind` on the `--json` object (retired 2026-09-03, see decision 50)
Core's error code passed through verbatim on a Core-originated failure, one of a small native set otherwise, so a script could branch on failure kind rather than on a finer exit-code taxonomy. **Never built, and retired rather than built** — decision 50 has the argument. A caller branches on `success` plus the exit code; the finer signal is an [open.md](../open.md) item with a prerequisite in another repo.

### 24 — `schema_version` on every `--json` object
It is there **from the start rather than after a consumer depends on an unversioned shape** — an anticipated UI is exactly the external reader that would otherwise have no way to detect a breaking change. Bumped by hand only on a rename, removal or retype; adding a field is not, since a reader that ignores unknown fields is unaffected.

- **`1` means "the shape as of 2026-09-03"**, not "unchanged since the beginning". The surface moved repeatedly while unversioned and no honest earlier number exists, so the counter starts where the guarantee starts.
- **It is this crate's own counter and leans on nothing Core serves.** Core's `/status` carries `core_version` and `study_designer_schema_version` and deliberately **no** contract version — and an upstream number would be the wrong one anyway: this versions *this crate's* `--json` shape, which moves without Core moving.
- **Every NDJSON line of `study-status --follow` carries it too**, not only that stream's `summary` — stronger than this entry's "the `--json` object", and decision 47's own argument: a reader of a live feed has to know the shape from the first record.

### 50 — `schema_version` built, `error_kind` retired, and one serializer to keep the first honest
Decisions 16 and 24 were written together and neither was built, while [tools.md](../interfaces/tools.md) told a caller to read both. The two were **not** equally cheap to keep, so they got different endings.

**`schema_version` is built**, at the cost of a stamp in the one function every `--json` object already funnelled through.

**`error_kind` is retired because its headline half cannot be delivered.** "Core's own error code verbatim" needs Core's structured `{code, message, cause}` body (`embarch-core` decision 12) to *reach* this crate as a code. It does not: **Core serves plain text on every non-2xx**, and that body is deferred-with-a-trigger. `embarch-core-client` parses the shape on `/study/*` and immediately flattens it to prose, so even the one endpoint that tries has no code to hand on. Building it honestly means Core first, then a new public typed error on the shared crate `embarch-ui` also depends on, then a kind chosen at ~43 sites here — and it would still be absent for most failures. **A second documented-but-not-really-there field, at several times the cost of the one that could be kept.**

**The cheap substitute is a trap, and this is the entry that says so.** The only machine-readable signal crossing the api→Core hop today is the HTTP status code, and a kind derived from it is **strictly coarser than decision 12's `code` enum** — one token per status, not per failure mode. Shipping that under decision 16's name is how two vocabularies come to be assumed to be one. If the field returns, it carries Core's codes or a different name. The exit code stays a single `1`; exit-code granularity is open again in [open.md](../open.md), prerequisite named.

**The field is unconditional by construction, not by convention** — the thing whose absence let this rot for the crate's whole life. `json_out` is the only module turning a `serde_json` value into text; `finish`, the NDJSON sites and MCP's `ok_json`/`err_json` route through it, so an emitter gets the stamp by existing. A guard test fails if `cli.rs` or `tools.rs` grows a serializer of its own, `tests/json_surface.rs` drives **every** subcommand through the real binary, and a tripwire on the subcommand count stops a new one being added without being added there. **The same path carries a startup failure** — unreadable config, unresolvable token — which had escaped as `main`'s `anyhow::Error`, printing **nothing at all** under `--json`; MCP mode still returns the error, having no JSON surface to put it on.

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

*Read since 2026-09-04:* `embarch-umbrella` check 11 shells out to it (its 33, 35, 36); that binary's own constant is now warn-only. No live `doctor` run yet — umbrella's debt.
