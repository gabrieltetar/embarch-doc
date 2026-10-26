# 110 — Core's POST /probes/enroll reports the row a probe vacated

**State:** open
**Source:** embarch-topology task 063 (decision 42), landed as topology `6732ad6`
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-topology` now offers `validate::enroll_reporting`, returning `(EnrolledBoard, enrollment::Upserted)` where `Upserted { displaced, vacated, vacated_kept }` (re-exported as `hardware::Upserted`). `POST /probes/enroll` (`embarch-core/src/api.rs:944-1008`) calls `enroll` and returns neither the row that lost the role to this probe (`displaced`) nor the role this probe vacated (`vacated`). Switch Core to `enroll_reporting` and carry both in the response (additive fields).

## Why now

Today only a `tracing::warn!` in the topology crate says a role moved. A caller (UI, api MCP) cannot tell the user that re-enrolling the dev-bench probe as `dut` vacated `dev-bench`.

## Done when

- [ ] The enroll response carries `displaced` and `vacated` (+ `vacated_kept`), absent when none; a test covers role->role.
- [ ] Core's decision/spec names the fields; changelog fragment.
