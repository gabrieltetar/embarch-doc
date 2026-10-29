# 122 — Two capture-timing tests fail about one full `cargo test` run in four, on `main` too

**State:** claimed by agent/core/122-capture-timing-flakes, 2026-10-28 21:55 — re-claimed for a resume: the 17:25 worker died with its leg at ~17:35 holding an uncommitted two-test fix (`capture.rs`, `host_study.rs`), committed by the next leg's recovery as `a24c7d7` on the code branch (unverified, not yet run 20 times); the worktrees are kept and a fresh worker continues from it.
**Reserve at dispatch (2026-10-28):** `embarch-core/spec.md` 462 B left, `open.md` 316 B left, `decisions/probes.md` 1,025 B left, all filed on `core/112`, blocked on `In flux: yes`. Do not grow them; if this unit must edit one, compact that file as part of the unit, carrying `core/112`'s `Must not delete:` list, and strike only that file off `core/112`'s `Compacts:` line (delete it, say so in the body).
**Source:** `suite/048`'s landing, 2026-10-28: the supervisor's gate on the merge result went red once on a test the unit did not touch, and repeated runs showed the same two tests failing on unchanged `main`. Measured: 2 failures in 7 full runs at `52d4659` (before the unit), 2 in 10 on the unit's branch; never in isolation (9 of 9 single-test runs passed).
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Two tests in `embarch-core` fail intermittently under a full parallel `cargo test` and pass alone:

- `host_study::tests::two_tapped_consoles_with_exchanges_on_both_are_each_opened_once_and_lose_nothing` — panicked at the assertion on one tap's text, which held `"pd role\nresult\r\n> dut: attach\ndut: contract 9V\n"`.
- `capture::tests::lines_carry_receive_times_and_offsets_match_text_across_a_gap`.

Both drive in-process fake serial pairs with real time between writes and reads (decisions 92, 98), so they are sensitive to how busy the machine is. When this is done, both pass reliably under a full parallel run (find what each waits on by wall clock and wait on the condition instead), or the test says in its own comment why a timing margin is the only option and the margin is wide enough that 20 consecutive full runs pass.

## Why now

A supervisor re-runs the gate on every merge result and a red gate blocks a unit (protocol §6). A flake that fails one run in four either blocks real work or teaches the supervisor to re-run until green, which is the habit that lets a real failure through.

## Done when

- [ ] Both tests pass in 20 consecutive full `cargo test` runs.
- [ ] No production code changed unless a test found a real race; if it did, that is a decision.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.
