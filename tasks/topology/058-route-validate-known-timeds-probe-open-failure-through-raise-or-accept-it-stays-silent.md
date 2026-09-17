# 058 — Route `validate_known_timed`'s probe-open failure through `raise`, or accept it stays silent

**State:** open
**Filed by:** leg 134, from `inbox/topology-route-probe-open-failure-through-raise.md`, written by
the `topology/056` worker while landing that unit. Filed verbatim except for the two corrections
noted below, both mine. I re-checked the `Hardware: verify-only` claim myself and it holds: the
topology-side change is reachable by a unit test, and the `embarch-core` half is explicitly deferred
to a paired task rather than needed to land this one.
**Source:** `tasks/topology/056` (the fourth of leg 133's census findings). That task fixed the two
in-repo claims that mismatched the code (`TopologyMismatch::live_hardware_id`'s doc comment, and
`validate.rs`'s module header) to describe current behavior accurately. It deliberately did **not**
change behavior — its own "Not yours" section reserved that decision for a follow-up, since the
consumer-visible half crosses into `embarch-core` and no bench was available to exercise either side.
**Scope:** topology
**Hardware:** verify-only — the topology-side code change itself needs no board (same shape as
`tasks/core/041`'s resolution: reachable by unit test, since the two paths differ only in whether
`probe_info.open()` `Ok`s or `Err`s). Confirming `embarch-core`'s `POST /validate` renders the
widened alert/error correctly is free the next time a probe is physically busy/permission-denied,
but nothing here needs a board to land.
**Owner:** no

## What

In `embarch-topology/src/hardware/validate.rs`, `validate_known_timed` only calls `raise` (which
constructs a `TopologyMismatch` and durably logs an `Alert`) for two of its failure points: the
probe missing from `Lister::list_all()` entirely, and a hardware-ID compare that fails. **The other
five** — `probe_info.open()`, `check_target_powered`, `.attach()`, `session.core(0)` and
`hardware_id::read`, all part of the same "open and read the board" sequence —
each return a bare `anyhow::Error` via `?`.

*(Correction, leg 134: the drop as written said "two of its five failure points" and then "the other
three points" before listing five. Two raise and five do not — seven in total. The `topology/056`
worker's own report and the corrected module comment it landed name the same five, so the list is
right and the two counts around it were not. Re-count them yourself before acting on the number.)* None of these is downcastable to `TopologyMismatch`, none
is durably logged to `alerts.jsonl`, and a caller like `embarch-core`'s `POST /validate` falls
through to its generic (non-mismatch) error arm for all of them.

The case most worth naming: **a probe that lists but won't open** — another process holding it, a
permission denial, a half-wedged J-Link. That's common in practice and is exactly where an operator
or an unattended supervisor most wants the structured "this needs a human" answer decision 12
describes, not a generic I/O error indistinguishable from any other failure in the suite.

## Why now

`embarch-topology` decision 20's own incident (a bench that "flashed, booted, ran, and timed out"
under a papered-over mismatch) is the standing reason this suite treats a mismatch as a safety
property, not a nicety. `tasks/core/041` already fixed the adjacent defect — Core was collapsing
"not attached" and "wrong hardware ID" under one lead — on the strength of the same reasoning. This
is the third case that incident didn't cover: not attached, wrong ID, and (unhandled) attached-but-
won't-open.

## Done when

- [ ] A decision on whether `validate_known_timed`'s open/power/attach/core-select/read failures
      should route through `raise` (widening what's alertable and what `TopologyMismatch` can
      report), or a documented reason the current silent behavior is correct as-is. If routing
      through `raise`, decide what `reason`/`live_hardware_id` should say for each of the five call
      sites — they are not interchangeable (an unpowered board is a different fact than a busy
      probe).
- [ ] If behavior changes: a topology decision recording why (this crate's `decisions/alerts.md`,
      alongside decision 12, or a new one — decision 12 itself is correct as written and needs no
      amendment).
- [ ] **Named but explicitly out of this task's reach:** whether `embarch-core`'s `POST /validate`
      (and `flash`/`reset`/`run_study`'s dev-bench gate, all downstream of the same `TopologyMismatch`
      downcast per `tasks/core/041`) handles the widened set of alertable failures correctly, and
      whether its `kind` classification (`"not_attached"` / `"mismatch"`, `embarch-core` decision 59)
      needs a third value for "couldn't open/attach/read, but the probe is physically there." That is
      `embarch-core`'s to verify, and belongs in a paired `embarch-core` task once the topology side
      lands, the same two-repo shape `core/041`'s own resolution used.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) in `embarch-topology`; `changelog.d/`
      fragment; `spec.md`/`decisions.md` updated if behavior or a decision changes.

## Not yours (for whoever picks this up)

Do not touch `embarch-core` from this task — same boundary `topology/056` respected. If the answer
is "route through raise," file the `embarch-core`-side verification as its own task rather than
reaching across.
