#!/usr/bin/env python3
"""Run the six embarch-doc checks as ONE command, and say which failed.

Why a wrapper for something a `for` loop already did: a `for ... done` line has
no command prefix, so no permission rule can ever match it, and an agent that
emits one gets a prompt no allowlist can remove. A background leg that stops on a
prompt is worse than a slow one -- nobody is watching, and it blocks until the
owner happens to look. `embarch-parallel-agents-ops.md` §3 has the shapes to
avoid; this removes the most common of them by making the gate a single
allowlistable invocation.

It is a convenience wrapper, not a new gate: the six checks and what they mean
are unchanged (`DOC-PROTOCOL.md` §5, `embarch-parallel-agents.md` §10). Every
check still runs even after one fails, because a supervisor wants the whole
picture before deciding whether to block a task, not the first red.

Usage:
  scripts/check-docs.py            run all six, print one line each
  scripts/check-docs.py --quiet    print only failures
Exit status: 0 if all six pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# build_changelog is a gate only with --check; it assembles without it.
CHECKS = (
    ("check-links.py", []),
    ("check-staleness.py", []),
    ("check-decision-refs.py", []),
    ("check-doc-conventions.py", []),
    ("check-doc-size.py", []),
    ("build_changelog.py", ["--check"]),
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args()

    failed = []
    for name, extra in CHECKS:
        r = subprocess.run([sys.executable, os.path.join(HERE, name), *extra],
                           capture_output=True, text=True)
        label = name + (" " + " ".join(extra) if extra else "")
        if r.returncode == 0:
            if not args.quiet:
                print(f"  PASS  {label}")
        else:
            failed.append(label)
            print(f"  RED   {label}")
            out = (r.stdout + r.stderr).strip()
            for line in out.splitlines()[-12:]:
                print(f"        {line}")

    if failed:
        print(f"\n{len(failed)} of {len(CHECKS)} checks RED: {', '.join(failed)}")
        return 1
    if not args.quiet:
        print(f"\nall {len(CHECKS)} checks green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
