# 050 — The client-name check scans what a push sends: every new commit message, and every blob in history

**State:** blocked — built (fleet `e1565b7`), two boxes wait on the owner: `embarch-dev-bench` history fails `--history`, and the GitHub Support purge is unrecorded; see `## Blocked`
**Source:** a full-history run of `check-client-names.py` (`--base <root commit>`) across all twelve repos on 2026-10-20. Five commit messages on public `origin/main` carried denylisted names (embarch-api, embarch-doc, embarch-dev-bench, embarch-ui twice; dated 2026-09-19 to 2026-10-14), and so did one public blob in embarch-fleet's history. Every gate run had reported all of them clean. The owner had the five histories rewritten and force-pushed the same day: 685 commits on `main` got new hashes, and the citations were repointed (embarch-doc 0f68533a, embarch-fleet ffc851f).
**Scope:** suite
**Hardware:** none
**Owner:** required — every path it must write is in `embarch-fleet` (`scripts/check-client-names.py`, `scripts/install-hooks.py` and the hook it installs, `decisions.md`), which `check-ownership.py --supervisor` reserves to the owner. Set on filing by the 2026-10-25 leg; the drop said `no`.

## What

The pre-push hook (`~/.git-hooks-personal/pre-push.embarch-impl:58-59`, installed by `embarch-fleet/scripts/install-hooks.py`) runs `check-client-names.py --repo <root>` with no `--base`. The script then scans commit messages in `<main or origin/main>..HEAD` (`embarch-fleet/scripts/check-client-names.py:288-294`). The suite commits straight to `main` (`embarch-doc/embarch-dev-workflow.md` §6), so on `main` that range is empty and no commit message is ever scanned, by the hook or by the gate. The tree scan reads only the current tree, so a name that a later commit removed from a file stays in pushed history unseen. When done, the hook reads git's pre-push stdin (`<local ref> <local sha> <remote ref> <remote sha>`) and scans every commit the push sends, `<remote sha>..<local sha>`, or the whole history of `<local sha>` when the remote ref is new. It scans each commit's message and each blob that commit adds or changes, with the same decoders the tree scan uses. The gate keeps its tree scan and adds `--history`, which scans every reachable commit's message and blobs. The supervisor runs `--history` once per day and before it creates any new public repo.

## Why now

The check exists because of the 2026-09-04 scrub, and every gate since then reported each repo clean while five commit messages carrying names went out on public `main`. The most recent one, a dev-bench commit message on 2026-10-14, named the field project. The 2026-10-20 rewrite removed them, and nothing stops the next one.

## Done when

- [x] The pre-push hook scans `<remote sha>..<local sha>` for messages and added or changed blobs; a fixture repo test pushes a commit whose message names a test-denylist entry and is refused, on `main` and on a branch.
- [ ] A push of a new branch or a new repo scans its whole history.
- [ ] `check-client-names.py --history` scans every reachable commit's message and blobs; a fixture test finds a name in a message and in a blob that a later commit removed, and all twelve repos pass it today.
- [x] The supervisor's daily phase and the new-repo checklist run `--history`.
- [ ] `embarch-fleet/decisions.md` records the 2026-10-20 rewrite (five repos, force-pushed `main`, citations repointed). It also records whether GitHub Support was asked to purge the unreachable old commits, which GitHub keeps reachable by SHA until it collects them.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Blocked

Built 2026-10-29 in the owner's session: fleet `e1565b7` (`check-client-names.py --pre-push REMOTE`, `--history`, `--suite --history`; the hook passes `--pre-push "$1"`; `leg.md`'s first unit after midnight runs `--suite --history`; `install-hooks.py` creates the hooks directory before its first write), `DOC-PROTOCOL.md` §6 for a new repo, the record in `embarch-fleet/open.md` ("Whether the framework's prose is portable"; the fleet has no `decisions.md` by design, `embarch-fleet/spec.md`). A fixture with invented names passes 27 of 27 through a hook rendered by `install-hooks.py` into a throwaway `core.hooksPath`; the old hook fails 11 of them, `main` among them.

**One deliberate change from box 2:** a new branch is scanned for every commit the remote lacks (`<tip> --not --remotes=<remote>`), not its whole history. A new repo, with no remote refs, is still read whole. Whole history of `embarch-doc` is 104 MB of blobs and 21 s; a worker pushes two new branches per unit; what they send is a few commits, 0.3 s. A name already public is not taken back by refusing a new branch, and the daily `--suite --history` is what finds it. Reverting to the literal box is one line in `pre_push_revs()`.

**What only the owner can close:**

1. **`embarch-dev-bench` fails `--history` today** — the other 13 repos pass. Ten blob versions of `app/tests/serial_protocol/src/main.c`, 2026-08-25 to 2026-09-06, reachable from `origin/main`, hex-encode denylist entry #18: the 2026-09-06 leak `check-client-names.py`'s header describes, which the 2026-10-20 rewrite's text search could not see. Taking it out is a history rewrite and a force-push of public `main`. The daily run stays red until then.
2. **Whether GitHub Support was asked to purge the commits the 2026-10-20 force-push left behind** is recorded nowhere. `embarch-fleet/open.md` says so; one line there closes it.
3. **The live hook is still the old one** until `scripts/install-hooks.py` is run after this lands — script first, hook second: a hook rendered before the script lands passes a flag the old script refuses, and every push is refused.

