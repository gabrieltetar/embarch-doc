# embarch-api: `stack`

**Status:** active, 2026-10-28.

Truth for the `stack` subcommand family. Why: [decisions/stack.md](../decisions/stack.md) 96. CLI only; git only; no config, no Core.

| Command | Does | Never |
|---|---|---|
| `stack plan [<base>] [--since <rev>] [--repo <dir>] [--plan-file <path>] [--dry-run]` | one `fixup! <sha>` per target commit for every hunk it can attribute; the rest stays in the tree and goes in the plan file | touch a hunk it cannot place |
| `stack fold [<base>] [--curation <file>] [--repo <dir>]` | back up, autosquash `fixup!`/`amend!`, apply curation, prove tree identity | push; run on a dirty tree |
| `stack restack <bottom>..<top> [--onto <ref>] [--remote <r>] [--no-push]` | rebase each branch onto the new tip below with `--update-refs`, push all in one `--atomic` with a lease each | push if any ref moved; push a landed branch |

`--json` output carries `success`, and per command `placed`/`unplaced`, `backups`, `tree`, `branches`, `landed`, `pushed`. Curation file: `<commit> | <new subject>` per line, `#` comments. Backups: `refs/backup/<branch>-<12 sha>`. On a conflict `fold` and `restack` put every branch back at its backup and name the commit and files.

**The one permission rule.** Allow the family in auto mode with a single prefix rule, `Bash(embarch-api stack:*)`, instead of `git rebase *`, `git cherry-pick *`, `git commit --amend *` and `git push --force-with-lease *`. The rule is narrower than those: every history rewrite it performs is preceded by a backup, `fold` and `restack` refuse a dirty tree, tree identity is proved, and the push is atomic with a lease per branch. It is the engineer's setting; nothing here edits it.
