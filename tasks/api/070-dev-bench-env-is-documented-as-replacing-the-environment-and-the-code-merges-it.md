# 070 — `[dev_bench] env` is documented as *replacing* the inherited environment, and the code merges it

**State:** open
**Source:** refill sweep for scope spread, leg 090, 2026-09-11. The line numbers below are as the
sweep reported them — **re-verify every one against the source before you act on it.**
**Scope:** api
**Hardware:** none.
**Owner:** no

## What

`embarch-api/interfaces/config.md` describes the same-named `env` field twice, with opposite
semantics, and the code has only one behaviour.

- **:78** (`[dev_bench]` row): *"**Replaces** the inherited environment rather than extending it.
  `cargo` must be on `PATH` for every board …"*
- **:44** (`[[projects]]` row): *"**Additive** over the inherited environment, not a replacement.
  PATH and toolchain setup stay with whatever launches this process"*

Both kinds funnel into one `BuildPlan.env` (`src/build.rs:49`) with two producers
(`src/resolve.rs` for projects, `src/dev_bench.rs:57` for dev-bench) and **one** consumer,
`src/build.rs:277`:

```rust
command
    .args(args)
    .current_dir(&plan.cwd)
    .envs(&plan.env)
```

`Command::envs` merges over the inherited environment; a replacement needs `.env_clear()`, and the
sweep reports `env_clear` appears nowhere in the crate. So the two config kinds are identical in
behaviour and the doc asserts a difference that does not exist.

## Why it costs something

Someone configuring a bench from that row believes they must re-declare `PATH`, `HOME` and the
toolchain variables in `embarch.toml`, or — worse — relies on an isolation from the launching shell
that is not there: a stray `ZEPHYR_BASE` or `ZEPHYR_SDK_INSTALL_DIR` in the MCP server's own
environment reaches every bench build silently. Both readings produce real wrong configuration.

Note the row's own rationale argues *against* its own claim: under a true replacement the inherited
`PATH` would be gone, and "`cargo` must be on `PATH`" could not hold.

## What to do

Correct the `[dev_bench]` row to say the field is additive, in the same register as the
`[[projects]]` row, **after confirming additivity from the code yourself** — count the producers and
consumers of `BuildPlan.env` and check for `env_clear` rather than trusting this task or either doc.
Keep the existing toolchain rationale; it is correct and it is the reason the row is worth reading.

**Do not make the code match the doc.** Changing the spawn to clear the environment is a behaviour
change that would need a numbered decision and would break every working bench config; the sweep and
this task both read additive as the intended and shipped behaviour. If your reading says otherwise,
stop and say so here rather than changing either side.

**Then check the rest of that file's rows against the code they describe.** Two rows of one table
disagreeing about one field name is a pattern worth one pass. Two candidates the sweep already
flagged, neither of which you must fix here:

- `:81` says an absent `[dev_bench]` errors from *"the three dev-bench tools"*; the sweep counted
  **four** call sites of `self.dev_bench_config()` (`src/tools.rs:767, 796, 824, 884`). If it is a
  plain miscount, fix it. If fixing it requires deciding whether `dev_bench_hello`/`dev_bench_link`
  belong in that sentence, that is a judgement — **report it here and leave it**, do not decide it.
- `interfaces/tools-dev-bench.md:5`'s parameter lists for `flash_dev_bench` /
  `build_and_flash_dev_bench` may not match `src/tools.rs`. Report what you find.

## Done when

- [ ] `interfaces/config.md`'s `[dev_bench]` `env` row states additive semantics, verified by
      reading `BuildPlan.env`'s producers and its single consumer.
- [ ] No code change and no new numbered decision.
- [ ] The `:81` count and the `tools-dev-bench.md` parameter lists are each checked and the result
      reported in this file, fixed only where the fix is a plain factual correction.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
