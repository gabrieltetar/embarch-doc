# doctor's board-validation check should show `validated_at_utc_ms` when it's available

**State:** blocked
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** umbrella
**Hardware:** none
**Blocked on:** `tasks/core/026-validate-handler-wires-validated-at.md`, and
then `tasks/api/045` if `doctor` reads through `embarch-api`'s mirror. Until
Core's handler sends the field there is nothing for the check to report.

## What

`embarch-topology` decision 26 adds `validated_at_utc_ms` — when the live
identity check ran — alongside the existing `confirmed_at_utc_ms`, which is
enrolment time and can be days stale on a passing check. `doctor`'s board
check is exactly the "how stale is this?" reader `topology/009` names as the
one most likely to misread the old field, and ranking two boards' freshness
against each other on `confirmed_at_utc_ms` alone is the specific failure
observed (two roles, both `ok: true`, timestamps six days apart).

Depends on `embarch-core`'s `POST /validate` picking the field up first (a
separate inbox drop) and `embarch-api`'s mirror carrying it through, if
`doctor` reads through that layer rather than calling topology directly.

## Why now

Not urgent — additive, filed so the fix is visible once the field reaches
`doctor`'s input, per the `topology/009` supervisor direction to enumerate
every consumer before the response shape changes.

## Done when

- [ ] `doctor`'s validation check reports `validated_at_utc_ms` where present,
      and does not present `confirmed_at_utc_ms` alone as a freshness answer.
