# 019 — Two actors allocated `tasks/doc/015` an hour apart, both landed on `main`, and the full gate passed

**State:** open
**Source:** observed by leg 018, 2026-09-06, while rebasing onto the owner's `7ef47f2`.
**Scope:** doc
**Hardware:** none. One check in `scripts/`, or a deliberate decision that no check is wanted.
**Owner:** required — `scripts/` is owner-only (`../../embarch-fleet/protocol.md` §3).

## What

`tasks/README.md` says **NNN** is "three digits, monotonic per sub-project, never
reused." On 2026-09-06 it was reused, by the two actors least likely to notice:

- **03:34**, leg 018's `inbox/` drain committed `tasks/doc/015-check-links-flags-example-links-in-code-spans.md` (`1657f86`).
- **04:19**, the owner committed `tasks/doc/015-the-doc-gate-scans-gitignored-inbox-drops.md` (`7ef47f2`).

Both reached `main`. **`python3 scripts/check-docs.py` — all nine checks — passed
on the result**, in the leg worktree and in the owner's checkout. Leg 018 found it
by eye, an hour later, only because the rebase listed the directory.

Leg 018 renumbered **its own** to `018`, because the owner's commit message cites
his by number. That resolves this instance and not the class.

## Why this is worse than a cosmetic clash

A task number is the handle everything else uses. A `Must not delete:` list cites
one; a `blocked on` field cites one; a supervisor log entry cites one; a
compaction task's `Compacts:` field is reconciled against one. **Two files
answering to `doc/015` means every one of those references is ambiguous**, and the
ambiguity is silent — the wrong file is a plausible file.

It is also structurally likely to recur rather than a fluke. The claim commit is
the interlock against two *supervisors* dispatching one task
(`../../embarch-fleet/protocol.md` §4), and it works. **There is no interlock at
all between the supervisor and the owner**, who both write `tasks/` by design
(§3's table gives both `write`), and who are most likely to be filing at the same
time precisely when the fleet is busy. `tasks/doc/` is the directory they *share*,
so it is the likeliest place for this, and it is where it happened.

## What would close it

The cheap version is a check, and it is a few lines: **no two files under
`tasks/<scope>/` share an `NNN` prefix.** It belongs in `check-docs.py`'s list
rather than anywhere clever, because the property is about the working tree and
not about any one commit.

A stronger version would also catch **a number reused after its file was deleted**
— every completed task file is `git rm`'d at its fold, so the highest number on
disk is not the highest ever issued, and the next filer reading the directory will
eventually re-issue one. That needs git history rather than the tree, which is
more than the cheap check and may not be worth it; say so either way.

## Done when

- [ ] `check-docs.py` fails on two files sharing an `NNN` under one
      `tasks/<scope>/`, **or** the suite decides deliberately that it should not
      and says so in `tasks/README.md` beside the "never reused" sentence — which
      is currently a rule with no mechanism.
- [ ] A position on the deleted-file case above: caught, or explicitly out of
      scope with the reason.
- [ ] A regression case for whichever way it goes.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
