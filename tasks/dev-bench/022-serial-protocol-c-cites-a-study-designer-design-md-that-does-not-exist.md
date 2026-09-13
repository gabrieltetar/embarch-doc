# 022 — Four `embarch-dev-bench` C files cite an `embarch-study-designer/design.md §3` that does not exist

**State:** claimed by agent/dev-bench/022-dead-design-md-citations, 2026-09-13 11:50
**Source:** split out of `dev-bench/019`, 2026-09-12. **Re-scoped by leg 106, 2026-09-13** to cover
all four remaining files in one pass rather than four — see "Why one task, not four" below.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## What

Four files in `embarch-dev-bench` carry **122** citations of the dead
`embarch-study-designer/design.md §3` filename between them. Counts re-verified on `main` by the
supervisor at 2026-09-13 11:48 with `grep -c 'design\.md\|milestone-'`:

| file | citations |
|---|---|
| `app/src/serial_protocol.c` | 37 |
| `app/src/main.c` | 36 |
| `app/tests/serial_protocol/src/main.c` | 28 |
| `app/src/ble_bridge.h` | 21 |

Same defect class as `dev-bench/019` (`eap.h`/`eap_interp.h`/`eap_interp.c`), `dev-bench/020`,
`dev-bench/021`, `ui/033`/`ui/039` and `core/008`. `019` confirmed only that the filename is dead
and the counts, by mechanical grep — **the per-hit decision numbers have not been checked** against
`embarch-study-designer`'s `decisions.md` index. Across the four files the distinct numbers cited
are 6, 7, 10, 11, 12, 16, 18, 20, 21, 24, 27, 29, 35, 36, 37, 38, 39, 42, 43, 44, 47, 53, 54, 55,
58, 60, 61, 62 — 28 of them, so resolving the set costs one read of that index, not 122 lookups.

**A number that does not resolve is not yours to renumber.** Leave that citation alone, say so
plainly in your report, and drop a finding to `/home/gabriel/Github/embarch/embarch-doc/inbox/`
(absolute path). `dev-bench/020` and `outpost/019` both found a minority of hits that were *not*
instances of the defect and left them; that discrimination is the value of the unit, and a blind
`sed` over the whole file destroys it.

**One path in the old task files was wrong.** Retired `dev-bench/025` named
`tests/serial_protocol/src/main.c`; the file is at `app/tests/serial_protocol/src/main.c`. Its
`Done when` grep would therefore have returned zero against a path that does not exist — a
checkbox passing for the wrong reason. Use the table above, not the old paths.

## Why one task, not four

`022`, `023`, `024` and `025` were four task files describing one mechanical sweep over four files
in one repo. One-task-per-sub-project is **per slot**, so they could never run concurrently: four
tasks meant four legs each spending a unit — worker, gate, fold, reviewer — on ~30 citations of the
same transformation. The expensive half is resolving the 28 distinct decision numbers, which is
paid once whether the sweep covers one file or four. `023`, `024` and `025` are therefore
`blocked` on this task rather than dispatchable; whatever this unit does not cover unparks them.

## Why now

No gate can see it: `check-decision-refs.py` resolves decision numbers in `*.md` under a repo root
only, and these are C comments. The filename it points at was deleted, so every one of the 122 is a
citation into nothing.

## Done when

- [ ] `grep -rn 'design\.md\|milestone-' app/src/serial_protocol.c app/src/main.c
      app/src/ble_bridge.h app/tests/serial_protocol/src/main.c` returns zero, **or** returns only
      hits you deliberately left, each named in your report with the reason.
- [ ] Each rewritten hit becomes `` `embarch-study-designer` decision N `` — the cross-repo form
      settled in `api/052` — with **N unchanged** and confirmed resolvable in that repo's
      `decisions.md`.
- [ ] Any number that does not resolve is left in place, reported, and dropped to `inbox/`.
- [ ] If you cannot finish all four files, say which you completed: the three retired task files
      are `blocked` on this one and the supervisor unparks the remainder from your report.
- [ ] Host-side checks green; say plainly what could and could not be run (the Zephyr `tests/unit`
      ztest suite cannot be built from a worker's worktree — standing debt, not introduced here).
- [ ] `changelog.d/` fragment.

## Do not

Do not change a decision number, do not reflow surrounding comment prose, and do not touch any file
outside the four in the table.
