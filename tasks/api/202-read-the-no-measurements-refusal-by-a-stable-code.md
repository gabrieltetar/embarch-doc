# 202 — Read Core's no-measurements refusal by a stable code, not its wording

**State:** claimed by agent/api/202-read-the-no-measurements-refusal-by-a-stable-code, 2026-11-25 13:46
**Source:** EMB-553 — Core's measurements route still refuses a host study that now has measurements (the `embarch-api` half; `core/164` is Core's)
**Issue:** EMB-553
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`GET /study/{id}/measurements` answers `422` with a message ending "or is a host
study", and `embarch-api` pins that text to explain the refusal to an agent
(`tests/core_client_http.rs`, the `no-measurements` row). `core/164` changes the
wording, because a host study that declares a `parse` now has a
`measurements.json` (core decision 131), and adds a stable `code` to the `422`
body. This half makes the api independent of the wording first, so the two can
land in either order:

- The refusal is recognised by a `code` field of `"no_measurements"` in Core's
  JSON body when present, and by the `422` status alone otherwise (an older
  Core); never by matching the message text.
- The agent-facing explanation (the `read_measurements` tool's description and
  its error, `src/tools.rs`) stops saying a host study cannot have
  measurements: it says the study declared none, did not complete, or is a host
  study with no `parse` step.
- The client test pins the status and the code, not the sentence.

## Where to look

- `src/tools.rs` — the measurements tool's description and refusal handling
- `crates/embarch-core-client/src/client.rs` — how the `422` reaches the caller
  (additive only: the crate is shared with `embarch-ui` and `embarch-umbrella`)
- `tests/core_client_http.rs` — the `no-measurements` row
- `embarch-doc/embarch-core/decisions/` 131 (host parse) for what changed

## Where the doc goes

The tool's row in `interfaces/` and the decision that named Core's refusals by
name, amended in place if it has room; `check-doc-size.py --pressure` lists
lease#90, test-plans#134, ledger#98, bench-exchange#89 and failure-reporting#67
over or near their limits, so do not grow those. `embarch-api/spec.md` is in
reserve (`tasks/api/201`, blocked, `In flux: yes`): do not write it in this unit.

## Done when

- [ ] A `422` with `code: "no_measurements"` and any message is explained as
      no-measurements.
- [ ] A `422` with no `code` (an older Core) is still explained as
      no-measurements.
- [ ] No test or code path matches Core's message text.
- [ ] The tool's text no longer says a host study has no measurements.
- [ ] Gate green, the client crate included.
