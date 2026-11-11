# 126 — `build` returns a verdict, not the log, and builds named variants in their own dirs

**State:** done — agent/api/126-build-returns-a-verdict-and-takes-named-variants, 2026-11-10; the field variant pair is still to replay (see the replay box)
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 897 build calls: 537 raw `west build`, 127 `twister`, 155 through wrapper scripts written in 12 sessions, 3 through the MCP tool; the two successful MCP builds returned 26.9 KB and 19.9 KB, the hand-filtered Bash builds a median 389 characters; 256 builds carried `-D` or `EXTRA_CONF_FILE` (53 combinations), which a static project's `build` refuses
**Scope:** api
**Hardware:** toolchain
**Owner:** no

## What

Today `build` hands back stdout and stderr up to 64 KB each plus the first `error:` line (`embarch-api/crates/embarch-firmware-build/src/build.rs:20`, `src/tools.rs:81-90`), so the field sessions piped `west build` through `grep -v '^\[[0-9]*/'`, `tail -40` and a size grep instead, each time with a PATH preamble for the venv's cmake (661 calls), and wrote their own wrappers that printed one line per build: name, commit, exit code, warning count, image size, FLASH and RAM. Make that line the default answer: exit code, timed out, seconds, warning count with the first ten warnings as `file:line: message`, the first error block with its cascade dropped (compiler, Kconfig, devicetree or CMake), FLASH and RAM used and total from the linker summary, artifact path and freshness, and `log_path` to the full log kept on disk; `verbose: true` returns today's shape. Add named variants to project config (`extra_conf_files`, `-D` arguments, overlays), accepted by static and `zephyr-west` projects alike, each building in its own persistent directory so that switching variant is an incremental build rather than `-p always` (335 pristine builds, median 18 s, against 7.5 s incremental). With `vs=<variant>` the verdict adds the FLASH and RAM change (the Kconfig difference is the atlas's `config vs=` item). A `twister` run gets the same treatment: one line per test case and the first failing assertion. Building every commit of a stack is a separate item (the review-loop tools); the target discovery gap (`zephyr-west` finding no boards) is another.

## Why now

Builds and the `.config`, `zephyr.dts` and build-log reads that followed them were 1,418 calls, 1,382 turns and 6.3% of all context tokens, and 5.3 h of main-thread tool time; even with discovery fixed, one MCP build would cost about seventy times the characters of the filtered Bash build it replaces.

## Done when

- [x] Default `build`/`build_and_flash` answer is the verdict object, documented in
      `interfaces/tools-build-flash.md`. Measured through the binary: a clean real Zephyr build
      answered 630 B, a failing fixture with a 3,000-line error cascade 607 B (limits 2 KB, 6 KB;
      `tests/build_verdict.rs` asserts both). `schema_version` is now 2 (decision 24: the default
      answer dropped `stdout`/`stderr`).
- [x] The full log is written as `embarch-build.log` **inside** the build directory, beside
      `target.json`, not beside the directory: that is where decision 19 already keeps a build's
      own provenance, and a common `build*/` ignore covers it. A plan with no directory (a
      `static` project's default build) writes under `<temp dir>/embarch-build-logs/`. Named in
      `log_path`; `verbose: true` gives today's answer plus `log_path`.
- [x] Named variants: `[projects.build_variants.<name>]` (`extra_conf_files`, `overlays`,
      `defines`), accepted by both discovery kinds, each with its own build dir. Pristine only when
      asked or when the dir's `target.json` shows other variant settings. With a matching CMake
      cache the variant's arguments are left off, so `west` does not reconfigure (switching:
      0.5 s against 6.8 s pristine, measured). A `static` project needs a plain `west build`
      argv and an artifact under `build/`, refused at load otherwise.
- [x] `vs=<variant>` (or `default`) adds the per-region FLASH/RAM change against that variant's
      last recorded build, read before this build starts.
- [x] A test run answers one line per case with the first failing assertion: a real ztest sample
      on `native_sim/native/64` through `embarch-api build` (`west build -t run`) answered
      `"tests": ["FAIL framework_tests.test_assert"]` and the `Assertion failed at …` line.
      Twister per-scenario lines are fixture-tested only.
- [x] Replay — **a substitute pair, not the field's**: the field's recorded pair lives in a
      client workspace no worker may touch. Instead: Zephyr 4.4.0's `hello_world` on
      `qemu_cortex_m3`, default and a `bench` variant adding a logging Kconfig fragment, at one
      tree, through the CLI. Results: the two default human answers 214 + 246 = 460 B (331 B
      without the `log:` lines), against the wrappers' ~480; JSON verdicts 630 B and 1,004 B
      (with `vs`: FLASH +10,468 B, RAM +72 B); today's answer (`--verbose`) for a pristine build
      15,740 B, against the field's 26.9 KB for a larger app. **Debt for the owner: replay the
      field pair itself** (`open.md` names it).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), and `embarch-ui` checked to compile
      against the changed shared crate (`cargo check --all-targets`, its `HEAD` beside this
      branch).
- [x] `spec/implementation.md` §3 and §7, decisions 102 and 103 (plus 24's version note),
      `interfaces/tools-build-flash.md`, `interfaces/config.md`, `interfaces/tools.md`, `open.md`
      updated; `changelog.d/api-build-verdict-and-variants.added.md` and
      `features.d/api-095-build-verdict-and-variants.md` dropped. The `open.md` bullet put that
      file 307 B into its size reserve; the debt is filed as `tasks/api/150-compact-api.md`.

## Shipped

- `crates/embarch-firmware-build/src/verdict.rs` (new): the log parser, `verdict_json`,
  `verdict_text`, the `vs` baseline.
- `build.rs`: one combined log alongside the two pipes, `seconds`, the log and its record written
  after every build, `BuildOutcome` gains `seconds`, `log_path`, `verdict`,
  `memory_from_previous_build`. `BuildPlan` is unchanged, so `embarch-ui` and the `api/108`
  Windows test build as before.
- `config.rs`: `BuildVariant` and its load checks. `resolve.rs`: `BuildChoice`, `resolve_with`,
  `resolve_build_with`; `Resolved`/`ResolvedBuild` gain `pristine`. `Selection` is unchanged
  because `embarch-ui` builds it field by field.
- MCP `build`/`build_and_flash` take `build_variant`, `vs`, `pristine`, `verbose`; `flash` takes
  `build_variant`. CLI: `--build-variant`, `--vs`, `--pristine`, `--verbose` on `build` and
  `build-and-flash`, `--build-variant` on `flash`. `bootload`, `build_and_bootload` and the
  dev-bench builds keep their old shape.
- The doc branch is stacked on `agent/api/108-windows-tree-kill` because both edit the
  `decisions.md` row for `decisions/build.md`; land 108 first.
