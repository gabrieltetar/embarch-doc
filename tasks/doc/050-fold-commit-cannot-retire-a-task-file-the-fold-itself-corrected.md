# 050 — `fold-commit.py`'s `git rm` refuses a finished task file the fold itself modified, after the log commit has already landed

**State:** open
**Source:** leg 104, 2026-09-13, unit `dev-bench/028`. Hit live; the fold had to be finished by
hand and the leg says so in its log entry and in the commit message (`embarch-doc` `9f6f567`).
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is one flag in `scripts/fold-commit.py`, a reserved path.

## What

`fold-commit.py` retires a finished task file itself rather than trusting the caller to, and its
own docstring says so:

> This fold does the `git rm` itself rather than trusting the caller to.

It runs `git rm -q -- <task file>`. Plain `git rm` **refuses a file with local modifications**:

```
git rm -q -- tasks/dev-bench/028-...md failed in /home/gabriel/Github/embarch/.worktrees/embarch-doc/leg:
error: the following file has local modifications:
    tasks/dev-bench/028-...md
(use --cached to keep the file, or -f to force removal)
```

## Why a supervisor hits it, and why it is not a rare shape

The modification was the supervisor **correcting the task's own state line so the fold could
retire it at all.** The worker had written `**State:** closed`. `closed` is not one of the four
words (`tasks/README.md`: "`closed` is not a synonym for `done`; write `done`"), and
`unit_task_not_settled()` in this same script refuses a fold whose task does not say `done` or
`blocked`. So the supervisor is *required* to edit the file, and editing it is what makes the
`git rm` fail.

Those two behaviours are in the same script and they contradict each other:

- refuse the fold unless the task file says `done`, which for a worker that wrote anything else
  means the supervisor edits it in the fold;
- then delete that file with a command that refuses an edited file.

`closed` is the likeliest trigger — the queue has already lost five tasks to it — but **any**
supervisor edit to the task file in the fold does it: striking a paid file off a `Compacts:` line,
adding a `## Blocked` section, correcting a dispatch note.

## Why the recovery is expensive rather than annoying

The failure lands **after the log commit**, by design: `fold-commit.py` commits
`supervisor-log.md` first so the orderings a kill can leave are "nothing", "log only", or "both".
The `git rm` is on the instance side, which is last. So the state after the failure is **log
only** — the entry is committed and the fold is not — and re-running is refused by the guard that
exists to catch exactly that:

> `supervisor-log.md` has no uncommitted change, so this unit's entry is either already committed
> or was never written. Check before retrying.

Correct refusal, no way forward through the script. The supervisor must finish the fold by hand:
`git rm -f`, `git add` the rest, commit with the same message, push, and prune the landed branch
itself — every step the script exists to make atomic, done manually at the one moment the atomicity
mattered.

## It happened twice in the leg that filed it

Second occurrence, ~20 minutes later, on `suite/010`: the fold marked the task `done` and wrote a
`## Closed` section into it — an ordinary supervisor edit, nothing to do with the `closed`/`done`
vocabulary — and the `git rm` refused for the same reason, again after the log commit had landed
(`embarch-fleet` `e038fe3`). **So the `closed` case is the likeliest trigger but not the shape of
the defect**: any unit whose fold touches its own task file hits this, which is most folds that do
more than tick a checkbox. Two of this leg's four units did.

## Suggested fix

`git rm -q -f --` for the finished task file. The file is being deleted in this very commit, so
its working-tree content is about to stop existing either way — there is nothing for `-f` to
destroy that the fold was not already destroying.

**Do not** fix it by refusing a fold that modified the task file: that forbids the state
correction this same script requires, and it would have turned this unit into a blocked one over a
single word.

## Worth considering alongside, but not required

`unit_task_not_settled()` could say, when it sees `closed` specifically, that the word is a known
worker mistake with a known fix — it already knows the vocabulary is closed and already prints the
offending token. That is a message improvement, not the defect.

## Done when

- [ ] A fold whose unit's task file was modified in that same fold retires the file instead of
      failing after the log commit has landed.
- [ ] Gate green.
