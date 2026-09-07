# Add `link_port_interface` to `EnrolledBoardResponse`, and pin both unpinned mirrors

**State:** claimed by `agent/api/032-enrolled-board-mirror`, leg 039, 2026-09-07
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

## Supervisor's note, leg 039

**The doc side of this scope is nearly out of room, so plan the doc footprint before you write
it.** Reserve for `api`, measured at this dispatch:

| file | size / cap | headroom | filed against |
|---|---|---|---|
| `embarch-api/decisions/core-link.md` | 12,266 / 12,288 B | **22 B** | `tasks/api/026-compact-api.md` — **blocked** |
| `embarch-api/open.md` | 4,491 / 5,120 B | 629 B | `tasks/api/026-compact-api.md` — **blocked** |
| `embarch-api/decisions/surface.md` | 11,873 / 12,288 B | 415 B | `tasks/api/043-compact-api.md` — **blocked** |
| `embarch-api/spec.md` | 9,087 / 10,240 B | 1,153 B | `tasks/api/026-compact-api.md` — **blocked** |

**22 bytes is not headroom.** If this unit genuinely needs a new numbered decision and
`decisions/core-link.md` is where it belongs, do **a verbatim topic split of that file** — the
move `core/020` made on `embarch-core/interfaces.md` on 2026-09-07 — and not a compaction pass.
`DOC-COMPACTION.md` §3 makes a split the default, and `tasks/api/026`'s `In flux: yes` park
**cannot forbid a split**, because a verbatim split restates nothing and so cannot write a clean
statement of something a first live SSE run is expected to contradict. If you split, update
`tasks/api/026`'s `Compacts:` list to name the new files, and leave its `Must not delete:` list
alone — you are not closing it.

**Prefer not needing one at all.** Pinning a mirror to a type that already exists is arguably
not a decision — it is the *absence* of drift — and a `changelog.d/` fragment plus the
`open.md` bullet the "Done when" already asks for may be the whole doc footprint. Spend the
415-to-629 B you have rather than manufacturing a reason to spend 12 KB of restructuring.

**One stale citation in the task text above, corrected here:** it cites
`embarch-doc/embarch-core/interfaces.md:30` for the `/probes/enrolled` row. That file was split
by `core/020` on 2026-09-07 and the row now lives in
`embarch-doc/embarch-core/interfaces/topology.md`. The `inbox/` drop the task asks you to file
for the `embarch-core` half should name the new path, not the old line number.
