# 024 — Compact embarch-topology/spec.md

**State:** blocked — in flux, `tasks/topology/004` and `020` still moving in this file
**Size debt due:** 2026-09-24
**Source:** `scripts/check-doc-size.py` — 89.4% of cap after `tasks/topology/011`'s edit
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/spec.md` is at 9151/10240 B (1089 B left, inside reserve).
Compact it per `DOC-COMPACTION.md` §3/§7 — a pass over its own prose, not a
new section — down to comfortably below the 90% floor.

**Compacts:** `embarch-topology/spec.md`

**In flux:** yes. `tasks/topology/011` just added a sentence describing the
CLI's mutation-refusal behavior (decision 28), and `tasks/topology/004` and
`tasks/topology/020` are open against the same file's surface. A compaction
pass must not delete or blur the decision-28 sentence, the "Storage and
roles" section, or the process/call-site table just above it — check
`open.md` and `decisions.md` for anything else still moving in this crate
before cutting.

**Must not delete:**
- The decision-28 sentence added to the "two things built from it" list
  (CLI mutation refusal / local-bootstrap).
- The process/call-site code block (`Core, mid-flash/reset/run_study: ...`).
- Anything `open.md` currently points at by section name.

## Why now

`check-doc-size.py` names a file in reserve with no debt filed as a gate
failure (`protocol.md` §5 step 5); this records the debt rather than leaving
it unfiled.

## Done when

- [ ] `embarch-topology/spec.md` is below 90% of its cap.
- [ ] Nothing on the **Must not delete** list is gone or now reads as false.
- [ ] Gate green.
