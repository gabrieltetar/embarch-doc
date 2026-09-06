# 004 — `chip-list --help` routes the operator into a key that now fails config load

**State:** open
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

- [ ] `chip-list --help` and the two `chip_resolve.rs` comments name where the value actually
      goes, and say the table is compiled in.
- [ ] `embarch-core` decisions 8 and 34 no longer ground `chip-list` in a retired
      `embarch-api` field. Amend **in place**, in the heading as well as the body if the
      heading carries the claim.
- [ ] Nothing in `embarch-core` still says `soc_chip_overrides` — check with
      `grep -rn soc_chip_overrides embarch-core/`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/core-*` fragment
      dropped.
