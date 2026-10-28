# 097 — The Topology tab's bench box draws the raw board qualifier until the next poll

**State:** claimed by agent/ui/097-bench-box-label-on-first-draw, 2026-10-28 14:59
**Reserve (supervisor, 2026-10-28):** `embarch-ui/open.md` 935 B left, parked under `ui/088` (`blocked`, `In flux: yes`). If this unit adds to `open.md`, compact it in the same unit, carrying `ui/088`'s `Must not delete:` list; otherwise leave it.
**Source:** `ui/096`'s close note and its reviewer, 2026-10-28 leg. The worker found the bench box first
draws the raw west qualifier and takes its label only on the next snapshot poll, because
`loadRolePickers()` (`assets/app.js:6781`) does not redraw the diagram when `/api/topology/pickers`
answers; it fixed the drive check's timing and left the UI alone. The reviewer added that the two
comments it wrote (`tests/browser/drive_topology.py:431`, `:653`) cite "decision 45" for the label rule,
which is decision 45 of `topology-roles.md` (probe versus board-type bindings); the rule is the
unnumbered section "A dev-bench board type is shown by its label, never by its qualifier" in
`decisions/topology-boards.md`.
**Scope:** ui
**Hardware:** none — the stub Core and `drive_topology.py` reproduce it.
**Owner:** no

## What

When the pickers answer, the diagram redraws, so the bench box shows the board's label from the first
draw that has one and never the qualifier for a whole poll interval. The two comments cite the section
that holds the rule.

## Why now

`topology-boards.md` says the label is shown, never the qualifier; for up to one poll after every load
it is the qualifier. Found while fixing the check that waits for it, so the context is fresh.

## Done when

- [ ] `loadRolePickers()` (or its caller) redraws the diagram once the pickers arrive; the drive
      check's wait can go back to a short one and still pass.
- [ ] The two `drive_topology.py` comments cite `topology-boards.md`'s section, not decision 45.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
