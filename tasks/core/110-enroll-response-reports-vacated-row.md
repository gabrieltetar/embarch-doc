# 110 — Core's POST /probes/enroll reports the row a probe vacated

**State:** claimed by agent/core/110-enroll-response-reports-vacated-row, 2026-10-26 03:24
**Source:** embarch-topology task 063 (decision 42), landed as topology `6732ad6`
**Scope:** core
**Hardware:** none
**Owner:** no

## Dispatch note, second dispatch (2026-10-26 03:24) — read this one first

Reclaimed after its first worker stopped on the topology gap in `## Blocked` below, which
`topology/065` closed: `embarch-topology` `7c1ef59` makes `hardware::enroll_reporting` public
beside `hardware::enroll`, and gates the `Upserted` re-export on `hardware` (Core builds with that
feature, so it sees both). The `## Blocked` section is history; its "Ready to apply" paragraph is
the plan, and its wire check stands. That worker's scratch patch is not in git, so rebuild the
change from that paragraph. Check that decision 87 is still the next free number in
`embarch-core/decisions/` before using it. Everything in the note below still holds.

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

## Blocked

**2026-10-26 — the topology half is not callable from Core.** `embarch_topology::hardware::enroll_reporting` does not exist: `validate::enroll_reporting` is `pub` inside the private `mod validate`, and `hardware::enroll` (the wrapper Core calls) still discards the report; only `Upserted` is re-exported. Swapping the call in `src/api.rs` fails `E0425`. Not Core's to fix; drop filed as `inbox/topology-reexport-enroll-reporting.md` (a one-wrapper topology task). No Core code or docs were committed (the gate would be red).

**Ready to apply once it lands** (all built and reviewed on this branch, then reverted): in `src/api.rs` add `displaced: Option<EnrolledBoard>`, `vacated: Option<EnrolledBoard>`, `vacated_kept: Option<bool>` to `EnrollProbeResponse`, each `#[serde(skip_serializing_if = "Option::is_none")]` (`vacated_kept` = `Some(up.vacated_kept)` only when `vacated` is `Some`); move the response construction into a pure `enroll_response(board, upserted)` fn so a unit test can cover role->role without a probe; call `enroll_reporting`. Docs: new decision 87 in `decisions/enrollment.md` (+ index row), the `POST /probes/enroll` row in `interfaces/topology.md`, changelog fragment.

**Wire check (done):** `embarch-api`'s `EnrollProbeResponse` mirror (`crates/embarch-core-client/src/client.rs:275`) has no `deny_unknown_fields`, and none exists on any enroll-response type in api or ui, so additive fields are not a break. They are silently dropped there (the UI re-serialises that mirror), so surfacing them is a later client/UI half.
