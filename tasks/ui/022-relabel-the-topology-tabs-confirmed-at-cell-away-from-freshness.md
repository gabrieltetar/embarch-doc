# 022 — Relabel the Topology tab's `confirmed_at_utc_ms` cell away from any freshness wording

**State:** done — leg 067, 2026-09-10, branch `agent/ui/022-confirmed-at-label`.
**Filed from `inbox/` by leg 066, 2026-09-10**, in the same fold as `umbrella/036`, and for the
same reason as its sibling `tasks/umbrella/045`: `core/027` decided that the fix for "enrolment
time misread as freshness" is a **label**, and these two tasks are the only things that carry that
fix to a screen. Decision 54 is otherwise a decision whose entire user-visible effect is owed by
someone else.

**This is the one of the pair with something concrete to change**, since the Topology tab does
render `EnrolledBoardResponse` today. The wording decision 54 settles on is **"Enrolled"** (or
"Enrolled at"), never "Validated" or "Last validated"; a UI wanting to say something is stale has
to call `POST /validate` and show *that* response's `validated_at_utc_ms`, which takes the hardware
lock and is a different feature.
**Source:** `tasks/core/027`, `embarch-core` decision 54 (`decisions/surfaces.md`)
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The Topology tab renders `EnrolledBoardResponse` (`src/snapshot.rs`), never a
`ValidateResponse` — confirmed against the code as it stands, and correctly:
`EnrolledBoardResponse` carries `confirmed_at_utc_ms` alone, and leg 044's
reviewer already confirmed it was correctly left without `validated_at_utc_ms`,
because its upstream body (`GET /probes/enrolled`, `GET /status`) never carries
that field.

Check whatever label the Topology tab currently puts next to
`confirmed_at_utc_ms`, if any (searched and found no occurrence of
`confirmed_at_utc_ms` in `src/` at the time this was filed, so it may not be
rendered at all yet). Whenever it is rendered, it must not be labeled in a way
that implies a live check — "Validated", "Last validated", "Verified", or
similar reads as an answer to "how stale is this identity check?", which this
field cannot answer: it is enrolment time, unmoving until someone re-enrolls.
`embarch-core` decision 54 declined to persist a real last-validation instant
next to it (the store change belongs to `embarch-topology`, and every
already-enrolled board would have no honest value to backfill), so the field
this cell has to work with is staying exactly what it is today.

The honest word both this cell and `embarch-umbrella`'s `doctor` can use is
**"Enrolled"** (or "Enrolled at"). If the Topology tab wants to show freshness
for real, it needs a `POST /validate` call and that response's own
`validated_at_utc_ms` — a live, hardware-touching call, not a passive read of
the enrolled-board snapshot.

## Why now

Residue of a four-task chain (`embarch-topology/tasks/topology/009` →
`embarch-core` decision 50 → `tasks/umbrella/041`, `tasks/ui/020`, both closed
unsatisfiable). `tasks/core/027` closed the design question by choosing
"label, don't add" rather than persisting a second timestamp, and its decision
requires this follow-up be filed rather than assumed.

## Done when

- [x] Whatever the Topology tab currently renders next to
      `confirmed_at_utc_ms` (if anything) is checked against this wording, and
      relabeled if it currently implies freshness.
      Found it rendered — not in `src/`, but in `assets/app.js` /
      `assets/index.html`: the Dashboard's and Topology/Enroll tab's shared
      "Enrolled boards" table has a `<th>Confirmed</th>` column header over
      `formatTimestamp(b.confirmed_at_utc_ms)`. Relabeled to `Enrolled` in
      both `assets/index.html` table headers (the Dashboard copy and the
      Topology/Enroll copy).
- [x] If it renders nothing today, fold this reasoning into `snapshot.rs`'s
      own doc comments or `embarch-ui`'s spec, so the first person who adds
      such a display finds decision 54's wording rather than guessing.
      Not applicable (it does render) — added the guard anyway as a doc
      comment on `Snapshot::enrolled` in `src/snapshot.rs`, and a matching
      comment above `enrolledTableRows` in `assets/app.js`, citing
      `embarch-core` decision 54.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
