# 001 — Bump the atlas when HEAD moves, without a session ritual

**State:** done
**Owner's word, 2026-11-10, given directly in his interactive session:** allow model invocation. Drop `disable-model-invocation: true` from the three atlas skills that build or update an atlas, so "update the atlas" said in a session starts one. He accepted the trade-off that the flag is all-or-nothing, so a session may also start one on its own judgement.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — six bumps between 2026-10-05 and 2026-10-08 took 59 lifecycle CLI runs and 14 `--help` lookups, and one of them was finished from Python by hand after reading `update.py`; no bump in the twelve days after; the second-look queue has owed about 1,980 items against 545-570 verdicts since 2026-10-05, and blind readers ran once (11 agents, 2026-10-06)
**Scope:** atlas
**Hardware:** toolchain
**Owner:** no

## What

Since b99d21a (`update: stop only while a translation is behind its source`), `embarch-atlas update <target>` bumps an atlas in one command, and in the field the deterministic part took about 20 s (19 s on 2026-10-06). What is left is that a person or a session has to remember to run it after every commit, and the atlas-* skills cannot be invoked by Claude (`disable-model-invocation: true`, `embarch-atlas/skills/atlas-update/SKILL.md:4`), so a session asked to update followed the skill by hand. Add an opt-in bump on HEAD moves: `embarch-atlas hook install <target>` (offered by `init`) writes `post-commit`, `post-checkout`, `post-merge` and `post-rewrite` hooks that start `update <target>` detached, under a lock, after HEAD has been quiet for a debounce interval (a rebase moves HEAD many times), with a log under the atlas dir. The previous atlas stays current until the new one has joined. A bump that cannot run says why in the MAP's stale line and in `src:` (see atlas-stale-signal): a translation behind its source, a build failure, or a west workspace whose projects are not at the manifest's revisions (on 2026-10-06 a bump failed with "cannot get sha for uncloned project"). Second-look batches are queued, never run by the hook. For the backlog, which `update` deliberately leaves alone (`update.py:199-206` batches only the diff), add `second-look queue --used <usage log> --top N`: batch the unverified facts that sessions' answers actually returned (`find_fact`, `part_card`, `register` hits), so reading effort goes to facts in use; or record a decision that the backlog stays manual. Ask the owner, and record the answer, whether an explicit user request may invoke the atlas-* skills.

## Why now

The bump itself is now cheap. What remains is that someone has to remember to run it, and in the field nobody did for twelve days while the branches moved by about 100 commits.

## Done when

- [x] `hook install` and `hook uninstall` exist; a test on a fixture repo with a fake build command shows one bump after a burst of HEAD moves, a lock that refuses a second concurrent bump, and the previous atlas current until the new one joined.
- [x] A bump that stops or fails leaves its reason where the stale line and `src:` show it.
- [x] A west workspace not at the manifest's revisions stops the bump with that reason before building.
- [x] `second-look queue --used` batches from a fixture usage log, or `decisions.md` records that the backlog stays manual.
- [x] The owner's answer on model invocation of the atlas-* skills is in DESIGN.md.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Result

Shipped on `agent/atlas/001-bump-on-head` (embarch-atlas 67cec65; this branch carries the doc half). The atlas has no `spec.md`/`decisions.md`/`open.md`: its contract is the repo's `DESIGN.md` ("Bumping when HEAD moves", "When `update` stops", "How a session sees the atlas", the layout and the CLI table), plus a short note in `embarch-atlas/design.md` here and `changelog.d/atlas-bump-on-head.added.md`. No `features.d/` row: atlas has no section in the feature inventory.

- **Hooks** (`bump.py`): `hook install <target>... [--debounce S]` writes a marked block into `post-commit`, `post-checkout` (skipped for a file checkout), `post-merge` and `post-rewrite` in the hooks dir git resolves; a hook that is not ours keeps its text and gets the block appended; `hook uninstall` removes the block and deletes a hook that held nothing else. The block writes `bump/moved` and starts `hook run` detached unless `bump/worker.pid` is live. `init` offers it.
- **Worker**: waits until HEAD has been quiet `--debounce` seconds (default 10) and no rebase, merge, cherry-pick, revert or bisect is in progress, then runs `update` per target under the bump lock, logging to `bump/log`, then `status`. `bump/handled` records the last move bumped, so the extra workers a burst starts before the first writes its pid exit with nothing to do (a first test run showed five bumps for five commits without it). It drops `GIT_DIR`-style variables a hook's environment carries.
- **Lock and state**: every `update` takes `bump/update.lock` (exit 3 with the running bump named when held) and records running/ok/stopped/failed and the reason in `bump/state.json`. `project.atlas_state` turns a running, stopped or failed bump to HEAD into a stale reason, so the MAP's `> **Stale:**` line and every `src:` say why; `stale.py` keys its cache on the state file too.
- **Previous atlas current until joined**: an atlas whose bump is running and whose MAP.md is not written yet (`bump.joining`) is neither a `current.json` match (`status` lists it as `joining`) nor the lookups' fallback.
- **West workspace**: `update.workspace_drift` stops a bump before building when a cloned project's HEAD is not its manifest revision (a SHA or tag resolved in its clone; a branch compared with `manifest-rev`) or its clone lacks the revision. An uncloned project is listed, not a stop (a manifest can name projects the build never uses). The manifest compared is the one west reads (the manifest repo's working tree), not the bumped commit's `west.yml`.
- **Second look from use**: `find_fact` and `register` append the record ids they return to `usage.jsonl`, `part_card` the pages its card cites; `second-look queue <atlas> --used <log> [--top N]` batches only the queued facts those answers returned, most used first.
- **Tests** (`tests/test_bump.py`, 8): real git hooks on a fixture repo, five commits in a row are one bump of the last commit (stragglers waited out); the lock refuses a second bump and a second worker; at the moment the new atlas's join starts, `current_atlas` is still the previous one and the MAP line says a bump is running; a stopped and a failed bump each reach the MAP line and `src:`; a fake `west` with a module off its manifest SHA stops the bump before `run_build`, a tag revision passes, an uncloned project is listed; lookups log ids and card pages; `--used` batches from a fixture log. Gate: 739 passed, 3 skipped (no real west workspace), `test_public_guard` ran.
- **Choice made here**: the burst test's target has no Zephyr board (`no_board = true`), so the "build" it runs is the stamp-only build and the join is real; the west path is covered by the drift test's fake `west`. No real west workspace bump was run.
- **Unverified**: a bump on a real west workspace from a hook, and a rebase of many commits (the in-progress check reads `git rev-parse --git-path rebase-merge` and friends, tested only by construction).

## Blocked (history)

One box needs the owner, and no agent can ask him: **may an explicit user request ("update the atlas") invoke the atlas-* skills**, which are `disable-model-invocation: true` today, so a session asked to update follows the skill by hand? His answer goes into DESIGN.md "The skills" (and, if yes, the three SKILL.md frontmatters). The bump on HEAD moves makes the question less pressing but does not answer it.

Unparked by the owner's word above. Shipped on the same branch (embarch-atlas 0fc13a2): `atlas-translate-docs`, `atlas-build` and `atlas-update` no longer carry `disable-model-invocation: true`; DESIGN.md "The skills" and `install.py`'s docstring say a session may invoke any atlas skill, and that the flag being all-or-nothing means it may also do so on its own judgement. Gate re-run: pytest 739 passed, 3 skipped; check-docs, client-names and ownership green on both branches.
