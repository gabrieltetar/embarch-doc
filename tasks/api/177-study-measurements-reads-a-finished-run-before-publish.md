# 177 — `study_measurements` reads a finished run's `measurements.json` before publish

**State:** done — study_measurements tool and CLI subcommand ship with named Core refusals; pinned guide updated; drift guard red by construction
**Source:** Fleet Ready issue, found while writing the HIL guide's Study section
**Issue:** EMB-246
**Scope:** api
**Hardware:** none
**Owner:** no

## What

An agent writing a Study's prose has to read `measurements.json` before it
publishes, and `embarch-api` has nothing that returns it then: `study_status`,
`list_study_streams` and `study_stream_data` cover the run and its captures, and
the file is served only inside a publish. `core/139` adds the Core route that
returns a finished run's own `measurements.json` as Core wrote it; read the
route, its refusals and their statuses from
`embarch-doc/embarch-core/interfaces/measurements.md` as that task left it.

When this is done, a `study_measurements` MCP tool and an
`embarch-api study-measurements <study_id>` subcommand return the file as Core
wrote it, and pass Core's refusals through by name rather than as a generic
failure. `core/139` landed `GET /study/{study_id}/measurements` with four: 404
(no such run), 409 (still running), 422 (no `measurements.json`) and 410 (the
run's files are gone).

## Why now

The HIL guide's Study step 4 publishes a throwaway first revision for want of
this, so every real Study's zip carries an `-r2` for that reason alone.

## Constraints

- **Return the file unchanged.** No summary, no reshaping: the guide tells the
  reader to cite each entry's `value`, `unit`, `by`, `u_source` and
  `declared_by` as written.
- Put the Core call where the other study reads are (`crates/embarch-core-client`
  if that is where `study_status`'s lives). That is a shared crate: say so in
  your report, and keep the change to that one call.
- **The guide.** Change Study step 4's item 2 in the pinned copy,
  `embarch-api/guide/hil-guide.md`, to name `study_measurements` and
  `study-measurements` in place of the publish-once-and-unzip route, and change
  nothing else in the file. You may not write `embarch-doc/suite/hil-guide.md`:
  drop a `status.d/` fragment targeting it that says "copy `embarch-api`'s
  `guide/hil-guide.md` over it", and the supervisor folds it so the two match.
- **The drift guard is red in your tree by construction.** Run `cargo test` with
  `EMBARCH_DOC_DIR=<your embarch-doc worktree>`, so
  `the_pinned_copy_matches_the_suite_guide_where_one_is_reachable` reads the
  suite guide at your branch's base rather than the owner's checkout. After your
  guide edit that one test fails, because you cannot write the suite copy. Report
  it as the one expected red, with its message; every other test must be green.
  `tests/ble_gatt_rate_fixture.rs` also reads the guide: it must stay green.

## Where

- `src/tools.rs` (the study tools), `src/main.rs` and `src/cli.rs` (subcommands).
- `crates/embarch-core-client` (Core calls).
- `guide/hil-guide.md`, Study, "4. Read the losses, then the measurements".

## Dispatch note

No `embarch-api` doc file is in size reserve. Per-decision caps close to their
limit in this scope: `ledger` #98 (15 B), `bench-exchange` #89 (122 B),
`failure-reporting` #67 (192 B). If the tool needs a decision, file a new one
rather than growing any of those.

Also, while you are in `embarch-core-client`: `api/176` split the funnel into
`dispatch` (a wrapper) and `dispatch_with(.., bearer)`, and decision 55's prose
still says `dispatch` applies the token. Correct that sentence in place, and
name `dispatch_with` in decision 129 if it fits in one clause. No new decision.

## Done when

- [x] One MCP tool and one CLI subcommand return a finished run's
      `measurements.json` before any publish, unchanged.
- [x] Core's four refusals reach the caller by name; a test covers the file
      and each refusal without a live Core.
- [x] The pinned guide's Study step 4 names the tool instead of the
      first-revision workaround; `status.d/` fragment for `suite/hil-guide.md`.
- [x] Gate green (`../../embarch-fleet/gate.md`), bar the drift guard above.
- [x] `spec.md`/`decisions.md`/`interfaces/` updated where they list the study
      tools, `changelog.d/` fragment dropped.

## Notes

- Shipped: MCP `study_measurements`, CLI `study-measurements <study_id> [--out]`; `CoreClient::get_study_measurements` and `MeasurementsRefusal` (names `no-such-run`, `still-running`, `no-measurements`, `files-gone`) in `crates/embarch-core-client/src/client.rs` only. Decisions 55 and 129 amended in place.
- Drift guard `the_pinned_copy_matches_the_suite_guide_where_one_is_reachable` is the one expected red until the supervisor folds `status.d/api-177-hil-guide-copy.md`.
- No new decision was needed; the refusal type's design lives in `interfaces/studies.md`. Verified against a mock Core only; **hardware-verification debt: none** (a live Core's route is core/139's to prove).
