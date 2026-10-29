# 055 — Close the pre-October tasks that no longer describe real work

**State:** open — drained from `inbox/` and announced 2026-10-29 14:29:00 (`ts` `1793305740.224299`); the 30-minute window closes 14:59:00. A later leg reads the thread and runs it.
**Source:** owner's session, 2026-10-29 — cleanup pass; 17 non-owner tasks filed 2026-09-06 to 09-17 still open, blocked, bench or hw-gated
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Every task filed before 2026-10-01 that is not `done` and not `Owner:
required` gets a verdict, from code, docs and git history only:

- **already fixed** — the change it asks for is on `main`; cite the commit;
- **superseded** — a later task, decision or reversal replaced it; cite it;
- **source gone** — the `Source:` doc line or the code it points at no longer
  exists; cite the commit that removed it;
- **keep** — still describes real, unbuilt work, or telling would need hardware.

**Obsolete tasks are closed by the fleet, settled by the owner 2026-10-29.** A
closure sets `**State:** done — closed as obsolete: <verdict>, <evidence>` and
`git rm`s the file in the same commit, and the leg digest lists every one so the
owner can reopen it. `keep` changes nothing.

**Out of scope:** the four tasks the owner parked on 2026-09-07 (`api/029`,
`outpost/002`, `study-designer/007`, `ui/007`) — "unparked by him saying so, and
by nothing else". A verdict on them goes in the digest as a recommendation only.

The 2026-10-29 candidates, besides those four: `api/059`, `api/108`,
`dev-bench/003`, `004`, `010`, `016`, `017`, `035`, `outpost/018`, `suite/030`,
`032`, `037`, `ui/059`. Re-derive the list from `queue-status.py` at claim time.
The owner's pass the same day landed some 40 fleet-tooling fixes, which is the
likeliest reason one of these is now moot.

## Why now

The owner's cleanup pass, 2026-10-29. Six weeks of suite change have landed on
top of these; a task whose premise is already false costs a worker a claim to
find out.

## Done when

- [ ] Every candidate has a verdict line with evidence in the leg digest.
- [ ] Every non-`keep` candidate outside the parked four is closed and
      retired, with no inbound doc link left dangling (`check-links.py` green).
- [ ] Any follow-up a closed task carried that has no other home is re-homed
      to the owning `open.md` or an `inbox/` drop first.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
