# tasks

The work queue background agents pull from. One file per task, committed to
`main`, claimed by editing the file. Governed by
[../embarch-parallel-agents.md](../embarch-parallel-agents.md).

    tasks/<sub-project>/<NNN>-<slug>.md

- **sub-project** — without the `embarch-` prefix (`core`, `api`, `dev-bench`,
  `study-designer`, `outpost`, `ui`, `topology`, `umbrella`, `promptu`,
  `atlas`), or `doc` for this repo, or `suite` for a task spanning several.
  A `suite/` task is **never dispatched to a worker** — the supervisor executes
  it itself (`embarch-parallel-agents.md` §8).
- **NNN** — three digits, monotonic per sub-project, never reused.
- **slug** — short, hyphenated.

## File format

```markdown
# 007 — Drain the SSE subscriber on api's study_status

**State:** open
**Source:** embarch-core/open.md — "api/CLI consumption of /study/{id}/events is not built"
**Scope:** api                     <!-- one sub-project, or `suite` -->
**Hardware:** none                 <!-- none | verify-only | required -->

## What

One paragraph. What is to be true when this is done.

## Why now

One or two sentences, and the doc that says so. A task with no source doc is a
task the supervisor invented; that is allowed, and it says so here.

## Done when

- [ ] Concrete, checkable items.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
```

## States

`open` → `claimed` → `done`, or → `blocked`.

- **claimed** — the claim line becomes
  `**State:** claimed by agent/<scope>/<NNN-slug>, <yyyy-mm-dd HH:MM>`.
  Claiming is a commit to `main` by the supervisor **before** dispatch, not by
  the worker after it starts. Two supervisors cannot both claim; one supervisor
  is what this relies on.

  **The timestamp is load-bearing, not decoration.** A supervisor that dies
  mid-batch — killed, rate-limited, crashed — leaves its tasks claimed by a
  worker that no longer exists, and nothing would ever release them. So refill
  (`embarch-parallel-agents.md` §6 phase 1) **reclaims any claim older than 4
  hours** back to `open`, after checking whether its branch exists: a branch
  with commits on it means the work may be salvageable and the task goes to
  `blocked` with the branch named, not back to `open` where a second worker
  would redo it.
- **blocked** — the worker appends a `## Blocked` section saying what it found
  and exits. State returns to `open` only when whatever it named is resolved.
- **done** — the file is deleted in the merge that closes it. Git holds it, and
  a completed task left in the queue competes with the open ones for attention
  — the same reasoning `DOC-PROTOCOL.md` §3 applies to a shipped milestone doc.

## Hardware field

`none` — fully host-side, dispatchable. `verify-only` — the change can be built
and unit-tested by a worker but its real behaviour needs a board; dispatchable,
and it must leave a hardware-verification debt (§7). `required` — cannot be
started without hardware; **not dispatchable**, it waits for the owner's own
session. A task nobody has classified is treated as `required`.

## Why the queue is a file and not the supervisor's head

Two supervisor runs cannot dispatch the same task; a task outlives the thread
working it; and the reason a task exists is written next to it rather than
re-derived from the roadmap each batch. The cost is that the queue is a *view*
of the docs and can drift from them — refill reconciles, in one direction only
(`embarch-parallel-agents.md` §12).
