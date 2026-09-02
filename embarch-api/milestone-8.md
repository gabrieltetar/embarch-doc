# embarch-api: milestone 8 — Dev Bench Self-Test

**Status:** done, 2026-08-20 (draft 2026-08-18). Every DoD item done. Execution plan for [embarch-roadmap.md](../embarch-roadmap.md)'s Milestone 2 ("Dev Bench Self-Test" — filed on disk as `milestone-8`). Companion to [embarch-core/milestone-8.md](../embarch-core/milestone-8.md) (Core's `study.rs`) and [embarch-dev-bench/milestone-8.md](../embarch-dev-bench/milestone-8.md) (the firmware and self-test fixture this milestone drives). See [embarch-study-designer/design.md](../embarch-study-designer/design.md) §6 for the durable, already-locked-in tool/subcommand surface this doc implements for the first time.

## 1. Goal, restated for embarch-api

The roadmap originally scoped Milestone 2 as Core+Dev-Bench only, with no `embarch-api` involvement. That scope was expanded during this milestone's design-questions pass (2026-08-18): rather than validating `study.rs` with a raw HTTP call, this milestone builds the `run_study`/`study_status` MCP+CLI surface `embarch-study-designer/design.md` §6 already named and locked the shape of, ahead of any implementation — the same "recorded ahead of code" posture that section itself uses. This is the first real code behind either tool.

**Scope decision carried in from the same pass, confirmed 2026-08-18:** `study_power_data`/`study_waveform_data` are built alongside `run_study`/`study_status` in this milestone too, for symmetry with `embarch-core/milestone-8.md`'s decision to implement Core's full four-endpoint `/study*` surface now rather than deferring the two data-export rows to Milestone 4.

## 2. Scope for this milestone

- **New tools/subcommands only:** `run_study`, `study_status`, `study_power_data`, `study_waveform_data` — no changes to `build`/`flash`/`build_and_flash`/`reset`/`serial_log`/`list_projects`, all already proven in Milestone 1.
- **No `project` param** on any of these, per `embarch-study-designer/design.md` §6's own design: a study isn't tied to a configured project, it targets whatever DUT/bench is connected through Core's one dev-bench serial link.
- **CLI shape:** `--study-file <path>` for `run_study` (a `Study`'s nesting makes per-field flags impractical, per §6's own rationale); `study_id` (positional or flag, matching the existing `study_status`-shape convention) for the other three; `--out <path>` (falling back to stdout) for the two CSV-returning calls.
- **No blocking "run and wait" convenience wrapper** — deliberately deferred per §6's own text; the self-test validation in §3.6 below uses the two-call poll loop as designed.
- **Out of scope:** anything to do with `embarch-dev-bench` firmware or `embarch-core`'s serial link internals — this doc only adds the client-facing layer over endpoints the companion docs implement.

## 3. Steps

### 3.1 Add `core_client.rs` methods for the four new endpoints

`post_study(Study) -> { study_id }`, `get_study_status(study_id) -> StudyStatus`, `get_study_power_data(study_id) -> Bytes`, `get_study_waveform_data(study_id) -> Bytes` — plain `reqwest` wrappers mirroring the existing five-endpoint pattern (`design.md` §10), including surfacing Core's `{code, message, cause}` error body (`embarch-core/design.md` §3 decision 12) rather than a generic HTTP error.

### 3.2 Add `run_study`

MCP tool (`study: Study`, JSON) and CLI subcommand (`--study-file <path>`, loading and parsing the same JSON shape) — calls §3.1's `post_study` and returns `{ study_id }` immediately. A `400` from Core (failed pre-flight validation or `steps_crc` check) surfaces as an immediate error with no `study_id`, distinct from a later `study_status` `"failed"`.

### 3.3 Add `study_status`

MCP tool and CLI subcommand taking `study_id` — calls §3.1's `get_study_status` and returns the status/`current_step`/`total_steps`/`result`/`reason` shape verbatim.

### 3.4 Add `study_power_data` / `study_waveform_data`

MCP tools and CLI subcommands taking `study_id` — return raw CSV bytes as MCP tool content, or write to stdout / a `--out <path>` file for the CLI, matching `serial_log`'s existing output-handling convention.

