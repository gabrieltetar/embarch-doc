# Add `link_port_interface` to `EnrolledBoardResponse`, and pin both unpinned mirrors

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/open.md`'s "unfinished couplings" bullet, which has now fired
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client/src/client.rs:293-303` mirrors `embarch_topology::hardware::EnrolledBoard`
but stops at `link_port_serial`. The real type carries a further `link_port_interface: Option<u8>`
(`embarch-topology/src/hardware/enrollment.rs`), which Core serialises verbatim from
`GET /probes/enrolled` (`embarch-core/src/api.rs:628`). The mirror silently drops it.

`EnrolledBoardResponse` gains the field with `#[serde(default)]`, matching the real type field for
field. `AlertResponse` and `EnrolledBoardResponse` each get a `const …_JSON` literal and a
round-trip test in the same shape `SIGNAL_LINK_JSON` already uses (`client.rs:1600-1620`), with a
comment naming the Core-side half that still needs writing.

**Scope this to the `embarch-api` half only.** Pinning both mirrors "from each side" needs a
matching test in `embarch-core`, and `embarch-doc/embarch-core/interfaces.md:30`'s
`/probes/enrolled` row also omits the field — that is a second task in a second repo, and a
worker must not reach across (`../../embarch-fleet/protocol.md` §5 rule 2). Drop it in `inbox/`.

## Why now

`embarch-api/open.md:13` predicted this exactly — "The alert and enrolled-board response types are
unpinned mirrors. No crate compiles both sides, so nothing typechecks the coupling." The failure it
names as hypothetical has already happened: the field was added after a real debugging cycle (the
nRF54L15DK two-VCOM case, `embarch-topology` decision 20), and the one client every UI reads
enrolment through cannot see it.

## Done when

- [ ] `EnrolledBoardResponse` deserialises a `GET /probes/enrolled` body carrying
      `link_port_interface` and preserves it.
- [ ] One JSON literal per mirror with a round-trip test asserting both directions, and a comment
      naming the Core-side counterpart test that does not exist yet.
- [ ] A body with the field absent still parses (an older Core), asserted.
- [ ] `embarch-doc/embarch-api/open.md`'s bullet records that the drift happened and that the api
      half is now pinned.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
