# 155 — A build asked from a worktree session builds that worktree, or refuses

**State:** claimed by agent/api/155-a-worktree-session-build-builds-the-worktree, 2026-11-14 11:24
**Source:** EMB-181, filed by the `api/154` worker after it established, by a test, that such a build runs the main clone's tree
**Issue:** EMB-181
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`api/154` found that an `embarch-api` server started in a Start work worktree
loads the main clone's linked `embarch/embarch.toml`, whose `source_path` and
`build_dir_root` are absolute paths into the main clone, and the plan uses them
verbatim: `west` runs with cwd = `source_path`, the app dir is
`<source_path>/app/<app>`, `-d` is under `build_dir_root`. The working
directory only finds the config. So a build ships an image from the main
clone's tree, and an edit in the worktree changes nothing with nothing saying
so — the failure `embarch-desk` decision 80 exists to end for a shell build.

Make a build from a server whose working directory is inside a git worktree of
the clone `source_path` points into either **build that worktree** (run in,
and pass the app path from, the same relative path under the worktree's root)
or **refuse with a message naming both trees**. Which, and when each applies
(say, the worktree lacks the path), is your design; record it as a numbered
decision in `embarch-api`'s decisions and replace `spec.md`'s "Known defect"
bullet about `source_path` with the rule that now holds.

**The build directory.** State the choice for this case so a worktree build
never overwrites the main clone's build directory, and never reuses one built
from the other tree without a pristine rebuild.

**Where, from the issue.** `crates/embarch-firmware-build/src/resolve.rs`
`resolve_zephyr_build` and `resolve_static` take `source_path` and
`build_dir_root` verbatim; `src/main.rs` startup near `find_config_upward`
finds the config but never relates the working directory to `source_path`.

**`embarch-firmware-build` has a second consumer: `embarch-ui`**
(`embarch-ui/Cargo.toml` path-depends on it). A change to that crate's public
API that breaks `embarch-ui`'s build is a cross-repo change and not yours to
make. So either do the relating in `embarch-api`'s own code before it calls
the crate, or keep the crate's public API additive only (new items, no changed
signatures), and say in this file which you chose. If neither works, stop and
say so here.

**Detecting a worktree.** Do it with read-only `git` (`rev-parse
--show-toplevel`, `--git-common-dir`) or by reading `.git` files; never a
tree-mutating subcommand (`spec.md`'s invariant on `git`).

**Tests.** A unit test pins the new behaviour over a temporary repo and a
`git worktree add` of it, and **replaces** `api/154`'s pinning test
(`a_zephyr_build_runs_in_and_builds_the_configured_source_path_not_the_working_directory`
in `resolve.rs`), which states the old behaviour. Do not run a real
`west build` and do not build any configured project's sources.

**Not in scope.** Whether a worktree's `.claude/settings.local.json` `env`
reaches the MCP server's process at all is `embarch-desk`'s side; if your
design depends on it, say so here rather than assuming it.

**What you may change.** Only `embarch-api` and `embarch-doc/embarch-api/`.

**Doc reserve.** Nothing of `embarch-api`'s is in reserve. Decision topic
files near their limit: `ledger` 15 B left, `bench-exchange` 122 B,
`failure-reporting` 192 B; a build decision belongs in `build.md` or
`firmware-build-crate.md`, neither near its limit.

## Why now

The owner's worktree sessions build firmware through this server, and today
every one of them builds the main clone while the session edits the worktree.

## Done when

- [ ] A build from a server whose working directory is a git worktree of the clone `source_path` points into runs in, and passes the app path from, that worktree, or refuses with a message naming both trees.
- [ ] The build directory choice for that case is stated, so a worktree build never overwrites the main clone's build directory.
- [ ] A unit test pins it, replacing `api/154`'s pinning test.
- [ ] A numbered decision records the rule; `spec.md`'s known-defect bullet is replaced by it.
- [ ] `embarch-ui` still builds against the crate, or the crate is untouched; this file says which.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `changelog.d/` fragment dropped.
