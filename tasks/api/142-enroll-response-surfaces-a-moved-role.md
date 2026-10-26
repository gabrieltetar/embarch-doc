# 142 — The client and the enroll result say when an enrol moved a role

**State:** claimed by agent/api/142-enroll-response-surfaces-a-moved-role, 2026-10-26 03:42
**Doc reserve (dispatch, 2026-10-26):** `embarch-api/decisions/client-crate.md` 11,581 / 12,288 B (707 B left), filed against `tasks/api/140` (open); nothing else in `embarch-api/` is in reserve. If your edit pushes any other file into reserve, file `tasks/api/<NNN>-compact-api.md` in the same commit.
**Source:** embarch-core task 110 (core decision 87), inbox drop `api-surface-enroll-vacated-row.md`, filed 2026-10-26
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core's `POST /probes/enroll` now returns optional `displaced` (EnrolledBoard), `vacated` (EnrolledBoard) and `vacated_kept` (bool), absent when empty (`embarch-core` `9b0d016`, decision 87 in `embarch-core/decisions/enrollment.md`). `embarch-core-client`'s `EnrollProbeResponse` mirror (`crates/embarch-core-client/src/client.rs`) drops them silently. Add them as optional fields and have the enroll CLI/MCP result say that a role moved (e.g. re-enrolling the dev-bench probe as `dut` vacated `dev-bench`). A UI follow-up (the UI re-serialises that mirror) can be filed after, as an inbox drop.

## Why now

A caller cannot otherwise tell the user a role moved; only a topology log line did.

## Done when

- [ ] The mirror carries the three fields and a test deserializes a body with and without them.
- [ ] The enroll result text names the vacated/displaced role.
- [ ] Gate green, docs per `DOC-PROTOCOL.md`, `changelog.d/` fragment.

## Supervisor note, filing

`embarch-core-client` is path-depended on by `embarch-ui` and `embarch-umbrella`, so the change must stay additive. `embarch-api/decisions/client-crate.md` is in reserve (11,581 / 12,288 B, filed against `tasks/api/140`); if this unit's decision belongs there, keep it short or put it in the topic file that already owns enrolment.
