# 055 — `spec.md` says `setup` and `init` each end by running `doctor`, and neither of them does

**State:** claimed (leg 090, 2026-09-11)
**Source:** refill sweep for scope spread, leg 090, 2026-09-11. The line numbers below are as the
sweep reported them — **re-verify every one against the source before you act on it.**
**Scope:** umbrella
**Hardware:** none.
**Owner:** no

## What

`embarch-umbrella/spec.md`'s command table asserts a step neither command takes.

- **:53** (`embarch setup`): *"Detect topology, install Core as a service, … record the class and the
  Windows-side Core path, **then run `doctor`**."*
- **:54** (`embarch init`): *"Scaffold the repo's `embarch/` config, exclude it locally, register the
  MCP server, **then run `doctor`**."*

`doctor::doctor` has exactly one call site in the crate — the `doctor` subcommand itself,
`src/main.rs:184`:

```rust
Command::Doctor { json } => doctor::doctor(json).await,
```

Both commands instead end by *pointing at something else*: `src/setup.rs:377` prints *"Next:
`embarch status` to confirm, then `embarch init` in a firmware repo."*, and `src/init.rs:854` prints
*"Then: `embarch status`, and `embarch-api --config … build {name}`."* The sweep reports no spawn of
an `embarch doctor` process anywhere either.

## Why it costs something

`spec.md` is the file an operator or an agent reads to know what a command does. Read as written, a
clean `setup` means the seventeen-check chain has run and passed — so a green-looking setup is taken
for a **verified** chain when nothing verified anything. It also mis-scripts an agent that skips a
`doctor` call on the grounds that setup already made it.

## What to do

**Correct the doc, not the code.** Make both rows say what the commands actually end with — a
next-step pointer — verified by finding every call site of `doctor::doctor` yourself and by reading
the tail of `setup.rs` and `init.rs` rather than trusting this task.

**Do not make `setup`/`init` chain into `doctor`.** That is a behaviour change, it would need a new
numbered decision, and this task is not authority for it. If your reading says the chaining was
genuinely intended and the code is the stale side, **stop and say so here** — a fork recorded is
worth more than a guess acted on.

**Then check the rest of that table's rows against their subcommands.** Two adjacent rows asserting
the same non-existent step is a pattern worth one pass.

## Two adjacent instances the sweep also flagged

Fix them only if each is a plain factual correction; report either one you leave.

- `src/doctor.rs:67` — `Check.code`'s doc comment says *"Checks 1, 5, 10 and 14 carry one today"*,
  but 13 (`not-configured`/`stale`/`unresolvable`) and 17 (`bind-*`) carry one too.
  `interfaces/doctor-chain.md:111` already has the correct six (1, 5, 10, 13, 14, 17), so here it is
  the **code comment** that is stale — the opposite direction from the defect above, which is the
  reason to fix both in one pass rather than assume the docs are always the wrong side.
- `Cargo.toml:31` cites `decisions/doctor.md 33` for the `embarch-study-designer` dependency;
  decision 33 lives in `decisions/schema-skew.md` (`doctor.md` holds 18, 31, 42). Same miscitation
  class `umbrella/043` and `core/008` found — the settled form is bare `decision M` same-repo,
  `` `<repo>` decision M `` cross-repo.

## Done when

- [ ] `spec.md`'s `setup` and `init` rows describe what those commands actually do at their end,
      verified against every `doctor::doctor` call site.
- [ ] No behaviour change and no new numbered decision.
- [ ] `src/doctor.rs:67`'s comment and `Cargo.toml:31`'s citation are each checked, and fixed or
      reported here.
- [ ] A pass over the rest of `spec.md`'s command table is reported here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
