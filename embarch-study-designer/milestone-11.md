# embarch-study-designer: milestone 11 — Study Designer UI

**Status:** draft, 2026-08-24. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 5 ("Study Designer UI" — filed on disk as `milestone-11`, continuing past Milestone 4's reserved `milestone-10`). See [design.md](design.md) §3 decisions 34/35 for the durable decisions this doc turns into steps.

## 1. Goal, restated

Decisions 34/35 are design-only as of the pass that produced them — no code exists yet. This milestone writes it: a local web UI, living inside this crate, whose main surface is a table-based `Study` builder; a merged action list (built-in `Action`s + live `GattDiscover` + static `GattConfigExtractor`); and a user-authored custom-action registry (name + enumerated parameter values, persisted in a firmware repo's own `embarch/` folder) that the UI reads and writes. The UI can submit a `Study` and watch it run, but never flashes or provisions hardware itself.

**What this milestone cannot close by itself, and shouldn't try to:** getting real captured GATT activity out of a specific DUT (the failure that opened this whole design pass) requires a human who actually knows that DUT's protocol to register at least one real custom action through this UI. This milestone's own Definition of Done is the pipeline working — accepting engineer input and acting on it correctly — not a specific DUT finally streaming data. §3.8 below is that real-hardware step, and it is explicitly gated on the user supplying the action, not on this milestone inventing one.

## 2. Scope for this milestone

- **Lives entirely inside `embarch-study-designer`**, a new `std`-only, feature-gated binary (`study-ui` feature, matching `gatt-extract`'s existing precedent) — never linked by dev-bench firmware or gated behind `#![no_std]`.
- **Registry file:** `<firmware-repo>/embarch/study-actions.toml`, sibling to `embarch.toml`, same TOML format convention. Locking this in now — decision 35 left the exact name/format as an implementation detail for this doc to resolve.
- **Core access, submit-and-poll only:** the UI shells out to `embarch-api`'s existing `run-study --study-file <path>` / `study-status <id>` CLI subcommands as subprocesses (decision 34's own "Recommended" option, not contradicted since) — zero new HTTP/auth/`base_url` resolution code, and no dependency-direction change (`embarch-api` still depends on this crate, not the reverse). Live `GattDiscover` for the merged action list (§2.2) works the same way: the UI shells out to submit a small ad hoc one-step `GattDiscover` `Study` and reads its result back, rather than growing its own Core client.
- **Web framework: `axum`**, matching `embarch-topology`'s own local-UI precedent (`embarch-topology/design.md` §3 decision 5) — one dependency shape already proven in this suite, not a new one.
- **Out of scope:** anything that flashes or provisions hardware (stays `embarch-api`'s job, unchanged); a semantic "what does this action do" field anywhere in the registry (decision 35's own explicit non-goal); multi-user/concurrent-editing of the same registry file (single-engineer scope, matching `embarch.md` §5's suite-wide stance).

## 3. Steps

### 3.1 Registry schema and parser — done, 2026-08-24

New `src/registry.rs`, `study-ui`-feature-gated, `std`-only: `RegisteredAction { name, uuid, operation: RegisteredOperation, fields: Vec<ActionField> }` (`RegisteredOperation` is `Read`/`Write`/`Subscribe`/`Notify`/`Indicate` — a subset of `GattOperation`, not the type itself, since a registry entry has no per-call timeout). `ActionField { name, byte_offset, byte_len, values: Vec<ActionFieldValue> }`; `ActionFieldValue { label, bytes: Vec<u8> }` — **the exact literal bytes for that choice, engineer-supplied, not a numeric value this module would have to encode itself.** Deliberately not `value: u64`/similar as originally sketched here: encoding a number into bytes requires assuming a width and endianness, which is precisely the kind of DUT-protocol fact nobody writing this module is in a position to know — the engineer supplies the final bytes directly, and building a payload from a chosen value is a pure byte-offset splice, no interpretation. `ActionRegistry::validate()` checks every value's `bytes.len()` against its field's own `byte_len`, named as `RegistryError::FieldLengthMismatch` rather than silently truncating/padding a hand-edited file's mistake. `load`/`save` at `<firmware-repo>/embarch/study-actions.toml`; a missing file loads as an empty registry, not an error (§5's own "no `init`-equivalent yet" note). 8 unit tests (round-trip through TOML, save-then-load on disk, a missing file, a validation failure both in-memory and loaded from disk).

### 3.2 Merged action-list function — done, 2026-08-24

New `src/merged_actions.rs`, `study-ui`-feature-gated, `std`-only: `merge_actions(live: Option<&[GattServiceInfo]>, static_extraction: Option<&[GattServiceInfo]>, registry: &ActionRegistry) -> Vec<MergedAction>`, pure and offline. `MergedAction` is `BuiltIn` (the three one-click actions this list always offers — `BleConnect`/`GattDiscover`/`GattMonitorAll`; `DataExchange` is deliberately not one, since authoring it directly means already knowing a raw UUID+payload, exactly what this feature exists to avoid), `Registered` (a characteristic with at least one engineer-registered action, shown by name), or `Unregistered { uuid, properties, sources }` (detected by live discovery and/or static extraction, not yet named — `DiscoverySources` records which). A registered characteristic is deduplicated against its own detection — it shows once, as `Registered`, never also as `Unregistered`. Order is deterministic (built-ins, then registry order, then first-seen detection order) so identical inputs always render identically. 5 unit tests, including a registered action persisting in the list with no matching discovery at all (the registry is the source of truth once an action is named, not contingent on this particular run finding it again).

### 3.3 Web UI skeleton: the Study table

`axum` server (`bin/study_ui.rs`, `study-ui` feature) serving one page: an editable table, one row per `Step` — action dropdown (from §3.2's merged list), parameter dropdowns (enumerated values for a registered action; the natural fields for a built-in `Action`), `timeout_ms`, `continue_on_fail`. Add/remove/reorder rows client-side; "sequencing" is row order, no separate field (decision 34's own call). A "Save" action serializes the table into a real `Study` (matching §4.1's schema exactly — `steps_crc` left as 0/omitted, since whichever `run-study` call submits it recomputes that regardless, per `embarch-study-designer/design.md` §3 decision 26).

### 3.4 Registry management UI

A second, linked view: pick a detected-but-unregistered characteristic from §3.2's list, fill in a name, operation, and (for a write) named fields with enumerated `{label, value}` pairs — no free-text "what it does" field anywhere in this form, per decision 35. Saves back to `<firmware-repo>/embarch/study-actions.toml` (§3.1). This is the actual pipeline decision 35 exists for — the only place in this whole feature where DUT-specific knowledge enters the system, and it only ever comes from whoever's sitting at this form.

### 3.5 Run and watch

A "Run" action on the table view: writes the current table's `Study` to a temp file, shells out to `embarch-api run-study --study-file <path>`, captures the returned `study_id`, then polls `embarch-api study-status <id>` (matching this crate's own "poll loop is the intended backpressure mechanism" stance, §3 decision 29) and renders each step's live outcome (`Pass`/`Fail`/`TimedOut`/still-running) as it updates — no new Core-facing code, both calls are existing `embarch-api` CLI subcommands run as subprocesses.

### 3.6 A one-click "discover" action, backing §3.2's live half

A small button that submits a one-step `BleConnect`→`GattDiscover` `Study` the same way §3.5 does, and folds the result into the merged action list — this is what makes "live discovery" in §2/§3.2 concrete rather than requiring the engineer to already have a `GattDiscover` result lying around from some other run.

### 3.7 Unit tests

§3.1's parser (round-trip a `study-actions.toml` fixture), §3.2's merge function (every combination of built-in/live/static/registered present or absent), and §3.3's table-to-`Study` serialization (confirm it produces a schema-valid `Study` `serde_json` can deserialize back, matching this crate's existing round-trip-test discipline).

### 3.8 Real-hardware validation — gated on the user, not on this milestone alone

Once §3.1–3.7 are code-complete and unit-tested: the user (or a firmware engineer with real knowledge of a real DUT's protocol) registers at least one real custom action through the UI built in §3.4, builds a `Study` using it through §3.3, and runs it through §3.5 against real hardware. This is the actual close of the gap that opened this milestone — confirming the pipeline, end to end, with knowledge that came from a person who actually knows it, not from this session inferring it. **This step cannot start until that knowledge is supplied** — flagged here rather than silently skipped or worked around.

## 4. Definition of done

- [x] Registry schema/parser implemented and round-trip tested (§3.1).
- [x] Merged action-list function implemented and unit-tested across every source-presence combination (§3.2).
- [ ] Study-builder table UI: add/remove/reorder rows, every field editable, produces a schema-valid `Study` (§3.3).
- [ ] Registry management UI: register a custom action with named enumerated values, no semantic-description field anywhere (§3.4).
- [ ] Run-and-watch: submits via `embarch-api`'s existing CLI, polls, renders live per-step outcomes (§3.5).
- [ ] One-click live discovery folds into the merged action list (§3.6).
- [ ] `cargo build --features study-ui`/`cargo test --features study-ui`/`cargo clippy --features study-ui --all-targets -- -D warnings` clean, alongside every other existing feature combination unaffected.
- [ ] Real-hardware validation: a real custom action, supplied by the user, registered and run successfully through the full pipeline (§3.8) — blocked on that input, not a code gap.
- [ ] Any real gap found folded back into `design.md` per `DOC-PROTOCOL.md` §5.

## 5. Open questions / risks carried into execution

- **No `init`-equivalent for `study-actions.toml` yet** — `embarch.toml` gets scaffolded by `embarch init`; this new file doesn't have an equivalent bootstrap step, so the UI creating it on first save (§3.1: "a missing file is an empty registry") is the only onboarding path for now. Revisit if that turns out to be confusing in practice.
- **Concurrent edits to the same `study-actions.toml`** (two engineers, or a human editing it by hand while the UI has it loaded) — single-engineer scope assumption carried over from the rest of the suite; no locking/merge logic planned. A real gap only if it's ever actually hit.
- **Whether shelling out to `embarch-api`'s CLI is fast enough for a snappy "watch it run" UI** — untested until §3.5 is real; a subprocess-per-poll is simple but not free. If polling latency turns out to matter, the fallback (an extracted shared client crate, decision 34's other named option) is still available without a redesign.
- **`GattOperation` reuse in `RegisteredAction` (§3.1) may not fit every real custom action shape** — e.g. a multi-field write where different fields need different enumerated sets is the assumed common case; a firmware whose custom actions don't fit this shape at all would need the schema extended, not redesigned, matching decision 33's own "generic at the trait boundary" precedent.

## 6. Changelog

- 2026-08-24 — **§3.1/§3.2 executed: the registry and the merged-action-list function, both `std`-only behind a new `study-ui` feature.** `RegisteredAction`/`ActionField`/`ActionFieldValue` (`src/registry.rs`) and `merge_actions`/`MergedAction` (`src/merged_actions.rs`), 13 new unit tests. One real correction to this doc's own §3.1 sketch, caught writing the code rather than after: a value's payload bytes are stored literally (`ActionFieldValue.bytes: Vec<u8>`), not as a numeric `value` this module would encode itself — encoding a number into bytes means assuming a width/endianness, exactly the kind of DUT-protocol fact this whole milestone exists to never guess at. `cargo build`/`test`/`clippy --all-targets -D warnings` clean with `--features study-ui`, and every other existing feature combination (`default`/`std`/`core-validation`/`ffi`/`gatt-extract`/`--all-features`) re-verified unaffected.
- 2026-08-24 — Initial draft, scoping this milestone's execution plan from `design.md` §3 decisions 34/35, resolving the implementation details those decisions deliberately left open (registry file location/format, Core-access mechanism, web framework).
