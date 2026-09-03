# embarch-api decisions: The tool and CLI surface

**Status:** active, 2026-09-03.

What the two front-ends expose, how failures are shaped, and the arguments whose *description* is the design.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 16 — `error_kind` on the `--json` object (retired 2026-09-03, see decision 50)
Core's error code passed through verbatim on a Core-originated failure, one of a small native set otherwise, so a script could branch on failure kind rather than on a finer exit-code taxonomy. **Never built, and retired rather than built** — decision 50 has the argument. A caller branches on `success` plus the exit code; the finer signal is now an [open.md](../open.md) item with a named prerequisite in a different repo.

### 24 — `schema_version` on every `--json` object
It is there **from the start rather than after a consumer depends on an unversioned shape** — an anticipated UI is exactly the kind of external reader that would otherwise have no way to detect a breaking change. Bumped by hand only on a rename, removal or retype; adding a field is not a bump, since a reader that ignores unknown fields is unaffected.

**Built 2026-09-03, having been documented and absent since this crate's first commit** (decision 50). Two things the original entry left implicit and the implementation had to settle:

- **`1` means "the shape as of 2026-09-03"**, not "unchanged since the beginning". The surface moved repeatedly while unversioned and no honest earlier number exists, so the counter starts where the guarantee starts.
- **It is this crate's own counter and leans on nothing Core serves.** Core's `/status` carries `core_version` and `study_designer_schema_version` and deliberately **no** contract version, so there is no upstream number to derive this one from — and it would be the wrong number anyway: this field versions *this crate's* `--json` shape, which can change without Core moving at all.
- **Every NDJSON line of `study-status --follow` carries it too**, not only that stream's `summary` line — which is stronger than this entry's "the `--json` object" and follows from decision 47's own argument: a reader of a live feed has to know the shape from the first record, not from the one that arrives after the study finishes.

### 50 — `schema_version` built, `error_kind` retired, and one serializer to keep the first honest
Decisions 16 and 24 were written together and neither was built: from the first commit until 2026-09-03 neither string appeared in this crate, while [tools.md](../interfaces/tools.md) told a caller to read both. The two halves were **not** equally cheap to keep, so they got different endings.

**`schema_version` was ~10 lines and is built.** The CLI already funnelled every `--json` object through one function (`finish`), so the field cost a stamp in one place, and decision 24's motivating reader — "an anticipated UI" — now exists.

**`error_kind` is retired because its headline half cannot be delivered.** "Core's own error code verbatim" needs Core's structured `{code, message, cause}` body (`embarch-core` decision 12) to *reach* this crate as a code. It does not: **Core serves plain text on every non-2xx**, and that body was formally deferred-with-a-trigger on 2026-09-03 rather than built. `embarch-core-client` attempts to parse the shape on `/study/*` and immediately flattens whatever it gets into a prose string, so even the one endpoint that tries has no code to hand on. So building `error_kind` honestly means Core first, then a new public typed error on the shared crate `embarch-ui` also depends on, then a kind chosen at ~43 error sites here — and the field would still be native-set-only or absent for most real failures. **That is a second documented-but-not-really-there field, bought at several times the cost of the one that could be kept.**

**The cheap substitute is a trap, and this is the entry that says so.** The only machine-readable signal crossing the api→Core hop today is the HTTP status code. An `error_kind` derived from it would be **strictly coarser than decision 12's `code` enum** — one token per status, not per failure mode — and shipping it under decision 16's name is how two different vocabularies come to be assumed to be one. If the field returns, it returns carrying Core's codes, or under a different name that says what it actually is. The exit code stays a single `1`; "CLI exit-code granularity", which decision 16 claimed to retire, is open again as an [open.md](../open.md) item with its prerequisite named and ordered.

**The field is unconditional by construction, not by convention** — the task's own condition, and the thing whose absence let this rot for the crate's whole life. `json_out` is the only module that turns a `serde_json` value into text; `finish`, the two NDJSON sites and MCP's `ok_json`/`err_json` all route through it, so an emitter gets the stamp by existing. A source-level guard test fails if `cli.rs` or `tools.rs` grows a serializer of its own, and `tests/json_surface.rs` drives **every** subcommand through the real binary and asserts the field on whatever each one printed. A tripwire test on the subcommand count is what stops a new subcommand from being added without being added there.

