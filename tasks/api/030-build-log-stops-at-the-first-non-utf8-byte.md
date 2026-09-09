# A build log with one non-UTF-8 byte is silently truncated, with no marker

**State:** done
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/spec.md` §2 and §3 both promise what this breaks
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`src/build.rs:191-199` drains a child's output with
`while let Ok(Some(line)) = lines.next_line().await`, which treats a decode error identically to
end-of-stream. `tokio` returns `InvalidData` on a non-UTF-8 byte, so the drain ends there and
everything after it is dropped — no error, no marker, and worst on exactly the failing builds this
surface exists for. `tests/build_capture.rs` covers the cap, both boundaries and the two-pipe
drain, and has no invalid-UTF-8 case.

Draining should read bytes and decode lossily (or report the decode failure inline), so a toolchain
emitting a latin-1 path or a stray control byte no longer costs the rest of the compiler output.
If any bytes are dropped or substituted, the capture says so, in the marker style truncation
already uses.

## Why now

`spec.md` §2 promises "**An expected failure comes back as tool content** … so a calling agent sees
the real compiler error", and §3 promises truncation is always marked. A silent mid-log stop breaks
both, and an agent reading the capture cannot tell it happened.

## Done when

- [x] A child emitting `b"error: bad\n\xff\xfe\nerror: the real one\n"` yields **both** `error:`
      lines to the caller. Pinned by
      `a_non_utf8_byte_does_not_truncate_the_rest_of_the_log` in
      `tests/build_capture.rs`, through a real child process.
- [x] Any lossy substitution or byte drop is visible in the returned text, not silent. Every
      line that fails `String::from_utf8` is decoded with `from_utf8_lossy` and named (by line
      number) in a summary marker appended to the capture.
- [x] The existing cap, head/tail split and UTF-8-boundary tests pass unchanged — all 19
      `build_capture.rs` tests pass (18 pre-existing + the 1 new one above).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` all clean in the code worktree;
      `scripts/check-docs.py` all 10 green in the doc worktree.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. `spec.md` §3's Capture bullet and
      decision 18 (`decisions/build.md`) amended; `open.md`'s decision-corpus-headroom note
      updated to record `build.md` crossing the reserve line. No suite-level doc's facts were
      made false by this fix (no `status.d/` fragment). No new numbered decision was authored,
      per the burndown-mode constraint — this is an amendment to existing decision 18, not a
      new design call.

## Shipped, `agent/api/030-build-log-utf8`, 2026-09-08

**What changed:** `src/build.rs`'s `drain_stream` used to read each line via
`AsyncBufReadExt::lines()`/`next_line()`, which decodes UTF-8 per line and returns
`Err(InvalidData)` on the first non-UTF-8 byte — and the old
`while let Ok(Some(line)) = lines.next_line().await` treated that identically to a clean
end-of-stream, silently dropping everything the child wrote afterward. Rewrote it to read raw
bytes via `read_until(b'\n', ..)` (which has no decode step to fail), decode each line with
`String::from_utf8`, and fall back to `from_utf8_lossy` only for the one line that actually
fails. Every line needing the lossy fallback is named, by line number, in a summary marker
appended to the end of the capture — visible rather than silently wrong.

**One byproduct worth naming:** the amendment to decision 18 pushed
`embarch-api/decisions/build.md` from 10,934 B to 11,134 B, past the 11,059 B reserve line
(90.6% of its 12,288 B cap). Filed `tasks/api/050-compact-api.md` for it in the same commit,
`In flux: yes` (this file's log-capture mission has now been revisited for correctness twice),
per `DOC-COMPACTION.md` §2.

**Left undone / unsure about:** none on the code side — the fix is small, targeted, and every
`Done when` box above is checked with a real test. On the doc side, `tasks/api/050-compact-api.md`
is a new *compaction* task (not a decision), which the burndown-mode note does not restrict;
flagging it here in case that reading is wrong. `decisions/build.md` now carries its own
`### 18` amendment rather than a fresh numbered entry — if the supervisor's read is that this
change is architecturally distinct enough to deserve its own number, that is a call I deliberately
did not make under the burndown constraint.

## Supervisor's dispatch note, leg 053 (2026-09-08, burndown)

**This leg runs in burndown mode, which adds one constraint to your unit: do not author a new
numbered decision.** Implement, document and fix freely; if you conclude this change genuinely
needs a new numbered decision in `embarch-api/decisions/`, **stop and say so in your report**
instead, and leave the task file with a state line explaining what the decision would say. A
decision is the most expensive thing in this suite to reverse and burndown is the mode explicitly
optimising for volume. Amending or correcting an *existing* decision is fine and is not this rule.

**Doc-size reserve for `api` — every one of these is inside the last 10% of its cap:**

| file | size/cap | headroom | filed against |
|---|---|---|---|
| `embarch-api/decisions/tool-wrapping.md` | 12222/12288 | **66 B** | `tasks/api/047-compact-api.md` (blocked, `In flux: yes`) |
| `embarch-api/decisions/core-link.md` | 12076/12288 | 212 B | `tasks/api/026-compact-api.md` (blocked, `In flux: yes`) |
| `embarch-api/open.md` | 4734/5120 | 386 B | `tasks/api/026-compact-api.md` (blocked) |
| `embarch-api/spec.md` | 9087/10240 | 1153 B | `tasks/api/026-compact-api.md` (blocked) |

Plan around this rather than discovering it. Two rules follow:

1. **If your work spends the reserve** — pushes a file into it, or leaves one there that nothing has
   filed — file `tasks/api/<NNN>-compact-api.md` in the same commit, per `tasks/README.md`. Use
   `python3 scripts/check-task-numbers.py --next api` for the number; do not read the directory.
2. **Both parked compaction tasks are blocked on `In flux: yes`, which parks the pass and not the
   reserve.** If an edit of yours would push one of those files *past* its cap, you compact that
   file as part of this unit — read the parked task's `Must not delete:` list first and carry it
   verbatim, closing only that file's item. You are the actor making the flux, so you are the only
   one who can shorten what you are rewriting. Otherwise aim net-neutral.
