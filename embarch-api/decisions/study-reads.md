# embarch-api decisions: What a study reads back

**Status:** active, 2026-09-11.

Seals, the MCP schema that read as "anything", and the manifest/stream tools that replaced three
fixed-channel aliases.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The other half
of this split, reflashing: [study-reflash.md](study-reflash.md).

### 27, 28 — Validate capacities and fill the seals before the HTTP call
Capacity validation lived only in Core, but **this crate is the one holding the file** for a `--study-file` submission — so a JSON exceeding a bound failed with a raw deserialize error here, before Core's friendlier field-naming message ever ran. And the seals are computed and overwritten here, so a hand-authored study **no longer needs a human to compute a CRC by hand**, closing the gap between the integrity check and the suite's symmetric-human/agent principle. Recomputation is idempotent, so a caller that already computed a correct value is unaffected. Core's own checks are unchanged and stay the authoritative, un-bypassable gate for any other caller.

A refusal names every bound it exceeds — field, count, limit — a string in **bytes**, since that is what `heapless::String<N>` bounds, and says these are dev-bench's compile-time buffer sizes, so nobody hunts a per-submission knob. The caller used to get `sequence exceeds its bound at line 1 column 8785`.

**Diagnostic, not a second gate**, which is what makes the rest safe: it runs only *after* `serde` refused the value, so a bound stated wrongly there can worsen a message and never reject a study `serde` would accept. Hence a deliberately partial table — `name`, `requires`, the four lists and their entry names — over a second, drifting copy of every limit in `embarch-study-designer`; anything else falls back to `serde`'s error, which is what every case got before.

### 31, 33 — `run_study`'s schema declares an object, and the handler tolerates a stringified one
*(One decision under two numbers, both resolving here — [../decisions.md](../decisions.md) has what went wrong.)*

`serde_json::Value`'s own generated JSON Schema is the literal `true` — "matches anything", with **no `type` key at all** for a client to key off. At least one real client, this suite's own daily driver, read that as "no declared shape" and sent the entire study **JSON-encoded as a string** rather than an inline object, failing deserialization with a confusing "expected struct, got a string".

**A failure mode the CLI path structurally cannot hit**, since `--study-file` parses the file directly with no schema involved — which is why MCP coverage cannot be implied by CLI coverage here. **Fixed two ways:** the schema is overridden to declare an object, for clients that read the type; and the handler unwraps a string by parsing it as JSON first, for those that do not.

### 39 — The manifest rides the build, and one parameterised stream tool replaces three
**The manifest is a build output, so this repo is the only place that can see it.** A DUT firmware repo built with the outpost module emits it next to its artifact; Core needs it to decode a trace and can never produce it. So the flash carries it — no new user-facing step and nothing to remember, **because the failure mode of forgetting is silent mislabelling** and the only reliable fix is for the manifest to travel with the build that produced it. Absent, it is simply not sent; that is the normal case, not an error.

**Derived from the firmware path rather than added as a parameter, and that follows from the reasoning above.** A parameter is a thing a caller can forget, and there are a dozen flash call sites across the two front-ends and the reflash path — every one a place to forget it. A rule applied inside the client cannot be. It also means nothing needs to know which board it is talking to: a dev-bench build leaves no manifest beside its artifact, so none is sent.

**This inherits the artifact-transfer gap in a second place and does not fix it**, named here rather than discovered later; [../open.md](../open.md) is where it is tracked.

`study_stream_data` replaces the three fixed per-channel tools, mirroring Core's collapse of three routes into one parameterised one. **The three stayed as aliases for one release** rather than breaking an agent's working invocation mid-flight. `list_study_streams` names what a study actually captured, since an agent that must *guess* a tap name to read one has been handed a worse tool than it had.

> **Retired 2026-09-11 (`tasks/suite/015`).** `study_power_data`, `study_waveform_data` and
> `study_gatt_data` are gone, with `get_study_power_data`/`get_study_waveform_data`/`get_study_gatt_data`
> on `embarch-core-client` and the `study-power-data`/`study-waveform-data`/`study-gatt-data` CLI
> subcommands. **The grant above could not expire on its own**: `v0.1.0` is still the suite's only
> release, so "one release" had no closing edge and nothing tracked it. What forced the call is the
> second bullet below — the aliases are the suite's only study-read path that *structurally cannot
> report a truncated capture*, so every extra day they stood was a day an agent could be handed a
> short capture that read as complete. One caller existed anywhere (`embarch-ui`'s GATT download);
> it was repointed at `study_streams` + `get_study_stream` in the same change.

Two rules the implementation settled:

- **`truncated` is what the listing is *for*.** It is set both by a retention rotation deleting a segment and by a close reporting a non-zero drop count — two different losses a reader cares about identically. A listing that dropped the flag would hand back a capture that reads complete and is not, which is worse than no listing.
- **The aliases' descriptions were updated, not frozen.** The don't-move-ground-under-a-live-client posture protects a *working invocation* — same name, same params, same bytes. **It does not protect stale prose**, and one alias's text still described an `Action` retired several schema versions earlier. Leaving a description that is simply false is the mislabelling class this whole area keeps closing. *(Moot since the retirement above; kept because the rule it states outlives the tools it was stated about.)*
