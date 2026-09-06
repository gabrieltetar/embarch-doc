# Fix the dev-bench README: it names the wrong board and links a deleted doc

**State:** open
**Source:** owner's repo survey, 2026-09-06 — commit `a6d5355` fixed this breakage in `CLAUDE.md` and stopped there
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`README.md:16` calls the nordic workspace "Currently inactive" and `:22` calls the ESP32-C5
"Milestone 2's actual target board" — exactly inverted from `embarch-doc/embarch-dev-bench/spec.md:19`,
"The board, as of 2026-08-31: `nrf54l15dk/nrf54l15/cpuapp` (`workspaces/nordic`)". `README.md:6` and
`:34` point at `embarch-doc/embarch-dev-bench/design.md` and `embarch-core/design.md`, files the
four-file split deleted.

The workspace list should match `spec.md`: nordic is the bench, espressif stays in the tree and
working per decision 43, native_sim is the host build. Doc links resolve to `spec.md`/`decisions.md`
(a decision number addresses the sub-project, not a file, so `decisions.md` is the correct landing
page). The enrolment fact an operator needs and cannot infer — **`link_port_interface = 2`, because
this DK's console is VCOM1** — belongs where the build instructions are.

Doc-only; no build required.

## Why now

This is the first file a new engineer opens, and it currently sends them to build and flash the
board that is *not* on the bench, over links that 404.

## Done when

- [ ] No `design.md` reference remains in `README.md`.
- [ ] The three workspace bullets agree with `spec.md` §1 and §2 on which board is current.
- [ ] The nordic build/flash section is the primary one, and the `link_port_interface = 2` caveat
      appears with it.
- [ ] Every markdown link in the file resolves against the current `embarch-doc` tree.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
