# Topology tab should label `confirmed_at` as enrolment time and show `validated_at_utc_ms` alongside it

**State:** blocked
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** ui
**Hardware:** none
**Blocked on:** `tasks/api/045`. The Core half landed in leg 042
(`tasks/core/026`, `embarch-core` `b0bf60d`, decision 50), so the field is on
the wire; what is still missing is `embarch-api`'s mirror, which is how the UI
reads it. **If whoever takes this finds the UI calls Core directly rather than
through that mirror, this is unblocked now** — check the read path before
assuming the dependency, and say which it was.

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
