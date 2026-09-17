# 074 — A method fix found in one scope's audit chain has no path to another's

**State:** open
**Source:** `study-designer/060`'s reviewer, leg 131, 2026-09-17. Filed by the supervisor at that
unit's fold — the reviewer declined to drop it in `inbox/` because no locked decision is
contradicted by it, which is the right read of its charter and is also why it would otherwise have
existed nowhere but a subagent's report.
**Scope:** doc
**Hardware:** none — a question about how the fleet's task files carry method. Nothing is built, no
board, no probe, no live Core.
**Owner:** required — every candidate fix is an owner-reserved path. A propagation mechanism is
either a rule (`../../DOC-PROTOCOL.md`, `../../../embarch-fleet/protocol.md`, `.claude/leg.md`) or a
script under `scripts/`, and a supervisor that writes its own propagation rules has none. Filed so
it is visible in the queue rather than nowhere; **do not dispatch it.**

## What happened

The citation-audit chains in this suite carry their method **inside each task file**, copied forward
from unit to unit. `embarch-study-designer`'s chain did that for sixteen consecutive units
(`044`–`059`), and every one of them carried this line:

```
grep -rlIE '[Dd]ecisions[[:space:]]*$'
```

That pattern matches only the **plural** "decisions" at end of line. A citation whose word wraps in
the **singular** — `— decision` ending one line, `52 (interfaces/decoders.md).` beginning the next —
is invisible to it, and equally invisible to the per-file `grep -cE '[Dd]ecisions? [0-9]+'` census,
which needs the number on the same line. Each of those sixteen units re-ran the grep, found nothing
new, and closed the file. `060` found the gap by **reading the file**, not by running the tool.

**Two other scopes had already found and fixed the same gap, before `060` ran.** `history/api.md`
records `api/106` as a *"singular-wrapped citation re-check"* and `history/umbrella.md` records
`umbrella/074`'s *"singular-wrapped citation census"*, both on 2026-09-16. Neither produced an
`inbox/` drop and neither produced a `tasks/suite/*` entry; the fix was recorded only inside each
scope's own `history/` file. So `study-designer`'s chain kept carrying the broken pattern forward
and **rediscovered the gap from scratch**, three legs later, at the cost of a whole unit's attention
and thirteen citation lines in six already-closed files that now need a re-check
(`tasks/study-designer/061`).

## Why this is a mechanism gap and not a worker mistake

Every actor behaved correctly:

- `api/106`'s and `umbrella/074`'s workers fixed the pattern **in their own scope**, which is the
  whole of what a worker owns (`../../../embarch-fleet/protocol.md` §5).
- The supervisors that folded them recorded the fix in `history/` and `supervisor-log.md`, which is
  where a shipped change and a decision go.
- `060`'s worker carried its predecessor's method paragraph forward verbatim, which is what the task
  file told it to do and is why the chain has been reproducible across nineteen units.
- `060`'s reviewer found the cross-scope fact — and it could only find it because it was asked to
  read two other scopes' `history/` files, which is not a reviewer's standing brief.

**Nothing in that sequence has a channel from "a method was fixed in scope A" to "scope B's task
file still carries the broken version".** `supervisor-log.md` is not it: it folds daily and rolls
into `log-archive/`, so a method note in it is on a timer, and nothing dispatches from it.
`history/<scope>.md` is not it: it is per-scope by construction. `open.md` is not it: nothing
dispatches from there either.

## The one mechanism that does exist, and why it did not fire

`tasks/suite/041` came from exactly this shape — `outpost/025`'s worker hit a methodological
question outside its mandate, dropped it in `inbox/` per its own task's instruction, and the
supervisor filed it as a suite-level task at the fold. **That is the sanctioned path.** It requires
the worker who fixes a method to recognise that the fix is not scope-local and to drop it, and
neither `api/106` nor `umbrella/074` did — reasonably, since each was handed a task framed as a
re-check of its own repo.

## Done when — the choice is the owner's, and these are the candidates

- [ ] **Decide whether method belongs in task files at all.** The copied-forward paragraph is what
      makes these chains reproducible and is also what makes them un-patchable. A single
      `DOC-CITATION-METHOD.md` (or a section of an existing reserved doc) that every chain *cites*
      rather than copies would make a fix land once — at the cost of a task file that no longer
      states its own method, which is a real loss for a worker reading cold.
- [ ] **Or add the obligation to the worker contract**: a worker that corrects a *method* rather
      than a finding files an `inbox/` drop saying so, the way it already files a size debt. Cheap,
      and it depends on the worker classifying its own fix correctly.
- [ ] **Or make it mechanical.** The broken pattern is a literal string in `tasks/**`, so a check
      that greps task files for a *superseded* method line is possible — but somebody has to
      maintain the list of superseded lines, which is the same propagation problem one level up.
- [ ] Whichever is chosen, **check whether any other scope's chain still carries the plural-only
      pattern.** `study-designer/061` now carries the corrected one; `dev-bench`, `topology`, `ui`,
      `core` all ran wrap-aware censuses on 2026-09-16 and their task text should be checked rather
      than assumed.

## Not yours

Do not "fix" this by editing another scope's task file to insert the corrected grep. That treats
one instance and leaves the mechanism, and a supervisor or worker rewriting other scopes' method
paragraphs is how nineteen units of reproducibility gets lost in one pass.
