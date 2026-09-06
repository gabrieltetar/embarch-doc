#!/usr/bin/env python3
"""Run the embarch-doc checks as ONE command, and say which failed.

Why a wrapper for something a `for` loop already did: a `for ... done` line has
no command prefix, so no permission rule can ever match it, and an agent that
emits one gets a prompt no allowlist can remove. A background leg that stops on a
prompt is worse than a slow one -- nobody is watching, and it blocks until the
owner happens to look. `embarch-fleet/ops.md` §3 has the shapes to
avoid; this removes the most common of them by making the gate a single
allowlistable invocation.

It is a convenience wrapper, not a new gate: the checks and what they mean are
unchanged (`DOC-PROTOCOL.md` §5, `embarch-fleet/protocol.md` §10). Every check
still runs even after one fails, because a supervisor wants the whole picture
before deciding whether to block a task, not the first red.

Usage:
  scripts/check-docs.py            run them all, print one line each
  scripts/check-docs.py --quiet    print only failures
Exit status: 0 if all pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# build_changelog and build_features are gates only with --check; they
# assemble without it. Both --check modes validate FRAGMENTS and nothing else.
# build_features has a second, stricter `--check-assembled` that also asserts
# suite/features.md matches them -- deliberately NOT here, because that file is
# refused to every worker by check-ownership.py, so asserting it in the gate
# everyone runs made every feature-shipping branch red (tasks/doc/002). It runs
# in CI on a push to main, and the supervisor's fold assembles.
#
# The last two live in the embarch-fleet repo and are invoked by their framework
# path rather than through their shim, so that both are SKIPPED rather than RED
# when that checkout is absent -- an instance without the framework beside it is
# a broken setup, not a doc defect.
#
# install.py --check asserts a different kind of thing from the rest: this repo's
# `.claude/`, its four protocol READMEs and the fleet shims in `scripts/` are
# rendered from templates in the framework repo, so a hand-edit here is a change
# that the next install silently reverts.
#
# check-client-names.py is the ninth, added 2026-09-05. It runs on ONE repo, this
# one, and the supervisor runs it again per code repo in the merge gate
# (`embarch-fleet/protocol.md` §10) -- 80% of the suite's bytes are in repos that
# never run this wrapper, and the 2026-09-04 leak was mostly on that side. It
# cannot be one pass over the sibling repos, because a worker and a leg run this
# from a worktree where sibling resolution finds other worktrees.
CHECKS = (
    ("check-links.py", []),
    ("check-staleness.py", []),
    ("check-decision-refs.py", []),
    ("check-doc-conventions.py", []),
    ("check-doc-size.py", []),
    ("build_changelog.py", ["--check"]),
    ("build_features.py", ["--check"]),
    (os.path.join(HERE, "..", "..", "embarch-fleet", "scripts", "install.py"),
     ["--check", "--repo", os.path.dirname(HERE)]),
    (os.path.join(HERE, "..", "..", "embarch-fleet", "scripts", "check-client-names.py"),
     ["--repo", os.path.dirname(HERE)]),
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
