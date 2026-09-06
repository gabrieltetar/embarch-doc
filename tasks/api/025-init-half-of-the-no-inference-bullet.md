# 025 — `embarch-api/open.md`'s first bullet is half-answered: the `init` clause shipped, the compare-against-hardware clause did not

**State:** open
**Source:** `inbox/api-init-half-of-the-no-inference-bullet.md`, dropped by `tasks/umbrella/022` 2026-09-06, which built the `init` half in another sub-project and so could not edit this file (`../../embarch-fleet/protocol.md` §3).
**Scope:** api
**Hardware:** none for the doc edit. The surviving clause is itself hardware-gated; recording that it survives is not.
**Owner:** no

## What

`embarch-api/open.md`'s first bullet names one defect from the consumer side and
two candidate fixes. **One of the two now exists and the bullet does not say so.**

Built 2026-09-06 in `embarch-umbrella` (its decision 41, in
`embarch-umbrella/decisions/projects.md`): the clause "`init` refusing to *write*
an inferred board unconfirmed — cheap, and enough." `embarch init` now writes the
board it read out of `build_info.yml` as `CHANGE-ME`, quotes the displaced value
in a comment above `build_command` and on stdout together with how old that build
is, and where a repo holds more than one recorded `build_info.yml` it names every
candidate with the board each recorded and derives no build command at all.

**Not built, and the clause that survives:** anything that compares a config's
declared board or chip against what is actually attached — the `validate`/`status`
half. Nothing in the suite reads hardware and tells you the config disagrees with
it. `init` now only declines to assert, which is not the same as detecting.

Rewrite the bullet so it carries the surviving half and its evidence and drops the
half that shipped. **Do not delete the bring-up incident it records** — that is
the evidence for the remaining half too, and it is the only place in the suite
where a day lost to this is written down.

## Why now

As written the bullet reads as entirely unaddressed, so the next sweep over
`embarch-api/open.md` will re-file work that is done and under-weight the work
that is not. It is also the source `tasks/umbrella/022` was written from, so
leaving it unchanged means the same task can be generated twice.

## Done when

- [ ] `embarch-api/open.md`'s first bullet states the `init` half as **built,
      dated 2026-09-06, and pointing at `embarch-umbrella` decision 41** — by
      decision number, which is how `DOC-CONVENTIONS.md` says a cross-sub-project
      reference resolves. Verify the pointer resolves before you write it; the
      decision moved into `decisions/projects.md` and a sibling split moved
      decisions 10 and 12 out of that file the same day.
- [ ] The `validate`/`status`-compare-against-hardware half survives as the open
      question, with the bring-up incident kept as its evidence.
- [ ] `changelog.d/` fragment if the answer changes what the doc claims is
      unbuilt. Gate green (`../../embarch-fleet/protocol.md` §10).

## Doc-size reserve for `api` at dispatch time

`embarch-api/open.md` is **4,521 B against a 5,120 B cap, 87 B below its reserve
line of 4,608 B.** This unit writes that exact file. **Plan to come out net
smaller or level** — the bullet loses a shipped clause, so that should be the
natural direction. If you leave it in reserve, file
`tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md` —
**`tasks/api/`, not `tasks/doc/`**, which `check-ownership.py` refuses to you.

Nothing in `embarch-api/` is in reserve today, but five files are one paragraph
from it: `decisions/zephyr.md` 11,056 (3 B of headroom), `interfaces/config.md`
11,008, `decisions/build.md` 10,934, `decisions/surface.md` 10,928,
`decisions/core-link.md` 10,879, against a reserve line of 11,059. This unit
should not need any of them.
