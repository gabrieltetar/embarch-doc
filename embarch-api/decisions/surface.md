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

### 41 — `erase` exists, and its *description* is the design point
The surface half of Core's erase delegation. **Every other argument on these tools is a routine knob** — a chip name, a path, a probe serial — and an agent reaching for one more costs nothing. `erase` is the only argument here that can leave a board unrecoverable by any other tool in the suite, and an LLM picking it because "a clean flash sounds more thorough" is a realistic failure mode, not a contrived one. So the description states plainly that it is a **destructive full-chip erase**, that a non-erase flash cannot undo it, and that a normal reflash does not need it. `false` by default, and never sent implicitly as `true` by any convenience path.

**This crate does not choose the erase mechanism and must not grow its own.** Which tool performs it, and whether a target supports one, is Core's. A refusal is surfaced verbatim rather than retried by another route.
