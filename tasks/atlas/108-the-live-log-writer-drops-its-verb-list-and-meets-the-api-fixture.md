# 108 — The live-log writer drops its verb list and meets the api's fixture

**State:** open — `api/191`'s 19 cases landed in `embarch-api/tests/fixtures/live-log/` at `c254d15`, described in `embarch-doc/embarch-api/interfaces/live-log.md` "The shared fixture"
**Source:** EMB-319 — the atlas live-log writer keeps a verb list the api output already answers
**Issue:** EMB-319
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`src/embarch_atlas/livelog.py` keeps `UNGATED`, a list of `embarch-api` verbs
that reach no lease-gated route (line 29, read at line 78). The api's `--json`
output already says the same thing by leaving `core_calls` empty or absent, and
`note()`'s next test (`if not live: return`) decides it again. When this is
done, `UNGATED` is gone, the atlas still writes no line for a verb that reached
no gated route, and a test proves both.

And a test fails when the atlas's writer and `embarch-api`'s disagree:
`api/191` puts cases pinning the shared rules (the 4096-byte answer cap, the
schema, the board-resolution order, the path rule, the `<date>-<session>`
name) in `embarch-api/tests/fixtures/live-log/`, described in
`embarch-doc/embarch-api/interfaces/live-log.md`. A pytest reads them from the
sibling checkout (`../embarch-api/` beside the repo, as `test_public_guard`
finds `.atlas-local/`), runs each case through `livelog.py`, and compares the
fields the interface says both writers fill. Where `livelog.py` cannot take a
case's inputs without a live `embarch-api`, split out the pure part rather
than copying it into the test. Without the sibling the test skips and says
why; the fleet's gate links it, so there it runs.

## Why now

EMB-319, after `api/191`. Each rule `livelog.py` repeats is one a change to
`live_log.rs` would silently leave behind.

**Burndown leg: no new numbered decision.** Amend the atlas's own live-log
decision or `design.md` paragraph in place where it names `UNGATED`.

## Done when

- [ ] `UNGATED` is gone and a test shows a lease-free verb writes no line.
- [ ] A pytest runs `api/191`'s cases through `livelog.py` and fails on a
      difference in a shared field.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
