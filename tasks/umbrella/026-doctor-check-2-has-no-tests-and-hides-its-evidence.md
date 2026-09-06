# Give `doctor` check 2 tests, and make its Fail detail name the evidence it inferred the class from

**State:** open
**Source:** `embarch-umbrella/open.md` — "`saved.host` is sticky, and `doctor` check 2 still reads it … check 17's fix line was fixed off it, **check 2 was not**"
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`src/doctor.rs:383-410` — `check_service` has four fix arms and **no test in the 121-test module
calls it**. `src/doctor.rs:2766` feeds it `config.core.host` *or* a sticky `saved.host`, so an old
`--host` makes it print "Core runs on another machine. On that machine: `embarch-core install`" on a
`wsl-host` bench, and its whole detail is the string `"not reachable"`.

Pin the four arms with tests. Make the Fail detail state *why* it concluded that class — "inferred
`remote` from a saved `--host` of `<x>`, recorded by an earlier `setup`" — so an operator sees the
input before following a remedy on another machine.

**The verdict does not change and nothing clears `saved.host`.** `open.md` records that the clearing
half was withheld deliberately, because it changes behaviour on real machines on a guess. Naming the
evidence is the half that costs nothing.

## Why now

`open.md` names this exactly and says the fix was withheld for the reason above. Check 17's fix line
was already corrected off the same defect; check 2 was left.

## Done when

- [ ] Tests cover Pass and the Remote / WslHost / Local / no-binary fix arms.
- [ ] A test pins that a sticky `saved.host` with no `config.core.host` produces a detail naming
      that host as the reason.
- [ ] No verdict or fix-command changes; `saved.host` handling is untouched.
- [ ] The `open.md` bullet is updated **without growing the file** — it is near its cap and
      `tasks/umbrella/009` is the parked compaction.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
