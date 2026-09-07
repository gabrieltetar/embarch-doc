#!/usr/bin/env python3
"""Check that a task number is allocated once and never reused.

`tasks/README.md` says **NNN** is "three digits, monotonic per sub-project,
never reused." Until 2026-09-06 that was a rule with no mechanism, and it had
already been broken twice on `main` with all nine checks green:

  * `tasks/doc/007` -- `daily-log-fold-has-no-safe-mechanism` and
    `permission-alert-fires-for-the-owner-not-the-fleet`.
  * `tasks/doc/015` -- leg 018's inbox drain at 03:34 and the owner's own file
    at 04:19, an hour apart. Leg 018 found it by eye while rebasing.

`doc/015` is the one `tasks/doc/019` was filed for; `doc/007` was found by this
script's own history scan and had never been reported. Two instances, not one,
which is why this is a gate and not a note in a README.

**Why it recurs by construction.** The claim commit interlocks two *supervisors*
against dispatching one task, and it works. There is no interlock at all between
the supervisor and the owner, who both hold `write` on `tasks/` (protocol §3) and
who are most likely to be filing at the same moment -- when the fleet is busy.
`tasks/doc/` is the directory they share, and it is where both collisions landed.

Three things fail:

  1. **A live collision** -- two files under one `tasks/<scope>/` sharing an NNN.
     Tree only, no git. This is the cheap check and the one that fires.
  2. **A reissue** -- a file in the tree carrying an NNN that this branch's
     history shows once belonged to a different slug. Every completed task is
     `git rm`'d at its fold, so the highest number *on disk* is not the highest
     ever *issued*, and a filer reading the directory will eventually re-issue
     one. That is the case a tree-only check structurally cannot see.
  3. **A malformed name** -- a `.md` under `tasks/<scope>/` that is neither
     `NNN-slug.md` nor `README.md`. A file with no parseable number holds no
     number, so nothing else in the queue can address it.

**The history half reads `HEAD`, deliberately not `--all`.** `--all` would sweep
in abandoned worker branches and burn their numbers forever, so a perfectly good
file on `main` could be reddened by a branch nobody ever merged. What "issued"
means here is "issued on this line of history". It costs ~30 ms.

**Where it degrades, it says so rather than passing quietly.** A shallow clone
(`actions/checkout` defaults to depth 1) cannot answer question 2, so the
history half is skipped with a `NOTE:` that `check-docs.py` surfaces. The CI job
for this check sets `fetch-depth: 0` precisely so it is not skipped there.

**Prevention, not just detection.** `--next` prints the number that is actually
safe to issue per scope -- max(ever issued, on disk) + 1 -- and a failure names
it too. Reading the directory is what both colliding filers did.

Usage:
  scripts/check-task-numbers.py             gate
  scripts/check-task-numbers.py --next      next free NNN, every scope
  scripts/check-task-numbers.py --next doc  next free NNN for one scope
Exit status: 0 if every task number is unique and never reused, 1 otherwise.
"""
import collections
import glob
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TASK_RE = re.compile(r'^tasks/([^/]+)/(\d{3})-(.+)\.md$')
# Not a task, and not malformed: the queue's own README.
EXEMPT = {'README.md'}


def tree_tasks():
    """{scope: {NNN: [slug, ...]}} for the files on disk right now."""
    found = collections.defaultdict(lambda: collections.defaultdict(list))
    malformed = []
    pattern = os.path.join(REPO_ROOT, 'tasks', '*', '*.md')
    for path in sorted(glob.glob(pattern)):
        rel = os.path.relpath(path, REPO_ROOT).replace(os.sep, '/')
        m = TASK_RE.match(rel)
        if m:
            found[m.group(1)][m.group(2)].append(m.group(3))
        elif os.path.basename(rel) not in EXEMPT:
            malformed.append(rel)
    return found, malformed


def history_tasks():
    """({scope: {NNN: {slug, ...}}}, why_skipped) from HEAD's history.

    `why_skipped` is None when the scan ran, else a one-line reason.
    """
    def git(*args):
        return subprocess.run(('git', '-C', REPO_ROOT) + args,
                              capture_output=True, text=True, check=True).stdout
    try:
        if git('rev-parse', '--is-shallow-repository').strip() == 'true':
            return {}, 'shallow clone -- no history to read'
        out = git('log', '--pretty=format:', '--name-only', '--', 'tasks/')
    except (OSError, subprocess.CalledProcessError) as exc:
        return {}, f'git unavailable ({exc.__class__.__name__})'
    ever = collections.defaultdict(lambda: collections.defaultdict(set))
    for rel in set(out.split('\n')):
        m = TASK_RE.match(rel)
        if m:
            ever[m.group(1)][m.group(2)].add(m.group(3))
    return ever, None


def next_free(tree, ever):
    """{scope: NNN} -- one past the highest number ever issued or on disk."""
    nxt = {}
    for scope in set(tree) | set(ever):
        nums = {int(n) for n in tree.get(scope, ())} | {int(n) for n in ever.get(scope, ())}
        nxt[scope] = max(nums) + 1 if nums else 1
    return nxt


def main():
    args = sys.argv[1:]
    tree, malformed = tree_tasks()
    ever, skipped = history_tasks()
    nxt = next_free(tree, ever)

    if args and args[0] == '--next':
        scopes = args[1:] or sorted(nxt)
        for scope in scopes:
            print(f'{scope} {nxt.get(scope, 1):03d}')
        return 0

    failures = []
    for scope in sorted(tree):
        for nnn in sorted(tree[scope]):
            slugs = tree[scope][nnn]
            if len(slugs) > 1:
                failures.append((f'tasks/{scope}/{nnn}', 'two files share it',
                                 sorted(slugs), nxt[scope]))
                continue
            reissued = ever.get(scope, {}).get(nnn, set()) - {slugs[0]}
            if reissued:
                failures.append((f'tasks/{scope}/{nnn}', 'reissued; history has it as',
                                 sorted(reissued), nxt[scope]))
    for rel in malformed:
        failures.append((rel, 'not <NNN>-<slug>.md, so it holds no number', [], None))

    if skipped:
        # NOTE: is the marker check-docs.py surfaces on an otherwise-green run.
        print(f'NOTE: reuse-after-deletion not checked -- {skipped}. '
              f'Live collisions still are.')
        print()

    if failures:
        print(f'{len(failures)} task-number problem(s):\n')
        for what, why, slugs, free in failures:
            print(f'  {what} -- {why}')
            for slug in slugs:
                print(f'      {slug}')
            if free is not None:
                print(f'      next free for this scope: {free:03d}')
        print('\n`tasks/README.md`: NNN is three digits, monotonic per '
              'sub-project, and never reused.\n'
              '`--next <scope>` gives a number that is safe to issue.')
        return 1

    total = sum(len(v) for v in tree.values())
    print(f'All {total} task number(s) unique across {len(tree)} scope(s)'
          + ('' if skipped else ', and none reissued from history') + '.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