*Found and fixed in the same pass:* a startup failure — unreadable config, unresolvable token — escaped as `main`'s `anyhow::Error`, so `--json` printed **nothing at all** and exited 1. tools.md promised that failure as an object on stdout, for exactly the class a script hits first on a fresh machine. CLI mode now emits it through the same path; MCP mode still returns the error, since there is no JSON surface to put it on.

### 18 — Truncation keeps head *and* tail, not just the tail
For a Zephyr build the **first** compiler error is usually the actionable one, and a long build's early failure can scroll entirely out of a tail-only cap by the time `cmake` and `ninja` finish emitting later, less useful output. Head plus tail with a marker naming how much was dropped from the middle; unchanged for anything under the cap.

### 23 — No `doctor` tool here, deliberately
Adding one would mean either reimplementing `embarch-umbrella`'s full diagnostic chain or gaining a dependency on its binary — both break the one-way relationship that keeps this crate unaware umbrella exists. Resolved instead by **stating explicitly what was previously left for an agent to discover**: shell out to `embarch doctor --json`, do not assume an equivalent tool exists here.

### 29 — Naming the study data tools ahead of implementing them
Previously left as "a small remaining item, deferred to whichever milestone implements this surface". Named to match what the shared crate locks in, ahead of the work — the same posture every other planned-but-unbuilt row already uses, so the surface tables never describe a name that will change.

### 34 — `enroll_probe`, wrapping Core's enrollment endpoint
The two-layer wrapping every other Core capability gets. It takes **no selection params**, since enrollment is not build-target selection but "record which physical probe I mean" — matching the precedent already set for things that are genuinely not project-shaped. **The guided flow is conversational, not a single call**, and the enforcement is not client-side: Core's refusal on anything but exactly one attached probe is what actually makes "plug in only the board you mean" hold. No new config schema, because the resulting table is Core-local knowledge, not this crate's to store.

### 35 — `validate` and `alerts`, and "relay, don't auto-open" confirmed for the agent path
Until these, no surface here called into the topology crate's validate or alert mechanism at all, so the suite's relay-don't-auto-open leaning for a mismatch's fix-it URL had **nothing exercising it end to end from the agent side**. A mismatch comes back as an error naming recorded vs. live hardware ID and the URL **as plain text** — the tool never fetches or opens it, mirroring the CLI's own behaviour and Core's posture toward its callers. Whatever is in the human's hands decides whether to open it. This decision does not re-litigate that; it gives it a real call site so it is confirmed rather than reasoned-about.

### 47 — Live study events are a flag on `study-status` and a bounded twin tool, not one shared surface
"What is this study doing" is one question and it already has a name, so the CLI gets `study-status --follow` rather than a second subcommand: a caller should not have to know *which mechanism* answers, which is the point, since a follow that loses its stream keeps answering by polling. The flag promises **watch until it is done**, not "use SSE", so the fallback is not a broken promise. `--json` on it is **NDJSON** — one object per line, a `summary` line last — and it is the only `--json` in this surface that is not one object, because a reader of a live feed has to see a record before the last one has happened.

**MCP cannot take the same flag.** A tool call is request/response, so `study_watch` is bounded on three axes instead: `wait_secs` (60, capped 600) — call it again to keep watching; `max_events` (100, capped 1000); and `include_samples`, **false by default**, which counts `SampleBatch`/`GattTranscript` per tap rather than listing them. Without that last one a single study with a power tap would return tens of thousands of events into an agent's context, and the bulk data already has a right way out (`study_stream_data`).

*Rejected: making `study_status` itself stream.* It has one shape today and callers depend on it; polling stays exactly as it was.

### 41 — `erase` exists, and its *description* is the design point
The surface half of Core's erase delegation. **Every other argument on these tools is a routine knob** — a chip name, a path, a probe serial — and an agent reaching for one more costs nothing. `erase` is the only argument here that can leave a board unrecoverable by any other tool in the suite, and an LLM picking it because "a clean flash sounds more thorough" is a realistic failure mode, not a contrived one. So the description states plainly that it is a **destructive full-chip erase**, that a non-erase flash cannot undo it, and that a normal reflash does not need it. `false` by default, and never sent implicitly as `true` by any convenience path.

**This crate does not choose the erase mechanism and must not grow its own.** Which tool performs it, and whether a target supports one, is Core's. A refusal is surfaced verbatim rather than retried by another route.
