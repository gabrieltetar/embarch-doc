# 130 — Fold review fixes into their commits and restack a PR stack with one allowlistable command

**State:** done 2026-10-28
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 20 of 25 auto-mode denials, in 14 sessions, hit rebase, cherry-pick, amend or force-push commands or notes describing them; a 229-line hand-kept fold map (76 calls) was discarded at the re-slice; 97 `fixup!`/`amend!` commits and 46 "folds into" commits; 17 one-off sequence-editor, message-fix and conflict scripts; fold mechanics were 6.7 % of cost and 4.4 active hours
**Scope:** api
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-28 leg

- **Reserve:** `embarch-api/open.md` is 4,674/5,120 B (446 B left), filed against `tasks/api/144` (open, no clock). Its bullet "`serial_log signal=` needs Core's half … until it lands Core refuses it" is **stale**: `core/120` landed Core's half (core decision 101). Delete that bullet in the same edit as anything you add there. If your work still leaves the file in reserve, `tasks/api/144` already records the debt; do not file another.
- **Tree identity** in `stack fold` does not need `build --each --same-tree-as` (`tasks/api/127`, toolchain-gated and not built): compare `<tip>^{tree}` before and after with git directly, and say so in the decision.
- New decisions go in a new `decisions/<topic>.md` rather than a file near its cap; check `scripts/check-doc-size.py --pressure` before you choose.

## What

Add an `embarch-api stack` command family. It is git-only, and the owner may move it to its own crate. **`stack plan [<base>]`** looks at each uncommitted hunk and each commit above the branch's last reviewed point, finds the commit in `<base>..HEAD` that last touched those lines, and emits `fixup!` commits. Hunks it cannot place (new files, or lines no commit in range owns) go in a generated plan file, which replaces the hand-kept fold map. Commit-message corrections are queued as `amend!` commits or as entries in a curation file. **`stack fold`** backs up every branch it will move (`backup/<branch>-<sha>`), autosquashes non-interactively, and applies the queued message corrections. It refuses on a dirty tree. On a conflict it stops, puts the branch back at its backup and names the commit and files. It checks that the folded tip's tree equals the pre-fold tip using `build --each --same-tree-as`. It never pushes. **`stack restack <bottom>..<top>`** rebases each PR branch onto the new tip of the one below with `--update-refs`. When the bottom PR has landed by rebase merge, it drops the landed commits by patch-id. It then pushes all the branches in one `git push --atomic` with `--force-with-lease=<branch>:<expected sha>` for each, and aborts if another session moved any ref. It is one command with its own safeguards: backups, leases and a tree-identity check. The engineer can therefore allow just this command in auto mode, a narrower permission than the `git push --force-with-lease *` and `git rebase *` rules they had to add in the field.

## Why now

Folding was fast whenever it was allowed: five measured folds took 14–32 min each. The cost was the deferral. Rewrites were refused, fixes piled up as dozens of additive commits with a hand-kept map of where each belongs, and the map was thrown away when the history was re-sliced from the final tree. One session also found its branch rebased and pushed under it by another session.

## Done when

- [x] `stack plan` places hunks on a fixture repo with at least three commits, lists the hunks it cannot place, and writes the plan file.
- [x] `stack fold` creates the backups, folds `fixup!` and `amend!` commits, applies a curation file, proves tree identity, and never pushes.
- [x] `stack restack` on a 4-branch fixture stack updates every ref and pushes atomically with leases to a local bare remote. A remote ref moved by someone else aborts the whole push with nothing sent.
- [x] After a rebase merge of the bottom branch, `stack restack --onto origin/main` drops the landed commits by patch-id.
- [x] The single permission rule (`Bash(embarch-api stack:*)`) is documented in `embarch-api/interfaces/stack.md`; the user guide is suite-owned and in reserve, so `status.d/api-stack-user-guide.md` asks the supervisor to fold one paragraph into §6.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
