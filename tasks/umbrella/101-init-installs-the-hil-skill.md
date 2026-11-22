# 101 — `embarch init` installs the `embarch-hil` skill beside the MCP server

**State:** open
**Source:** `embarch-api/open.md`: "The `embarch-hil` skill is not installed anywhere. It ships in this repo (`skills/embarch-hil/`), but copying it into a firmware repo is `embarch-umbrella`'s (`embarch init`, `embarch-hil-proposal.md`'s table)." The proposal's `embarch-umbrella` row: "`embarch init` installs the `embarch-hil` skill beside the MCP server". `embarch-api` decision 108 (`decisions/guide.md`) for the skill and the guide it points at.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch init` registers the MCP server in a firmware repo; it now also installs the `embarch-hil` skill there, so an agent in that repo finds the pointer to `embarch-api guide hil` without an `embarch-doc` checkout. `--uninstall` removes it, `--dry-run` prints it, and the skill is excluded locally like the rest of what `init` writes (decision 12: committing the integration for a team is a step `init` does not take).

## Why now

`tasks/api/163` shipped the skill and the guide command on 2026-11-20, and nothing puts the skill where an agent reads it; until something does, the guide is reachable only by an agent that already knows the command.

## Dispatch notes

- **Where the skill's text comes from is this unit's decision**, and it has a cost either way: a copy pinned into `embarch-umbrella` at build time drifts from `embarch-api`'s unless something checks it; asking the located `embarch-api` binary at `init` time couples `init` to an `embarch-api` new enough to answer. `embarch-api` decision 108 made the same choice for the guide; read it. You may not change `embarch-api`: if the cleanest route needs something from it, say so in a `## Finding` and build the other route.
- **Where a skill lives for the agent CLI** is a fact to read off the CLI's own documentation or config, not to assume; say which you relied on, and mark it `[assumed]` if you could not confirm it.
- **The guide it points at is a skeleton** until `suite/hil-guide.md` (plan unit M1.13) exists; installing the pointer now is still right, and `doctor` need not check the guide's content.
- **`embarch-umbrella/spec.md` is in reserve: 9,147 of 10,240 B, 1,093 B left**, and its compaction, `tasks/umbrella/099`, is parked on `In flux: yes` for the release paragraph. That park does not cover you: if this unit adds to `spec.md`, **compact it as part of this unit** by moving reference text verbatim into `spec/` with a link left behind, leaving the release paragraph alone, until `check-doc-size.py --pressure` no longer lists it. Carry `umbrella/099`'s **Must not delete**: the "What a release carries" paragraph's statement that nothing has run on a tag until the owner tags one.
- Decisions near their size limit: `prune-policy` #26 (19 B), `deploy` #32 (29 B), `mirrors` #20 (32 B), `probe-vendors` #49 (140 B), `sticky-host` #48 (186 B), `budgets` #44 (200 B).
- Out of scope: the guide's content (M1.13), and `setup` (machine-wide; the skill is per repo).

## Done when

- [ ] `embarch init` in a scratch repo installs the skill, `--uninstall` removes it, and `--dry-run` names it without writing (tests, in a temporary directory, never a real firmware repo).
- [ ] The installed skill's text matches what `embarch-api` ships, by whatever route the decision picks, and a test fails if it drifts.
- [ ] `spec.md`, `decisions/` updated; `changelog.d/` fragment dropped; the closing note says what `embarch-api/open.md`'s line should now read, and the supervisor amends it at the fold.
- [ ] Gate green (`../../embarch-fleet/gate.md`; `check-ownership.py --scope umbrella` on both branches).
