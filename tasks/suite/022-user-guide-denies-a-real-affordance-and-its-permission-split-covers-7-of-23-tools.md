# 022 — Two sections of `suite/user-guide.md` are wrong where it matters: §6 denies a config discovery that exists, and §7.1's permission split covers 7 of 23 MCP tools

**State:** done — leg 085, 2026-09-11. Announced to `#embarch-fleet` at `ts 1789179351.424089`,
opening `ops.md` §4's 30-minute silence-as-consent window; the channel was re-polled at the close
and twice in between, **0 actionable, no objection**, and this ran as the leg's last unit. The one
unmet checkbox is recorded in full below and carried by `tasks/suite/030`.
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

- [x] §6 states `--config` → `EMBARCH_API_CONFIG` → cwd-upward search, and no longer claims
      `list-projects` fails without the first two. It now leads with the cwd-upward case, since §5
      leaves the reader standing in it, and the code block `cd`s into the repo instead of
      exporting the variable. The closing line says why that order: **an export makes the search
      unreachable**, which is the self-reinforcing half of the original defect.
- [x] §7.1's split names every MCP tool `embarch-api` exposes, on one side or the other.
      **The surface is 29, not 23** — it drifted again between this task being filed on 2026-09-06
      and being run. Enumerated from `src/tools.rs` and classified against each tool's own
      description string, not by name: 17 allow (reads, plus `build`/`build_dev_bench`, which the
      descriptions state outright *"does not touch hardware"*), 12 ask. `run_study` and `validate`
      each get a sentence, because the first builds and flashes from the working tree as it stands
      on both boards, and the second is the only non-destructive entry on the ask side.
- [ ] `suite/user-guide.md` is no larger than it is now. — **Not met, deliberately, and filed as
      `tasks/suite/030` instead.** 23,796 → 25,044 B (97.8% of a 25,600 B cap, 556 B left). This
      checkbox rested on the filer's expectation that both fixes would shrink the file; the §6 fix
      roughly broke even and **the §7.1 fix could not shrink it, because making the split
      exhaustive over 29 tools cannot cost fewer bytes than naming 7.** A squeeze was considered
      and refused: the two squeezes this suite has run on full files each deleted a fact recorded
      nowhere else (`api/026`, `api/031`), and the part of this file that grew is the part that
      must keep growing by a line per new tool. `suite/030` carries the debt, dated 2026-09-18,
      with the split argument (§7 becoming its own agent-facing guide) and the one thing blocking
      it: a new `suite/*.md` needs a `DOC-BUDGET.md` cap entry, and that file is owner-reserved.
- [x] `embarch-promptu/design.md`'s restatement of the split and its tool count are corrected or
      pointed at §7.1 rather than restating it. **Both instances.** §1's *"nine (and growing) MCP
      tools"* — wrong when written and wronger since — now says "`embarch-api`'s whole MCP tool
      surface", naming no number. §2 item 1's inline copy of the seven-tool split is replaced by a
      pointer to §7.1 saying explicitly that the lists are not restated here **because a copy is a
      copy that goes stale**. That is the same defect this task exists to fix, so re-creating it
      one file away would have been perverse.
- [x] Gate green. 11/11.

**Note:** `tasks/suite/004` lists `suite/user-guide.md` under `Compacts:` but is a byte-count task
whose `Must not delete` names only §5.1's placeholder argument. A false factual claim in §6 is not
what it asks anyone to fix; these fixes are compatible with it and reduce the byte count.
