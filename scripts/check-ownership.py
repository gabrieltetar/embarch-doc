#!/usr/bin/env python3
"""Enforce embarch-parallel-agents.md §3's ownership map on a worker's branch.

§3 is the whole conflict-avoidance mechanism -- branches are only the backstop.
But it was written as a table in prose, and nothing checked it: a worker that
edited embarch.md's status table would sail through every other gate, because
`check-staleness.py` only flags a row that *disagrees* with a sub-project doc,
and a worker's edit is plausible by construction. Then two workers touch the
same table in one batch and the supervisor is merging two intents it never held
-- exactly what §9 exists to prevent.

So: given the sub-project a branch belongs to, verify every changed path is one
that sub-project's worker is allowed to write.

In embarch-doc a worker may write:
    embarch-<scope>/**        its own sub-project's four files
    changelog.d/<scope>-*     its own history fragment
    status.d/<scope>-*        its request to change a shared suite-level doc
    tasks/<scope>/**          its own task file
and nothing else -- notably not embarch.md, embarch-features.md,
embarch-roadmap.md, embarch-decision-reversals.md, embarch-glossary.md,
embarch-user-guide.md, DOC-PROTOCOL.md, DOC-COMPACTION.md,
embarch-parallel-agents.md, embarch-dev-workflow.md, or scripts/.

In a code repo the worker owns the whole tree, so the only question this can
answer is whether it is in the right repo at all; pass --code-repo to assert
that and skip the path rules.

The `suite` scope is not a worker scope: a cross-repo change is the supervisor's
(§8), and this refuses it outright rather than granting it everything.

Usage:
  scripts/check-ownership.py --scope api                     # HEAD vs merge-base with main
  scripts/check-ownership.py --scope api --base origin/main
  git diff --name-only main...HEAD | scripts/check-ownership.py --scope api --stdin
  scripts/check-ownership.py --scope api --code-repo         # in a code repo
Exit status: 0 if every changed path is owned, 1 otherwise.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

# Paths a worker for <scope> may write in embarch-doc, as prefix rules.
def allowed(path: str, scope: str) -> bool:
    return (
        path.startswith(f"embarch-{scope}/")
        or path.startswith(f"tasks/{scope}/")
        or (path.startswith("changelog.d/") and _frag_scope(path, "changelog.d/") == scope)
        or (path.startswith("status.d/") and _frag_scope(path, "status.d/") == scope)
    )


def _frag_scope(path: str, prefix: str) -> str | None:
    """A fragment is <scope>-<slug>.<...>.md; the scope is the longest known
    prefix, so `dev-bench-foo` resolves to `dev-bench`, not `dev`. Mirrors
    build_changelog.py's own rule rather than inventing a second one."""
    name = path[len(prefix):]
    if "/" in name or name == "README.md":
        return None
    for s in sorted(KNOWN_SCOPES, key=len, reverse=True):
        if name.startswith(s + "-"):
            return s
    return None


def known_scopes(repo_root: str) -> set[str]:
    out = subprocess.run(["git", "-C", repo_root, "ls-tree", "--name-only", "HEAD"],
                         capture_output=True, text=True).stdout.split()
    return {d.replace("embarch-", "") for d in out if d.startswith("embarch-") and "." not in d} | {"doc", "suite"}


def changed_paths(base: str | None, repo_root: str) -> list[str]:
    if base is None:
        for cand in ("origin/main", "main"):
            r = subprocess.run(["git", "-C", repo_root, "rev-parse", "--verify", "-q", cand],
                               capture_output=True, text=True)
            if r.returncode == 0:
                base = cand
                break
    if base is None:
        print("cannot find a base ref (tried origin/main, main); pass --base", file=sys.stderr)
        sys.exit(2)
    r = subprocess.run(["git", "-C", repo_root, "diff", "--name-only", f"{base}...HEAD"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr.strip(), file=sys.stderr)
        sys.exit(2)
    return [p for p in r.stdout.split("\n") if p.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, help="sub-project, without the embarch- prefix")
    ap.add_argument("--base", help="ref to diff against (default: origin/main, else main)")
    ap.add_argument("--repo", default=".", help="repo root (default: cwd)")
    ap.add_argument("--stdin", action="store_true", help="read changed paths from stdin instead of git")
    ap.add_argument("--code-repo", action="store_true",
                    help="this is the worker's own code repo, where it owns the whole tree")
    args = ap.parse_args()

    global KNOWN_SCOPES
    KNOWN_SCOPES = known_scopes(args.repo)

    if args.scope == "suite":
        print("REFUSED: `suite` is not a worker scope -- a cross-repo change is the")
        print("supervisor's to execute in one sequenced pass (embarch-parallel-agents.md §8).")
        return 1
    if args.scope not in KNOWN_SCOPES:
        print(f"unknown scope '{args.scope}' (known: {', '.join(sorted(KNOWN_SCOPES))})")
        return 1

    paths = ([p.strip() for p in sys.stdin.read().split("\n") if p.strip()]
             if args.stdin else changed_paths(args.base, args.repo))

    if args.code_repo:
        print(f"OK: code repo, worker for '{args.scope}' owns the whole tree "
              f"({len(paths)} path(s) changed, not path-checked).")
        return 0

    bad = [p for p in paths if not allowed(p, args.scope)]
    if bad:
        print(f"{len(bad)} path(s) outside what an '{args.scope}' worker may write "
              f"(embarch-parallel-agents.md §3):\n")
        for p in bad:
            hint = ""
            if p in ("embarch.md", "embarch-features.md", "embarch-roadmap.md",
                     "embarch-decision-reversals.md", "embarch-glossary.md",
                     "embarch-user-guide.md"):
                hint = "  <- drop a status.d/ fragment instead (§9)"
            elif p.startswith("scripts/") or p.startswith("DOC-"):
                hint = "  <- supervisor or owner only"
            elif p.startswith("embarch-"):
                hint = "  <- another sub-project's docs"
            print(f"  {p}{hint}")
        print(f"\nAllowed for '{args.scope}': embarch-{args.scope}/**, tasks/{args.scope}/**, "
              f"changelog.d/{args.scope}-*, status.d/{args.scope}-*")
        return 1

    print(f"OK: all {len(paths)} changed path(s) owned by the '{args.scope}' worker.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