### 3.5 Confirm the self-test fixture loads and validates

Using `embarch-dev-bench/milestone-8.md` §2's `self_test_study.json` — parse it through `run_study`'s JSON deserialization locally (no Core call yet) to catch a schema mismatch before it's ever sent over the wire.

### 3.6 Run the self-test study end to end, via CLI

`embarch-api run-study --study-file self_test_study.json` against the real Core from `embarch-core/milestone-8.md`, talking to the real dev-bench firmware from `embarch-dev-bench/milestone-8.md`; poll `embarch-api study-status <study_id>` to `"completed"`. This is the actual cross-repo Definition of Done the roadmap names this milestone for.

### 3.7 Confirm `study_power_data`/`study_waveform_data` both answer cleanly with no data

Since the self-test study is `BleAdvertise`-only, both calls are expected to surface Core's `404` ("no power/waveform data captured") as a clean, expected CLI/MCP error — not a crash or a hang — confirming the full surface is wired correctly even though nothing exercises its actual data path until Milestone 4.

### 3.8 Repeat §3.6 via MCP, not just CLI

Mirroring Milestone 1's pattern of validating both front-ends independently (`embarch-api/milestone-7.md` §3.9) — an MCP client (e.g. Claude Code) calling `run_study`/`study_status` against the same real hardware, confirming the MCP and CLI paths converge on identical `core_client.rs` behavior rather than only ever being tested through one of them.

## 4. Definition of done

**Status (2026-08-19/20): every DoD item done.** §3.1–3.6 were already done (all 4 tools/subcommands implemented, fixture round-trips, the self-test study completing end to end via the CLI). §3.7 and §3.8 closed this pass: `study_power_data`/`study_waveform_data` both cleanly report "no data" (confirmed via MCP), and the same self-test run was repeated successfully via a hand-rolled MCP client — which found and fixed a real MCP-specific bug the CLI path structurally can't hit (`design.md` decision 31): `run_study`'s schema didn't declare `study` as an object, so at least one real client sent it as a JSON-encoded string instead, failing deserialization. The same investigation reproduced last pass's flagged stack-overflow risk for real in a debug build, and confirmed a `--release` build doesn't hit it (`embarch-study-designer/design.md` §7). Decision 27's friendlier capacity-error message remains genuinely unimplemented — unrelated to this milestone, not addressed here.

- [x] `run_study`, `study_status`, `study_power_data`, `study_waveform_data` all implemented as both MCP tools and CLI subcommands (§3.1–3.4).
- [x] The self-test fixture (`embarch-dev-bench/milestone-8.md` §2) round-trips through `run_study`'s deserialization cleanly (§3.5).
- [x] The self-test study runs to `"completed"` end to end via the CLI, against real Core + real dev-bench hardware (§3.6).
- [x] `study_power_data`/`study_waveform_data` both cleanly report "no data" for this study, with no crash/hang (§3.7) — confirmed via MCP: both calls return `isError: true` with a clear "no power/waveform data captured" message.
- [x] The same end-to-end run repeated successfully via MCP (§3.8) — via a hand-rolled MCP stdio client against a freshly-built release binary (this session's own already-connected MCP server predates the schema fix below, so it couldn't itself be used); found and fixed the real schema/string-fallback bug, decision 31.
- [x] `embarch-study-designer/design.md` §6's table updated from "not yet implemented" to real, matching what actually shipped; any surface deviation found during implementation folded back per `DOC-PROTOCOL.md` §5.

## 5. Open questions / risks carried into execution

- **CLI flag naming for `study_id`** (positional vs. `--study-id`) isn't locked by `embarch-study-designer/design.md` §6 — pick whichever matches this repo's existing convention for a single required identifier arg (check `flash`'s `--project` precedent) rather than inventing a new pattern.
- This milestone is the first real test of `embarch-study-designer` actually being consumed as a Cargo dependency by `embarch-api` for the `Study` JSON type — the roadmap's own **Next** bucket lists "`embarch-core`/`embarch-api` actually depending on `embarch-study-designer`" as still-open future work; this doc assumes that dependency gets wired up as part of §3.1's implementation, not separately scheduled.
