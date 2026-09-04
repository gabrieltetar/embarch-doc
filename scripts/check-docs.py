#!/usr/bin/env python3
"""Run the embarch-doc checks as ONE command, and say which failed.

Why a wrapper for something a `for` loop already did: a `for ... done` line has
no command prefix, so no permission rule can ever match it, and an agent that
emits one gets a prompt no allowlist can remove. A background leg that stops on a
prompt is worse than a slow one -- nobody is watching, and it blocks until the
owner happens to look. `embarch-fleet/ops.md` §3 has the shapes to
avoid; this removes the most common of them by making the gate a single
allowlistable invocation.

It is a convenience wrapper, not a new gate: the six checks and what they mean
are unchanged (`DOC-PROTOCOL.md` §5, `embarch-fleet/protocol.md` §10). Every
check still runs even after one fails, because a supervisor wants the whole
picture before deciding whether to block a task, not the first red.

Usage:
  scripts/check-docs.py            run all six, print one line each
  scripts/check-docs.py --quiet    print only failures
Exit status: 0 if all pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# build_changelog is a gate only with --check; it assembles without it.
#
# install.py is the seventh and it checks a different kind of thing: this repo's
# `.claude/`, its four protocol READMEs and the fleet shims in `scripts/` are
# rendered from templates in the embarch-fleet repo, so a hand-edit here is a
# change that the next install silently reverts. It lives in that repo, so it is
# skipped rather than failed when the checkout is absent -- an instance without
# the framework beside it is a broken setup, but it is not a doc defect.
CHECKS = (
    ("check-links.py", []),
    ("check-staleness.py", []),
    ("check-decision-refs.py", []),
    ("check-doc-conventions.py", []),
    ("check-doc-size.py", []),
    ("build_changelog.py", ["--check"]),
    (os.path.join(HERE, "..", "..", "embarch-fleet", "scripts", "install.py"), ["--check"]),
)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args()

    failed = []
    for name, extra in CHECKS:
        path = name if os.path.isabs(name) else os.path.join(HERE, name)
        if not os.path.exists(path):
            if not args.quiet:
                print(f"  SKIP  {os.path.basename(name)} (not present)")
            continue
        r = subprocess.run([sys.executable, path, *extra],
                           capture_output=True, text=True)
        label = os.path.basename(name) + (" " + " ".join(extra) if extra else "")
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
