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

Four rules, and all of them fail the gate:

  1. **`**State:**` token zero is one of `open`, `claimed`, `done`, `blocked`**,
     exactly -- no trailing comma, no `partially`, no `closed`. Prose follows
     after a dash, comma or parenthesis and is never inspected. It is
     mechanical, it has no policy in it, and it had three live victims.
  2. **`In flux:` token zero is `yes`, `no` or `per`** -- the third being
     `per file`, for a task naming several docs whose answers differ.
  3. **`In flux: yes` implies `blocked`** (`.claude/leg.md`), *unless the task
     is `Owner: required`*, which already makes it undispatchable.
  4. **`In flux: per` names every path on the `Compacts:` line** inside the
     `In flux:` block itself, so "per file" cannot be an answer that declines
     to say which file.

**Rule 3 warned rather than failed until 2026-09-09, and `tasks/doc/030` is
where that got decided.** The holding position was that `.claude/leg.md` and
this repo's size ledger pointed opposite ways: enforcing would move four more
debts into `blocked`, and `check-doc-size.py`'s header called `blocked` "the
parked state that absorbed 13 of 28 debts". Both sides turned out to be right
and **the field was wrong.**

  * **`In flux:` is a per-FILE judgement that was being recorded in a per-TASK
    field.** A task names several docs, one of them is paid and struck off the
    `Compacts:` line, and the flux answer that belonged to *it* stays behind
    reading as though it covered the rest. Three of the four live violations
    were exactly that: `core/022`'s block argued about `interfaces.md` (closed
    2026-09-07), `dev-bench/012`'s about `decisions/ble.md` (struck off by leg
    057), and `study-designer/006` had it backwards -- its unpark note claimed
    the remaining files were never parked, while the park's own argument names
    `open.md`'s FFI bullet outright. Rule 4 is what stops the field drifting
    from the line again.
  * **`blocked` is no longer absorbing**, so rule 3 costs what it used to
    cost. Every reserve debt carries a `**Size debt due:**` date and a leg
    spends its first unit on the oldest overdue entry *blocked or not*
    (`.claude/leg.md`); `check-doc-size.py` fails a blocked debt with no date
    at all. The absorption that phrase describes was measured before the clock
    existed.
  * **`blocked` keeps meaning "nothing here can be done"**, so a task is
    blocked only when *every* file on its line is in flux. A mixed task stays
    `open` and its dispatch note says which file to leave alone -- which is
    why `study-designer/006` is `open` and `dev-bench/012` is `blocked`.
  * **`Owner: required` is the exemption**, and it is `tasks/doc/024`'s
    argument generalised: ownership already keeps every agent off the task, so
    `blocked` would protect nothing and would hide the debt from the one actor
    who can pay it. `DOC-PROTOCOL.md` and `DOC-COMPACTION.md` are reserved
    forever, so this case recurs by construction.

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
COMPACTS_RE = re.compile(r"^\*\*Compacts:\*\*[ \t]*(.+)$", re.M)
OWNER_RE = re.compile(r"^\*\*Owner:\*\*\s*(\S+)", re.M)
# `In flux:` answers. `per` is `per file`/`per-file`: several docs on one
# `Compacts:` line whose answers differ, which is the common case once a file
# is paid and struck off. See the header.
FLUX_LEGAL = ("yes", "no", "per")
# Where the `In flux:` block ends: the next task field, or the first section.
# The block matters because rule 4 is about what the block itself names -- a
# path mentioned only on the `Compacts:` line is not the field saying which.
NEXT_FIELD_RE = re.compile(
    r"^(?:\*\*(?:State|Source|Scope|Hardware|Owner|Compacts|Size debt due|"
    r"Must not delete|Depends on|Blocks):\*\*|## )", re.M)


def flux_block(text: str) -> str:
    """The `In flux:` field's own text, field label through to the next field."""
    m = IN_FLUX_RE.search(text)
    if not m:
        return ""
    rest = text[m.start():]
    nxt = NEXT_FIELD_RE.search(rest, 1)
    return rest[: nxt.start()] if nxt else rest


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
        # The `Compacts:` line is DATA, and a struck-off path must be removed
        # rather than annotated in place. Leg 057 struck one through with
        # `~~...~~` plus prose and `check-doc-size.py` stopped recognising the
        # line at all, reporting two filed files as unfiled and failing the
        # whole gate. A bare `~~path~~` does not break that parser today -- it
        # yields a junk path that matches no doc -- which is worse, because it
        # is silent. `study-designer/006` was carrying one on 2026-09-09.
        for m in COMPACTS_RE.finditer(text):
            if "~~" in m.group(1):
                fails.append(
                    f"{rel}\n    `Compacts:` carries a struck-through path: "
                    f"{m.group(1).strip()[:80]}\n    that line is parsed. "
                    f"Delete the paid path from it and say so in the body -- "
                    f"leg 057\n    broke the size gate annotating one in place.")

        flux = IN_FLUX_RE.search(text)
        if flux:
            answer = flux.group(1).lower().strip("*_`.,:-")
            owner = OWNER_RE.search(text)
            owner_req = bool(owner) and owner.group(1).lower().strip(
                "*_`.,") == "required"
            if answer not in FLUX_LEGAL:
                fails.append(
                    f"{rel}\n    `In flux:` answer {answer!r} is not one of "
                    f"{', '.join(FLUX_LEGAL)}\n    `per` is `per file`, for a "
                    f"task whose docs do not share one answer -- see this "
                    f"script's header")
            elif answer == "yes" and tok != "blocked" and not owner_req:
                fails.append(
                    f"{rel}\n    `In flux: yes` but state is {tok!r}\n"
                    f"    every file on the `Compacts:` line is in flux, so "
                    f"nothing here is dispatchable: `.claude/leg.md`. Set "
                    f"`blocked`\n    and name what unparks it -- with a "
                    f"`**Size debt due:**` date, which is what keeps a park "
                    f"from\n    absorbing. If the answer differs per file, say "
                    f"`per file` and name each; if only SOME files\n    are in "
                    f"flux the task stays `open` and its dispatch note says "
                    f"which to leave alone.")
            elif answer == "per":
                block = flux_block(text)
                named = []
                for m in COMPACTS_RE.finditer(text):
                    named += [t.strip().strip("`,~ ") for t in m.group(1).split(",")]
                missing = [q for q in named if q and q not in block]
                if missing:
                    fails.append(
                        f"{rel}\n    `In flux: per file` but the block names no "
                        f"answer for: {', '.join(missing)}\n    a per-file "
                        f"answer that does not say which file is the field "
                        f"drifting from the\n    `Compacts:` line again, which "
                        f"is what tasks/doc/030 found on three of four tasks.")

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
