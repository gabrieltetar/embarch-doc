# 079 — `interfaces/modules.md`'s module map has no row for `dev_bench.rs`

**State:** claimed
**Source:** leg 101's refill sweep, 2026-09-12. Verified by reading both sides.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api/src/dev_bench.rs` is a real 186-line module, declared at `src/main.rs:4` (`mod
dev_bench;`), and it owns a distinct responsibility: turning `[dev_bench]` config into a
`resolve::Resolved` so that `build.rs`'s `BuildLocks`/`run_build` and `embarch-core-client`'s
`CoreClient::flash` are reused unchanged — which is what the four tools `build_dev_bench`,
`flash_dev_bench`, `build_and_flash_dev_bench` and `reset_dev_bench` are built on.

`embarch-doc/embarch-api/interfaces/modules.md`'s `| Module | Owns |` table (lines 12–26) has a row
for every other module in the repo — `main.rs`, `config.rs`, `zephyr.rs`, `resolve.rs`, `build.rs`,
`reflash.rs`, `study.rs`, `capacity.rs`, `tools.rs`/`cli.rs`, `logging.rs`, `json_out.rs`, `tests/`,
`crates/embarch-core-client/` — and **no row for `dev_bench.rs`.** The only other absentee is
`lib.rs`, which is the `build.rs` lib target its own row already describes.

That file states its own job at line 7: *"Read it when you need to know where something lives."*

## Why now

The bench-resolution path is the one a reader is most likely to come looking for and least likely to
guess, because it is deliberately **outside** `[[projects]]` — a design choice with its own numbered
decisions rather than an oversight, which is exactly the kind of thing a module map exists to tell
someone before they go hunting through `[[projects]]` for a bench that was never going to be there.

## Done when

- [ ] `interfaces/modules.md` has a `dev_bench.rs` row saying what it owns, and citing the decisions
      that put the bench outside `[[projects]]` (`decisions/dev-bench.md` 32 and 45 — **read both
      bodies and confirm they are the right two** before citing them; do not take this line's word
      for it).
- [ ] This check prints nothing but `lib.rs`, where today it also prints `dev_bench.rs`:
      ```
      for f in embarch-api/src/*.rs; do b=$(basename $f); \
        grep -q "\`$b\`" embarch-doc/embarch-api/interfaces/modules.md || echo "missing $b"; done
      ```
      Run it as a single command, not as a loop you paste in pieces.
- [ ] `embarch-api` `cargo build` / `test` / `clippy --all-targets -- -D warnings` green. This is
      expected to be a docs-only change; if you find yourself editing `src/`, stop and say why in
      your report rather than widening.
- [ ] `changelog.d/` fragment.

**Doc-size note:** `embarch-api` has the deepest compaction backlog in the suite. In reserve and
already filed: `interfaces/config.md` (91.1%, `tasks/api/071`, blocked), `decisions/client-crate.md`
(94.7%, `tasks/api/073`, blocked), `decisions/surface.md` (91.6%, `tasks/api/069`, blocked).
`interfaces/modules.md` itself is **not** in reserve, so one table row is affordable — but check it
against its cap before you write, and if your row pushes it or any other `embarch-api` doc into
reserve, file `tasks/api/NNN-compact-api.md` in the same commit. Your own scope only, never
`tasks/doc/`.
