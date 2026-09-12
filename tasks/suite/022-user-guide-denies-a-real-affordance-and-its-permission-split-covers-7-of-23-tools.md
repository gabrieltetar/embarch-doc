# 022 — Two sections of `suite/user-guide.md` are wrong where it matters: §6 denies a config discovery that exists, and §7.1's permission split covers 7 of 23 MCP tools

**State:** open — **announced, window running.** Leg 085, 2026-09-11: posted to `#embarch-fleet`
at `ts 1789179351.424089`, which opens `ops.md` §4's 30-minute silence-as-consent window. If this
leg ends before the window closes, the **next leg reads that `ts` and completes the window rather
than restarting it** (`.claude/leg.md`). A reply saying go runs it now; a cancel drops this back to
plain `open` with the reply quoted here.
**Source:** suite review pass 2026-09-06, dimension 7 (the newcomer). Both halves code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Two independent defects in the one doc `embarch.md` §6 sends a newcomer to first. Filed together
because they are in one file, and that file is **23,246 B against a 23,040 B reserve line**
(`tasks/suite/004`) — so it must not grow, and both fixes shrink or hold it.

**1. §6 tells the reader an affordance does not exist that does.** Lines 170 and 184:

> *"Every invocation needs to know which config to use — **there is no auto-discovery the way
> `doctor` and `init` have.** Point at it once per shell, or pass `--config` every time"*
> *"Without either, **every one of these — including `list-projects`** — exits immediately with
> `no config path given`."*

The real order is `--config` → `EMBARCH_API_CONFIG` → **a cwd-upward search for
`embarch/embarch.toml`** (`embarch-api/src/main.rs:391-402`, wired in at `:481`). The error text
itself says so: *"no config path given: pass --config <path>, set EMBARCH_API_CONFIG, or run from
within (or under) a firmware repo containing embarch/embarch.toml"* (`:483-484`). It is documented
correctly at `embarch-api/interfaces/config.md:9` and decided at
`embarch-api/decisions/shape.md:26-29`, whose rationale is *"an engineer working across several
firmware repos has no single `EMBARCH_API_CONFIG` value that is ever correct."* §5 has just told
the reader to `cd` into their firmware repo, so they are standing in the case that works.

The belief is self-reinforcing: exporting the env var makes the search unreachable, so they never
discover it, and the first thing that breaks is exactly the case decision 25 was written for.

**2. §7.1's permission split — the only safety guidance in the suite — classifies 7 of 23 MCP
tools, and omits every destructive one.** Line 204:

> *"**Reading and building are safe and frequent; anything that touches the board should be a
> decision you make.** A reasonable split in `.claude/settings.local.json`: allow
> `list_projects`, `status`, `build` and `serial_log`; ask for `flash`, `build_and_flash` and
> `reset`."*

`grep -c 'tool(description' embarch-api/src/tools.rs` → **23**. Unclassified and either
hardware-touching or state-writing: `flash_dev_bench`, `build_and_flash_dev_bench`,
`reset_dev_bench`, `enroll_probe`, `validate`, and **`run_study`** — which with `reflash`
*"build[s] and flash[es] from the working tree AS IT CURRENTLY STANDS"* on **both** boards
(`embarch-api/src/tools.rs:919`).

The split is not framed as illustrative; it is the answer to the section's own question. The count
drifted silently as the surface grew, and the suite's own record of the guidance never noticed:
`embarch-promptu/design.md:7` still restates the same seven and says `embarch init` registers
*"nine (and growing) MCP tools."*

Candidate direction for both: correct §6 to state the three-step resolution, leading with the
cwd-upward case; make §7.1 exhaustive over the tool surface, and consider keeping it that way
mechanically — most cheaply by deriving the tool list the way `tasks/api/034` proposes to, so a
new `#[tool]` that no allow/ask list names fails a check.

## Why now

A newcomer who follows §7.1 believes anything touching their board will ask first, and six
hardware-touching tools are left at whatever their client defaults to. And §6 teaches an
unnecessary step per shell that gets actively worse the moment they own a second firmware repo.
Neither is visible to any other check: both sections are internally coherent, and only a reader
who follows the newcomer's *order* — guide, then code — meets the contradiction.
`embarch-promptu` is Planned with no repo, so this prose is what exists today.

## Done when

- [ ] §6 states `--config` → `EMBARCH_API_CONFIG` → cwd-upward search, and no longer claims
      `list-projects` fails without the first two.
- [ ] §7.1's split names every MCP tool `embarch-api` exposes, on one side or the other.
- [ ] `suite/user-guide.md` is no larger than it is now.
- [ ] `embarch-promptu/design.md`'s restatement of the split and its tool count are corrected or
      pointed at §7.1 rather than restating it.
- [ ] Gate green.

**Note:** `tasks/suite/004` lists `suite/user-guide.md` under `Compacts:` but is a byte-count task
whose `Must not delete` names only §5.1's placeholder argument. A false factual claim in §6 is not
what it asks anyone to fix; these fixes are compatible with it and reduce the byte count.
