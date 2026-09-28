# 092 — `embarch-core/interfaces/studies.md` is in reserve

**State:** claimed by agent/core/092-compact-core-interfaces-studies, 2026-09-28 16:31
**Dispatch note (supervisor, 2026-09-28):** **the numbers below are stale, and worse.** The file is
now **12,101 / 12,288 B, 187 B left**, overdue since 2026-09-25 — `core/094` (landed this afternoon,
doc `fe7c52c9`) added a 72-byte pointer to the new `decisions/outpost-preflight.md` that decision 74
moved into; keep that pointer and bare `(decision 74)` on line 13 resolving. Re-derive every
number and re-check `git log` first. The split the task names (`/stream/{name}*` rows into
`interfaces/streams.md`, verbatim) is still the preferred move — no `interfaces/streams.md` exists
yet, so check the name against `interfaces.md`'s index and add its row there. Also in reserve in
this sub-project and **not yours**: `decisions/surfaces.md` (709 B left, `091`, blocked),
`decisions/auth.md` (932 B, `046`, blocked), `decisions/streams.md` (1,194 B, `093`, blocked) —
push none of them further in. A citation **outside `core`** that a moved row breaks you do not
edit: drop an inbox file by absolute path (`/home/gabriel/Github/embarch/embarch-doc/inbox/`) with
the exact fix and say so in your report; the supervisor repoints it at landing. **Native Windows
build**: not owed if no `embarch-core` source changes; say so either way.
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
