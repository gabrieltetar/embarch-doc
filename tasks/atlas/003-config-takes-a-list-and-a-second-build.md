# 003 — `config` and `dt_node` take a list of names and a second build to compare

**State:** done
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 516 `grep`s of a build's `zephyr/.config` or `zephyr.dts`, 193 of them after `config`/`dt_node` landed on 2026-10-06 (77 atlas build-query calls in the same span); a `.config` grep checked a median of 4 symbols at once, 27 were `diff <(grep … a/.config) <(grep … b/.config)`, and 4 of 67 `config`/`dt_node` calls named a build other than the pinned one
**Scope:** atlas
**Hardware:** toolchain
**Owner:** no

## What

`config` answers one symbol or one glob (`embarch-atlas/src/embarch_atlas/query.py:682`), so checking the four shell and driver options a test image needs is four calls, and comparing two builds is not possible at all, while `footprint` already takes `vs=` (`query.py:704`). Let `config` take several names at once (`symbols` as a list on MCP, comma-separated on the CLI, globs allowed) and answer one line per symbol (value, the fragment that set it, an unmet `depends on` when it is `n`), with the full per-symbol answer still available for a single name. Add `vs=<build dir | pinned>` to `config` and `dt_node`: the answer lists only what differs between the two builds (symbol or property, both values, and where each side's value was set), so "what does the bring-up image change" and "what did the Zephyr bump change in our config" are one call. Keep the existing guard that falls back to value-and-assignment answers when a build's version does not match the workspace, and say per line which fields it could not give.

## Why now

The greps and diffs of build artefacts (with `nm`, `objdump` and `.su` reads) were 593 calls and 2.0% of all context tokens, and the atlas lookups that cover them went mostly unused because each answered one name about one build.

## Done when

- [x] `config` accepts a list or comma-separated names and globs, one line per symbol, capped at the tool budget with `next=`.
- [x] `config vs=` and `dt_node vs=` list only the differences, with both sides' sources.
- [x] MCP signatures and `embarch-atlas q` verbs match; `atlas-use` SKILL.md shows the list and `vs=` forms.
- [x] Synthetic test: two fixture builds that differ in three symbols and one devicetree property answer exactly those.
- [x] Replay: five recorded multi-symbol `.config` greps and three recorded `.config` diffs answered through the atlas, with calls and result characters compared.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Result

**Shipped** (embarch-atlas `718c4fe`):

- `query.config(a, symbol=None, build=None, vs=None, offset=0)`: `symbol` is a name, a comma- or space-separated string, or a list, with `*` patterns allowed. One name keeps the full answer. Several names or a pattern give one line per symbol: value, the fragment line or the select/implied/default/choice that set it, and an unmet `depends on`. Patterns expand over `.config` and are no longer cut at 60 matches: the list pages at the `config` budget with `next=`.
- `config vs=<build dir | pinned>` (`buildq.config_diff_answer`) and `dt_node vs=` (`buildq.dt_diff_answer`) list only what differs. `config` gives each differing symbol with both values and where each side's value was set. `dt_node` gives the nodes only one build has, and per node the status, compatible, labels, each property with both values and the `file:line` that set each, and the pins. A symbol list, a pattern or a node narrows the comparison; no name, or `*`, compares everything. The `src:` line names both builds (`<build> kconfig vs <build> kconfig`).
- Guard kept (`kconfig.workspace_mismatch`): a build made on another Zephyr than the workspace's answers value and fragment assignments only, the reason is stated once at the top, and each line marks `[not given: select/default | depends on | whether it is a symbol here]` for what it lacks. A devicetree comparison with a side that cannot load names that side and why.
- MCP: `config(symbol=None, symbols: list[str] = None, build=None, vs=None, offset=0)`, with the old single `symbol` still working (both may be given); `dt_node(node=None, build=None, vs=None, offset=0)`. CLI: `q config A,B,USB_* [--build D] [--vs D|pinned]` (space-separated names also work) and `q dt-node [node] [--build D] [--vs D|pinned]`. `buildq.versus` resolves `vs` for `config`, `dt_node` and `footprint` alike.
- `atlas-use` SKILL.md quick-lookup table shows the list form and both `vs=` forms. DESIGN.md "Query surface" describes both. Atlas has no `spec.md`, `decisions.md` or `open.md`: as in earlier atlas units, that box is met by DESIGN.md plus the changelog fragment `changelog.d/atlas-config-list-and-vs.added.md`.
- Tests (`tests/test_buildq.py`, 7 new): the list form with and without `kconfig.json`. Two fixture builds that differ in exactly three symbols and one devicetree property: `config vs=` lists exactly those three, `dt_node vs=` exactly that property, and node ordinals that moved are not reported. The guard on the `vs` side gives per-line `[not given]` marks and writes no cache. Paging of the list and both `vs` answers concatenates to the uncut body. The MCP tools and `q` verbs give the same answers.

**Gate:** `pytest -q` 738 passed, 3 skipped (the real-workspace, real-atlas and vendor-SVD skips; `test_public_guard` ran). `check-client-names.py` and `check-ownership.py --scope atlas --code-repo` are green on the code branch; `check-docs.py` and `check-ownership.py --scope atlas` are green on this branch.

**Replay** on the USB PD charger board's recorded sessions, against a `/tmp` copy of its atlas dir, with each shell command re-run read-only against the build dir as it is now. Numbers only:

- Five multi-symbol `.config` greps (8, 5, 11, 9 and 3 names or prefixes; a prefix the grep left open became a `*` pattern):
  - grep: 5 calls, 299 / 386 / 726 / 1668 / 148 result characters (3,227 total).
  - `config` one name per call (the `origin/main` code): 36 calls, 2,359 / 1,644 / 3,918 / 5,554 / 884 characters (14,359 total). The fourth was incomplete: the old pattern answer stopped at 60 matches.
  - `config` list form: 6 calls (one each, and the fourth paged once), 1,281 / 1,308 / 2,486 / 8,992 / 816 characters (14,883 total).
  - All five builds were made on an older Zephyr than the workspace's now, so the guard applied to every one: 138 of 148 symbol lines carry a `[not given]` mark.
- Three `.config` diffs:
  - shell diff: 3 calls, 1,795 / 104 / 134 characters (2,033 total). Each recorded diff had its own filter (one dropped log-level lines, one kept only `=y` lines, one kept only set lines).
  - `config` before this change: no answer.
  - `config vs=`: 4 calls (one paged once), 9,054 / 1,565 / 1,136 characters (11,755 total), 57 / 5 / 4 differing symbols, where the shell diffs printed 44 / 6 / 7 lines. The guard applied on both sides of all three: 69 `[not given]` marks over 66 rows.
- One extra pair of builds that were on the workspace's Zephyr, so with full `kconfig.json` on both sides: the shell diff took 1 call and 726 characters. `config vs=` took 1 call and 3,421 characters, listed 22 symbols each with its setting fragment, select/default or unmet `depends on`, and had no `[not given]`. `dt_node vs=` took 1 call and 413 characters: no difference over 187 nodes. The first `config vs=` took 7.8 s (two Kconfig extractions, cached after) and `dt_node vs=` 0.7 s.

Calls drop from one per name to one per question, and a two-build comparison now exists. Characters rise against a raw grep or diff because every line says where its value came from and the `src:` line names both builds (about 350 to 600 characters with absolute build paths). Against one `config` call per name, the list form costs fewer characters in four of the five greps.

**Unverified:**

- `dt_node vs=` has not been run on a real pair whose devicetrees differ. The one real pair on the workspace's Zephyr had none, so only the synthetic test covers a difference.
- The MCP tools ran in process (`call_tool`) and not through a Claude Code session.
- Fragment assignments are read from the fragment files as they are now, not as they were at build time. This was already the case for the single answer, and two replayed lines showed `asked <v>, not applied` that may come from a fragment edited after the build.

**Choices made without the owner:**

- In `config vs=`, absent, unset and `n` count as the same value, so `# CONFIG_X is not set` against a symbol missing from the other `.config` is not a difference.
- `dt_node` takes `vs=` but not a list. The title names both lookups, but "What" and "Done when" ask the list of `config` only, and commas occur inside compatibles, so a comma form cannot work for nodes. A `nodes: list[str]` form can follow if field use asks for it.
- A devicetree comparison compares property values, not where they were set, and skips node ordinals, the compiled driver and ELF presence.
- When a side's devicetree cannot load, the comparison stops and says which side and why. It does not fall back to a text comparison of `zephyr.dts`.
- `_build_src` now also catches an error raised while answering (an extraction failure answers `src: none` with the error), as `footprint` already did.

**For the owner:** 41 of the 44 image build dirs in the field workspace were made on an older Zephyr than the workspace's now. On those, `config` answers only value and fragment, and `dt_node` with or without `vs=` cannot answer unless an earlier query cached the extraction. Should the extraction run right after each engineer build so it is cached before the next Zephyr bump, or should `dt_node vs=` fall back to comparing `zephyr.dts` text? Filed separately: EMB-148, a replay harness, so the next replay is one command instead of another throwaway script.
