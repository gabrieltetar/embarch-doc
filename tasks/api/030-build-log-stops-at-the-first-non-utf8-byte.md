# A build log with one non-UTF-8 byte is silently truncated, with no marker

**State:** claimed by agent/api/030-build-log-utf8, 2026-09-08 22:07
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

- [ ] A child emitting `b"error: bad\n\xff\xfe\nerror: the real one\n"` yields **both** `error:`
      lines to the caller.
- [ ] Any lossy substitution or byte drop is visible in the returned text, not silent.
- [ ] The existing cap, head/tail split and UTF-8-boundary tests pass unchanged.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

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
