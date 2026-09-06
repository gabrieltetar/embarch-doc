# 025 — Two `embarch-api/open.md` bullets have been answered in another repo and neither says so

**State:** done, agent/api/025-open-md-two-answered-bullets, 2026-09-06
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

## And a second bullet, folded in here 2026-09-06 rather than filed separately

`inbox/api-open-md-versions-is-read-now.md`, dropped by `agent/umbrella/023-locate-embarch-api`,
reports that **`open.md`'s "Nothing reads `versions` yet" bullet is false twice
over.** It is a second bullet in the same file answered by the same other repo,
so it belongs in this unit rather than in a fourth `api` task on `open.md`.

The bullet reads: *"Nothing reads `versions` yet (decisions/surface.md 52):
`doctor` check 11 compares `embarch`'s **own** host schema copy, so a mixed
install stays invisible. Another repo's fix."* Both halves are closed:

- **`doctor` check 11 has shelled out to `embarch-api --json versions` since
  `embarch-umbrella` decisions 33/36.** It no longer compares `embarch`'s own
  constant as the primary reading; that constant survives only as a mixed-install
  warn.
- **`embarch-umbrella` decision 42, 2026-09-06, made check 1 actually locate the
  binary** — via the agent CLI's MCP registration and `setup`'s install directory
  as well as `PATH` — which was the reason the shell-out had never had a target on
  the reference machine.

Measured on that machine 2026-09-06: both `embarch-api` binaries present answer
`host_type_schema_version: 17`, matching the Core the same bench serves.

**What may survive is narrower, and check before you write it:** check 11 has
still never run end-to-end inside a `doctor` against a live Core. That debt is
already recorded in `embarch-umbrella/open.md` and is **that** sub-project's, not
this one's — so duplicating it here is the wrong answer. Deleting the bullet
outright is likely right; argue it either way.

## Why now

As written the bullets read as entirely unaddressed, so the next sweep over
`embarch-api/open.md` will re-file work that is done and under-weight the work
that is not. It is also the source `tasks/umbrella/022` was written from, so
leaving it unchanged means the same task can be generated twice.

## Done when

- [x] `embarch-api/open.md`'s first bullet states the `init` half as **built,
      dated 2026-09-06, and pointing at `embarch-umbrella` decision 41** — by
      decision number, which is how `DOC-CONVENTIONS.md` says a cross-sub-project
      reference resolves. Verify the pointer resolves before you write it; the
      decision moved into `decisions/projects.md` and a sibling split moved
      decisions 10 and 12 out of that file the same day.
- [x] The `validate`/`status`-compare-against-hardware half survives as the open
      question, with the bring-up incident kept as its evidence.
- [x] The "Nothing reads `versions` yet" bullet is rewritten or deleted per the
      section above, and does **not** duplicate a debt `embarch-umbrella/open.md`
      already owns.
- [x] `changelog.d/` fragment if the answer changes what the doc claims is
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

## Outcome, 2026-09-06

**First bullet: rewritten, both halves named.** All four `embarch-umbrella`
decision numbers were resolved in the tree before being written, not assumed —
41 is in `decisions/projects.md`, 42 in `decisions/doctor.md`, 33 and 36 in
`decisions/schema-skew.md`. `embarch-api` has its own decisions 36, 41 and 42 on
unrelated subjects, which is exactly why the citation names the sub-project.

**Second bullet: deleted, not rewritten.** Both halves are closed and the
narrowest residual — check 11 has never run inside a `doctor` against a live
Core — is `embarch-umbrella/open.md`'s ("No `doctor` run has used decision 42's
wider locator"), and decision 42 itself says so in its own words. *The argument
against:* `versions` is a surface this crate ships whose only consumer is in
another repo, which is the shape of the unpinned-mirror bullet above it, so a
one-line "pinned from one side only" note was defensible. It loses because
decision 42 records the shape **measured** against both `embarch-api` binaries
on 2026-09-06 — `--json` before the subcommand, `host_type_schema_version: 17`
— so it is an observed contract, not a mirror. Nothing api-owned was left.

**The reserve was not cleared, and could not have been by this task alone.**
`open.md` went 4,873 B → 4,711 B against a 5,120 cap; the reserve line is 4,608.
Deleting the `versions` bullet outright frees 251 B, so even a first bullet
rewritten to **zero** net growth lands at 4,622 — 14 B inside reserve. The
first bullet had to grow by 31 B to carry decision 41, the date and the
still-asserting-configs caveat. `tasks/api/028` therefore keeps its `open.md`
item; its **Must not delete** protection of this bullet ("until `api/025`
lands") is now spent, and Settled-deferred is still the cut it names.
This task's dispatch-time figure of 4,521 B predates `api/024`, which landed
decision 56 into this file.
