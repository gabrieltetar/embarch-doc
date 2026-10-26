# 050 — The client-name check scans what a push sends: every new commit message, and every blob in history

**State:** open
**Source:** a full-history run of `check-client-names.py` (`--base <root commit>`) across all twelve repos on 2026-10-20. Five commit messages on public `origin/main` carried denylisted names (embarch-api, embarch-doc, embarch-dev-bench, embarch-ui twice; dated 2026-09-19 to 2026-10-14), and so did one public blob in embarch-fleet's history. Every gate run had reported all of them clean. The owner had the five histories rewritten and force-pushed the same day: 685 commits on `main` got new hashes, and the citations were repointed (embarch-doc 0f68533a, embarch-fleet ffc851f).
**Scope:** suite
**Hardware:** none
**Owner:** required — every path it must write is in `embarch-fleet` (`scripts/check-client-names.py`, `scripts/install-hooks.py` and the hook it installs, `decisions.md`), which `check-ownership.py --supervisor` reserves to the owner. Set on filing by the 2026-10-25 leg; the drop said `no`.

## What

The pre-push hook (`~/.git-hooks-personal/pre-push.embarch-impl:58-59`, installed by `embarch-fleet/scripts/install-hooks.py`) runs `check-client-names.py --repo <root>` with no `--base`. The script then scans commit messages in `<main or origin/main>..HEAD` (`embarch-fleet/scripts/check-client-names.py:288-294`). The suite commits straight to `main` (`embarch-doc/embarch-dev-workflow.md` §6), so on `main` that range is empty and no commit message is ever scanned, by the hook or by the gate. The tree scan reads only the current tree, so a name that a later commit removed from a file stays in pushed history unseen. When done, the hook reads git's pre-push stdin (`<local ref> <local sha> <remote ref> <remote sha>`) and scans every commit the push sends, `<remote sha>..<local sha>`, or the whole history of `<local sha>` when the remote ref is new. It scans each commit's message and each blob that commit adds or changes, with the same decoders the tree scan uses. The gate keeps its tree scan and adds `--history`, which scans every reachable commit's message and blobs. The supervisor runs `--history` once per day and before it creates any new public repo.

## Why now

The check exists because of the 2026-09-04 scrub, and every gate since then reported each repo clean while five commit messages carrying names went out on public `main`. The most recent one, a dev-bench commit message on 2026-10-14, named the field project. The 2026-10-20 rewrite removed them, and nothing stops the next one.

## Done when

- [ ] The pre-push hook scans `<remote sha>..<local sha>` for messages and added or changed blobs; a fixture repo test pushes a commit whose message names a test-denylist entry and is refused, on `main` and on a branch.
- [ ] A push of a new branch or a new repo scans its whole history.
- [ ] `check-client-names.py --history` scans every reachable commit's message and blobs; a fixture test finds a name in a message and in a blob that a later commit removed, and all twelve repos pass it today.
- [ ] The supervisor's daily phase and the new-repo checklist run `--history`.
- [ ] `embarch-fleet/decisions.md` records the 2026-10-20 rewrite (five repos, force-pushed `main`, citations repointed). It also records whether GitHub Support was asked to purge the unreachable old commits, which GitHub keeps reachable by SHA until it collects them.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
