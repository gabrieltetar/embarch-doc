# Close the shell-wrapper bypass in `reject_tree_mutating_command`

**State:** done by agent/api/033-shell-wrapper-git-guard, 2026-09-09
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/spec.md` §2 asserts coverage this guard does not have
**Scope:** api
**Hardware:** none
**Owner:** no

## Supervisor's dispatch note, leg 058 (2026-09-09, burndown)

**`embarch-api` is the tightest sub-project in the suite for doc size. Read this before you plan
your doc edits.** Five files are inside the last 10% of their cap. All are still writable and the
gate still passes — but every one of them is filed against a **blocked** compaction task, so a
worker may not compact them and you must not spend their headroom:

| file | size/cap | headroom | filed against |
|---|---|---|---|
| `embarch-api/decisions/tool-wrapping.md` | 12,222/12,288 B | **66 B** | `tasks/api/047` [BLOCKED] |
| `embarch-api/decisions/core-link.md` | 12,076/12,288 B | **212 B** | `tasks/api/026` [BLOCKED] |
| `embarch-api/open.md` | 4,802/5,120 B | **318 B** | `tasks/api/026` [BLOCKED] |
| `embarch-api/spec.md` | 9,350/10,240 B | **890 B** | `tasks/api/026` [BLOCKED] |
| `embarch-api/decisions/build.md` | 11,134/12,288 B | 1,154 B | `tasks/api/050` [BLOCKED] |

**`spec.md` is the one you legitimately need**, because its §2 over-claim ("This crate never runs
`git checkout` … Enforced against the config file too") is exactly what this unit corrects. Make
that a **replacement** rather than an addition: the honest wording is not longer than the
over-claim, and 890 B is ample for a net-neutral edit. **Do not touch the other four.** In
particular the "update spec.md/decisions.md/open.md" line in the Done-when below is boilerplate,
not a checklist — leave `open.md` alone unless this unit made a statement in it false, and if it
did, say so in your report rather than squeezing 318 B.

If your work does push a file into reserve or leaves one there unfiled, file
`tasks/api/<next free NNN>-compact-api.md` in the same commit (`tasks/README.md` has the shape, and
the path is `tasks/api/`, never `tasks/doc/`).

**This leg runs in burndown mode: do not author a new numbered decision.** Extending the guard is
an implementation of the coverage `spec.md` §2 already claims, not a new position — record it in the
`changelog.d/` fragment and the corrected `spec.md` §2 prose. If you conclude it genuinely needs its
own numbered decision, stop and say so in your report rather than writing one.

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

- [x] `reject_tree_mutating_command` refuses `["bash","-lc","git checkout main && git describe"]`,
      `["sh","-c","git reset --hard"]` and `["/usr/bin/env","git","stash"]`, each naming the
      offending subcommand.
- [x] `["bash","-lc","git describe --always --dirty"]` and `["cat","VERSION"]` still pass.
- [x] `a_non_git_program_is_not_second_guessed` is **rewritten, not deleted**, to state the
      narrowed rule, and the module doc names what the guard still cannot see.
- [x] `src/reflash.rs`'s `the_reflash_path_never_moves_the_tree` covers at least one wrapper case.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Closing note (leg 058)

Fixed by adding `SHELL_OR_EXEC_WRAPPER_PROGRAMS` (`sh`, `bash`, `zsh`, `dash`, `env`, `cmd`,
`powershell`, `pwsh`) to `reject_tree_mutating_command` in
`crates/embarch-core-client/src/version.rs`: when the program is one of those, its remaining argv
is flattened (splitting any argument that itself contains whitespace, so a `-c`/`-lc` script
string is scanned word by word) and checked for a `git` token alongside a mutating subcommand
token, refusing with the same message an operator already got for a bare `git` invocation. Module
doc comment and one test rewritten to name the narrowed rule honestly (an opaque
`./scripts/version.sh` is still out of reach — this rule reads argv, not a script's contents); two
new tests added for the wrapper-refusal and wrapper-still-passes-on-a-read cases.
`src/reflash.rs`'s `the_reflash_path_never_moves_the_tree` gained a `bash -lc` case.

Docs: `spec.md` §2's over-claim replaced with the honest "never knowingly runs a tree-mutating
`git` subcommand" wording (net +75 B, well inside its 890 B headroom). `decisions/studies.md`
decision 40 — which explicitly mirrors that spec.md sentence and says so — updated the same way,
plus a clause on the wrapper coverage and the opaque-script limit (it had ample headroom, not one
of the five near-cap files, so no separate filing needed). Per the dispatch note, `open.md`,
`decisions/tool-wrapping.md`, `decisions/core-link.md` and `decisions/build.md` were **not**
touched — nothing in this unit made an `open.md` statement false. No new numbered decision was
needed or written: this implements the coverage decision 40 / `spec.md` §2 already claimed.
`changelog.d/api-shell-wrapper-git-guard.fixed.md` dropped. No suite-level (`status.d/`) fact was
made false — the over-claim was scoped to this crate's own docs.

Gate: `cargo build`, `cargo test` (all green, including the new tests) and
`cargo clippy --all-targets -- -D warnings` (clean) in the code worktree; `scripts/check-docs.py`
(10/10 green), `scripts/check-client-names.py --repo <code worktree>` (clean against 7 denylist
entries) and `scripts/check-ownership.py --scope api` / `--code-repo` (both OK) in the doc
worktree.
