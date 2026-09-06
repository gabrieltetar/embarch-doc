# 019 — decision 20's refusal says "remove `west_binary`" and "add `west_binary`" in one message

**State:** done, agent/api/019-decision-20-remedy, 2026-09-06
**Source:** `api/017`'s reviewer, 2026-09-05, reviewing merge `4ef324f` / `495a7bf`. Reported
as an observation rather than a contradiction — both halves are individually correct — and
filed here by the supervisor.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Decision 20 refuses five zephyr-west-only fields at config load on a `static` project, and
`api/017` completed its second remedy so a reader following it literally no longer lands in
the next arm of the same `validate()`. That completion made the message
**self-contradictory for two of the five fields.** When the offending field is `west_binary`
or `build_dir_root`, it now reads, in substance:

> sets `west_binary`, which only a `discovery = "zephyr-west"` project can honour … Remove
> it, or set `discovery = "zephyr-west"` and drop `build_command`/`chip`/`artifact_path`,
> adding `west_binary` and `build_dir_root`, which it requires.

Remove `west_binary`, or add `west_binary`. Both branches are right — the second means
"switch kinds, and those two are then required, which you already have" — and the new test
`static_project_setting_any_zephyr_only_field_fails_validation` exercises both fields and
passes. **The sentence is confusing exactly where the fix was aimed.**

**A one-line conditional tail settles it**: when the offending field is already one of the two
the `zephyr-west` arm requires, the second remedy should not list it again — it should say
the field is *kept* and name only what else is needed. Keep it to one clause; this is a string
and a test, not a redesign of the message.

**Three postures already exist for one class of config mistake** — this refusal, decision 53's
retired-key refusal, and decision 51's absent-stays-absent — and `api/016` explicitly declined
to add a fourth. **Do not add one here.** If you find the message cannot be made
non-contradictory without changing posture, that is a finding worth writing into decision 20
rather than a licence to change it.

## Why now

`api/015` was itself a reviewer find about remedy text that misadvised a zephyr project, and
decision 51 is the record of it. This is the same sub-project, the same class, and one
sentence. It is also the last loose end of the decision-20 thread that has now run through
`015`, `016` and `017`.

## Reserve

`embarch-api/decisions/zephyr.md` sits at **10,962 / 12,288 B (89.2%)** — *not* in reserve,
so nothing may be filed against it (`DOC-COMPACTION.md` §5), and one edit puts it in.
`api/017` reported this explicitly as the state the next `api` unit walks into. If your edit
crosses 90%, file `tasks/api/<NNN>-compact-api.md` in the same commit per `tasks/README.md`.
Amending a string's description in place is the cheap way to stay under; adding a new
paragraph is not.

## Done when

- [x] The refusal message is not self-contradictory for any of the five fields, and a test
      pins the `west_binary` / `build_dir_root` wording specifically rather than only the
      substring the current test checks.
- [x] Decision 20's body reflects the final wording; no fourth posture was introduced.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/api-*` fragment
      dropped.
