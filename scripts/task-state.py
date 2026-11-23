#!/usr/bin/env python3
"""Move one task file through the transitions a worker or a leg owns.

`check-task-state.py` reads a task's `**State:**` line back and fails what no
reader can parse; nothing wrote a correct one. Workers rewrote the line with a
one-off `sed` or an inline script at every claim and every close, six scripts
for three tasks in one session (EMB-151). This writes the line, and it parses
the old one with `check-task-state.py`'s own patterns, so the writer and the
checker share one grammar.

    scripts/task-state.py claim tasks/api/174-slug.md [--branch B] [--at "yyyy-mm-dd HH:MM"] [--note PROSE]
    scripts/task-state.py close tasks/api/174-slug.md done --why PROSE
    scripts/task-state.py close tasks/api/174-slug.md blocked --why PROSE [--unparks CONDITION]

**claim** writes `claimed by agent/<scope>/<NNN-slug>, <yyyy-mm-dd HH:MM>`, the
prefix `queue-status.py` parses, then ` — <note>` if given. The branch defaults
to the one the path names. A task must be `open` or `blocked` to be claimed, and
a park's `**Unparks when:**` field goes in the same edit, since a claimed task is
no longer parked.

**close** writes `done — <why>` or `blocked — <why>`. A `blocked` task needs an
`**Unparks when:**` field (`check-task-state.py` rule 7): `--unparks` adds one
under the state line, or replaces the one there; with neither, it refuses.

Exit status: 0 written, 1 refused (nothing written), 2 not a task file.
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("check_task_state", HERE / "check-task-state.py")
cts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cts)

TASK_PATH_RE = re.compile(r"(?:^|/)tasks/([a-z][a-z-]*)/(\d{3}-[^/]+)\.md$")
CLAIMABLE = ("open", "blocked")
CLOSES = ("done", "blocked")
DASH = " — "


def branch_of(path: Path) -> str | None:
    m = TASK_PATH_RE.search(path.resolve().as_posix())
    return f"agent/{m.group(1)}/{m.group(2)}" if m else None


def state_line(text: str) -> re.Match:
    """The one `**State:**` line every reader takes, outside fenced examples."""
    fenced = [(f.start(), f.end()) for f in cts.FENCE_RE.finditer(text)]
    for m in cts.STATE_RE.finditer(text):
        if not any(a <= m.start() < b for a, b in fenced):
            return m
    raise Refused("no `**State:**` line outside a fenced example")


def drop_unparks(text: str) -> str:
    block = cts.unpark_block(text)
    if block is None:
        return text
    at = text.index(block)
    end = at + len(block)
    if text[end:end + 2] == "\n\n":
        end += 1
    elif text[end:end + 1] == "\n":
        end += 1
    return text[:at] + text[end:]


def set_state(text: str, value: str) -> str:
    m = state_line(text)
    return text[:m.start()] + f"**State:** {value}" + text[m.end():]


def claim(text: str, branch: str, at: str, note: str | None) -> str:
    tok = cts.token(state_line(text).group(1))
    if tok not in CLAIMABLE:
        raise Refused(f"it is `{tok}`; only an `open` or `blocked` task is claimed")
    value = f"claimed by {branch}, {at}" + (f"{DASH}{note.strip()}" if note else "")
    return drop_unparks(set_state(text, value))


def close(text: str, state: str, why: str, unparks: str | None) -> str:
    tok = cts.token(state_line(text).group(1))
    if tok == "done":
        raise Refused("it is already `done`")
    out = set_state(text, f"{state}{DASH}{why.strip()}")
    if state != "blocked":
        if unparks:
            raise Refused("`--unparks` belongs to a `blocked` close")
        return drop_unparks(out)
    if unparks:
        out = drop_unparks(out)
        m = state_line(out)
        out = out[:m.end()] + f"\n\n**Unparks when:** {unparks.strip()}" + out[m.end():]
    elif cts.unpark_block(out) is None:
        raise Refused("a `blocked` task names what returns it to `open`: give `--unparks`")
    return out


class Refused(Exception):
    pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("claim")
    p.add_argument("path")
    p.add_argument("--branch", help="default: agent/<scope>/<NNN-slug>, from the path")
    p.add_argument("--at", help="yyyy-mm-dd HH:MM, default now")
    p.add_argument("--note", help="prose after the time")
    p = sub.add_parser("close")
    p.add_argument("path")
    p.add_argument("state", choices=CLOSES)
    p.add_argument("--why", required=True, help="prose after the state")
    p.add_argument("--unparks", help="what returns a blocked task to open")
    args = ap.parse_args()

    path = Path(args.path)
    if not path.is_file() or not TASK_PATH_RE.search(path.resolve().as_posix()):
        print(f"not a task file (tasks/<scope>/<NNN-slug>.md): {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    try:
        if args.cmd == "claim":
            at = args.at or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", at):
                raise Refused(f"--at {at!r} is not yyyy-mm-dd HH:MM")
            new = claim(text, args.branch or branch_of(path), at, args.note)
        else:
            new = close(text, args.state, args.why, args.unparks)
    except Refused as e:
        print(f"{path}: nothing written; {e}", file=sys.stderr)
        return 1
    path.write_text(new, encoding="utf-8")
    print(f"{path}: **State:** {cts.STATE_RE.search(new).group(1)[:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
