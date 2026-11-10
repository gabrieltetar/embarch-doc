# 015 — `embarch-chat`'s spec status line says decisions 94–100 are installed

**State:** open
**Source:** Linear issue EMB-68, filed by a session
**Issue:** EMB-68
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`embarch-chat/spec.md`'s **Status:** line (line 3) stops saying decisions 94–100 are "not installed", and says they are installed, with the build they came from.

It reads today: "**Decisions 94–99 built, review round 1's findings fixed, not installed; 67 retired** (`embarch-promptu` build step 3). **Decision 100 built 2026-11-01 13:40** (embarch-chat d95f45d), unreviewed, not installed."

Measured by a session on 2026-11-05: the installed extension's `dist/extension.js` was byte-identical (md5) to the clone's `dist/extension.js`, built 2026-11-04 02:10, after `origin/main`'s then-last commit `2b04ff5` (2026-11-04 00:39). The install time is not recorded anywhere.

## Why now

The status line reads older than what runs, so a reader plans against a stale picture.

## Dispatch notes

- **Doc only.** The `embarch-chat` worktree is there to read; leave it clean and do not push it.
- **Whether decision 100 has been reviewed is the owner's to say, and nobody has said it.** Do not mark it reviewed. Say it is not recorded as reviewed, and drop an `open.md` question if none exists.
- `main` has moved since that measurement (`bce5ac7`, the launcher rework). Write the status as of what `main` holds now, citing the measurement as a dated fact, not as a claim about today's install.
- Edit the line; do not append another status line.

## Done when

- [ ] The status line says decisions 94–100 are installed, with the build they came from and the date that was measured.
- [ ] It says whether decision 100 is recorded as reviewed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
