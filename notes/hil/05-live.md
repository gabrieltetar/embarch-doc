# HIL notes: Live access

**Status:** draft, 2026-11-15.

## What Live is

**An instant read or action on the DUT or a bench board, during a development session.** No study, no report: an answer now, a line in the live log, and, when the answer settles something the documents left open, a fact written back to the atlas.

**"Close gaps in the documentation" means both:** the procedure closes the gaps in today's agent docs ([07-procedure-doc.md](07-procedure-doc.md#gaps-it-closes)), and a live finding closes a gap in the atlas.

## Reach and permission

- **Reach: the DUT and the bench's boards** (dev bench, PD partner and other companion boards). **Instruments are reached only through a Study or a Test.**
- **Free, no question asked:** reads (registers, memory, core state, stacks, serial log), resets, **any shell command on the DUT or a bench board.** Kept after review round 1, which proposed a project list of destructive DUT commands that ask (owner: all stay free).
- **Asks every time:** flashing and bootloading, a read that clears what it reads (`reg_read_clear`), a read that writes a page select (`reg_read_bank`).
- **agent-guide.md §1.1 changes to match**: everything this list makes free moves from ask to allow, which is `reset`, `signal_exchange`, `mem_read`, `core_state` and `bench_exchange` in §1.1; **the atlas's own MCP server** has tools §1.1 does not list (`reg_read`, `shell`, `shell_run`, `live_stacks`, and its own `core_state`, which decodes what embarch-api's returns), and they get a list of their own there (review round 2, recommended). **The identity tools leave §1.1 and the MCP surface altogether** (`enroll_probe`, `unenroll_probe`, `set_role_board`, `declare_instrument`, `remove_instrument`, `declare_signal`, `remove_signal`, the bootload-port tools): they become the person's, made in the UI or the CLI with the person's token, and **the agent proposes them** ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)). A first Live session on a new bench therefore starts with the person enrolling its probes and declaring its signals, which the agent can no longer do alone (review round 2, recommended). The guide's lists and the procedure must not disagree.
- **The lease**: a short one (900 s, renewed by the MCP server), taken with a purpose, released at the end ([01-modes.md](01-modes.md#the-lease)).
- **Never during a run**: while a study or a test runs, Core refuses every Live call, reads included (owner, review round 1; [12](12-prevention.md#what-stays-outside-prevention-and-is-said-so)).

## With and without an atlas

**The atlas is optional.**

| | With an atlas | Without one |
|---|---|---|
| Registers | `reg_read`: decoded by field against the SVD, reset values marked, clock gate checked, read-to-clear guarded | `mem_read`: raw words |
| Where the core is | `core_state`: decoded, PC samples as functions and lines once the flash matches the ELF | `core_state`: raw words |
| Shell | `shell` / `shell_run`: the console picked from the build, output cleaned, five distinct answers | `signal_exchange` on a declared signal |
| Stacks | `live_stacks`, joined to the stack symbols | the shell's `kernel thread stacks`, raw |
| Write-back | yes | no |

The atlas half is the `embarch-atlas` repo's `DESIGN.md`, "Live (`live.py`)"; it reaches the board only through `embarch-api mem-read` and Core ([embarch-core live reads](../../embarch-core/decisions/live-read.md)).

## The live log

**Every live call is appended to `embarch/live/<date>-<session>.jsonl` in the firmware repo**, untracked like the rest of `embarch/`: what was read or sent, to which board, the image hash on it, the time, and the answer. **One file and one line shape, written by both embarch-api (raw calls) and embarch-atlas (decoded calls).** A write-back receipt points at its line.

## Writing a finding back

**A live answer that settles something the datasheet or schematic left open becomes a `measured` fact in the atlas, with its receipt**: the live call, the board's identity, the image hash, the time, the live-log line. It is shown beside the datasheet's claim, and **a disagreement with the datasheet becomes a check finding.** `measured` is already one of the atlas's provenance levels (`DESIGN.md`).

**A measured fact says how it was measured** (owner, review round 1): `via: live`, or `via: study` / `via: test` with the published zip's hash. **The atlas answers a `via: live` fact as development evidence**, so a Live result cannot be cited through the atlas when it could not be cited directly ([When Live is not enough](#when-live-is-not-enough)).

**A finding measured on an image other than the atlas's pinned build is still written, never refused**: the receipt records the image it was measured on, and the atlas shows it as measured on a different build. **That image is Core's `last_images` record** of what it last flashed on the chip; a board flashed outside EmbArch leaves that record wrong or absent, and an absent chip is recorded as unknown, never guessed ([lease tools](../../embarch-api/interfaces/tools-lease.md)). **So the receipt says which it is**: "read back" when the atlas's `image_check` matched the image, else "as last flashed by Core", which a flash outside EmbArch makes wrong (review round 2, recommended).

## When Live is not enough

**When a result is about to be cited** in a PR, a ticket or a report, **it is redone as a Study or a Test**, so it has a published receipt. A live answer stays development evidence.

## Open

- **Bench-board commands are free**, including ones that put power or protocol traffic on the DUT (a PD partner asking for 20 V). Recorded as decided, and review round 1's runtime envelope was declined (owner: safety is an authoring concern, [03](03-test.md#benches)); Live has no authoring step, so worth a second look once the first live session on the PD bench has run.
- **The write-back command**: an atlas CLI verb and MCP tool, its name and fields. The atlas rework's call.
- **The live log's fields.** To fix with the first writer.
