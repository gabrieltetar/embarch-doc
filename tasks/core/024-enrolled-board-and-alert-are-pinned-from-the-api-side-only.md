# Pin `EnrolledBoard`/`Alert` in `embarch-core` against `embarch-api`'s new mirror literals

**State:** claimed by agent/core/024-pin-enrolled-board-alert, 2026-09-07 17:30
**Source:** `agent/api/032-enrolled-board-mirror`, leg 039, 2026-09-07 — split off `tasks/api/032-enrolled-board-mirror-drops-link-port-interface.md`, whose "Scope this to the `embarch-api` half only" says the Core half is a second task in a second repo.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-api`'s `embarch-core-client::client::EnrolledBoardResponse` and `AlertResponse` are
hand-maintained mirrors of `embarch_topology::hardware::EnrolledBoard` and `::Alert`
(`embarch-core/src/api.rs:628` serialises the real types verbatim over `GET /probes/enrolled` and
`GET /alerts`). Task `api/032` pinned the `embarch-api` side of that coupling: it added
`link_port_interface: Option<u8>` to the mirror (it had silently dropped the field since
`embarch-topology` decision 20) and added `ENROLLED_BOARD_RESPONSE_JSON`/`ALERT_RESPONSE_JSON`
literals with round-trip tests in `crates/embarch-core-client/src/client.rs` (search
`an_enrolled_board_round_trips_against_the_pinned_shape` and
`an_alert_round_trips_against_the_pinned_shape`).

No test in `embarch-core` or `embarch-topology` pins the real types against those same literals,
so the coupling is only checked from one side — a future field added to `EnrolledBoard` or `Alert`
without a matching client-side change would again typecheck cleanly and fail only against a live
Core. Add a test in `embarch-topology` (or `embarch-core`, wherever `Alert`/`EnrolledBoard` are
most naturally tested) that serializes/deserializes the same JSON shape the two client-side
literals above use, so a future field-level drift fails at `cargo test` on both sides instead of
only one.

Also update the `/probes/enrolled` row in `embarch-doc/embarch-core/interfaces/topology.md`
(**not** `interfaces.md:30` — that file was split by `core/020` on 2026-09-07 into topic files, and
the row now lives in `interfaces/topology.md`) to show `link_port_interface` alongside
`link_port_serial`.

## Why now

`embarch-api/open.md`'s "unfinished couplings" bullet predicted this: "the alert and
enrolled-board response types are unpinned mirrors... nothing typechecks the coupling." It already
fired once (`link_port_interface` silently dropped for a release, `embarch-topology` decision 20).
Pinning only one side halves the risk, not the whole of it.

## Supervisor's note on filing it, leg 039

**Put the test in `embarch-core`, not `embarch-topology`.** The drop offers a choice of repo and a
worker cannot take it: `Scope: core` gives it `embarch-core` and nothing else (`protocol.md` §5
rule 2), and a `core` worker that adds a test file to `embarch-topology` fails
`check-ownership.py` on its own branch. `embarch-core` is where the serialising route lives
(`src/api.rs`'s `GET /probes/enrolled`), so pinning the shape there also pins the thing that
actually goes on the wire, which is the stronger of the two placements anyway. If it turns out the
types genuinely cannot be exercised from `embarch-core`, that is a finding for `inbox/` and a
`topology`-scoped task, not a reach across.

**The doc half is yours too**: `embarch-doc/embarch-core/interfaces/topology.md` is in the `core`
worker's ownership, and the drop already carries the corrected path.

## Doc-size reserve for `core` — supervisor, leg 040

`scripts/check-doc-size.py --pressure` at this leg's start puts one `core` file in reserve:

- `embarch-core/open.md` — **4478/5120 B, 642 B left** (87.5%), filed against
  `tasks/core/022-compact-core.md`, which is **blocked**.

Plan around it: this unit's doc footprint is `embarch-core/interfaces/topology.md` (not in
reserve) plus a `changelog.d/` fragment, so it should not need `open.md` at all. **If your work
does push a file into reserve, or leaves one there that nothing has filed, file
`tasks/core/<NNN>-compact-core.md` in the same commit** (`tasks/README.md` has the shape; the path
is `tasks/core/`, never `tasks/doc/`). You are not being asked to *do* a compaction — only to
record the debt while you still hold the context of whether this subsystem is in flux.

## Done when

- [ ] A test in `embarch-topology` (or `embarch-core`) asserts `EnrolledBoard` and `Alert`
      serialize to / deserialize from the exact JSON literals `embarch-api`'s
      `ENROLLED_BOARD_RESPONSE_JSON` / `ALERT_RESPONSE_JSON` use (or documents why an equivalent
      shared literal differs), with a comment cross-referencing the client-side test by name.
- [ ] `embarch-doc/embarch-core/interfaces/topology.md`'s `/probes/enrolled` row lists
      `link_port_interface`.
- [ ] Gate green.
