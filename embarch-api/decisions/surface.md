# embarch-api decisions: The tool and CLI surface

**Status:** active, 2026-09-02.

What the two front-ends expose, how failures are shaped, and the arguments whose *description* is the design.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 16, 24 — `error_kind` and `schema_version` on the `--json` object
Core's structured error body gives a real error *kind* to pass through instead of parsing prose: a Core-originated failure's code becomes `error_kind` verbatim. For a failure that never reaches Core — an unloadable config, a build that failed before any HTTP call, an unresolvable target — it takes one of a small native set instead. **This retires "CLI exit-code granularity" as a distinct problem:** a script that needs to branch on failure kind now has a field, not a reason to invent a finer exit-code taxonomy.

`schema_version` is there **from the start rather than after a consumer depends on an unversioned shape** — an anticipated UI is exactly the kind of external reader that would otherwise have no way to detect a breaking change. Bumped by hand only on a rename, removal or retype.

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
