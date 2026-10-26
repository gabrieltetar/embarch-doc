# 104 — The dev-bench identity gate takes `hw_lock`, and `GET /dev-bench/hello` holds `study_lock` while it uses the link

**State:** claimed by agent/core/104-dev-bench-gate-and-hello-take-locks, 2026-10-26 01:20
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-core findings 2 and 7), verified by Opus against embarch-core@40a58ccb
**Scope:** core
**Hardware:** none — lock ordering is host-testable. The collision was found by reading the code; nobody has observed it on the bench.
**Owner:** no

## Dispatch note, 2026-10-26

- **Line numbers above are from `40a58cc`**; `main` has moved since (core/096, 097, 098, 107 landed
  in the last two hours, all in the signal-exchange and flash paths). Re-find each site by name.
- **`embarch-topology` is a path dependency you read but may not edit.** If the gate's attach needs a
  topology change to be lock-aware, stop and say so in the task file rather than reaching across.
- **Doc reserve:** nothing in `embarch-core/` is in reserve. `decisions/platform.md` (decisions
  4/14/15) is 5,927 B, plenty of room. `decisions/surfaces.md` is 11,042 B, **17 B under** its
  11,059 B reserve line (its compaction task `core/091` was retired an hour ago for being under):
  if you must touch it, any growth puts it back in reserve, and then you file
  `tasks/core/<next NNN>-compact-core.md` in the same commit (`scripts/check-task-numbers.py --next
  core`). `decisions/stream-index.md` is 10,986 B, same rule. `spec.md` is 8,937 B against a 9,216 B
  reserve line.
- **Native Windows build** is a debt you record, not a gate item you run (`embarch-fleet/gate.md`).

## What

Two dev-bench entry points skip locks that the rest of Core takes.

- **The identity gate attaches a probe without `hw_lock`.** `enforce_dev_bench_gate` (`embarch-core/src/study.rs:1095-1106` at `40a58cc`) calls `embarch_topology::hardware::validate_role`. That call opens the dev-bench's debug probe and attaches to it (`embarch-topology/src/hardware/validate.rs:325`, `:352`). Neither caller holds `hw_lock` at that point. `POST /study` reaches the gate at `study.rs:1364` and takes the lock only later, inside the outpost pre-flight (`study.rs:1247`). `GET /dev-bench/hello` reaches it at `study.rs:1185` and never takes the lock. So a `/flash`, `/reset`, `/validate`, `/live/mem-read` or `/probes/enroll` on that probe can run during the gate's attach. That puts two owners on one probe, and one side fails for no fault of the bench: a healthy study is refused `502`, or a flash fails partway.
- **Hello checks `study_lock` and then lets go of it.** `hello_handler` checks `study_lock` in a scope that drops it (`study.rs:1166-1174`). It then resolves the port, runs the gate and opens the dev-bench link for the handshake, which can take up to `HANDSHAKE_TIMEOUT_MS` (5 s, `study.rs:68`), all without marking the link busy. A `POST /study` that arrives at any point in that time passes its own `study_lock` check and opens the same serial port. On Windows the second open fails with an opaque `502`. On Linux both opens succeed, and the two handshakes interleave on one wire.

When this is done, no route attaches to a probe without holding `hw_lock`. Hello marks `study_lock` for as long as it holds the link, the way `POST /study` does, so a study that arrives meanwhile is refused `409` naming hello, and the reverse. The worker chooses whether `POST /study` keeps `hw_lock` from the gate through the pre-flight or releases it in between. Either way, the existing pre-flight path must not deadlock.

## Why now

`embarch-core/spec.md` §2 (line 26) says one `hw_lock` serialises all hardware access. `interfaces.md:12` lists every route that opens a physical connection as taking it. The gate's attach is a physical connection that appears in neither place. The collision needs two callers on one bench at the same moment, which is what several agent sessions sharing a bench already produce, and `embarch doctor`'s check 13 calls hello on its own schedule.

**Sequencing:** `tasks/core/099` (bench lease) builds a lease on top of `hw_lock`. Land this one first, so the lease starts from routes that all take the lock, or fold it into 099.

## Done when

- [x] While another route holds `hw_lock`, neither `POST /study` nor `GET /dev-bench/hello` reaches the probe. Both answer the decision-14 `503` naming the holder, shown by a host test that holds the lock.
- [x] While hello holds the dev-bench link, `POST /study` is refused `409` naming it, and hello is still refused `409` while a study is in flight, as today.
- [x] A study with an outpost mode requirement still runs its pre-flight. The existing pre-flight and study tests pass unchanged.
- [x] `interfaces.md`'s lock list and decisions 4/14/15 (`decisions/platform.md`) name the locks that `POST /study`'s gate and `GET /dev-bench/hello` take.
- [x] Follow-up: dropped `inbox/` for umbrella (check 13 now sees `503` from hello when hw_lock is held).
- [x] Gate green (native Windows build not run: debt) (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.

## Result, 2026-10-26

Built in `embarch-core/src/study.rs`: `enforce_dev_bench_gate(state, route)` takes `hw_lock` for the attach and drops it (pre-flight takes it later, no deadlock); hello holds `study_lock` as `GET /dev-bench/hello` via a drop guard. Three host tests added. Decision order: `study_lock` then `hw_lock`. No topology change needed.

**Debts:** native Windows build not run (embarch-core debt, per gate). Hello's `503` path with port resolved is not tested end to end (needs a bench to resolve a port); the gate function is tested directly.
