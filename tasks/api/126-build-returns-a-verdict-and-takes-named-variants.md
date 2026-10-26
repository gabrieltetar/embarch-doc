# 126 — `build` returns a verdict, not the log, and builds named variants in their own dirs

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 897 build calls: 537 raw `west build`, 127 `twister`, 155 through wrapper scripts written in 12 sessions, 3 through the MCP tool; the two successful MCP builds returned 26.9 KB and 19.9 KB, the hand-filtered Bash builds a median 389 characters; 256 builds carried `-D` or `EXTRA_CONF_FILE` (53 combinations), which a static project's `build` refuses
**Scope:** api
**Hardware:** toolchain
**Owner:** no

## What

Today `build` hands back stdout and stderr up to 64 KB each plus the first `error:` line (`embarch-api/crates/embarch-firmware-build/src/build.rs:20`, `src/tools.rs:81-90`), so the field sessions piped `west build` through `grep -v '^\[[0-9]*/'`, `tail -40` and a size grep instead, each time with a PATH preamble for the venv's cmake (661 calls), and wrote their own wrappers that printed one line per build: name, commit, exit code, warning count, image size, FLASH and RAM. Make that line the default answer: exit code, timed out, seconds, warning count with the first ten warnings as `file:line: message`, the first error block with its cascade dropped (compiler, Kconfig, devicetree or CMake), FLASH and RAM used and total from the linker summary, artifact path and freshness, and `log_path` to the full log kept on disk; `verbose: true` returns today's shape. Add named variants to project config (`extra_conf_files`, `-D` arguments, overlays), accepted by static and `zephyr-west` projects alike, each building in its own persistent directory so that switching variant is an incremental build rather than `-p always` (335 pristine builds, median 18 s, against 7.5 s incremental). With `vs=<variant>` the verdict adds the FLASH and RAM change (the Kconfig difference is the atlas's `config vs=` item). A `twister` run gets the same treatment: one line per test case and the first failing assertion. Building every commit of a stack is a separate item (the review-loop tools); the target discovery gap (`zephyr-west` finding no boards) is another.

## Why now

Builds and the `.config`, `zephyr.dts` and build-log reads that followed them were 1,418 calls, 1,382 turns and 6.3% of all context tokens, and 5.3 h of main-thread tool time; even with discovery fixed, one MCP build would cost about seventy times the characters of the filtered Bash build it replaces.

## Done when

- [ ] Default `build`/`build_and_flash` answer is the verdict object, documented in the interface docs; a clean build answers in at most 2 KB, a failed one in at most 6 KB.
- [ ] The full log is written beside the build dir and named in `log_path`; `verbose: true` gives today's answer.
- [ ] Named variants in config, accepted by both discovery modes, each with its own build dir; pristine only when asked or when the variant's CMake cache no longer matches.
- [ ] `vs=<variant>` adds the FLASH and RAM change against that variant's last build.
- [ ] A test run answers one line per case with the first failing assertion.
- [ ] Replay: build one recorded variant pair (the default image and a test-bench image at one commit) through the tool and compare result characters with the session's wrapper output (two lines, about 480 characters) and with today's MCP answer (26.9 KB).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
