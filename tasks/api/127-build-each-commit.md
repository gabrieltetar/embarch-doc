# 127 — Build every commit of a range in each configuration, and prove a rewrite kept the tree

**State:** done — agent/api/127-build-each-commit, 2026-11-10; stacked on agent/api/126-build-returns-a-verdict-and-takes-named-variants
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 74 per-commit build runs in 15 sessions through about 12 hand-written build scripts (`percommit.sh` written in 4 sessions); re-verification was 6.4 % of review-loop cost and 7.2 active hours; two "byte-identical" checks on 2026-10-07 were invalid because a worktree build used the main checkout's module
**Scope:** api
**Hardware:** toolchain
**Owner:** no

## What

Add `embarch-api build --each <base>..<tip>` and a matching MCP tool. For every commit in the range, it builds each named variant (the project-config variants of `api-build-returns-a-verdict-and-takes-named-variants`, which this builds on) and reports per commit and variant, as that draft's verdict object: pass/fail, warnings new against the previous commit, flash and RAM with the delta, and headroom left in the code partition. Each commit is built from **its own module sources**. That means a detached checkout of the module at that commit, made visible to west in place of the workspace's module. It must not be a `git worktree` outside the west workspace, because west then silently builds the main checkout's boards and drivers, which invalidated two field checks. `--same-tree-as <ref>` asserts that the tip's tree equals a reference ref, the check every fold in the field did by hand. It also asserts that the tip image differs from the reference ref's image only in the embedded commit id. Output is JSON plus a short table, with an option to stop at the first failure.

## Why now

After every fold the field sessions rebuilt each commit in two or three configurations to prove nothing in the middle of the stack broke. Each session wrote its own loop, and the most common one was rewritten four times. Re-verification is the third-largest review-loop step, after reviewer rounds and fixes.

## Done when

- [x] `build --each` CLI and the `build_each` MCP tool, with the JSON result in
      `interfaces/tools-build-flash.md` (the api's interfaces are split; `tools.md` indexes the
      tool). The parity test records `build_each`/`build --each` as a documented asymmetry, like
      `study_watch`/`study-status --follow`.
- [x] A fixture commit that changes only a board file builds with that change. **Real Zephyr
      4.4 run** in a scratch west workspace under `/tmp` (Zephyr and CMSIS shared-cloned from an
      existing workspace, a module repo with board `embarchfx` copied from `qemu_cortex_m3` and a
      hello app): C1 only adds `CONFIG_LOG=y` to the board's defconfig. **Control**: C1's sources
      in a checkout outside the module, built with plain `west build` from the workspace, used the
      workspace's board (checked out at C0): `CONFIG_LOG` unset, FLASH 9,376 B — the field
      failure. **`build --each C0..C2`**: C1 built with its own board, FLASH 14,344 B; C2 +4 B.
      The engineer's checkout stayed at C0, clean. Also `tests/build_each.rs` end to end with a
      fake `west` whose "board" value comes from whichever module the build was given, with a
      dirty working tree that no commit has.
- [x] `--same-tree-as`: on the real fixture, a squashed rewrite with C2's tree passed — "default:
      differs only in embedded commit ids (1 run(s)); bench: …" — once `app_version.h` is
      removed before each build (without that, every image carried the first commit's id and the
      comparison read "identical"). Against C1 it failed naming `app/hello/src/main.c`. Unit tests
      cover a non-commit hex run, a size change and a byte outside any run.
- [x] Per-commit FLASH/RAM deltas (from the previous commit, same variant), new warnings and FLASH
      headroom (linker `FLASH` total minus used) for each variant; `--stop-at-first-failure`
      stops at the first failing build.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `embarch-ui` checked to compile against
      the changed shared crate.
- [x] Decision 104, `spec/implementation.md` §3, `interfaces/tools-build-flash.md`,
      `interfaces/tools.md`, `open.md` (the `build --each` limits) updated;
      `changelog.d/api-build-each.added.md` and `features.d/api-096-build-each.md` dropped;
      `tasks/api/150` (the `open.md` reserve debt) updated for this bullet.

## Shipped

- `src/build_each.rs` (new): range parsing, the shared-clone checkout under
  `<topdir>/.embarch-build-each/<project>-<hash>/`, the per-commit loop, the image comparison.
- Shared crate, all additive: `ProjectConfig`/`DefaultTarget` derive `Clone`;
  `config::require_plain_west_build` (was private to build variants); `build::key_file_stem`
  public; `Verdict::all_warnings`.
- CLI: `build --each <BASE..TIP>` with `--same-tree-as` and `--stop-at-first-failure`; `--vs`,
  `--pristine` and `--verbose` are refused with `--each`.

## Limits found

- **Sysbuild**: `app_version.h` is removed at `<build>/zephyr/include/…`; a sysbuild image's sits
  under `<build>/<app>/zephyr/…` and stays stale. A commit id a project computes at CMake
  configure time stays stale in any incremental build, and this tool cannot see it.
- **The module must be the one the project builds.** The override replaces the module named like
  the project's repository; a commit range in a *different* module the app depends on is not
  covered.
