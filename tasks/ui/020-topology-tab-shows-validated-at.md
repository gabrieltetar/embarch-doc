# Topology tab should label `confirmed_at` as enrolment time and show `validated_at_utc_ms` alongside it

**State:** blocked
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** ui
**Hardware:** none
**Blocked on:** `tasks/core/026-validate-handler-wires-validated-at.md`, and
then `tasks/api/045` if the UI reads through `embarch-api`'s mirror rather
than calling Core directly. Until Core's handler sends the field there is
nothing for the tab to show.

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
