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

- [x] `grep -rn 'design\.md\|milestone-' app/src/serial_protocol.c app/src/main.c
      app/src/ble_bridge.h app/tests/serial_protocol/src/main.c` returns zero, **or** returns only
      hits you deliberately left, each named in your report with the reason.
- [x] Each rewritten hit becomes `` `embarch-study-designer` decision N `` — the cross-repo form
      settled in `api/052` — with **N unchanged** and confirmed resolvable in that repo's
      `decisions.md`.
- [x] Any number that does not resolve is left in place, reported, and dropped to `inbox/`.
- [x] If you cannot finish all four files, say which you completed: the three retired task files
      are `blocked` on this one and the supervisor unparks the remainder from your report.
- [x] Host-side checks green; say plainly what could and could not be run (the Zephyr `tests/unit`
      ztest suite cannot be built from a worker's worktree — standing debt, not introduced here).
- [x] `changelog.d/` fragment.

## Closed

All four files done in one pass, all 122 citations, zero left. Every one of the 122 grep hits
was read in context (not `sed`ed blind) and resolved to one of three repos:

- **~89 `embarch-study-designer`'s** — the `.eap` protocol manifest (decisions 58-62), the
  stream-schema-v8 generalization (decision 39, distinguished per hit from dev-bench's own
  same-numbered decision — see below), COBS (10), GATT discovery/monitor (31/32/36/53),
  BLE naming/security/unbond (43/44/50), schema fields (42/47/58/62/54), and more.
- **~19 `embarch-dev-bench`'s own** — the file-header decision lists, the `LogLine` channel
  (7), the generic inbound-pipeline/declared-taps mechanism (29(a)), two real SRAM-overflow
  findings (27), the `ble_bridge_real`/`_stub` split and native_sim testing philosophy (16),
  real per-`Study` dispatch (21), and study-scoped bonding (11/37).
- **3 `embarch-core`'s own** — the hardware-ID handshake (35) and the log-destination/ack-race
  handshake (37).

**Why not just decode by number.** `embarch-study-designer`'s and `embarch-dev-bench`'s own
decision ranges overlap for every number ≤ 46 (`embarch-dev-bench`'s own decisions run 1–46
with no gaps), so a bare `design.md §3 decision 39` could be either repo's real decision 39
until its paragraph is read: the stream-schema-v8 refactor is study-designer's; a
`dev_bench_log_level` field is dev-bench's own, same number, unrelated topic. Six citations
of decision 39 turned out to be dev-bench's own on that basis; the rest were study-designer's.
Decision 18 similarly exists in both `embarch-study-designer` (Core validates a submitted
`Study` structurally) and `embarch-dev-bench` (`HelloAck` carries a firmware-identity string)
— the one bare citation of it (`serial_protocol.c`) matched the former by content.

**Two source citations turned out to name the wrong repo outright, not just be bare/ambiguous**
(caught by content, not by number): `app/tests/serial_protocol/src/main.c`'s `---- GATT
transcript (embarch-dev-bench decision 36)` header cited dev-bench's own decision 36 (chip-ID
`HelloAck` reporting) for a section that is unmistakably about the GATT-transcript streamed-
pinning mechanism `embarch-study-designer`'s decision 36 describes verbatim, elsewhere in the
same file, in the same words. And `main.c`'s `RunProtocol`-index pre-flight-check comment cited
`` `embarch-core/design.md` §3 decision 18 `` for the exact same "Core validates a submitted
`Study` before touching the link" concept `serial_protocol.c` cites bare as decision 18 and
resolves to `embarch-study-designer`; `embarch-core`'s own decision 18 is about flashing
(`Format::Bin` at the merge address) and does not fit. Both repointed to
`embarch-study-designer` decision 36/18 respectively, per content, with **N unchanged** in both
cases. Flagged here rather than silently fixed since it changes which repo a reader would
open.

**A handful of citations (11) carried no decision number at all** — a bare `design.md §4.8`/
`§4.3a`/`§4.5`/`§4`/`§1` section pointer, the file's dead narrative sections rather than one of
its permanent decision numbers. These are stripped of the dead `design.md`/repo-prefix text
(so the grep gate is clean) and left as a bare section number, the same treatment
`dev-bench/020`'s `serial_protocol.h` fold already applied to the same pattern — not a decision
citation, so nothing to resolve or drop to `inbox/`.

**All resolved numbers confirmed against their cited repo's `decisions.md` index before
rewriting** (`embarch-study-designer`'s and `embarch-dev-bench`'s own read in full; `embarch-core`'s
checked for the three numbers actually cited). **None were unresolvable** — nothing dropped to
`inbox/`.

Comment-only change; no firmware behaviour altered. Verified: `grep` gate zero across all four
files; `/*`…`*/` comment-block balance unchanged per file; no line introduced over 100 columns.
**Could not run:** this worker's sandbox has no `west` binary and no Zephyr SDK/toolchain
reachable (checked), so neither a `native_sim` build nor the `app/tests/serial_protocol` ztest
suite could be built — standing debt per `dev-bench/019`/`020`, not introduced or worsened
here. No Rust/`cargo` project exists in this repo (`embarch-dev-bench` is C/Zephyr only), so
`cargo build`/`test`/`clippy` do not apply.

Code: `embarch-dev-bench` branch `agent/dev-bench/022-dead-design-md-citations`, pushed.

## Do not

Do not change a decision number, do not reflow surrounding comment prose, and do not touch any file
outside the four in the table.
