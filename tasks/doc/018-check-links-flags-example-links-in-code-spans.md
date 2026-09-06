# 018 — `check-links.py` flags markdown links written as examples inside code spans

**State:** open
**Source:** `inbox/doc-check-links-ignores-code-spans.md`, dropped by `agent/api/023-split-shape-by-mission` 2026-09-06. The task file `tasks/api/023-split-shape-md-by-mission.md` failed `check-links.py` at its own claim commit `57ab4dc`, before the worker changed anything.
**Scope:** doc
**Hardware:** none. One script in `scripts/`, plus whatever prose it unblocks.
**Owner:** required — `scripts/` is owner-only (`../../embarch-fleet/protocol.md` §3).

> **Renumbered 015 → 018 by leg 018, 2026-09-06.** I filed this as `tasks/doc/015`
> at 03:34 and the owner independently filed a *different* `tasks/doc/015` at
> 04:19; both reached `main` and the full gate passed on the result. `NNN` is
> supposed to be monotonic per sub-project and never reused, and **nothing in
> `scripts/` checks that** — see `tasks/doc/019`, filed for it. Mine is the one
> that moved, because the owner's commit message cites his by number.

## What

`scripts/check-links.py` reads each `*.md` file's raw text and runs `LINK_RE`
over the whole thing. It strips **nothing** first: no fenced code blocks, no
inline code spans. The only backtick handling in the file is inside `slug()`,
which is for heading anchors, not for link extraction.

So a doc that *documents* the shape of a reference by quoting one — the natural
way to explain a convention — is reported as a broken relative link, because the
example target resolves relative to the doc explaining it rather than to the doc
that would carry it. `tasks/api/023` did exactly this: it warned that a
bracket-then-parenthesis reference to `decisions/shape.md` with a decision number
beside it keeps resolving after that number has moved out of the file. Written
from `tasks/api/`, the example target resolved to `tasks/api/decisions/shape.md`,
which has never existed.

The worker reworded its own task file so no example reference remains, which is
the only fix available to it. That is a workaround per doc, not a fix: the next
author who quotes a reference pays it again, and the cheapest response —
deleting the example — makes the doc worse. **This task file is itself written
around the bug**, which is the second instance.

**The likely fix** is to blank out fenced blocks and inline code spans before
running `LINK_RE`, the way a renderer would. Worth checking against the corpus
first: any doc currently relying on a backticked link being checked would stop
being checked, and that trade should be made deliberately.

## Why now

Nothing is broken today — the gate is green. It matters because the failure mode
is confusing rather than loud: the check names a target that looks real, and a
reader's first instinct is to hunt for a missing file. `DOC-CONVENTIONS.md` and
the `tasks/` and `inbox/` READMEs are the docs most likely to want an example
reference, and they are exactly the docs nobody should have to reword around a
checker.

**It has also now cost a leg directly.** Leg 017 pushed a red `main` because it
committed this task file's ancestor without re-running the gate; the next
worker's first minutes went to proving the red was not its own.

## Done when

- [ ] `check-links.py` ignores link syntax inside fenced code blocks and inline
      code spans, **or** the suite decides deliberately that it should not and
      says so where an author would read it.
- [ ] A regression case: a doc containing a code-spanned reference to a path that
      does not exist passes.
- [ ] The corpus re-checked, and any link that was only being validated because
      it sat inside backticks is named rather than silently dropped from coverage.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
