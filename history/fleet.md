# fleet: history

**Status:** active, 2026-09-05. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB — older windows roll into [archive/](archive/).

## 2026-09

### Added
- check-client-names.py: the doc gate and the per-repo merge gate refuse a client's name in a file, a path or a commit message, from a denylist outside every repo. It never prints the match.
- check-fleet-doc-size.py caps the framework repo's own docs as a ratchet, run by deploy.py. Nothing covered that corpus before, so protocol.md and ops.md had drifted to 32 KB unnoticed.
- fold-commit.py deletes a unit's pushed agent/* branches once git cherry proves them on origin/main. Five had accumulated from one leg, and they silently defeated a history rewrite.

### Changed
- The framework README stops telling you to wire `install.py --check` into CI, which cannot see the framework repo; the local check-docs.py gate every fold runs is the guard.
- The reviewer is collected before its log entry is written, not predicted; the entry's seven `**Field:**` markers are enforced by `fold-commit.py` before it stages anything.
- fold-day.py --roll keeps the two newest days and archives the rest; the 40 KB byte line is gone. Two byte lines were written for this log and neither was reachable.

### Fixed
- Recovery reclaims a claim by the worktree's state, not the branch's commit count: a killed worker's finished work lives in an uncommitted tree.
- The daily fold's ledger is bounded so a correct fold can pass it: reviewer lines are a floor, and only debt lines naming a board must be carried.
- `fold-commit.py --check` resolves a merge SHA by asking the suite's repos, not by reading the word before it as a repo name; it reported 17 of 28 healthy log states as broken.

### Decided
- No advisory warn band under the doc-size reserve: at 80% it names 29 files against the 2 in reserve. open.md carries what would un-defer it — a cap that actually misfiles or loses work.
- No blocked-repeat detector yet: eleven legs produced zero blocked units, so it would calibrate against nothing. risks.md names the trigger — a second unit blocked by a failure already logged.
## 2026-09

### Added
- `embarch-fleet` gets a suite directory ([spec](../embarch-fleet/spec.md)); `fleet` is refused as a worker scope so the layout does not grant one its own rules.
- `fold-day.py` folds a log day by ledger-checked splice, and an `embarch-log-folder` subagent does it, so a leg pays two lines instead of ~35 K tokens.

### Fixed
- `check-ownership.py` derives its own base — the furthest-forward merge-base — ending three legs of false reds from a stale or unpushed `main`.
