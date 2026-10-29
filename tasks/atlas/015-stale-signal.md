# 015 — Say on every answer when the atlas is behind HEAD

**State:** claimed by agent/atlas/015-stale-signal, 2026-10-29 16:36
**Dispatch note:** `atlas/012` (landed `197784a`, 2026-10-29) just added `pdf=<path>` to the `src:` line of
`part_card` and every `doc_section` answer; your `stale=` goes on the same line, so build on that format rather than
beside it. Line numbers below may predate four other landings today; read the code on `main`. No `embarch-atlas` doc
is in size reserve; the design doc is `DESIGN.md` in the code repo.
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — the atlas was last bumped on 2026-10-08, about 100 commits followed on the firmware's branches, and 587 of 1,358 static answers (43%) came from that atlas with no stale mark in any answer, in the MAP or in `current.json`
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

Staleness is computed only by `status` (`embarch-atlas/src/embarch_atlas/project.py:356` is the only caller of `mark_map`), and DESIGN.md:231-233 relies on "every atlas skill" running `status` as it loads. In the field the `atlas-use` skill loaded 5 times in six weeks, across 37 sessions that used the atlas tools, so the MAP that loads every session never gained its stale line, and `current_atlas()` (`query.py:47`) kept trusting a `current.json` written on 2026-10-08 that still says the old atlas matches HEAD. Make staleness part of every answer: each lookup's `src:` line carries `stale=<reasons> (HEAD <sha12>)` when HEAD is not the atlas's commit or a source changed, computed per call and cached on the mtime of `.git/HEAD` and the current ref, so it costs one `git rev-parse` when HEAD moves and nothing otherwise. The MCP server runs the `status` check when it starts, so the MAP line and `current.json` are right for the session that starts it; `current_atlas()` treats a `current.json` whose commit is not HEAD as no match. Fix the MAP's reference-manual line in the same pass: `update.run` writes the MAP in its first join (`update.py:233`) before `rm_todo` rewrites the worklist for the new atlas (`update.py:234`), and the second join runs only when verdicts were carried (`update.py:236`); a hand-run `build` + `join` never rewrites the worklist at all. `mapgen.worklist()` then skips the worklist as "for another atlas" (`mapgen.py:176`), and the field MAP says "RM chapters in use: not selected yet" while all 168 units of its 14 chapters are frozen.

## Why now

Sessions on branches answered hardware and configuration questions from a twelve-day-old build with nothing telling them so. The cost of saying it is one git call per HEAD move.

## Done when

- [ ] Every lookup's `src:` line names the staleness reasons when there are any; a test moves a fixture repo one commit past its atlas and sees the mark, then rebuilds and sees it go.
- [ ] Per-call cost with an unchanged HEAD is under 5 ms (measured in the test).
- [ ] The MCP server runs the `status` check at start; `current_atlas()` does not take a `current.json` whose commit is not HEAD.
- [ ] After `update`, and after `build` + `join`, the MAP lists the RM chapters of the worklist that applies; a test covers both paths.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
