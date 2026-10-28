# 080 — A pure reordering is reported under the wrong part

**State:** done 2026-10-28 (agent/study-designer/080-order-label)
**Dispatch note (supervisor):** no `embarch-study-designer` file is in the size reserve. This is a shared crate; the supervisor reads the diff before merging.
**Source:** `study-designer/079`'s fold (supervisor log, 2026-10-28 15:48, "Least sure about"), the reviewer's note on decision 87: `compare()` files a pure reordering of sources, frames or session variables under part `state`, name `(order)`, so a UI showing it would mislabel which part moved.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`eap_repo::compare` (`src/eap_repo.rs`, behind `eap-parse`) runs `diff_named` over sources, frames, session variables and states by name, and when every part comes back equal but the two `ProtocolDef`s are still unequal it pushes one `Difference { part: "state", name: "(order)", how: Modified }`. That is right about *what* happened (only an order changed, and indices are positional, so it is a real difference) and wrong about *where*: reordering two frames reports a state change. It also catches any other field of `ProtocolDef` that differs while every named part matches, and labels that `state` too.

When this is done, an order-only difference names the part whose order changed (`source`, `frame`, `session variable` or `state`, one `(order)` entry per part that moved), and a difference in no named part and no order is reported under a part that says so rather than borrowing `state`. `Difference::part`'s doc comment lists every value it can now take, since `embarch-ui` is about to show it (`tasks/ui/099`).

## Why now

`embarch-ui` is about to render these differences to a person (`tasks/ui/099`, filed in the same refill). A label that points at the wrong part of a protocol is worse than no label, because the reader goes looking in the wrong place and finds nothing changed there.

## Done when

- [x] Reordering only the frames reports `frame` `(order)`; likewise for sources, session variables and states; tests for each.
- [x] Reordering two parts reports both.
- [x] A `ProtocolDef` differing only outside the four named lists is reported under a part that is not `state` (name the field if it can be named cheaply; otherwise a generic part), with a test.
- [x] `Difference::part`'s doc comment lists every value; decision 87 amended in place (its last sentence describes the old labelling), or a new decision if the change is larger than a correction.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including every CI feature cell this crate runs.
- [x] `spec.md`/`decisions/`/`open.md` updated as needed, `changelog.d/` fragment dropped.
