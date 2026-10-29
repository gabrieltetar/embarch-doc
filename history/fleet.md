# fleet: history

**Status:** active, 2026-09-05. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-10

### Added
- A leg takes a lock before step 0 and waits while another leg holds it, so a second leg can no longer run recovery over a live one.
- The doc gate fails a `claimed` line `queue-status.py` cannot read, by asking that script, and the queue listing names each unreadable claim.
- The merge gate names its first Python repo: `embarch-atlas` runs `pytest` in a venv of its own, never the main checkout's, whose editable install tests `main`.
- `/review-loop`: a pre-PR reviewer loop with delta rounds after the first, one context pack, a findings ledger outside `/tmp`, and a stop rule after two rounds clean of high and medium.
- check-dispatch.py --created proves each worker worktree was made where asked, on its branch, with every Cargo path-dep resolving; a relative path is refused.

### Changed
- A reviewer writes its verdict to a file as its last act, so a lost completion notification no longer turns a clean review into `skipped`.
- A shared crate is gated under every feature set its consumers build it with, read from their manifests, not only defaults and `--all-features`.
- A spread-only refill is skipped while no source a sweep reads has changed since the last spread sweep that filed nothing; `--refill-owed` says when only spread fired.
- The pre-push hook scans every commit a push sends — messages, paths, blobs — not just the tree, and the first leg after midnight runs `check-client-names.py --suite --history`.
- Workers verify a sibling repo against its main checkout; the Windows `source/repos` copies are rsync targets with no `.git`, and the worker definition now says so.
- `.claude/leg.md` quotes the claim line at the claim step; a leg number or window `ts` goes after the timestamp, never in place of the branch.
- leg.md: never pipe `fold-commit.py` — a pipe hid its refusal from a chained push and `leg-fold` tick twice (`tasks/doc/086`).

### Fixed
- A fold may stage `reversals/`, the DOC-COMPACTION split of `embarch-decision-reversals.md` that holds the rows (`tasks/doc/073`).
- `check-ownership.py` takes its scope list from `fleet.toml` when run outside embarch-doc, and names the missing `--code-repo` instead of calling a real scope unknown (`tasks/doc/036`).
- `fleet-hardware.py --refresh` no longer crashes on an unattached DUT, and the plain form says when the last refresh failed instead of only that the buffer is stale.
- `fold-commit.py` deletes a landed unit's local `agent/*` branches with its pushed ones, so `git worktree remove` no longer leaks one per unit (`tasks/doc/066`).
- `fold-commit.py` prunes a landed `agent/*` branch by its content, so one landed through a conflicted cherry-pick or rebase is no longer stranded (`tasks/doc/061`, `080`).
- `fold-commit.py` retires a finished task file the fold itself edited (`git rm -f`), instead of failing after the log commit (`tasks/doc/050`).
- `fold-commit.py` stages the instance half before committing the log, and re-running a fold that died between its two commits finishes it (`tasks/doc/075`, `082`).
- `queue-status.py` lists open `suite` tasks on their own line and keeps them out of `dispatchable`, the number that sizes a wave of workers.
- `queue-status.py` reads `Hardware:`, `Scope:` and `Owner:` past Markdown emphasis; a bolded `**none**` no longer gates a task as `required`.
- `queue-status.py` reads `fleet.toml`'s instance when the cwd has no `tasks/`, and exits 2 naming the paths it tried instead of reporting an empty queue.
- leg.md gives the worker-worktree command with an absolute target and names the git -C trap that put twelve worktrees inside their own repos.
- leg.md says where a remaining branch is rebased: its own unit worktree or a cherry-pick in the leg worktree, never a repo checkout.
- leg.md's worktree link table lists every sibling the suite reads: umbrella gains api, core gains smp, outpost and dev-bench get their non-cargo readers.

### Removed
- check-dispatch.py drops the classifier-blocked --allow-existing; its refusal names a recovery that needs no flag: commit, push, remove, re-dispatch.
## 2026-09

### Added
- A task can be `Hardware: toolchain` — host-side but needing a toolchain no worktree carries; the supervisor runs it in the main checkout, serialized.
- `fleet-hardware.py` buffers the whole bench topology — measured and stated fields tagged apart — so selecting bench work costs no hardware attach.
- check-client-names.py: the doc gate and the per-repo merge gate refuse a client's name in a file, a path or a commit message, from a denylist outside every repo. It never prints the match.
- check-fleet-doc-size.py caps the framework repo's own docs as a ratchet, run by deploy.py. Nothing covered that corpus before, so protocol.md and ops.md had drifted to 32 KB unnoticed.
- fold-commit.py deletes a unit's pushed agent/* branches once git cherry proves them on origin/main. Five had accumulated from one leg, and they silently defeated a history rewrite.
- `embarch-fleet` gets a suite directory ([spec](../embarch-fleet/spec.md)); `fleet` is refused as a worker scope so the layout does not grant one its own rules.
- `fold-day.py` folds a log day by ledger-checked splice, and an `embarch-log-folder` subagent does it, so a leg pays two lines instead of ~35 K tokens.

### Changed
- - The fleet repo's risk register split by mission into [risks-authority.md](../../embarch-fleet/risks-authority.md), its stepped ratchet ported, and every remaining seam stated in advance.
- The worker contract forbids `cargo fmt`, and says the cargo gate reaches only the packages it selects; the Windows build's two failure modes are both recorded.
- The framework README stops telling you to wire `install.py --check` into CI, which cannot see the framework repo; the local check-docs.py gate every fold runs is the guard.
- The reviewer is collected before its log entry is written, not predicted; the entry's seven `**Field:**` markers are enforced by `fold-commit.py` before it stages anything.
- fold-day.py --roll keeps the two newest days and archives the rest; the 40 KB byte line is gone. Two byte lines were written for this log and neither was reachable.

### Fixed
- A 429 whose own `resetsAt` has passed no longer HOLDs the fleet; the lookback is UTC-correct and the verdict reads parsed fields, not a substring.
- The client-name check reads what a file encodes, not only what it spells, and `fold-commit.py` and `deploy.py` now scan the framework repo nothing else did.
- Recovery reclaims a claim by the worktree's state, not the branch's commit count: a killed worker's finished work lives in an uncommitted tree.
- The daily fold's ledger is bounded so a correct fold can pass it: reviewer lines are a floor, and only debt lines naming a board must be carried.
- `fold-commit.py --check` resolves a merge SHA by asking the suite's repos, not by reading the word before it as a repo name; it reported 17 of 28 healthy log states as broken.
- `check-ownership.py` derives its own base — the furthest-forward merge-base — ending three legs of false reds from a stale or unpushed `main`.

### Decided
- No advisory warn band under the doc-size reserve: at 80% it names 29 files against the 2 in reserve. open.md carries what would un-defer it — a cap that actually misfiles or loses work.
- No blocked-repeat detector yet: eleven legs produced zero blocked units, so it would calibrate against nothing. risks.md names the trigger — a second unit blocked by a failure already logged.
