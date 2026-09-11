# 038 — `DOC-PROTOCOL.md`'s two enumerations of the suite-level docs do not know `suite/decisions.md` exists

**State:** open
**Source:** `tasks/suite/008`, executed by the supervisor on leg 073, 2026-09-10. That task created
`suite/decisions.md` and explicitly required the supervisor to stop if the new doc could not be
introduced **without** amending `DOC-PROTOCOL.md` or `DOC-COMPACTION.md`. It could — neither needs
amending for the file to be correct, resolvable or gated — so the move landed. What is left is
narrower and is genuinely the owner's: two enumerations inside a reserved file are now
**incomplete**, not wrong.
**Scope:** doc
**Hardware:** none
**Owner:** **required** — `DOC-PROTOCOL.md` is owner-reserved (`check-ownership.py --supervisor`),
so no agent may make this edit. Filed here rather than left in a log entry so it is visible in
`queue-status.py` instead of riding a file that folds daily and rolls into `log-archive/`.

## What

Two lines in [DOC-PROTOCOL.md](../../DOC-PROTOCOL.md) enumerate the suite-level docs and now omit
`suite/decisions.md`:

- **Line 26**, the directory-tree sketch: `├── suite/  overview, index, roadmap, features, glossary, user-guide`
- **Line 43**, the prose definition of "Suite-level": *"the overview and index, the roadmap, the
  feature inventory, the glossary, `embarch-token.md`, `embarch-dev-workflow.md`,
  `embarch-decision-reversals.md`, and `suite/user-guide.md`"*

Neither says anything false. Both are lists that a reader will reasonably take as closed, which is
exactly how a second home for suite-wide decisions gets invented by someone who looked here first
and concluded there was none — the situation `suite/008` existed to end.

## Why it is the owner's and not the supervisor's

`suite/008`'s own boundary section drew the line: creating a new shared suite-level doc sits close
to the edge between design (the supervisor's, under full delegation) and the doc corpus's own
structure (`DOC-PROTOCOL.md`, reserved). The supervisor's reading, recorded here so it can be
disagreed with:

- **The file did not need `DOC-PROTOCOL.md` amended to be legitimate.** `DOC-BUDGET.md` already
  caps `suite/*.md` at 10 KB, so the new file inherited a real cap with no edit —
  `suite/decisions.md` is 5,826 B against it. `check-docs.py` is green on all 11 checks, and
  `check-ownership.py --supervisor` reports all 16 top-level docs still classified, since the new
  file is not top-level. Nothing was bypassed.
- **But whether the suite-level doc *class* now has a new member is a statement about the corpus's
  shape**, and that sentence lives in a file a supervisor may not write. A supervisor that edited
  it would be editing the rules it runs under to accommodate a file it had just created.

## Done when

- [ ] Line 26's `suite/` sketch and line 43's suite-level list either name `suite/decisions.md`, or
      the owner decides the file belongs somewhere else and says where — **that decision retires
      `suite/decisions.md`, and `embarch.md` §5's pointer plus the two citations updated alongside
      it (`embarch-api/decisions/tests.md`, `tasks/api/039`) follow it.**
- [ ] If it stays, one line somewhere in `DOC-PROTOCOL.md` saying what belongs in it versus in a
      sub-project's own `decisions.md` — `suite/decisions.md`'s own header states the supervisor's
      answer, which is the thing to ratify or replace rather than the authority for it.
