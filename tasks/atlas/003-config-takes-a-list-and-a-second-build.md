# 003 — `config` and `dt_node` take a list of names and a second build to compare

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 516 `grep`s of a build's `zephyr/.config` or `zephyr.dts`, 193 of them after `config`/`dt_node` landed on 2026-10-06 (77 atlas build-query calls in the same span); a `.config` grep checked a median of 4 symbols at once, 27 were `diff <(grep … a/.config) <(grep … b/.config)`, and 4 of 67 `config`/`dt_node` calls named a build other than the pinned one
**Scope:** atlas
**Hardware:** toolchain
**Owner:** no

## What

`config` answers one symbol or one glob (`embarch-atlas/src/embarch_atlas/query.py:682`), so checking the four shell and driver options a test image needs is four calls, and comparing two builds is not possible at all, while `footprint` already takes `vs=` (`query.py:704`). Let `config` take several names at once (`symbols` as a list on MCP, comma-separated on the CLI, globs allowed) and answer one line per symbol (value, the fragment that set it, an unmet `depends on` when it is `n`), with the full per-symbol answer still available for a single name. Add `vs=<build dir | pinned>` to `config` and `dt_node`: the answer lists only what differs between the two builds (symbol or property, both values, and where each side's value was set), so "what does the bring-up image change" and "what did the Zephyr bump change in our config" are one call. Keep the existing guard that falls back to value-and-assignment answers when a build's version does not match the workspace, and say per line which fields it could not give.

## Why now

The greps and diffs of build artefacts (with `nm`, `objdump` and `.su` reads) were 593 calls and 2.0% of all context tokens, and the atlas lookups that cover them went mostly unused because each answered one name about one build.

## Done when

- [ ] `config` accepts a list or comma-separated names and globs, one line per symbol, capped at the tool budget with `next=`.
- [ ] `config vs=` and `dt_node vs=` list only the differences, with both sides' sources.
- [ ] MCP signatures and `embarch-atlas q` verbs match; `atlas-use` SKILL.md shows the list and `vs=` forms.
- [ ] Synthetic test: two fixture builds that differ in three symbols and one devicetree property answer exactly those.
- [ ] Replay: five recorded multi-symbol `.config` greps and three recorded `.config` diffs answered through the atlas, with calls and result characters compared.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
