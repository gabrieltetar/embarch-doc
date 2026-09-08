# `POST /validate`'s JSON body never picks up `validated_at_utc_ms`

**State:** done — leg 042, 2026-09-07, branch `agent/core/026-validate-handler-2`.
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** core
**Hardware:** none

## Dispatch history (leg 042)

**First dispatch did nothing and its worktrees are quarantined.** The worker
spawned at 18:29 reported completion after ~33 seconds with a single sentence
of supervisor-shaped narration as its entire result ("That was a mistake — I'll
just wait quietly for the agent's completion notification now"), and a
`general-purpose` agent — not an `embarch-worker` — appeared under the leg's
session immediately afterwards. Both worktrees were clean with zero commits and
neither branch was pushed, so **no work was done and nothing was lost.**

`/home/gabriel/Github/embarch/.worktrees/embarch-core/026-validate-handler` and
`/home/gabriel/Github/embarch/.worktrees/embarch-doc/026-validate-handler`,
with the branch `agent/core/026-validate-handler`, are **left in place
deliberately and must not be reused.** An unidentified agent may still be
holding them, and `protocol.md`'s own rule is that nothing readable about a
worktree may retire the worker in it — leg 012 reused trees on exactly that
reading and ran two workers concurrently in them. The second dispatch uses
fresh paths (`026-validate-handler-2`) and the branch
`agent/core/026-validate-handler-2`. **A later leg should remove the first pair
once it can confirm nothing is running**, not this one.

## Supervisor direction (leg 042)

**This is not a wire-schema bump and does not take the §8 announcement route,
and the reasoning matters more than the conclusion.** `ops.md` §4 parks "any
change that bumps a wire schema version". This adds a field and changes
nothing that exists: `ok`, `role`, `hardware_id` and `confirmed_at_utc_ms`
keep their names, types and meanings, so every one of the four hand-maintained
mirrors keeps deserializing untouched, and `embarch-core/interfaces/topology.md`
already documents this response as open-ended rather than a closed schema
(`topology/009`'s reviewer checked exactly that). **If you find that
characterisation is wrong** — the response is declared closed somewhere, or a
mirror uses `deny_unknown_fields`, or there is a version constant to move —
**stop and write it into this task file rather than proceeding.** That would
make this a `suite` unit that a `core` worker may not land.

**Do not rename or re-meaning `confirmed_at_utc_ms`.** The previous leg closed
that arm deliberately: it is wire-visible across four repos and is `suite`
work. Both timestamps ship side by side.

**Keep `validate_serial`/`validate_role` callable.** Topology deliberately
left the old signatures intact and added `_timed` variants; your job is to
switch Core's `POST /validate` handler to the `_timed` variant, not to remove
anything.

**Record the addition as an `embarch-core` decision.** `decisions/surfaces.md`
is the likely home (5,809/12,288 B — plenty of room) unless the file layout
says otherwise; the decision should say the field is additive, that four repos
mirror this shape by hand, and that the three consumers are already filed
(`tasks/api/045`, `tasks/umbrella/041`, `tasks/ui/020`, all blocked on this
task).

**Doc-size reserve for `core`:** `embarch-core/open.md` is at 4,478/5,120 B —
**642 bytes left**, and its compaction task `tasks/core/022-compact-core.md` is
**blocked on `In flux: yes`**. Prefer not to write `open.md` at all. If your
work genuinely needs an open question recorded there, compact that file as
part of this unit, carrying `tasks/core/022`'s `Must not delete:` list and
closing only `open.md`'s item on it. Every other `embarch-core` doc has room.

**Hardware:** none, and do not touch the live Core, the bench, or any board.
This is a handler change plus host tests.

## What

`embarch-topology` decision 26 (2026-09-07) adds `validate_serial_timed`/
`validate_role_timed`, returning a new `Validation { board: EnrolledBoard,
validated_at_utc_ms: u64 }` alongside the unchanged `validate_serial`/
`validate_role` — additive, so nothing broke. `embarch-core`'s own
`POST /validate` handler is the piece that actually assembles the wire
response (`{ ok, role, hardware_id, confirmed_at_utc_ms }`) from an
`EnrolledBoard`, and it is a **direct in-process caller** of these functions
(topology is linked live, not called over the wire) — so it is the one place
that has to switch to the `_timed` variant and add `validated_at_utc_ms` to
that JSON body before the new field means anything to any consumer.

This is the consumer the supervisor's own enumeration for `tasks/topology/009`
did not name (it listed `embarch-api`'s core-client mirror and MCP tool,
`embarch-umbrella`'s doctor, `embarch-ui`'s Topology tab) — worth flagging on
its own, since without this half none of those four ever see the field.

## Why now

The observed defect (`tasks/topology/009`): two `validate` calls minutes or
days apart both return the same `confirmed_at_utc_ms`, which is enrolment
time, not the live check's — a caller reading it as freshness gets a
plausible, wrong answer, silently, in the safe-looking direction.

## Done when

- [x] `POST /validate`'s handler calls `validate_role_timed`/
      `validate_serial_timed` and adds `validated_at_utc_ms` to the response
      body, alongside the unchanged `confirmed_at_utc_ms`. (The handler only
      ever called `validate_role` — `validate_serial` is used by
      `hardware::flash`/`reset`'s own internal re-checks, not by this
      endpoint, so only `validate_role_timed` needed switching here;
      `validate_serial`/`validate_role` are both left callable, per the
      supervisor direction above.)
- [x] A decision records the wire-schema addition (this is `suite`-visible —
      four repos share this response shape by hand-maintained mirror), and
      `embarch-api`, `embarch-umbrella`, `embarch-ui` each pick it up in their
      own time since every existing mirror keeps deserializing regardless.
      `embarch-core/decisions/surfaces.md` decision 50 (numbered 50, not 29 —
      decision numbers are global across `decisions/*.md`, not per file; the
      directory-wide max was 49 before this).

## Verification (this dispatch)

**Additive-only claim checked, not assumed** (per the supervisor direction
above): grepped `deny_unknown_fields` across `embarch-core`, `embarch-api` and
`embarch-ui` — the only hits are unrelated (`embarch-api/src/config.rs`'s
config-file struct; a code comment in `embarch-ui/src/study_designer.rs`
explicitly noting `Study`'s own deserializer has none). `embarch-api`'s wire
mirror, `embarch-core-client::ValidateResponse`, derives plain `Deserialize`
with no field-closing attribute. No schema-version constant exists for this
endpoint to move. `embarch-core/interfaces/topology.md`'s `/validate` row
already documents the response with a trailing `…`, i.e. open-ended. This is
additive; the change is landed as a `core`-only unit, not escalated to
`suite`.

**Handler + response shape:** `src/api.rs`'s `validate_handler` now calls
`embarch_topology::hardware::validate_role_timed`, and `ValidateOkResponse`
gained `validated_at_utc_ms: u64` alongside the unchanged `confirmed_at_utc_ms`
field, same names/types/meanings on every other field.

**Gate:** `cargo build`, `cargo test` (169 passed, 0 failed, 2 ignored),
`cargo clippy --all-targets -- -D warnings` all clean in the code worktree.
`python3 scripts/check-docs.py` and `check-ownership.py --scope core` /
`--code-repo` run clean in the doc worktree (see commit for exact output).

**Left for later, not this unit:** `features.d/topology-105-validate-reports-
when-the-live.md`'s `Status` caveat ("`embarch-core`'s `/validate` … have not
switched over") is now half-stale — it's `topology` scope, so I dropped an
`inbox/` request rather than edit it myself. `open.md`'s 642 bytes of headroom
were not touched — nothing here needed it.
