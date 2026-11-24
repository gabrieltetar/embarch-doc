# 104 — The atlas's live-log lines agree with embarch-api's on image hash, board and when a line is written

**State:** claimed by agent/atlas/104-live-log-lines-agree-with-embarch-api, 2026-11-23 22:05
**Source:** reviewer of `atlas/103` (2026-11-23), reading the atlas's new live-log writer against embarch-api's on `origin/main`
**Issue:** EMB-289
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`atlas/103` made each atlas live tool append one decoded `embarch-live/1` line
(`src/embarch_atlas/livelog.py`). Three fields are filled differently from
embarch-api's writer (`embarch-api`'s `src/live_log.rs`, read only), so a raw
line and its decoded line can disagree about the same call. When this is done:

- **Image hash.** The atlas reads it the way embarch-api does: Core's
  `last_images`, looked up by probe serial and chip, best effort, and
  `"unknown"` only when Core has none. Today the atlas always writes
  `"unknown"`. `notes/hil/05-live.md` says the mirror holds the image hash.
- **When a line is written.** A decoded line is written only when the call
  reached a lease-gated route, as `embarch-api/interfaces/live-log.md` says.
  A call whose Core is unreachable, or whose answer is not JSON, writes no
  decoded line. A call refused before it ran still writes its `did-not-run`
  line.
- **Board.** Taken in embarch-api's order: the request body, then the tool
  arguments, then the answer. Today the atlas takes it from the answer's
  `read` or `state` object.

`embarch-api/interfaces/live-log.md` is `embarch-api`'s doc. Read it; do not
edit it. `api/184` is settling what it leaves unsaid, so if you find another
gap, name it in your report.

## Why now

The engineer reading a Live session back sees the raw line and its decoded
line disagree. The next atlas unit, the measured write-back (`atlas/105`),
reads the image the same way and names the decoded line in its receipt.

**Burndown leg: no new numbered decision.** `embarch-atlas/design.md` and the
repo's `DESIGN.md` "Live" are amended in place. If the work needs a new
decision, stop and say so in this file and in your report.

## Done when

- [ ] With a fake `embarch-api` and a fake Core `status` carrying `last_images`, an atlas line names the same image hash as the raw line.
- [ ] A call whose Core is unreachable writes no decoded line, and a refused call still writes its `did-not-run` line.
- [ ] A test pins `board` to the request's role and probe when the answer names another.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), in the worktree's own venv, with `test_public_guard` running rather than skipped.
- [ ] `embarch-atlas/design.md` and `DESIGN.md` updated where they describe the line, `changelog.d/` fragment dropped.
