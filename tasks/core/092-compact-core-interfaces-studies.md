# 092 — `embarch-core/interfaces/studies.md` is in reserve

**State:** done — 2026-09-28 — the three `/stream/{name}*` sub-routes (`arrivals`,
`load`, `load/spans`) split verbatim into new `interfaces/streams.md` (3,969 B).
`studies.md` is now 9,076 B (was 12,101 B), well clear of the 12,288 B cap.
`interfaces.md`'s index gained a Streams row; a one-line pointer in `studies.md`
sends a reader to the new file. No `embarch-core` source comment cited these
rows by file, so the code repo has **zero commits** — checked with
`grep -rn` for `interfaces/studies` across `.rs` files, no hits. Native Windows
build: **not owed**, no source changes.
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

- [x] Out of reserve, or the task says why not. `studies.md` 12,101 B → 9,076 B.
- [x] **Nothing about a refusal was dropped.** All three moved rows' `400`/
      `404`/`422` text carried verbatim into `streams.md` — the shared
      tap-resolution `404`, `/load`'s `400`/`422`, and `/load/spans`'s "same
      `400`/`404`/`422` cases as `/load`" cross-reference, none rewritten.
- [x] Every inbound link to a moved row still resolves — `check-links.py` and
      `check-decision-refs.py` both green; no source comment or doc anywhere in
      either repo cited these rows by `interfaces/studies.md` line number.
- [x] Byte numbers before and after — see below.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/`
      fragment (`changelog.d/core-interfaces-streams-split.changed.md`).

## Bytes before/after

| File | Before | After |
|---|---|---|
| `embarch-core/interfaces/studies.md` | 12,101 B | 9,076 B |
| `embarch-core/interfaces/streams.md` | — (new) | 3,969 B |
| `embarch-core/interfaces.md` | 6,185 B | 6,401 B (Streams index row added) |
