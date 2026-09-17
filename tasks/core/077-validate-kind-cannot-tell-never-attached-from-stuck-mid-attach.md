# 077 — `POST /validate`'s `kind` classifier can't tell "never attached" from "attached but stuck mid-open", and that's now a live gap, not a hypothetical one

**State:** open
**Filed by:** leg 136, 2026-09-17, from
`inbox/core-validate-kind-classifier-cant-tell-not-attached-from-stuck-mid-attach.md`. Filed
verbatim except for this header and the note below. I re-checked the `Hardware: none` claim myself
and it holds: this is a read of `src/api.rs`, `embarch-topology/src/hardware/validate.rs` and the
`decisions/` tree, plus a decision — no board, no probe, no live Core, exactly as its predecessor
`core/074` settled.

**Supervisor note — the premise this task rests on is now landed, not pending.** The drop was
written while `topology/058` was still in flight and says "once `topology/058` lands". It has:
code `b96f758` in `embarch-topology`, doc `c34532e` in `embarch-doc`, `embarch-topology` decision 34.
So read the five `reason` strings from `main`, not from a branch.
**Source:** written by the `topology/058` worker while landing that unit (`agent/topology/058-route-probe-open-failure-through-raise`). `tasks/topology/058` itself required this be filed as a paired `embarch-core` task rather than answered by reaching into that crate — this is that drop.
**Scope:** core
**Hardware:** none (my honest read) — this is a code-reading and (if a third `kind` value is chosen) response-shape question, answered from `src/api.rs`/`src/hardware.rs`/`src/study.rs`, the same way `tasks/core/074` (its immediate predecessor in this same pair) settled without a board.
**Owner:** no

## What

`embarch-core` decision 59 already documents (as amended by `core/074`, done 2026-09-17) that its
`kind: "not_attached" | "mismatch"` classifier on `POST /validate`'s error response — built from
`TopologyMismatch::live_hardware_id.is_none()` — cannot distinguish "the enrolled probe was never
attached" from "the enrolled probe was attached but got stuck opening/attaching/reading it," because
both cases produce `live_hardware_id: None`. `core/074` recorded that as an **accepted, previously
un-actionable gap**, explicitly deferred until `embarch-topology` decided whether to route the
mid-attach failures through `raise()` at all — because until it did, the gap was moot: those five
failures never reached `TopologyMismatch` in the first place, so there was nothing for `kind` to
misclassify.

**`embarch-topology` has now made that decision** (`topology/058`, decision 34, code commit on
`agent/topology/058-route-probe-open-failure-through-raise`): all five of `validate_known_timed`'s
mid-attach failure points (`probe_info.open()`, `check_target_powered`, `.attach()`,
`session.core(0)`, `hardware_id::read`) now route through `raise()`, each with a distinct `reason`
naming the failing step. So the gap `core/074` filed as "accepted because inactionable" is now live: a
probe that lists but won't open (another process holding it, permission denied, a half-wedged
J-Link — the case both units name as most worth naming) will, once `topology/058` lands, produce a
real `TopologyMismatch` that `POST /validate` downcasts successfully and reports as
`kind: "not_attached"` — the same `kind` a genuinely unplugged board gets, even though the two facts
call for different operator actions (check the USB connection vs. close whatever else has the probe
open). `live_hardware_id` stays `None` for all five new cases, same as the true not-attached case —
`embarch-topology` deliberately did not widen that field or add a new one to carry more structure,
reasoning that doing so is a shape change reaching every `TopologyMismatch` consumer and belongs to
the consumer that would actually use it, not assumed on its behalf.

Decide: does `POST /validate` (and `describe_topology_error`/`describe_gate_error`'s plain-text
`flash`/`reset`/dev-bench-gate paths, per `core/074`'s own item 2) need a third `kind`/lead-text value
for "attached, but couldn't complete the open/attach/read sequence," or is collapsing it into
`not_attached` an acceptable operator experience now that it is a real, reachable case rather than a
theoretical one? Either answer is legitimate — but it needs to be a decision made by reading the
current handler code and `topology/058`'s five new `reason` strings, not assumed from this drop's own
description.

## Why now

`core/074`'s own supervisor note 2 anticipated exactly this: *"If you conclude a third `kind` arm is
warranted, that is a wire change with consumers in `embarch-api`, `embarch-ui` and the user
guide — do not implement it; say so, and drop it in `inbox/`."* `core/074` correctly declined to
speculate ahead of `topology/058` landing. Now that it has, the premise `core/074` reasoned from
("this case doesn't currently reach `TopologyMismatch`, so there's nothing to reclassify") no longer
holds, and `topology/058`'s own "Not yours" section named this as the place to answer it — a paired
task, not a reach across from the topology side.

## Done when

- [ ] Re-derived from `embarch-topology/src/hardware/validate.rs` (the sibling checkout this crate's
      `Cargo.toml` path-dependency resolves to) what each of the five newly-`raise`-routed failures'
      `reason` text now says, and from `src/api.rs`'s `validate_handler`
      (`TopologyMismatch::downcast_ref` arm) exactly what `kind` and status it produces for each.
- [ ] A decision: add a third `kind` value (name it, and say what changes in `embarch-api`,
      `embarch-ui` and the user guide to consume it — do not implement the wire change in this task
      per `core/074`'s supervisor note 2, file it back to `inbox/` in full task format if warranted),
      or record why collapsing all five into `not_attached` is acceptable as a considered choice
      rather than an inherited accident.
- [ ] `describe_topology_error`/`describe_gate_error`'s plain-text `flash`/`reset`/dev-bench-gate
      paths (decision 59, `core/074` item 2) checked against the same question: do their lead-text
      strings now need to say more than "not attached" for these five cases, given they carry the
      distinction only in message text, never structurally?
- [ ] `decisions/surfaces.md` decision 59 amended (again) if the classifier's scope or behavior
      changes or if this task documents the gap as newly-live rather than newly-moot; `interfaces.md`
      / `interfaces/topology.md` updated to match, the same "one consistent account" bar `core/074`
      held itself to.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-core`; `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

- **Do not change `embarch-topology`.** `topology/058` already landed the behavior this task reads;
  re-reading its source is fine, editing it is not.
- **If a third `kind` value is warranted, do not implement it here.** It is a wire change reaching
  `embarch-api`, `embarch-ui` and the user guide — name it, and drop it back in `inbox/` in full task
  format, per `core/074`'s own supervisor note 2.
- **`embarch-core/decisions/auth.md` is in reserve** (filed under `tasks/core/046`, blocked) —
  do not write into it. Run `python3 scripts/check-doc-size.py --pressure` before and after; if this
  task's edits push another file into the reserve band, file the compaction task in the same commit.
