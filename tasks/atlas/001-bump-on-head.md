# 001 — Bump the atlas when HEAD moves, without a session ritual

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — six bumps between 2026-10-05 and 2026-10-08 took 59 lifecycle CLI runs and 14 `--help` lookups, and one of them was finished from Python by hand after reading `update.py`; no bump in the twelve days after; the second-look queue has owed about 1,980 items against 545-570 verdicts since 2026-10-05, and blind readers ran once (11 agents, 2026-10-06)
**Scope:** atlas
**Hardware:** toolchain
**Owner:** no

## What

Since b99d21a (`update: stop only while a translation is behind its source`), `embarch-atlas update <target>` bumps an atlas in one command, and in the field the deterministic part took about 20 s (19 s on 2026-10-06). What is left is that a person or a session has to remember to run it after every commit, and the atlas-* skills cannot be invoked by Claude (`disable-model-invocation: true`, `embarch-atlas/skills/atlas-update/SKILL.md:4`), so a session asked to update followed the skill by hand. Add an opt-in bump on HEAD moves: `embarch-atlas hook install <target>` (offered by `init`) writes `post-commit`, `post-checkout`, `post-merge` and `post-rewrite` hooks that start `update <target>` detached, under a lock, after HEAD has been quiet for a debounce interval (a rebase moves HEAD many times), with a log under the atlas dir. The previous atlas stays current until the new one has joined. A bump that cannot run says why in the MAP's stale line and in `src:` (see atlas-stale-signal): a translation behind its source, a build failure, or a west workspace whose projects are not at the manifest's revisions (on 2026-10-06 a bump failed with "cannot get sha for uncloned project"). Second-look batches are queued, never run by the hook. For the backlog, which `update` deliberately leaves alone (`update.py:199-206` batches only the diff), add `second-look queue --used <usage log> --top N`: batch the unverified facts that sessions' answers actually returned (`find_fact`, `part_card`, `register` hits), so reading effort goes to facts in use; or record a decision that the backlog stays manual. Ask the owner, and record the answer, whether an explicit user request may invoke the atlas-* skills.

## Why now

The bump itself is now cheap. What remains is that someone has to remember to run it, and in the field nobody did for twelve days while the branches moved by about 100 commits.

## Done when

- [ ] `hook install` and `hook uninstall` exist; a test on a fixture repo with a fake build command shows one bump after a burst of HEAD moves, a lock that refuses a second concurrent bump, and the previous atlas current until the new one joined.
- [ ] A bump that stops or fails leaves its reason where the stale line and `src:` show it.
- [ ] A west workspace not at the manifest's revisions stops the bump with that reason before building.
- [ ] `second-look queue --used` batches from a fixture usage log, or `decisions.md` records that the backlog stays manual.
- [ ] The owner's answer on model invocation of the atlas-* skills is in DESIGN.md.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
