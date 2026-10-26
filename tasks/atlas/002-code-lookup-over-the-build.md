# 002 — Look up a symbol or a state machine in the sources a build compiled

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 12,738 `grep`/`sed -n`/`Read` calls on C sources (4,824 Zephyr, 7,914 application and driver) were 42% of all context tokens and returned 67 MB; 1,364 `sed -n` ranges came on the call right after a `grep -n` on the same file; the USB-C stack (`subsys/usb/usb_c`, the UCPD TCPC driver, their headers, `lib/smf`) took 3,350 of the Zephyr reads and was re-read from scratch by 203 separate agents
**Scope:** atlas
**Hardware:** toolchain
**Owner:** no

## What

Add two build-joined lookups beside `config` and `dt_node`, with the same `build=` parameter (default the pinned build) and the same `src:` line. `code <symbol>` (also `<file>:<symbol>`) returns the definition of a function, struct, enum, typedef or macro as compiled: file and line, the translation unit it came from, the body cut at the tool budget with `next=`, and its references among the build's compiled translation units as one `file:line function` line each. `states <table | directory>` reads Zephyr SMF state tables (`SMF_CREATE_STATE` entries) and returns one row per state: name, parent, entry/run/exit functions with their lines, and the states each run function can move to (`smf_set_state` targets found in it). The source set is `compile_commands.json` of the named build, so a variant build, a scratch Zephyr worktree with west patches applied, or a version bump answers for its own tree and never for the workspace checkout. Extraction is deterministic (a tags index or libclang when the build's toolchain provides it, regex otherwise) and cached per build like `kconfig.json`.

## Why now

Every lookup cost two calls (find the line, then print a range) and the answers were re-derived per agent: the eight review rounds of one Zephyr version bump each spent 63 to 78 of their roughly 110 calls reading Zephyr source. The `grep`→`sed` pairs alone were about 1,364 turns and 0.41 B context tokens (5.5% of the total).

## Done when

- [ ] `code` and `states` exist as MCP tools and `embarch-atlas q` verbs, take `build=`, and cite the build's version in `src:`.
- [ ] A function body over the budget pages with `next=`, and a symbol defined in several compiled units lists each one, never just the first.
- [ ] Lookups against a build whose Zephyr tree is a patched worktree return the patched lines; a test builds a fixture where the workspace and the build disagree.
- [ ] `states subsys/usb/usb_c` on an upstream Zephyr v4.4 build lists the PE, TC and PRL tables with their transitions (public tree, so the fixture can ship).
- [ ] Replay: answer the Zephyr-source questions of one recorded review subagent (63 to 78 `grep`/`sed`/`Read` calls) with `code`/`states`, and report calls and result characters before and after; target at least half the calls.
- [ ] `atlas-use` SKILL.md and DESIGN.md "Query surface" name the two lookups.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.

## Evidence

### Token and wall-time hogs, field project, 2026-09-09 to 2026-10-20

Method. (1) Parsed the 89 main transcripts and their 318 subagent transcripts (this analysis session excluded) and counted each API response once by `message.id`: the digest counts every content block, which doubles usage, so the real totals are 27.1k turns, 7.66 B cache-read tokens, 0.13 B cache-creation tokens and 12.8 M output tokens (not 52k / 14.85 B / 28.4 M). (2) Classified the 28.8k tool calls into exclusive activities by tool name and command regex; each turn's context tokens (cache read + creation + input) are split evenly among the calls it issued; review subagents are recognised by their task description. (3) Share = an activity's context tokens over the 7.4 B spent on tool-calling turns (741 text-only turns, 0.26 B, left out); wall time = main-thread tool execution, capped at 1 h per call, user waits excluded.

