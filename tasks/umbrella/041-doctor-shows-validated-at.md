# doctor's board-validation check should show `validated_at_utc_ms` when it's available

**State:** open
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** umbrella
**Hardware:** none
**Was blocked on:** `tasks/api/045`, **which landed in leg 043**
(`embarch-api` `c6a5a2d`, doc `782400d`) — unparked by leg 044. The whole chain
below `doctor` is now in place: Core sends the field (`tasks/core/026`,
`embarch-core` `b0bf60d`, decision 50) and `embarch-api`'s mirror carries it.
You still owe the read-path check the original block asked for — say whether
`doctor` reads Core directly or through the mirror, because it decides which
shape you are handling.

**Read the field's shape before you write against it.** `tasks/api/046` (leg
044) changed `ValidateResponse::validated_at_utc_ms` from a required `u64` to
`Option<u64>` with `#[serde(default)]`, so that an `embarch-api` built against
an older Core still parses. **`None` means "this Core did not report it", not
"never validated"** — and for a `doctor` check that distinction is the whole
point, since a check that prints "never validated" for a version skew is
exactly the misleading verdict `umbrella/032` was about. If you find the field
is still a bare `u64`, `api/046` did not land as described — say so rather than
working around it.

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
