# embarch-study-designer decisions: Authoring surfaces

**Status:** active, 2026-09-02.

The UI, the registry, and where engineer knowledge enters the system.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6 — Symmetric human/agent access

Follows the suite-wide principle already established for Core/API (`embarch.md` §5: every hardware-facing capability is reachable both by an agent and directly by a human, converging on the same underlying modules). Concretely, study-running code means new MCP tools *and* CLI subcommands (§6) — not one without the other, matching `build`/`flash`'s existing pattern. Decision 26 exists because decision 17's CRC requirement would otherwise have broken the human half of this.

### 34 — A Study Designer UI: an interactive, table-based `Study` builder

**Implemented 2026-08-24** (milestone 11): `src/study_builder.rs` (table rows → `Study`) and `tools/study_designer_ui.rs` (the `axum` server, since retired — see below), live-smoke-tested against the real `reference-dut-fw` repo.

Motivated by a real gap Milestone 3's own closing session hit directly: a real `GattMonitorAll` run against the reference-dut DUT came back with an **empty `gatt_activity`** — nothing was captured because nothing in that `Study` ever *wrote* anything, and there was no way for whoever authored it to know what to write, since that is DUT-specific knowledge no generic discovery can produce. Closing that gap needed two things: a real authoring UI (this decision) and a place for that DUT-specific knowledge to live (decision 35).

