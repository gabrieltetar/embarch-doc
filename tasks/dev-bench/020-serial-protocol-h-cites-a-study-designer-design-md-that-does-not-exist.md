# 020 — `serial_protocol.h` cites an `embarch-study-designer/design.md §3` that does not exist

**State:** open
**Source:** split out of `dev-bench/019`, 2026-09-12.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`embarch-dev-bench/app/src/serial_protocol.h` has **48** citations of the dead
`embarch-study-designer/design.md §3` filename (same defect class as `dev-bench/019`,
which fixed `eap.h`/`eap_interp.h`/`eap_interp.c`). `019` confirmed only the filename is
dead and the counts, by mechanical grep — **the per-hit decision numbers in this file have
not been checked** against `embarch-study-designer`'s `decisions.md` index. Say so again in
whatever unit picks this up if any number turns out not to resolve.

## Why now

Same defect class cleared out of `embarch-ui` by `ui/033`/`ui/039`, out of `embarch-core` by
`core/008`, and out of the `.eap` trio by `dev-bench/019`. No gate can see it:
`check-decision-refs.py` resolves decision numbers in `*.md` under a repo root only, and
these are C comments.

## Done when

- [ ] `grep -n "design\.md\|milestone-" app/src/serial_protocol.h` returns zero.
- [ ] Each becomes `` `embarch-study-designer` decision N `` — the cross-repo form settled in
      `api/052` — with N **unchanged** and confirmed resolvable in that repo's `decisions.md`.
- [ ] Host-side checks green; say plainly what could and could not be run (the Zephyr
      `tests/unit` ztest suite cannot be built from a worker's worktree — standing debt, not
      introduced here).
