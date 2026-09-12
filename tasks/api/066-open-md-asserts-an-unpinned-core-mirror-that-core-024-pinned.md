# 066 — `open.md` still asserts Core's wire mirror is unpinned; `core/024` pinned it

**State:** done — leg 084, 2026-09-11
**Source:** leg 084's refill sweep off `embarch-api/open.md`, 2026-09-11. Code-confirmed before
filing — this is a reconciliation, not a suspicion.
**Scope:** api
**Hardware:** none
**Owner:** no

**Reserve in `embarch-api` at dispatch (leg 084):** `embarch-api/open.md` is **out** of reserve
(73.8%) and this unit should keep it that way — `tasks/api/060` is the item that will be closed if
you leave it out. Two decision files are **over cap and parked**: `decisions/zephyr.md`
14,269/12,288 B (`tasks/api/057`, `In flux: yes`) and `decisions/core-link.md` 13,164/12,288 B
(`tasks/api/061`, `In flux: yes`). **Do not file anything into either.** This unit is not expected
to need a decision at all; if you find one is genuinely owed, stop and say so in the task file
rather than choosing whichever file has room — that exact move is how `api` filed a decision in the
wrong topic file on 2026-09-05. If your work leaves any `embarch-api` file in reserve that nothing
has filed, file `tasks/api/<NNN>-compact-api.md` in the same commit.

## What

[`embarch-api/open.md`](../../embarch-api/open.md) carries this bullet:

> **The alert/enrolled-board response types were unpinned mirrors**: `link_port_interface`
> (`embarch-topology` decision 20) reached Core's wire body and the client mirror silently dropped
> it. `api`'s half is pinned against a JSON literal now (task `032`); **Core's is not** — filed to
> `embarch-core`'s inbox.

**Core's half is pinned.** `embarch-core/src/api.rs` now carries
`ENROLLED_BOARD_RESPONSE_JSON` and `ALERT_RESPONSE_JSON` and two tests —
`enrolled_board_round_trips_against_the_client_s_pinned_shape` and its `Alert` sibling — against
**the same JSON literals** this crate's `an_enrolled_board_round_trips_against_the_pinned_shape`
and `an_alert_round_trips_against_the_pinned_shape` use, `link_port_interface` included. The
comment above them names `tasks/core/024` as the unit that did it and states the interlock
explicitly: *"if the two literals below and the client-side ones ... ever disagree, that
disagreement (not just a red test here) is the finding."*

So the open question is **answered**, and the bullet now misdirects in the expensive direction: it
tells the next reader that a cross-repo wire mirror is unguarded when it is guarded, which is an
invitation either to re-do `core/024` or to distrust a test that is doing its job.

## Why now

An `open.md` bullet that names **another repo's** state is the shape most likely to go stale
without anything failing — nothing in the gate compares a sentence in this repo against a test in
that one. This is the second such staleness this queue has found in a week
(`suite/019` found three in one task), so the sweep below is the actual value of the unit; the one
bullet is the entry point.

## Done when

