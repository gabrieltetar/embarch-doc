# 020 — `hardware_id` is two different values for one board on two routes of Core's HTTP surface

**State:** open
**Source:** suite review pass 2026-09-06, dimension 5 (cross-surface consistency). Code-confirmed.
**Scope:** core
**Hardware:** none. A field rename plus its interface row; both values are already recorded in the docs.
**Owner:** no

## What

Two different facts share one field name on one API.

- **The probe-read ID.** `EnrolledBoard.hardware_id`
  (`embarch-topology/src/hardware/enrollment.rs:27`) is served as `hardware_id` by
  `/probes/enroll`, `/probes/enrolled` and `/validate` — and as **`probe_hardware_id`** by
  `/dev-bench/hello`, because `embarch-core/src/study.rs:685` does
  `let probe_hardware_id = enrolled.hardware_id.clone();`.
- **The self-reported ID.** `HelloAckInfo.hardware_id` (`embarch-core/src/study.rs:595-600`) is
  documented in place as *"What the bench says its own chip ID is"* — the `hwinfo_get_device_id`
  value, not the JTAG one — and is served as `hardware_id` by `/dev-bench/hello`.

**They are different strings for the same board, measured and written down.**
`embarch-topology/decisions/validation.md:19` records *"JTAG `6fcddc36cb781b71`, self-reported
`cb781b716fcddc36`, relation *match*"* — the halves swapped. And the same board answers
`"hardware_id": "6fcddc36cb781b71"` on `POST /validate`, quoted live in
`tasks/topology/009`.

So the probe-read ID has three spellings across the surface (`hardware_id`, `probe_hardware_id`,
and `live_hardware_id`/`recorded_hardware_id` in the validation report) while the **self-reported**
ID reuses the first. Both are documented as-is at `embarch-core/interfaces.md:31,36,45`.

Candidate direction: give the two sources two names on every route, so the JTAG-read ID has one
spelling everywhere and the self-reported one is visibly not it.

## Why now

A caller that reads `hardware_id` from `/dev-bench/hello` and compares it against `hardware_id`
from `/probes/enrolled` — the obvious thing to do, both being 16 hex digits under one name on one
API — gets a mismatch on a **correct** bench, because one is the probe's reading and the other is
the board's own, and their relation is chip-specific and, for every chip but this one,
undeclared. Nothing can catch it: both fields are honest about their own value, both are
`String`, and the only place the relation is stated is `link_identity`, which a caller comparing
the two by hand never touches.

**`tasks/api/036` is about to put both fields in front of every agent over MCP.** It names them
with their meanings in parentheses but scopes itself to exposing the route; a worker doing 036
should not have to invent the rename. If both are worked, this lands first.

## Done when

- [ ] The probe-read hardware ID has one spelling on every Core route that serves it.
- [ ] The bench's self-reported ID is not called `hardware_id` on any route that also serves the
      probe-read one.
- [ ] `embarch-core/interfaces.md` rows 31, 36 and 45 match the router.
- [ ] `status.d/core-*` fragment for `embarch-topology/decisions/validation.md`'s vocabulary if the
      rename reaches it.
- [ ] Gate green; `changelog.d/core-*` fragment.
