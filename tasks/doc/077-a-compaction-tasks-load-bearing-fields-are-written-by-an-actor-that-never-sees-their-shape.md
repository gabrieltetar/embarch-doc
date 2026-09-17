# 077 — a compaction task's load-bearing fields are written by an actor that never sees their shape

**State:** open
**Source:** `inbox/workers-file-compaction-tasks-that-no-consumer-can-read.md`, filed by the leg 133
supervisor while landing three units that each spent doc-size reserve. Not a worker's report — each
worker believed it had filed correctly.
**Scope:** doc
**Hardware:** none — a mismatch between what `tasks/README.md` and `DOC-COMPACTION-PASS.md` require
of a compaction task and what a worker actually writes when it files one mid-unit.
**Owner:** required — the candidate fixes live in `.claude/leg.md` (generated from
`embarch-fleet/scripts/install.py`'s template), `tasks/README.md`, and
`scripts/check-task-state.py`. All three are owner-reserved, and a supervisor amending the
instruction that tells it how to dispatch is the thing the ownership split exists to prevent.

## What happened

Two units in leg 133 pushed a doc into reserve and each filed its own compaction task, as
`.claude/leg.md` requires. Neither file was in the shape the rules expect, in two different ways,
and **the gate was green both times**:

- **`tasks/umbrella/077-compact-docs.md`** (filed by `umbrella/076`): `**State:** open`, while its
  own `## In flux` section answers **Yes** for its single `Compacts:` file. `.claude/leg.md` is
  explicit that `yes` for every file on the line means `blocked`. It also carried no `**In flux:**`
  field at a line start, no `**Unparks when:**`, and no `**Must not delete:**`, so
  `grep '^\*\*In flux:'` saw nothing and a leg reading fields rather than prose would have
  dispatched a worker into it.
- **`tasks/topology/057-compact-topology.md`** (filed by `topology/055`): **two `**State:**`
  lines** — `open` at line 3 and `blocked — unparks when tasks/topology/056 lands` at line 34,
  inside a `## In flux: yes` section whose last sentence is the instruction *"Set `**State:**
  blocked`"*. The worker wrote the reasoning, reached the right answer, and left the instruction in
  the file instead of applying it to the field at the top.

Leg 133's supervisor corrected both by hand at the fold and said so in each file.

## Why it costs something

**A compaction task is the one task type whose *fields* decide whether it may be dispatched**, and
the worker filing it is the only actor holding the context that answers the flux question. So the
field is written by whoever knows the answer and read by whoever must not dispatch, and nothing
checks the handoff. `check-task-state.py` validates `State:`'s first token but is happy with two
`State:` lines and with a flux answer that lives in a heading. `check-doc-size.py` reads the debt
and its date, which were both fine in both files.

Without those two hand edits: `topology/057` would have read `open` to `queue-status.py`'s
`split()[0]` on line 3 while reading `blocked` to anything that greps for the last match, and
`umbrella/077` would have been a dispatchable compaction task whose own body says do not compact
this yet.

**This is the third and fourth structural miss on compaction-task fields on record.**
`tasks/doc/030` already settled that `In flux:` is answered per file, after three live violations;
`tasks/doc/039` records a bolded `Owner: required` value being invisible to `queue-status.py`. The
pattern is the same every time: **a field whose shape is load-bearing, written by an actor that
never sees the shape.**

## Three candidate fixes, cheapest first — the choice is the owner's

1. **Put the field list in the worker's dispatch instruction.** `.claude/leg.md` tells the
   supervisor to tell the worker to *file* `tasks/<scope>/<NNN>-compact-<scope>.md` and points at
   `tasks/README.md` for the shape. A worker mid-unit does not open `tasks/README.md`. Naming the
   five literal fields — `State`, `Compacts`, `In flux`, `Size debt due`, `Must not delete` — in
   the dispatch note itself is one line and would have prevented both misses.
2. **Make `check-task-state.py` refuse a second `**State:**` line**, and refuse a compaction task
   (one with a `Compacts:` line) carrying no `**In flux:**` field at a line start. Both are
   mechanical, and both failures were silent.
3. **Let the worker file the debt without deciding the state** — e.g. a `**State:** filed` that
   `queue-status.py` never counts as dispatchable, leaving the supervisor to resolve it to
   `open`/`blocked` at the fold. The largest change, and the only one that removes the class rather
   than catching it, because it stops asking the worker for a field only the queue reads.

## Done when

- [ ] One of the three above (or something better) is chosen and applied.
- [ ] If it is option 2, the check is added and both of leg 133's corrected files still pass.
- [ ] `tasks/README.md` and `.claude/leg.md` agree on the field list, whichever way it lands.