| # | Activity | Calls | Turns | Result MB | Share of context tokens | of it in review subagents | Main-thread tool h | Proposed tool | Draft |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | Firmware (application, driver) source reads: `sed -n`, `grep -n`, whole-file `Read` | 7,914 | 7,220 | 48.4 | 24.8% | 14.5% | 0.8 | symbol and state-table lookup over the build's compiled sources | `atlas-code-lookup-over-the-build.md` |
| 2 | Zephyr source reads (3,350 of them in the USB-C stack, `lib/smf` and the UCPD driver) | 4,824 | 4,667 | 18.7 | 17.0% | 12.5% | 0.3 | same lookup; `states` for SMF tables | `atlas-code-lookup-over-the-build.md` |
| 3 | USB PD spec text greps on a `pdftotext` dump | 3,646 | 3,607 | 17.4 | 15.6% | 13.4% | 0.3 | covered by the static-atlas drafts | none (other agent) |
| 4 | git and gh (review, fold, rebase, status) | 3,003 | 2,832 | 10.8 | 9.2% | 2.5% | 1.0 | covered by the review-loop drafts | none (other agent) |
| 5 | Builds: `west build`, `twister`, wrapper scripts, then `.config`/`zephyr.dts`/ELF/build-log reads | 1,418 | 1,382 | 1.7 | 6.3% | 1.4% | 5.3 | build verdict plus named variants; `config` list and `vs=` | `api-build-returns-a-verdict-and-takes-named-variants.md`, `atlas-config-takes-a-list-and-a-second-build.md` |
| 6 | Bench runs: consoles (434 calls, 2.0%), flash through J-Link Commander and EmbArch (287, 1.5%), e-load SCPI (201, 1.0%), atlas live reads (205, 0.8%); bench lock, port and probe checks overlap these (about 300 calls, 1.3%) | 1,290 | 1,066 | 1.5 | 6.2% | 0.4% | 2.9 | console sequence plus merged timeline; the rest is covered by the instrument, live-tool and Core-friction drafts | `api-bench-exchange-one-call-both-consoles-one-timeline.md` |
| 7 | Miscellaneous: small bash, edits, plan mode, web, Linear | 2,727 | 2,388 | 6.8 | 8.2% | 2.9% | 4.3 | no single repeated pattern | none |
| 8 | EmbArch's own sources read from field sessions (suite work done from the field repo) | 1,108 | 1,027 | 3.6 | 4.7% | 0.0% | 1.1 | suite meta-work, out of scope | none |
| 9 | Atlas static queries | 1,237 | 816 | 3.0 | 2.9% | 2.2% | 0.2 | covered by the static-atlas drafts | none (other agent) |
| 10 | Memory, plans, notes and rule files (separately, the start-of-session orientation across all activities: 1,303 calls, about 1.6%) | 989 | 816 | 4.0 | 2.8% | 0.3% | 0.6 | Claude Code memory, not an EmbArch tool | none |
| 11 | Subagent orchestration (waiting on subagents) | 483 | 356 | 0.3 | 1.9% | 0.9% | 3.7 | covered by the review-loop drafts | none (other agent) |
| 12 | Other log reads (bench captures) | 153 | 152 | 2.3 | 0.5% | 0.2% | 0.0 | below threshold | none |

Findings that change how to read the table:

- Session length is the multiplier, not result size. The first turn of a session carries about 48k tokens; the median session averages 152k per turn and the largest reached 967k. 89 sessions compacted 7 times. Tool results account for about 29% of context tokens through re-reading (2.3 B of 7.8 B, at 3.6 characters per token), and firmware source reads alone are 42% of that carry.
- Reading Zephyr and firmware source is the largest hog in reach (42%). It is mostly two calls per lookup (1,364 `sed -n` ranges directly after a `grep -n` on the same file, 0.41 B tokens) and the same files re-derived by 203 agents.
- Builds are cheap per call (median result 389 characters, because every session hand-filtered them) but frequent and slow: 897 build calls, 335 pristine builds at a median 18 s against 7.5 s incremental, 12 sessions writing their own wrapper. Only 3 builds went through the MCP tool, whose successful answers were 26.9 KB and 19.9 KB.
- PD protocol logs were not a token hog: only 94 tool results carried five or more Zephyr log lines (0.2 MB), because the helpers filtered them (`grep -v PRL_`, `head -40`), and only 10 assistant messages rebuilt a PD message sequence by hand. A trace decoder is below the 1% threshold; the console draft's filters cover the filtering.
- Wall time sits in builds (5.3 h of main-thread tool time), subagent waits (3.7 h) and bench calls (2.9 h); reading source costs model time instead (about 4.7 h outside review subagents, 38 h summed over all agents, at most 600 s counted per turn).
