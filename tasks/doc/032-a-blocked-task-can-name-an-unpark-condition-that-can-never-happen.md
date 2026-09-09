# 032 — a `blocked` task can name an unpark condition that can never happen, and the soonest debt in the ledger is one

**State:** open
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is a field in `tasks/README.md` and a check in `scripts/`, both
reserved (`../../embarch-fleet/fleet.toml`'s `reserved` list). `tasks/README.md` is also
**generated** from `embarch-fleet/templates/protocol/tasks.README.md`, so the edit is the template
plus `deploy.py`.
**Source:** owner's session 2026-09-09, checking the size ledger after closing `tasks/doc/030`.
`tasks/api/035` had already found the instance on 2026-09-06, leg 021, and filed it as an `api`
concern; this is the class behind it.
**In flux:** no

## What

**`.claude/leg.md` and `tasks/README.md` both require a `blocked` task to name what unparks it.
Nothing checks that the named thing exists.** `tasks/api/026-compact-api.md` names
`tasks/api/001-sse-client.md`, which **is not in the queue and never was** — so its stated unpark
condition cannot be met by the mechanism as written, and `api/035` says so in as many words:
*"nothing will ever land a task that is not in the queue."*

That park is not harmless. `api/026` holds the **soonest-due** entry in the whole ledger
(2026-09-14, three files) and covers `embarch-api/decisions/core-link.md`, filed at **22 bytes**
of headroom and now at 188. `queue-status.py` does not offer a blocked task to a leg, so the debt
is invisible; `check-doc-size.py`'s own header cites this exact file as the motivating failure —
*"a task parked on `In flux: yes` sat at 22 bytes with the argument that unparked it written
inside it."* It is still sitting there, three days after a supervisor wrote down why.

**And the premise has separately gone stale**: the park reads *"the event-stream half of this file
(decisions 48, 49) has never met a real `embarch-core`"*, and on 2026-09-06 `study_watch` returned
pushed frames from a live installed Core against a real study. `api/035` carries that half.

## Why this is the class and not just `api/026`

`tasks/doc/028` (a hand-written `State:`), `tasks/doc/029` (a hand-written scope claim) and
`tasks/doc/030` (an `In flux:` answer that outlived its file) are all *"a task file asserts
something no script checks"*. **This is the fourth**, and it is the one with a live cost in the
ledger. The pattern is now well enough established that the remedy shape is known: a claim must be
**declared in a field**, never inferred from the body.

## The measurement, so nobody repeats the naive version

**Scanning a blocked task's body for `<scope>/<NNN>` references and checking they resolve does not
work, and this has now been measured.** Over the 15 blocked tasks on `main` on 2026-09-09 it
reports dead references in **11** of them, and almost every hit is a *completed* task cited as
history — `umbrella/009` alone names eight (`umbrella/006`, `017`, `018`, `020`, `021`, `022`,
`023`, `037`), every one of which is a paid debt correctly recorded. **A task file is deleted at
its fold**, so citing past work always looks like a dangling reference.

That is the third time this trap has been measured: `Compacts:` matches one declared field because
a mere mention made five of one day's twelve files read as filed, and `doc/029`'s scope check reads
titles because the body flags 76 of 87. **Do not build the body-scanning version.**

## Two shapes, and the light one is probably right

1. **A declared `**Unparked by:**` field on every `blocked` task**, checked by
   `check-task-state.py`: any `tasks/<scope>/<NNN>` it names must resolve, and a `blocked` task
   without the field fails. Cheap, mechanical, and it turns a rule both docs already state into
   one that holds. 15 files gain a field, most by moving a clause they already carry — `ui/021` has
   it on its `State:` line, `dev-bench/012` and `api/026` inside `In flux:`, `study-designer/006`
   in a section. **That inconsistency is itself the argument for a field.**
2. **Also require the condition to be non-task-shaped or resolvable** — i.e. allow "a live
   narrow-bound Core", "the dev-bench FFI staticlib cross-build", a date — and only validate the
   references that look like queue paths. This is (1) plus a sentence in `tasks/README.md`; it is
   not really a second option so much as the honest scope of (1).

**Deliberately not proposed: a rule that a park must name a queued task.** Several live parks are
correctly waiting on something that is not a task at all (`study-designer/006` on a cross-build,
`ui/007` on a real stale prefix), and forcing those into the queue would file work nobody chose —
`risks.md`'s refill risk, from the other direction.

## Done when

- [ ] A `blocked` task's unpark condition is declared in a field, and a queue path it names that
      does not resolve fails the gate.
- [ ] The 15 blocked tasks on `main` carry it, moved from wherever each states it today.
- [ ] `tasks/README.md` (via the template) and `.claude/leg.md` say it, since both currently state
      the naming requirement as prose with no mechanism.
- [ ] **Not this task:** re-judging `api/026`'s premise and splitting `core-link.md`. That is
      `tasks/api/035` and `tasks/api/026`, both `Owner: no` and dispatchable — this task must not
      do a worker's unit.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
