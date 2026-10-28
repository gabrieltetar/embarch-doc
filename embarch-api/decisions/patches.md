# embarch-api decisions: The patch-series round trip

**Status:** active, 2026-10-28.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 92 — `patches` round-trips a west manifest's patch series through one scratch tree

`embarch-api patches export | import | regroup` (`tasks/api/129`; field cost: one scratch tree, one regen script and one hand-split "Fix:" commit per review round). **CLI only and host-side only** — it needs `git`, no config and no embarch-core, so `main` dispatches it before either is looked for, as it does `versions`, and the CLI-has-no-tool asymmetry list grows by `patches` (spec §1).

- **`export --series patches.yml --repo <module> --base <rev> --scratch <dir>`** clones the module (`--shared`, no checkout), branches `embarch-patches/series` at the base and runs `git am` per `path:` entry, so each patch is one commit with its author, date and message. An existing scratch tree with the tool's state file is **reused**, not rebuilt (`--force` rebuilds); a directory without it is refused. The base is an explicit revision, not read from `west.yml`: the manifest's pin of the module is the caller's fact to supply.
- **`import --scratch <dir>`** rewrites a patch file only when its commit is no longer the one `export` recorded, and then with `git format-patch --zero-commit --no-signature` and the file's own existing `[PATCH n/m]` prefix — so an untouched series, or a commit merely re-parented by a rebase, comes back **byte-identical**. Each entry's `sha256sum` is set from the file on disk; `patches.yml` is edited line-wise so comments and the other keys survive. Output lists the files changed.
- **Fix commits fold by blame.** Commits stacked on the recorded tip are split per hunk (`git diff -U0`), each hunk is attributed to the **latest** series commit that last touched its old lines (`git blame`; lines no patch owns go to the last patch touching that file, a new file to the last patch), one temporary commit per target is cherry-picked onto the tip as `fixup! <sha>`, and `rebase --autosquash` folds them. The result is checked: the tree must equal the fix commit's. Fixes fold in order; a merge commit, a rename, a deletion or a binary change is refused by name rather than guessed.
- **`regroup --scratch <dir> --map <file>`** — lines `new/path.patch: 0001, 0002 | optional subject`, every old patch exactly once — builds the new series on a side branch and writes nothing unless the **git tree id after equals the one before**. New files are written, old ones removed, entries rewritten from the first source's metadata. Patch-number references (a digit run of the series' number width on a line mentioning "patch", or in a `NNNN-….patch` name) are rewritten old→new in the commit messages, and the result lists those rewritten and those it saw but could not map.

**Measured or assumed.** All of it is exercised on a throwaway 3-patch fixture (`tests/patches_cli.rs`); none of it has met a real `west patch` manifest or a stack of upstream-format patches, so mbox-less plain diffs (`git apply`-style entries) are **unsupported** — `git am` rejects them, naming the file.

**Rejected:** a worktree on the module (writes into the source repo's metadata), reading the base out of `west.yml`, and attributing a fix hunk by path alone (a "Fix:" across patches 0013 and 0015 touches one file twice).
