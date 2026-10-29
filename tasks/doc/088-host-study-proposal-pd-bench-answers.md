# 088 — Bring the host-study proposal's PD bench up to what it became: two shields, its own workspace, the README as its command reference

**State:** done — proposal: owner choice 6 (own workspace, 2026-10-20, cites `tasks/dev-bench/036` until its decision exists), point 5 drift, PD bench section to decision 49 + README; classified `fleet_writable` (fleet `f8c897d`); dev-bench spec/open already current
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the proposal still describes one shield and five `pd` commands while pd-bench has two shields (`embarch-dev-bench` decision 49) and seventeen commands, and its open question on a self-hosted workspace was answered by the owner on 2026-10-20
**Scope:** doc
**Hardware:** none
**Owner:** required — for now. `embarch-host-study-proposal.md` is classified by neither of `check-ownership.py`'s lists (reserved or fleet-writable), and classifying it is the owner's call, not a leg's. Once he adds it to `fleet_writable` this becomes an ordinary supervisor doc unit; set to `required` on filing by the 2026-10-25 leg so no leg writes an unclassified doc on a guess.

## What

`embarch-host-study-proposal.md` is the design that phase 3 (host-run studies) builds from, and three of its PD bench statements are now out of date.

1. **The open question is answered.** "A self-hosted workspace for `pd-bench/` once the USB-C fixes are upstream" was answered on 2026-10-20, before the fixes landed. pd-bench gets its own west workspace in `embarch-dev-bench`, pinning Zephyr v4.4.2 and carrying the six USB-C patches it needs (the pd-bench manifest task, filed with this one). Move it out of Open questions and into the owner's choices.
2. **Point 5 says "the same stack as the DUT".** pd-bench now pins its own copy of the same fixes, so the two can drift. The caveat still holds: a bug common to both ends passes unseen, and key results still need a third-party partner.
3. **The PD bench section** describes the SNK1M1 only and lists five commands. Name both shields and point to `pd-bench/README.md` as the command reference, rather than copying a list that has already gone stale once.

The `Exchange` step's verdict and its prefix-`until` truncation are not this task's concern. A core task (the exchange reads to the end of the matched line) and a study-designer task (whether `Exchange` may declare a refusal marker) cover them, and each updates this file's study model through its own fold.

## Why now

Phase 3 is the next consumer of this file. A phase-3 worker reading it today would build against one shield, a five-command shell and a workspace question that is already closed.

## Done when

- [x] Open questions no longer asks for a self-hosted workspace. The owner's choice is recorded with its date, and points to the `embarch-dev-bench` decision that adds the workspace once that decision exists.
- [x] Point 5 says that pd-bench pins its own copy of the fixes, and keeps the common-bug caveat.
- [x] The PD bench section names both shields, cites decision 49, and points to `pd-bench/README.md` for the shell. It holds no command list.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
