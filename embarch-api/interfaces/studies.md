# embarch-api: study tools and subcommands

**Status:** active, 2026-09-04.

Submitting a study, reading its result, and watching it live. The rest of the surface: [tools.md](tools.md). Why: [../decisions/studies.md](../decisions/studies.md), [../decisions/surface.md](../decisions/surface.md). Current truth: [../spec.md](../spec.md).

MCP tools are `snake_case`, CLI subcommands `kebab-case`, over one implementation ([tools.md](tools.md)). `P` is the project-selection set defined there.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `run_study` | `study` (MCP) / `--study-file <path>` (CLI), `reflash?`, `allow_version_mismatch?`, `project?`, `P` | Recomputes and overwrites **all three seals**, then Core `POST /study`, returning `{ study_id }` at once alongside what it reflashed. `reflash` is `none` (default) / `dev-bench` / `dut` / `both`, building the tree **as it stands** — never `git checkout`. `project` is required only by `dut`/`both`: a *study* is not project-shaped, rebuilding a DUT's firmware is. `allow_version_mismatch` proceeds past an unsatisfied requirement, the override **recorded**, never silently honoured |
| `study_status` | `study_id` | Core `GET /study/{id}` verbatim. **CLI only:** `--follow` watches the study live instead (below); without it, one snapshot, unchanged |
| `study_watch` (MCP) | `study_id`, `wait_secs?`, `max_events?`, `include_samples?` | Subscribes to Core `GET /study/{id}/events` and returns every step, status change and (optionally) sample batch pushed in the window, in order. Bounded because an MCP call is request/response: `wait_secs` defaults to 60, caps at 600 — `complete: true` means terminal, otherwise call again. `include_samples` defaults to **false**, counting `SampleBatch`/`GattTranscript` per tap instead of listing them; the bulk data's exit is `study_stream_data` |
| `study_stream_data` | `study_id`, `name`, `raw?` | One declared tap's capture, by the name the study gave it. Rendered file where the encoding has one; `raw` serves the bytes. **Nothing here inspects content to decide** — an encoding is declared, never sniffed. A non-UTF-8 capture returns a clear error saying that is *expected* for a raw tap, pointing at `--out`, not a decode failure reading like the capture broke |
| `list_study_streams` | `study_id` | Per declared tap: `name`, `bytes_written`, and **`truncated`** — the reason this exists, since the aliases below structurally cannot report it. `bytes_written: 0` means a tap was declared and captured nothing, a different fact from one never declared |
| `study_power_data` · `study_waveform_data` · `study_gatt_data` | `study_id` | **Aliases kept for one release**, each serving whichever tap answers that alias. Names, params and returned bytes are pinned; their *descriptions* say what each resolves, that it is an alias, and that truncation lives in `list_study_streams` |

CLI data subcommands take `[--out <path>]`. **`--out` is how a binary capture gets out intact** — a raw tap's bytes are not text, and the no-`--out` path writes them to stdout untouched. `list-study-streams` marks a short capture on its own row, not a column an eye slides past.

## Watching a study live

`study-status --follow` (CLI) and `study_watch` (MCP) are **an addition to polling, never a replacement** — `study_status` with no flag is byte-for-byte what it was. Both consume the same client ([decisions](../decisions/core-link.md) 48, 49); they differ only in that a CLI user can be handed a stream and an MCP caller cannot.

- **`event: lagged` is a reported fact, not an error.** Core emits it deliberately when a subscriber falls behind, rather than skipping messages silently. The CLI prints a `[lagged]` line inline and repeats the count in its summary; the MCP result carries a `lagged: {events, note}` object. Both say the same: the events are missing **from this live feed only**, the study is unaffected, and `study_status`/`study_steps` hold the complete record. Neither fails the call.
- **A dropped or refused stream falls back to polling** `GET /study/{id}` and says so on its own line (`transport` in the MCP result, `[polling]` on the CLI) with the reason. No reconnect: Core keeps no replay, so reconnecting would resume with a silent hole. The only genuine failure is neither mechanism answering.
- **`events_omitted` (this crate's `max_events` cap) and `lagged` (Core's) are different facts**, reported as two. A caller told only that events are missing cannot tell which happened, and the remedies differ.
- **CLI `--follow --json` is NDJSON**, not one object: one compact record per line, ending with a `{"type": "summary", ...}` line. The only `--json` here shaped that way, and it has to be — a stream cannot be one object. `--follow-timeout <secs>` stops watching early and **exits 1**; a study that *fails* still exits 0, because reporting a failed study is a successful report.
