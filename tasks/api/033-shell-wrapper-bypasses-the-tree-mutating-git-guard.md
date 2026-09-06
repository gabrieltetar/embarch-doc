# Close the shell-wrapper bypass in `reject_tree_mutating_command`

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/spec.md` §2 asserts coverage this guard does not have
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client/src/version.rs:70-73` returns `Ok(())` for any program whose file
stem is not `git`, so `version_command = ["bash","-lc","git checkout main && git describe"]`
passes the guard and `derive_version` runs it (`version.rs:104-112`). The existing test
`a_non_git_program_is_not_second_guessed` (`version.rs:165-170`) pins that hole as intended.

The guard should also refuse a command whose argv *visibly* contains a tree-mutating `git`
subcommand when the program is a shell or exec wrapper — `sh`, `bash`, `zsh`, `dash`, `env`,
`cmd`, `powershell`, `pwsh` — including inside a `-c`/`-lc` string, whitespace-split before
matching. The refusal message stays the one an operator already gets, naming the subcommand.
The over-rejection posture is unchanged, an opaque `./scripts/version.sh` is still out of
reach, and the module doc comment should say that honestly instead of implying total coverage.

## Why now

`spec.md` §2 states "**This crate never runs `git checkout`.** … Enforced against the config
file too, not just this code," and `src/reflash.rs:394`'s `the_reflash_path_never_moves_the_tree`
claims exactly that coverage — while the config-file route around it is open. `spec.md:19`
explicitly blesses `["bash","-lc","…"]` as a normal argv shape for this crate's config, which
is what makes the exemption unsafe rather than academic.

## Done when

- [ ] `reject_tree_mutating_command` refuses `["bash","-lc","git checkout main && git describe"]`,
      `["sh","-c","git reset --hard"]` and `["/usr/bin/env","git","stash"]`, each naming the
      offending subcommand.
- [ ] `["bash","-lc","git describe --always --dirty"]` and `["cat","VERSION"]` still pass.
- [ ] `a_non_git_program_is_not_second_guessed` is **rewritten, not deleted**, to state the
      narrowed rule, and the module doc names what the guard still cannot see.
- [ ] `src/reflash.rs`'s `the_reflash_path_never_moves_the_tree` covers at least one wrapper case.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
