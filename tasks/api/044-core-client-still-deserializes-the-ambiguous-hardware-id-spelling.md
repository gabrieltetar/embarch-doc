# 044 — `embarch-core-client` still deserializes the ambiguous `hardware_id` spelling on three routes

**State:** done — leg 077, 2026-09-10, supervisor-executed. Window from leg 076 at ts
`1789097485.649139` elapsed (38m) with no objection in-thread; not restarted.
Original state line follows.
**Was:** open — announced to #embarch-fleet by leg 076 at ts `1789097485.649139`; the `ops.md` §4
30-minute window opened then. Cross-repo (`embarch-core` + `embarch-api`), so supervisor-executed
despite the `api` scope. Do not restart the window: if this leg dies first, the next leg reads that
`ts` with `fleet-read.py --thread` and completes the remaining time.
**Source:** worker on `agent/core/020-hardware-id-two-spellings`, 2026-09-07, closing `tasks/core/020`; filed from `inbox/` by the supervisor, leg 037
**Scope:** api
**Hardware:** none
**Owner:** no

## Supervisor's note on filing it, leg 037

**This is not a one-worker task as written, and a worker that claims it will get stuck.** Its own
"Done when" asks for a rollout shape spanning `embarch-core` (which serves the field) and
`embarch-api` (which deserializes it), and §5 gives a worker exactly one repo. Two shapes work:
either a supervisor executes it as a cross-repo unit, or it is split into a `core` half that serves
both spellings for one release and an `api` half that moves to the new one, with the compatibility
window written down before either is dispatched.

**What I verified while landing `core/020`, so nobody re-derives it:**
`embarch-api/crates/embarch-core-client/src/client.rs`'s `HelloAckResponse` (line ~621)
deserializes only `schema_version`, `compatible` and `firmware_version` — so the rename that
already landed broke nothing. The three structs named below are a different matter and the drop's
reading of them is the one to trust until someone re-checks it.

## What

`tasks/core/020` found that Core's HTTP surface serves the probe/JTAG-read hardware
ID and the bench's self-reported one under names that collide (`hardware_id` on
both) or nearly collide (`probe_hardware_id` vs. `hardware_id`). It fixed the safe
half: `GET /dev-bench/hello`'s self-reported field is now `self_reported_hardware_id`
(Core decision 47) — safe because no client parsed that route's `hardware_id`/
`probe_hardware_id`/`link_identity` fields at all before this change.

**It deliberately did not rename `/probes/enroll`, `/probes/enrolled` or
`POST /validate`'s `hardware_id` field**, because `embarch-api/crates/
embarch-core-client/src/client.rs` deserializes all three with `hardware_id:
String` — required, no `#[serde(default)]` — in `EnrollProbeResponse` (line ~207),
`ValidateResponse` (line ~225), and `EnrolledBoardResponse` (line ~298). Renaming
Core's wire field there breaks every existing caller (the CLI, the MCP tools,
`embarch-ui`) at runtime, the first time one of those routes is called — not a
compile error, since these are freestanding structs, not shared with Core.

## Why now

`tasks/api/036` is about to put both `hardware_id`-named concepts in front of
every agent over MCP and would otherwise reinvent this exact naming question.
Whoever picks up the full rename needs to either open a compatibility window
(Core serves both `hardware_id` and a new name for one release) or land a single
coordinated commit touching both `embarch-core` and `embarch-api` together — a
cross-repo call this worker's single-repo scope could not make on its own
(`embarch-core/decisions/handshake.md` decision 47 has the full argument).

## Done when

- [x] Someone with authority over both `embarch-core` and `embarch-api` (or two
      coordinated units) decides the rollout shape (compat window vs. one
      coordinated commit) and files it. — **Neither: the rename is cancelled.**
      `embarch-core` decision 55, `decisions/handshake.md`.
- [x] `embarch-core-client`'s `hardware_id` fields on `EnrollProbeResponse`,
      `ValidateResponse`, `EnrolledBoardResponse` are updated to match whatever
      Core ends up serving. — They already matched; what they lacked was saying
      *which* ID they carry. Each now has a doc comment naming the concept and
      citing decision 55. No wire change in either repo.
- [x] `embarch-core/interfaces/topology.md`'s note pointing at decision 47 is
      either resolved or superseded by the new decision. — Rewritten to point at
      55 and state the default rather than the deferral.

## Resolution — leg 077, 2026-09-10

**The collision this task inherited was already gone, and that is what settled it.**
`tasks/core/020` fixed the dangerous half: `hardware_id` used to mean the self-reported
ID on `GET /dev-bench/hello` and the probe-read one on the three probe routes — one
spelling, two concepts, four fields apart in one body. Renaming the hello field to
`self_reported_hardware_id` ended that. What survived is one *concept* under two
spellings, which no single response can make a reader get wrong.

Weighed against that: renaming `hardware_id` on `/probes/enroll`, `/probes/enrolled`
and `POST /validate` is not a compile error anywhere — `embarch-core-client`'s structs
are freestanding — so it fails at runtime, on the first call, in the CLI, every MCP
tool and `embarch-ui` at once. A compatibility window buys that back only by serving
two live names for one field. Both prices are higher than the inconsistency they buy.

**Least certain:** that `probe_hardware_id` on one route and `hardware_id` on three
will not re-confuse someone reading the two routes side by side. The decision's answer
is that a prefix earns its keep only where it disambiguates against a neighbour; that
is a judgement, not a proof, and it is written down so it can be reversed with one.