- [x] The bullet is **rewritten, not deleted** — the unpinned-mirror episode is real history and
      `embarch-topology` decision 20 is still the reason the pinning exists. What changes is the
      claim about Core: say both halves are pinned against the same literals, name the two test
      functions and `tasks/core/024`, and keep the standing fact that the two literals are a
      **copy, not a shared constant**, and that a disagreement between them is itself the finding.
      If nothing about the bullet is open any more, it belongs in `decisions/` or in the test's own
      comment rather than in `open.md` — say which you chose and why.

      **Chose: the test's own comment, not `decisions/`.** Nothing about this bullet is open any
      more — both halves are pinned, `core/024` closed it — so it is not `open.md` material at all.
      The topical decision home would be `decisions/core-link.md` ("Reaching Core"), but that file
      is over cap and parked (this unit's reserve line forbids filing into it), and no other
      decisions file is a topical fit for a client/Core wire-mirror pinning contract. So the bullet
      is **deleted from `open.md`** (`embarch-api/open.md`) and its content moved into the two stale
      code comments it corrects: `crates/embarch-core-client/src/client.rs`, the doc comments on
      `an_alert_round_trips_against_the_pinned_shape` and
      `an_enrolled_board_round_trips_against_the_pinned_shape` (both `#[cfg(test)] mod tests`).
      Both previously said "the Core-side counterpart test ... does not exist yet"; both now name
      `embarch-core`'s `alert_round_trips_against_the_client_s_pinned_shape` /
      `enrolled_board_round_trips_against_the_client_s_pinned_shape` (`src/api.rs`,
      `tasks/core/024`) and restate the interlock: a disagreement between the two literals, not
      just a red test here, is the finding. This keeps the mirror-contract fact exactly where a
      future editor of these tests will read it, rather than in a doc file three hops away.

- [x] **Every other bullet in `embarch-api/open.md` that asserts something about a repo other than
      `embarch-api` is re-checked against that repo's current source**, and each one is either
      confirmed (say so in the task file, with the file and line you read) or corrected. There are
      several: the `embarch-umbrella` `artifact_path_for_core` scaffold, `embarch init` never
      writing `serial_port`, Core's deferred `{code, message, cause}` body, and Core's bounded
      `serial_log` endpoint. **Read the source, not the other repo's docs** — a doc that is stale
      the same way confirms nothing.

      All four re-checked against source, all still true, no edits needed:

      - **`embarch-umbrella` still scaffolds `artifact_path_for_core`.** Confirmed:
        `embarch-umbrella/src/config.rs:101` (`pub artifact_path_for_core: Option<String>`),
        `embarch-umbrella/src/init.rs:534` (still emitted for a `static` project on a WSL2 split),
        `embarch-umbrella/src/doctor.rs:1373-1471` (check 9 still reads it). `list_targets`/
        `soc_chip_overrides` are refused by name (`embarch-api` decision 64) while this one still
        loads unread, per the bullet.
      - **`embarch init` never writes `serial_port`.** Confirmed by absence: no occurrence of
        `serial_port` anywhere in `embarch-umbrella/src/init.rs` (only a field declaration at
        `config.rs:363`, never populated by the init writer).
      - **Core's `{code, message, cause}` body is deferred, not built.** Confirmed by absence: no
        `ErrorBody`/`error_kind`/`{code, message, cause}` construct anywhere under
        `embarch-core/src/`. `api.rs`'s handlers still return plain-text error bodies, matching
        `embarch-api` decision 50's account.
      - **Core's `serial_log` endpoint is still bounded, not streaming.** Confirmed:
        `embarch-core/src/serial.rs:43` (`serial_log_max_bytes()`) and
        `embarch-core/src/api.rs:577-601` (`serial_log_handler` enforces `max_bytes`), plus its own
        tests `serial_log_over_the_duration_cap_is_a_bad_request_naming_both_numbers` and
        `serial_log_at_the_duration_cap_is_unchanged` (`api.rs:1135-1170`) — still one-shot and
        capped, no streaming route added.

- [x] **You may not edit `embarch-core`, `embarch-umbrella` or `embarch-topology`.** If a re-check
      finds a defect in one of those, write an `inbox/` drop at the absolute path
      `/home/gabriel/Github/embarch/embarch-doc/inbox/` and say so in the task file.

      No defect found in any of the three — nothing dropped to `inbox/`. Only `embarch-api` (code
      and doc tree) was touched.

- [x] Gate green: `python3 scripts/check-docs.py` in the doc repo, and `cargo build` / `test` /
      `clippy --all-targets -- -D warnings` in `embarch-api` (a docs-only diff on the code side is
      the expected outcome — say so rather than inventing a change).

      All green. The code-side diff is **not** docs-only: it also rewrites two stale doc comments in
      `crates/embarch-core-client/src/client.rs` (test-module documentation, not behavior) — no
      production code, no test assertions, no `Cargo.toml` changed. `cargo build`/`test`/
      `clippy --all-targets -- -D warnings` all pass with no new warnings. Doc gate
      (`check-docs.py`, 11/11 checks), `check-client-names.py --repo` (clean), and
      `check-ownership.py` (both `--scope api` in the doc worktree and `--code-repo` in the code
      worktree) all pass.

## Out of scope

Actually closing any of the open questions you re-check. This unit corrects **what the file claims
is true today**; a question that is genuinely still open stays open, unchanged.
