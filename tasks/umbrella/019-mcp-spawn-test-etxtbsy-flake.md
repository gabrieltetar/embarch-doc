# 019 — `a_real_spawn_separates_answering_broken_and_hanging` fails ~1 run in 20 with ETXTBSY

**State:** done — `agent/umbrella/019-etxtbsy-flake`
**Source:** `umbrella/018`'s worker, 2026-09-06, while running the gate. Reproduced 3 times in ~90 `cargo test` runs on `agent/umbrella/018-check-17-evidence`; predates that branch (the test came in with `4e48c77`, and nothing in `018` touches check 10).
**Scope:** umbrella
**Hardware:** none
**Owner:** no

**Reserve, at dispatch (leg 016).** One `embarch-umbrella` file is in the last 10% of its cap:
`embarch-umbrella/decisions/doctor.md`, **11,519 / 12,288 B — 93.7%, 769 B left.** It is filed
against `tasks/umbrella/009-compact-docs.md`, which is `blocked` with `In flux: yes`. Plan
against that number rather than discovering it.

**What that means for you.** This is a test-harness race, not a change in what `doctor`
decides, so it may well warrant no decision at all — a `changelog.d/umbrella-*` fragment and
the code may be the whole of it. Say so if that is your read.

- If you **do not** write `decisions/doctor.md`, you owe nothing extra.
- If you **do** write it, and the write leaves it in reserve, then under `DOC-COMPACTION.md` §2
  you compact that file **as part of this unit** rather than filing a new task — `009` is
  parked and cannot absorb it, and you are the actor making the flux. Carry `009`'s
  `Must not delete:` list verbatim, close only that file's item there, and do not touch
  `spec.md` or `open.md`.
- If your work pushes some *other* umbrella file into reserve and nothing has filed it, file
  `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit (`tasks/README.md` has the
  shape). **Not `tasks/doc/`** — `check-ownership.py` refuses that path to every worker.

**Do not run `cargo fmt`.** No repo in this suite is `rustfmt`-clean and the gate has never
asked; `cargo fmt` here rewrites ~209 files in `embarch-umbrella` alone, all outside your task,
and `check-ownership.py` will not stop you because in a code repo you own the whole tree. The
suite's posture on this is `tasks/suite/006`, announced and parked this leg — until it is
decided, leave formatting alone.

## What

`src/doctor.rs`'s check-10 test writes three `#!/bin/sh` fakes into a tempdir with
`std::fs::write` + `set_permissions(0o755)` and immediately spawns them. Roughly one run in
twenty, the first spawn dies:

```
left: Failed("couldn't start `/tmp/embarch-umbrella-doctor-test-.../answers`: Text file busy (os error 26)")
right: Answered("embarch-api")
```

`cargo test` runs the suite multithreaded. `std::fs::write` closes its own fd, but any
**other** test thread that forks in that window inherits the still-open write descriptor,
and Linux refuses to `exec` a file that some process holds open for writing. The verdict is
the shell script's own text being busy — nothing to do with what the test asserts about
`mcp_initialize`.

It is a genuine red in CI, non-deterministic, and it will be blamed on whichever unrelated
unit happens to be in flight when it lands.

## What to do

Close the write handle deterministically before spawning: write with an explicit `File`,
`sync_all()`, drop it, then set permissions — or, more robustly against the fork race,
retry the spawn on `ETXTBSY` a bounded number of times, or serialise the fake-writing tests
behind a mutex. The retry is the only one that actually beats another thread's inherited fd;
the others narrow the window.

## Done when

- [x] 200 consecutive `cargo test` runs green, or the fix names why the race is closed
      rather than narrowed.
- [x] Gate green; `changelog.d/umbrella-*` fragment dropped.

## What shipped

**The flake is in *two* tests, not one.** Reproducing it took two `cargo test` runs on the
unfixed branch, and the one that failed was check 8's
`a_located_binary_is_actually_spawned_and_its_failures_are_reported` — same shape, same
`ETXTBSY`, never reported. Both are fixed; a report of one flaky spawn test here should be
read as a report of the class.

**Fix: the bounded retry** (`src/doctor.rs`, test module only — no production path changed,
because nothing about what `doctor` decides is wrong). `past_text_file_busy` re-runs a spawn
while its verdict contains `Text file busy`, 50 attempts 20 ms apart, ~1 s ceiling. Both
tests now spawn through a small local closure that wraps the real call
(`api_host_schema_version` for check 8, `mcp_initialize` for check 10).

**Why this closes the race rather than narrowing it.** The write descriptor is not ours by
the time we `exec` — `std::fs::write` closed it. It belongs to a *copy* made by a `fork` in
another test thread, which dies at that child's own `exec` microseconds later. Nothing on
the writing side can shorten a window it does not hold, which is why `File` + `sync_all` +
drop only narrows; retrying outlives the copy by construction.

**What the bound costs, stated.** After 50 attempts the last verdict is returned unchanged,
so a *genuine* `ETXTBSY` — a binary really held open for writing — still fails its assertion
with the same message, up to a second later. It is never masked into a pass and never turned
into a hang. That is asserted, not just described:
`a_text_file_busy_spawn_is_retried_until_it_clears_and_no_further` pins all three arms
(clears, never clears, a non-busy error is not retried at all).

**Evidence:** 200 consecutive `cargo test` runs, 0 failures. Baseline for comparison: the
unfixed tree failed on run 2 of a 60-run loop.

**No `decisions/doctor.md` write, so no compaction owed.** This is a test-harness race; no
decision changed, and `spec.md` / `open.md` say nothing this makes false. The mechanism is
recorded where it is load-bearing — the doc comment on `past_text_file_busy`.
