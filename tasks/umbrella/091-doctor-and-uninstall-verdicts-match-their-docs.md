# 091 — Fix four operator-facing verdicts in `doctor` and `setup --uninstall` that say the wrong thing

**State:** claimed by agent/umbrella/091-doctor-and-uninstall-verdicts-match-their-docs, 2026-10-26 02:57
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-umbrella findings 1, 2, 3 and 4), verified by Opus against embarch-umbrella@1e521166
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## Dispatch note, 2026-10-26 leg

Nothing in `embarch-umbrella/` docs is in reserve (`open.md` was compacted to 3,672 B by
`umbrella/090` an hour ago; keep it under its 3,920 B reserve line or file a compaction task in the
same commit). `umbrella/092` (check 13 reading hello's 503/409 as busy) touches the same check and
is **not** running this leg. The dev-bench CMake fact in finding 3 is context: never edit
`embarch-dev-bench`; a doc fix there is an inbox drop by absolute path to
`/home/gabriel/Github/embarch/embarch-doc/inbox/`. **Never run `setup`, `install`, `uninstall`,
`up` or `down` against the real machine**, and never touch the Windows service or the live Core: the
uninstall exit-code test must drive the step outcomes without a service. Your worktree's parent links
`embarch-topology`, `embarch-study-designer` and `embarch-api`.

## What

Four small defects. In each, what the operator is told contradicts the docs or the machine.

1. **`setup --uninstall` always exits 0.** A failed service uninstall, a failed token removal and a failed install undo are each only printed to stderr. A script chaining `embarch setup --uninstall && …` carries on with Core still installed. Direction: exit 1 when any step it attempted failed, naming each failed step in a final line. `setup`'s own failed-install arm has the same shape; decide both consistently with decision 7's fallback ("print the exact command, exit nonzero").
2. **Check 1 turns a suite-manifest mismatch into a FAIL.** Decision 14 says "a version mismatch against the suite manifest is a warning (decision 24)", and `manifest.rs`'s header says the same. Direction: Warn, with the `manifest-mismatch` code and fix line kept.
3. **Check 13 calls a dirty checkout "stale".** `git describe --dirty` makes a local `X-dirty` that never equals a bench flashed from clean `X`, so any uncommitted change gives `stale` and "rebuild and reflash". Dev-bench's CMake runs `git describe` only at configure time, and an unstaged edit triggers no reconfigure, so an incremental rebuild can leave the FAIL in place. In reverse, `X-dirty` against `X-dirty` passes whatever the two diffs are. Direction: give the dirty case its own code and wording ("the bench matches HEAD; the checkout has uncommitted changes"), with a fix line that would actually clear it. Say what a dirty-against-dirty match does and does not prove.
4. **Check 2's fix line omits `--bind`.** For `wsl-host` and `remote` it prints a bare `install`. Core then defaults to `127.0.0.1`, and check 17 reports exactly that on the next run. Direction: take the bind address from the same `recommended_bind_address` that `setup` uses.

## Why now

- 1: `src/setup.rs:391-429` (returns `0` at :429) and `:297-301`. Contradicts `spec.md:60` ("`1` failure with the message on stderr") and `decisions/topology.md` 7.
- 2: `src/doctor.rs:333-346`; `src/manifest.rs:1-7`; `decisions/install.md` 14. It has been FAIL since it was introduced.
- 3: `src/doctor.rs:2366` and `:2466-2487`; `embarch-dev-bench` `app/CMakeLists.txt:66-69` (at `5282206`): "Doesn't cover the plain-`--dirty` case". `decisions/dev-bench-firmware.md` 19/47 cover the UNC always-dirty case and not this one.
- 4: `src/doctor.rs:458-464`, against `src/setup.rs:258, 267, 279, 292` and check 17's own fixes. `embarch-core` `src/main.rs:37` (at `40a58cc`): `DEFAULT_BIND = "127.0.0.1"`.

**Adjacent:** `tasks/suite/047` adds a doctor check that an installed binary is older than its checkout's `HEAD`. This drop's dirty-checkout half sits in the same part of doctor; whoever lands second rebases on the first.

## Done when

- [x] `setup --uninstall` exits non-zero when a step it attempted failed, and names each one. A run with nothing failed exits 0. Unit-tested over the step outcomes, with no service touched.
- [x] A check-1 manifest mismatch renders as Warn, code `manifest-mismatch`. `doctor`'s exit status for it is the same as for any other Warn.
- [x] Check 13, given a local `X-dirty` and a bench `X`, no longer emits `stale`. It emits its own code, and its fix would clear the result (unit test against a temp git repo, as the existing check-13 tests do). Dirty-against-dirty behaviour is stated in the decision.
- [x] Check 2's fix line for `wsl-host` and `remote` contains the same `--bind` value `setup` passes for that class. A test fails if the two diverge.
- [x] `--json` keeps its always-present `code`/`path` keys for every changed arm.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` and `interfaces/doctor-chain.md` updated, `changelog.d/` fragment dropped.

## Result

All four fixed in `embarch-umbrella` (`src/setup.rs`, `src/doctor.rs`). `setup`'s own failed-install arm now also exits 1. Check 13's dirty case is a Warn, code `dirty-checkout`; dirty-against-dirty stays `match` and decision 19 says what that proves. The `--bind` test calls the same `recommended_bind_address` `setup` uses.

Gate note: `embarch-topology` main (`6732ad6`) does not build without `--features embarch-topology/hardware` (`Upserted` is cfg-gated but re-exported ungated in `hardware/mod.rs`), so the umbrella gate was run with that feature added; reported to inbox.
