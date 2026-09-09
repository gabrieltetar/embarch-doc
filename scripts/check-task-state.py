#!/usr/bin/env python3
"""Check that a task file's machine-read fields are actually machine-readable.

`tasks/README.md` gives four states -- `open` -> `claimed` -> `done`, or
`blocked` -- and every consumer reads them the same cheap way
`queue-status.py` does: take the `**State:**` line, split on whitespace, look
at token zero. Everything after that token is prose for a human, and that is
the right design; the field has to carry *why*, and no vocabulary would ever
cover it.

**What had no mechanism was token zero itself.** It is written by hand, by a
worker or a supervisor, at the end of a unit, and nothing has ever read it back.
`tasks/doc/028` filed the class after six instances in two legs. Three more were
sitting on `main` when it was fixed, and they are the argument for this file:

  * **Two tasks whose own text says they are open were invisible to dispatch.**
    `dev-bench/012` ends its state line with *"This task stays open for that
    remaining half"* and `umbrella/036` with *"mirrors 2 and 3 still open"* --
    and both began `partially`, so `split()[0]` was `"partially"`, which is not
    `open`, so `classify()` filed them under `other` and no leg could ever see
    them. Real remaining work, correctly described, structurally undispatchable.
  * **Five completed tasks were never retired.** They said `closed`, which is
    not one of the four states and never has been. `fold-commit.py` deletes a
    task file at its fold by matching `^\\*\\*State:\\*\\*\\s*done\\b`, so all
    five silently survived the folds meant to remove them and sat in the queue
    for up to four days.

Neither failure is loud. Both are one word.

**This checks the vocabulary and nothing else.** It does not read a state back
against what happened -- that is `fold-commit.py`'s job at the fold, where the
truth is known, and this file cannot know it. It refuses to guess a correction
for the same reason `tasks/doc/028` says not to: every one of those instances
was resolved by a judgement about what actually occurred, and a script that
guessed would turn a loud wrong field into a quiet one.

Two rules, and only one of them fails the gate:

  1. **`**State:**` token zero is one of `open`, `claimed`, `done`, `blocked`**,
     exactly -- no trailing comma, no `partially`, no `closed`. Prose follows
     after a dash, comma or parenthesis and is never inspected. **This fails.**
     It is mechanical, it has no policy in it, and it had three live victims.
  2. **`In flux: yes` implies `blocked`** (`.claude/leg.md`). **This warns.**

**Why (2) only warns, which is a judgement and should be read as one.** The rule
is real and `.claude/leg.md` states it plainly. But four tasks on `main` violate
it today and all four have a live, well-argued flux reason, so enforcing it
would move four more size debts into `blocked` -- and `check-doc-size.py`'s own
header calls `blocked` "the parked state that absorbed 13 of 28 debts" and
treats that absorption as the problem it is trying to end. So a hard rule here
would satisfy one rule by feeding the failure mode of another, on a corpus where
the second one is already losing. Reconciling them is a decision nobody has
made; making it silently, inside a checker, by picking whichever rule was easier
to code, is precisely the move `tasks/doc/028` exists to stop. Warning keeps it
visible until someone decides.

Usage:
    scripts/check-task-state.py            check tasks/ and inbox/
    scripts/check-task-state.py --list     print every state token in use
Exit status: 0 all task files parse, 1 at least one does not.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# tasks/README.md "## States". `claimed by agent/<...>, <date>` is still
# `claimed` at token zero, which is exactly why token zero is what is checked.
LEGAL = ("open", "claimed", "done", "blocked")

# `inbox/` drops carry the same format minus the number (inbox/README.md), and
# a drop is always `open` -- but it is checked here rather than exempted,
# because a malformed drop becomes a malformed task the moment it is promoted.
DIRS = ("tasks", "inbox")

STATE_RE = re.compile(r"^\*\*State:\*\*\s*(.+?)\s*$", re.M)
IN_FLUX_RE = re.compile(r"^\*\*In flux:\*\*\s*(\S+)", re.M)


def token(raw: str) -> str:
    """Token zero, the way every consumer reads it: `raw.split()[0]`.

    Markdown emphasis is stripped first and nothing else is. A state written
    `**open**` reads as `**open**` to `queue-status.py` and is a bug, but it is
    a bug about emphasis rather than about vocabulary, so it is reported with
    the real name rather than as an unknown word.
    """
    parts = raw.split()
    return parts[0].strip("*_`") if parts else ""


def task_files() -> list[Path]:
    out = []
    for d in DIRS:
        root = REPO / d
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*.md")):
            if p.name != "README.md":
                out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true",
                    help="print every state token in use and how many carry it")
    args = ap.parse_args()

    fails: list[str] = []
    warns: list[str] = []
    seen: dict[str, int] = {}
    for p in task_files():
        rel = p.relative_to(REPO)
        text = p.read_text(encoding="utf-8", errors="replace")
        m = STATE_RE.search(text)
        if not m:
            fails.append(f"{rel}\n    no `**State:**` line -- every consumer "
                         f"reads one, and a file without it is unclassified")
            continue
        raw, tok = m.group(1), token(m.group(1))
        seen[tok] = seen.get(tok, 0) + 1
        if tok not in LEGAL:
            fails.append(
                f"{rel}\n    state token {tok!r} is not one of "
                f"{', '.join(LEGAL)}\n    line: **State:** {raw[:90]}"
                f"\n    every consumer reads `split()[0]`, so this file is "
                f"whatever `{tok}` sorts into -- for `queue-status.py` that is "
                f"`other`, i.e. not dispatchable")
        flux = IN_FLUX_RE.search(text)
        if flux and flux.group(1).lower().strip("*_`.,") == "yes" and tok != "blocked":
            warns.append(
                f"{rel}: `In flux: yes` but state is {tok!r}")

    if args.list:
        for k, v in sorted(seen.items(), key=lambda kv: -kv[1]):
            mark = " " if k in LEGAL else "  <-- not a state"
            print(f"  {v:3d}  {k}{mark}")

    if warns:
        print(f"{len(warns)} `In flux: yes` task(s) not `blocked` -- advisory, "
              f"nothing failed:\n")
        for w in warns:
            print(f"  {w}")
        print("\n  `.claude/leg.md` says such a task is `blocked` and names what\n"
              "  unparks it. Not enforced: see this script's header -- parking\n"
              "  four more debts feeds the bucket `check-doc-size.py` is trying\n"
              "  to drain, and which rule wins is nobody's decision yet.\n")

    if fails:
        print(f"{len(fails)} task file(s) with an unreadable state field:\n")
        for f in fails:
            print(f"  {f}\n")
        print("tasks/README.md '## States' has the four; prose goes after "
              "token zero, never in it.")
        return 1
    n = len(task_files())
    print(f"OK: all {n} task file(s) carry one of {', '.join(LEGAL)} at "
          f"token zero.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
