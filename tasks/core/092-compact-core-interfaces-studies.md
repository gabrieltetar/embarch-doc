# 092 — `embarch-core/interfaces/studies.md` is in reserve

**State:** open
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by the `/stream/{name}/arrivals` row
**Scope:** core
**Hardware:** none
**Owner:** no
**Compacts:** embarch-core/interfaces/studies.md
**Size debt due:** 2026-09-25
**In flux:** no

## What

The studies-route reference is **11,622 / 12,288 B (94.6%), 666 B left**. Out of
reserve when this closes, or the task says why not.

The row that crossed the floor is `GET /study/{id}/stream/{name}/arrivals` — one
tap's arrival sidecar, and the route that makes a console placeable on a shared
axis after the run. It is not the row to cut: it is the newest and the one a
reader is most likely to reach for.

The seam that is actually available is the **three `/stream/{name}*` rows**,
which between them carry ~5 KB and re-state a great deal of shared tap
resolution — the same `404` list three times, and the same `400`/`422` refusals
twice. A split by mission into `interfaces/streams.md` moves them verbatim and
leaves the run/status routes behind, which is the remedy DOC-BUDGET.md prefers
over squeezing.

## Why now

666 bytes is less than one route row. The next route added to this surface
cannot be documented without paying first, and a reference that refuses new
routes stops being a reference.

## Done when

- [ ] Out of reserve, or the task says why not.
- [ ] **Nothing about a refusal was dropped.** Each route's `400`/`404`/`422`
      cases survive the move, including which of them name the tap's real
      encoding — those are what a caller branches on.
- [ ] Every inbound link to a moved row still resolves (`check-links.py`,
      `check-decision-refs.py`).
- [ ] Byte numbers before and after.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
