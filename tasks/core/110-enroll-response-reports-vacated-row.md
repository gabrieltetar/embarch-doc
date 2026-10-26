# 110 — Core's POST /probes/enroll reports the row a probe vacated

**State:** claimed by agent/core/110-enroll-response-reports-vacated-row, 2026-10-26 02:57
**Source:** embarch-topology task 063 (decision 42), landed as topology `6732ad6`
**Scope:** core
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 leg

Nothing in `embarch-core/` docs is in reserve. The topology side is landed on `embarch-topology`
`main` (`6732ad6`, decision 42 in `decisions/link-declares.md`); your worktree's parent links the
main checkouts of `embarch-topology`, `embarch-study-designer` and `embarch-smp`. Never edit
`embarch-topology` or `embarch-api`. The new fields must be additive and absent when empty: check
how `embarch-api`'s `embarch-core-client` reads the enroll response (`deny_unknown_fields` or a
shared topology `wire` type would turn an additive field into a break) and say what you found in your
report. If a client or UI half is wanted, write it as an inbox drop by absolute path to
`/home/gabriel/Github/embarch/embarch-doc/inbox/`, not an edit. Native Windows build is a debt the
owner runs; record it, do not attempt it. Never touch the live Core or any hardware.

## What

`embarch-topology` now offers `validate::enroll_reporting`, returning `(EnrolledBoard, enrollment::Upserted)` where `Upserted { displaced, vacated, vacated_kept }` (re-exported as `hardware::Upserted`). `POST /probes/enroll` (`embarch-core/src/api.rs:944-1008`) calls `enroll` and returns neither the row that lost the role to this probe (`displaced`) nor the role this probe vacated (`vacated`). Switch Core to `enroll_reporting` and carry both in the response (additive fields).

## Why now

Today only a `tracing::warn!` in the topology crate says a role moved. A caller (UI, api MCP) cannot tell the user that re-enrolling the dev-bench probe as `dut` vacated `dev-bench`.

## Done when

- [ ] The enroll response carries `displaced` and `vacated` (+ `vacated_kept`), absent when none; a test covers role->role.
- [ ] Core's decision/spec names the fields; changelog fragment.
