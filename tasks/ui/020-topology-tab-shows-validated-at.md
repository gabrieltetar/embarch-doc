# Topology tab should label `confirmed_at` as enrolment time and show `validated_at_utc_ms` alongside it

**State:** open
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** ui
**Hardware:** none
**Was blocked on:** `tasks/api/045`, **which landed in leg 043**
(`embarch-api` `c6a5a2d`, doc `782400d`) — unparked by leg 044. The whole chain
below the UI is now in place: Core sends the field (`tasks/core/026`,
`embarch-core` `b0bf60d`, decision 50) and `embarch-api`'s mirror carries it.

**Read the field's shape before you write against it.** `tasks/api/046` (leg
044) changed `ValidateResponse::validated_at_utc_ms` from a required `u64` to
`Option<u64>` with `#[serde(default)]`, so that an `embarch-api` built against
an older Core still parses. **`None` means "this Core did not report it", not
"never validated"**, and the UI must not render an absent value as a date or a
zero. If you find the field is still a bare `u64`, `api/046` did not land as
described — say so rather than working around it.

## What

`embarch-topology` decision 26 adds `validated_at_utc_ms` — when the live
identity check ran — additive alongside the existing `confirmed_at_utc_ms`,
which names enrolment time and does not move on a successful re-validation.
If the Topology tab currently shows `confirmed_at_utc_ms` as-is next to a
green/`ok` validation result, it reads exactly the way `topology/009`
describes the defect: a human sees "confirmed, at this time" and reads it as
freshness, when it can be days stale on a board nobody touched.

Depends on `embarch-core`'s `POST /validate` picking the field up first (a
separate inbox drop) and however the UI's own request path reaches it
(directly, or through `embarch-api`'s mirror).

## Why now

Not urgent — additive, filed so the fix is visible once the field reaches the
UI's input, per the `topology/009` supervisor direction to enumerate every
consumer before the response shape changes.

## Done when

- [ ] The Topology tab shows `validated_at_utc_ms` alongside
      `confirmed_at_utc_ms` where both are present, each labelled for what it
      actually is (enrolled vs. last live-checked), rather than one field
      standing in for both.
