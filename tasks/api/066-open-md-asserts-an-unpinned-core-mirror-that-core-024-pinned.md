# 066 — `open.md` still asserts Core's wire mirror is unpinned; `core/024` pinned it

**State:** claimed by agent/api/066-open-md-mirror, 2026-09-11 20:12 (leg 084)
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

- [ ] The bullet is **rewritten, not deleted** — the unpinned-mirror episode is real history and
      `embarch-topology` decision 20 is still the reason the pinning exists. What changes is the
      claim about Core: say both halves are pinned against the same literals, name the two test
      functions and `tasks/core/024`, and keep the standing fact that the two literals are a
      **copy, not a shared constant**, and that a disagreement between them is itself the finding.
      If nothing about the bullet is open any more, it belongs in `decisions/` or in the test's own
      comment rather than in `open.md` — say which you chose and why.
- [ ] **Every other bullet in `embarch-api/open.md` that asserts something about a repo other than
      `embarch-api` is re-checked against that repo's current source**, and each one is either
      confirmed (say so in the task file, with the file and line you read) or corrected. There are
      several: the `embarch-umbrella` `artifact_path_for_core` scaffold, `embarch init` never
      writing `serial_port`, Core's deferred `{code, message, cause}` body, and Core's bounded
      `serial_log` endpoint. **Read the source, not the other repo's docs** — a doc that is stale
      the same way confirms nothing.
- [ ] **You may not edit `embarch-core`, `embarch-umbrella` or `embarch-topology`.** If a re-check
      finds a defect in one of those, write an `inbox/` drop at the absolute path
      `/home/gabriel/Github/embarch/embarch-doc/inbox/` and say so in the task file.
- [ ] Gate green: `python3 scripts/check-docs.py` in the doc repo, and `cargo build` / `test` /
      `clippy --all-targets -- -D warnings` in `embarch-api` (a docs-only diff on the code side is
      the expected outcome — say so rather than inventing a change).

## Out of scope

Actually closing any of the open questions you re-check. This unit corrects **what the file claims
is true today**; a question that is genuinely still open stays open, unchanged.
