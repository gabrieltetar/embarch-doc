# 093 — A study refuses a stream tap no step subscribes to

**State:** open
**Source:** decision 55 (`decisions/payload-meaning.md`) — a GATT notify tap must actually produce records; today only the UI's authoring path refuses a tap no step subscribes to
**Issue:** EMB-308
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-ui/src/study_designer.rs` refuses a `StreamSource::GattNotify` tap
whose characteristic no step subscribes to (`any_step_subscribes`: an
unfiltered `GattMonitorAll`/`GattMonitorStart`, or a selective
`GattMonitorSelected`/`GattMonitorSelectedStart` naming that service and
characteristic). Nothing else does, so a study submitted through `run_study`
or Core's `/studies` with such a tap runs, captures nothing, and passes.

When this is done the crate owns the check, beside its siblings
`Study::validate_wait_budgets` and `Study::validate_monitor_windows`: a
`Study` method that walks `streams` against `steps` and refuses the first
GATT notify tap no step subscribes to, with its **own** error type naming the
tap and the characteristic, so a consumer can match it and keep its own
wording. Additive, like its siblings: nothing calls it implicitly, no existing
public enum gains a variant, and no existing signature changes, so every
consumer still compiles unchanged against this branch. Run `cargo check` in
`embarch-core`, `embarch-ui` and `embarch-api` against it and say so.

The consumers adopt it in their own units, parked behind this one:
`tasks/core/152` (Core's submit path, which `run_study` reaches) and
`tasks/ui/119` (the tab catches the typed error).

## Why now

The audit (EMB-308) found the refusal only in the UI, which is the privileged
path `embarch.md` §5 warns about. The sibling checks already live here.

**Burndown leg: no new numbered decision.** Decision 55 describes this exact
case; amend it in place with one sentence saying the crate computes the check,
or say it in `interfaces.md` alone. If the work genuinely needs a new decision,
stop and say so in this file.

**Doc-size note (dispatch):** no study-designer file is in reserve. Decisions
near their per-decision cap: streams#39 (64 B), versioning#12 (67 B),
seals#17 (72 B), protocols#58, authoring#73, declares#40, protocol-exec#60,
ble#44. Leave them alone.

## Done when

- [ ] A `Study` method refuses an unsubscribed GATT notify tap with a typed
      error naming the tap; a tap subscribed by an unfiltered monitor, by a
      selective one naming it, and a non-GATT tap all pass. Tests for each.
- [ ] `cargo check` green in Core, the UI and the api against this branch.
- [ ] Clippy and tests green under the crate's feature sets (`../../embarch-fleet/gate.md`).
- [ ] `interfaces.md` (or the topic file it points to) lists the check beside
      its siblings; `changelog.d/` fragment dropped.
