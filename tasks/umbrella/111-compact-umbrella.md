# 111 — compact `embarch-umbrella/open.md`

**State:** blocked — umbrella open.md in reserve; install subsystem still moving

**Unparks when:** the install-core follow-up units (self-elevation, service registration, setup calling it) have landed
**Scope:** umbrella
**Hardware:** none
**Owner:** no
**Compacts:** embarch-umbrella/open.md
**Size debt due:** 2026-12-09
**In flux:** yes
**Must not delete:** every hardware or owner debt line, with the command it names to run (the `install-core` one from `umbrella/110`, check 15's `binary_sha256`, check 17's stopped arm, the desk steps of decision 58).

## What

`open.md` is 4,634 of 5,120 B after `umbrella/110` added the `install-core` debt. Compact it under `DOC-COMPACTION.md`. Answered by the unit that just worked in it: the install subsystem is still moving (service registration, self-elevation, installing from staging and `setup` calling `install-core` are all next units), so each of those will rewrite its line.

## Done when

- [ ] `open.md` is out of reserve and every `Must not delete:` line survives.
