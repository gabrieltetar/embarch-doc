# 072 — `fold-commit.py` cannot fold a `suite/` task, because the supervisor edits that task file in its own working tree

**State:** open
**Source:** leg 127, 2026-09-16, hit live while folding `suite/040`. Reproduced by the failure
itself, not inferred.
**Scope:** doc
**Hardware:** none — one script and its callers. Nothing is built for a board, no probe, no live
Core.
**Owner:** required — the fix is in `scripts/fold-commit.py`, which is owner-reserved
(`../../embarch-fleet/protocol.md` §2). A supervisor that can edit the script enforcing its own fold
discipline has none, which is exactly why this is filed rather than fixed.

## What happens

`fold-commit.py` commits the log entry first, then settles the doc-repo paths, and it retires a
completed task with a plain `git rm`. That `git rm` **fails on a file carrying an unstaged
modification**, and refuses with git's own message:

```
error: the following file has local modifications:
    tasks/suite/040-....md
(use --cached to keep the file, or -f to force removal)
```

By then the log commit has already landed — which is the ordering the script deliberately chooses,
so the recoverable state is "an entry for a fold that has not happened" rather than "a fold nobody
logged". The recovery is real but manual: `git add` the task file, `git rm -f` it, and write the
doc-side commit by hand, at which point `fold-commit.py` refuses a retry (correctly) because the log
no longer has an uncommitted change.

## The documented workaround does not work, and it is the one two other docs tell you to use

**Added by leg 136, 2026-09-17, hit live while folding `suite/043`.** The recovery paragraph above
opens with *"`git add` the task file"*, and `.claude/leg.md`'s dispatch guidance says the same in
the other direction — `tasks/suite/043`'s own "known mechanical traps" section says, in as many
words, *"`git add` this file before the fold."* **I did exactly that, and it fails too, with a
different git message:**

```
error: the following file has changes staged in the index:
    tasks/suite/043-....md
(use --cached to keep the file, or -f to force removal)
```

So `git rm` refuses **both** states a `suite/` task file can be in at fold time — unstaged
modification *and* staged modification. Its only accepted state is a file identical to `HEAD` that
already reads `**State:** done`, and a `suite/` task is never in that state, because the supervisor
is the actor that writes `done` and there is no branch for it to arrive on. **The pre-emptive
`git add` does not avoid the failure; it converts it into a second one that looks unrelated**, and
it costs the same log-committed-fold-not-committed recovery.

What actually worked, and what the fix should probably make unnecessary: `git rm -f` the task file
directly (its content is about to be deleted, so the unlanded `done` edit is discarded harmlessly),
then write the doc-side commit by hand naming the already-landed log commit. Landed that way as
`095797a`, log `embarch-fleet@409134c`.

**Two documents to correct when this is fixed** — both owner-reserved, which is why they are named
rather than edited: `.claude/leg.md`'s `suite`-task guidance, and this task's own recovery
paragraph. A workaround that is wrong in two places is worse than no workaround, because it reads
as tested.

## Why it only bites `suite/` tasks

**Every ordinary unit's task file arrives already committed.** A worker sets `**State:** done` on
its own branch and pushes; by fold time the change is in `HEAD`, so `git rm` sees a clean file.

**A `suite/` task has no worker and no branch.** `../../embarch-fleet/protocol.md` §8 has the
supervisor execute it itself, so the supervisor edits `tasks/suite/<NNN>.md` **in its own leg
working tree**, where the edit is unstaged right up to the moment `fold-commit.py` runs. So the one
class of task the protocol reserves to the supervisor is the one class its fold script cannot
retire.

It is not rare, and it is not new — it will fire on **every** `suite/` task, every time. It has
presumably been absorbed by hand before now without anyone filing it.

## Possible fixes, for whoever holds the script

1. **`git add` each `--path` before settling it.** The script already stages by explicit path; a
   completed task file is one of those paths, so staging it first and then removing it costs
   nothing and cannot sweep anything the path list did not name.
2. **`git rm -f`** for a file whose only modification is the one this fold is landing. Narrower,
   but `-f` discards without looking, and the script's whole design is about not doing that.
3. **Refuse earlier.** Check the path list for unstaged task-file modifications *before* committing
   the log, so a supervisor gets "stage this first" instead of a half-landed fold. Cheapest, and it
   keeps the invariant the current ordering exists to protect.

(1) and (3) compose; that is probably the answer, but the call is the owner's.

## Done when

- [ ] Folding a `suite/` task the supervisor executed and edited in its own tree completes in one
      `fold-commit.py` invocation, with no hand-written commit and no half-landed log entry.
- [ ] Whatever the fix is, it cannot stage a path outside the `--path` list — that refusal is why
      `--only` and explicit paths exist at all (legs 004, 005 and 016).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
