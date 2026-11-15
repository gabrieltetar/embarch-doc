# Atlas notes: the firmware plane

**Status:** draft, 2026-11-15.

## Today

**Structural, commit-pinned and current.** Each atlas is built from a worktree at its commit; `config`, `dt_node`, `code`, `states`, `footprint` and `stacks` answer from that build or one the caller names; the hook bumps the atlas when HEAD moves, and the code index re-reads only files whose content changed (`embarch-atlas` repo, `DESIGN.md`, "Query surface", "Caching", "Bumping when HEAD moves"). Nothing in it says what the firmware *does*.

## Module cards

**A card per module says what the firmware does**: what the module does, its states, the interfaces it exposes, the requirements and design claims it serves, and why it is the way it is, with commit and PR cites. A module is what `graph.json` already calls one: `apps/<app>/**` (app), `lib/<name>` (middleware), a driver's directory; kernel, arch and HAL code are not modules (same doc, "The whole-atlas graph").

## Range replay

**On each atlas update, every module whose files changed since the previous atlas gets one LLM read**: the diff over that range, plus the commit messages and PRs in it. Unchanged modules keep their card.

- **The commits are attached for free**: `git log <previous>..<new> -- <module paths>`. The PRs come from the desk's index, whose PR rows carry their branch and issue keys ([embarch-desk routes](../../embarch-desk/interfaces/chat-routes.md)).
- **Cost scales with what changed, not with the number of commits.** Five commits to one module are one read.
- **A rebase or a branch switch is just another range**: the previous atlas's commit to the new one, or, when one is not an ancestor of the other, the difference between the two trees.

Chosen over replaying each commit in order, which the owner proposed and weighed: it keeps every intermediate step but costs one read per commit, reads states that no longer exist (fixups, reverts), and has no line of history to follow across a rebase. **What per-commit replay offered that is worth keeping is the why, and the attached commit messages keep it.**

## Open

- **"On update" against "on demand".** LLM work runs only on demand, in a session ([10](10-running-cost.md)), and the hook's bump runs none. Recommended: the bump marks each changed module's card as behind and attaches the range's commits; the card is rewritten when a session runs `/atlas-update` or looks the module up.
- **The freeze key.** Recommended: the module's files' content hashes and the procedure version, as a reference-manual unit is keyed, so two branches with the same module content share one card.
- **The first atlas.** Range replay from nothing writes a card for every module; its cost on a real firmware repo is not measured.
- **The card's fields and budget.** Recommended: at most 1.5K tokens, as a part card is.
- **A `module` lookup**, and `code` pointing at a symbol's card.
- **Out-of-tree boards and drivers that live outside the module rules above.** Not looked at.
