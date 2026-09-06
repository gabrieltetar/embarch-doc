# 004 — `chip-list --help` routes the operator into a key that now fails config load

**State:** done, 2026-09-05, on `agent/core/004-chip-list-help`
**Source:** `api/017`'s reviewer, 2026-09-05, reviewing merge `4ef324f` / `495a7bf`. Not a
contradiction — help text is not a decision — so it was reported rather than dropped in
`inbox/`, and filed here by the supervisor.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`api/017` **retired** `embarch-api` decision 13: the per-project `soc_chip_overrides` table
is gone, and a config still declaring the key is now **refused at load**, on both discovery
kinds, naming the retirement.

`embarch-core`'s own user-facing text still sends people there:

- `embarch-core/src/main.rs:100` — the `ChipList` clap doc comment, i.e. what
  `embarch-core chip-list --help` prints: *"This is where the value for an `embarch-api`
  `soc_chip_overrides` entry comes from when a SoC isn't in the built-in table."*
- `embarch-core/src/chip_resolve.rs:105` and `:182` — two module comments saying the same.
- `embarch-core/decisions/probes.md` 8 and 34 ground `chip-list`'s existence in "configuring
  an override for an unmapped SoC."

So an operator who follows Core's own help writes a key that stops `embarch-api` from
starting. `chip-list` itself is **not** obsolete — it still produces exactly the string the
new remedy asks for; what changed is where that string goes. Fix the destination, do not
delete the tool.

**Where the string goes now, and the second half of this task.** The api refusal says *add
the mapping to Core's own SoC→chip table*, and that table is a source `const` —
`SOC_TO_CHIP` at `embarch-core/src/chip_resolve.rs:26`, with **no config path at all**. So
the honest remedy is "edit Core's source and redeploy", and neither `chip-list --help` nor
the api error says so. A reader will hunt for a config file that does not exist.

`embarch-api` decision 13's tombstone already names *a Core the operator cannot rebuild* as
the condition that would reverse the retirement, so the rebuild requirement is deliberate and
recorded — **this task is not the place to add a config path for the table.** It is the place
to stop the text implying one exists. If you conclude the text cannot be made honest without
that config path, say so in the decision entry and file it separately rather than building it
here.

## Why now

It is a live dangling cross-repo reference in the surface text an operator reads at exactly
the moment they are stuck, and this suite spent `api/015` learning what that costs. Cheap:
three comments and a decision amendment.

## Done when

- [x] `chip-list --help` and the two `chip_resolve.rs` comments name where the value actually
      goes, and say the table is compiled in. **Two more sites were fixed than the three
      named**, both the same defect: the `SOC_TO_CHIP` const doc (now states it is the only
      place a mapping can live), and — the one an operator actually hits — `UnmappedSoc`'s
      `Display`, the text of the `/resolve-chip` 404, which still said *"run `probe-rs chip
      list` (or `embarch-core detect-dev-bench`'s sibling chip-list item, once it exists)
      … and configure it manually"*. Stale twice over: `chip-list` exists, and "configure it
      manually" is the config file that does not exist. It now names `chip-list`, the
      `SOC_TO_CHIP` edit, and the rebuild.
- [x] `embarch-core` decisions 8 and 34 amended in place. The heading gained "compiled in";
      the body's *"configuring an override for an unmapped SoC"* became *"finding a probe-rs
      target name for"*, and two paragraphs were added — one recording what the entry used to
      say and where the string goes now, one rejecting a config path for the table and
      pointing at `embarch-api` 13's tombstone for why the rebuild requirement is a recorded
      choice. `embarch-core/interfaces.md`'s `/resolve-chip` row now names the remedy too.
- [x] `grep -rn soc_chip_overrides` over the code worktree returns nothing.
- [x] `changelog.d/core-chip-list-points-at-the-table.fixed.md` dropped. Gate: `cargo build`,
      `cargo test` (171 pass), `cargo clippy --all-targets -- -D warnings`, `check-docs.py`
      (9/9), `check-client-names.py` and `check-ownership.py` on both branches all green.
      **`cargo build --target x86_64-pc-windows-msvc` is red and was red before this unit** —
      see `## Note` below.

## Note — the Windows-target gate item is not runnable here

`cargo build --target x86_64-pc-windows-msvc` fails in `hidapi`'s build script, which
compiles `etc/hidapi/windows/hid.c` with the host `cc`; WSL has no MSVC C compiler or
Windows SDK. Confirmed pre-existing by stashing this unit's diff and re-running on the
untouched base — identical failure. Nothing here is `#[cfg]`-gated: the diff is doc
comments and one `write!` format string, all compiled on every target, and the Linux
build, tests and clippy cover them.

Dropped as `inbox/core-windows-target-build-unrunnable-in-wsl.md`, because the fix is
either build tooling or a `protocol.md` §10 wording change and neither is a worker's.
