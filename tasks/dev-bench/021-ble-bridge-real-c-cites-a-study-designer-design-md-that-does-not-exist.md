# 021 — `ble_bridge_real.c` cites an `embarch-study-designer/design.md §3` that does not exist

**State:** claimed by agent/dev-bench/021-ble-bridge-real-citations, 2026-09-13 10:45
**Source:** split out of `dev-bench/019`, 2026-09-12.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

`embarch-dev-bench/app/src/ble_bridge_real.c` has **39** citations of the dead
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

- [x] `grep -n "design\.md\|milestone-" app/src/ble_bridge_real.c` returns zero.
- [x] Each becomes `` `embarch-study-designer` decision N `` — the cross-repo form settled in
      `api/052` — with N **unchanged** and confirmed resolvable in that repo's `decisions.md`.
- [x] Host-side checks green; say plainly what could and could not be run (the Zephyr
      `tests/unit` ztest suite cannot be built from a worker's worktree — standing debt, not
      introduced here).

## Closed (agent/dev-bench/021-ble-bridge-real-citations, 2026-09-13)

All 39 citations were checked against code context, not blindly reformatted — some cite
`embarch-study-designer`'s `decisions.md`, some cite `embarch-dev-bench`'s own, mixed
throughout and mostly bare (no repo prefix). Two decision numbers are used independently by
both repos for unrelated content: **15** (study-designer's bounded-collection limits vs.
dev-bench's one-connection-at-a-time) and **32** (study-designer's `GattMonitorAll` overflow
vs. dev-bench's advertised-name scan filter) — resolved per-citation by matching the
surrounding comment/code against both repos' `decisions/*.md` prose, not by the number alone.

- **31 of 39** are cross-repo, now `` `embarch-study-designer` decision N ``: 12, 15, 16, 19,
  20, 21, 31, 32, 36, 43, 44, 50, 53, 54, 55, 60 (several repeated). All confirmed resolvable
  in `embarch-study-designer/decisions.md`'s index.
- **8 of 39** are same-repo (`embarch-dev-bench`'s own `design.md` §3, which this repo's own
  `decisions.md` says it had before the split into `decisions/*.md` — decisions.md line 7),
  now bare `decision N` matching the file's existing same-repo convention: 15, 16, 32, 34
  (×4), 37. All confirmed resolvable in `embarch-dev-bench/decisions.md`'s own index.
- **No decision number was changed.**
- **3 of 39 were not decision citations at all** — `design.md §4.3`/`§4.3a`, a bare section
  reference with no decision number and no successor section in the current flat `spec.md`
  (it has no numbered subsections). These don't "resolve" in `decisions.md` because they were
  never decision cites; stripped of `design.md` and left as bare `§4.3`/`§4.3a`, the same
  treatment `dev-bench/019` gave `eap.h`'s `§4.9`. Flagging this rather than inventing an
  attribution for a citation form the task didn't ask this unit to redesign.

**Host-side:** no `Cargo.toml` exists anywhere in `embarch-dev-bench` (documented already in
`decisions/platform.md` decision 9's correction), so `cargo build`/`test`/`clippy` select
nothing in this repo. No `west`/Zephyr toolchain is available in this worker's worktree (the
`workspaces/*` dirs are present but empty of an actual Zephyr checkout) to attempt even a
`native_sim` build — the same standing gap `dev-bench/019` worked under. Comment-only change;
no firmware behaviour altered.

No reserve doc (`open.md`, `spec.md`, `decisions/link.md`) was touched — this unit needed
none of them, as the dispatch note anticipated.

## Dispatch note (leg 105)

**In reserve for `dev-bench`, all three already filed and parked:**
`embarch-dev-bench/open.md` 4782/5120 (338 B left, `tasks/dev-bench/012`, blocked),
`embarch-dev-bench/spec.md` 9460/10240 (780 B left, same task, blocked),
`embarch-dev-bench/decisions/link.md` 11241/12288 (1047 B left, `tasks/dev-bench/014`,
blocked). Plan your doc writes around those headrooms — this unit should need none of them,
since it is a C-comment citation repoint with a `changelog.d/` fragment. If you do spend
reserve in a file nothing has filed, file `tasks/dev-bench/<NNN>-compact-dev-bench.md` in the
same commit.
