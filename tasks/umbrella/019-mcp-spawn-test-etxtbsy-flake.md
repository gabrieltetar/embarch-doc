# 019 — `a_real_spawn_separates_answering_broken_and_hanging` fails ~1 run in 20 with ETXTBSY

**State:** open
**Source:** `umbrella/018`'s worker, 2026-09-06, while running the gate. Reproduced 3 times in ~90 `cargo test` runs on `agent/umbrella/018-check-17-evidence`; predates that branch (the test came in with `4e48c77`, and nothing in `018` touches check 10).
**Scope:** umbrella
**Hardware:** none
**Owner:** no

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

- [ ] 200 consecutive `cargo test` runs green, or the fix names why the race is closed
      rather than narrowed.
- [ ] Gate green; `changelog.d/umbrella-*` fragment dropped.
