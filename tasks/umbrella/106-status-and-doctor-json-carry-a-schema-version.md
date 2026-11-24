# 106 — `status --json` and `doctor --json` carry a schema version

**State:** claimed by agent/umbrella/106-status-and-doctor-json-carry-a-schema-version, 2026-11-24 08:50
**Source:** suite review audit, 2026-11-23: the umbrella spec calls its two `--json` outputs a stable machine-readable contract, and neither is versioned
**Issue:** EMB-299
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-api` decision 24 (`embarch-doc/embarch-api/decisions/surface.md`) puts
`schema_version` on every `--json` object, from a hand-bumped constant in the
crate whose shape it versions. The umbrella's two do not:
`embarch-umbrella/src/main.rs` (`status_json`) emits
`{reachable, base_url, ..., attempts}` with no version and no `success` key, and
`src/doctor.rs` (`render_json`) emits `{success, checks}`.
`embarch-doc/embarch-umbrella/spec.md` calls the output a stable
machine-readable contract.

When this is done both objects carry `schema_version` from one umbrella-owned
constant (decision 24's reasoning: the counter belongs to the crate whose shape
it versions; do not import the api's), `status --json` also carries `success`,
and a test pins each object's top-level keys and the version.

Docs, in `embarch-doc/embarch-umbrella/`: `spec.md` (and `interfaces/` if it
describes either output) says both carry `schema_version` and when it is
bumped. If an existing umbrella decision already governs the shape of these
outputs (`decisions/schema-skew.md` is the first place to look), amend it in
place.

## Why now

A consumer of a contract with no version cannot tell a shape change from a bug.
EMB-299.

**Burndown leg: no new numbered decision.** If the change seems to need one,
stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-umbrella` file is in reserve.
Decisions near their per-decision limit: prune-policy#26 19 B, deploy#32 29 B,
mirrors#20 32 B, probe-vendors#49 140 B, sticky-host#48 186 B, budgets#44
200 B. Do not grow those.

## Done when

- [ ] `embarch status --json` and `embarch doctor --json` each carry
      `schema_version`; `status --json` carries `success`.
- [ ] A test pins both shapes, and fails if a key is dropped or the version
      changes without the constant.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md` updated; `changelog.d/` fragment dropped.
