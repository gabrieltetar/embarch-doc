# 005 — A truncated build log keeps the tail, and the first error is in the head

**State:** claimed by agent/api/005-build-log-head-and-tail, 2026-09-04 20:13
**Source:** embarch-api/open.md — "**The build-log cap keeps the tail only**, while `spec.md` claimed 'head and tail' from the initial commit until 2026-09-03 — an intent nobody built."
**Scope:** api
**Hardware:** none
**In reserve for this sub-project (supervisor, leg 007):** `embarch-api/open.md` 4821/5120 B — **299 B left**; `embarch-api/decisions/surface.md` 11305/12288 B — **983 B left**. `spec.md` is **not** in reserve any more (the 2026-09-04 compaction pass took it to 8,4xx of 10,240) — leg 006's handoff said it was at 10237/10240 and that is now stale, so you have real room there. Both reserve files are already filed against `tasks/api/007-compact-docs.md`, which is deliberately `blocked`; **do not unblock it**. Closing the `open.md` bullet should free bytes rather than spend them. File `tasks/doc/<NNN>-compact-api.md` in the same commit **only** if you push a third `api` doc into reserve, or leave one there that `api/007` does not name — shape in `tasks/README.md` § "Compaction tasks".

## What

`build::truncate_tail` keeps the last `OUTPUT_CAP_BYTES` (64 KB) of a build's
stdout and stderr behind a marker, cut on a UTF-8 character boundary. A Zephyr
build's *first* error is usually the actionable one, and everything after it is
cascade — so a build that fails early and then produces 64 KB of noise returns a
log with the useful part scrolled off the top.

`open.md` states the fork plainly: **split it, or accept tail-only.** Both are
legitimate answers and this task does not pre-decide which. What it does require
is that the answer stop being accidental:

- If you split it, the marker has to say what was dropped and how much, the cut
  has to stay UTF-8-safe at **both** boundaries, and the total must stay within
  the same cap rather than doubling it.
- If you accept tail-only, say so as a decision with the reason in
  `decisions.md`, and remove the item from `open.md` rather than leaving it
  reading as owed work.

Note that `spec.md` §"Truncation" has **already been corrected** to describe the
built behaviour — it is not lying today. So this is not a doc-repair task; the
doc is honest and the question of which behaviour is right is what is open.

## Why now

It is the third item under `embarch-api/open.md`'s **"Known wrong, not fixed"**,
it is entirely host-side, and `tests/build_capture.rs` already covers drain,
truncation and freshness — so whichever way it goes, the test surface to extend
is in place.

## Done when

- [ ] The truncation behaviour is whatever you decided, and a test pins the
      boundary behaviour of that decision (including the UTF-8 edges if you
      split).
- [ ] `embarch-api/decisions.md` (the right file under `decisions/`) records the
      call and why, and `open.md`'s build-log bullet is closed or rewritten to
      what is genuinely still open.
- [ ] `spec.md`'s truncation paragraph and the `capture cap` row in its table
      match what the code now does. The row is marked `[assumed]` today; if your
      change makes it measured, say so.
- [ ] Gate green (`embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Not in scope

The other two "Known wrong" bullets. The inferred-`board` one in particular is
not this repo's `init`.
