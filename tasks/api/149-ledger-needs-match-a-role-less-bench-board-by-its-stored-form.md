# 149 — The test ledger's `needs` matches a role-less bench board by a form nobody confirmed

**State:** done — agent/api/149-ledger-role-less-board-needs, 2026-10-28
**Reserve (dispatch note, 2026-10-28):** no `embarch-api` file is in reserve (`check-doc-size.py --pressure`). If this unit pushes one past 90% of its cap, file `tasks/api/<NNN>-compact-api.md` in the same commit.
**Source:** `api/128`'s fold (supervisor log, 2026-10-28 16:43, "Least sure about"): "how a role-less bench board (topology decision 48) counts toward a test's `needs`; the worker assumed by role and by board name and could not confirm the stored form."
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api` decision 98's `tests.toml` lets a test name what it `needs` by role, board name or instrument name, and `ledger_pending` groups a test under each missing need using Core's topology (falling back to `bench.json`). A role-less bench board (`embarch-topology` decisions 41 and 48) is enrolled with no role; how it is identified in Core's topology response (name, probe serial, both) is defined by `embarch-topology`'s types, which this crate path-depends on. When this is done, the ledger's matching of a board need is checked against that stored form, read from `embarch-topology`'s source rather than assumed: a test needing a role-less board by the name the enrolment stores is runnable when that board is attached and grouped under it when it is not, with a unit test for each, and an instrument need is matched against the instruments table the same way. If the form makes "board name" ambiguous (two boards, one name), the ledger says so rather than picking one. Record what was confirmed in decision 98 in place.

## Why now

The ledger exists to say which tests the bench on the desk can run; a need that silently never matches leaves a test "never run" forever, and the worker that built it said it could not confirm this half.

## Done when

- [x] Board and instrument needs matched against the stored forms in `embarch-topology`'s types, with unit tests for attached and absent.
- [x] Decision 98 states the confirmed form in place.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment dropped.
