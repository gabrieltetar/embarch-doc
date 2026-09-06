# A build log with one non-UTF-8 byte is silently truncated, with no marker

**State:** open
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
