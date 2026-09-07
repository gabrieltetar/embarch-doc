# 020 — `hardware_id` is two different values for one board on two routes of Core's HTTP surface

**State:** claimed by agent/core/020-hardware-id-two-spellings, 2026-09-07 15:20
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

**Confirmed live in a single response body** [supervisor, leg 030, 2026-09-07, `tasks/umbrella/034`'s
bench run]: one authenticated `GET /dev-bench/hello` returned
`{"schema_version":15,"compatible":true,"firmware_version":"49958d34","hardware_id":"cb781b716fcddc36","link_identity":"match","probe_hardware_id":"6fcddc36cb781b71"}`,
and `POST /validate` for the same role in the same sitting returned
`"hardware_id":"6fcddc36cb781b71"`. So the two spellings sit **four fields apart in one JSON
object**, differing only by a swap of their two 4-byte halves — which is what makes a caller's
`==` look like a near-miss rather than a category error.

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

## Doc-size reserve for `core` — supervisor, leg 036, 2026-09-07

**Two `core` docs are in reserve and one of them is the file this task must edit.**

- `embarch-core/interfaces.md` — **14,527 / 15,360 B, 833 B left.** In reserve.
- `embarch-core/open.md` — **4,478 / 5,120 B, 642 B left.** In reserve.

Both are filed under `tasks/core/022-compact-core.md`, which is **`blocked` with `In flux: yes`**
(it waits on `core/021` and `api/032`). Per `.claude/leg.md`, a blocked compaction task parks the
*pass*, not the *reserve* — so **compacting `interfaces.md` is part of this unit**, because you are
the actor making the flux and you are the only one who can shorten what you are rewriting without
writing a clean statement of something about to be wrong.

What that means concretely:

- Prefer a **split** over a squeeze — `core/022`'s own note says so, and `DOC-COMPACTION.md` §2
  makes a split the default remedy, because a verbatim move restates nothing and costs no argument.
- Carry `core/022`'s **`Must not delete:`** list verbatim or faithfully restated: the
  `GET /serial-log` caller-side-ceiling paragraph (a cross-repo measurement, not a description);
  the `404`-is-often-expected / `502`-vs-`503` vocabulary paragraph in Conventions; and
  `GET /study/{id}`'s `current_step` "consequence, not an invariant" sentence.
- **Do not close `tasks/core/022`.** Close only its `interfaces.md` item, by editing its
  `**Compacts:**` line and saying in the task file what you did and what is left. `open.md` and its
  `core/021`/`api/032` gate stay parked.
- If your edit leaves any other `core` file in reserve with nothing filed against it, file
  `tasks/core/<next NNN>-compact-core.md` in the same commit (`tasks/README.md` has the shape).
