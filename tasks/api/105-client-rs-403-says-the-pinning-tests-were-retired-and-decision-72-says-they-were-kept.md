# 105 — `client.rs`'s line-403 comment says the pinning tests were retired; decision 72 says they were kept

**State:** claimed by agent/api/105-pinning-tests-kept-not-retired, 2026-09-16 20:57
**Source:** `inbox/api-104-review-client-rs-403-contradicts-decision-72.md` — filed by the
`embarch-reviewer` spawned for unit `api/104`, drained into the queue by the supervisor on
2026-09-16.
**Scope:** api
**Hardware:** none — a comment reword in a Rust source file; confirming it needs no board and
nothing here executes.
**Owner:** no

## What

`crates/embarch-core-client/src/client.rs:398-418` asserts a fact about what shipped that is
false, and cites the decision that says the opposite as its authority. The block closes:

> "**Those tests are retired with the types they pinned** — the guarantee is now structural, since
> there is one type and Core and this crate both name it (`embarch-api` decision 72)."

`embarch-api` decision 72 (`decisions/client-crate.md`) says, in its own words:

> "**The pinning tests are kept, and that is the part that is not a refactor.** ... The literals
> are the only thing positioned to notice, so **they stay** — re-scoped from 'our copy matches
> theirs' to 'the wire has not moved under a deployed Core'."

Two further things in the same file confirm decision 72 rather than line 403: the comment at
`client.rs:~2006-2020` states the re-scoping correctly and explicitly ("*not retired with the
mirror it used to guard*"), and the three round-trip tests it describes
(`a_declared_signal_serializes_to_the_shape_core_parses`,
`an_alert_round_trips_against_the_pinned_shape`,
`an_enrolled_board_round_trips_against_the_pinned_shape`) are **present and passing** today.

So the file contradicts itself, and the half that is wrong is the half a reader meets first.

Reword lines 407-413 so they say the pinning tests were **kept and re-scoped**, consistent with
decision 72 and with the file's own later comment. **The decision-number citations at line 403
(37, 38, and the `embarch-topology` 31 citation) are correct and are not what this task is
about** — leave them alone; the defect is the prose built on top of them.

## Why now

This is the first time in the `doc/069` plural-citation sweep chain that a **"0 false sentences"**
verdict has been shown to be wrong, and it was `api/104`'s. The falsehood sits one clause past the
citation it cites, which is exactly the blind spot of a sweep methodology that checks "does the
number resolve, and does the immediate sentence read true".

The wrong sentence does **not** originate with `api/104` — `git log -S` traces it to `7d817a3`
(`suite/035`, which retired the seven hand-mirrored `embarch-topology` types) and it survived
`api/100` (`b1f99b9`) and every commit since. `api/104` read it and signed it off. So this is a
correction to shipped prose, **not a revert of anything**.

## Done when

- [ ] `crates/embarch-core-client/src/client.rs:407-413` states that the round-trip pinning tests
      were kept and re-scoped — "the wire has not moved under a deployed Core" — rather than
      retired, and stops contradicting the same file's comment at ~line 2012.
- [ ] The three decision-number citations in that block are unchanged and still resolve.
- [ ] Nothing else in the block's account of the mirror retirement changes — the *types* were
      genuinely retired by `suite/035`; only the claim about the *tests* is wrong.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test --workspace`, `cargo clippy --all-targets -- -D warnings` in `embarch-api`, and
      `check-docs.py` in `embarch-doc`.
- [ ] `changelog.d/` fragment dropped. No decision is created or amended: decision 72 already says
      the right thing and is not being touched.

## Notes for whoever runs this

- **Do not amend decision 72.** It is correct; the source comment is what is wrong.
- The reviewer's full reasoning, including the `git log -S` trace and the exact quotes, is in the
  unit `api/104` entry of `../../embarch-fleet/supervisor-log.md` (2026-09-16 20:47).
- `tasks/api/104`'s own result table, now retired, labelled this citation "correct". That verdict
  was wrong and is superseded by this task; nothing needs to be done about the retired file.
