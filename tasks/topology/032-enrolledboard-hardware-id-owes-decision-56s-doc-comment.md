# 032 — `embarch-topology`'s `EnrolledBoard::hardware_id` owes `embarch-core` decision 56's promised doc comment

**State:** open
**Source:** `embarch-core/tasks/core/044`, found while paying decision 56's own debt.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-core` decision 56 (`decisions/handshake.md`) promised a doc comment on `hardware_id`
saying it is the probe-read value, on every response type serving it. Two of the three types it
named live in `embarch-core` and now carry that comment. The third, `EnrolledBoardResponse`, does
not exist there: `GET /probes/enrolled` serves `embarch_topology::hardware::EnrolledBoard` directly
(`embarch-core/src/api.rs:737`). That struct's `hardware_id` field
(`embarch-topology/src/hardware/enrollment.rs:27`) has no field-level doc comment of its own — only
a struct-level comment (lines 18-21) that mentions it in passing.

## Why now

Decision 56 traded away a rename on the condition that the probe-read-versus-self-reported
distinction be legible at the struct, not only on the wire, for every route that serves it. Two of
three routes are paid; this is the third, and it cannot be paid from `embarch-core` since the type
belongs here.

## Done when

- [ ] `EnrolledBoard::hardware_id` carries a doc comment saying it is the probe-read (JTAG) value,
      not the bench's self-reported one, citing `embarch-core` decision 56.
- [ ] Gate green.
- [ ] `changelog.d/` fragment.
