# 024 — Compact embarch-topology/spec.md

**State:** open — unparked by leg 080, 2026-09-11: every task this park named is `done`
**Size debt due:** 2026-09-24
**Source:** `scripts/check-doc-size.py` — 89.4% of cap after `tasks/topology/011`'s edit
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/spec.md` was at 9151/10240 B when this task was filed.
`tasks/topology/025` added a new section (caller granularity contract,
decision 29) and paid its own compaction debt in the same commit per
`DOC-COMPACTION.md` §2 — the file is now 9195/10240 B (89.8%, just under the
90% floor) — but it is still inside reserve and this task stays open: any
further growth from `004`/`020` lands back over the floor with no slack
left. Compact it per `DOC-COMPACTION.md` §3/§7 — a pass over its own prose,
not a new section — down to comfortably below the 90% floor.

**Compacts:** `embarch-topology/spec.md`

**In flux:** no, as of 2026-09-11 — one file (`embarch-topology/spec.md`), and the flux is
spent. This field read `yes` on the grounds that `tasks/topology/011` had just added the
decision-28 sentence and that `tasks/topology/004` and `tasks/topology/020` were "open against
the same file's surface". **All four of those are now `done`** — `011`, `004` and `025` landed
2026-09-08 through 2026-09-10, `020` at leg 050 — and `topology/024` is the only task left in
this scope, so nothing is moving in `spec.md` for a compaction pass to race. Unparked by leg 080
after `topology/027`'s reviewer found this `State:` line still asserting `020` as live work three
days after it closed; the park's reason was stale, not wrong when written. The **Must not
delete** list below is unchanged and still binds — it is what a settled file still owes a
compactor.

**Must not delete:**
- The decision-28 sentence added to the "two things built from it" list
  (CLI mutation refusal / local-bootstrap).
- The process/call-site code block (`Core, mid-flash/reset/run_study: ...`).
- The "What a caller may assume across calls" section and its decision-29
  pointer (added by `tasks/topology/025`).
- Anything `open.md` currently points at by section name.

## Why now

`check-doc-size.py` names a file in reserve with no debt filed as a gate
failure (`protocol.md` §5 step 5); this records the debt rather than leaving
it unfiled.

## Done when

- [ ] `embarch-topology/spec.md` is below 90% of its cap.
- [ ] Nothing on the **Must not delete** list is gone or now reads as false.
- [ ] Gate green.