**Shape:** the main surface is a table where each row is a `Step` — an `Action` from a dropdown, its parameters filled in, `timeout_ms`, `continue_on_fail`. Rows can be added, removed and reordered, and **sequencing is expressed purely by row order**, not a separate precondition field, matching how `Study.steps` already works (§4.1; no state passes between steps, per decision 32's self-contained-action stance).

**The action list a row can pick from is merged from three sources, not one:** this crate's built-in `Action` variants; live `GattDiscover` results, when a DUT happens to be connected; and `GattConfigExtractor`'s static output (decision 33) — the same dual-source cross-check decision 33 established, now feeding one UI instead of being two things a human diffs by hand.

**Scope: author, run, and watch — read-only outside the authoring table.** It can submit the `Study` it just built and poll each step's live result, because a human shouldn't need a second tool to try what they built. It does **not** build or flash anything — provisioning the DUT/dev-bench (`build_and_flash`/`build_and_flash_dev_bench`) stays a separate `embarch-api` step, done before the "run" button means anything.

**This crate's own `tools/study_designer_ui.rs` binary is retired** (2026-08-24, milestone 1 §4.9). `embarch-ui`'s Study Designer tab is the successor: the same merged action list, the same table model, the same registry, but calling `registry`/`merged_actions`/`study_builder` in-process rather than running a second local web server, and submitting via `embarch-core-client` over HTTP+Bearer rather than shelling out to `embarch-api`'s CLI — which is the "left to implementation" question this decision deliberately deferred, resolved by `embarch-ui` rather than here. `src/study_builder.rs`, `src/registry.rs` and `src/merged_actions.rs` are entirely unaffected; only the binary that wrapped them in a server is gone.

### 35 — A user-authored custom-action registry: names and enumerated parameter choices only, never a semantic description

This is the actual fix for what motivated decision 34. Closing Milestone 3, an attempt to figure out what a custom GATT write "does" by reading the DUT firmware's own source and asserting a conclusion from it **was flagged directly as destructive to the dev process** — reading code and inferring behavior from it isn't the same as knowing it, and presenting that inference as fact is worse than not answering at all. The fix isn't a smarter inference; it is removing inference from the loop entirely: this knowledge only ever comes from the engineer, explicit and unambiguous, through a registry the UI reads and writes.

**What the engineer provides — mechanical, not documentary:** for a detected characteristic they want to use, a freely-chosen `name` (shown in the dropdown), which characteristic it targets, its `operation` (read/write/subscribe/notify/indicate), and — for a write — its payload described as one or more named fields, each with a small enumerated set of engineer-supplied `{label, value}` pairs. Building a step against a registered action means clicking a name and clicking a value; nothing is typed as raw hex, and **nothing describes *why* a value does what it does — there is deliberately no "what this does" field at all**, since that would be this crate inventing a place to write down another guess.

A value's bytes are **the engineer's own literal bytes, never a numeric type this crate encodes itself** (which would require assuming a width and endianness nobody here is in a position to know). `ActionRegistry`/`RegisteredAction`/`ActionField`/`ActionFieldValue` in `src/registry.rs`, **implemented 2026-08-24** and confirmed round-tripping against the real `reference-dut-fw` repo; the correction that a value's bytes are the engineer's literal bytes, and why, is milestone 11 §3.1's own account.

**Persisted in the firmware repo's own `embarch/` folder** as `study-actions.toml`, sibling to `embarch.toml` — it travels with the firmware, is versioned in that repo's git history, and is shared across engineers the same way `embarch.toml` already is; not a catalog this tool owns separately, and not re-entered per `Study`.

**The durable principle, stated plainly since it generalizes past this one crate:** *no EmbArch component should ever present an inference about what a specific piece of hardware or firmware does — derived from reading its source, its comments, or any other heuristic — as established fact.* Where that knowledge is needed, the answer is a pipeline for the engineer who actually knows to supply it explicitly, built once, generically, for any project. This registry is that pipeline for "what does this GATT action do", not a one-off for `reference-dut-fw`. Decisions 41, 45, 52, 56 and 58 are each that rule applied somewhere else.

### 37 — A free-text payload path alongside the registry: `RowAction::Raw`

Decision 35's registry is the right home for a *named, reusable* action, but it was the only way to send a payload at all, which makes a one-off — an ad-hoc shell command, a value being tried once to see what happens — require editing `study-actions.toml` first. `RowAction::Raw { service_uuid, characteristic_uuid, operation, payload }` (§4.3c) takes a UUID pair typed directly and a payload supplied as literal bytes.

**This does not weaken decision 35.** That rule forbids two specific things: this crate inventing a *semantic description* of what an action does, and this crate *encoding a number into bytes* on an engineer's behalf. `Raw`'s payload is already bytes when it reaches this crate — parsed client-side by the same parser the registration form uses, from either UTF-8 text with explicit escapes or hex tokens — so nothing here interprets or encodes anything. The registry remains how an action gets *named and re-used*; this is how one gets *sent before it has a name*.

`Uuid::parse` arrives alongside it, accepting the hyphenated 128-bit form, 32 bare hex digits, or the 16-bit shorthand expanded against the Bluetooth SIG Base UUID. That expansion is a Core Spec fact — a 16-bit UUID *means* that 128-bit value by definition — not an inference about any particular DUT, so it doesn't cross decision 35's line either.

### 38 — A saved-study library at `<firmware-repo>/embarch/studies/*.json`

Until this, a `Study` authored in the UI existed only as long as the browser tab did; re-running one meant rebuilding the table by hand. Saved studies live beside `study-actions.toml`, same per-repo convention, so a study travels with the firmware it was written against and is versionable with it.

**The file *is* a `Study`** — `embarch-api run-study --study-file <path>` re-runs it directly, with no conversion step. The authoring rows ride along in one extra key, `_embarch_ui_rows`, which `Study`'s own deserializer ignores (no `deny_unknown_fields` anywhere in this crate). That single-file choice is what makes a saved study both re-runnable from the CLI *and* re-loadable into an editable table; a sidecar file would have made one of the two lossy or the pair separable. A `Study` JSON dropped into that directory by hand or by an agent is still listed and still runnable — it just has no rows to load back, and the UI says so rather than offering a Load that would silently produce an empty table.

This is also what makes decision 39's `StreamSource::Signal` and decision 40's reflash-is-a-run-parameter rules load-bearing: a saved study has to survive a rewired bench and has to not reflash a board every time someone re-reads its results.

---

